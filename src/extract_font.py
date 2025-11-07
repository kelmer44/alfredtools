#!/usr/bin/env python3
"""
Extract and render the Alfred Pelrock font
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw

def extract_font(alfred9_path):
    """Extract 8x8 bitmap font from ALFRED.9"""
    with open(alfred9_path, 'rb') as f:
        f.seek(0x8f32)
        font_data = f.read(0x800)  # 256 characters * 8 bytes

    if len(font_data) != 0x800:
        raise ValueError(f"Expected 2048 bytes, got {len(font_data)}")

    return font_data

def render_char(font_data, char_code, fg_color=(255, 255, 255), bg_color=(0, 0, 0)):
    """Render a single character as an 8x8 image"""
    offset = char_code * 8
    img = Image.new('RGB', (8, 8), bg_color)
    pixels = img.load()

    for y in range(8):
        byte = font_data[offset + y]
        for x in range(8):
            if byte & (1 << (7 - x)):
                pixels[x, y] = fg_color

    return img

def render_text(font_data, text, scale=4, fg_color=(255, 255, 255), bg_color=(0, 0, 0)):
    """Render text string using the font"""
    char_width = 8
    char_height = 8
    spacing = 0

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
            char_img = render_char(font_data, char_code, fg_color, bg_color)
            # Scale up
            char_img = char_img.resize((char_width * scale, char_height * scale), Image.NEAREST)
            img.paste(char_img, (x_pos, 0))
        x_pos += (char_width + spacing) * scale

    return img

def show_font_sheet(font_data, output_path, chars_per_row=16):
    """Create a sheet showing all printable ASCII characters"""
    char_width = 8
    char_height = 8
    scale = 3

    # Show ASCII 32-127 (printable characters)
    start_char = 32
    end_char = 128
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

        char_img = render_char(font_data, char_code, (255, 255, 255), (40, 40, 40))
        char_img = char_img.resize((char_width * scale, char_height * scale), Image.NEAREST)
        img.paste(char_img, (x, y))

    img.save(output_path)
    print(f"Font sheet saved to {output_path}")

def main():
    if len(sys.argv) < 2:
        print("Extract and render Alfred Pelrock font")
        print("\nUsage: python extract_font.py <ALFRED.9> [text]")
        print("\nExample:")
        print('  python extract_font.py ALFRED.9 "Hello world"')
        sys.exit(1)

    alfred9_path = sys.argv[1]
    text = sys.argv[2] if len(sys.argv) > 2 else "Hello world"

    if not Path(alfred9_path).exists():
        print(f"Error: File not found: {alfred9_path}")
        sys.exit(1)

    # Extract font
    print(f"Extracting font from {alfred9_path}...")
    font_data = extract_font(alfred9_path)
    print(f"  Extracted {len(font_data)} bytes (256 characters)")

    # Render text
    print(f'\nRendering "{text}"...')
    img = render_text(font_data, text, scale=4)
    output_file = "rendered_text.png"
    img.save(output_file)
    print(f"  Saved to {output_file}")

    # Create font sheet
    print("\nCreating font sheet...")
    show_font_sheet(font_data, "font_sheet.png")

    print("\nDone!")

if __name__ == "__main__":
    main()
