#!/usr/bin/env python3
"""
Alfred Pelrock - Background Extractor with Palettes
Extracts backgrounds and applies their correct palettes
"""

import struct
import sys
from pathlib import Path
from PIL import Image

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

def extract_palette(data, room_offset):
    """Extract palette from room structure (pair 11)"""
    # Pair 11 contains the palette (768 bytes)
    pair_offset = room_offset + (11 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size == 0x300:  # 768 bytes
        palette_data = data[offset:offset+768]

        # Convert VGA 6-bit palette to 8-bit
        # VGA colors are 0-63, need to multiply by 4 to get 0-255
        palette = []
        for i in range(256):
            r = palette_data[i * 3] * 4
            g = palette_data[i * 3 + 1] * 4
            b = palette_data[i * 3 + 2] * 4
            palette.extend([r, g, b])

        return palette

    return None

def extract_background(data, room_offset):
    """Extract background by combining first 8 blocks"""
    pairs = []

    # Read pairs 0-7 (background blocks)
    for pair_idx in range(8):
        pair_offset = room_offset + (pair_idx * 8)
        offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
        size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

        if offset > 0 and size > 0 and offset < len(data):
            pairs.append((offset, size))

    # Decompress and combine all blocks
    combined = bytearray()
    for offset, size in pairs:
        block_data = decompress_rle_block(data, offset, size)
        combined.extend(block_data)

    return bytes(combined)

def extract_all_backgrounds(alfred1_path, output_dir):
    """Extract all backgrounds with their correct palettes"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print(f"File size: {len(data)} bytes ({len(data) / 1024 / 1024:.2f} MB)\n")

    WIDTH = 640
    HEIGHT = 400
    EXPECTED_SIZE = WIDTH * HEIGHT
    ROOM_STRUCT_SIZE = 104
    NUM_ROOMS = 56

    print(f"Extracting {NUM_ROOMS} backgrounds with palettes...")
    print("="*70 + "\n")

    success_count = 0

    for room_num in range(NUM_ROOMS):
        room_offset = room_num * ROOM_STRUCT_SIZE

        # Extract background
        background_data = extract_background(data, room_offset)

        # Extract palette
        palette = extract_palette(data, room_offset)

        if len(background_data) >= EXPECTED_SIZE * 0.9 and palette:
            # Trim or pad to exact size
            img_data = background_data[:EXPECTED_SIZE]
            if len(img_data) < EXPECTED_SIZE:
                img_data += bytes([0] * (EXPECTED_SIZE - len(img_data)))

            # Create image with palette
            img = Image.new('P', (WIDTH, HEIGHT))
            img.putpalette(palette)
            img.putdata(img_data)

            output_file = output_path / f"room_{room_num:02d}.png"
            img.save(output_file)

            print(f"Room {room_num:2d}: ✓ Saved {output_file.name} ({len(background_data)} bytes)")
            success_count += 1
        else:
            print(f"Room {room_num:2d}: ✗ Failed (bg={len(background_data)} bytes, palette={'OK' if palette else 'MISSING'})")

    print("\n" + "="*70)
    print(f"Extraction complete!")
    print(f"Successfully extracted: {success_count}/{NUM_ROOMS} backgrounds")
    print(f"Output directory: {output_path.absolute()}")
    print("="*70)

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_with_palettes.py <alfred.1> [output_dir]")
        print("\nExample:")
        print("  python extract_with_palettes.py alfred.1 backgrounds_color/")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "backgrounds_color"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    extract_all_backgrounds(alfred1_path, output_dir)

if __name__ == "__main__":
    main()
