
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

def find_font_locations():
    """Try to find font data in different ALFRED files"""
    possible_files = ["ALFRED.4", "ALFRED.7", "ALFRED.9"]
    font_locations = {}

    # Known offsets to try
    large_font_offsets = [0x7dc8, 0xfe945, 0x2137a8]  # Found these in various code references
    small_font_offsets = [0x8f32]  # This one we know works

    for file in possible_files:
        try:
            with open(file, 'rb') as f:
                data = f.read()

            print(f"Checking {file}...")

            # Check small font location (we know this one)
            if len(data) >= 0x8f32 + 0x800:
                sample = extract_small_font_char(data[0x8f32:0x8f32+0x800], 65)  # Try extracting 'A'
                if is_valid_font_char(sample):
                    font_locations[f"{file}_small"] = (file, 0x8f32)

            # Try all possible large font locations
            for offset in large_font_offsets:
                if len(data) >= offset + 0x12C0:
                    sample = extract_large_font_char(data[offset:offset+0x12C0], 65)  # Try extracting 'A'
                    if is_valid_font_char(sample):
                        font_locations[f"{file}_large_{offset:x}"] = (file, offset)

        except FileNotFoundError:
            print(f"File {file} not found, skipping...")
            continue

    return font_locations

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

    # Try to find font data in different files
    font_locations = find_font_locations()

    # Process each found font location
    for loc_name, (filename, offset) in font_locations.items():
        print(f"\nProcessing {loc_name} from {filename} at offset 0x{offset:x}")

        with open(filename, 'rb') as f:
            data = f.read()

        if "_small" in loc_name:
            # Extract small font (256 characters)
            font_data = data[offset:offset + 0x800]
            chars = []
            for i in range(256):
                char = extract_small_font_char(font_data, i)
                chars.append(char)
            font_img = create_font_image(chars, 8, 8, 16)

            # Save files
            font_img.save(output_path / f'{loc_name}.png')
            with open(output_path / f'{loc_name}.bin', 'wb') as f:
                f.write(font_data)

        else:
            # Extract large font (96 characters)
            font_data = data[offset:offset + 0x12C0]
            chars = []
            for i in range(96):
                char = extract_large_font_char(font_data, i)
                chars.append(char)
            font_img = create_font_image(chars, 12, 24, 16)

            # Save files
            font_img.save(output_path / f'{loc_name}.png')
            with open(output_path / f'{loc_name}.bin', 'wb') as f:
                f.write(font_data)

if __name__ == "__main__":
    main()
