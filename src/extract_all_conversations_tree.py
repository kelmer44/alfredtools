#!/usr/bin/env python3
"""
Extract all conversations from all rooms with complete tree structure.
Handles:
- FD FE pattern (initial greeting/opening)
- FD pattern (normal conversation flow)
- F7 pattern (return greeting and alternate entry points)
- F4 FB/F1 pattern (alternative player choices)
- F8 embedded alternatives
- Choice groups linking alternatives together
"""

import struct
import json
from pathlib import Path
from collections import defaultdict

def read_room_pair(data, room, pair_num):
    """Read a specific pair for a room"""
    room_offset = room * 104
    pair_offset = pair_num * 8

    dir_pos = room_offset + pair_offset
    offset = struct.unpack('<I', data[dir_pos:dir_pos + 4])[0]
    size = struct.unpack('<I', data[dir_pos + 4:dir_pos + 8])[0]

    if size == 0 or offset >= len(data):
        return None, 0, 0

    return data[offset:offset + size], offset, size

def count_all_sprites(pair10_data):
    """Count ALL sprites - iterate through all entries before 0x1BE"""
    sprite_count = 0
    offset = 0x06

    while offset + 44 <= 0x1BE and offset + 44 <= len(pair10_data):
        width = pair10_data[offset + 4]
        height = pair10_data[offset + 5]

        if width > 0 or height > 0:
            sprite_count += 1

        offset += 44

    return sprite_count

def count_hotspots(pair10_data):
    """Count static hotspots"""
    if 0x47A >= len(pair10_data):
        return 0
    return pair10_data[0x47A]

def extract_conversations_from_room(data, room_num):
    """Extract conversations from a room with full structure"""
    # Read Pair 10 for counts
    pair10_data, _, _ = read_room_pair(data, room_num, 10)
    if pair10_data is None:
        return None

    sprite_count = count_all_sprites(pair10_data)
    hotspot_count = count_hotspots(pair10_data)
    total_desc = sprite_count + hotspot_count

    # Read Pair 12
    pair12_data, pair12_off, pair12_sz = read_room_pair(data, room_num, 12)
    if pair12_data is None:
        return None

    # Count 0xFF markers to find where conversations start
    ff_count = sum(1 for b in pair12_data if b == 0xFF)

    # Find end of descriptions
    ff_seen = 0
    desc_end = 0
    for i in range(len(pair12_data)):
        if pair12_data[i] == 0xFF:
            ff_seen += 1
            if ff_seen == total_desc:
                for j in range(i + 1, min(i + 200, len(pair12_data))):
                    if pair12_data[j] == 0xFD:
                        desc_end = j + 1
                        break
                break

    if desc_end == 0:
        return None

    # Parse conversations starting from BEFORE desc_end to catch opening lines
    # Back up a bit to catch any FD FE pattern that might be at the boundary
    conv_start = max(0, desc_end - 10)
    conv_data = pair12_data[conv_start:]

    conversations = []
    current_entry_point = None  # Track which entry point we're currently in
    i = 0

    while i < len(conv_data):
        byte = conv_data[i]

        # FD FE pattern - opening greeting/initial conversation
        if byte == 0xFD and i + 1 < len(conv_data) and conv_data[i + 1] == 0xFE:
            if i + 8 < len(conv_data):
                unknown = conv_data[i + 2]
                control = conv_data[i + 3]
                speaker_id = conv_data[i + 4]
                marker = conv_data[i + 5]
                sep = conv_data[i + 6]
                index = conv_data[i + 7]
                term = conv_data[i + 8]
                
                if marker == 0x08 and term == 0x00:
                    speaker = "ALFRED" if sep == 0x20 else "NPC"
                    current_entry_point = f"initial_0x{index:02X}"  # Set current entry point
                    
                    # Extract text
                    text_start = i + 9
                    text_bytes = bytearray()
                    j = text_start
                    
                    while j < len(conv_data):
                        b = conv_data[j]
                        if b == 0xFD or (b >= 0xF0 and b != 0xF8):
                            break
                        if b >= 0x20:
                            text_bytes.append(b)
                        j += 1
                    
                    text = text_bytes.decode('latin-1', errors='ignore').strip()
                    conversations.append({
                        'index': index,
                        'speaker': speaker,
                        'text': text,
                        'entry_point': 'initial',
                        'entry_point_id': current_entry_point,
                        'speaker_id': speaker_id,
                        'offset': conv_start + i
                    })
                    i = j
                    continue
        
        # F7 pattern - return greeting/alternate entry point
        elif byte == 0xF7:
            if i + 6 < len(conv_data):
                control = conv_data[i + 1]
                speaker_id = conv_data[i + 2]
                marker = conv_data[i + 3]
                sep = conv_data[i + 4]
                index = conv_data[i + 5]
                term = conv_data[i + 6]
                
                if marker == 0x08 and term == 0x00:
                    speaker = "ALFRED" if sep == 0x20 else "NPC"
                    current_entry_point = f"return_0x{index:02X}"  # Set current entry point
                    
                    # Extract text
                    text_start = i + 7
                    text_bytes = bytearray()
                    j = text_start
                    
                    while j < len(conv_data):
                        b = conv_data[j]
                        if b == 0xFD or b == 0xF7 or (b >= 0xF0 and b != 0xF8):
                            break
                        if b >= 0x20:
                            text_bytes.append(b)
                        j += 1
                    
                    text = text_bytes.decode('latin-1', errors='ignore').strip()
                    conversations.append({
                        'index': index,
                        'speaker': speaker,
                        'text': text,
                        'entry_point': 'return',
                        'entry_point_id': current_entry_point,
                        'speaker_id': speaker_id,
                        'offset': conv_start + i
                    })
                    i = j
                    continue

        # FD pattern - normal conversation flow
        elif byte == 0xFD:
            if i + 6 < len(conv_data):
                control = conv_data[i + 1]
                choice_group_id = conv_data[i + 2]
                marker = conv_data[i + 3]
                sep = conv_data[i + 4]
                index = conv_data[i + 5]
                term = conv_data[i + 6]

                if marker == 0x08 and term == 0x00:
                    speaker = "ALFRED" if sep == 0x20 else "NPC"

                    # Extract text
                    text_start = i + 7
                    text_bytes = bytearray()
                    j = text_start
                    has_embedded = False

                    while j < len(conv_data):
                        b = conv_data[j]

                        # Check for F8 embedded alternative
                        if b == 0xF8 and j + 8 < len(conv_data):
                            pot_ctrl = conv_data[j + 3]
                            if pot_ctrl in [0xFB, 0xFC, 0xF1]:
                                emb_choice_gid = conv_data[j + 4]
                                emb_mark = conv_data[j + 5]
                                emb_sep = conv_data[j + 6]
                                emb_idx = conv_data[j + 7]
                                emb_term = conv_data[j + 8]

                                if emb_mark == 0x08 and emb_term == 0x00:
                                    # Save main line first
                                    main_text = text_bytes.decode('latin-1', errors='ignore').strip()
                                    conversations.append({
                                        'index': index,
                                        'speaker': speaker,
                                        'text': main_text,
                                        'choice_group_id': choice_group_id,
                                        'entry_point_id': current_entry_point,
                                        'offset': conv_start + i
                                    })

                                    # Extract embedded text
                                    emb_speaker = "ALFRED" if emb_sep == 0x20 else "NPC"
                                    emb_text_start = j + 9
                                    emb_text_bytes = bytearray()
                                    k = emb_text_start

                                    while k < len(conv_data):
                                        eb = conv_data[k]
                                        if eb == 0xFD or eb >= 0xF0:
                                            break
                                        if eb >= 0x20:
                                            emb_text_bytes.append(eb)
                                        k += 1

                                    emb_text = emb_text_bytes.decode('latin-1', errors='ignore').strip()
                                    conversations.append({
                                        'index': emb_idx,
                                        'speaker': emb_speaker,
                                        'text': emb_text,
                                        'embedded': True,
                                        'parent_index': index,
                                        'choice_group_id': emb_choice_gid,
                                        'entry_point_id': current_entry_point,
                                        'offset': conv_start + j
                                    })

                                    has_embedded = True
                                    i = k
                                    break

                        # Stop on control codes
                        if b == 0xFD or (b >= 0xF0 and b != 0xF8):
                            break
                        if b >= 0x20:
                            text_bytes.append(b)
                        j += 1

                    if not has_embedded:
                        text = text_bytes.decode('latin-1', errors='ignore').strip()
                        conversations.append({
                            'index': index,
                            'speaker': speaker,
                            'text': text,
                            'choice_group_id': choice_group_id,
                            'entry_point_id': current_entry_point,
                            'offset': conv_start + i
                        })
                        i = j
                        continue

        # F4 FB pattern - alternative player choice
        elif byte == 0xF4 and i + 1 < len(conv_data):
            next_byte = conv_data[i + 1]
            if next_byte in [0xFB, 0xF1]:
                if i + 6 < len(conv_data):
                    choice_group_id = conv_data[i + 2]
                    marker = conv_data[i + 3]
                    sep = conv_data[i + 4]
                    index = conv_data[i + 5]
                    term = conv_data[i + 6]

                    if marker == 0x08 and term == 0x00:
                        speaker = "ALFRED" if sep == 0x20 else "NPC"

                        # Extract text
                        text_start = i + 7
                        text_bytes = bytearray()
                        j = text_start

                        while j < len(conv_data):
                            b = conv_data[j]
                            if b == 0xFD or (b >= 0xF0 and b != 0xF8):
                                break
                            if b >= 0x20:
                                text_bytes.append(b)
                            j += 1

                        text = text_bytes.decode('latin-1', errors='ignore').strip()
                        conversations.append({
                            'index': index,
                            'speaker': speaker,
                            'text': text,
                            'alternative': True,
                            'choice_group_id': choice_group_id,
                            'entry_point_id': current_entry_point,
                            'offset': conv_start + i
                        })
                        i = j
                        continue

        i += 1

    if not conversations:
        return None

    # Build tree structure
    # Group by entry_point_id AND choice_group_id to find alternatives
    choice_groups = defaultdict(lambda: defaultdict(list))
    for conv in conversations:
        gid = conv.get('choice_group_id')
        ep_id = conv.get('entry_point_id')
        if gid is not None and ep_id is not None:
            choice_groups[ep_id][gid].append(conv['index'])
    
    # Flatten to only show groups with alternatives
    flat_choice_groups = {}
    for ep_id, groups in choice_groups.items():
        for gid, indices in groups.items():
            if len(indices) > 1:
                key = f"{ep_id}_grp_0x{gid:02X}"
                flat_choice_groups[key] = {
                    'entry_point_id': ep_id,
                    'choice_group_id': gid,
                    'indices': indices
                }
    
    # Find entry points
    entry_points = [c for c in conversations if c.get('entry_point') in ['initial', 'return']]
    
    return {
        'room': room_num,
        'sprites': sprite_count,
        'hotspots': hotspot_count,
        'total_descriptions': total_desc,
        'ff_markers': ff_count,
        'match': ff_count == total_desc,
        'conversations': conversations,
        'choice_groups': flat_choice_groups,
        'entry_points': entry_points,
        'conversation_count': len(conversations)
    }

def build_tree_text(room_data):
    """Build a human-readable tree view of conversations"""
    conversations = room_data['conversations']
    choice_groups = room_data.get('choice_groups', {})

    # Sort by index
    conversations.sort(key=lambda x: x['index'])

    lines = []
    lines.append(f"\n{'='*80}")
    lines.append(f"ROOM {room_data['room']} - Conversation Tree")
    lines.append(f"{'='*80}")
    lines.append(f"Sprites: {room_data['sprites']}, Hotspots: {room_data['hotspots']}, Total Descriptions: {room_data['total_descriptions']}")
    lines.append(f"0xFF markers: {room_data['ff_markers']} {'✓' if room_data['match'] else '✗'}")
    lines.append(f"Total conversation lines: {room_data['conversation_count']}")
    lines.append("")

    # Show entry points first
    entry_points = room_data.get('entry_points', [])
    if entry_points:
        lines.append("Entry Points:")
        for ep in entry_points:
            ep_type = ep.get('entry_point', 'unknown').upper()
            lines.append(f"  [{ep_type}] Index 0x{ep['index']:02X}: {ep['speaker']} - {ep['text'][:60]}")
        lines.append("")

    # Show all conversations
    lines.append("All Conversation Lines (sorted by index):")
    lines.append("-" * 80)

    for conv in conversations:
        idx = conv['index']
        speaker = conv['speaker']
        text = conv['text'][:70]

        flags = []
        if conv.get('entry_point') == 'initial':
            flags.append("INITIAL")
        elif conv.get('entry_point') == 'return':
            flags.append("RETURN")
        if conv.get('embedded'):
            flags.append(f"EMBEDDED (parent:0x{conv.get('parent_index', 0):02X})")
        if conv.get('alternative'):
            flags.append("ALT CHOICE")

        gid = conv.get('choice_group_id')
        if gid is not None:
            # Check if this index is in a choice group
            gid_hex = f"0x{gid:02X}"
            if gid_hex in choice_groups and len(choice_groups[gid_hex]) > 1:
                flags.append(f"group:{gid_hex}")

        flag_str = f" [{', '.join(flags)}]" if flags else ""
        lines.append(f"  0x{idx:02X} | {speaker:6s} | {text}{flag_str}")

    # Show choice groups organized by entry point
    if choice_groups:
        lines.append("")
        lines.append("Choice Groups (alternatives at same decision point):")
        lines.append("-" * 80)
        
        # Group by entry point
        by_entry = defaultdict(list)
        for key, group_data in sorted(choice_groups.items()):
            ep_id = group_data['entry_point_id']
            by_entry[ep_id].append(group_data)
        
        for ep_id in sorted(by_entry.keys()):
            lines.append(f"\n  Entry Point: {ep_id}")
            for group_data in by_entry[ep_id]:
                gid = group_data['choice_group_id']
                indices = group_data['indices']
                lines.append(f"    Group 0x{gid:02X} ({len(indices)} alternatives):")
                for idx in indices:
                    conv = next((c for c in conversations if c['index'] == idx), None)
                    if conv:
                        alt_marker = " [F4]" if conv.get('alternative') else " [FD]"
                        lines.append(f"      - 0x{idx:02X}{alt_marker}: {conv['text'][:50]}")
    
    lines.append("="*80)
    return "\n".join(lines)

def main():
    with open('files/ALFRED.1', 'rb') as f:
        data = f.read()

    print("Extracting conversations from all rooms with tree structure...")
    print("="*80)

    all_rooms = []
    all_trees = []

    for room in range(56):
        result = extract_conversations_from_room(data, room)
        if result and result['conversations']:
            print(f"\nRoom {room}: {result['sprites']} sprites + {result['hotspots']} hotspots = {result['total_descriptions']} descriptions")
            print(f"  0xFF markers: {result['ff_markers']} {'✓' if result['match'] else '✗'}")
            print(f"  Conversations: {result['conversation_count']}")
            print(f"  Entry points: {len(result['entry_points'])}")
            print(f"  Choice groups: {len(result['choice_groups'])}")

            all_rooms.append(result)
            all_trees.append(build_tree_text(result))

    # Save JSON
    json_path = Path('src/all_conversations_tree.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_rooms, f, indent=2, ensure_ascii=False)

    # Save tree view
    tree_path = Path('src/all_conversations_tree.txt')
    with open(tree_path, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(all_trees))

    print(f"\n\nSaved {len(all_rooms)} rooms with conversations")
    print(f"JSON: {json_path}")
    print(f"Tree view: {tree_path}")

if __name__ == '__main__':
    main()
