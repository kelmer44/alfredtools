#!/usr/bin/env python3
"""
RLE Decompressor for ALFRED.7
Decompresses RLE data from a specific offset to raw bytes
"""

import sys
from pathlib import Path

def decompress_rle_block(data, offset, size):
    """
    Decompress a single block - handles both RLE and uncompressed

    Some blocks are stored uncompressed (when size is 0x8000 or 0x6800)
    Others are RLE compressed with [count][value] pairs

    Args:
        data: Full file data
        offset: Starting offset
        size: Block size

    Returns:
        Decompressed bytes
    """
    # Check for uncompressed markers
    if size == 0x8000 or size == 0x6800:
        # Uncompressed block - read directly
        print(f"  Block at 0x{offset:06X}: uncompressed, reading {size} bytes directly")
        return data[offset:offset+size]

    # RLE compressed - decompress
    print(f"  Block at 0x{offset:06X}: RLE compressed, size {size} (0x{size:X})")
    result = bytearray()
    pos = offset
    end = offset + size

    while pos + 2 <= min(end, len(data)):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break

        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    return bytes(result)

def decompress_rle(data, offset, target_size):
    """
    Decompress RLE data starting at offset until target_size bytes are extracted

    Continuously decompresses until:
    - Target size is reached
    - A BUDA marker is hit (indicating end of data)
    - End of file

    Args:
        data: Full file data
        offset: Starting offset for decompression
        target_size: Number of bytes to decompress (e.g., 256000 for 640x400)

    Returns:
        Tuple of (decompressed bytes, end position)
    """
    result = bytearray()
    pos = offset

    print(f"  Starting continuous decompression from 0x{pos:06X}")

    while pos + 2 <= len(data) and len(result) < target_size:
        # Check for BUDA marker (end of compressed block)
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            print(f"  Hit BUDA marker at offset 0x{pos:06X}")
            break

        # Read RLE pair
        count = data[pos]
        value = data[pos + 1]

        # Expand
        result.extend([value] * count)
        pos += 2

    return bytes(result), pos

def main():
    if len(sys.argv) < 3:
        print("RLE Decompressor for ALFRED.7")
        print("=" * 70)
        print()
        print("Usage: python decompress_rle.py <offset> <size> [mode] [alfred7_path] [output]")
        print()
        print("Arguments:")
        print("  offset       - Starting offset (decimal or hex with 0x prefix)")
        print("  size         - Bytes to decompress OR block size if mode=block")
        print("  mode         - 'continuous' (default) or 'block' (optional)")
        print("  alfred7_path - Path to ALFRED.7 file (default: ./ALFRED.7)")
        print("  output       - Output filename (default: decompressed_<offset>.bin)")
        print()
        print("Modes:")
        print("  continuous - Decompress RLE continuously until target size reached")
        print("  block      - Decompress single block (auto-detects uncompressed)")
        print()
        print("Examples:")
        print("  python decompress_rle.py 2405266 256000")
        print("  python decompress_rle.py 0x24B392 0x3E800 ALFRED.7 output.bin")
        print("  python decompress_rle.py 0x24082C 0x8000 block ALFRED.7")
        print()
        sys.exit(1)

    # Parse offset (supports decimal or hex)
    offset_str = sys.argv[1]
    if offset_str.startswith('0x') or offset_str.startswith('0X'):
        offset = int(offset_str, 16)
    else:
        offset = int(offset_str)

    # Parse size
    size_str = sys.argv[2]
    if size_str.startswith('0x') or size_str.startswith('0X'):
        size = int(size_str, 16)
    else:
        size = int(size_str)

    # Parse optional mode
    mode = 'continuous'
    arg_offset = 3

    if len(sys.argv) > 3 and sys.argv[3] in ['continuous', 'block']:
        mode = sys.argv[3]
        arg_offset = 4

    # Input file
    alfred7_path = sys.argv[arg_offset] if len(sys.argv) > arg_offset else 'ALFRED.7'

    # Output file
    if len(sys.argv) > arg_offset + 1:
        output_file = sys.argv[arg_offset + 1]
    else:
        output_file = f'decompressed_0x{offset:06X}.bin'

    # Check input file exists
    if not Path(alfred7_path).exists():
        print(f"Error: File not found: {alfred7_path}")
        sys.exit(1)

    # Read ALFRED.7
    print("=" * 70)
    print("RLE Decompressor for ALFRED.7")
    print("=" * 70)
    print()

    with open(alfred7_path, 'rb') as f:
        data = f.read()

    print(f"Input file: {alfred7_path}")
    print(f"File size: {len(data):,} bytes ({len(data) / 1024 / 1024:.2f} MB)")
    print()
    print(f"Start offset: {offset} (0x{offset:06X})")
    print(f"Size: {size:,} bytes (0x{size:X})")
    print(f"Mode: {mode}")
    print()

    # Check if we're at a BUDA marker
    if offset >= 4 and data[offset-4:offset] == b'BUDA':
        print(f"Note: Offset is +4 from BUDA marker at 0x{offset-4:06X}")
    elif data[offset:offset+4] == b'BUDA':
        print(f"Warning: Starting AT BUDA marker - adding +4 to skip it")
        offset += 4

    print()
    print("Decompressing...")
    print()

    # Decompress based on mode
    if mode == 'block':
        # Single block decompression
        decompressed = decompress_rle_block(data, offset, size)
        end_pos = offset + size
    else:
        # Continuous decompression
        decompressed, end_pos = decompress_rle(data, offset, size)

    print()
    print(f"Decompressed: {len(decompressed):,} bytes")
    print(f"End offset: 0x{end_pos:06X}")

    if mode == 'continuous':
        print(f"Bytes read: {end_pos - offset:,} (compressed)")

        if len(decompressed) < size:
            print()
            print(f"Warning: Only decompressed {len(decompressed)} of {size} requested bytes")
            print(f"         ({len(decompressed) / size * 100:.1f}% of target)")
    else:
        print(f"Block size: {size:,} bytes")
        if size in [0x8000, 0x6800]:
            print(f"Block was uncompressed (size marker: 0x{size:X})")
        else:
            print(f"Block was RLE compressed")

    # Save output
    with open(output_file, 'wb') as f:
        f.write(decompressed)

    print()
    print("=" * 70)
    print(f"✓ Saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
