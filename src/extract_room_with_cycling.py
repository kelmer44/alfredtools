#!/usr/bin/env python3
"""
Alfred Pelrock - Room Background with Palette Cycling Animation
Extracts a room background and creates multiple frames showing palette cycling animation
"""

import struct
import sys
from pathlib import Path
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
        return palette, palette_data
    return None, None

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

def get_palette_cycling_config(alfred9_data, room_num):
    """Get palette cycling config from ALFRED.9"""
    ROOM_SIZE = 1024
    room_offset = room_num * ROOM_SIZE
    room_data = alfred9_data[room_offset:room_offset + ROOM_SIZE]

    # Search for valid cycling config
    for offset in range(len(room_data) - 12):
        mode = room_data[offset + 1]
        if mode < 1 or mode > 10:
            continue
        rgb_values = room_data[offset+2:offset+11]
        if not all(v <= 63 for v in rgb_values):
            continue

        config_bytes = room_data[offset:offset+12]
        return {
            'start_index': config_bytes[0],
            'mode': mode,
            'current_rgb': [config_bytes[2], config_bytes[3], config_bytes[4]],
            'min_rgb': [config_bytes[5], config_bytes[6], config_bytes[7]],
            'max_rgb': [config_bytes[8], config_bytes[9], config_bytes[10]],
            'flags': config_bytes[11],
            'direction': 'max' if config_bytes[11] & 0x40 else 'min',
            'speed': config_bytes[11] & 0x3F
        }
    return None

def apply_palette_cycling_rotate(palette_data, config, frame_num):
    """Apply rotate mode palette cycling for a given frame"""
    palette = list(palette_data)  # Make a copy

    start_idx = config['start_index']
    mode = config['mode']  # mode value indicates number of colors to rotate
    num_colors = mode

    # Rotate the palette entries
    rotation = frame_num % num_colors

    # Extract the colors to rotate (3 bytes each)
    colors_to_rotate = []
    for i in range(num_colors):
        idx = (start_idx + i) * 3
        colors_to_rotate.append([palette[idx], palette[idx+1], palette[idx+2]])

    # Apply rotation
    for i in range(num_colors):
        src_idx = (i + rotation) % num_colors
        dst_idx = (start_idx + i) * 3
        palette[dst_idx] = colors_to_rotate[src_idx][0]
        palette[dst_idx+1] = colors_to_rotate[src_idx][1]
        palette[dst_idx+2] = colors_to_rotate[src_idx][2]

    return palette

def apply_palette_cycling_fade(palette_data, config, frame_num, total_frames):
    """Apply fade mode palette cycling for a given frame"""
    palette = list(palette_data)  # Make a copy

    start_idx = config['start_index']
    r_min, g_min, b_min = config['min_rgb']
    r_max, g_max, b_max = config['max_rgb']

    # Calculate interpolation factor (0.0 to 1.0)
    t = frame_num / (total_frames - 1) if total_frames > 1 else 0.0

    # Ping-pong: go from min to max and back
    if config['direction'] == 'max':
        if t <= 0.5:
            t = t * 2  # 0 to 1
        else:
            t = (1.0 - t) * 2  # 1 to 0

    # Interpolate RGB
    r = int(r_min + (r_max - r_min) * t)
    g = int(g_min + (g_max - g_min) * t)
    b = int(b_min + (b_max - b_min) * t)

    # Apply to palette entry (multiply by 4 for 8-bit)
    idx = start_idx * 3
    palette[idx] = r * 4
    palette[idx+1] = g * 4
    palette[idx+2] = b * 4

    return palette

def create_cycling_frames(alfred1_path, alfred9_path, room_num, num_frames, output_dir):
    """Create multiple frames showing palette cycling animation"""

    # Read ALFRED.1
    with open(alfred1_path, 'rb') as f:
        alfred1_data = f.read()

    # Read ALFRED.9
    with open(alfred9_path, 'rb') as f:
        alfred9_data = f.read()

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Extracting room {room_num} with palette cycling animation...")
    print("=" * 70)

    # Extract background and base palette
    room_offset = room_num * 104
    background_data = extract_background(alfred1_data, room_offset)
    base_palette, palette_data_6bit = extract_palette(alfred1_data, room_offset)

    if not base_palette or not palette_data_6bit:
        print(f"ERROR: Could not extract palette for room {room_num}")
        return

    WIDTH = 640
    HEIGHT = 400
    EXPECTED_SIZE = WIDTH * HEIGHT

    if len(background_data) < EXPECTED_SIZE * 0.9:
        print(f"ERROR: Background data too small ({len(background_data)} bytes)")
        return

    # Pad if needed
    img_data = background_data[:EXPECTED_SIZE]
    if len(img_data) < EXPECTED_SIZE:
        img_data += bytes([0] * (EXPECTED_SIZE - len(img_data)))

    # Get palette cycling config
    cycling_config = get_palette_cycling_config(alfred9_data, room_num)

    if not cycling_config:
        print(f"No palette cycling found for room {room_num}")
        print("Creating single frame with base palette...")
        img = Image.new('P', (WIDTH, HEIGHT))
        img.putpalette(base_palette)
        img.putdata(img_data)
        output_file = output_path / f"room_{room_num:02d}_frame_00.png"
        img.save(output_file)
        print(f"Saved: {output_file.name}")
        return

    print(f"Palette cycling config:")
    print(f"  Mode: {cycling_config['mode']} ({'fade' if cycling_config['mode'] == 1 else 'rotate'})")
    print(f"  Start index: {cycling_config['start_index']}")
    print(f"  Current RGB: {cycling_config['current_rgb']}")
    print(f"  Min RGB: {cycling_config['min_rgb']}")
    print(f"  Max RGB: {cycling_config['max_rgb']}")
    print(f"  Direction: {cycling_config['direction']}, Speed: {cycling_config['speed']}")
    print()

    # Generate frames
    print(f"Generating {num_frames} frames...")

    for frame_num in range(num_frames):
        # Apply palette cycling
        if cycling_config['mode'] == 1:
            # Fade mode
            animated_palette = apply_palette_cycling_fade(
                palette_data_6bit, cycling_config, frame_num, num_frames
            )
            # Convert to 8-bit
            palette_8bit = []
            for i in range(256):
                palette_8bit.extend([
                    animated_palette[i*3] * 4,
                    animated_palette[i*3+1] * 4,
                    animated_palette[i*3+2] * 4
                ])
        else:
            # Rotate mode
            animated_palette = apply_palette_cycling_rotate(
                palette_data_6bit, cycling_config, frame_num
            )
            # Convert to 8-bit
            palette_8bit = []
            for i in range(256):
                palette_8bit.extend([
                    animated_palette[i*3] * 4,
                    animated_palette[i*3+1] * 4,
                    animated_palette[i*3+2] * 4
                ])

        # Create image with animated palette
        img = Image.new('P', (WIDTH, HEIGHT))
        img.putpalette(palette_8bit)
        img.putdata(img_data)

        output_file = output_path / f"room_{room_num:02d}_frame_{frame_num:02d}.png"
        img.save(output_file)
        print(f"  Frame {frame_num:2d}: {output_file.name}")

    print()
    print("=" * 70)
    print(f"Created {num_frames} frames in {output_path.absolute()}")
    print()
    print("To create an animated GIF:")
    print(f"  convert -delay 10 -loop 0 {output_path}/room_{room_num:02d}_frame_*.png room_{room_num:02d}_animated.gif")
    print("=" * 70)

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nUsage: python extract_room_with_cycling.py <alfred.1> <alfred.9> <room_num> [num_frames] [output_dir]")
        print("\nExamples:")
        print("  python extract_room_with_cycling.py ALFRED.1 ALFRED.9 2")
        print("  python extract_room_with_cycling.py ALFRED.1 ALFRED.9 2 16 frames/")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    alfred9_path = sys.argv[2]
    room_num = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    num_frames = int(sys.argv[4]) if len(sys.argv) > 4 else 8
    output_dir = sys.argv[5] if len(sys.argv) > 5 else f"room_{room_num:02d}_cycling"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    if not Path(alfred9_path).exists():
        print(f"Error: File not found: {alfred9_path}")
        sys.exit(1)

    create_cycling_frames(alfred1_path, alfred9_path, room_num, num_frames, output_dir)

if __name__ == "__main__":
    main()
