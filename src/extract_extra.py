#!/usr/bin/env python3
"""
Extract extra screens (close-ups) from ALFRED.7
These are 640x400 non-interactive full-screen images
"""

import struct
import sys
from pathlib import Path
from PIL import Image


def decompress_rle_block(data, offset, end_offset):
    """
    Decompress RLE block until BUDA marker or end
    Format: [count][value] pairs
    """
    result = bytearray()
    pos = offset

    while pos + 2 <= min(end_offset, len(data)):
        # Check for BUDA marker
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break

        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    return bytes(result)


def find_all_buda_markers(data):
    """Find all BUDA marker positions"""
    positions = []
    pos = 0
    while pos < len(data) - 4:
        if data[pos:pos+4] == b'BUDA':
            positions.append(pos)
        pos += 1
    return positions


def find_palette_for_screen(data, buda_positions, screen_buda_idx):
    """
    Find the palette for a screen by searching nearby BUDA blocks
    Palettes are stored RAW (uncompressed) as 768 bytes right after BUDA
    Returns palette data or None
    """
    # Search strategy:
    # 1. Check previous BUDA (most common)
    # 2. Check next few BUDAs
    # 3. Check a few BUDAs before

    search_indices = []

    # Check previous BUDA first
    if screen_buda_idx > 0:
        search_indices.append(screen_buda_idx - 1)

    # Then check next few BUDAs
    for i in range(1, 16):
        if screen_buda_idx + i < len(buda_positions):
            search_indices.append(screen_buda_idx + i)

    # Then check a few before
    for i in range(2, 16):
        if screen_buda_idx - i >= 0:
            search_indices.append(screen_buda_idx - i)

    for idx in search_indices:
        if idx < 0 or idx >= len(buda_positions) - 1:
            continue

        # Read RAW palette data (not RLE compressed!)
        palette_start = buda_positions[idx] + 4

        if palette_start + 768 > len(data):
            continue

        palette = data[palette_start:palette_start + 768]

        # Check if it's a VGA palette (max value <= 63)
        max_val = max(palette)
        if max_val <= 63:
            non_zero = sum(1 for b in palette if b > 0)
            if non_zero > 100:  # Must have some variety
                return palette, idx

    return None, None


def extract_screen_at_buda(data, buda_positions, buda_index):
    """
    Extract a screen starting at a BUDA marker
    Returns: (image_data, palette_data, palette_buda_idx, blocks_used)
    """
    WIDTH = 640
    HEIGHT = 400
    EXPECTED_SIZE = WIDTH * HEIGHT

    combined = bytearray()
    blocks_used = 0

    # Start after this BUDA marker
    start_idx = buda_index

    # Decompress blocks until we have a full screen
    for i in range(start_idx, min(start_idx + 20, len(buda_positions) - 1)):
        block_start = buda_positions[i] + 4
        block_end = buda_positions[i + 1]

        block_data = decompress_rle_block(data, block_start, block_end)
        combined.extend(block_data)
        blocks_used += 1

        if len(combined) >= EXPECTED_SIZE:
            break

    # Check if we got a full screen
    if len(combined) < EXPECTED_SIZE * 0.95:
        return None, None, None, 0

    if len(combined) > EXPECTED_SIZE * 1.1:
        return None, None, None, 0

    # Trim to exact size
    image_data = bytes(combined[:EXPECTED_SIZE])

    # Find palette for this screen
    palette_data, palette_idx = find_palette_for_screen(data, buda_positions, buda_index)

    return image_data, palette_data, palette_idx, blocks_used


def extract_all_screens(alfred7_path, output_dir):
    """Extract all extra screens from ALFRED.7"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred7_path, 'rb') as f:
        data = f.read()

    print(f"ALFRED.7 size: {len(data)} bytes ({len(data) / 1024 / 1024:.2f} MB)")

    buda_positions = find_all_buda_markers(data)
    print(f"Found {len(buda_positions)} BUDA markers")
    print("\n" + "="*70)
    print("Extracting screens...\n")

    WIDTH = 640
    HEIGHT = 400
    extracted = 0
    i = 0

    while i < len(buda_positions) - 1:
        image_data, palette_data, palette_idx, blocks_used = extract_screen_at_buda(data, buda_positions, i)

        if image_data:
            # Create image
            if palette_data:
                # VGA 6-bit palette - convert to 8-bit
                palette = []
                for j in range(256):
                    r = palette_data[j * 3] * 4
                    g = palette_data[j * 3 + 1] * 4
                    b = palette_data[j * 3 + 2] * 4
                    palette.extend([r, g, b])

                img = Image.new('P', (WIDTH, HEIGHT))
                img.putpalette(palette)
                img.putdata(image_data)
            else:
                # No palette - use grayscale
                img = Image.new('L', (WIDTH, HEIGHT))
                img.putdata(image_data)

            output_file = output_path / f"extra_screen_{extracted:02d}_buda{i:03d}.png"
            img.save(output_file)

            if palette_data and palette_idx is not None:
                palette_status = f"palette=BUDA#{palette_idx}"
            elif palette_data:
                palette_status = "palette=found"
            else:
                palette_status = "NO PALETTE"

            print(f"Screen {extracted:2d}: BUDA #{i:3d} -> {output_file.name} ({palette_status}, {blocks_used} blocks)")

            extracted += 1

            # Skip past the blocks we used
            i += blocks_used
        else:
            i += 1

    print("\n" + "="*70)
    print(f"Extracted {extracted} screens to {output_path.absolute()}")
    print("="*70)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_alfred7_screens.py <ALFRED.7> [output_dir]")
        print("\nExtracts all 640x400 extra screens from ALFRED.7")
        sys.exit(1)

    alfred7_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "alfred7_screens"

    if not Path(alfred7_path).exists():
        print(f"Error: File not found: {alfred7_path}")
        sys.exit(1)

    extract_all_screens(alfred7_path, output_dir)


if __name__ == "__main__":
    main()
