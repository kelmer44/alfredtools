#!/usr/bin/env python3
"""
ALFRED.2 - Talking Animation Extractor (Improved)

Extracts talking/mouth animations from ALFRED.2 with proper metadata handling.
"""

import struct
import sys
from pathlib import Path
from PIL import Image
import json

HEADER_SIZE = 55

def parse_header(data, offset):
    """Parse a 55-byte animation header"""
    if offset + HEADER_SIZE > len(data):
        return None

    header = data[offset:offset + HEADER_SIZE]

    data_offset = struct.unpack('<H', header[0:2])[0]

    return {
        'data_offset': data_offset,
        'anim1': {
            'width': header[9],
            'height': header[10],
            'frames': header[13],
        },
        'anim2': {
            'width': header[21],
            'height': header[22],
            'frames': header[25],
        },
        'palette_id': (offset // HEADER_SIZE * 13) + 11
    }

def decompress_rle(data, start, max_pixels):
    """Decompress RLE data starting at position"""
    result = bytearray()
    pos = start

    while len(result) < max_pixels and pos + 2 <= len(data):
        # Check for BUDA marker
        if data[pos:pos+4] == b'BUDA':
            break

        count = data[pos]
        color = data[pos + 1]
        result.extend([color] * count)
        pos += 2

    return bytes(result)

def get_palette(palette_id):
    """Generate a default grayscale palette (replace with actual palette loading)"""
    palette = []
    for i in range(256):
        # Simple grayscale for now
        # TODO: Load actual palette file based on palette_id
        val = i
        palette.extend([val, val, val])
    return palette

def save_animation(pixels, width, height, frames, output_path):
    """Save animation frames as a horizontal strip PNG"""
    if not pixels or width == 0 or height == 0 or frames == 0:
        return False

    total_width = width * frames

    # Create image
    img = Image.new('P', (total_width, height))
    img.putpalette(get_palette(0))

    # Layout frames horizontally
    for frame in range(frames):
        frame_offset = frame * width * height
        for y in range(height):
            for x in range(width):
                pixel_idx = frame_offset + (y * width) + x
                if pixel_idx < len(pixels):
                    img.putpixel((frame * width + x, y), pixels[pixel_idx])

    img.save(output_path)
    return True

def extract_alfred2(filepath, output_dir):
    """Extract all animations from ALFRED.2"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'rb') as f:
        data = f.read()

    print("=" * 80)
    print("ALFRED.2 - Talking Animation Extractor")
    print("=" * 80)
    print(f"\nFile: {filepath}")
    print(f"Size: {len(data)} bytes ({len(data) / 1024:.2f} KB)\n")

    # Find first valid header
    current_offset = 0
    header_index = 0

    while current_offset < len(data):
        data_offset = struct.unpack('<H', data[current_offset:current_offset+2])[0]
        if data_offset != 0:
            break
        current_offset += HEADER_SIZE
        header_index += 1

    print(f"Starting at header index {header_index}, offset 0x{current_offset:08X}\n")

    animations_extracted = 0
    metadata = []

    # Track position in pixel data
    pixel_data_pos = None

    while current_offset < len(data) - HEADER_SIZE:
        header = parse_header(data, current_offset)

        if header is None or header['data_offset'] == 0:
            # Check if we should continue
            current_offset += HEADER_SIZE
            if current_offset + 2 <= len(data):
                next_offset = struct.unpack('<H', data[current_offset:current_offset+2])[0]
                if next_offset == 0:
                    break
            else:
                break
            continue

        # Initialize pixel data position if first valid header
        if pixel_data_pos is None:
            pixel_data_pos = header['data_offset']

        # Extract animation A
        anim1 = header['anim1']
        if anim1['width'] > 0 and anim1['height'] > 0 and anim1['frames'] > 0:
            pixels_needed = anim1['width'] * anim1['height'] * anim1['frames']
            pixels = decompress_rle(data, pixel_data_pos, pixels_needed)

            output_file = output_path / f"anim_{animations_extracted:03d}_a.png"
            success = save_animation(pixels, anim1['width'], anim1['height'],
                                   anim1['frames'], output_file)

            if success:
                print(f"Animation {animations_extracted:3d}a: {anim1['width']:3d}x{anim1['height']:3d} "
                      f"× {anim1['frames']:2d} frames → {output_file.name}")

            # Move to next position (after current pixels)
            # In practice, need to track actual compressed size

        # Extract animation B
        anim2 = header['anim2']
        if anim2['width'] > 0 and anim2['height'] > 0 and anim2['frames'] > 0:
            # Offset for anim2 is after anim1
            anim2_offset = anim1['width'] * anim1['height'] * anim1['frames']
            pixels_needed = anim2['width'] * anim2['height'] * anim2['frames']

            # This is approximate - need to track actual RLE position
            pixels = decompress_rle(data, pixel_data_pos + anim2_offset * 2, pixels_needed)

            output_file = output_path / f"anim_{animations_extracted:03d}_b.png"
            success = save_animation(pixels, anim2['width'], anim2['height'],
                                   anim2['frames'], output_file)

            if success:
                print(f"Animation {animations_extracted:3d}b: {anim2['width']:3d}x{anim2['height']:3d} "
                      f"× {anim2['frames']:2d} frames → {output_file.name}")

        metadata.append({
            'index': animations_extracted,
            'header_offset': current_offset,
            'palette_id': header['palette_id'],
            'anim_a': anim1,
            'anim_b': anim2
        })

        current_offset += HEADER_SIZE
        animations_extracted += 1

        # Find next BUDA marker to advance pixel position
        while pixel_data_pos < len(data) - 4:
            if data[pixel_data_pos:pixel_data_pos+4] == b'BUDA':
                pixel_data_pos += 4
                break
            pixel_data_pos += 1

    # Save metadata
    with open(output_path / "metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 80)
    print(f"Extraction complete!")
    print(f"  Total animations: {animations_extracted}")
    print(f"  Output directory: {output_path.absolute()}")
    print("=" * 80)

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_alfred2.py <ALFRED.2> [output_dir]")
        print("\nExample:")
        print("  python extract_alfred2.py files/ALFRED.2 talking_anims/")
        sys.exit(1)

    filepath = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "talking_anims"

    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    extract_alfred2(filepath, output_dir)

if __name__ == "__main__":
    main()
