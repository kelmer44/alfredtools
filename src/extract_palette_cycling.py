#!/usr/bin/env python3
"""
Alfred Pelrock - Palette Cycling Extractor from ALFRED.1

Based on the code analysis, palette cycling data is likely embedded
within Pair 10 (room data) at a specific offset.

Known Pair 10 offsets:
  +0x005: animation count
  +0x006: animation array (44 bytes each)
  +0x1BE: exit count
  +0x1BF: exit array (14 bytes each)
  +0x213: walkbox count
  +0x218: walkbox array (9 bytes each)
  +0x47A: hotspot count
  +0x47C: hotspot array (9 bytes each)

Palette cycling config (12 bytes) could be at:
  - A fixed offset before or after known structures
  - After the hotspot array
  - In an unused area

Let's scan Pair 10 for all rooms and look for 12-byte patterns
that match palette cycling config format.
"""

import struct
import json
import sys
from pathlib import Path

def extract_pair10_data(data, room_num):
    """Extract Pair 10 data for a room"""
    room_offset = room_num * 104
    pair10_offset = room_offset + (10 * 8)

    offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
    size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

    if offset > 0 and size > 0 and offset < len(data):
        return data[offset:offset+size], offset, size
    return None, 0, 0

def looks_like_cycling_config(data, offset):
    """Check if 12 bytes look like a valid palette cycling config"""
    if offset + 12 > len(data):
        return False, None

    config = data[offset:offset+12]

    start_index = config[0]
    mode = config[1]

    # Valid checks:
    # - start_index should be 0-255
    # - mode should be 1-10 or so (1=fade, 2+=rotate)
    # - RGB values should be 0-63 (6-bit VGA)

    if mode < 1 or mode > 10:
        return False, None

    # Check RGB values are in valid VGA range (0-63)
    for i in range(2, 11):
        if config[i] > 63:
            return False, None

    return True, {
        'start_index': start_index,
        'mode': mode,
        'current_rgb': [config[2], config[3], config[4]],
        'min_rgb': [config[5], config[6], config[7]],
        'max_rgb': [config[8], config[9], config[10]],
        'flags': config[11],
        'direction': 'max' if config[11] & 0x40 else 'min',
        'speed': config[11] & 0x3F
    }

def scan_for_cycling_configs(pair10_data):
    """Scan Pair 10 data for potential palette cycling configs"""
    configs = []

    # Check common offsets first
    common_offsets = [
        0x00,   # Start of Pair 10
        0x500,  # After typical hotspot data
        0x600,
        0x700,
        0x800,
    ]

    for offset in common_offsets:
        valid, config = looks_like_cycling_config(pair10_data, offset)
        if valid:
            configs.append({
                'offset': offset,
                'config': config
            })

    # Scan entire structure if nothing found
    if not configs:
        for offset in range(0, len(pair10_data) - 12, 1):
            valid, config = looks_like_cycling_config(pair10_data, offset)
            if valid:
                configs.append({
                    'offset': offset,
                    'config': config
                })
                break  # Only take first match

    return configs

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_palette_cycling.py <alfred.1> [output_dir]")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "palette_cycling"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - Palette Cycling Extractor")
    print("=" * 70)
    print()
    print("Scanning Pair 10 (room data) for all 56 rooms...")
    print()

    rooms_with_cycling = []

    for room_num in range(56):
        pair10_data, file_offset, size = extract_pair10_data(data, room_num)

        if pair10_data:
            configs = scan_for_cycling_configs(pair10_data)

            if configs:
                print(f"Room {room_num:2d}: Found cycling config at offset +0x{configs[0]['offset']:03X}")
                config = configs[0]['config']
                print(f"  Mode: {config['mode']}, Start index: {config['start_index']}")
                print(f"  Current RGB: {config['current_rgb']}")
                print(f"  Min RGB: {config['min_rgb']}")
                print(f"  Max RGB: {config['max_rgb']}")
                print(f"  Flags: 0x{config['flags']:02X} (dir={config['direction']}, speed={config['speed']})")
                print()

                rooms_with_cycling.append({
                    'room': room_num,
                    'pair10_offset': configs[0]['offset'],
                    'config': config
                })

    print("=" * 70)
    print(f"Found {len(rooms_with_cycling)} room(s) with palette cycling")

    if rooms_with_cycling:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        json_file = output_path / "palette_cycling.json"
        with open(json_file, 'w') as f:
            json.dump({
                'description': 'Alfred Pelrock palette cycling configurations',
                'note': 'Data found in Pair 10 (room data) of ALFRED.1',
                'rooms': rooms_with_cycling
            }, f, indent=2)

        print(f"Saved to: {json_file}")
    else:
        print("No palette cycling configs found.")
        print()
        print("The data might be:")
        print("1. In a different file (ALFRED.0, ALFRED.8, ALFRED.9?)")
        print("2. At a different location in ALFRED.1")
        print("3. Embedded in the executable's data section")

    print("=" * 70)

if __name__ == "__main__":
    main()
