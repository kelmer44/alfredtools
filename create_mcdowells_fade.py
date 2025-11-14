#!/usr/bin/env python3
"""
Create accurate McDowells sign fade animation using the actual min/max RGB values.
"""

import struct
from PIL import Image

def decompress_rle_block(data, offset, size):
    """Decompress a single block - handles both RLE and uncompressed"""
    if size == 0x8000 or size == 0x6800:
        return data[offset:offset+size]

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
    pair_offset = room_offset + (11 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size == 0x300:
        palette_data = data[offset:offset+768]
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
    for pair_idx in range(8):
        pair_offset = room_offset + (pair_idx * 8)
        offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
        size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]
        if offset > 0 and size > 0 and offset < len(data):
            pairs.append((offset, size))

    combined = bytearray()
    for offset, size in pairs:
        block_data = decompress_rle_block(data, offset, size)
        combined.extend(block_data)
    return bytes(combined)

def create_palette_fade(base_palette, palette_index, min_rgb, max_rgb, steps=16):
    """
    Create a series of palettes showing a fade animation.

    Args:
        base_palette: Base palette (768 bytes, 256 colors)
        palette_index: Index to animate (0-255)
        min_rgb: Minimum RGB values (r, g, b) in 8-bit format
        max_rgb: Maximum RGB values (r, g, b) in 8-bit format
        steps: Number of steps in the fade

    Returns:
        List of modified palettes
    """
    palettes = []

    # Fade from current -> max -> min -> max (full cycle)
    current_r = base_palette[palette_index * 3]
    current_g = base_palette[palette_index * 3 + 1]
    current_b = base_palette[palette_index * 3 + 2]

    min_r, min_g, min_b = min_rgb
    max_r, max_g, max_b = max_rgb

    # Create fade: current -> max -> min -> current
    cycle_steps = [
        # Go to max
        *[i / steps for i in range(steps + 1)],
        # Stay at max briefly
        1.0, 1.0,
        # Go to min
        *[1.0 - (i / steps) for i in range(steps + 1)],
        # Stay at min briefly
        0.0, 0.0,
        # Back to max
        *[i / steps for i in range(steps + 1)],
    ]

    for t in cycle_steps:
        new_palette = list(base_palette)

        # Interpolate between min and max
        new_r = int(min_r + (max_r - min_r) * t)
        new_g = int(min_g + (max_g - min_g) * t)
        new_b = int(min_b + (max_b - min_b) * t)

        new_palette[palette_index * 3] = new_r
        new_palette[palette_index * 3 + 1] = new_g
        new_palette[palette_index * 3 + 2] = new_b

        palettes.append(new_palette)

    return palettes

def main():
    alfred1_path = 'files/ALFRED.1'
    room_num = 2

    print(f"Reading room {room_num} data...")

    with open(alfred1_path, 'rb') as f:
        file_data = f.read()

    room_offset = room_num * 104

    # Extract palette and background
    palette = extract_palette(file_data, room_offset)
    background_data = extract_background(file_data, room_offset)

    # Trim to 640x400
    WIDTH = 640
    HEIGHT = 400
    EXPECTED_SIZE = WIDTH * HEIGHT
    final_pixels = background_data[:EXPECTED_SIZE]
    if len(final_pixels) < EXPECTED_SIZE:
        final_pixels += bytes([0] * (EXPECTED_SIZE - len(final_pixels)))

    # Create base image
    base_img = Image.new('P', (640, 400))
    base_img.putpalette(palette)
    base_img.putdata(final_pixels)

    # User-provided min/max values (8-bit RGB)
    # Darkest: R48 G81 B32
    # Lightest: R146 G178 B32
    min_rgb = (48, 81, 32)
    max_rgb = (146, 178, 32)

    # The animating palette index is 250 (found in JUEGO.EXE at 0x0004B860)
    # Config: FA 01 24 2C 08 0C 14 08 24 2C 08 05
    # Mode 1 (fade), palette index 250, min=(12,20,8), max=(36,44,8) in 6-bit
    palette_index = 250

    print(f"Creating fade animation for palette index {palette_index}...")
    print(f"  Min RGB: {min_rgb}")
    print(f"  Max RGB: {max_rgb}")
    print(f"  Base RGB: ({palette[palette_index*3]}, {palette[palette_index*3+1]}, {palette[palette_index*3+2]})")

    # Create fade palettes
    fade_palettes = create_palette_fade(palette, palette_index, min_rgb, max_rgb, steps=12)

    # Create animated GIF
    print("Generating animated GIF...")
    frames = []
    for i, fade_palette in enumerate(fade_palettes):
        frame = Image.new('P', (640, 400))
        frame.putpalette(fade_palette)
        frame.putdata(final_pixels)
        frames.append(frame)

    output_path = 'room_02_mcdowells_fade.gif'
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,  # 50ms per frame
        loop=0
    )

    print(f"Animation saved to: {output_path}")
    print(f"Total frames: {len(frames)}")
    print("\nThis animation shows the McDowells sign logo fading between:")
    print(f"  Darkest green: RGB{min_rgb}")
    print(f"  Lightest green: RGB{max_rgb}")

if __name__ == '__main__':
    main()
