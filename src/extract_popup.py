#!/usr/bin/env python3
"""
Alfred Pelrock - Balloon & Action Icon Extractor

Extracts the thinking balloon popup and action icons from ALFRED.7
These are shown when player long-presses on a hotspot.

Location: 0xFE945 (1,042,757) - 4,766 bytes (RLE compressed)
After decompression: 49,686 bytes = possibly 6 icons of 91x91
"""

import sys
from pathlib import Path
from PIL import Image

# Balloon/icon data
BALLOON_OFFSET = 0xFE945
BALLOON_SIZE = 0x129E  # 4,766 bytes compressed

def decompress_rle(data, offset, size):
    """Decompress RLE data"""
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

def find_budas(data):
    """Find BUDA markers"""
    budas = []
    pos = 0
    while pos < len(data) - 4:
        if data[pos:pos+4] == b'BUDA':
            budas.append(pos)
        pos += 1
    return budas

def is_valid_palette(data, offset):
    """Check for VGA palette"""
    if offset + 768 > len(data):
        return False
    pal_data = data[offset:offset+768]
    return all(b <= 63 for b in pal_data) and len(set(pal_data)) > 10

def extract_palette(data, offset):
    """Extract VGA palette"""
    pal_data = data[offset:offset+768]
    palette = []
    for i in range(256):
        r = min(255, pal_data[i * 3] * 4)
        g = min(255, pal_data[i * 3 + 1] * 4)
        b = min(255, pal_data[i * 3 + 2] * 4)
        palette.extend([r, g, b])
    return palette

def find_nearest_palette(data, budas, target_offset):
    """Find nearest palette"""
    best_palette = None
    best_distance = float('inf')

    for buda in budas:
        if is_valid_palette(data, buda + 4):
            distance = abs(buda - target_offset)
            if distance < best_distance:
                best_distance = distance
                best_palette = extract_palette(data, buda + 4)

    return best_palette

def main():
    if len(sys.argv) < 2:
        print("Alfred Pelrock - Balloon & Action Icon Extractor")
        print("=" * 70)
        print()
        print("Usage: python extract_balloon_icons.py <ALFRED.7> [output_dir]")
        print()
        print("Extracts the thinking balloon popup and action icons shown")
        print("when player long-presses on a hotspot.")
        print()
        print(f"Location: 0x{BALLOON_OFFSET:06X} ({BALLOON_OFFSET:,})")
        print(f"Size: {BALLOON_SIZE:,} bytes (RLE compressed)")
        print()
        sys.exit(1)

    alfred7_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "balloon_icons"

    if not Path(alfred7_path).exists():
        print(f"Error: File not found: {alfred7_path}")
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read file
    with open(alfred7_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - Balloon & Action Icon Extractor")
    print("=" * 70)
    print(f"File: {alfred7_path}")
    print(f"Size: {len(data):,} bytes")
    print()

    # Find palette
    print("Finding palette...")
    budas = find_budas(data)
    palette = find_nearest_palette(data, budas, BALLOON_OFFSET)

    if not palette:
        print("Warning: No palette found, using grayscale")
        palette = []
        for i in range(256):
            palette.extend([i, i, i])
    else:
        print("✓ Found palette")
    print()

    # Decompress balloon data
    print(f"Decompressing data from 0x{BALLOON_OFFSET:06X}...")
    decompressed = decompress_rle(data, BALLOON_OFFSET, BALLOON_SIZE)
    print(f"Compressed: {BALLOON_SIZE:,} bytes")
    print(f"Decompressed: {len(decompressed):,} bytes")
    print()

    # Try different interpretations
    print("=" * 70)
    print("Extracting possible formats:")
    print("=" * 70)

    # Try as 6 icons of 91x91
    if len(decompressed) == 49686:
        icon_size = 8281  # 91x91
        num_icons = 6

        print(f"\n6 icons of 91x91 (8,281 bytes each):")
        for i in range(num_icons):
            offset = i * icon_size
            if offset + icon_size <= len(decompressed):
                icon_data = decompressed[offset:offset + icon_size]

                # Create image
                img = Image.new('P', (91, 91))
                img.putpalette(palette)
                img.putdata(icon_data)

                output_file = output_path / f"icon_{i}_91x91.png"
                img.save(output_file)

                # RGBA with transparency
                img_rgba = Image.new('RGBA', (91, 91))
                for y in range(91):
                    for x in range(91):
                        pixel_idx = icon_data[y * 91 + x]
                        if pixel_idx == 255:
                            img_rgba.putpixel((x, y), (0, 0, 0, 0))
                        else:
                            r = palette[pixel_idx * 3]
                            g = palette[pixel_idx * 3 + 1]
                            b = palette[pixel_idx * 3 + 2]
                            img_rgba.putpixel((x, y), (r, g, b, 255))

                output_rgba = output_path / f"icon_{i}_91x91_trans.png"
                img_rgba.save(output_rgba)

                # 2x upscale
                img_large = img_rgba.resize((182, 182), Image.NEAREST)
                output_large = output_path / f"icon_{i}_91x91_2x.png"
                img_large.save(output_large)

                print(f"  Icon {i}: ✓ {output_file.name}")

    # Try as single large image
    for width, height in [(247, 201), (201, 247)]:
        if width * height <= len(decompressed):
            size = width * height
            img_data = decompressed[:size]

            img = Image.new('P', (width, height))
            img.putpalette(palette)
            img.putdata(img_data)

            output_file = output_path / f"combined_{width}x{height}.png"
            img.save(output_file)

            # RGBA
            img_rgba = Image.new('RGBA', (width, height))
            for y in range(height):
                for x in range(width):
                    if y * width + x < len(img_data):
                        pixel_idx = img_data[y * width + x]
                        if pixel_idx == 255:
                            img_rgba.putpixel((x, y), (0, 0, 0, 0))
                        else:
                            r = palette[pixel_idx * 3]
                            g = palette[pixel_idx * 3 + 1]
                            b = palette[pixel_idx * 3 + 2]
                            img_rgba.putpixel((x, y), (r, g, b, 255))

            output_rgba = output_path / f"combined_{width}x{height}_trans.png"
            img_rgba.save(output_rgba)

            print(f"\n{width}x{height} combined: ✓ {output_file.name}")

    print()
    print("=" * 70)
    print(f"Extraction complete!")
    print(f"Output: {output_path.absolute()}")
    print()
    print("Files created:")
    print("  - icon_X_91x91.png : Individual icons (indexed)")
    print("  - icon_X_91x91_trans.png : With transparency")
    print("  - icon_X_91x91_2x.png : 2x upscaled")
    print("  - combined_WxH.png : Full data as single image")
    print("=" * 70)

if __name__ == "__main__":
    main()
