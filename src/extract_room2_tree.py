#!/usr/bin/env python3
"""
Extract Room 2 conversations with proper tree structure.
Based on the working extract_room2_with_openings.py logic.
"""

import struct
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
    """Count ALL sprites"""
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

# Read data
with open('files/ALFRED.1', 'rb') as f:
    data = f.read()

ROOM = 2

# Get Pair 10 and Pair 12
pair10_data, _, _ = read_room_pair(data, ROOM, 10)
pair12_data, pair12_offset, pair12_size = read_room_pair(data, ROOM, 12)

# Count descriptions
sprite_count = count_all_sprites(pair10_data)
hotspot_count = count_hotspots(pair10_data)
total_desc = sprite_count + hotspot_count

print(f"Room {ROOM} Analysis:")
print(f"  Sprites: {sprite_count}")
print(f"  Hotspots: {hotspot_count}")
print(f"  Total descriptions: {total_desc}")
print(f"  Pair 12 offset: 0x{pair12_offset:08X}, size: {pair12_size}")
print()

# Find end of descriptions
ff_count = 0
desc_end = 0
ff_seen = 0

for i in range(len(pair12_data)):
    if pair12_data[i] == 0xFF:
        ff_count += 1
        ff_seen += 1
        if ff_seen == total_desc:
            # Find FD after this description
            for j in range(i + 1, min(i + 200, len(pair12_data))):
                if pair12_data[j] == 0xFD:
                    desc_end = j + 1
                    break
            break

print(f"Found {ff_count} 0xFF markers (expected {total_desc})")
print(f"Descriptions end at offset: 0x{desc_end:04X}")
print(f"Conversations start at: 0x{pair12_offset + desc_end:08X}")
print()
print("="*80)
print("SCANNING CONVERSATIONS")
print("="*80)

# Parse conversations - back up a bit to catch any FD FE at boundary
conv_start = max(0, desc_end - 20)
conv_data = pair12_data[conv_start:]
print(f"Scanning from offset 0x{conv_start:04X} (backed up from desc_end)")
print()
conversations = []
current_entry_point = None
entry_point_counter = 0

i = 0
while i < len(conv_data):
    byte = conv_data[i]
    
    # FD FE pattern - INITIAL greeting
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
                entry_point_counter += 1
                current_entry_point = entry_point_counter
                speaker = "NPC" if sep == 0x20 else "ALFRED"
                
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
                    'choice_group_id': None,
                    'offset': conv_start + i
                })
                
                print(f"[ENTRY POINT {current_entry_point}] 0x{index:02X} {speaker}: {text[:60]}")
                i = j
                continue
    
    # F7 pattern - RETURN greeting
    elif byte == 0xF7:
        if i + 6 < len(conv_data):
            control = conv_data[i + 1]
            speaker_id = conv_data[i + 2]
            marker = conv_data[i + 3]
            sep = conv_data[i + 4]
            index = conv_data[i + 5]
            term = conv_data[i + 6]
            
            if marker == 0x08 and term == 0x00:
                entry_point_counter += 1
                current_entry_point = entry_point_counter
                speaker = "NPC" if sep == 0x20 else "ALFRED"
                
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
                    'choice_group_id': None,
                    'offset': conv_start + i
                })
                
                print(f"[ENTRY POINT {current_entry_point}] 0x{index:02X} {speaker}: {text[:60]}")
                i = j
                continue
    
    # FD pattern - normal conversation
    elif byte == 0xFD:
        if i + 6 < len(conv_data):
            control = conv_data[i + 1]
            choice_group_id = conv_data[i + 2]
            marker = conv_data[i + 3]
            sep = conv_data[i + 4]
            index = conv_data[i + 5]
            term = conv_data[i + 6]
            
            if marker == 0x08 and term == 0x00:
                speaker = "NPC" if sep == 0x20 else "ALFRED"
                
                # Extract text
                text_start = i + 7
                text_bytes = bytearray()
                j = text_start
                has_embedded = False
                
                while j < len(conv_data):
                    b = conv_data[j]
                    
                    # Check for F8 embedded
                    if b == 0xF8 and j + 8 < len(conv_data):
                        pot_ctrl = conv_data[j + 3]
                        if pot_ctrl in [0xFB, 0xFC, 0xF1]:
                            emb_choice_gid = conv_data[j + 4]
                            emb_mark = conv_data[j + 5]
                            emb_sep = conv_data[j + 6]
                            emb_idx = conv_data[j + 7]
                            emb_term = conv_data[j + 8]
                            
                            if emb_mark == 0x08 and emb_term == 0x00:
                                # Save main line
                                main_text = text_bytes.decode('latin-1', errors='ignore').strip()
                                conversations.append({
                                    'index': index,
                                    'speaker': speaker,
                                    'text': main_text,
                                    'entry_point_id': current_entry_point,
                                    'choice_group_id': choice_group_id,
                                    'offset': conv_start + i
                                })
                                
                                # Extract embedded
                                emb_speaker = "NPC" if emb_sep == 0x20 else "ALFRED"
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
                                    'entry_point_id': current_entry_point,
                                    'choice_group_id': emb_choice_gid,
                                    'offset': conv_start + j
                                })
                                
                                has_embedded = True
                                i = k
                                break
                    
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
                        'entry_point_id': current_entry_point,
                        'choice_group_id': choice_group_id,
                        'offset': desc_end + i
                    })
                    i = j
                    continue
    
    # F4 FB/F1 pattern - alternative choice
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
                    speaker = "NPC" if sep == 0x20 else "ALFRED"
                    
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
                        'entry_point_id': current_entry_point,
                        'choice_group_id': choice_group_id,
                        'offset': desc_end + i
                    })
                    i = j
                    continue
    
    i += 1

print()
print("="*80)
print("CONVERSATION TREE")
print("="*80)

# Sort by entry point, then by index
# Filter out conversations without entry_point_id (orphaned)
conversations = [c for c in conversations if c.get('entry_point_id') is not None]
conversations.sort(key=lambda x: (x['entry_point_id'], x['index']))

# Group by entry point
entry_points = defaultdict(list)
for conv in conversations:
    ep_id = conv.get('entry_point_id')
    if ep_id is not None:
        entry_points[ep_id].append(conv)

# Print by entry point
for ep_id in sorted(entry_points.keys()):
    lines = entry_points[ep_id]
    
    # Find the entry point line
    ep_line = next((l for l in lines if l.get('entry_point')), None)
    if ep_line:
        print(f"\n━━━━ ENTRY POINT {ep_id}: {ep_line['entry_point'].upper()} ━━━━")
        print(f"0x{ep_line['index']:02X} | {ep_line['speaker']:6s} | {ep_line['text']}")
        print()
    
    # Show all lines in this entry point
    for conv in lines:
        if conv.get('entry_point'):
            continue  # Already showed this
        
        idx = conv['index']
        speaker = conv['speaker']
        text = conv['text'][:70]
        
        flags = []
        if conv.get('embedded'):
            flags.append(f"embedded in 0x{conv['parent_index']:02X}")
        if conv.get('alternative'):
            flags.append("ALT CHOICE")
        
        gid = conv.get('choice_group_id')
        if gid is not None:
            flags.append(f"group:0x{gid:02X}")
        
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        print(f"  0x{idx:02X} | {speaker:6s} | {text}{flag_str}")
    
    # Show choice groups within this entry point
    # Only show groups that represent actual player choices (multiple ALFRED lines with same group ID)
    # Don't show response groups (like 0x41 which is NPC's responses)
    choice_groups = defaultdict(list)
    for conv in lines:
        gid = conv.get('choice_group_id')
        # Only include ALFRED choices (player choices), not NPC responses
        if gid is not None and not conv.get('entry_point') and conv.get('speaker') == 'ALFRED':
            choice_groups[gid].append(conv)
    
    multi_groups = {k: v for k, v in choice_groups.items() if len(v) > 1}
    if multi_groups:
        print()
        print(f"  Player Choice Groups in Entry Point {ep_id}:")
        for gid in sorted(multi_groups.keys()):
            group = multi_groups[gid]
            print(f"    Group 0x{gid:02X} ({len(group)} alternatives):")
            for c in group:
                alt_marker = " [F4]" if c.get('alternative') else " [FD]"
                print(f"      - 0x{c['index']:02X}{alt_marker}: {c['text'][:50]}")

print()
print("="*80)
print(f"Total lines: {len(conversations)}")
print(f"Total entry points: {len(entry_points)}")
