#!/usr/bin/env python3
"""
Alfred Pelrock - Background Extractor
Backgrounds are composed of multiple 32KB RLE-compressed blocks
"""

import struct
import sys
from pathlib import Path
from PIL import Image

DEFAULT_PALETTE = []
for i in range(256):
    DEFAULT_PALETTE.extend([i, i, i])

def decompress_rle_block(data, offset, size):
    """Decompress a single block - handles both RLE and uncompressed"""
    # Check for uncompressed markers
    if size == 0x8000 or size == 0x6800:
        # Uncompressed block - read directly
        return data[offset:offset+size]

    # RLE compressed - decompress
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

def extract_backgrounds(alfred1_path, output_dir):
    """Extract backgrounds from Alfred.1"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print(f"File size: {len(data)} bytes ({len(data) / 1024 / 1024:.2f} MB)\n")

    WIDTH = 640
    HEIGHT = 400
    EXPECTED_SIZE = WIDTH * HEIGHT  # 256,000 bytes
    BLOCK_SIZE = 32768  # 0x8000 - standard block size
    EXPECTED_BLOCKS = 8  # 256,000 / 32,768 ≈ 8 blocks

    ROOM_STRUCT_SIZE = 104
    num_rooms = 56  # Known from Ghidra

    print(f"Extracting from {num_rooms} rooms...")
    print(f"Expected: {EXPECTED_BLOCKS} blocks of ~{BLOCK_SIZE} bytes each = {EXPECTED_SIZE} bytes")
    print("="*70 + "\n")

    backgrounds_found = 0

    for room_num in range(num_rooms):
        room_offset = room_num * ROOM_STRUCT_SIZE

        print(f"Room {room_num:2d}:", end=" ")

        # Read all offset/size pairs
        pairs = []
        for pair_idx in range(13):
            pair_offset = room_offset + (pair_idx * 8)
            if pair_offset + 8 > len(data):
                break

            offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
            size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

            if offset > 0 and size > 0 and offset < len(data):
                pairs.append((pair_idx, offset, size))

        # Strategy: Try to combine first N consecutive blocks
        # Backgrounds are typically the first 8 blocks (pairs 0-7)
        best_result = None
        best_score = 0
        best_range = None

        # Try different ranges of consecutive blocks
        for start_idx in range(len(pairs)):
            for num_blocks in range(6, 10):  # Try 6-9 blocks
                if start_idx + num_blocks > len(pairs):
                    continue

                # Decompress and combine these blocks
                combined = bytearray()
                for i in range(num_blocks):
                    pair_idx, offset, size = pairs[start_idx + i]
                    block_data = decompress_rle_block(data, offset, size)
                    combined.extend(block_data)

                combined_size = len(combined)

                # Score based on how close to expected size
                if combined_size > 0:
                    size_ratio = combined_size / EXPECTED_SIZE
                    if 0.9 <= size_ratio <= 1.1:  # Within 10%
                        score = 100 - abs(size_ratio - 1.0) * 100
                        if score > best_score:
                            best_score = score
                            best_result = bytes(combined)
                            best_range = (start_idx, start_idx + num_blocks - 1)

        # Save if we found a good match
        if best_result and best_score > 85:
            start, end = best_range
            print(f"✓ Background from pairs {start}-{end} ({len(best_result)} bytes, score={best_score:.1f})")

            # Trim or pad to exact size
            img_data = best_result[:EXPECTED_SIZE]
            if len(img_data) < EXPECTED_SIZE:
                img_data += bytes([0] * (EXPECTED_SIZE - len(img_data)))

            img = Image.new('P', (WIDTH, HEIGHT))
            img.putpalette(DEFAULT_PALETTE)
            img.putdata(img_data)

            output_file = output_path / f"room_{room_num:02d}.png"
            img.save(output_file)
            backgrounds_found += 1
        else:
            if best_score > 0:
                print(f"✗ Best score too low ({best_score:.1f})")
            else:
                print(f"✗ No suitable combination found")

    print("\n" + "="*70)
    print(f"Extraction complete!")
    print(f"Total backgrounds extracted: {backgrounds_found}/{num_rooms}")
    print(f"Output directory: {output_path.absolute()}")
    print("="*70)

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_alfred1_backgrounds.py <alfred.1> [output_dir]")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "backgrounds_output"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    extract_backgrounds(alfred1_path, output_dir)

if __name__ == "__main__":
    main()
