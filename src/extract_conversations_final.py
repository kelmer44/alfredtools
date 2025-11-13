#!/usr/bin/env python3
"""
Extract all conversations from all rooms - Fixed version
Room 2 has 4 sprites + 6 hotspots = 10 total descriptions
"""

import struct
import json
from pathlib import Path

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
    """Count ALL sprites (not just clickable ones) - iterate through all entries before 0x1BE"""
    sprite_count = 0
    offset = 0x06
    
    # Sprites end at offset 0x1BE where exit count begins
    while offset + 44 <= 0x1BE and offset + 44 <= len(pair10_data):
        width = pair10_data[offset + 4]
        height = pair10_data[offset + 5]
        
        # Count non-empty sprites
        if width > 0 or height > 0:
            sprite_count += 1
        
        offset += 44
    
    return sprite_count

def count_hotspots(pair10_data):
    """Count static hotspots"""
    if 0x47A >= len(pair10_data):
        return 0
    return pair10_data[0x47A]

def extract_room(data, room_num):
    """Extract conversations from one room"""
    # Read Pair 10
    pair10_data, _, _ = read_room_pair(data, room_num, 10)
    if pair10_data is None:
        return None
    
    # Count ALL sprites + hotspots
    sprite_count = count_all_sprites(pair10_data)
    hotspot_count = count_hotspots(pair10_data)
    total_desc = sprite_count + hotspot_count
    
    # Read Pair 12
    pair12_data, pair12_off, pair12_sz = read_room_pair(data, room_num, 12)
    if pair12_data is None:
        return None
    
    # Count 0xFF markers
    ff_count = sum(1 for b in pair12_data if b == 0xFF)
    
    # Find end of descriptions
    ff_seen = 0
    desc_end = 0
    for i in range(len(pair12_data)):
        if pair12_data[i] == 0xFF:
            ff_seen += 1
            if ff_seen == total_desc:
                # Find FD after this description
                for j in range(i + 1, min(i + 200, len(pair12_data))):
                    if pair12_data[j] == 0xFD:
                        desc_end = j + 1
                        break
                break
    
    if desc_end == 0:
        return None
    
    # Parse conversations
    conv_data = pair12_data[desc_end:]
    conversations = []
    
    i = 0
    while i < len(conv_data):
        if conv_data[i] == 0xFD and i + 6 < len(conv_data):
            marker = conv_data[i + 1]
            if marker in [0xFC, 0xFB, 0xF1]:
                speaker = conv_data[i + 2]
                sep = conv_data[i + 4]
                idx = conv_data[i + 5]
                
                # Extract text
                text_start = i + 7
                text_end = text_start
                while text_end < len(conv_data):
                    if conv_data[text_end] in [0xFD, 0xF4, 0xF8]:
                        break
                    text_end += 1
                
                text = conv_data[text_start:text_end].decode('latin-1', errors='ignore').strip()
                
                conversations.append({
                    'speaker': f"0x{speaker:02X}",
                    'index': idx,
                    'text': text
                })
                
                i = text_end
                continue
        i += 1
    
    return {
        'room': room_num,
        'sprites': sprite_count,
        'hotspots': hotspot_count,
        'total_descriptions': total_desc,
        'ff_found': ff_count,
        'match': ff_count == total_desc,
        'pair12_offset': f"0x{pair12_off:08X}",
        'conversations': conversations
    }

def main():
    with open('files/ALFRED.1', 'rb') as f:
        data = f.read()
    
    print("Extracting all conversations...")
    print("=" * 70)
    
    all_rooms = []
    for room in range(56):
        result = extract_room(data, room)
        if result:
            print(f"\nRoom {room}: {result['sprites']} sprites + {result['hotspots']} hotspots = {result['total_descriptions']} descriptions")
            print(f"  0xFF markers: {result['ff_found']} {'✓' if result['match'] else '✗'}")
            print(f"  Conversations: {len(result['conversations'])}")
            
            if result['conversations']:
                all_rooms.append(result)
    
    # Save JSON
    out_path = Path('src/all_conversations_final.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(all_rooms, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nSaved {len(all_rooms)} rooms to {out_path}")

if __name__ == '__main__':
    main()
