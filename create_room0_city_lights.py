#!/usr/bin/env python3
"""
Create Room 0 city lights animation using the actual palette cycling values.

Room 0 has a window to the city at night with building windows that turn on/off.
Uses Mode 6 ROTATE with 6 palette indices (200-205) cycling every ~5 seconds.
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

def create_palette_rotation(base_palette, start_index, count, frames=2):
    """
    Create a series of palettes showing rotation animation.

    Args:
        base_palette: Base palette (768 bytes, 256 colors)
        start_index: Starting palette index for rotation
        count: Number of colors to rotate
        frames: Number of rotation frames (default 2 for on/off effect)

    Returns:
        List of modified palettes
    """
    palettes = []
    
    # Extract the colors that will rotate
    rotating_colors = []
    for i in range(count):
        idx = start_index + i
        color = (
            base_palette[idx * 3],
            base_palette[idx * 3 + 1],
            base_palette[idx * 3 + 2]
        )
        rotating_colors.append(color)
    
    # Create rotation frames
    for frame in range(frames):
        new_palette = list(base_palette)
        
        # Rotate the colors
        for i in range(count):
            idx = start_index + i
            # Get color from rotated position
            rotated_color = rotating_colors[(i + frame) % count]
            new_palette[idx * 3] = rotated_color[0]
            new_palette[idx * 3 + 1] = rotated_color[1]
            new_palette[idx * 3 + 2] = rotated_color[2]
        
        palettes.append(new_palette)
    
    return palettes

def main():
    alfred1_path = 'files/ALFRED.1'
    room_num = 0

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

    # Room 0 cycling config found at 0x4B88C:
    # Raw bytes: c806005ae004000467070001
    # Mode 6 (ROTATE), palette indices 200-205 (6 colors)
    # Byte 3 = 90 (0x5A) = ~5 second delay at 18 FPS
    start_index = 200  # 0xC8
    rotation_count = 6
    
    print(f"Creating rotation animation for palette indices {start_index}-{start_index+rotation_count-1}...")
    print(f"  Mode: 6 (ROTATE {rotation_count} colors)")
    print(f"  Delay: 90 frames (~5 seconds at 18 FPS)")
    
    # Print the colors being rotated
    print(f"\nColors in rotation:")
    for i in range(rotation_count):
        idx = start_index + i
        r = palette[idx * 3]
        g = palette[idx * 3 + 1]
        b = palette[idx * 3 + 2]
        print(f"  Index {idx}: RGB({r}, {g}, {b})")

    # Create rotation palettes
    # For city windows, we want to show the full cycle
    rotation_palettes = create_palette_rotation(palette, start_index, rotation_count, frames=rotation_count)

    # Create animated GIF
    print("\nGenerating animated GIF...")
    frames = []
    for i, rot_palette in enumerate(rotation_palettes):
        frame = Image.new('P', (640, 400))
        frame.putpalette(rot_palette)
        frame.putdata(final_pixels)
        frames.append(frame)

    output_path = 'room_00_city_lights.gif'
    # Use longer duration to match the ~5 second in-game delay
    # 5000ms / 6 frames = ~833ms per frame
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=833,  # ~833ms per frame for 5 second cycle
        loop=0
    )

    print(f"Animation saved to: {output_path}")
    print(f"Total frames: {len(frames)}")
    print("\nThis animation shows the city windows at night cycling through")
    print(f"6 palette indices ({start_index}-{start_index+rotation_count-1}), creating the")
    print("effect of building windows turning on and off.")

if __name__ == '__main__':
    main()
