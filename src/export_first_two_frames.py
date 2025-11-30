#!/usr/bin/env python3
"""
SSN Video Frame Extractor: First Frame and First Delta
Exports the first frame and the first delta-applied frame from ESCENAX.SSN
"""


from PIL import Image
import sys
sys.path.append('src')
from extract_buda_7 import decompress_rle

def extract_palette(data):
    """Extract and convert VGA palette to 8-bit RGB"""
    file_palette = data[0x0009:0x0009 + 768]
    palette = []
    for i in range(256):
        r = file_palette[i * 3 + 0] * 4
        g = file_palette[i * 3 + 1] * 4
        b = file_palette[i * 3 + 2] * 4
        palette.extend([r, g, b])
    return palette

def decode_block_copy_frame(data, chunk_offset):
    """
    Decode a Type 2 (block copy) frame
    Args:
        data: Full file data
        chunk_offset: Offset to chunk header
    Returns:
        bytearray of 256,000 pixels
    """
    frame_buffer = bytearray([0x00] * 256000)
    pos = chunk_offset + 0x0D
    while pos + 5 < len(data):
        dest_lo = data[pos]
        dest_mid = data[pos + 1]
        dest_hi = data[pos + 2]
        length = data[pos + 4]
        if length == 0:
            break
        dest_offset = dest_lo | (dest_mid << 8) | (dest_hi << 16)
        print(f"Decoding block copy: dest={dest_offset:06X}, length={length}")

        if dest_offset + length > 256000:
            break
        pos += 5
        pixel_data = data[pos:pos + length]
        frame_buffer[dest_offset:dest_offset + length] = pixel_data
        pos += length
    return frame_buffer

def main():
    ssn_file = "files/ESCENAX.SSN"
    with open(ssn_file, 'rb') as f:
        data = f.read()
    palette = extract_palette(data)


    # Frame extraction order (from ssn_format_summary.md)
    delta_offsets = [
        # 0xF0000,
        0x64000,
        0x69000,
        0x6E000,
        0x73000,
        0x78000,
        0x7D000,
        0x82000,
        0x87000
    ]


    # Extract background (frame 0)
    chunk0 = bytearray()
    for i in range(13):
        chunk0.extend(data[0x5000 + i*0x5000 : 0x5000 + (i+1)*0x5000])
    background = decode_block_copy_frame(chunk0, 0)

    # Save frame 0 (background)
    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(background)
    img.save('frame0.png')
    print('Exported: frame0.png')

    # # XOR the frame at 0x46000 as the first delta
    first_delta_offset = 0xF0000

    first_delta = decode_block_copy_frame(data, first_delta_offset)
    accumulated = bytearray(background)
    for i in range(256000):
        accumulated[i] ^= first_delta[i]
    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(accumulated)
    img.save('frame1.png')
    print('Exported: frame1.png')

    # Export subsequent frames: start from accumulated
    for idx, offset in enumerate(delta_offsets):
        print(f'Applying delta {idx+2} at offset {hex(offset)}')
        delta = decode_block_copy_frame(data, offset)
        for i in range(256000):
            accumulated[i] ^= delta[i]
        img = Image.new('P', (640, 400))
        img.putpalette(palette)
        img.putdata(accumulated)
        img.save(f'frame{idx+2}.png')
        print(f'Exported: frame{idx+2}.png')

    print("All frames exported (frame0.png ... frame10.png)")

if __name__ == "__main__":
    main()
