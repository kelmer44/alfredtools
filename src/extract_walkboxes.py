#!/usr/bin/env python3
import struct
import sys
import json
from pathlib import Path

def extract_walkboxes(alfred1_path, output_dir):
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    all_rooms = []

    for room_num in range(56):
        room_offset = room_num * 104
        pair10_offset = room_offset + (10 * 8)
        offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
        size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

        if size == 0 or offset >= len(data):
            continue

        pair10_data = data[offset:offset+size]

        if 0x213 >= len(pair10_data):
            continue

        walkbox_count = pair10_data[0x213]
        walkbox_offset = 0x218

        walkboxes = []
        for i in range(walkbox_count):
            box_offset = walkbox_offset + (i * 9)

            if box_offset + 9 > len(pair10_data):
                break

            x = struct.unpack('<H', pair10_data[box_offset:box_offset+2])[0]
            y = struct.unpack('<H', pair10_data[box_offset+2:box_offset+4])[0]
            w = struct.unpack('<H', pair10_data[box_offset+4:box_offset+6])[0]
            h = struct.unpack('<H', pair10_data[box_offset+6:box_offset+8])[0]
            flags = pair10_data[box_offset+8]

            walkboxes.append({'x': x, 'y': y, 'width': w, 'height': h, 'flags': flags})

        if walkboxes:
            all_rooms.append({'room': room_num, 'walkboxes': walkboxes})

    with open(output_path / "walkboxes.json", 'w') as f:
        json.dump({'rooms': all_rooms}, f, indent=2)

    with open(output_path / "walkboxes.py", 'w') as f:
        f.write("WALKBOXES = {\n")
        for room_data in all_rooms:
            f.write(f"    {room_data['room']}: [\n")
            for box in room_data['walkboxes']:
                f.write(f"        {box},\n")
            f.write("    ],\n")
        f.write("}\n")

    print(f"Extracted {sum(len(r['walkboxes']) for r in all_rooms)} walkboxes from {len(all_rooms)} rooms")
    print(f"Output: {output_path.absolute()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_walkboxes.py <alfred.1> [output_dir]")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "walkboxes"

    extract_walkboxes(alfred1_path, output_dir)
