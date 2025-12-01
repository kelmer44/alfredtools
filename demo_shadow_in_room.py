#!/usr/bin/env python3
"""
Shadow Demonstration Script

For a given room, this script:
1. Extracts the background
2. Extracts the character sprite from ALFRED.3
3. Places the character at multiple positions in the room
4. Applies shadow/shading based on shadow map
5. Exports composite images as PNG

Usage:
    python demo_shadow_in_room.py <room_number> [output_dir]

Example:
    python demo_shadow_in_room.py 5 shadow_demo/
"""

import sys
import struct
from pathlib import Path
from PIL import Image
import numpy as np


# File paths
ALFRED1_PATH = "files/ALFRED.1"
ALFRED3_PATH = "files/ALFRED.3"
ALFRED5_PATH = "files/ALFRED.5"
ALFRED9_PATH = "files/ALFRED.9"

# Character palette offsets in ALFRED.9
CHAR_PALETTE_OFFSET = 0x7b00  # 768 bytes - character's base palette
CHAR_SHADOW_REMAP_OFFSET = 0x7e00  # 256 bytes - shadow remap table

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
ROOM_STRUCT_SIZE = 104


def decompress_rle_block(data, offset, size):
    """Decompress a single RLE block"""
    # Check if it's uncompressed (specific size markers)
    if size == 0x8000 or size == 0x6800:
        return data[offset:offset + size]

    # RLE decompression
    result = bytearray()
    pos = offset
    end = offset + size

    while pos + 2 <= min(end, len(data)):
        # Check for BUDA terminator
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break

        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    return bytes(result)


def extract_palette(data, room_offset):
    """Extract VGA palette from room structure (pair 11)"""
    pair_offset = room_offset + (11 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size == 0x300:
        palette_data = data[offset:offset+768]

        # Convert VGA 6-bit palette to 8-bit (multiply by 4)
        palette = []
        for i in range(256):
            r = palette_data[i * 3] * 4
            g = palette_data[i * 3 + 1] * 4
            b = palette_data[i * 3 + 2] * 4
            palette.extend([r, g, b])

        return palette

    return None


def extract_background(data, room_offset):
    """Extract 640×400 background by combining 8 blocks"""
    pairs = []

    # Read pairs 0-7 (background blocks)
    for pair_idx in range(8):
        pair_offset = room_offset + (pair_idx * 8)
        offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
        size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

        if offset > 0 and size > 0 and offset < len(data):
            pairs.append((offset, size))

    # Decompress and combine all blocks
    combined = bytearray()
    for offset, size in pairs:
        block_data = decompress_rle_block(data, offset, size)
        combined.extend(block_data)

    return bytes(combined)


def extract_shadow_map(alfred5_data, room_number):
    """Extract shadow map for a specific room from ALFRED.5"""
    # Read directory entry (6 bytes per room)
    entry_offset = room_number * 6

    # Extract 24-bit little-endian offset
    shadow_offset = (alfred5_data[entry_offset] |
                    (alfred5_data[entry_offset + 1] << 8) |
                    (alfred5_data[entry_offset + 2] << 16))

    # Decompress RLE data
    pixels = bytearray()
    offset = shadow_offset

    while offset < len(alfred5_data) - 1:
        # Check for BUDA terminator
        if alfred5_data[offset:offset+4] == b'BUDA':
            break

        # Read RLE pair: [count, color]
        count = alfred5_data[offset]
        color = alfred5_data[offset + 1]
        pixels.extend([color] * count)
        offset += 2

        # Safety check
        if len(pixels) >= SCREEN_WIDTH * SCREEN_HEIGHT:
            break

    # Ensure correct size
    expected_size = SCREEN_WIDTH * SCREEN_HEIGHT
    if len(pixels) < expected_size:
        pixels.extend([0xFF] * (expected_size - len(pixels)))
    elif len(pixels) > expected_size:
        pixels = pixels[:expected_size]

    return pixels


def load_character_palette():
    """Load the character's base palette from ALFRED.9
    
    Returns 768 bytes (256 colors × 3 RGB bytes)
    """
    with open(ALFRED9_PATH, 'rb') as f:
        f.seek(CHAR_PALETTE_OFFSET)
        palette = f.read(768)
    
    return palette


def map_char_palette_to_room(char_palette, room_palette):
    """Create mapping from character palette indices to room palette indices
    
    For each character color, finds the closest matching color in the room palette
    """
    mapping = bytearray(256)
    
    for char_idx in range(256):
        char_r = char_palette[char_idx * 3]
        char_g = char_palette[char_idx * 3 + 1]
        char_b = char_palette[char_idx * 3 + 2]
        
        # Find closest color in room palette
        best_idx = 0
        best_dist = 999999
        
        for room_idx in range(256):
            room_r = room_palette[room_idx * 3]
            room_g = room_palette[room_idx * 3 + 1]
            room_b = room_palette[room_idx * 3 + 2]
            
            dist = (char_r - room_r)**2 + (char_g - room_g)**2 + (char_b - room_b)**2
            if dist < best_dist:
                best_dist = dist
                best_idx = room_idx
        
        mapping[char_idx] = best_idx
    
    return mapping


def load_character_shadow_remap(room_number):
    """Load the room-specific character shadow palette remap table from ALFRED.9
    
    Each room has its own 256-byte shadow remap table.
    Pattern: ALFRED.9 offset = 0x200 + (room_number * 1024)
    There is only ONE shadow level for the character.
    """
    remap_offset = 0x200 + (room_number * 1024)
    
    with open(ALFRED9_PATH, 'rb') as f:
        f.seek(remap_offset)
        remap_table = f.read(256)
    
    return remap_table


def extract_character_sprite():
    """Extract character sprite from ALFRED.3 (first sprite: 51×102)"""
    with open(ALFRED3_PATH, 'rb') as f:
        data = f.read()

    # Decompress RLE data
    sprite_data = bytearray()
    pos = 0

    while pos + 2 <= len(data):
        if data[pos:pos+4] == b'BUDA':
            break
        count = data[pos]
        value = data[pos + 1]
        sprite_data.extend([value] * count)
        pos += 2

    # Extract first sprite: 51×102 pixels
    width, height = 51, 102
    total_pixels = width * height

    sprite_pixels = bytes(sprite_data[0:total_pixels])

    return sprite_pixels, width, height


def apply_shadow_to_sprite(sprite_pixels, sprite_width, sprite_height,
                           char_x, char_y, shadow_map, palette_remap):
    """
    Apply shadow effect to character sprite based on position

    According to the game's algorithm:
    - Sample shadow at character's base position
    - If shadow value != 0xFF, remap all sprite colors
    """
    # Sample shadow at character's position (not foot, just the base Y)
    # The game checks before rendering at (char_y, char_x)
    shadow_y = char_y
    shadow_x = char_x

    # Check bounds
    if shadow_y >= SCREEN_HEIGHT or shadow_x >= SCREEN_WIDTH:
        return sprite_pixels  # Out of bounds, no shadow

    if shadow_x < 0 or shadow_y < 0:
        return sprite_pixels  # Out of bounds, no shadow

    # Look up shadow value
    shadow_index = (shadow_y * SCREEN_WIDTH) + shadow_x

    if shadow_index >= len(shadow_map):
        return sprite_pixels  # Safety check

    shadow_value = shadow_map[shadow_index]

    # Debug: Print shadow detection
    print(f"    Shadow check at ({shadow_x}, {shadow_y}): value=0x{shadow_value:02X}", end="")

    # Check if in shadow (0xFF means no shadow, anything else means shadowed)
    if shadow_value == 0xFF:
        print(" - NOT SHADOWED (0xFF)")
        return sprite_pixels
    
    print(f" - SHADOWED (value {shadow_value})")

    # Apply shadow by remapping colors using the fixed character remap table
    if not palette_remap:
        print("    WARNING: No palette remap table, returning unshadowed")
        return sprite_pixels

    # The character uses a simple 256-byte remap table (only one shadow level)
    # Just look up each pixel color directly
    shadowed_sprite = bytearray()

    for pixel in sprite_pixels:
        if pixel == 0xFF:  # Transparent
            shadowed_sprite.append(0xFF)
        else:
            # Look up remapped color
            if pixel >= len(palette_remap):
                shadowed_sprite.append(pixel)  # Safety fallback
            else:
                shadowed_color = palette_remap[pixel]
                shadowed_sprite.append(shadowed_color)

    return shadowed_sprite


def draw_sprite_on_background(bg_array, sprite_pixels, sprite_width, sprite_height,
                              x, y):
    """Draw sprite on background array at given position"""
    for sy in range(sprite_height):
        for sx in range(sprite_width):
            screen_x = x + sx
            screen_y = y + sy

            # Check bounds
            if screen_x < 0 or screen_x >= SCREEN_WIDTH:
                continue
            if screen_y < 0 or screen_y >= SCREEN_HEIGHT:
                continue

            # Get sprite pixel
            sprite_idx = sy * sprite_width + sx
            if sprite_idx >= len(sprite_pixels):
                continue

            pixel_value = sprite_pixels[sprite_idx]

            # Skip transparent pixels (0xFF)
            if pixel_value == 0xFF:
                continue

            # Draw to background
            bg_idx = screen_y * SCREEN_WIDTH + screen_x
            bg_array[bg_idx] = pixel_value


def create_shadow_demo(room_number, output_dir="shadow_demo"):
    """Create demonstration images for a room with character at multiple positions"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Creating shadow demonstration for Room {room_number}")
    print("=" * 70)

    # Load data files
    print("Loading ALFRED.1...")
    with open(ALFRED1_PATH, 'rb') as f:
        alfred1_data = f.read()

    print("Loading ALFRED.3...")
    sprite_pixels, sprite_width, sprite_height = extract_character_sprite()
    print(f"  Character sprite: {sprite_width}×{sprite_height} pixels")

    print("Loading ALFRED.5...")
    with open(ALFRED5_PATH, 'rb') as f:
        alfred5_data = f.read()

    # Extract room data
    room_offset = room_number * ROOM_STRUCT_SIZE

    print(f"\nExtracting Room {room_number} data...")
    background_data = extract_background(alfred1_data, room_offset)
    palette = extract_palette(alfred1_data, room_offset)
    shadow_map = extract_shadow_map(alfred5_data, room_number)
    
    # Load room-specific character shadow remap from ALFRED.9
    palette_remap = load_character_shadow_remap(room_number)

    if not palette:
        print("ERROR: Could not extract palette")
        return

    # Trim/pad background to correct size
    expected_size = SCREEN_WIDTH * SCREEN_HEIGHT
    if len(background_data) < expected_size:
        background_data += bytes([0] * (expected_size - len(background_data)))
    else:
        background_data = background_data[:expected_size]

    print(f"  Background: {len(background_data)} bytes")
    print(f"  Shadow map: {len(shadow_map)} bytes")

    # Analyze shadow coverage
    shadow_pixels = sum(1 for v in shadow_map if v != 0xFF)
    unique_values = set(shadow_map)
    print(f"  Shadow coverage: {shadow_pixels}/{len(shadow_map)} pixels ({shadow_pixels/len(shadow_map)*100:.1f}%)")
    print(f"  Unique shadow values: {sorted(unique_values)}")

    # Define test positions (grid across the room)
    test_positions = [
        (100, 100, "top_left"),
        (300, 100, "top_center"),
        (500, 100, "top_right"),
        (100, 200, "middle_left"),
        (300, 200, "center"),
        (500, 200, "middle_right"),
        (100, 280, "bottom_left"),
        (300, 280, "bottom_center"),
        (500, 280, "bottom_right"),
    ]

    print(f"\nGenerating {len(test_positions)} demonstration images...")
    print("-" * 70)

    for x, y, label in test_positions:
        # Check shadow at this position
        foot_y = y + sprite_height
        foot_x = x

        if foot_y < SCREEN_HEIGHT and foot_x < SCREEN_WIDTH:
            shadow_idx = foot_y * SCREEN_WIDTH + foot_x
            shadow_value = shadow_map[shadow_idx]
            is_shadowed = (shadow_value != 0xFF)
        else:
            shadow_value = 0xFF
            is_shadowed = False

        # Apply shadow to sprite
        if is_shadowed:
            sprite_to_draw = apply_shadow_to_sprite(
                sprite_pixels, sprite_width, sprite_height,
                x, y, shadow_map, palette_remap
            )
            status = f"⚫ SHADOWED (level {shadow_value})"
        else:
            sprite_to_draw = sprite_pixels
            status = "☀ LIT"

        # Create composite image
        composite = bytearray(background_data)
        draw_sprite_on_background(composite, sprite_to_draw, sprite_width, sprite_height, x, y)

        # Save as PNG
        img = Image.new('P', (SCREEN_WIDTH, SCREEN_HEIGHT))
        img.putpalette(palette)
        img.putdata(composite)

        output_file = output_path / f"room{room_number:02d}_{label}_x{x}_y{y}.png"
        img.save(output_file)

        print(f"  ✓ {label:15s} ({x:3d}, {y:3d}) {status:25s} → {output_file.name}")

    # Create a composite image with all positions
    print("\nCreating composite overview...")

    # Create grid: 3 columns × 3 rows
    grid_cols = 3
    grid_rows = 3
    composite_width = SCREEN_WIDTH * grid_cols
    composite_height = SCREEN_HEIGHT * grid_rows

    composite_img = Image.new('P', (composite_width, composite_height))
    composite_img.putpalette(palette)

    for idx, (x, y, label) in enumerate(test_positions):
        # Apply shadow
        foot_y = y + sprite_height
        foot_x = x

        if foot_y < SCREEN_HEIGHT and foot_x < SCREEN_WIDTH:
            shadow_idx = foot_y * SCREEN_WIDTH + foot_x
            shadow_value = shadow_map[shadow_idx]
            is_shadowed = (shadow_value != 0xFF)
        else:
            is_shadowed = False

        if is_shadowed:
            sprite_to_draw = apply_shadow_to_sprite(
                sprite_pixels, sprite_width, sprite_height,
                x, y, shadow_map, palette_remap
            )
        else:
            sprite_to_draw = sprite_pixels

        # Create scene
        scene = bytearray(background_data)
        draw_sprite_on_background(scene, sprite_to_draw, sprite_width, sprite_height, x, y)

        # Place in grid
        grid_x = idx % grid_cols
        grid_y = idx // grid_cols

        scene_img = Image.new('P', (SCREEN_WIDTH, SCREEN_HEIGHT))
        scene_img.putpalette(palette)
        scene_img.putdata(scene)

        composite_img.paste(scene_img, (grid_x * SCREEN_WIDTH, grid_y * SCREEN_HEIGHT))

    composite_file = output_path / f"room{room_number:02d}_composite_grid.png"
    composite_img.save(composite_file)
    print(f"  ✓ Grid composite saved: {composite_file.name}")

    print("\n" + "=" * 70)
    print("Shadow demonstration complete!")
    print(f"Output directory: {output_path.absolute()}")
    print("=" * 70)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable rooms: 0-54")
        sys.exit(1)

    room_number = int(sys.argv[1])
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "shadow_demo"

    if room_number < 0 or room_number > 54:
        print(f"Error: Room number must be between 0 and 54")
        sys.exit(1)

    # Check if required files exist
    for path_str in [ALFRED1_PATH, ALFRED3_PATH, ALFRED5_PATH]:
        if not Path(path_str).exists():
            print(f"Error: Required file not found: {path_str}")
            sys.exit(1)

    create_shadow_demo(room_number, output_dir)


if __name__ == '__main__':
    main()
