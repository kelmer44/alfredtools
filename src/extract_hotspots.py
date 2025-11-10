#!/usr/bin/env python3
"""
Extract hotspot rectangles from ALFRED.1
Produces output in the same format as posiciones*.txt files
"""

import struct
import sys
from pathlib import Path


def extract_hotspots_for_room(data, room_num):
    """Extract hotspot data for a specific room"""

    # Room structure is 104 bytes (13 pairs of offset+size)
    room_offset = room_num * 104

    # Pair 10 contains the room data with hotspots
    pair10_offset_pos = room_offset + (10 * 8)
    pair10_data_offset = struct.unpack('<I', data[pair10_offset_pos:pair10_offset_pos+4])[0]
    pair10_size = struct.unpack('<I', data[pair10_offset_pos+4:pair10_offset_pos+8])[0]

    if pair10_data_offset == 0 or pair10_size == 0:
        return []

    # Hotspot count is at offset 0x47A in Pair 10
    count_offset = pair10_data_offset + 0x47a

    if count_offset >= len(data):
        return []

    count = data[count_offset]

    # Hotspot data starts at offset 0x47C, 9 bytes per hotspot
    # Format: [type][x_low][x_high][y_low][y_high][width][height][extra_low][extra_high]
    hotspots = []
    hotspot_data_start = pair10_data_offset + 0x47c

    for i in range(count):
        obj_offset = hotspot_data_start + i * 9

        if obj_offset + 9 > len(data):
            break

        obj_bytes = data[obj_offset:obj_offset+9]

        type_byte = obj_bytes[0]
        x = obj_bytes[1] | (obj_bytes[2] << 8)
        y = obj_bytes[3] | (obj_bytes[4] << 8)
        w = obj_bytes[5]
        h = obj_bytes[6]
        extra = obj_bytes[7] | (obj_bytes[8] << 8)

        hotspots.append({
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'extra': extra,
            'type': type_byte
        })

    return hotspots


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_hotspots.py <alfred.1> [output_dir]")
        print("\nExample:")
        print("  python extract_hotspots.py ALFRED.1 hotspots/")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "hotspots"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("Extracting hotspots from ALFRED.1...")
    print("="*70)

    total_hotspots = 0
    rooms_with_hotspots = 0

    # Extract for all 56 rooms
    for room_num in range(56):
        hotspots = extract_hotspots_for_room(data, room_num)

        if hotspots:
            output_file = output_path / f"posiciones{room_num}.txt"

            with open(output_file, 'w') as f:
                print(f"\nRoom {room_num} hotspots:")
                for hotspot in hotspots:
                    # Format: x,y,width,height,extra,type
                    f.write(f"{hotspot['x']},{hotspot['y']},{hotspot['width']},{hotspot['height']},{hotspot['extra']},{hotspot['type']}\n")
                    print(f"  At ({hotspot['x']:3d},{hotspot['y']:3d}) size {hotspot['width']}x{hotspot['height']} - Type: {hotspot['type']:02X}h Extra: {hotspot['extra']:04X}h")

            print(f"Room {room_num:2d}: {len(hotspots):2d} hotspots -> {output_file.name}")
            total_hotspots += len(hotspots)
            rooms_with_hotspots += 1

    print("="*70)
    print(f"Extraction complete!")
    print(f"  Rooms with hotspots: {rooms_with_hotspots}/56")
    print(f"  Total hotspots: {total_hotspots}")
    print(f"  Output directory: {output_path.absolute()}")
    print("="*70)


if __name__ == "__main__":
    main()
