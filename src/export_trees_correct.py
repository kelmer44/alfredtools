#!/usr/bin/env python3
"""
Export Conversation Trees - Correctly Handling Choice vs Auto-dialogue
=======================================================================

The key insight: If a choice index appears multiple times, it's an actual
player choice menu. If it appears only once, it's automatic dialogue continuation.

Usage:
    python3 export_trees_correct.py [room_number]
    python3 export_trees_correct.py --all
"""

import struct
import sys
from pathlib import Path
from collections import Counter

def read_room_pair(data, room_num, pair_num):
    """Read a specific pair from a room"""
    room_offset = room_num * 104
    pair_offset_pos = room_offset + (pair_num * 8)
    offset = struct.unpack('<I', data[pair_offset_pos:pair_offset_pos+4])[0]
    size = struct.unpack('<I', data[pair_offset_pos+4:pair_offset_pos+8])[0]

    if size == 0 or offset >= len(data):
        return None

    return data[offset:offset+size]

def decode_byte(b):
    """Decode a byte to character"""
    special = {
        0x80: 'ñ', 0x81: 'í', 0x82: '¡', 0x83: '¿', 0x84: 'ú',
        0x7B: 'á', 0x7C: 'é', 0x7D: 'í', 0x7E: 'ó', 0x7F: 'ú',
    }

    if b in special:
        return special[b]
    elif 0x20 <= b <= 0x7A:
        return chr(b)
    else:
        return None

def extract_descriptions(data):
    """Extract sprite/hotspot descriptions"""
    descriptions = []
    pos = 0
    last_desc_pos = 0

    while pos < len(data):
        if data[pos] == 0xFF:
            pos += 1
            if pos >= len(data):
                break

            pos += 4  # Skip item_id and 2 bytes and index
            if pos >= len(data):
                break

            text = ""
            while pos < len(data) and data[pos] != 0xFD:
                char = decode_byte(data[pos])
                if char:
                    text += char
                pos += 1

            descriptions.append(text)
            last_desc_pos = pos

            if pos < len(data) and data[pos] == 0xFD:
                pos += 1
        else:
            pos += 1

    return descriptions, last_desc_pos + 1

def clean_text(text):
    """Clean control sequences from text"""
    text = text.strip()

    # Remove leading [XX][00] patterns
    while text and '[' in text[:15]:
        idx = text.find('[')
        if idx >= 0 and idx < 10:
            end_idx = text.find(']', idx)
            if end_idx > idx and end_idx < idx + 10:
                text = text[end_idx+1:].lstrip()
            else:
                break
        else:
            break

    # Remove single leading control characters
    if len(text) > 1 and text[0] in 'AH' and (text[1].isupper() or text[1] in '¿¡['):
        text = text[1:].lstrip()
    elif len(text) > 1 and text[0] in '#%\')!+,.-"*&$(/':
        text = text[1:].lstrip()

    return text.strip()

def parse_elements_with_indices(conv_data):
    """Parse conversation and track choice indices"""
    elements = []
    choice_indices = []  # Track all choice indices
    pos = 0

    while pos < len(conv_data):
        b = conv_data[pos]

        if b == 0x08:  # SPEAKER
            pos += 1
            if pos < len(conv_data):
                speaker_id = conv_data[pos]
                speaker = 'ALFRED' if speaker_id == 0x0D else 'NPC'
                pos += 1

                # Read text
                text = ""
                while pos < len(conv_data) and conv_data[pos] not in [0x08, 0xFB, 0xF1, 0xF8, 0xFD, 0xFC, 0xF4, 0xF7, 0xF5, 0xFE, 0xEB, 0xF0]:
                    char = decode_byte(conv_data[pos])
                    if char:
                        text += char
                    pos += 1

                text = clean_text(text)
                if text:
                    elements.append({'type': 'dialogue', 'speaker': speaker, 'text': text, 'choice_index': None})

        elif b in [0xFB, 0xF1]:  # CHOICE marker
            pos += 1
            choice_index = None
            if pos < len(conv_data):
                choice_index = conv_data[pos]
                choice_indices.append(choice_index)
                pos += 1

            # Skip next 2 bytes (speaker marker)
            if pos < len(conv_data):
                pos += 1
            if pos < len(conv_data):
                pos += 1

            # Read text
            text = ""
            while pos < len(conv_data) and conv_data[pos] not in [0x08, 0xFB, 0xF1, 0xF8, 0xFD, 0xFC, 0xF4, 0xF7, 0xF5, 0xFE, 0xEB, 0xF0]:
                char = decode_byte(conv_data[pos])
                if char:
                    text += char
                pos += 1

            text = clean_text(text)
            if text:
                elements.append({'type': 'choice_marker', 'text': text, 'choice_index': choice_index})

        elif b == 0xF8:  # ACTION
            pos += 3

        elif b == 0xF4:  # END_CONV
            elements.append({'type': 'end_conv'})
            pos += 1

        elif b == 0xF7:  # END_BRANCH
            elements.append({'type': 'end_branch'})
            pos += 1

        elif b in [0xFD, 0xFC, 0xF5, 0xFE, 0xEB, 0xF0]:
            pos += 1

        else:
            pos += 1

    # Count occurrences of each choice index
    index_counts = Counter(choice_indices)

    # Mark which indices are actual choices (appear multiple times)
    for elem in elements:
        if elem.get('choice_index') is not None:
            elem['is_real_choice'] = index_counts[elem['choice_index']] > 1

    return elements, index_counts

def build_tree_structure(elements):
    """Build tree using proper choice detection"""
    roots = []
    stack = []
    current_root = None
    i = 0

    while i < len(elements):
        elem = elements[i]

        if elem['type'] == 'dialogue' and elem['speaker'] == 'NPC':
            if not stack:
                # New root conversation
                current_root = {'type': 'root', 'text': elem['text'], 'choices': []}
                roots.append(current_root)
            else:
                # NPC response within a branch
                parent = stack[-1]['node']
                parent.setdefault('responses', []).append({'speaker': 'NPC', 'text': elem['text']})
            i += 1

        elif elem['type'] == 'choice_marker':
            if elem.get('is_real_choice'):
                # Real choice - player selects from menu
                choice_node = {
                    'type': 'choice',
                    'text': elem['text'],
                    'choice_index': elem['choice_index'],
                    'responses': [],
                    'subchoices': []
                }

                # Find where to attach this choice
                while stack and stack[-1]['index'] >= elem['choice_index']:
                    stack.pop()

                if stack:
                    parent = stack[-1]['node']
                    parent['subchoices'].append(choice_node)
                else:
                    current_root['choices'].append(choice_node)

                stack.append({'node': choice_node, 'index': elem['choice_index']})
            else:
                # Auto-dialogue - ALFRED just speaks
                if stack:
                    parent = stack[-1]['node']
                    parent.setdefault('responses', []).append({'speaker': 'ALFRED', 'text': elem['text']})
            i += 1

        elif elem['type'] == 'dialogue' and elem['speaker'] == 'ALFRED':
            if stack:
                parent = stack[-1]['node']
                parent.setdefault('responses', []).append({'speaker': 'ALFRED', 'text': elem['text']})
            i += 1

        elif elem['type'] == 'end_conv':
            if stack:
                stack[-1]['node']['terminated'] = True
                stack.pop()
            i += 1

        elif elem['type'] == 'end_branch':
            stack = []
            current_root = None
            i += 1

        else:
            i += 1

    return roots

def format_tree_output(roots, output_lines=None):
    """Format tree with proper indentation"""
    if output_lines is None:
        output_lines = []

    for root in roots:
        output_lines.append(f"NPC: {root['text']}")

        for choice_idx, choice in enumerate(root['choices'], 1):
            format_choice(choice, choice_idx, 1, output_lines)

    return output_lines

def format_choice(choice, choice_num, indent_level, output_lines):
    """Recursively format a choice"""
    indent = "    " * indent_level

    output_lines.append(f"{indent}CHOICE {choice_num}: {choice['text']}")
    output_lines.append(f"{indent}    ALFRED: {choice['text']}")

    for response in choice.get('responses', []):
        output_lines.append(f"{indent}    {response['speaker']}: {response['text']}")

    for sub_idx, subchoice in enumerate(choice.get('subchoices', []), 1):
        format_choice(subchoice, sub_idx, indent_level + 1, output_lines)

    if choice.get('terminated'):
        output_lines.append(f"{indent}    TERMINATES CONVERSATION AND REMOVES BRANCH")

def export_room_tree(data, room_num, output_dir):
    """Export conversation tree for a room"""
    pair12 = read_room_pair(data, room_num, pair_num=12)

    if pair12 is None:
        return None

    descriptions, conv_start_pos = extract_descriptions(pair12)
    conv_data = pair12[conv_start_pos:]

    if len(conv_data) == 0:
        return {'room': room_num, 'has_conversations': False}

    elements, index_counts = parse_elements_with_indices(conv_data)
    roots = build_tree_structure(elements)

    output_file = output_dir / f"room{room_num:02d}_tree.txt"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"ROOM {room_num} - CONVERSATION TREE\n")
        f.write("=" * 80 + "\n\n")

        if descriptions:
            f.write("DESCRIPTIONS:\n")
            for i, desc in enumerate(descriptions, 1):
                f.write(f"  #{i}: {desc}\n")
            f.write("\n")

        f.write("CONVERSATION TREE:\n")
        f.write("=" * 80 + "\n\n")

        output_lines = format_tree_output(roots)
        for line in output_lines:
            f.write(line + "\n")

    return {'room': room_num, 'has_conversations': True, 'file': str(output_file)}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 export_trees_correct.py [room_number]")
        print("       python3 export_trees_correct.py --all")
        sys.exit(1)

    print("Loading ALFRED.1...")
    with open('files/ALFRED.1', 'rb') as f:
        data = f.read()

    output_dir = Path('conversation_trees_final')
    output_dir.mkdir(exist_ok=True)

    if sys.argv[1] == '--all':
        print("Exporting all rooms...")
        for room_num in range(55):
            result = export_room_tree(data, room_num, output_dir)
            if result and result['has_conversations']:
                print(f"  Room {room_num:02d}: ✓")
        print(f"\nDone! Trees exported to {output_dir}/")
    else:
        room_num = int(sys.argv[1])
        print(f"Exporting room {room_num}...")
        result = export_room_tree(data, room_num, output_dir)
        if result and result['has_conversations']:
            print(f"✓ Tree exported to {result['file']}")
        else:
            print(f"Room {room_num} has no conversations")

if __name__ == '__main__':
    main()
