#!/usr/bin/env python3
"""
Alfred Pelrock - Comprehensive Room Data Extractor
Extracts hotspots, walkboxes, and exits from ALFRED.1

This script combines the functionality of:
- extract_hotspots.py: Interactive hotspot rectangles
- extract_walkboxes.py: Walkable area definitions
- extract_exits.py: Room connections and transitions

Usage:
    python extract_room_data.py <alfred.1> [output_dir] [--format json|txt|py|all]

Data Structures in Pair 10:
  Hotspots:
    - Offset 0x47A: count (1 byte)
    - Offset 0x47C: array (9 bytes per hotspot)

  Walkboxes:
    - Offset 0x213: count (1 byte)
    - Offset 0x218: array (9 bytes per walkbox)

  Exits:
    - Offset 0x1BE: count (1 byte)
    - Offset 0x1BF: array (14 bytes per exit)
"""

import struct
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class RoomDataExtractor:
    """Extracts all room data from ALFRED.1"""

    def __init__(self, alfred1_path: str):
        self.alfred1_path = alfred1_path
        with open(alfred1_path, 'rb') as f:
            self.data = f.read()

    def extract_hotspots(self, room_num: int) -> Optional[List[Dict[str, Any]]]:
        """Extract hotspot rectangles for a specific room

        Hotspots are interactive areas (9 bytes each):
          [type][x_low][x_high][y_low][y_high][width][height][extra_low][extra_high]
        """
        room_offset = room_num * 104
        pair10_offset_pos = room_offset + (10 * 8)
        pair10_data_offset = struct.unpack('<I', self.data[pair10_offset_pos:pair10_offset_pos+4])[0]
        pair10_size = struct.unpack('<I', self.data[pair10_offset_pos+4:pair10_offset_pos+8])[0]

        if pair10_data_offset == 0 or pair10_size == 0:
            return None

        count_offset = pair10_data_offset + 0x47a
        if count_offset >= len(self.data):
            return None

        count = self.data[count_offset]
        if count == 0:
            return []

        hotspots = []
        hotspot_data_start = pair10_data_offset + 0x47c

        for i in range(count):
            obj_offset = hotspot_data_start + i * 9
            if obj_offset + 9 > len(self.data):
                break

            obj_bytes = self.data[obj_offset:obj_offset+9]
            type_byte = obj_bytes[0]
            x = obj_bytes[1] | (obj_bytes[2] << 8)
            y = obj_bytes[3] | (obj_bytes[4] << 8)
            w = obj_bytes[5]
            h = obj_bytes[6]
            extra = obj_bytes[7] | (obj_bytes[8] << 8)

            hotspots.append({
                'type': type_byte,
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'extra': extra
            })

        return hotspots if hotspots else None

    def extract_walkboxes(self, room_num: int) -> Optional[List[Dict[str, Any]]]:
        """Extract walkable area boxes for a specific room

        Walkboxes define where the character can walk (9 bytes each):
          [x_low][x_high][y_low][y_high][w_low][w_high][h_low][h_high][flags]
        """
        room_offset = room_num * 104
        pair10_offset = room_offset + (10 * 8)
        offset = struct.unpack('<I', self.data[pair10_offset:pair10_offset+4])[0]
        size = struct.unpack('<I', self.data[pair10_offset+4:pair10_offset+8])[0]

        if size == 0 or offset >= len(self.data):
            return None

        pair10_data = self.data[offset:offset+size]

        if 0x213 >= len(pair10_data):
            return None

        walkbox_count = pair10_data[0x213]
        if walkbox_count == 0:
            return []

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

            walkboxes.append({
                'x': x,
                'y': y,
                'width': w,
                'height': h,
                'flags': flags
            })

        return walkboxes if walkboxes else None

    def extract_exits(self, room_num: int) -> Optional[List[Dict[str, Any]]]:
        """Extract exit/connection data for a specific room

        Exits are trigger zones that transition to other rooms (14 bytes each):
          [dest_room_low][dest_room_high][flags]
          [trigger_x_low][trigger_x_high][trigger_y_low][trigger_y_high]
          [trigger_width][trigger_height]
          [dest_x_low][dest_x_high][dest_y_low][dest_y_high]
          [dest_direction]
        """
        room_offset = room_num * 104
        pair10_offset = room_offset + (10 * 8)
        offset = struct.unpack('<I', self.data[pair10_offset:pair10_offset+4])[0]
        size = struct.unpack('<I', self.data[pair10_offset+4:pair10_offset+8])[0]

        if size == 0 or offset >= len(self.data):
            return None

        pair10_data = self.data[offset:offset+size]

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

    def extract_room(self, room_num: int) -> Dict[str, Any]:
        """Extract all data for a single room"""
        return {
            'room': room_num,
            'hotspots': self.extract_hotspots(room_num),
            'walkboxes': self.extract_walkboxes(room_num),
            'exits': self.extract_exits(room_num)
        }

    def extract_all_rooms(self, num_rooms: int = 56) -> List[Dict[str, Any]]:
        """Extract data for all rooms"""
        return [self.extract_room(i) for i in range(num_rooms)]


class OutputWriter:
    """Handles writing extracted data in various formats"""

    def __init__(self, output_dir: str):
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def write_json(self, rooms_data: List[Dict[str, Any]]):
        """Write combined JSON file with all room data"""
        json_file = self.output_path / "room_data.json"

        output = {
            'description': 'Alfred Pelrock comprehensive room data',
            'game': 'Alfred Pelrock (1997)',
            'source': 'ALFRED.1',
            'directions': {
                '0': 'right',
                '1': 'left',
                '2': 'down',
                '3': 'up'
            },
            'rooms': rooms_data
        }

        with open(json_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"  JSON: {json_file}")
        return json_file

    def write_python(self, rooms_data: List[Dict[str, Any]]):
        """Write Python module with separate dictionaries"""
        py_file = self.output_path / "room_data.py"

        with open(py_file, 'w') as f:
            f.write("# Alfred Pelrock - Room Data\n")
            f.write("# Auto-generated from ALFRED.1\n\n")

            # Hotspots
            f.write("# Interactive hotspot rectangles\n")
            f.write("HOTSPOTS = {\n")
            for room in rooms_data:
                if room['hotspots']:
                    f.write(f"    {room['room']}: [\n")
                    for hotspot in room['hotspots']:
                        f.write(f"        {hotspot},\n")
                    f.write("    ],\n")
            f.write("}\n\n")

            # Walkboxes
            f.write("# Walkable area definitions\n")
            f.write("WALKBOXES = {\n")
            for room in rooms_data:
                if room['walkboxes']:
                    f.write(f"    {room['room']}: [\n")
                    for walkbox in room['walkboxes']:
                        f.write(f"        {walkbox},\n")
                    f.write("    ],\n")
            f.write("}\n\n")

            # Exits
            f.write("# Room exits and connections\n")
            f.write("EXITS = {\n")
            for room in rooms_data:
                if room['exits']:
                    f.write(f"    {room['room']}: [\n")
                    for exit_data in room['exits']:
                        f.write(f"        {exit_data},\n")
                    f.write("    ],\n")
            f.write("}\n")

        print(f"  Python: {py_file}")
        return py_file

    def write_text(self, rooms_data: List[Dict[str, Any]]):
        """Write human-readable text summary"""
        txt_file = self.output_path / "room_data.txt"

        with open(txt_file, 'w') as f:
            f.write("Alfred Pelrock - Comprehensive Room Data\n")
            f.write("=" * 70 + "\n\n")

            for room in rooms_data:
                room_num = room['room']
                has_data = any([room['hotspots'], room['walkboxes'], room['exits']])

                if not has_data:
                    continue

                f.write(f"Room {room_num}\n")
                f.write("-" * 70 + "\n")

                # Hotspots
                if room['hotspots']:
                    f.write(f"  Hotspots ({len(room['hotspots'])}):\n")
                    for i, hotspot in enumerate(room['hotspots']):
                        f.write(f"    [{i}] Type {hotspot['type']}: "
                               f"({hotspot['x']}, {hotspot['y']}) "
                               f"{hotspot['width']}x{hotspot['height']} "
                               f"extra={hotspot['extra']}\n")
                    f.write("\n")

                # Walkboxes
                if room['walkboxes']:
                    f.write(f"  Walkboxes ({len(room['walkboxes'])}):\n")
                    for i, walkbox in enumerate(room['walkboxes']):
                        f.write(f"    [{i}] ({walkbox['x']}, {walkbox['y']}) "
                               f"{walkbox['width']}x{walkbox['height']} "
                               f"flags=0x{walkbox['flags']:02X}\n")
                    f.write("\n")

                # Exits
                if room['exits']:
                    f.write(f"  Exits ({len(room['exits'])}):\n")
                    for i, exit_data in enumerate(room['exits']):
                        trig = exit_data['trigger']
                        dest = exit_data['destination']
                        direction_names = ['right', 'left', 'down', 'up']
                        dir_name = direction_names[dest['direction']] if dest['direction'] < 4 else f"unknown({dest['direction']})"

                        f.write(f"    [{i}] Trigger: ({trig['x']}, {trig['y']}) "
                               f"{trig['width']}x{trig['height']}\n")
                        f.write(f"        → Room {exit_data['destination_room']} "
                               f"at ({dest['x']}, {dest['y']}) "
                               f"facing {dir_name}\n")
                    f.write("\n")

                f.write("\n")

        print(f"  Text: {txt_file}")
        return txt_file

    def write_separate_hotspots(self, rooms_data: List[Dict[str, Any]]):
        """Write individual hotspot files (compatible with posiciones*.txt format)"""
        hotspots_dir = self.output_path / "hotspots"
        hotspots_dir.mkdir(exist_ok=True)

        count = 0
        for room in rooms_data:
            if room['hotspots']:
                hotspot_file = hotspots_dir / f"posiciones{room['room']}.txt"
                with open(hotspot_file, 'w') as f:
                    for hotspot in room['hotspots']:
                        f.write(f"{hotspot['x']},{hotspot['y']},{hotspot['width']},{hotspot['height']},{hotspot['extra']}\n")
                count += 1

        print(f"  Hotspots: {count} files in {hotspots_dir}")
        return hotspots_dir


def print_summary(rooms_data: List[Dict[str, Any]]):
    """Print extraction summary to console"""
    print("\nExtraction Summary:")
    print("=" * 70)

    total_hotspots = sum(len(r['hotspots']) for r in rooms_data if r['hotspots'])
    total_walkboxes = sum(len(r['walkboxes']) for r in rooms_data if r['walkboxes'])
    total_exits = sum(len(r['exits']) for r in rooms_data if r['exits'])

    rooms_with_hotspots = sum(1 for r in rooms_data if r['hotspots'])
    rooms_with_walkboxes = sum(1 for r in rooms_data if r['walkboxes'])
    rooms_with_exits = sum(1 for r in rooms_data if r['exits'])

    print(f"  Hotspots:  {total_hotspots:3d} items in {rooms_with_hotspots:2d} rooms")
    print(f"  Walkboxes: {total_walkboxes:3d} items in {rooms_with_walkboxes:2d} rooms")
    print(f"  Exits:     {total_exits:3d} items in {rooms_with_exits:2d} rooms")
    print(f"  Total rooms: {len(rooms_data)}")

    return {
        'hotspots': total_hotspots,
        'walkboxes': total_walkboxes,
        'exits': total_exits
    }


def print_detailed_report(rooms_data: List[Dict[str, Any]]):
    """Print detailed room-by-room report"""
    print("\nDetailed Room Report:")
    print("=" * 70)
    print(f"{'Room':<6} {'Hotspots':<10} {'Walkboxes':<11} {'Exits':<10}")
    print("-" * 70)

    for room in rooms_data:
        h_count = len(room['hotspots']) if room['hotspots'] else 0
        w_count = len(room['walkboxes']) if room['walkboxes'] else 0
        e_count = len(room['exits']) if room['exits'] else 0

        if h_count or w_count or e_count:
            print(f"{room['room']:<6} {h_count:<10} {w_count:<11} {e_count:<10}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_room_data.py <alfred.1> [output_dir] [--format json|txt|py|all]")
        print("\nExamples:")
        print("  python extract_room_data.py ALFRED.1")
        print("  python extract_room_data.py ALFRED.1 output/")
        print("  python extract_room_data.py ALFRED.1 output/ --format json")
        print("  python extract_room_data.py ALFRED.1 output/ --format all")
        print("\nOutput formats:")
        print("  json - Single JSON file with all data")
        print("  py   - Python module with dictionaries")
        print("  txt  - Human-readable text summary")
        print("  all  - All formats (default)")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = "output" if len(sys.argv) < 3 else sys.argv[2]

    # Parse format argument
    output_format = "all"
    if len(sys.argv) >= 4 and sys.argv[-2] == "--format":
        output_format = sys.argv[-1]
    elif len(sys.argv) >= 3 and sys.argv[-1].startswith("--format="):
        output_format = sys.argv[-1].split("=")[1]

    if output_format not in ['json', 'txt', 'py', 'all']:
        print(f"Error: Invalid format '{output_format}'. Must be json, txt, py, or all")
        sys.exit(1)

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    print("Alfred Pelrock - Comprehensive Room Data Extractor")
    print("=" * 70)
    print(f"Source: {alfred1_path}")
    print(f"Output: {output_dir}/")
    print(f"Format: {output_format}")
    print()

    # Extract all data
    print("Extracting room data...")
    extractor = RoomDataExtractor(alfred1_path)
    rooms_data = extractor.extract_all_rooms()

    # Print summary
    print_summary(rooms_data)
    print_detailed_report(rooms_data)

    # Write output files
    print("\nWriting output files:")
    print("-" * 70)
    writer = OutputWriter(output_dir)

    if output_format in ['json', 'all']:
        writer.write_json(rooms_data)

    if output_format in ['py', 'all']:
        writer.write_python(rooms_data)

    if output_format in ['txt', 'all']:
        writer.write_text(rooms_data)

    # Always write separate hotspot files for compatibility
    writer.write_separate_hotspots(rooms_data)

    print("=" * 70)
    print(f"Extraction complete! Output saved to: {Path(output_dir).absolute()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
