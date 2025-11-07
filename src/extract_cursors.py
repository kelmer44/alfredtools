#!/usr/bin/env python3
"""
Alfred Pelrock - Enhanced Cursor Extractor
Extracts all 5 cursor sprites from ALFRED.7 and attempts to apply proper palettes

Based on Ghidra reverse engineering analysis:
- Cursors are loaded in load_fonts_and_graphics() at hardcoded offsets
- Each cursor is 16x18 pixels (288 bytes)
- Palette index 255 (0xFF) is transparent
- A graphic/palette is loaded at 0xFE945 (just after cursors)
"""

import sys
from pathlib import Path
from PIL import Image

# Cursor data locations (hardcoded in game executable)
CURSORS = [
    {
        'offset': 0x0FDCDD,
        'decimal': 1039581,
        'name': 'cursor1_hotspot_hover',
        'var': 'cursor_hotspot_ptr',
        'desc': 'Interactive hotspot/object cursor',
        'usage': 'Shown when hovering over interactive objects, animations, or hotspots'
    },
    {
        'offset': 0x0FDDFD,
        'decimal': 1039869,
        'name': 'cursor2_default',
        'var': 'cursor_default_ptr',
        'desc': 'Default pointer cursor',
        'usage': 'Menu, inventory, verb panel, or when not over anything interactive'
    },
    {
        'offset': 0x0FDF1D,
        'decimal': 1040157,
        'name': 'cursor3_exit_hover',
        'var': 'cursor_exit_ptr',
        'desc': 'Exit/doorway hover cursor',
        'usage': 'Shown when hovering over room exits only'
    },
    {
        'offset': 0x0FE33D,
        'decimal': 1041213,
        'name': 'cursor4_animation_hover',
        'var': 'cursor_animation_ptr',
        'desc': 'Animation with flag cursor',
        'usage': 'Shown when hovering over animations with special flag set'
    },
    {
        'offset': 0x367EF0,
        'decimal': 3571440,
        'name': 'cursor5_combination',
        'var': 'cursor_combination_ptr',
        'desc': 'Exit + hotspot combination cursor',
        'usage': 'Shown when hovering over exit AND hotspot at same location'
    },
]

# Palette/graphic loaded just after cursors (might be cursor palette)
POTENTIAL_PALETTE_OFFSET = 0xFE945
POTENTIAL_PALETTE_SIZE = 0x129E

CURSOR_WIDTH = 16
CURSOR_HEIGHT = 18
CURSOR_SIZE = 288  # 16 * 18

def decompress_rle(data, offset, size):
    """Decompress RLE data"""
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

def find_budas(data):
    """Find all BUDA markers in the file"""
    budas = []
    pos = 0
    while pos < len(data) - 4:
        if data[pos:pos+4] == b'BUDA':
            budas.append(pos)
        pos += 1
    return budas

def is_valid_palette(data, offset):
    """Check if data at offset looks like a VGA palette"""
    if offset + 768 > len(data):
        return False
    pal_data = data[offset:offset+768]
    # VGA palettes use 6-bit values (0-63)
    return all(b <= 63 for b in pal_data) and len(set(pal_data)) > 10

def extract_palette(data, offset):
    """Extract VGA palette and convert to 8-bit RGB"""
    pal_data = data[offset:offset+768]
    palette = []
    for i in range(256):
        r = min(255, pal_data[i * 3] * 4)
        g = min(255, pal_data[i * 3 + 1] * 4)
        b = min(255, pal_data[i * 3 + 2] * 4)
        palette.extend([r, g, b])
    return palette

def create_grayscale_palette():
    """Create a simple grayscale palette"""
    palette = []
    for i in range(256):
        palette.extend([i, i, i])
    return palette

def extract_cursor(data, offset):
    """Extract raw cursor data"""
    if offset + CURSOR_SIZE > len(data):
        return None
    return data[offset:offset + CURSOR_SIZE]

def find_nearest_palette(data, budas, cursor_offset):
    """Find the nearest palette BUDA before cursor offset"""
    best_palette = None
    best_distance = float('inf')

    for buda_offset in budas:
        if buda_offset < cursor_offset and is_valid_palette(data, buda_offset + 4):
            distance = cursor_offset - buda_offset
            if distance < best_distance:
                best_distance = distance
                best_palette = extract_palette(data, buda_offset + 4)

    return best_palette

def main():
    if len(sys.argv) < 2:
        print("Alfred Pelrock - Enhanced Cursor Extractor")
        print("=" * 70)
        print()
        print("Usage: python extract_cursors_enhanced.py <ALFRED.7> [output_dir]")
        print()
        print("Extracts all 5 cursor sprites with proper palettes if found")
        print()
        print("Cursor Information:")
        for cursor in CURSORS:
            print(f"\n  {cursor['name']}")
            print(f"    Offset: 0x{cursor['offset']:06X} ({cursor['decimal']:,})")
            print(f"    Variable: {cursor['var']}")
            print(f"    Usage: {cursor['usage']}")
        print()
        sys.exit(1)

    alfred7_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "cursors_enhanced"

    if not Path(alfred7_path).exists():
        print(f"Error: File not found: {alfred7_path}")
        sys.exit(1)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Read ALFRED.7
    with open(alfred7_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - Enhanced Cursor Extractor")
    print("=" * 70)
    print(f"File: {alfred7_path}")
    print(f"Size: {len(data):,} bytes ({len(data) / 1024 / 1024:.2f} MB)")
    print()

    # Find all BUDA markers and palettes
    print("Scanning for BUDA markers and palettes...")
    budas = find_budas(data)
    print(f"Found {len(budas)} BUDA markers")

    palette_count = 0
    for buda in budas:
        if is_valid_palette(data, buda + 4):
            palette_count += 1
    print(f"Found {palette_count} palette BUDAs")
    print()

    # Check if cursor palette exists at known offset
    cursor_palette = None
    if is_valid_palette(data, POTENTIAL_PALETTE_OFFSET):
        cursor_palette = extract_palette(data, POTENTIAL_PALETTE_OFFSET)
        print(f"✓ Found palette at 0x{POTENTIAL_PALETTE_OFFSET:06X} (potential cursor palette)")
    else:
        print(f"✗ No valid palette at 0x{POTENTIAL_PALETTE_OFFSET:06X}")
        print("  Will attempt to find nearest palette for each cursor")
    print()

    grayscale_palette = create_grayscale_palette()
    success_count = 0

    print("=" * 70)
    print("Extracting Cursors:")
    print("=" * 70)

    for cursor in CURSORS:
        print(f"\n{cursor['name']}:")
        print(f"  Offset: 0x{cursor['offset']:06X} ({cursor['decimal']:,})")
        print(f"  Description: {cursor['desc']}")
        print(f"  Usage: {cursor['usage']}")

        cursor_data = extract_cursor(data, cursor['offset'])

        if not cursor_data:
            print(f"  ✗ Failed (offset out of bounds)")
            continue

        # Try to find the best palette for this cursor
        palette_to_use = cursor_palette
        palette_source = "cursor palette"

        if palette_to_use is None:
            palette_to_use = find_nearest_palette(data, budas, cursor['offset'])
            if palette_to_use:
                palette_source = "nearest BUDA palette"
            else:
                palette_to_use = grayscale_palette
                palette_source = "grayscale fallback"

        print(f"  Using palette: {palette_source}")

        # Save with indexed palette
        img_indexed = Image.new('P', (CURSOR_WIDTH, CURSOR_HEIGHT))
        img_indexed.putpalette(palette_to_use)
        img_indexed.putdata(cursor_data)

        output_file = output_path / f"{cursor['name']}.png"
        img_indexed.save(output_file)

        # Save RGBA version with transparency
        img_rgba = Image.new('RGBA', (CURSOR_WIDTH, CURSOR_HEIGHT))
        for y in range(CURSOR_HEIGHT):
            for x in range(CURSOR_WIDTH):
                pixel_idx = cursor_data[y * CURSOR_WIDTH + x]
                if pixel_idx == 255:  # Transparent
                    img_rgba.putpixel((x, y), (0, 0, 0, 0))
                else:
                    r = palette_to_use[pixel_idx * 3]
                    g = palette_to_use[pixel_idx * 3 + 1]
                    b = palette_to_use[pixel_idx * 3 + 2]
                    img_rgba.putpixel((x, y), (r, g, b, 255))

        output_file_rgba = output_path / f"{cursor['name']}_transparent.png"
        img_rgba.save(output_file_rgba)

        # Save 4x upscaled version for easier viewing
        img_large = img_rgba.resize((CURSOR_WIDTH * 4, CURSOR_HEIGHT * 4), Image.NEAREST)
        output_file_large = output_path / f"{cursor['name']}_4x.png"
        img_large.save(output_file_large)

        print(f"  ✓ {output_file.name}")
        print(f"  ✓ {output_file_rgba.name}")
        print(f"  ✓ {output_file_large.name} (4x scale)")
        success_count += 1

    print()
    print("=" * 70)
    print(f"Extraction Complete!")
    print(f"  Successfully extracted: {success_count}/{len(CURSORS)} cursors")
    print(f"  Output directory: {output_path.absolute()}")
    print()
    print("Files created per cursor:")
    print("  - .png : Indexed palette version")
    print("  - _transparent.png : RGBA with transparency")
    print("  - _4x.png : 4x upscaled for easier viewing")
    print("=" * 70)

if __name__ == "__main__":
    main()
