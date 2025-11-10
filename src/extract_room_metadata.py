#!/usr/bin/env python3
"""
extract_room_metadata.py

Unified room metadata extractor for Alfred Pelrock.
Extracts all metadata from room Pair 10 data blocks:
  - Hotspots (interactive objects)
  - Exits (room connections/doorways)
  - Walkboxes (walkable areas)
  - Hover areas (cursor change regions)

All data is stored in a single unified JSON file.
"""

import struct
import json
import argparse
from pathlib import Path


def extract_pair10_data(data, room_num):
    """Get Pair 10 data block for a room."""
    room_offset = room_num * 104
    pair10_header_offset = room_offset + (10 * 8)

    if pair10_header_offset + 8 > len(data):
        return None, None, None

    offset = struct.unpack('<I', data[pair10_header_offset:pair10_header_offset + 4])[0]
    size = struct.unpack('<I', data[pair10_header_offset + 4:pair10_header_offset + 8])[0]

    if size == 0 or offset >= len(data):
        return None, None, None

    pair10_data = data[offset:offset + size]
    return offset, size, pair10_data


def extract_hotspots(pair10_data):
    """
    Extract hotspot rectangles.

    Structure in Pair 10:
      Offset 0x47A: hotspot count (1 byte)
      Offset 0x47C: hotspot array (9 bytes per hotspot)

    Each hotspot (9 bytes):
      +0x00: type (uint8)
      +0x01-0x02: x (uint16 LE)
      +0x03-0x04: y (uint16 LE)
      +0x05: width (uint8)
      +0x06: height (uint8)
      +0x07-0x08: extra/action_id (uint16 LE)
    """
    if 0x47A >= len(pair10_data):
        return []

    count = pair10_data[0x47A]
    if count == 0:
        return []

    hotspots = []
    hotspot_base = 0x47C

    for i in range(count):
        offset = hotspot_base + (i * 9)
        if offset + 9 > len(pair10_data):
            break

        obj_bytes = pair10_data[offset:offset + 9]
        hotspots.append({
            'index': i,
            'type': obj_bytes[0],
            'x': obj_bytes[1] | (obj_bytes[2] << 8),
            'y': obj_bytes[3] | (obj_bytes[4] << 8),
            'width': obj_bytes[5],
            'height': obj_bytes[6],
            'extra': obj_bytes[7] | (obj_bytes[8] << 8)
        })

    return hotspots


def extract_exits(pair10_data):
    """
    Extract exit/connection data.

    Structure in Pair 10:
      Offset 0x1BE: exit count (1 byte)
      Offset 0x1BF: exit array (14 bytes per exit)

    Each exit (14 bytes):
      +0x00-0x01: destination_room (uint16 LE)
      +0x02: flags (uint8)
      +0x03-0x04: trigger_x (uint16 LE)
      +0x05-0x06: trigger_y (uint16 LE)
      +0x07: trigger_width (uint8)
      +0x08: trigger_height (uint8)
      +0x09-0x0A: destination_x (uint16 LE)
      +0x0B-0x0C: destination_y (uint16 LE)
      +0x0D: destination_direction (uint8) - 0=right, 1=left, 2=down, 3=up
    """
    if 0x1BE >= len(pair10_data):
        return []

    exit_count = pair10_data[0x1BE]
    if exit_count == 0:
        return []

    exits = []
    exit_base = 0x1BF

    for i in range(exit_count):
        offset = exit_base + (i * 14)
        if offset + 14 > len(pair10_data):
            break

        dest_room = struct.unpack('<H', pair10_data[offset:offset + 2])[0]
        flags = pair10_data[offset + 2]
        trigger_x = struct.unpack('<H', pair10_data[offset + 3:offset + 5])[0]
        trigger_y = struct.unpack('<H', pair10_data[offset + 5:offset + 7])[0]
        trigger_w = pair10_data[offset + 7]
        trigger_h = pair10_data[offset + 8]
        dest_x = struct.unpack('<H', pair10_data[offset + 9:offset + 11])[0]
        dest_y = struct.unpack('<H', pair10_data[offset + 11:offset + 13])[0]
        dest_dir = pair10_data[offset + 13]

        # Validate coordinates are within screen bounds (640x400)
        if trigger_x < 640 and trigger_y < 400 and dest_x < 640 and dest_y < 400:
            exits.append({
                'index': i,
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
                    'direction': dest_dir,
                    'direction_name': ['right', 'left', 'down', 'up'][dest_dir] if dest_dir < 4 else 'unknown'
                },
                'flags': flags
            })

    return exits


def extract_walkboxes(pair10_data):
    """
    Extract walkbox (walkable area) data.

    Structure in Pair 10:
      Offset 0x213: walkbox count (1 byte)
      Offset 0x218: walkbox array (9 bytes per box)

    Each walkbox (9 bytes):
      +0x00-0x01: x (uint16 LE)
      +0x02-0x03: y (uint16 LE)
      +0x04-0x05: width (uint16 LE)
      +0x06-0x07: height (uint16 LE)
      +0x08: flags (uint8)
    """
    if 0x213 >= len(pair10_data):
        return []

    count = pair10_data[0x213]
    if count == 0:
        return []

    walkboxes = []
    walkbox_base = 0x218

    for i in range(count):
        offset = walkbox_base + (i * 9)
        if offset + 9 > len(pair10_data):
            break

        x = struct.unpack('<H', pair10_data[offset:offset + 2])[0]
        y = struct.unpack('<H', pair10_data[offset + 2:offset + 4])[0]
        w = struct.unpack('<H', pair10_data[offset + 4:offset + 6])[0]
        h = struct.unpack('<H', pair10_data[offset + 6:offset + 8])[0]
        flags = pair10_data[offset + 8]

        walkboxes.append({
            'index': i,
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'flags': flags
        })

    return walkboxes


def extract_hover_areas(pair10_data, min_size=10):
    """
    Extract potential hover/cursor-change areas.

    This is a heuristic scan looking for coordinate-like patterns
    (x, y, width, height) scattered throughout the Pair 10 data.
    These regions correspond to where the mouse cursor changes.

    Filters by minimum size to reduce noise.
    """
    areas = []
    seen = set()

    # Scan the entire pair10 block for coordinate-like structures
    for scan_offset in range(0, len(pair10_data) - 6, 1):
        # Try both alignments (0 and 3) - different data may be aligned differently
        for align in (0, 3):
            pos = scan_offset + align
            if pos + 6 > len(pair10_data):
                continue

            try:
                x = struct.unpack('<H', pair10_data[pos:pos + 2])[0]
                y = struct.unpack('<H', pair10_data[pos + 2:pos + 4])[0]
                w = pair10_data[pos + 4]
                h = pair10_data[pos + 5]

                # Validate: within screen bounds and reasonable size
                if not (0 <= x < 640 and 0 <= y < 400 and min_size <= w < 200 and min_size <= h < 200):
                    continue

                # Deduplicate
                key = (x, y, w, h)
                if key in seen:
                    continue
                seen.add(key)

                # Classify by screen region
                if x > 500:
                    region = 'right'
                elif x < 100:
                    region = 'left'
                else:
                    region = 'center'

                areas.append({
                    'offset': pos,
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'region': region
                })
            except Exception:
                continue

    return areas


def extract_room_metadata(data, room_num, include_hover=True, hover_min_size=10):
    """Extract all metadata for a single room."""
    offset, size, pair10_data = extract_pair10_data(data, room_num)

    if pair10_data is None:
        return None

    metadata = {
        'room': room_num,
        'pair10_offset': offset,
        'pair10_size': size,
        'hotspots': extract_hotspots(pair10_data),
        'exits': extract_exits(pair10_data),
        'walkboxes': extract_walkboxes(pair10_data)
    }

    if include_hover:
        metadata['hover_areas'] = extract_hover_areas(pair10_data, hover_min_size)

    return metadata


def extract_all_rooms(alfred1_path, max_rooms=56, include_hover=True, hover_min_size=10):
    """Extract metadata for all rooms."""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    rooms = []
    for room_num in range(max_rooms):
        metadata = extract_room_metadata(data, room_num, include_hover, hover_min_size)
        if metadata:
            rooms.append(metadata)

    return rooms


def print_summary(rooms):
    """Print a summary of extracted data."""
    total_hotspots = sum(len(r['hotspots']) for r in rooms)
    total_exits = sum(len(r['exits']) for r in rooms)
    total_walkboxes = sum(len(r['walkboxes']) for r in rooms)
    total_hover = sum(len(r.get('hover_areas', [])) for r in rooms)

    print("=" * 70)
    print("Alfred Pelrock - Room Metadata Extraction Summary")
    print("=" * 70)
    print(f"Rooms processed: {len(rooms)}")
    print(f"Total hotspots: {total_hotspots}")
    print(f"Total exits: {total_exits}")
    print(f"Total walkboxes: {total_walkboxes}")
    if total_hover > 0:
        print(f"Total hover areas: {total_hover}")
    print("=" * 70)

    # Show per-room breakdown for first 10 rooms
    print("\nFirst 10 rooms:")
    for room in rooms[:10]:
        hover_str = f", {len(room.get('hover_areas', []))} hover" if 'hover_areas' in room else ""
        print(f"  Room {room['room']:2d}: {len(room['hotspots'])} hotspots, "
              f"{len(room['exits'])} exits, {len(room['walkboxes'])} walkboxes{hover_str}")


def save_output(rooms, output_dir, formats=None):
    """Save extracted data in various formats."""
    if formats is None:
        formats = ['json']

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    saved_files = []

    # JSON format (complete data)
    if 'json' in formats:
        json_file = output_path / "room_metadata.json"
        with open(json_file, 'w') as f:
            json.dump({
                'description': 'Alfred Pelrock complete room metadata',
                'rooms': rooms
            }, f, indent=2)
        saved_files.append(json_file)

    # Python format (for importing)
    if 'py' in formats:
        py_file = output_path / "room_metadata.py"
        with open(py_file, 'w') as f:
            f.write("# Alfred Pelrock - Room Metadata\n\n")
            f.write("ROOM_METADATA = {\n")
            for room in rooms:
                f.write(f"    {room['room']}: {{\n")
                f.write(f"        'hotspots': {room['hotspots']},\n")
                f.write(f"        'exits': {room['exits']},\n")
                f.write(f"        'walkboxes': {room['walkboxes']},\n")
                if 'hover_areas' in room:
                    f.write(f"        'hover_areas': {room['hover_areas']},\n")
                f.write("    },\n")
            f.write("}\n")
        saved_files.append(py_file)

    # Text format (human-readable)
    if 'txt' in formats:
        txt_file = output_path / "room_metadata.txt"
        with open(txt_file, 'w') as f:
            f.write("Alfred Pelrock - Room Metadata\n")
            f.write("=" * 70 + "\n\n")

            for room in rooms:
                f.write(f"Room {room['room']}\n")
                f.write("-" * 70 + "\n")

                f.write(f"Hotspots ({len(room['hotspots'])}):\n")
                for h in room['hotspots']:
                    f.write(f"  [{h['index']}] ({h['x']}, {h['y']}) {h['width']}x{h['height']} "
                           f"type=0x{h['type']:02X} extra=0x{h['extra']:04X}\n")

                f.write(f"\nExits ({len(room['exits'])}):\n")
                for e in room['exits']:
                    trig = e['trigger']
                    dest = e['destination']
                    f.write(f"  [{e['index']}] Trigger: ({trig['x']}, {trig['y']}) {trig['width']}x{trig['height']} "
                           f"→ Room {e['destination_room']} at ({dest['x']}, {dest['y']}) "
                           f"facing {dest['direction_name']}\n")

                f.write(f"\nWalkboxes ({len(room['walkboxes'])}):\n")
                for w in room['walkboxes']:
                    f.write(f"  [{w['index']}] ({w['x']}, {w['y']}) {w['width']}x{w['height']} "
                           f"flags=0x{w['flags']:02X}\n")

                if 'hover_areas' in room and room['hover_areas']:
                    f.write(f"\nHover Areas ({len(room['hover_areas'])}):\n")
                    for region in ['left', 'center', 'right']:
                        region_areas = [h for h in room['hover_areas'] if h['region'] == region]
                        if region_areas:
                            f.write(f"  {region.upper()}:\n")
                            for h in sorted(region_areas, key=lambda a: a['y']):
                                f.write(f"    ({h['x']}, {h['y']}) {h['width']}x{h['height']}\n")

                f.write("\n")
        saved_files.append(txt_file)

    return saved_files


def main():
    parser = argparse.ArgumentParser(
        description='Extract all room metadata (hotspots, exits, walkboxes, hover areas) from ALFRED.1'
    )
    parser.add_argument('alfred1', help='Path to ALFRED.1 file')
    parser.add_argument('--output', '-o', default='output/room_metadata',
                       help='Output directory (default: output/room_metadata)')
    parser.add_argument('--room', type=int, help='Extract single room only')
    parser.add_argument('--max-rooms', type=int, default=56,
                       help='Maximum number of rooms to scan (default: 56)')
    parser.add_argument('--formats', nargs='+', choices=['json', 'py', 'txt'],
                       default=['json', 'txt'],
                       help='Output formats (default: json txt)')
    parser.add_argument('--no-hover', action='store_true',
                       help='Skip hover area extraction (faster)')
    parser.add_argument('--hover-min-size', type=int, default=10,
                       help='Minimum size for hover areas (default: 10)')

    args = parser.parse_args()

    alfred1_path = Path(args.alfred1)
    if not alfred1_path.exists():
        print(f"Error: File not found: {alfred1_path}")
        return 1

    print(f"Extracting metadata from: {alfred1_path}")
    print()

    if args.room is not None:
        # Extract single room
        with open(alfred1_path, 'rb') as f:
            data = f.read()
        metadata = extract_room_metadata(data, args.room, not args.no_hover, args.hover_min_size)
        if metadata:
            rooms = [metadata]
        else:
            print(f"Error: No data found for room {args.room}")
            return 1
    else:
        # Extract all rooms
        rooms = extract_all_rooms(alfred1_path, args.max_rooms, not args.no_hover, args.hover_min_size)

    if not rooms:
        print("No room data extracted!")
        return 1

    # Print summary
    print_summary(rooms)
    print()

    # Save output
    saved_files = save_output(rooms, args.output, args.formats)

    print(f"Output saved to: {Path(args.output).absolute()}")
    for f in saved_files:
        print(f"  - {f.name}")

    return 0


if __name__ == "__main__":
    exit(main())
