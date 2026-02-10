#!/usr/bin/env python3
"""
Extract Conversation Tree with Action Emphasis
===============================================

Produces conversation trees for any room in the game with emphasis on action codes.
Trees show hierarchical structure with proper choice detection and all action triggers.

Usage:
    python3 src/extract_conversation_tree.py <room_number>
    python3 src/extract_conversation_tree.py 22

Output format matches room22_tree.txt with tree-drawing characters and action annotations.
Includes action summary section at the end for implementation reference.
"""

import struct
import sys
from pathlib import Path
from collections import Counter
from typing import List, Dict, Optional, Tuple


# ============================================================================
# CONTROL CODES
# ============================================================================

CTRL_SPEAKER = 0x08           # Speaker marker (followed by speaker ID)
CTRL_ALFRED_ID = 0x0D         # Alfred's speaker ID
CTRL_END_TEXT = 0xFD          # End of text line
CTRL_TEXT_TERM = 0xFC         # Alternative text terminator
CTRL_CHOICE_ONCE = 0xFB       # One-time choice (disabled after selection)
CTRL_CHOICE_REPEAT = 0xF1     # Repeatable choice
CTRL_DISABLED = 0xFA          # Disabled choice marker (replaces 0x08)
CTRL_PAGE_BREAK = 0xF9        # Long text page break
CTRL_ACTION = 0xF8            # Action trigger (followed by 2-byte action ID)
CTRL_END_BRANCH = 0xF7        # End conversation branch
CTRL_LINE_CONTINUE = 0xF6     # Line continuation
CTRL_END_CONV_ALT = 0xF5      # Alternative end marker
CTRL_ROOT_PRIMARY = 0xFE      # Primary conversation root
CTRL_END_CONV = 0xF4          # End conversation
CTRL_GO_BACK = 0xF0           # Return to previous menu
CTRL_ALT_END = 0xEB           # Another alternative end marker
CTRL_DESC_START = 0xFF        # Description block start

# Spanish character encoding
SPANISH_CHARS = {
    0x80: 'ñ', 0x81: 'í', 0x82: '¡', 0x83: '¿', 0x84: 'ú',
    0x7B: 'á', 0x7C: 'é', 0x7D: 'í', 0x7E: 'ó', 0x7F: 'ú',
}


# ============================================================================
# DATA STRUCTURES
# ============================================================================

class ConversationNode:
    """Node in the conversation tree"""
    def __init__(self, node_type: str):
        self.node_type = node_type  # 'root', 'npc', 'choice', 'auto'
        self.text: str = ""
        self.speaker: str = ""
        self.choice_type: Optional[str] = None  # 'FB', 'F1', 'FA'
        self.choice_index: Optional[int] = None
        self.action_code: Optional[int] = None
        self.has_go_back: bool = False
        self.has_f4_end: bool = False
        self.has_f7_branch: bool = False
        self.children: List['ConversationNode'] = []
        self.root_index: Optional[int] = None  # For FE roots
        
    def __repr__(self):
        return f"<{self.node_type}: {self.text[:30]}... children={len(self.children)}>"


class ConversationTree:
    """Complete conversation tree for a room"""
    def __init__(self, room_num: int):
        self.room_num = room_num
        self.roots: List[ConversationNode] = []
        self.actions_found: List[Tuple[int, str]] = []  # (action_id, context)
        self.descriptions: List[str] = []


# ============================================================================
# FILE READING UTILITIES
# ============================================================================

def read_room_pair(data: bytes, room_num: int, pair_num: int) -> Optional[bytes]:
    """Read a specific data pair from a room"""
    room_offset = room_num * 104  # 13 pairs × 8 bytes
    pair_offset_pos = room_offset + (pair_num * 8)
    
    if pair_offset_pos + 8 > len(data):
        return None
    
    offset = struct.unpack('<I', data[pair_offset_pos:pair_offset_pos+4])[0]
    size = struct.unpack('<I', data[pair_offset_pos+4:pair_offset_pos+8])[0]
    
    if size == 0 or offset >= len(data):
        return None
    
    return data[offset:offset+size]


def get_sprite_hotspot_counts(data: bytes, room_num: int) -> Tuple[int, int]:
    """Get sprite and hotspot counts from Pair 10"""
    pair10 = read_room_pair(data, room_num, pair_num=10)
    if pair10 is None:
        return 0, 0
    
    sprite_count = pair10[5] - 2 if len(pair10) > 5 else 0
    hotspot_count = pair10[0x47A] if len(pair10) > 0x47A else 0
    
    return sprite_count, hotspot_count


def decode_byte(b: int) -> Optional[str]:
    """Decode a byte to character"""
    if b in SPANISH_CHARS:
        return SPANISH_CHARS[b]
    elif 0x20 <= b <= 0x7A:
        return chr(b)
    else:
        return None


def clean_text(text: str) -> str:
    """Clean control sequences from text"""
    text = text.strip()
    
    # Remove leading [XX][00] patterns
    while text and '[' in text[:15]:
        idx = text.find('[')
        if 0 <= idx < 10:
            end_idx = text.find(']', idx)
            if idx < end_idx < idx + 10:
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


# ============================================================================
# DESCRIPTION EXTRACTION
# ============================================================================

def extract_descriptions(data: bytes, sprite_count: int, hotspot_count: int) -> Tuple[List[str], int]:
    """Extract sprite/hotspot descriptions and return conversation start position"""
    descriptions = []
    desc_count = sprite_count + hotspot_count
    pos = 0
    
    for _ in range(desc_count):
        # Find FF marker
        while pos < len(data) and data[pos] != CTRL_DESC_START:
            pos += 1
        
        if pos >= len(data):
            break
        
        pos += 1  # Skip FF
        if pos + 4 >= len(data):
            break
        
        pos += 4  # Skip item_id and header bytes
        
        # Read text until FD
        text = ""
        while pos < len(data) and data[pos] != CTRL_END_TEXT:
            char = decode_byte(data[pos])
            if char:
                text += char
            pos += 1
        
        if text:
            descriptions.append(clean_text(text))
        
        # Skip FD
        if pos < len(data) and data[pos] == CTRL_END_TEXT:
            pos += 1
    
    return descriptions, pos


# ============================================================================
# CONVERSATION PARSING
# ============================================================================

def read_text_until_control(data: bytes, pos: int) -> Tuple[str, int]:
    """Read text until hitting a control code"""
    end_markers = {
        CTRL_SPEAKER, CTRL_CHOICE_ONCE, CTRL_CHOICE_REPEAT, CTRL_ACTION,
        CTRL_END_TEXT, CTRL_TEXT_TERM, CTRL_END_CONV, CTRL_END_BRANCH,
        CTRL_END_CONV_ALT, CTRL_ROOT_PRIMARY, CTRL_ALT_END, CTRL_GO_BACK
    }
    
    text = ""
    while pos < len(data) and data[pos] not in end_markers:
        char = decode_byte(data[pos])
        if char:
            text += char
        pos += 1
    
    return clean_text(text), pos


def count_choice_indices(data: bytes) -> Counter:
    """Count occurrences of each choice index to detect real choices vs auto-dialogue"""
    choice_indices = []
    pos = 0
    
    while pos < len(data):
        if data[pos] in [CTRL_CHOICE_ONCE, CTRL_CHOICE_REPEAT]:
            pos += 1
            if pos < len(data):
                choice_indices.append(data[pos])
        pos += 1
    
    return Counter(choice_indices)


def parse_conversation_tree(conv_data: bytes, tree: ConversationTree) -> None:
    """Parse conversation data into tree structure"""
    if len(conv_data) == 0:
        return
    
    # Count choice indices to detect real choices
    index_counts = count_choice_indices(conv_data)
    
    pos = 0
    stack = []  # Stack of (node, level) tuples
    current_root = None
    current_level = 0
    
    while pos < len(conv_data):
        b = conv_data[pos]
        
        # === ROOT PRIMARY (FE) ===
        if b == CTRL_ROOT_PRIMARY:
            pos += 1
            root_index = conv_data[pos] if pos < len(conv_data) else 0
            pos += 1
            
            # Next should be FC (speaker)
            if pos < len(conv_data) and conv_data[pos] == CTRL_TEXT_TERM:
                pos += 1
                speaker_id = conv_data[pos] if pos < len(conv_data) else 0
                pos += 1
                
                # Skip 08 and voice bytes (3 bytes)
                if pos < len(conv_data) and conv_data[pos] == CTRL_SPEAKER:
                    pos += 4  # Skip 08 + 3 voice bytes
                
                # Read text
                text, pos = read_text_until_control(conv_data, pos)
                
                # Create root node
                current_root = ConversationNode('root')
                current_root.text = text
                current_root.speaker = 'NPC'
                current_root.root_index = root_index
                tree.roots.append(current_root)
                stack = [(current_root, 0)]
                current_level = 0
        
        # === ALTERNATIVE ROOT (F7 FC pattern) ===
        elif b == CTRL_END_BRANCH:
            pos += 1
            # Check if followed by FC (alternative root)
            if pos < len(conv_data) and conv_data[pos] == CTRL_TEXT_TERM:
                pos += 1
                speaker_id = conv_data[pos] if pos < len(conv_data) else 0
                pos += 1
                
                # Skip 08 and voice bytes
                if pos < len(conv_data) and conv_data[pos] == CTRL_SPEAKER:
                    pos += 4
                
                text, pos = read_text_until_control(conv_data, pos)
                
                current_root = ConversationNode('root')
                current_root.text = text
                current_root.speaker = 'NPC'
                tree.roots.append(current_root)
                stack = [(current_root, 0)]
                current_level = 0
            else:
                # Just a branch end
                stack.clear()
                current_root = None
        
        # === NPC SPEAKER (FC) ===
        elif b == CTRL_TEXT_TERM:
            pos += 1
            speaker_id = conv_data[pos] if pos < len(conv_data) else 0
            pos += 1
            
            # Skip 08 and voice bytes
            if pos < len(conv_data) and conv_data[pos] == CTRL_SPEAKER:
                pos += 4
            
            text, pos = read_text_until_control(conv_data, pos)
            
            node = ConversationNode('npc')
            node.text = text
            node.speaker = 'NPC'
            
            # Check for action code
            if pos < len(conv_data) and conv_data[pos] == CTRL_ACTION:
                pos += 1
                if pos + 1 < len(conv_data):
                    action_lo = conv_data[pos]
                    action_hi = conv_data[pos + 1]
                    action_code = action_lo | (action_hi << 8)
                    node.action_code = action_code
                    tree.actions_found.append((action_code, f"After: {text[:50]}"))
                    pos += 2
            
            # Check for go back
            if pos < len(conv_data) and conv_data[pos] == CTRL_GO_BACK:
                node.has_go_back = True
                pos += 1
            
            # Attach to parent
            if stack:
                parent, _ = stack[-1]
                parent.children.append(node)
        
        # === CHOICE MARKERS (FB, F1) ===
        elif b in [CTRL_CHOICE_ONCE, CTRL_CHOICE_REPEAT]:
            choice_type_byte = b
            pos += 1
            
            # Read choice index
            choice_index = conv_data[pos] if pos < len(conv_data) else 0
            pos += 1
            
            # Check if disabled (FA instead of 08)
            is_disabled = False
            if pos < len(conv_data):
                marker = conv_data[pos]
                if marker == CTRL_DISABLED:
                    is_disabled = True
                pos += 1
            
            # Skip speaker ID
            if pos < len(conv_data):
                pos += 1
            
            # Read choice text
            text, pos = read_text_until_control(conv_data, pos)
            
            # Skip FD if present
            if pos < len(conv_data) and conv_data[pos] == CTRL_END_TEXT:
                pos += 1
            
            # Determine if real choice or auto-dialogue
            is_real_choice = index_counts[choice_index] > 1
            
            if is_real_choice:
                # Real player choice
                node = ConversationNode('choice')
                node.text = text
                node.speaker = 'ALFRED'
                node.choice_type = 'F1' if choice_type_byte == CTRL_CHOICE_REPEAT else ('FA' if is_disabled else 'FB')
                node.choice_index = choice_index
                
                # Pop stack to correct level
                while stack and len(stack) > choice_index:
                    stack.pop()
                
                # Attach to parent
                if stack:
                    parent, _ = stack[-1]
                    parent.children.append(node)
                    stack.append((node, choice_index))
                elif current_root:
                    current_root.children.append(node)
                    stack.append((node, choice_index))
            else:
                # Auto-dialogue (Alfred speaks automatically)
                node = ConversationNode('auto')
                node.text = text
                node.speaker = 'ALFRED'
                node.choice_type = 'F1' if choice_type_byte == CTRL_CHOICE_REPEAT else 'FB'
                
                if stack:
                    parent, _ = stack[-1]
                    parent.children.append(node)
        
        # === ACTION (F8) ===
        elif b == CTRL_ACTION:
            pos += 1
            if pos + 1 < len(conv_data):
                action_lo = conv_data[pos]
                action_hi = conv_data[pos + 1]
                action_code = action_lo | (action_hi << 8)
                
                # Attach to last node in stack
                if stack:
                    last_node, _ = stack[-1]
                    last_node.action_code = action_code
                    tree.actions_found.append((action_code, f"After last node: {last_node.text[:50]}"))
                
                pos += 2
        
        # === END CONVERSATION (F4) ===
        elif b == CTRL_END_CONV:
            if stack:
                last_node, _ = stack[-1]
                last_node.has_f4_end = True
            pos += 1
        
        # === GO BACK (F0) ===
        elif b == CTRL_GO_BACK:
            if stack:
                last_node, _ = stack[-1]
                last_node.has_go_back = True
            pos += 1
        
        # === OTHER CONTROL CODES ===
        else:
            pos += 1


# ============================================================================
# TREE FORMATTING
# ============================================================================

def format_tree_output(tree: ConversationTree) -> List[str]:
    """Format tree with visual hierarchy"""
    lines = []
    
    lines.append("=" * 80)
    lines.append(f"ROOM {tree.room_num} CONVERSATION TREE")
    lines.append("=" * 80)
    lines.append("")
    
    if tree.descriptions:
        lines.append("DESCRIPTIONS:")
        for i, desc in enumerate(tree.descriptions, 1):
            lines.append(f"  #{i}: {desc}")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
    
    # Print each root
    for root in tree.roots:
        format_node(root, lines, prefix="", is_last=True, is_root=True)
        lines.append("")
    
    # Action summary
    if tree.actions_found:
        lines.append("")
        lines.append("=" * 80)
        lines.append("ACTION CODES FOUND IN THIS ROOM")
        lines.append("=" * 80)
        lines.append("")
        
        # Deduplicate actions
        unique_actions = {}
        for action_id, context in tree.actions_found:
            if action_id not in unique_actions:
                unique_actions[action_id] = context
        
        for action_id in sorted(unique_actions.keys()):
            context = unique_actions[action_id]
            lines.append(f"  → ACTION {action_id:04X} ({action_id:3d})  |  {context}")
        
        lines.append("")
        lines.append("Use these action codes for ScummVM implementation reference.")
        lines.append("See ACTION_DISPATCH_TABLES.md for handler details.")
    
    # Legend
    lines.append("")
    lines.append("=" * 80)
    lines.append("LEGEND")
    lines.append("=" * 80)
    lines.append("  [FB-ONCE]      = One-time choice (disabled after selection)")
    lines.append("  [F1-REPEAT]    = Repeatable choice (can be selected multiple times)")
    lines.append("  [FA-DISABLED]  = Already disabled choice")
    lines.append("  [F0-GO_BACK]   = Returns to parent menu after this response")
    lines.append("  [F4-END]       = Terminates conversation entirely")
    lines.append("  → ACTION XXXX  = Triggers action code XXXX")
    lines.append("")
    
    return lines


def format_node(node: ConversationNode, lines: List[str], prefix: str, is_last: bool, is_root: bool = False) -> None:
    """Recursively format a node with tree characters"""
    
    # Determine tree characters
    if is_root:
        connector = "└─ ROOT"
        child_prefix = "   "
    else:
        connector = "└─" if is_last else "├─"
        child_prefix = prefix + ("   " if is_last else "│  ")
    
    # Format node based on type
    if node.node_type == 'root':
        lines.append(f"{prefix}{connector}")
        
        # Show root index if present
        root_info = f" (root #{node.root_index})" if node.root_index is not None else ""
        lines.append(f"{child_prefix}NPC: {node.text}{root_info}")
        
    elif node.node_type == 'choice':
        # Choice marker
        marker = f"[{node.choice_type}-{'ONCE' if node.choice_type == 'FB' else ('DISABLED' if node.choice_type == 'FA' else 'REPEAT')}]"
        lines.append(f"{prefix}{connector} [{node.choice_index}] {marker} {node.text}")
        
    elif node.node_type == 'auto':
        # Auto-dialogue (no menu shown to player)
        lines.append(f"{prefix}{connector} [{node.choice_index}] [AUTO-DIALOGUE] {node.text}")
        
    elif node.node_type == 'npc':
        # NPC response
        action_str = f" → ACTION {node.action_code:04X}" if node.action_code else ""
        go_back_str = " [F0-GO_BACK]" if node.has_go_back else ""
        f4_str = " [F4-END]" if node.has_f4_end else ""
        
        lines.append(f"{prefix}{connector} NPC: {node.text}{action_str}{go_back_str}{f4_str}")
    
    # Format children
    for i, child in enumerate(node.children):
        is_last_child = (i == len(node.children) - 1)
        format_node(child, lines, child_prefix, is_last_child)


# ============================================================================
# MAIN EXTRACTION
# ============================================================================

def extract_conversation_tree(alfred1_data: bytes, room_num: int) -> ConversationTree:
    """Extract complete conversation tree for a room"""
    tree = ConversationTree(room_num)
    
    # Get Pair 12 (text data)
    pair12 = read_room_pair(alfred1_data, room_num, pair_num=12)
    if pair12 is None:
        return tree
    
    # Get sprite/hotspot counts to skip descriptions
    sprite_count, hotspot_count = get_sprite_hotspot_counts(alfred1_data, room_num)
    
    # Extract descriptions
    descriptions, conv_start_pos = extract_descriptions(pair12, sprite_count, hotspot_count)
    tree.descriptions = descriptions
    
    # Get conversation data
    conv_data = pair12[conv_start_pos:]
    
    # Parse conversation tree
    parse_conversation_tree(conv_data, tree)
    
    return tree


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 src/extract_conversation_tree.py <room_number>")
        print("")
        print("Example:")
        print("  python3 src/extract_conversation_tree.py 22")
        sys.exit(1)
    
    room_num = int(sys.argv[1])
    
    print(f"Loading ALFRED.1...")
    alfred1_path = Path('files/ALFRED.1')
    
    if not alfred1_path.exists():
        print(f"Error: {alfred1_path} not found!")
        print("Make sure you're running this from the alfredtools directory.")
        sys.exit(1)
    
    with open(alfred1_path, 'rb') as f:
        data = f.read()
    
    print(f"Extracting conversation tree for room {room_num}...")
    tree = extract_conversation_tree(data, room_num)
    
    if not tree.roots and not tree.descriptions:
        print(f"Room {room_num} has no conversations.")
        return
    
    # Format output
    lines = format_tree_output(tree)
    
    # Print to stdout
    for line in lines:
        print(line)
    
    # Also save to file
    output_dir = Path('output_conversation_trees')
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"room{room_num:02d}_tree.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\n✓ Tree saved to {output_file}")


if __name__ == '__main__':
    main()
