#!/usr/bin/env python3
"""
Systematically extract BUDA ranges to find 640x400 screens
"""

import sys
from pathlib import Path
from PIL import Image

def decompress_rle(data, offset, end_offset):
    result = bytearray()
    pos = offset
    while pos + 2 <= min(end_offset, len(data)):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break
        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2
    return bytes(result)

def find_budas(data):
    budas = []
    pos = 0
    while pos < len(data) - 4:
        if data[pos:pos+4] == b'BUDA':
            budas.append(pos)
        pos += 1
    return budas

def is_valid_palette(data, offset):
    if offset + 768 > len(data):
        return False
    pal_data = data[offset:offset+768]
    return all(b <= 63 for b in pal_data) and len(set(pal_data)) > 10

def extract_palette(data, offset):
    pal_data = data[offset:offset+768]
    palette = []
    for i in range(256):
        r = min(255, pal_data[i * 3] * 4)
        g = min(255, pal_data[i * 3 + 1] * 4)
        b = min(255, pal_data[i * 3 + 2] * 4)
        palette.extend([r, g, b])
    return palette

def main():
    alfred7 = sys.argv[1] if len(sys.argv) > 1 else "ALFRED.7"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "buda_scan"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred7, 'rb') as f:
        data = f.read()

    budas = find_budas(data)
    print(f"Found {len(budas)} BUDAs\n")

    # Find all palette BUDAs
    palettes = {}
    for i, buda in enumerate(budas):
        if is_valid_palette(data, buda + 4):
            palettes[i] = extract_palette(data, buda + 4)
            print(f"BUDA {i}: palette")

    print(f"\nFound {len(palettes)} palettes\n")
    print("="*70)

    # Now try combining consecutive BUDAs to get 640x400 images
    TARGET_SIZE = 640 * 400

    for start_buda in range(len(budas) - 1):
        # Skip palette BUDAs
        if start_buda in palettes:
            continue

        # Decompress and combine BUDAs until we have enough data
        combined = bytearray()
        budas_used = 0

        for i in range(start_buda, min(start_buda + 20, len(budas) - 1)):
            if i in palettes:
                # Found a palette, stop here
                break

            block = decompress_rle(data, budas[i] + 4, budas[i+1])
            combined.extend(block)
            budas_used += 1

            if len(combined) >= TARGET_SIZE * 0.9:  # Close enough
                break

        # Check if we got close to the target size
        if TARGET_SIZE * 0.85 <= len(combined) <= TARGET_SIZE * 1.2:
            # Find nearest palette
            pal_buda = None
            for p_idx in palettes.keys():
                if p_idx > start_buda and p_idx <= start_buda + budas_used + 10:
                    pal_buda = p_idx
                    break

            if pal_buda:
                print(f"BUDA {start_buda}-{start_buda+budas_used-1}: {len(combined)} bytes, palette {pal_buda}")

                # Create image
                img_data = bytes(combined[:TARGET_SIZE])
                if len(img_data) < TARGET_SIZE:
                    img_data += bytes([0] * (TARGET_SIZE - len(img_data)))

                img = Image.new('P', (640, 400))
                img.putpalette(palettes[pal_buda])
                img.putdata(img_data)

                output_file = output_path / f"buda{start_buda:03d}_to{start_buda+budas_used-1:03d}_pal{pal_buda:03d}.png"
                img.save(output_file)

if __name__ == "__main__":
    main()
