#!/usr/bin/env python3
"""
Extract and render the Alfred Pelrock fonts
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw

def extract_small_font(alfred9_path):
    """Extract 8x8 bitmap font from ALFRED.9 at 0x8f32"""
    with open(alfred9_path, 'rb') as f:
        f.seek(0x8f32)
        font_data = f.read(0x800)  # 256 characters * 8 bytes

    if len(font_data) != 0x800:
        raise ValueError(f"Expected 2048 bytes, got {len(font_data)}")

    return font_data

def extract_large_font(alfred9_path):
    """Extract 12x24 bitmap font from ALFRED.9 at 0x7dc8

    Format: 96 characters (ASCII 32-127), 48 bytes each (0x30)
    Each char is 12 pixels wide x 24 pixels tall
    Stored as 24 rows of 2 bytes (12 bits used per row)
    """
    with open(alfred9_path, 'rb') as f:
        f.seek(0x7dc8)
        font_data = f.read(0x12c0)  # 96 chars * 48 bytes

    if len(font_data) != 0x12c0:
        raise ValueError(f"Expected 4800 bytes, got {len(font_data)}")

    return font_data

def render_small_char(font_data, char_code, fg_color=(255, 255, 255), bg_color=(0, 0, 0)):
    """Render a single character from small 8x8 font"""
    offset = char_code * 8
    img = Image.new('RGB', (8, 8), bg_color)
    pixels = img.load()

    for y in range(8):
        byte = font_data[offset + y]
        for x in range(8):
            if byte & (1 << (7 - x)):
                pixels[x, y] = fg_color

    return img

def render_large_char(font_data, char_code, fg_color=(255, 255, 255), bg_color=(0, 0, 0)):
    """Render a single character from large 12x24 font"""
    if char_code < 32 or char_code > 127:
        # Return blank for unsupported characters
        return Image.new('RGB', (12, 24), bg_color)

    offset = (char_code - 32) * 0x30  # 48 bytes per char, starting at ASCII 32
    img = Image.new('RGB', (12, 24), bg_color)
    pixels = img.load()

    for y in range(24):
        byte_offset = offset + (y * 2)
        # Read 2 bytes (16 bits), use upper 12 bits
        byte1 = font_data[byte_offset]
        byte2 = font_data[byte_offset + 1]
        row_data = (byte1 << 8) | byte2

        for x in range(12):
            if row_data & (1 << (15 - x)):
                pixels[x, y] = fg_color

    return img

def render_text(font_data, text, scale=4, fg_color=(255, 255, 255), bg_color=(0, 0, 0), font_type='large'):
    """Render text string using the font"""
    if font_type == 'large':
        char_width = 12
        char_height = 24
        render_func = render_large_char
    else:
        char_width = 8
        char_height = 8
        render_func = render_small_char

    spacing = 1

    # Calculate dimensions
    width = len(text) * (char_width + spacing) * scale
    height = char_height * scale

    # Create image
    img = Image.new('RGB', (width, height), bg_color)

    # Render each character
    x_pos = 0
    for char in text:
        char_code = ord(char)
        if 0 <= char_code < 256:
            char_img = render_func(font_data, char_code, fg_color, bg_color)
            # Scale up
            char_img = char_img.resize((char_width * scale, char_height * scale), Image.NEAREST)
            img.paste(char_img, (x_pos, 0))
        x_pos += (char_width + spacing) * scale

    return img

def show_font_sheet(font_data, output_path, chars_per_row=16, font_type='large'):
    """Create a sheet showing all printable ASCII characters"""
    if font_type == 'large':
        char_width = 12
        char_height = 24
        render_func = render_large_char
        start_char = 32
        end_char = 128
    else:
        char_width = 8
        char_height = 8
        render_func = render_small_char
        start_char = 32
        end_char = 128

    scale = 2

    # Show printable characters
    num_chars = end_char - start_char

    rows = (num_chars + chars_per_row - 1) // chars_per_row

    width = chars_per_row * char_width * scale
    height = rows * char_height * scale

    img = Image.new('RGB', (width, height), (40, 40, 40))

    for i in range(num_chars):
        char_code = start_char + i
        row = i // chars_per_row
        col = i % chars_per_row

        x = col * char_width * scale
        y = row * char_height * scale

        char_img = render_func(font_data, char_code, (255, 255, 255), (40, 40, 40))
        char_img = char_img.resize((char_width * scale, char_height * scale), Image.NEAREST)
        img.paste(char_img, (x, y))

    img.save(output_path)
    print(f"Font sheet saved to {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Extract and render Alfred Pelrock fonts")
        print("\nUsage: python extract_font.py <ALFRED.9> [text] [font_type]")
        print("\nFont types:")
        print("  large - 12x24 dialog font (default)")
        print("  small - 8x8 system font")
        print("\nExample:")
        print('  python extract_font.py ALFRED.9 "Hello world" large')
        sys.exit(1)

    alfred9_path = sys.argv[1]
    text = sys.argv[2] if len(sys.argv) > 2 else "Hello world"
    font_type = sys.argv[3] if len(sys.argv) > 3 else "large"

    if not Path(alfred9_path).exists():
        print(f"Error: File not found: {alfred9_path}")
        sys.exit(1)

    # Extract fonts
    print(f"Extracting fonts from {alfred9_path}...")
    small_font = extract_small_font(alfred9_path)
    large_font = extract_large_font(alfred9_path)
    print(f"  Small font: {len(small_font)} bytes (8x8, 256 chars)")
    print(f"  Large font: {len(large_font)} bytes (12x24, 96 chars)")

    # Choose font
    if font_type == 'small':
        font_data = small_font
    else:
        font_data = large_font

    # Render text
    print(f'\nRendering "{text}" with {font_type} font...')
    img = render_text(font_data, text, scale=3, font_type=font_type)
    output_file = f"rendered_{font_type}.png"
    img.save(output_file)
    print(f"  Saved to {output_file}")

    # Create font sheets
    print("\nCreating font sheets...")
    show_font_sheet(small_font, "font_sheet_small.png", font_type='small')
    show_font_sheet(large_font, "font_sheet_large.png", font_type='large')

    print("\nDone!")

if __name__ == "__main__":
    main()
