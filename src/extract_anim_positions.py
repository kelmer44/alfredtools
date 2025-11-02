#!/usr/bin/env python3
"""
Alfred Pelrock - Animation/Sprite Extractor
Extracts animation positions and properties from ALFRED.1

Animations are dynamic sprites rendered on top of the static background.
They include things like flickering flames, steam, moving objects, etc.

Structure in Pair 10:
  Offset 0x05: animation count (1 byte)
  Offset 0x06: animation array (44 bytes per animation)

Each animation structure (44 bytes / 0x2C):
  +0x00-0x03: sprite_data_pointer (uint32) - pointer to sprite pixel data
  +0x04-0x05: x (uint16) - screen x coordinate
  +0x06-0x07: y (uint16) - screen y coordinate
  +0x08:      width (uint8) - sprite width in pixels
  +0x09:      height (uint8) - sprite height in pixels
  +0x0A-0x0B: stride (uint16) - bytes per scanline
  +0x0C:      total_frames (uint8) - number of animation frames
  +0x0D+:     additional fields (frame counters, flags, z-order)

Note: sprite_data_pointer is often 0x00000000 as sprite data is loaded
dynamically at runtime from other resource files.
"""

import struct
import json
import sys
from pathlib import Path

def extract_animations_from_room(data, room_num):
    """Extract animation data for a single room"""
    room_offset = room_num * 104
    pair10_offset = room_offset + (10 * 8)
    offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
    size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

    if size == 0 or offset >= len(data):
        return None

    pair10_data = data[offset:offset+size]

    # Animation count at 0x05
    if 0x05 >= len(pair10_data):
        return None

    anim_count = pair10_data[0x05]
    if anim_count == 0:
        return []

    animations = []
    anim_base = 0x06

    for i in range(anim_count):
        entry_base = anim_base + (i * 44)

        if entry_base + 44 > len(pair10_data):
            break

        sprite_ptr = struct.unpack('<I', pair10_data[entry_base:entry_base+4])[0]
        x = struct.unpack('<H', pair10_data[entry_base+4:entry_base+6])[0]
        y = struct.unpack('<H', pair10_data[entry_base+6:entry_base+8])[0]
        width = pair10_data[entry_base+8]
        height = pair10_data[entry_base+9]
        stride = struct.unpack('<H', pair10_data[entry_base+10:entry_base+12])[0]
        total_frames = pair10_data[entry_base+12]

        # Skip empty entries (all zeros)
        if x == 0 and y == 0 and width == 0 and height == 0:
            continue

        # Validate reasonable values (screen is 640x400)
        if x < 640 and y < 400 and width > 0 and height > 0:
            animations.append({
                'index': i,
                'position': {
                    'x': x,
                    'y': y
                },
                'size': {
                    'width': width,
                    'height': height
                },
                'frames': total_frames,
                'stride': stride,
                'sprite_pointer': sprite_ptr
            })

    return animations if animations else None

def extract_all_animations(alfred1_path, output_dir=None):
    """Extract animations from all rooms"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - Animation/Sprite Extractor")
    print("=" * 70)
    print()

    NUM_ROOMS = 56
    total_animations = 0
    all_rooms = []

    for room_num in range(NUM_ROOMS):
        animations = extract_animations_from_room(data, room_num)

        if animations:
            all_rooms.append({
                'room': room_num,
                'animations': animations
            })
            total_animations += len(animations)

            print(f"Room {room_num:2d}: {len(animations):2d} animation(s)")
            for anim in animations:
                pos = anim['position']
                size = anim['size']
                print(f"  Anim {anim['index']:2d}: ({pos['x']:3d},{pos['y']:3d}) "
                      f"{size['width']:3d}×{size['height']:3d} "
                      f"[{anim['frames']} frame(s)]")
        else:
            print(f"Room {room_num:2d}: No animations")

    print()
    print("=" * 70)
    print(f"Total: {len(all_rooms)} rooms with {total_animations} animations")

    # Save to files if output directory specified
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save as JSON
        json_file = output_path / "animations.json"
        with open(json_file, 'w') as f:
            json.dump({
                'description': 'Alfred Pelrock room animations/sprites',
                'note': 'These are dynamic sprites rendered on top of backgrounds',
                'rooms': all_rooms
            }, f, indent=2)

        print(f"Saved to: {json_file}")

        # Save as Python
        py_file = output_path / "animations.py"
        with open(py_file, 'w') as f:
            f.write("# Alfred Pelrock - Room Animations\n\n")
            f.write("ANIMATIONS = {\n")
            for room_data in all_rooms:
                f.write(f"    {room_data['room']}: [\n")
                for anim in room_data['animations']:
                    f.write(f"        {anim},\n")
                f.write("    ],\n")
            f.write("}\n")

        print(f"Saved to: {py_file}")

        # Save as text
        txt_file = output_path / "animations.txt"
        with open(txt_file, 'w') as f:
            f.write("Alfred Pelrock - Room Animations/Sprites\n")
            f.write("=" * 70 + "\n\n")

            for room_data in all_rooms:
                f.write(f"Room {room_data['room']}:\n")
                for anim in room_data['animations']:
                    pos = anim['position']
                    size = anim['size']
                    f.write(f"  Animation {anim['index']}:\n")
                    f.write(f"    Position: ({pos['x']}, {pos['y']})\n")
                    f.write(f"    Size: {size['width']}×{size['height']}\n")
                    f.write(f"    Frames: {anim['frames']}\n")
                    f.write(f"    Stride: {anim['stride']}\n")
                    f.write("\n")
                f.write("\n")

        print(f"Saved to: {txt_file}")

    return all_rooms

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_animations.py <alfred.1> [output_dir]")
        print("\nExample:")
        print("  python extract_animations.py ALFRED.1 animations/")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "animations"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    extract_all_animations(alfred1_path, output_dir)

if __name__ == "__main__":
    main()
