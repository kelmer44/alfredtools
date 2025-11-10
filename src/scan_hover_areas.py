"""
scan_hover_areas.py

Scan room pair-10 data blocks for potential hover/interactive areas.
This script can scan a single room or all rooms and writes results to
`output/hover_areas.json`.

Heuristic: look for 2-byte x, 2-byte y, 1-byte w, 1-byte h structures
within the pair-10 data block. Categorize by left/center/right by x.
"""

import struct
import json
import os
import argparse


def parse_room_pair10(data, room_num):
    """Return a dict with pair10 offset/size and detected areas for room_num.

    Returns None when there's no pair10 data for the room.
    """
    room_offset = room_num * 104
    pair10_header_offset = room_offset + (10 * 8)
    if pair10_header_offset + 8 > len(data):
        return None

    offset = struct.unpack('<I', data[pair10_header_offset:pair10_header_offset + 4])[0]
    size = struct.unpack('<I', data[pair10_header_offset + 4:pair10_header_offset + 8])[0]

    if size == 0 or offset >= len(data):
        return None

    pair10_data = data[offset:offset + size]

    result = {
        'room': room_num,
        'pair10_offset': offset,
        'pair10_size': size,
        'exits': [],
        'areas': []
    }

    # Parse exits at 0x1BE relative to pair10_data (if present)
    exit_base = 0x1BE
    for i in range(8):
        exit_offset = exit_base + (i * 14)
        if exit_offset + 14 > len(pair10_data):
            break
        try:
            x = struct.unpack('<H', pair10_data[exit_offset + 3:exit_offset + 5])[0]
            y = struct.unpack('<H', pair10_data[exit_offset + 5:exit_offset + 7])[0]
            w = pair10_data[exit_offset + 7]
            h = pair10_data[exit_offset + 8]
            if 0 <= x < 640 and 0 <= y < 400 and 0 < w < 200 and 0 < h < 200:
                result['exits'].append({'index': i, 'offset': exit_offset, 'x': x, 'y': y, 'w': w, 'h': h})
        except Exception:
            continue

    # Scan the entire pair10 block for coordinate-like structures
    for scan_offset in range(0, len(pair10_data) - 6, 1):
        # try both alignments (0 and 3) used earlier heuristics
        for align in (0, 3):
            pos = scan_offset + align
            if pos + 6 > len(pair10_data):
                continue
            try:
                x = struct.unpack('<H', pair10_data[pos:pos + 2])[0]
                y = struct.unpack('<H', pair10_data[pos + 2:pos + 4])[0]
                w = pair10_data[pos + 4]
                h = pair10_data[pos + 5]

                if not (0 <= x < 640 and 0 <= y < 400 and 0 < w < 200 and 0 < h < 200):
                    continue

                # Simple de-dup: skip if identical area already recorded
                area = {'offset': pos, 'x': x, 'y': y, 'w': w, 'h': h}
                if area in result['areas']:
                    continue

                # classify by x position
                if x > 500:
                    region = 'right'
                elif x < 100:
                    region = 'left'
                else:
                    region = 'center'

                area['region'] = region
                result['areas'].append(area)
            except Exception:
                continue

    return result


def scan_all_rooms(data, max_rooms=256):
    out = []
    for room in range(0, max_rooms):
        info = parse_room_pair10(data, room)
        if info is None:
            # treat as empty room and continue (rooms may be sparse)
            continue
        out.append(info)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', default='files/ALFRED.1', help='Game data file')
    parser.add_argument('--room', type=int, default=None, help='Single room to scan')
    parser.add_argument('--max-rooms', type=int, default=256, help='Max rooms to scan when --room not set')
    parser.add_argument('--out', default='output/hover_areas.json', help='Output JSON file')
    args = parser.parse_args()

    if not os.path.exists(os.path.dirname(args.out)):
        os.makedirs(os.path.dirname(args.out), exist_ok=True)

    with open(args.file, 'rb') as f:
        data = f.read()

    results = []
    if args.room is not None:
        info = parse_room_pair10(data, args.room)
        if info:
            results.append(info)
    else:
        results = scan_all_rooms(data, max_rooms=args.max_rooms)

    # Write JSON summary
    with open(args.out, 'w') as fo:
        json.dump(results, fo, indent=2)

    # Print small summary
    print(f"Wrote {len(results)} rooms to {args.out}")
    for r in results[:10]:
        print(f"Room {r['room']}: pair10 @0x{r['pair10_offset']:X} size {r['pair10_size']} - {len(r['areas'])} areas, {len(r['exits'])} exits")


if __name__ == '__main__':
    main()
