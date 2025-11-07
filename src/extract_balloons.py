#!/usr/bin/env python3
"""
Extract popup icons and speech balloons from ALFRED.4
Using Palette 11 from ALFRED.1 for correct colors
"""

import sys
import struct
from pathlib import Path
from PIL import Image

def extract_palette_11(alfred1_path):
    """Extract palette 11 from ALFRED.1 room 0"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    ROOM_STRUCT_SIZE = 104
    room_num = 0

    room_offset = room_num * ROOM_STRUCT_SIZE
    pair11_offset = room_offset + (11 * 8)

    offset = struct.unpack('<I', data[pair11_offset:pair11_offset+4])[0]
    size = struct.unpack('<I', data[pair11_offset+4:pair11_offset+8])[0]

    if size != 0x300:
        print(f"Warning: Palette size is {size}, expected 768")
        return None

    palette_data = data[offset:offset+768]

    # Convert VGA 6-bit to 8-bit (multiply by 4)
    palette = []
    for i in range(256):
        r = palette_data[i*3] * 4
        g = palette_data[i*3+1] * 4
        b = palette_data[i*3+2] * 4
        palette.extend([r, g, b])

    return palette

def decompress_rle(data, offset, max_size=200000):
    """Decompress RLE data"""
    result = bytearray()
    pos = offset

    while len(result) < max_size and pos + 2 <= len(data):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break

        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    return bytes(result), pos - offset

def extract_alfred4_with_palette(alfred4_path, alfred1_path, output_dir):
    """Extract all graphics with correct palette"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Load palette
    print("Loading palette 11 from ALFRED.1...")
    palette = extract_palette_11(alfred1_path)
    if palette is None:
        print("Error: Could not load palette!")
        return
    print("✓ Palette loaded (256 colors)\n")

    # Load ALFRED.4
    with open(alfred4_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - ALFRED.4 Graphics (With Palette 11)")
    print("="*70)
    print()

    # ===== POPUP ICONS =====
    ICON_WIDTH = 60
    ICON_HEIGHT = 60
    ICON_SIZE = ICON_WIDTH * ICON_HEIGHT
    NUM_ICONS = 9

    print(f"POPUP ICONS ({ICON_WIDTH}×{ICON_HEIGHT}):")
    print(f"  Offset: 0x000000")
    print(f"  Count: {NUM_ICONS}")
    print()

    icons_data = data[0:ICON_SIZE * NUM_ICONS]

    # Extract individual icons with palette
    for i in range(NUM_ICONS):
        icon_offset = i * ICON_SIZE
        icon_data = icons_data[icon_offset:icon_offset + ICON_SIZE]

        # Save with color
        icon_img = Image.new('P', (ICON_WIDTH, ICON_HEIGHT))
        icon_img.putpalette(palette)
        icon_img.putdata(icon_data)

        icon_file = output_path / f"popup_icon_{i}_color.png"
        icon_img.save(icon_file)
        print(f"  Icon {i}: {icon_file.name}")

    # Create strip with all icons
    strip_width = ICON_WIDTH * NUM_ICONS
    strip_img = Image.new('P', (strip_width, ICON_HEIGHT))
    strip_img.putpalette(palette)

    strip_pixels = []
    for y in range(ICON_HEIGHT):
        for icon in range(NUM_ICONS):
            icon_offset = icon * ICON_SIZE
            for x in range(ICON_WIDTH):
                pixel_offset = icon_offset + (y * ICON_WIDTH) + x
                strip_pixels.append(icons_data[pixel_offset])

    strip_img.putdata(strip_pixels)
    strip_file = output_path / "popup_icons_strip_color.png"
    strip_img.save(strip_file)
    print(f"\n  All icons strip: {strip_file.name}")

    # ===== SPEECH BALLOONS =====
    BALLOON_WIDTH = 247
    BALLOON_HEIGHT = 112
    FRAME_SIZE = BALLOON_WIDTH * BALLOON_HEIGHT

    BUDA_OFFSETS = [0x008F2E, 0x00A57A]

    print()
    print(f"SPEECH BALLOONS ({BALLOON_WIDTH}×{BALLOON_HEIGHT}):")
    print()

    for buda_idx, buda_offset in enumerate(BUDA_OFFSETS):
        print(f"  Set {buda_idx} (BUDA at 0x{buda_offset:06X}):")

        # Decompress
        decompressed, compressed_size = decompress_rle(data, buda_offset + 4, FRAME_SIZE * 4 + 10000)

        print(f"    Compressed: {compressed_size} bytes")
        print(f"    Decompressed: {len(decompressed)} bytes")

        # Also save raw
        rle_raw = output_path / f"decompressed_{buda_idx}.bin"
        with open(rle_raw, 'wb') as f:
            f.write(decompressed)


        # Determine frames
        frames = 4 if len(decompressed) >= FRAME_SIZE * 4 * 0.9 else 2
        # frames = 2
        print(f"    Frames: {frames}")

        actual_data = decompressed[:FRAME_SIZE * frames]

        # Save combined preview
        preview_width = BALLOON_WIDTH * frames
        combined_img = Image.new('P', (preview_width, BALLOON_HEIGHT))
        combined_img.putpalette(palette)

        combined_pixels = []
        for y in range(BALLOON_HEIGHT):
            for f in range(frames):
                frame_offset = f * FRAME_SIZE
                for x in range(BALLOON_WIDTH):
                    pixel_offset = frame_offset + (y * BALLOON_WIDTH) + x
                    if pixel_offset < len(actual_data):
                        combined_pixels.append(actual_data[pixel_offset])
                    else:
                        combined_pixels.append(0)

        combined_img.putdata(combined_pixels)
        combined_file = output_path / f"speech_balloon_{buda_idx}_4frames_color.png"
        combined_img.save(combined_file)
        print(f"    Combined: {combined_file.name}")

        # Extract individual frames
        for f in range(frames):
            frame_offset = f * FRAME_SIZE
            frame_data = actual_data[frame_offset:frame_offset + FRAME_SIZE]

            if len(frame_data) < FRAME_SIZE:
                break

            # Save raw
            frame_raw = output_path / f"speech_balloon_{buda_idx}_frame{f}.bin"
            with open(frame_raw, 'wb') as file:
                file.write(frame_data)

            # Save with color
            frame_img = Image.new('P', (BALLOON_WIDTH, BALLOON_HEIGHT))
            frame_img.putpalette(palette)
            frame_img.putdata(frame_data)

            frame_file = output_path / f"speech_balloon_{buda_idx}_frame{f}_color.png"
            frame_img.save(frame_file)
            print(f"      Frame {f}: {frame_file.name}")

        print()

    # Create info file
    info_file = output_path / "alfred4_info.txt"
    with open(info_file, 'w') as f:
        f.write("Alfred Pelrock - ALFRED.4 Graphics\n")
        f.write("Extracted with Palette 11 from ALFRED.1\n")
        f.write("="*70 + "\n\n")

        f.write("POPUP ICONS:\n")
        f.write(f"  Location: ALFRED.4 offset 0x000000\n")
        f.write(f"  Dimensions: {ICON_WIDTH}×{ICON_HEIGHT} pixels\n")
        f.write(f"  Count: {NUM_ICONS} icons\n")
        f.write(f"  Format: Raw uncompressed\n")
        f.write(f"  Total: {ICON_SIZE * NUM_ICONS} bytes\n\n")

        f.write("SPEECH BALLOONS:\n")
        f.write(f"  Dimensions: {BALLOON_WIDTH}×{BALLOON_HEIGHT} pixels\n")
        f.write(f"  Format: RLE compressed (BUDA markers)\n")
        f.write(f"  Frames per set: 4\n\n")

        f.write(f"  Set 0: BUDA at 0x008F2E (~5.7 KB compressed)\n")
        f.write(f"  Set 1: BUDA at 0x00A57A (~38 KB compressed)\n\n")

        f.write("PALETTE:\n")
        f.write(f"  Source: ALFRED.1, Room 0, Pair 11\n")
        f.write(f"  Offset in ALFRED.1: 0x02317C\n")
        f.write(f"  Format: VGA 6-bit RGB (converted to 8-bit)\n")
        f.write(f"  Colors: 256\n\n")

        f.write("FILES:\n")
        f.write(f"  *_color.png - Images with correct palette\n")
        f.write(f"  *.bin - Raw indexed bitmap data\n")

    print(f"Info saved: {info_file}")
    print()
    print("="*70)
    print("Extraction complete!")
    print(f"Output: {output_path.absolute()}")
    print()
    print("All images now use the correct VGA palette from ALFRED.1!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nUsage: python extract_alfred4_color.py <alfred.4> <alfred.1> [output_dir]")
        print("\nExample:")
        print("  python extract_alfred4_color.py ALFRED.4 ALFRED.1")
        print("  python extract_alfred4_color.py ALFRED.4 ALFRED.1 alfred4_color/")
        sys.exit(1)

    alfred4_path = sys.argv[1]
    alfred1_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "alfred4_color"

    if not Path(alfred4_path).exists():
        print(f"Error: File not found: {alfred4_path}")
        sys.exit(1)

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    extract_alfred4_with_palette(alfred4_path, alfred1_path, output_dir)
