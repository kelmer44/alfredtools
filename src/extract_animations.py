#!/usr/bin/env python3
"""
Extract all 4 animations from Room 13 of ALFRED.1
With corrected metadata from user-provided byte sequence
"""

import struct
import sys
from pathlib import Path
from PIL import Image


def decompress_rle(data, offset, size):
    """Decompress RLE data"""
    result = bytearray()
    pos = offset
    end = offset + size

    while pos + 2 <= end and pos + 2 <= len(data):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break
        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    return bytes(result)


def extract_palette(data, room_offset):
    """Extract palette from Pair 11"""
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


def extract_sprite_data(data, room_offset):
    """Extract sprite data from Pair 8"""
    pair_offset = room_offset + (8 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size > 0:
        return decompress_rle(data, offset, size)
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_room13_fixed.py <alfred.1> [output_dir]")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "room13_anims_fixed"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred1_path, 'rb') as f:
        data = f.read()

    room_num = 13
    room_offset = room_num * 104

    # Extract sprite data and palette
    sprite_data = extract_sprite_data(data, room_offset)
    palette = extract_palette(data, room_offset)

    if not sprite_data or not palette:
        print("Error: Could not extract sprite data or palette")
        sys.exit(1)

    print(f"Sprite data size: {len(sprite_data)} bytes")
    print(f"Palette: OK\n")

    # Animation metadata from user-provided byte sequence
    # Metadata is at 44-byte intervals starting at 0x25314B
    # The sequence shows:
    # Offset 0: 61x88, 10 frames
    # Offset 44: 31x39, 1 frame
    # Offset 88: 79x58, 9 frames
    # Offset 132: 39x30, 10 frames

    animations = [
        {'name': 'anim0', 'width': 61, 'height': 88, 'frames': 10},  # Person walking
        {'name': 'anim1', 'width': 31, 'height': 39, 'frames': 1},   # Signpost
        {'name': 'anim2', 'width': 79, 'height': 58, 'frames': 9},   # Flies
        {'name': 'anim3', 'width': 39, 'height': 30, 'frames': 10},  # Birds
    ]

    offset = 0
    for anim in animations:
        name = anim['name']
        w = anim['width']
        h = anim['height']
        frames = anim['frames']

        needed = w * h * frames

        if offset + needed > len(sprite_data):
            print(f"{name}: Not enough data (need {needed}, have {len(sprite_data) - offset})")
            continue

        anim_data = sprite_data[offset:offset + needed]

        # Create horizontal strip image
        img = Image.new('P', (w * frames, h))
        img.putpalette(palette)

        for frame in range(frames):
            frame_offset = frame * w * h
            for y in range(h):
                for x in range(w):
                    pixel_idx = frame_offset + (y * w) + x
                    pixel_value = anim_data[pixel_idx]
                    img.putpixel((frame * w + x, y), pixel_value)

        output_file = output_path / f"{name}.png"
        img.save(output_file)

        print(f"{name}: {w}x{h}x{frames} frames -> {output_file.name}")
        offset += needed

    print(f"\nExtracted {len(animations)} animations to {output_path.absolute()}")
    print(f"Used {offset} of {len(sprite_data)} bytes ({offset/len(sprite_data)*100:.1f}%)")


if __name__ == "__main__":
    main()
