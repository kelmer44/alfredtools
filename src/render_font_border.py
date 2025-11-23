#!/usr/bin/env python3
"""
Alfred Pelrock Font Renderer - CORRECTED
Applies the game's border rendering algorithm to render text with pink color and black borders

THE FIX: The original script was missing edge borders because the border algorithm
needs to check pixels OUTSIDE the character bounds. Solution: add 1 pixel padding
on all sides to accommodate border pixels that fall outside the original 12×24 character.
"""

from PIL import Image
import sys

def load_font(font_path):
    """Load the bitmap font image"""
    return Image.open(font_path).convert('RGB')

def extract_character(font_img, char):
    """
    Extract a character from the font bitmap

    Font layout (from the image):
    Row 0: !"#$%&'()*+,-./
    Row 1: 0123456789:;<=>?
    Row 2: @ABCDEFGHIJKLMNO
    Row 3: PQRSTUVWXYZ[¿]^_
    Row 4: `abcdefghijklmno
    Row 5: pqrstuvwxyz{¡}~

    Each character is 12 pixels wide × 24 pixels tall
    """
    char_width = 12
    char_height = 24

    # Map character to position
    char_map = {
        # Row 0
        '!': (0, 0), '"': (1, 0), '#': (2, 0), '$': (3, 0), '%': (4, 0),
        '&': (5, 0), "'": (6, 0), '(': (7, 0), ')': (8, 0), '*': (9, 0),
        '+': (10, 0), ',': (11, 0), '-': (12, 0), '.': (13, 0), '/': (14, 0),

        # Row 1
        '0': (0, 1), '1': (1, 1), '2': (2, 1), '3': (3, 1), '4': (4, 1),
        '5': (5, 1), '6': (6, 1), '7': (7, 1), '8': (8, 1), '9': (9, 1),
        ':': (10, 1), ';': (11, 1), '<': (12, 1), '=': (13, 1), '>': (14, 1), '?': (15, 1),

        # Row 2
        '@': (0, 2), 'A': (1, 2), 'B': (2, 2), 'C': (3, 2), 'D': (4, 2),
        'E': (5, 2), 'F': (6, 2), 'G': (7, 2), 'H': (8, 2), 'I': (9, 2),
        'J': (10, 2), 'K': (11, 2), 'L': (12, 2), 'M': (13, 2), 'N': (14, 2), 'O': (15, 2),

        # Row 3
        'P': (0, 3), 'Q': (1, 3), 'R': (2, 3), 'S': (3, 3), 'T': (4, 3),
        'U': (5, 3), 'V': (6, 3), 'W': (7, 3), 'X': (8, 3), 'Y': (9, 3),
        'Z': (10, 3), '[': (11, 3), '¿': (12, 3), ']': (13, 3), '^': (14, 3), '_': (15, 3),

        # Row 4
        '`': (0, 4), 'a': (1, 4), 'b': (2, 4), 'c': (3, 4), 'd': (4, 4),
        'e': (5, 4), 'f': (6, 4), 'g': (7, 4), 'h': (8, 4), 'i': (9, 4),
        'j': (10, 4), 'k': (11, 4), 'l': (12, 4), 'm': (13, 4), 'n': (14, 4), 'o': (15, 4),

        # Row 5
        'p': (0, 5), 'q': (1, 5), 'r': (2, 5), 's': (3, 5), 't': (4, 5),
        'u': (5, 5), 'v': (6, 5), 'w': (7, 5), 'x': (8, 5), 'y': (9, 5),
        'z': (10, 5), '{': (11, 5), '¡': (12, 5), '}': (13, 5), '~': (14, 5),

        # Space
        ' ': None  # Space is just blank
    }

    if char not in char_map:
        char = char.upper()  # Try uppercase
        if char not in char_map:
            return None

    pos = char_map[char]
    if pos is None:  # Space character
        return Image.new('RGB', (char_width, char_height), (0, 0, 0))

    col, row = pos
    x = col * char_width
    y = row * char_height

    # Extract the character
    char_img = font_img.crop((x, y, x + char_width, y + char_height))
    return char_img

def apply_border_algorithm(char_img, text_color=(255, 0, 255), border_color=(0, 0, 0)):
    """
    Apply the Alfred Pelrock border rendering algorithm

    THE FIX: Add 1 pixel padding on all sides so borders can extend outside
    the original character bounds.

    Algorithm:
    1. Expand canvas by 2 pixels (1 on each side) - 12×24 becomes 14×26
    2. Place character in center of padded canvas
    3. For each character pixel, mark 3×3 area around it for borders
    4. Draw borders only in empty (non-character) pixels
    5. Draw character pixels on top
    """
    orig_width, orig_height = char_img.size

    # Add padding: +1 pixel on each side
    width = orig_width + 2
    height = orig_height + 2

    # Convert character to bitmask
    pixels = char_img.load()
    mask = [[False for _ in range(width)] for _ in range(height)]

    # Place character in center of padded canvas (offset by 1)
    for y in range(orig_height):
        for x in range(orig_width):
            r, g, b = pixels[x, y]
            # White or light pixels are part of character
            mask[y + 1][x + 1] = (r + g + b) > 128 * 3

    # Create output image with white background
    output = Image.new('RGB', (width, height), (255, 255, 255))
    out_pixels = output.load()

    # Step 1: Mark border pixels
    # For each character pixel, mark a 3×3 area around it for border
    border_mask = [[False for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if mask[y][x]:  # If this is a character pixel
                # Mark 3×3 area around it for border
                for dy in range(-1, 2):  # -1, 0, 1
                    for dx in range(-1, 2):  # -1, 0, 1
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < height and 0 <= nx < width:
                            if not mask[ny][nx]:  # Only mark empty pixels
                                border_mask[ny][nx] = True

    # Step 2: Draw the borders (black)
    for y in range(height):
        for x in range(width):
            if border_mask[y][x]:
                out_pixels[x, y] = border_color

    # Step 3: Draw the character pixels (pink/text color) on top of borders
    for y in range(height):
        for x in range(width):
            if mask[y][x]:
                out_pixels[x, y] = text_color

    return output

def render_text(font_img, text, text_color=(255, 105, 180), border_color=(0, 0, 0)):
    """
    Render text using the font and border algorithm
    Pink color: (255, 105, 180) - hot pink (matches game palette)
    """
    char_width = 12
    char_height = 24

    # With padding, each character is 14×26
    padded_char_width = char_width + 2
    padded_char_height = char_height + 2

    # Calculate output size
    output_width = len(text) * padded_char_width
    output_height = padded_char_height

    # Create output image with white background
    output = Image.new('RGB', (output_width, output_height), (255, 255, 255))

    # Render each character
    for i, char in enumerate(text):
        char_img = extract_character(font_img, char)
        if char_img:
            # Apply border algorithm
            rendered_char = apply_border_algorithm(char_img, text_color, border_color)

            # Paste into output
            x_pos = i * padded_char_width
            output.paste(rendered_char, (x_pos, 0))

    return output

def main():
    font_path = '/mnt/user-data/uploads/large_font.png'

    # Load font
    print("Loading font...")
    font_img = load_font(font_path)

    # Render "Hello world" with pink text and black borders
    text = "Hello world"
    print(f"Rendering '{text}'...")

    # Use pink color (matches game's palette index 13)
    pink = (255, 105, 180)  # Hot pink
    black = (0, 0, 0)

    output = render_text(font_img, text, pink, black)

    # Save output
    output_path = '/mnt/user-data/outputs/hello_world_rendered.png'
    output.save(output_path)
    print(f"Saved to: {output_path}")

    # Also create a larger version for better visibility
    scale = 3
    large_output = output.resize((output.width * scale, output.height * scale), Image.NEAREST)
    large_output_path = '/mnt/user-data/outputs/hello_world_rendered_3x.png'
    large_output.save(large_output_path)
    print(f"Saved 3x version to: {large_output_path}")

    print("\n✓ Done! Borders now appear on all edges including left/right.")
    print(f"Image size: {output.width}×{output.height}")
    print(f"Text: '{text}' ({len(text)} characters)")
    print(f"Character size with borders: 14×26 pixels (12×24 + padding)")

if __name__ == "__main__":
    main()
