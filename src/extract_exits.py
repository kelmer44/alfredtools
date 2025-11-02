"""
Alfred Pelrock - Exit/Connection Extractor
Extracts room exits (doorways, passages, etc.) from ALFRED.1

Exits are trigger zones that, when entered by the character,
load a new room and place the character at specific coordinates.

Structure in Pair 10:
  Offset 0x1BE: exit count (1 byte)
  Offset 0x1BF: exit array (14 bytes per exit)

Each exit structure (14 bytes):
  +0x00-0x01: destination_room (uint16 LE)
  +0x02:      flags (uint8) - usually 0x00
  +0x03-0x04: trigger_x (uint16 LE)
  +0x05-0x06: trigger_y (uint16 LE)
  +0x07:      trigger_width (uint8)
  +0x08:      trigger_height (uint8)
  +0x09-0x0A: destination_x (uint16 LE)
  +0x0B-0x0C: destination_y (uint16 LE)
  +0x0D:      destination_direction (uint8) - 0=right, 1=left, 2=down, 3=up
"""

import struct
import json
import sys
from pathlib import Path

def extract_exits_from_room(data, room_num):
    """Extract exit data for a single room"""
    room_offset = room_num * 104
    pair10_offset = room_offset + (10 * 8)
    offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
    size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

    if size == 0 or offset >= len(data):
        return None

    pair10_data = data[offset:offset+size]

    # Exit count at 0x1BE
    if 0x1BE >= len(pair10_data):
        return None

    exit_count = pair10_data[0x1BE]
    if exit_count == 0:
        return []

    exits = []
    exit_base = 0x1BF

    for i in range(exit_count):
        entry_base = exit_base + (i * 14)

        if entry_base + 14 > len(pair10_data):
            break

        dest_room = struct.unpack('<H', pair10_data[entry_base:entry_base+2])[0]
        flags = pair10_data[entry_base+2]
        trigger_x = struct.unpack('<H', pair10_data[entry_base+3:entry_base+5])[0]
        trigger_y = struct.unpack('<H', pair10_data[entry_base+5:entry_base+7])[0]
        trigger_w = pair10_data[entry_base+7]
        trigger_h = pair10_data[entry_base+8]
        dest_x = struct.unpack('<H', pair10_data[entry_base+9:entry_base+11])[0]
        dest_y = struct.unpack('<H', pair10_data[entry_base+11:entry_base+13])[0]
        dest_dir = pair10_data[entry_base+13]

        # Validate reasonable values (screen is 640x400)
        if trigger_x < 640 and trigger_y < 400 and dest_x < 640 and dest_y < 400:
            exits.append({
                'destination_room': dest_room,
                'trigger': {
                    'x': trigger_x,
                    'y': trigger_y,
                    'width': trigger_w,
                    'height': trigger_h
                },
                'destination': {
                    'x': dest_x,
                    'y': dest_y,
                    'direction': dest_dir
                },
                'flags': flags
            })

    return exits if exits else None

def extract_all_exits(alfred1_path, output_dir=None):
    """Extract exits from all rooms"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - Exit/Connection Extractor")
    print("=" * 70)
    print()

    NUM_ROOMS = 56
    total_exits = 0
    all_rooms = []

    for room_num in range(NUM_ROOMS):
        exits = extract_exits_from_room(data, room_num)

        if exits:
            all_rooms.append({
                'room': room_num,
                'exits': exits
            })
            total_exits += len(exits)

            print(f"Room {room_num:2d}: {len(exits):2d} exit(s)")
            for i, exit_data in enumerate(exits):
                trig = exit_data['trigger']
                dest = exit_data['destination']
                print(f"  Exit {i}: [{trig['x']:3d},{trig['y']:3d} {trig['width']}x{trig['height']}] "
                      f"→ Room {exit_data['destination_room']:2d} "
                      f"at ({dest['x']:3d},{dest['y']:3d}) dir={dest['direction']}")
        else:
            print(f"Room {room_num:2d}: No exits")

    print()
    print("=" * 70)
    print(f"Total: {len(all_rooms)} rooms with {total_exits} exits")

    # Save to files if output directory specified
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save as JSON
        json_file = output_path / "exits.json"
        with open(json_file, 'w') as f:
            json.dump({
                'description': 'Alfred Pelrock room exits/connections',
                'directions': {
                    '0': 'right',
                    '1': 'left',
                    '2': 'down',
                    '3': 'up'
                },
                'rooms': all_rooms
            }, f, indent=2)

        print(f"Saved to: {json_file}")

        # Save as Python
        py_file = output_path / "exits.py"
        with open(py_file, 'w') as f:
            f.write("# Alfred Pelrock - Room Exits\n\n")
            f.write("EXITS = {\n")
            for room_data in all_rooms:
                f.write(f"    {room_data['room']}: [\n")
                for exit_data in room_data['exits']:
                    f.write(f"        {exit_data},\n")
                f.write("    ],\n")
            f.write("}\n")

        print(f"Saved to: {py_file}")

        # Save as text
        txt_file = output_path / "exits.txt"
        with open(txt_file, 'w') as f:
            f.write("Alfred Pelrock - Room Exits/Connections\n")
            f.write("=" * 70 + "\n\n")

            for room_data in all_rooms:
                f.write(f"Room {room_data['room']}:\n")
                for i, exit_data in enumerate(room_data['exits']):
                    trig = exit_data['trigger']
                    dest = exit_data['destination']
                    f.write(f"  Exit {i}:\n")
                    f.write(f"    Trigger: ({trig['x']}, {trig['y']}) {trig['width']}x{trig['height']}\n")
                    f.write(f"    Goes to: Room {exit_data['destination_room']}\n")
                    f.write(f"    Player placed at: ({dest['x']}, {dest['y']})\n")
                    f.write(f"    Facing: {['right', 'left', 'down', 'up'][dest['direction']]}\n")
                    f.write("\n")
                f.write("\n")

        print(f"Saved to: {txt_file}")

    return all_rooms

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_exits.py <alfred.1> [output_dir]")
        print("\nExample:")
        print("  python extract_exits.py ALFRED.1 exits/")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "exits"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    extract_all_exits(alfred1_path, output_dir)

if __name__ == "__main__":
    main()


