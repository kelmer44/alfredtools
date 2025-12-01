#!/usr/bin/env python3
"""
Test Dialog Overlay Palette Remapping
Applies both shadow and overlay remaps to room 2 with dialog choices
"""

import struct
from PIL import Image, ImageDraw

# Constants
ALFRED1_PATH = "files/ALFRED.1"
ALFRED9_PATH = "files/ALFRED.9"
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400
CHOICE_HEIGHT = 16

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

def load_shadow_remap(room_number):
    """Load shadow remap table from ALFRED.9"""
    with open(ALFRED9_PATH, 'rb') as f:
        remap_offset = 0x200 + (room_number * 1024)
        f.seek(remap_offset)
        return f.read(256)

def load_overlay_remap(room_number):
    """Load overlay remap table from ALFRED.9 (second 256 bytes)"""
    with open(ALFRED9_PATH, 'rb') as f:
        remap_offset = 0x200 + (room_number * 1024) + 256
        f.seek(remap_offset)
        return f.read(256)

def apply_remap_to_region(img_data, remap_table, y_start, y_end):
    """Apply palette remap to a region of the image"""
    pixels = bytearray(img_data)
    expected_size = SCREEN_WIDTH * SCREEN_HEIGHT
    
    # Ensure we have enough data
    if len(pixels) < expected_size:
        pixels.extend([0] * (expected_size - len(pixels)))
    
    for y in range(y_start, min(y_end, SCREEN_HEIGHT)):
        row_start = y * SCREEN_WIDTH
        
        for x in range(SCREEN_WIDTH):
            pixel_offset = row_start + x
            if pixel_offset < len(pixels):
                old_index = pixels[pixel_offset]
                new_index = remap_table[old_index]
                pixels[pixel_offset] = new_index
    
    return bytes(pixels[:expected_size])

def create_dialog_overlay_test(room_number, num_choices, output_path):
    """Create test image with dialog overlay"""
    print(f"Creating dialog overlay test for room {room_number} with {num_choices} choices...")
    
    # Load data
    with open(ALFRED1_PATH, 'rb') as f:
        alfred1_data = f.read()
    
    # Room structure is 13 pairs of 8 bytes (offset + size)
    room_offset = room_number * (13 * 8)
    
    # Extract background and palette
    print("  Extracting background...")
    bg_data = extract_background(alfred1_data, room_offset)
    palette = extract_palette(alfred1_data, room_offset)
    
    # Load remap tables
    print("  Loading remap tables from ALFRED.9...")
    shadow_remap = load_shadow_remap(room_number)
    overlay_remap = load_overlay_remap(room_number)
    
    # Calculate dialog overlay region
    overlay_height = num_choices * CHOICE_HEIGHT + 2  # +2 for padding
    overlay_y_start = SCREEN_HEIGHT - overlay_height
    
    print(f"  Overlay region: Y={overlay_y_start} to Y={SCREEN_HEIGHT} ({overlay_height} pixels)")
    
    # Apply overlay remap to dialog region
    print("  Applying overlay remap to dialog region...")
    modified_data = apply_remap_to_region(bg_data, overlay_remap, overlay_y_start, SCREEN_HEIGHT)
    
    # Create image
    img = Image.new('P', (SCREEN_WIDTH, SCREEN_HEIGHT))
    img.putpalette(palette)
    img.putdata(modified_data)
    
    # Draw text to show where choices would be
    img_rgb = img.convert('RGBA')
    draw = ImageDraw.Draw(img_rgb)
    
    for i in range(num_choices):
        y = overlay_y_start + (i * CHOICE_HEIGHT) + 4
        draw.text((20, y), f"Choice {i+1} text would appear here", fill=(255, 255, 255, 255))
    
    # Save
    img_rgb.save(output_path)
    print(f"  Saved to: {output_path}")
    
    # Also create a comparison with shadow remap
    shadow_output = output_path.replace('.png', '_shadow.png')
    print(f"\n  Creating comparison with shadow remap...")
    shadow_data = apply_remap_to_region(bg_data, shadow_remap, overlay_y_start, SCREEN_HEIGHT)
    
    img_shadow = Image.new('P', (SCREEN_WIDTH, SCREEN_HEIGHT))
    img_shadow.putpalette(palette)
    img_shadow.putdata(shadow_data)
    
    img_shadow_rgb = img_shadow.convert('RGBA')
    draw_shadow = ImageDraw.Draw(img_shadow_rgb)
    
    for i in range(num_choices):
        y = overlay_y_start + (i * CHOICE_HEIGHT) + 4
        draw_shadow.text((20, y), f"Choice {i+1} text would appear here", fill=(255, 255, 255, 255))
    
    img_shadow_rgb.save(shadow_output)
    print(f"  Saved shadow version to: {shadow_output}")
    
    # Stats
    print(f"\n  Remap table comparison:")
    diff_count = sum(1 for i in range(256) if shadow_remap[i] != overlay_remap[i])
    print(f"    Differences: {diff_count}/256 entries")
    print(f"    Shadow remap sample [0-15]: {' '.join(f'{b:02x}' for b in shadow_remap[:16])}")
    print(f"    Overlay remap sample[0-15]: {' '.join(f'{b:02x}' for b in overlay_remap[:16])}")

if __name__ == '__main__':
    # Test room 2 with 2 choices
    create_dialog_overlay_test(room_number=2, num_choices=2, output_path="room2_dialog_overlay.png")
    print("\n✓ Done! Check room2_dialog_overlay.png and room2_dialog_overlay_shadow.png")
