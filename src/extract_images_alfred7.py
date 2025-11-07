#!/usr/bin/env python3
"""
Extract All Confirmed Images from ALFRED.7

Extracts all 10 confirmed 640x400 images:
- 9 RLE compressed images
- 1 raw uncompressed image

Based on the confirmed offsets from alfred7_known_offsets.md
"""

import sys
from pathlib import Path
from PIL import Image

def find_all_budas(data):
    """Find all BUDA marker positions"""
    budas = []
    pos = 0
    while pos < len(data) - 4:
        if data[pos:pos+4] == b'BUDA':
            budas.append(pos)
        pos += 1
    return budas

def decompress_rle_block(data, offset, size):
    """
    Decompress a single block - handles both RLE and uncompressed

    Blocks with size 0x8000 or 0x6800 are uncompressed
    Others are RLE compressed with [count][value] pairs
    """
    # Check for uncompressed markers
    if size == 0x8000 or size == 0x6800:
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

def extract_palette(data, offset):
    """Extract VGA palette and convert to 8-bit RGB"""
    pal_data = data[offset:offset+768]
    palette = []
    for i in range(256):
        r = min(255, pal_data[i * 3] * 4)
        g = min(255, pal_data[i * 3 + 1] * 4)
        b = min(255, pal_data[i * 3 + 2] * 4)
        palette.extend([r, g, b])
    return palette

def extract_multi_buda_rle_image(data, budas, start_buda, end_buda, pal_buda, output_file):
    """
    Extract an image that spans multiple RLE compressed BUDAs

    Args:
        data: Full file data
        budas: List of BUDA offsets
        start_buda: Starting BUDA index
        end_buda: Ending BUDA index (inclusive)
        pal_buda: Palette BUDA index
        output_file: Output filename
    """
    print(f"  Extracting BUDAs {start_buda}-{end_buda} with palette {pal_buda}...")

    # Decompress and combine all blocks
    combined = bytearray()
    for i in range(start_buda, end_buda + 1):
        buda_offset = budas[i]
        next_buda = budas[i + 1] if i + 1 < len(budas) else len(data)
        data_start = buda_offset + 4
        block_size = next_buda - data_start

        block_data = decompress_rle_block(data, data_start, block_size)
        combined.extend(block_data)

    print(f"    Decompressed: {len(combined)} bytes")

    # Extract palette
    pal_offset = budas[pal_buda] + 4
    palette = extract_palette(data, pal_offset)

    # Create image
    TARGET_SIZE = 640 * 400
    img_data = bytes(combined[:TARGET_SIZE])

    if len(img_data) < TARGET_SIZE:
        img_data += bytes([0] * (TARGET_SIZE - len(img_data)))

    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(img_data)
    img.save(output_file)

    print(f"    ✓ Saved: {output_file.name}")

def extract_single_buda_rle_image(data, budas, buda_idx, pal_buda, output_file):
    """
    Extract an image from a single RLE compressed BUDA

    Args:
        data: Full file data
        budas: List of BUDA offsets
        buda_idx: BUDA index containing the image
        pal_buda: Palette BUDA index
        output_file: Output filename
    """
    print(f"  Extracting BUDA {buda_idx} with palette {pal_buda}...")

    # Decompress single block
    buda_offset = budas[buda_idx]
    next_buda = budas[buda_idx + 1] if buda_idx + 1 < len(budas) else len(data)
    data_start = buda_offset + 4
    block_size = next_buda - data_start

    block_data = decompress_rle_block(data, data_start, block_size)
    print(f"    Decompressed: {len(block_data)} bytes")

    # Extract palette
    pal_offset = budas[pal_buda] + 4
    palette = extract_palette(data, pal_offset)

    # Create image
    TARGET_SIZE = 640 * 400
    img_data = block_data[:TARGET_SIZE]

    if len(img_data) < TARGET_SIZE:
        img_data += bytes([0] * (TARGET_SIZE - len(img_data)))

    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(img_data)
    img.save(output_file)

    print(f"    ✓ Saved: {output_file.name}")

def extract_raw_uncompressed_image(data, budas, offset, pal_buda, output_file):
    """
    Extract a raw uncompressed bitmap image

    Args:
        data: Full file data
        budas: List of BUDA offsets
        offset: Starting offset of raw data
        pal_buda: Palette BUDA index
        output_file: Output filename
    """
    print(f"  Extracting raw data from offset 0x{offset:06X} with palette {pal_buda}...")

    # Read raw bytes - no decompression
    TARGET_SIZE = 640 * 400
    raw_data = data[offset:offset + TARGET_SIZE]

    print(f"    Read: {len(raw_data)} bytes (raw uncompressed)")

    # Extract palette
    pal_offset = budas[pal_buda] + 4
    palette = extract_palette(data, pal_offset)

    # Create image
    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(raw_data)
    img.save(output_file)

    print(f"    ✓ Saved: {output_file.name}")

def main():
    if len(sys.argv) < 2:
        print("Extract All Confirmed Images from ALFRED.7")
        print("=" * 70)
        print()
        print("Usage: python extract_all_confirmed_images.py <alfred.7> [output_dir]")
        print()
        print("Extracts:")
        print("  - 9 RLE compressed 640x400 images")
        print("  - 1 raw uncompressed 640x400 image")
        print()
        print("Example:")
        print("  python extract_all_confirmed_images.py ALFRED.7 confirmed_images/")
        print()
        sys.exit(1)

    alfred7_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "confirmed_images"

    if not Path(alfred7_path).exists():
        print(f"Error: File not found: {alfred7_path}")
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("Extracting All Confirmed Images from ALFRED.7")
    print("=" * 70)
    print()

    # Read ALFRED.7
    with open(alfred7_path, 'rb') as f:
        data = f.read()

    print(f"File: {alfred7_path}")
    print(f"Size: {len(data):,} bytes ({len(data) / 1024 / 1024:.2f} MB)")
    print()

    # Find all BUDAs
    print("Finding BUDA markers...")
    budas = find_all_budas(data)
    print(f"Found {len(budas)} BUDA markers")
    print()

    print("=" * 70)
    print("Extracting Images")
    print("=" * 70)
    print()

    # Image 1: buda009_to016_pal017
    print("Image 1: buda009_to016_pal017")
    extract_multi_buda_rle_image(
        data, budas, 9, 16, 17,
        output_path / "01_buda009_to016_pal017.png"
    )
    print()

    # Image 2: buda032_to039_pal040
    print("Image 2: buda032_to039_pal040")
    extract_multi_buda_rle_image(
        data, budas, 32, 39, 40,
        output_path / "02_buda032_to039_pal040.png"
    )
    print()

    # Image 3: buda069_to075_pal076
    print("Image 3: buda069_to075_pal076")
    extract_multi_buda_rle_image(
        data, budas, 69, 75, 76,
        output_path / "03_buda069_to075_pal076.png"
    )
    print()

    # Image 4: buda098_to105_pal106
    print("Image 4: buda098_to105_pal106")
    extract_multi_buda_rle_image(
        data, budas, 98, 105, 106,
        output_path / "04_buda098_to105_pal106.png"
    )
    print()

    # Image 5: buda145_to152_pal153
    print("Image 5: buda145_to152_pal153")
    extract_multi_buda_rle_image(
        data, budas, 145, 152, 153,
        output_path / "05_buda145_to152_pal153.png"
    )
    print()

    # Image 6: buda154 (single block)
    print("Image 6: buda154_pal076")
    extract_single_buda_rle_image(
        data, budas, 154, 76,
        output_path / "06_buda154_pal076.png"
    )
    print()

    # Image 7: buda155 (single block)
    print("Image 7: buda155_pal076")
    extract_single_buda_rle_image(
        data, budas, 155, 76,
        output_path / "07_buda155_pal076.png"
    )
    print()

    # Image 8: buda165_to172_pal173
    print("Image 8: buda165_to172_pal173")
    extract_multi_buda_rle_image(
        data, budas, 165, 172, 173,
        output_path / "08_buda165_to172_pal173.png"
    )
    print()

    # Image 9: buda186_to193_pal194
    print("Image 9: buda186_to193_pal194")
    extract_multi_buda_rle_image(
        data, budas, 186, 193, 194,
        output_path / "09_buda186_to193_pal194.png"
    )
    print()

    # Image 10: Raw uncompressed at 0x24B392
    print("Image 10: raw_at_0x24B392_pal076")
    extract_raw_uncompressed_image(
        data, budas, 0x24B392, 76,
        output_path / "10_raw_at_0x24B392_pal076.png"
    )
    print()

    print("=" * 70)
    print("Extraction Complete!")
    print("=" * 70)
    print(f"Successfully extracted: 10 images")
    print(f"Output directory: {output_path.absolute()}")
    print()
    print("Images extracted:")
    print("  01-05: Multi-BUDA RLE compressed images")
    print("  06-07: Single-BUDA RLE compressed images")
    print("  08-09: Multi-BUDA RLE compressed images")
    print("  10:    Raw uncompressed bitmap")
    print("=" * 70)

if __name__ == "__main__":
    main()
