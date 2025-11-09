
import sys
from pathlib import Path
from PIL import Image
import numpy as np

def extract_large_font_char(data, char_index):
    """Extract a single character from the large font data (12x24 pixels)
    Each character is 48 bytes (24 rows × 2 bytes per row)"""
    offset = char_index * 0x30  # 48 bytes per character
    char_data = data[offset:offset + 0x30]

    # Create 12x24 pixel array
    pixels = np.zeros((24, 12), dtype=np.uint8)

    # Process each row (2 bytes per row)
    for row in range(24):
        byte1 = char_data[row * 2]
        byte2 = char_data[row * 2 + 1]

        # Process 12 bits (12 pixels) from the two bytes
        for bit in range(8):
            pixels[row, bit] = 255 if (byte1 & (0x80 >> bit)) else 0
        for bit in range(4):
            pixels[row, bit + 8] = 255 if (byte2 & (0x80 >> bit)) else 0

    return pixels

def extract_small_font_char(data, char_index):
    """Extract a single character from the small font data (8x8 pixels)
    Each character is 8 bytes (8 rows × 1 byte per row)"""
    offset = char_index * 8  # 8 bytes per character
    char_data = data[offset:offset + 8]

    # Create 8x8 pixel array
    pixels = np.zeros((8, 8), dtype=np.uint8)

    # Process each row (1 byte per row)
    for row in range(8):
        byte = char_data[row]
        for bit in range(8):
            pixels[row, bit] = 255 if (byte & (0x80 >> bit)) else 0

    return pixels

def create_font_image(chars, char_width, char_height, chars_per_row=16):
    """Create a single image containing all characters in a grid"""
    rows = (len(chars) + chars_per_row - 1) // chars_per_row
    img_width = chars_per_row * char_width
    img_height = rows * char_height

    # Create the full image
    img = Image.new('L', (img_width, img_height), 0)

    # Place each character in the grid
    for i, char in enumerate(chars):
        row = i // chars_per_row
        col = i % chars_per_row
        x = col * char_width
        y = row * char_height

        # Convert numpy array to PIL Image and paste
        char_img = Image.fromarray(char)
        img.paste(char_img, (x, y))

    return img

# Known font locations and sizes
FONT_SPECS = {
    'small': {
        'file': "ALFRED.4",
        'offset': 0x8F32,
        'size': 0x800,      # 256 characters × 8 bytes
        'char_size': 8,     # 8 bytes per character (8×8 pixels)
        'width': 8,
        'height': 8,
        'chars': 256
    },
    'large': {
        'file': "ALFRED.7",
        'offset': 0x7DC8,
        'size': 0x12C0,     # 96 characters × 48 bytes
        'char_size': 0x30,  # 48 bytes per character (12×24 pixels)
        'width': 12,
        'height': 24,
        'chars': 96
    },
    'computer': {
        'file': "ALFRED.7",
        'offset': 0x1AA0A,
        'size': 0x70CA,     # Total screen data size
        'char_size': 8,     # Assumed 8 bytes per character
        'width': 8,
        'height': 8,
        'chars': 256
    }
}

def extract_font(font_type):
    """Extract a specific font type using its specifications"""
    spec = FONT_SPECS[font_type]

    try:
        with open(spec['file'], 'rb') as f:
            data = f.read()

        font_data = data[spec['offset']:spec['offset'] + spec['size']]
        chars = []

        # Extract each character
        for i in range(spec['chars']):
            if font_type == 'large':
                char = extract_large_font_char(font_data, i)
            else:
                char = extract_small_font_char(font_data, i)
            chars.append(char)

        return font_data, chars

    except FileNotFoundError:
        print(f"Error: {spec['file']} not found")
        return None, None

def is_valid_font_char(pixels):
    """Check if an extracted character looks like it could be valid font data"""
    # Simple heuristic: should have some black and some white pixels
    black_pixels = np.sum(pixels == 0)
    white_pixels = np.sum(pixels == 255)
    return white_pixels > 0 and black_pixels > 0

def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "font/"
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Extract each font type
    for font_type, spec in FONT_SPECS.items():
        print(f"\nExtracting {font_type} font from {spec['file']} at offset 0x{spec['offset']:x}")

        font_data, chars = extract_font(font_type)
        if font_data and chars:
            # Create and save visualization
            font_img = create_font_image(chars, spec['width'], spec['height'], 16)
            font_img.save(output_path / f'{font_type}_font.png')

            # Save raw font data
            with open(output_path / f'{font_type}_font.bin', 'wb') as f:
                f.write(font_data)

if __name__ == "__main__":
    main()
