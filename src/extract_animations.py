#!/usr/bin/env python3
"""
Alfred Pelrock - Sprite/Animation Extractor
Extracts sprite animations from ALFRED.1 with user-defined dimensions

This tool requires external metadata (dimension/frame count information)
as the file format doesn't contain easily parseable headers for sprites.
"""

import struct
import sys
from pathlib import Path
from PIL import Image


def decompress_rle(data, offset, size):
    """
    Decompress RLE-compressed data.
    Format: [count byte][value byte] repeated
    Stops at 'BUDA' marker or end of size
    """
    result = bytearray()
    pos = offset
    end = offset + size

    while pos + 2 <= end and pos + 2 <= len(data):
        # Check for BUDA marker (end of block)
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break

        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    return bytes(result)


def extract_palette(data, room_offset):
    """
    Extract color palette from room structure (Pair 11).
    Returns palette suitable for PIL Image in format [r,g,b,r,g,b,...]
    """
    pair_offset = room_offset + (11 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size == 0x300:  # 768 bytes
        palette_data = data[offset:offset+768]

        # Convert VGA 6-bit palette (0-63) to 8-bit (0-255)
        palette = []
        for i in range(256):
            r = palette_data[i * 3] * 4
            g = palette_data[i * 3 + 1] * 4
            b = palette_data[i * 3 + 2] * 4
            palette.extend([r, g, b])

        return palette

    return None


def extract_sprite_data(data, room_offset):
    """
    Extract and decompress sprite data from Pair 8 of room structure.
    """
    pair_offset = room_offset + (8 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size > 0:
        return decompress_rle(data, offset, size)

    return None


def extract_animations(alfred1_path, room_num, animations, output_dir):
    """
    Extract animations from a specific room.

    Args:
        alfred1_path: Path to ALFRED.1 file
        room_num: Room number (0-55)
        animations: List of (name, width, height, frames) tuples
        output_dir: Output directory path
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred1_path, 'rb') as f:
        data = f.read()

    # Calculate room offset (104 bytes per room header)
    ROOM_STRUCT_SIZE = 104
    room_offset = room_num * ROOM_STRUCT_SIZE

    # Extract sprite data and palette
    sprite_data = extract_sprite_data(data, room_offset)
    palette = extract_palette(data, room_offset)

    if not sprite_data or not palette:
        print(f"Error: Could not extract sprite data or palette for room {room_num}")
        return False

    print(f"Room {room_num}:")
    print(f"  Decompressed sprite data: {len(sprite_data)} bytes")
    print(f"  Palette: {'OK' if palette else 'MISSING'}")
    print()

    # Extract each animation sequentially
    offset = 0
    success_count = 0

    for anim_name, w, h, frames in animations:
        needed = w * h * frames

        if offset + needed > len(sprite_data):
            available = len(sprite_data) - offset
            frames_available = available // (w * h)

            if frames_available > 0:
                print(f"  ⚠ {anim_name}: Only {frames_available}/{frames} frames available")
                needed = frames_available * w * h
                frames = frames_available
            else:
                print(f"  ✗ {anim_name}: Not enough data ({available} bytes available, need {needed})")
                continue

        # Extract sprite data for this animation
        anim_data = sprite_data[offset:offset + needed]

        # Create image as horizontal strip
        img = Image.new('P', (w * frames, h))
        img.putpalette(palette)

        # Fill image frame by frame
        for frame in range(frames):
            frame_offset = frame * w * h
            for y in range(h):
                for x in range(w):
                    pixel_idx = frame_offset + (y * w) + x
                    pixel_value = anim_data[pixel_idx]
                    img.putpixel((frame * w + x, y), pixel_value)

        # Save image
        output_file = output_path / f"room{room_num:02d}_{anim_name}.png"
        img.save(output_file)

        print(f"  ✓ {anim_name}: {w}x{h}x{frames} frames ({needed} bytes)")
        print(f"     Saved: {output_file.name}")

        offset += needed
        success_count += 1

    print(f"\n  Total extracted: {offset}/{len(sprite_data)} bytes")
    print(f"  Remaining: {len(sprite_data) - offset} bytes")
    print(f"  Animations extracted: {success_count}/{len(animations)}")
    print()

    return success_count == len(animations)


def main():
    # Example usage for Room 13 (based on pantalla13.txt and reference images)
    if len(sys.argv) < 2:
        print("Alfred Pelrock - Sprite Extractor")
        print("=" * 70)
        print()
        print("Usage: python extract_sprites.py <alfred.1> [output_dir]")
        print()
        print("Example:")
        print("  python extract_sprites.py alfred.1 sprites/")
        print()
        print("This extracts Room 13 animations by default.")
        print("Edit the script to extract other rooms with their specific dimensions.")
        print()
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "sprites_extracted"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    print("=" * 70)
    print("Alfred Pelrock - Sprite Extractor")
    print("=" * 70)
    print()

    # Room 13 animations (from pantalla13.txt and manual analysis)
    # Format: (name, width, height, frame_count)
    room13_animations = [
        ('anim130_walking', 61, 88, 10),   # Character walking animation
        ('anim131_torch', 39, 30, 10),     # Torch/flame animation
        ('anim132_sign', 31, 70, 1),       # Static sign
        ('anim133_birds', 79, 58, 9),      # Flying birds (note: file contains 8)
    ]

    success = extract_animations(alfred1_path, 13, room13_animations, output_dir)

    print("=" * 70)
    if success:
        print("✓ Extraction completed successfully!")
    else:
        print("~ Extraction completed with warnings (see above)")
    print(f"Output directory: {Path(output_dir).absolute()}")
    print("=" * 70)
    print()
    print("To extract other rooms, you need to provide dimension information.")
    print("Dimension information can be found in:")
    print("  - pantalla*.txt files (if available)")
    print("  - Game resource editors")
    print("  - Manual analysis of decompressed sprite data")


if __name__ == "__main__":
    main()
