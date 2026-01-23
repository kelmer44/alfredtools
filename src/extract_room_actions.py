#!/usr/bin/env python3
"""
Alfred Pelrock - Room Actions Extractor
Extracts hotspots, sprites and their action flags from ALFRED.1

Action Flags (from Ghidra analysis):
  0x01 - execute_room_specific_script (room scripts)
  0x02 - handle_conversation_tree
  0x08 - handle_dialog_interaction
  0x10 - dispatch_hotspot_action_by_extra_id (simple actions)
  0x20 - execute_script_table_0x47c10 (TAKE actions)
  0x40 - execute_script_table_0x47c18 (PICK UP actions)
  0x80 - execute_script_table_0x47cbc
  0x200 - execute_complex_item_script_table (USE X WITH Y)

Sprite action flags (byte +0x22/34):
  0x01 - OPEN
  0x02 - CLOSE
  0x04 - PUSH
  0x08 - PULL
  0x10 - TALK
  0x20 - unknown
  0x40 - unknown
  0x80 - unknown
  (LOOK is always available)

Usage:
    python extract_room_actions.py <alfred.1> [rooms]
    
Example:
    python extract_room_actions.py files/ALFRED.1 0-5
"""

import struct
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple


# Action flag meanings for the dispatcher
DISPATCH_FLAGS = {
    0x01: "ROOM_SCRIPT",
    0x02: "CONVERSATION",
    0x08: "DIALOG",
    0x10: "HOTSPOT_ACTION",
    0x20: "TAKE",
    0x40: "PICKUP",
    0x80: "SCRIPT_0x47CBC",
    0x200: "USE_ITEM_COMBO",
}

# Sprite action flags (verb menu)
SPRITE_ACTION_FLAGS = {
    0x01: "OPEN",
    0x02: "CLOSE",
    0x04: "PUSH",
    0x08: "PULL",
    0x10: "TALK",
    0x20: "UNKNOWN_0x20",
    0x40: "UNKNOWN_0x40",
    0x80: "UNKNOWN_0x80",
}


def decode_action_flags(flags: int, flag_dict: Dict[int, str]) -> List[str]:
    """Decode a flags byte into a list of action names"""
    actions = []
    for bit, name in flag_dict.items():
        if flags & bit:
            actions.append(name)
    return actions


class RoomActionsExtractor:
    """Extracts action-related data from ALFRED.1"""

    def __init__(self, alfred1_path: str):
        self.alfred1_path = alfred1_path
        with open(alfred1_path, 'rb') as f:
            self.data = f.read()

    def get_pair_data(self, room_num: int, pair_index: int) -> Tuple[int, bytes]:
        """Get offset and data for a specific pair in a room"""
        room_offset = room_num * 104
        pair_offset_pos = room_offset + (pair_index * 8)
        
        data_offset = struct.unpack('<I', self.data[pair_offset_pos:pair_offset_pos+4])[0]
        data_size = struct.unpack('<I', self.data[pair_offset_pos+4:pair_offset_pos+8])[0]
        
        if data_offset == 0 or data_size == 0:
            return 0, b''
        
        return data_offset, self.data[data_offset:data_offset + data_size]

    def extract_hotspots(self, room_num: int) -> List[Dict[str, Any]]:
        """Extract static hotspots with their action flags"""
        _, pair10_data = self.get_pair_data(room_num, 10)
        
        if len(pair10_data) < 0x47C:
            return []
        
        count = pair10_data[0x47A]
        if count == 0:
            return []
        
        hotspots = []
        for i in range(count):
            offset = 0x47C + i * 9
            if offset + 9 > len(pair10_data):
                break
            
            type_flags = pair10_data[offset]
            x = struct.unpack('<H', pair10_data[offset+1:offset+3])[0]
            y = struct.unpack('<H', pair10_data[offset+3:offset+5])[0]
            w = pair10_data[offset+5]
            h = pair10_data[offset+6]
            extra = struct.unpack('<H', pair10_data[offset+7:offset+9])[0]
            
            # Decode the type/flags byte
            # High bit (0x80) might be enabled flag
            # Low 7 bits are action type flags
            enabled = (type_flags & 0x80) == 0  # Seems inverted
            action_type = type_flags & 0x7F
            
            hotspot = {
                'index': i,
                'type_raw': type_flags,
                'action_type': action_type,
                'enabled': enabled,
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'extra': extra,
                'actions': decode_action_flags(action_type, DISPATCH_FLAGS) if action_type else ['LOOK_ONLY'],
            }
            hotspots.append(hotspot)
        
        return hotspots

    def extract_sprites(self, room_num: int) -> List[Dict[str, Any]]:
        """Extract sprite data with action flags
        
        Sprite structure is 44 bytes (0x2C) with action_flags at +0x22 (34)
        """
        _, pair10_data = self.get_pair_data(room_num, 10)
        
        if len(pair10_data) < 6:
            return []
        
        # Sprite count is at offset 5 in pair10
        sprite_count = pair10_data[5]
        if sprite_count == 0:
            return []
        
        # Sprite data starts at offset 6
        sprites = []
        sprite_base = 6
        sprite_size = 44  # 0x2C bytes per sprite
        
        for i in range(1, sprite_count + 1):  # Sprites are 1-indexed
            offset = sprite_base + (i - 1) * sprite_size
            if offset + sprite_size > len(pair10_data):
                break
            
            sprite_data = pair10_data[offset:offset + sprite_size]
            
            # Key fields for actions
            x = struct.unpack('<H', sprite_data[10:12])[0]  # +0x0A
            y = struct.unpack('<H', sprite_data[12:14])[0]  # +0x0C
            w = sprite_data[14]  # +0x0E
            h = sprite_data[15]  # +0x0F
            
            sprite_type = sprite_data[33]  # +0x21
            action_flags = sprite_data[34]  # +0x22
            is_hotspot = sprite_data[38] if len(sprite_data) > 38 else 0xFF  # +0x26
            
            # Extra ID at +0x2A (42)
            extra_id = struct.unpack('<H', sprite_data[42:44])[0] if len(sprite_data) >= 44 else 0
            
            # Z-order/visibility
            z_order = struct.unpack('<h', sprite_data[8:10])[0]  # +0x08, signed
            
            # A sprite is interactive if:
            # - sprite_type != 0xFF
            # - is_hotspot == 0x00
            # - action_flags != 0x00
            is_interactive = (sprite_type != 0xFF and is_hotspot == 0x00 and action_flags != 0x00)
            
            sprite = {
                'index': i,
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'z_order': z_order,
                'sprite_type': sprite_type,
                'action_flags_raw': action_flags,
                'is_hotspot_byte': is_hotspot,
                'extra_id': extra_id,
                'is_interactive': is_interactive,
                'verb_actions': decode_action_flags(action_flags, SPRITE_ACTION_FLAGS) if action_flags else [],
            }
            
            # Only include sprites that have some action capability
            if action_flags != 0 or is_hotspot == 0:
                sprites.append(sprite)
        
        return sprites

    def extract_exits(self, room_num: int) -> List[Dict[str, Any]]:
        """Extract exit data"""
        _, pair10_data = self.get_pair_data(room_num, 10)
        
        if len(pair10_data) < 0x1BF:
            return []
        
        count = pair10_data[0x1BE]
        if count == 0:
            return []
        
        exits = []
        for i in range(count):
            offset = 0x1BF + i * 14
            if offset + 14 > len(pair10_data):
                break
            
            dest_room = struct.unpack('<H', pair10_data[offset:offset+2])[0]
            flags = pair10_data[offset+2]
            trigger_x = struct.unpack('<H', pair10_data[offset+3:offset+5])[0]
            trigger_y = struct.unpack('<H', pair10_data[offset+5:offset+7])[0]
            trigger_w = pair10_data[offset+7]
            trigger_h = pair10_data[offset+8]
            dest_x = struct.unpack('<H', pair10_data[offset+9:offset+11])[0]
            dest_y = struct.unpack('<H', pair10_data[offset+11:offset+13])[0]
            dest_dir = pair10_data[offset+13]
            
            direction_names = {0: 'RIGHT', 1: 'LEFT', 2: 'DOWN', 3: 'UP'}
            
            exits.append({
                'index': i,
                'destination_room': dest_room,
                'flags': flags,
                'trigger': {'x': trigger_x, 'y': trigger_y, 'w': trigger_w, 'h': trigger_h},
                'spawn': {'x': dest_x, 'y': dest_y, 'direction': direction_names.get(dest_dir, f'UNKNOWN_{dest_dir}')},
            })
        
        return exits

    def extract_room_actions(self, room_num: int) -> Dict[str, Any]:
        """Extract all action-relevant data for a room"""
        hotspots = self.extract_hotspots(room_num)
        sprites = self.extract_sprites(room_num)
        exits = self.extract_exits(room_num)
        
        return {
            'room': room_num,
            'hotspots': hotspots,
            'interactive_sprites': sprites,
            'exits': exits,
            'summary': {
                'total_hotspots': len(hotspots),
                'total_interactive_sprites': len(sprites),
                'total_exits': len(exits),
                'unique_extras': sorted(set(
                    [h['extra'] for h in hotspots] + 
                    [s['extra_id'] for s in sprites if s['extra_id'] > 0]
                )),
            }
        }

    def extract_multiple_rooms(self, room_nums: List[int]) -> List[Dict[str, Any]]:
        """Extract action data for multiple rooms"""
        return [self.extract_room_actions(r) for r in room_nums]


def format_room_output(room_data: Dict[str, Any]) -> str:
    """Format room data for readable output"""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"ROOM {room_data['room']}")
    lines.append(f"{'='*60}")
    
    # Hotspots
    lines.append(f"\nHOTSPOTS ({room_data['summary']['total_hotspots']}):")
    lines.append("-" * 40)
    for h in room_data['hotspots']:
        actions_str = ', '.join(h['actions']) if h['actions'] else 'NONE'
        lines.append(f"  [{h['index']:2d}] extra={h['extra']:4d}  type=0x{h['type_raw']:02X}  "
                    f"({h['x']:3d},{h['y']:3d} {h['width']:3d}x{h['height']:3d})  "
                    f"actions=[{actions_str}]")
    
    # Interactive Sprites
    lines.append(f"\nINTERACTIVE SPRITES ({room_data['summary']['total_interactive_sprites']}):")
    lines.append("-" * 40)
    for s in room_data['interactive_sprites']:
        verbs = ', '.join(s['verb_actions']) if s['verb_actions'] else 'LOOK'
        lines.append(f"  [{s['index']:2d}] extra={s['extra_id']:4d}  flags=0x{s['action_flags_raw']:02X}  "
                    f"z={s['z_order']:3d}  ({s['x']:3d},{s['y']:3d} {s['width']:3d}x{s['height']:3d})  "
                    f"verbs=[{verbs}]  interactive={s['is_interactive']}")
    
    # Exits
    lines.append(f"\nEXITS ({room_data['summary']['total_exits']}):")
    lines.append("-" * 40)
    for e in room_data['exits']:
        lines.append(f"  [{e['index']:2d}] -> Room {e['destination_room']:2d}  "
                    f"trigger=({e['trigger']['x']:3d},{e['trigger']['y']:3d} "
                    f"{e['trigger']['w']:3d}x{e['trigger']['h']:3d})  "
                    f"spawn=({e['spawn']['x']:3d},{e['spawn']['y']:3d} {e['spawn']['direction']})")
    
    # Summary
    lines.append(f"\nUNIQUE EXTRA IDs: {room_data['summary']['unique_extras']}")
    
    return '\n'.join(lines)


def parse_room_range(range_str: str) -> List[int]:
    """Parse room range like '0-5' or '0,1,3,5' or '5'"""
    rooms = []
    for part in range_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            rooms.extend(range(int(start), int(end) + 1))
        else:
            rooms.append(int(part))
    return sorted(set(rooms))


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_room_actions.py <alfred.1> [rooms]")
        print("  rooms: comma/range format like '0-5' or '0,1,3' (default: 0-55)")
        print("\nExample:")
        print("  python extract_room_actions.py files/ALFRED.1 0-5")
        sys.exit(1)
    
    alfred1_path = sys.argv[1]
    room_range = sys.argv[2] if len(sys.argv) > 2 else "0-55"
    
    try:
        rooms = parse_room_range(room_range)
    except ValueError:
        print(f"Error: Invalid room range '{room_range}'")
        sys.exit(1)
    
    print(f"Extracting actions from {alfred1_path} for rooms: {rooms}")
    
    extractor = RoomActionsExtractor(alfred1_path)
    
    all_room_data = []
    for room_num in rooms:
        room_data = extractor.extract_room_actions(room_num)
        all_room_data.append(room_data)
        print(format_room_output(room_data))
    
    # Save JSON output
    output_file = Path(alfred1_path).parent / f"room_actions_{room_range.replace(',', '_').replace('-', '_')}.json"
    with open(output_file, 'w') as f:
        json.dump({
            'description': 'Alfred Pelrock Room Actions Data',
            'dispatch_flags': DISPATCH_FLAGS,
            'sprite_action_flags': SPRITE_ACTION_FLAGS,
            'rooms': all_room_data
        }, f, indent=2)
    
    print(f"\n\nSaved JSON to: {output_file}")


if __name__ == '__main__':
    main()
