#!/usr/bin/env python3
"""
ALFRED.1 ↔ ALFRED.2 Animation Lookup Tool

Practical utilities for mapping between room sprites and talking animations
"""

import struct
from pathlib import Path
from typing import Optional, Dict, List, Tuple

HEADER_SIZE = 55
ROOM_HEADER_SIZE = 0x68

class AlfredAnimationMapper:
    """Maps ALFRED.1 room sprites to ALFRED.2 animations"""

    def __init__(self, alfred1_path: str, alfred2_path: str):
        self.alfred1_path = Path(alfred1_path)
        self.alfred2_path = Path(alfred2_path)
        self._mapping_cache = None

    def get_sprite_action_flags(self, room_id: int, sprite_index: int) -> int:
        """Get the action_flags byte for a specific sprite"""
        with open(self.alfred1_path, 'rb') as f:
            data = f.read()

        # Get room metadata offset
        room_offset = room_id * ROOM_HEADER_SIZE
        pairs = []
        for i in range(13):
            pair_offset = room_offset + (i * 8)
            offset_val = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
            size_val = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]
            pairs.append({'offset': offset_val, 'size': size_val})

        metadata_offset = pairs[10]['offset']
        metadata_size = pairs[10]['size']
        metadata_data = data[metadata_offset:metadata_offset + metadata_size]

        # Sprite structures start at offset 98, each is 44 bytes
        # Sprites are numbered from 2, so actual index is (sprite_index - 2)
        sprite_offset = 98 + (sprite_index - 2) * 44

        if sprite_offset + 44 > len(metadata_data):
            return 0

        sprite_data = metadata_data[sprite_offset:sprite_offset + 44]

        # action_flags is at byte 34 (0x22)
        return sprite_data[34] if len(sprite_data) > 34 else 0

    def sprite_can_talk(self, room_id: int, sprite_index: int) -> bool:
        """Check if a sprite has the TALK action flag"""
        action_flags = self.get_sprite_action_flags(room_id, sprite_index)
        return (action_flags & 0x10) != 0

    def get_animation_index(self, room_id: int, sprite_index: int) -> Optional[int]:
        """
        Get the ALFRED.2 animation index for a specific sprite.
        Returns None if the sprite doesn't have talking animations.
        """
        # Check if this sprite can talk
        if not self.sprite_can_talk(room_id, sprite_index):
            return None

        # Count talking sprites before this one
        counter = 0

        for r in range(room_id):
            num_sprites = self._get_num_sprites_in_room(r)
            for s in range(2, num_sprites):
                if self.sprite_can_talk(r, s):
                    counter += 1

        # Count sprites before this one in the same room
        num_sprites = self._get_num_sprites_in_room(room_id)
        for s in range(2, min(sprite_index, num_sprites)):
            if self.sprite_can_talk(room_id, s):
                counter += 1

        # Now find the actual ALFRED.2 index (skipping empty headers)
        with open(self.alfred2_path, 'rb') as f:
            data = f.read()

        found_count = 0
        offset = 0
        index = 0

        while offset < len(data) - HEADER_SIZE:
            data_offset = struct.unpack('<H', data[offset:offset+2])[0]

            if data_offset != 0:  # Valid header
                if found_count == counter:
                    return index
                found_count += 1

            offset += HEADER_SIZE
            index += 1

            # Safety check
            if index > 100:
                break

        return None

    def _get_num_sprites_in_room(self, room_id: int) -> int:
        """Get the number of sprites in a room"""
        with open(self.alfred1_path, 'rb') as f:
            data = f.read()

        room_offset = room_id * ROOM_HEADER_SIZE
        pairs = []
        for i in range(13):
            pair_offset = room_offset + (i * 8)
            offset_val = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
            size_val = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]
            pairs.append({'offset': offset_val, 'size': size_val})

        metadata_offset = pairs[10]['offset']
        metadata_size = pairs[10]['size']
        metadata_data = data[metadata_offset:metadata_offset + metadata_size]

        return metadata_data[5]

    def get_animation_info(self, animation_index: int) -> Optional[Dict]:
        """Get information about an ALFRED.2 animation"""
        with open(self.alfred2_path, 'rb') as f:
            data = f.read()

        offset = animation_index * HEADER_SIZE

        if offset + HEADER_SIZE > len(data):
            return None

        header_data = data[offset:offset + HEADER_SIZE]
        data_offset = struct.unpack('<H', header_data[0:2])[0]

        if data_offset == 0:
            return None

        return {
            'index': animation_index,
            'data_offset': data_offset,
            'palette_id': (animation_index * 13) + 11,
            'anim1': {
                'width': header_data[9],
                'height': header_data[10],
                'frames': header_data[13],
            },
            'anim2': {
                'width': header_data[21],
                'height': header_data[22],
                'frames': header_data[25],
            }
        }

    def get_sprite_info(self, room_id: int, sprite_index: int) -> Optional[Dict]:
        """Get detailed information about a sprite"""
        with open(self.alfred1_path, 'rb') as f:
            data = f.read()

        room_offset = room_id * ROOM_HEADER_SIZE
        pairs = []
        for i in range(13):
            pair_offset = room_offset + (i * 8)
            offset_val = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
            size_val = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]
            pairs.append({'offset': offset_val, 'size': size_val})

        metadata_offset = pairs[10]['offset']
        metadata_size = pairs[10]['size']
        metadata_data = data[metadata_offset:metadata_offset + metadata_size]

        sprite_offset = 98 + (sprite_index - 2) * 44

        if sprite_offset + 44 > len(metadata_data):
            return None

        sprite_data = metadata_data[sprite_offset:sprite_offset + 44]

        x = struct.unpack('<H', sprite_data[0:2])[0]
        y = struct.unpack('<H', sprite_data[2:4])[0]

        return {
            'room_id': room_id,
            'sprite_index': sprite_index,
            'x': x,
            'y': y,
            'width': sprite_data[4],
            'height': sprite_data[5],
            'num_anims': sprite_data[8],
            'sprite_type': sprite_data[33] if len(sprite_data) > 33 else 0,
            'action_flags': sprite_data[34] if len(sprite_data) > 34 else 0,
            'is_hotspot': sprite_data[38] if len(sprite_data) > 38 else 0,
            'can_talk': self.sprite_can_talk(room_id, sprite_index)
        }

    def find_all_talking_sprites(self) -> List[Tuple[int, int, int]]:
        """
        Find all talking sprites in the game.
        Returns list of (room_id, sprite_index, animation_index) tuples.
        """
        results = []

        for room_id in range(56):
            num_sprites = self._get_num_sprites_in_room(room_id)
            for sprite_index in range(2, num_sprites):
                if self.sprite_can_talk(room_id, sprite_index):
                    anim_idx = self.get_animation_index(room_id, sprite_index)
                    results.append((room_id, sprite_index, anim_idx))

        return results

    def lookup(self, room_id: int, sprite_index: int) -> Dict:
        """
        Complete lookup: sprite info + animation info
        """
        sprite_info = self.get_sprite_info(room_id, sprite_index)

        if not sprite_info or not sprite_info['can_talk']:
            return {
                'sprite': sprite_info,
                'animation': None,
                'can_talk': False
            }

        anim_index = self.get_animation_index(room_id, sprite_index)
        anim_info = self.get_animation_info(anim_index) if anim_index is not None else None

        return {
            'sprite': sprite_info,
            'animation': anim_info,
            'animation_index': anim_index,
            'can_talk': True
        }


# Example usage
def main():
    mapper = AlfredAnimationMapper(
        "/mnt/user-data/uploads/ALFRED.1",
        "/mnt/user-data/uploads/ALFRED.2"
    )

    print("="*80)
    print("ALFRED Animation Lookup Tool")
    print("="*80)

    # Test: Room 2, Sprite 2 (the hooker)
    print("\nTest 1: Room 2, Sprite 2 (The Hooker)")
    print("-" * 80)
    result = mapper.lookup(2, 2)

    if result['can_talk']:
        sprite = result['sprite']
        anim = result['animation']

        print(f"Sprite Info:")
        print(f"  Position: ({sprite['x']}, {sprite['y']})")
        print(f"  Size: {sprite['width']}×{sprite['height']}")
        print(f"  Action Flags: 0x{sprite['action_flags']:02X}")
        print(f"  Can Talk: {'Yes' if sprite['can_talk'] else 'No'}")

        print(f"\nAnimation Info:")
        print(f"  ALFRED.2 Index: {result['animation_index']}")
        print(f"  Palette ID: {anim['palette_id']}")
        print(f"  Animation A: {anim['anim1']['width']}×{anim['anim1']['height']} "
              f"× {anim['anim1']['frames']} frames")
        print(f"  Animation B: {anim['anim2']['width']}×{anim['anim2']['height']} "
              f"× {anim['anim2']['frames']} frames")

    # Find all talking sprites
    print("\n\nTest 2: All Talking Sprites in Game")
    print("-" * 80)
    talking = mapper.find_all_talking_sprites()
    print(f"Found {len(talking)} talking sprites:\n")
    print(f"{'Room':<6} {'Sprite':<8} {'Animation':<10}")
    print("-" * 30)
    for room, sprite, anim in talking[:10]:  # Show first 10
        print(f"{room:<6} {sprite:<8} {anim:<10}")
    print("...")

if __name__ == "__main__":
    main()
