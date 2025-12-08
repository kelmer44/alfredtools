#!/usr/bin/env python3
"""
Extract the right-click settings/load/save menu screen from ALFRED.7

The menu palette is located at offset 0x7984 in ALFRED.7 (768 bytes, VGA 6-bit format).
This was discovered through Ghidra analysis and pattern matching against known correct values.

The menu image data is assembled from multiple compressed and uncompressed blocks.
"""

import sys
from pathlib import Path
from PIL import Image

def decompress_rle(data, offset, end_offset):
    size = end_offset - offset
    if size == 0x8000 or size == 0x6800:
        # Uncompressed block - read directly
        return data[offset:offset+size]
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
    alfred7 = sys.argv[1] if len(sys.argv) > 1 else "files/ALFRED.7"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "menu"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred7, 'rb') as f:
        data = f.read()

    # Find all palette BUDAs
    budas = find_budas(data)
    print(f"Found {len(budas)} BUDAs\n")

    # Menu palette is at offset 0x2884c2 in ALFRED.7 (VGA 6-bit format)
    # This was found by searching for the correct DOSBox palette values (converted to 6-bit)
    # It's located right after the menu image data ends
    MENU_PALETTE_OFFSET = 0x2884c2
    palette = extract_palette(data, MENU_PALETTE_OFFSET)
    print(f"✓ Loaded menu palette from offset {hex(MENU_PALETTE_OFFSET)}")

    TARGET_SIZE = 640 * 400
    combined = bytearray()
    combined.extend(data[2405266:2405266 + 65536])
    combined.extend(decompress_rle(data, 2470802, 2470802 + 29418))
    combined.extend(data[2500220:2500220 + 32768])
    combined.extend(decompress_rle(data, 2500220 + 32768, 2500220 + 32768 + 30288))
    combined.extend(data[2563266:2563266 + 92162])
    # palettes[len(palettes)] = extract_palette(data, 2563266 + 92162)

    menuEnd = 2563266 + 92162
    img_data = bytes(combined[:TARGET_SIZE])
    if len(img_data) < TARGET_SIZE:
        img_data += bytes([0] * (TARGET_SIZE - len(img_data)))


    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(img_data)
    output_file = output_path / f"menu.png"
    img.save(output_file)

    # for i in range(0, 7170):
    #     palette = extract_palette(data, menuEnd + i)
    #     img = Image.new('P', (640, 400))
    #     img.putpalette(palette)
    #     img.putdata(img_data)
    #     output_file = output_path / f"menu_{i}.png"
    #     img.save(output_file)
    # for i, palette in enumerate(palettes.values()):
    #   img = Image.new('P', (640, 400))
    #   img.putpalette(palette)
    #   img.putdata(img_data)
    #   output_file = output_path / f"menu_{i}.png"
    #   img.save(output_file)

    # block = decompress_rle(data, 0, budas[0])
    # output_file = output_path / f'buda START.bin'
    # output_file_raw = output_path_raw / f'buda START.bin'
    # with open(output_file, 'wb') as f:
    #     f.write(block)

    # for start_buda in range(len(budas) - 1):
    #     # Skip palette BUDAs
    #     # real_start = start_buda
    #     isPalette = False
    #     if start_buda in palettes:
    #         # real_start += 768
    #         isPalette = True

    #     # for i in range(start_buda, min(real_start + 20, len(budas) - 1)):
    #     #     if i in palettes:
    #     #         # Found a palette, stop here
    #     #         break
    #     # real_start = budas[start_buda] if isPalette else budas[start_buda] + 768
    #     print(f'Decompressing {budas[start_buda]} to {budas[start_buda + 1]} isPalette = {isPalette}')
    #     block = decompress_rle(data, budas[start_buda] + 4, budas[start_buda+1])
    #     output_file = output_path / f'buda{start_buda:03d}_offset_{budas[start_buda]}_isPalette{isPalette}.bin'
    #     with open(output_file, 'wb') as f:
    #         f.write(block)

    #     output_file_raw = output_path_raw / f'buda{start_buda:03d}_offset_{budas[start_buda]}_isPalette{isPalette}.bin'
    #     with open(output_file_raw, 'wb') as f:
    #         f.write(data[budas[start_buda]:budas[start_buda + 1]])

    #     #     if len(combined) >= TARGET_SIZE * 0.9:  # Close enough
    #     #         break

    #     # # Check if we got close to the target size
    #     # if TARGET_SIZE * 0.85 <= len(combined) <= TARGET_SIZE * 1.2:
    #     #     # Find nearest palette
    #     #     pal_buda = None
    #     #     for p_idx in palettes.keys():
    #     #         if p_idx > start_buda and p_idx <= start_buda + budas_used + 10:
    #     #             pal_buda = p_idx
    #     #             break

    #     #     if pal_buda:
    #     #         print(f"BUDA {start_buda}-{start_buda+budas_used-1}: {len(combined)} bytes, palette {pal_buda}")

    #     #         # Create image
    #     #         img_data = bytes(combined[:TARGET_SIZE])
    #     #         if len(img_data) < TARGET_SIZE:
    #     #             img_data += bytes([0] * (TARGET_SIZE - len(img_data)))

    #     #         img = Image.new('P', (640, 400))
    #     #         img.putpalette(palettes[pal_buda])
    #     #         img.putdata(img_data)

    #     #         output_file = output_path / f"buda{start_buda:03d}_to{start_buda+budas_used-1:03d}_pal{pal_buda:03d}.png"
    #     #         img.save(output_file)

if __name__ == "__main__":
    main()
