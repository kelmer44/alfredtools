#!/usr/bin/env python3
"""
Extract popup menu graphics from ALFRED.7

After scroll arrows at 0x30A6E0:
- Popup background: 640x60 pixels (38,400 bytes)
- 7 popup frames: 60x54 pixels each (3,240 bytes each, 22,680 total)
"""

import sys
from pathlib import Path
from PIL import Image

def extract_popup_graphics(alfred7_path, output_dir):
    """Extract popup background and frame icons"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred7_path, 'rb') as f:
        data = f.read()

    # Offsets and sizes
    POPUP_START = 0x30A6E0
    BG_WIDTH = 640
    BG_HEIGHT = 60
    BG_SIZE = BG_WIDTH * BG_HEIGHT  # 38,400 bytes

    FRAME_WIDTH = 60
    FRAME_HEIGHT = 54
    FRAME_SIZE = FRAME_WIDTH * FRAME_HEIGHT  # 3,240 bytes
    NUM_FRAMES = 7
    FRAMES_SIZE = FRAME_SIZE * NUM_FRAMES  # 22,680 bytes

    print("Alfred Pelrock - Popup Menu Graphics Extractor")
    print("="*70)
    print()

    # Extract popup background
    print(f"Popup Background:")
    print(f"  Offset: 0x{POPUP_START:06X}")
    print(f"  Size: {BG_WIDTH}x{BG_HEIGHT} = {BG_SIZE} bytes")

    bg_data = data[POPUP_START:POPUP_START + BG_SIZE]

    # Save raw background
    bg_raw = output_path / "popup_background.bin"
    with open(bg_raw, 'wb') as f:
        f.write(bg_data)
    print(f"  Saved: {bg_raw}")

    # Create grayscale preview
    palette = []
    for i in range(256):
        palette.extend([i, i, i])

    bg_img = Image.new('P', (BG_WIDTH, BG_HEIGHT))
    bg_img.putpalette(palette)
    bg_img.putdata(bg_data)

    bg_preview = output_path / "popup_background_preview.png"
    bg_img.save(bg_preview)
    print(f"  Preview: {bg_preview}")
    print()

    # Extract popup frames
    print(f"Popup Frames (7 action verb backgrounds):")
    print(f"  Offset: 0x{POPUP_START + BG_SIZE:06X}")
    print(f"  Size: {FRAME_WIDTH}x{FRAME_HEIGHT} per frame ({FRAME_SIZE} bytes)")
    print()

    frames_offset = POPUP_START + BG_SIZE
    frames_data = data[frames_offset:frames_offset + FRAMES_SIZE]

    # Save all frames as one file
    frames_raw = output_path / "popup_frames_all.bin"
    with open(frames_raw, 'wb') as f:
        f.write(frames_data)
    print(f"  All frames saved: {frames_raw}")
    print()

    # Extract individual frames
    for i in range(NUM_FRAMES):
        frame_offset = i * FRAME_SIZE
        frame_data = frames_data[frame_offset:frame_offset + FRAME_SIZE]

        # Save raw
        frame_raw = output_path / f"popup_frame_{i}.bin"
        with open(frame_raw, 'wb') as f:
            f.write(frame_data)

        # Create preview
        frame_img = Image.new('P', (FRAME_WIDTH, FRAME_HEIGHT))
        frame_img.putpalette(palette)
        frame_img.putdata(frame_data)

        frame_preview = output_path / f"popup_frame_{i}_preview.png"
        frame_img.save(frame_preview)

        print(f"  Frame {i}: {frame_raw.name} / {frame_preview.name}")

    # Create combined strip preview
    print()
    print("Creating combined preview...")
    strip_width = FRAME_WIDTH * NUM_FRAMES
    strip_img = Image.new('P', (strip_width, FRAME_HEIGHT))
    strip_img.putpalette(palette)

    strip_pixels = []
    for y in range(FRAME_HEIGHT):
        for f in range(NUM_FRAMES):
            frame_offset = f * FRAME_SIZE
            for x in range(FRAME_WIDTH):
                pixel_offset = frame_offset + (y * FRAME_WIDTH) + x
                strip_pixels.append(frames_data[pixel_offset])

    strip_img.putdata(strip_pixels)
    strip_file = output_path / "popup_frames_strip_preview.png"
    strip_img.save(strip_file)
    print(f"  Strip preview: {strip_file}")

    # Create info file
    info_file = output_path / "popup_graphics_info.txt"
    with open(info_file, 'w') as f:
        f.write("Alfred Pelrock - Popup Menu Graphics\n")
        f.write("="*70 + "\n\n")
        f.write(f"Source: ALFRED.7\n\n")
        f.write("POPUP BACKGROUND:\n")
        f.write(f"  Offset: 0x{POPUP_START:06X} ({POPUP_START} decimal)\n")
        f.write(f"  Dimensions: {BG_WIDTH}x{BG_HEIGHT} pixels\n")
        f.write(f"  Size: {BG_SIZE} bytes (0x{BG_SIZE:X})\n")
        f.write(f"  Description: Horizontal bar background for action menu\n\n")
        f.write("POPUP FRAMES (Action Verb Backgrounds):\n")
        f.write(f"  Offset: 0x{frames_offset:06X} ({frames_offset} decimal)\n")
        f.write(f"  Dimensions: {FRAME_WIDTH}x{FRAME_HEIGHT} pixels per frame\n")
        f.write(f"  Frame size: {FRAME_SIZE} bytes (0x{FRAME_SIZE:X})\n")
        f.write(f"  Number of frames: {NUM_FRAMES}\n")
        f.write(f"  Total size: {FRAMES_SIZE} bytes (0x{FRAMES_SIZE:X})\n")
        f.write(f"  Description: Background frames for individual verb icons\n\n")
        f.write("Format: 8-bit indexed color (256 colors)\n")
        f.write("Palette: Apply game palette for correct colors\n\n")
        f.write("Ghidra References:\n")
        f.write("  render_action_popup_menu @ 0x1AD9A\n")
        f.write("  Scroll arrows loaded from 0x309D80 (20x60 each)\n")
        f.write("  Popup data starts at 0x30A6E0\n\n")
        f.write("Usage:\n")
        f.write("  Background displayed at Y=340 (0x154)\n")
        f.write("  Frames shown when hovering over actions\n")
        f.write("  Up to 10 verb icons visible at once\n")

    print(f"\nInfo file: {info_file}")
    print()
    print("="*70)
    print(f"Extraction complete!")
    print(f"Output directory: {output_path.absolute()}")
    print()
    print("Note: Preview images use grayscale palette.")
    print("Apply correct game palette for accurate colors.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_popup_graphics.py <alfred.7> [output_dir]")
        print("\nExample:")
        print("  python extract_popup_graphics.py ALFRED.7")
        print("  python extract_popup_graphics.py ALFRED.7 popup_graphics/")
        sys.exit(1)

    alfred7_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "popup_graphics"

    if not Path(alfred7_path).exists():
        print(f"Error: File not found: {alfred7_path}")
        sys.exit(1)

    extract_popup_graphics(alfred7_path, output_dir)
