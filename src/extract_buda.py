#!/usr/bin/env python3
"""
RLE Decompressor for ALFRED files
Decompresses RLE data from a specific offset until BUDA marker is found
"""

import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("RLE Decompressor")
        print("=" * 70)
        print()
        print("Usage: python extract_buda_7.py <offset> [alfred_file]")
        print()
        print("Arguments:")
        print("  offset      - Starting offset (decimal or hex with 0x prefix)")
        print("  alfred_file - Path to ALFRED file (default: files/ALFRED.7)")
        print()
        print("Example:")
        print("  python extract_buda_7.py 0x24082C")
        print("  python extract_buda_7.py 32400 files/ALFRED.4")
        print()
        sys.exit(1)

    # Parse offset (supports decimal or hex)
    offset_str = sys.argv[1]
    if offset_str.startswith('0x') or offset_str.startswith('0X'):
        offset = int(offset_str, 16)
    else:
        offset = int(offset_str)

    # Input file
    alfred_file = sys.argv[2] if len(sys.argv) > 2 else 'files/ALFRED.7'

    # Check input file exists
    if not Path(alfred_file).exists():
        print(f"Error: File not found: {alfred_file}")
        sys.exit(1)

    # Read file
    print("=" * 70)
    print("RLE Decompressor")
    print("=" * 70)
    print()

    with open(alfred_file, 'rb') as f:
        data = f.read()

    print(f"Input file: {alfred_file}")
    print(f"File size: {len(data):,} bytes ({len(data) / 1024 / 1024:.2f} MB)")
    print()
    print(f"Start offset: {offset} (0x{offset:06X})")
    print()

    # Decompress until BUDA marker
    result = bytearray()
    pos = offset

    print("Decompressing until BUDA marker...")

    while pos + 2 <= len(data):
        # Check for BUDA marker
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            print(f"  Hit BUDA marker at offset 0x{pos:06X}")
            break

        # Read RLE pair
        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    decompressed = bytes(result)
    end_pos = pos

    print()
    print(f"Decompressed: {len(decompressed):,} bytes")
    print(f"End offset: 0x{end_pos:06X}")
    print(f"Bytes read: {end_pos - offset:,} (compressed)")
    print()

    # Write output
    output_file = f'decompressed_0x{offset:06X}.bin'
    with open(output_file, 'wb') as f:
        f.write(decompressed)

    print(f"Saved to: {output_file}")

if __name__ == "__main__":
    main()
