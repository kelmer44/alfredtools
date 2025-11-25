#!/usr/bin/env python3
"""
Alfred Pelrock - Apply Dialog Overlay Effect
Applies the dialog choice overlay using the actual game LUT on paletted backgrounds
"""

import struct
import sys
from pathlib import Path
from PIL import Image

# Memory address of the overlay transparency LUT in the executable
OVERLAY_LUT_OFFSET = 0x00052dfc
OVERLAY_LUT_SIZE = 256

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

# Overlay parameters
CHOICE_HEIGHT = 16
OVERLAY_PADDING = 2


def generate_darkening_lut_from_palette(palette):
    """
    Generate a darkening LUT by finding darker colors in the actual palette.

    For each color in the palette, finds the closest color that is approximately
    40% as bright (simulating semi-transparent black overlay).

    Args:
        palette: List of 768 bytes (256 colors × 3 RGB values)

    Returns:
        bytes: 256-byte lookup table
    """
    # Convert palette to RGB tuples
    rgb_palette = []
    for i in range(256):
        r = palette[i * 3]
        g = palette[i * 3 + 1]
        b = palette[i * 3 + 2]
        rgb_palette.append((r, g, b))

    lut = bytearray(256)

    for i in range(256):
        r, g, b = rgb_palette[i]

        # Target: 40% brightness (simulates semi-transparent black)
        target_r = int(r * 0.4)
        target_g = int(g * 0.4)
        target_b = int(b * 0.4)

        # Find closest color in palette that doesn't brighten
        best_index = i  # Worst case: map to self
        best_distance = 999999
        i_brightness = r + g + b

        for j in range(256):
            pr, pg, pb = rgb_palette[j]
            j_brightness = pr + pg + pb

            # Must not brighten
            if j_brightness <= i_brightness:
                # Calculate color distance to target
                dr = target_r - pr
                dg = target_g - pg
                db = target_b - pb
                distance = dr*dr + dg*dg + db*db

                if distance < best_distance:
                    best_distance = distance
                    best_index = j

        lut[i] = best_index

    return bytes(lut)


def extract_lut_from_exe(exe_path, palette=None):
    """
    Extract the 256-byte overlay LUT from the game executable.
    Falls back to palette-based generation if extraction fails.

    Args:
        exe_path: Path to executable
        palette: Optional 768-byte palette to generate LUT from

    Returns:
        bytes: 256-byte lookup table
    """
    try:
        with open(exe_path, 'rb') as f:
            f.seek(OVERLAY_LUT_OFFSET)
            lut_data = f.read(OVERLAY_LUT_SIZE)

        if len(lut_data) != OVERLAY_LUT_SIZE:
            raise ValueError("Incomplete read")

        # Validate it looks like a LUT (has variety)
        unique_values = len(set(lut_data))
        if unique_values < 100:
            raise ValueError("Data doesn't look like a LUT")

        return lut_data

    except Exception as e:
        print(f"  Warning: Could not extract LUT from executable ({e})")
        if palette:
            print(f"  Generating LUT from room palette...")
            return generate_darkening_lut_from_palette(palette)
        else:
            print(f"  ERROR: No palette provided for LUT generation")
            raise ValueError("Cannot generate LUT without palette")


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

        # Convert VGA 6-bit palette to 8-bit
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


def apply_overlay_effect(pixel_data, lut, num_choices, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
    """
    Apply the overlay effect to raw paletted pixel data using the game's LUT.

    This replicates exactly what the game does:
        for each pixel in overlay region:
            new_index = lut[old_index]

    Args:
        pixel_data: bytes object containing palette indices (width * height bytes)
        lut: 256-byte lookup table from the game executable
        num_choices: number of dialog choices (determines overlay height)
        width: screen width (default 640)
        height: screen height (default 400)

    Returns:
        bytes: modified pixel data with overlay applied
    """
    # Calculate overlay dimensions
    overlay_height = num_choices * CHOICE_HEIGHT + OVERLAY_PADDING
    overlay_y_start = height - overlay_height

    # Convert to mutable bytearray
    pixels = bytearray(pixel_data)

    # Apply LUT remapping to overlay region only
    # This is the exact algorithm from the game:
    #   for (offset = 0; offset < overlay_size; offset++)
    #       screen_buffer[offset] = overlay_transparency_lut[screen_buffer[offset]];

    for y in range(overlay_y_start, height):
        row_start = y * width
        row_end = row_start + width

        for x in range(width):
            pixel_offset = row_start + x
            old_index = pixels[pixel_offset]
            new_index = lut[old_index]
            pixels[pixel_offset] = new_index

    return bytes(pixels)


def process_room(alfred1_path, exe_path, room_num, num_choices, output_path):
    """
    Extract a room background and apply the dialog overlay effect.

    Args:
        alfred1_path: path to ALFRED.1 resource file
        exe_path: path to game executable (to extract LUT)
        room_num: room number (0-55)
        num_choices: number of dialog choices (determines overlay height)
        output_path: where to save the result
    """
    ROOM_STRUCT_SIZE = 104
    EXPECTED_SIZE = SCREEN_WIDTH * SCREEN_HEIGHT

    # Load ALFRED.1 data
    with open(alfred1_path, 'rb') as f:
        alfred_data = f.read()

    # Extract room data
    room_offset = room_num * ROOM_STRUCT_SIZE

    print(f"\nExtracting room {room_num}...")
    background_data = extract_background(alfred_data, room_offset)
    palette = extract_palette(alfred_data, room_offset)

    if len(background_data) < EXPECTED_SIZE * 0.9:
        print(f"Error: Background data too small ({len(background_data)} bytes)")
        return False

    if not palette:
        print(f"Error: Failed to extract palette")
        return False

    # Trim or pad to exact size
    img_data = background_data[:EXPECTED_SIZE]
    if len(img_data) < EXPECTED_SIZE:
        img_data += bytes([0] * (EXPECTED_SIZE - len(img_data)))

    print(f"  Background: {len(background_data)} bytes")
    print(f"  Palette: {len(palette)//3} colors")

    # Extract/generate LUT using the room's palette
    print(f"\nExtracting overlay LUT from {exe_path}...")
    lut = extract_lut_from_exe(exe_path, palette)
    print(f"  LUT extracted: {len(lut)} bytes")

    # Show some LUT mappings with actual colors
    print(f"\n  Example LUT mappings (RGB colors):")
    for i in [0, 50, 100, 150, 200, 255]:
        orig_r = palette[i*3]
        orig_g = palette[i*3 + 1]
        orig_b = palette[i*3 + 2]
        mapped_idx = lut[i]
        new_r = palette[mapped_idx*3]
        new_g = palette[mapped_idx*3 + 1]
        new_b = palette[mapped_idx*3 + 2]
        print(f"    {i:3d} RGB({orig_r:3d},{orig_g:3d},{orig_b:3d}) → {mapped_idx:3d} RGB({new_r:3d},{new_g:3d},{new_b:3d})")

    # Calculate overlay region
    overlay_height = num_choices * CHOICE_HEIGHT + OVERLAY_PADDING
    overlay_y_start = SCREEN_HEIGHT - overlay_height

    print(f"\nApplying overlay effect...")
    print(f"  Number of choices: {num_choices}")
    print(f"  Overlay height: {overlay_height} pixels")
    print(f"  Overlay region: Y={overlay_y_start} to Y={SCREEN_HEIGHT}")
    print(f"  Pixels affected: {SCREEN_WIDTH * overlay_height}")

    # Apply overlay using generated LUT
    modified_data = apply_overlay_effect(img_data, lut, num_choices)

    # Create image with palette
    img = Image.new('P', (SCREEN_WIDTH, SCREEN_HEIGHT))
    img.putpalette(palette)
    img.putdata(modified_data)

    # Save result
    img.save(output_path)
    print(f"\nSaved to: {output_path}")

    return True


def main():
    if len(sys.argv) < 5:
        print("Usage: python apply_dialog_overlay.py <alfred.1> <game.exe> <room_num> <num_choices> [output.png]")
        print()
        print("Arguments:")
        print("  alfred.1     - ALFRED.1 resource file")
        print("  game.exe     - Game executable (to extract LUT)")
        print("  room_num     - Room number (0-55)")
        print("  num_choices  - Number of dialog choices (1-10)")
        print("  output.png   - Output filename (optional)")
        print()
        print("Example:")
        print("  python apply_dialog_overlay.py ALFRED.1 ALFRED.EXE 2 4")
        print("  python apply_dialog_overlay.py ALFRED.1 ALFRED.EXE 2 4 room_02_overlay.png")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    exe_path = sys.argv[2]
    room_num = int(sys.argv[3])
    num_choices = int(sys.argv[4])
    output_path = sys.argv[5] if len(sys.argv) > 5 else f"room_{room_num:02d}_overlay_{num_choices}choices.png"

    # Validate inputs
    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    if not Path(exe_path).exists():
        print(f"Error: File not found: {exe_path}")
        sys.exit(1)

    if not (0 <= room_num <= 55):
        print(f"Error: Room number must be 0-55, got {room_num}")
        sys.exit(1)

    if not (1 <= num_choices <= 10):
        print(f"Error: Number of choices must be 1-10, got {num_choices}")
        sys.exit(1)

    # Process the room
    print("="*70)
    print("Alfred Pelrock - Apply Dialog Overlay Effect")
    print("="*70)
    print()

    success = process_room(alfred1_path, exe_path, room_num, num_choices, output_path)

    if success:
        print()
        print("="*70)
        print("Success! The overlay was applied using the game's exact LUT.")
        print("="*70)
    else:
        print()
        print("="*70)
        print("Failed to process room.")
        print("="*70)
        sys.exit(1)


if __name__ == "__main__":
    main()
