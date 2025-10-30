#!/usr/bin/env python3
"""
Extract all animations from all rooms in ALFRED.1
Uses the discovered pattern: metadata is 112 bytes after Pair 8 sprite data ends
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
        return decompress_rle(data, offset, size), offset + size
    return None, None


def get_animation_metadata(data, sprite_end_offset):
    """
    Get animation metadata starting 112 bytes after sprite data ends.
    Each animation metadata is 44 bytes apart, up to 4 animations per room.
    Format: [width, height, ..., frames at +6, ...]
    """
    animations = []
    metadata_start = sprite_end_offset + 112

    for anim_idx in range(4):
        anim_offset = metadata_start + (anim_idx * 44)

        if anim_offset + 12 > len(data):
            break

        w = data[anim_offset]
        h = data[anim_offset + 1]
        frames = data[anim_offset + 6]

        # Valid animation check
        if w > 0 and w < 200 and h > 0 and h < 200 and frames > 0 and frames < 50:
            animations.append({
                'width': w,
                'height': h,
                'frames': frames
            })

    return animations


def extract_room_animations(data, room_num, output_path):
    """Extract all animations from a specific room"""
    room_offset = room_num * 104

    # Extract sprite data and metadata location
    sprite_data, sprite_end = extract_sprite_data(data, room_offset)
    if not sprite_data or not sprite_end:
        return 0

    # Get palette
    palette = extract_palette(data, room_offset)
    if not palette:
        return 0

    # Get animation metadata
    animations = get_animation_metadata(data, sprite_end)
    if not animations:
        return 0

    # Create room directory
    room_dir = output_path / f"room{room_num:02d}"
    room_dir.mkdir(parents=True, exist_ok=True)

    # Extract each animation
    offset = 0
    extracted = 0

    for anim_idx, anim in enumerate(animations):
        w = anim['width']
        h = anim['height']
        frames = anim['frames']

        needed = w * h * frames

        if offset + needed > len(sprite_data):
            break

        anim_data = sprite_data[offset:offset + needed]

        # Create horizontal strip image
        img = Image.new('P', (w * frames, h))
        img.putpalette(palette)

        for frame in range(frames):
            frame_offset = frame * w * h
            for y in range(h):
                for x in range(w):
                    pixel_idx = frame_offset + (y * w) + x
                    if pixel_idx < len(anim_data):
                        pixel_value = anim_data[pixel_idx]
                        img.putpixel((frame * w + x, y), pixel_value)

        output_file = room_dir / f"anim{anim_idx}.png"
        img.save(output_file)

        offset += needed
        extracted += 1

    return extracted


def main():
    if len(sys.argv) < 2:
        print("Extract all animations from ALFRED.1")
        print("=" * 70)
        print()
        print("Usage: python extract_all_animations.py <alfred.1> [output_dir]")
        print()
        print("This will extract animations from all 56 rooms.")
        print()
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "animations_all"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("=" * 70)
    print("Extracting all animations from ALFRED.1")
    print("=" * 70)
    print()

    total_animations = 0
    rooms_with_animations = 0

    for room_num in range(56):
        extracted = extract_room_animations(data, room_num, output_path)

        if extracted > 0:
            print(f"Room {room_num:2d}: {extracted} animation(s) extracted")
            total_animations += extracted
            rooms_with_animations += 1

    print()
    print("=" * 70)
    print(f"Extraction complete!")
    print(f"  Rooms with animations: {rooms_with_animations}/56")
    print(f"  Total animations: {total_animations}")
    print(f"  Output directory: {output_path.absolute()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
