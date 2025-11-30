#!/usr/bin/env python3
"""
Extract the missing RLE frame at 0x00046000
This is the frame that creates the "smoothing" effect!
"""

import struct
from pathlib import Path
from PIL import Image

def decode_rle(data, start_pos, max_size=256000):
    """
    Decode RLE format (Type 1)
    Based on Ghidra decompilation of decode_rle_frame

    Format:
    - If byte & 0xC0 == 0xC0: count = byte & 0x3F, next byte is value
    - Else: count = 1, current byte is value
    """
    result = bytearray()
    pos = start_pos

    while len(result) < max_size and pos < len(data):
        count_byte = data[pos]
        pos += 1

        if (count_byte & 0xC0) == 0xC0:
            # RLE: count in lower 6 bits, next byte is value
            count = count_byte & 0x3F
            if pos >= len(data):
                break
            value = data[pos]
            pos += 1
            result.extend([value] * count)
        else:
            # Literal: count is 1, this byte is the value
            result.append(count_byte)

    # Pad to exact size
    if len(result) < max_size:
        result.extend([0] * (max_size - len(result)))

    return bytes(result[:max_size])

def decode_block_copy(data, pos):
    """Decode block copy format (Type 2)"""
    frame = bytearray([0x00] * 256000)
    while pos + 5 <= len(data):
        dest = data[pos] | (data[pos+1] << 8) | (data[pos+2] << 16)
        length = data[pos + 4]
        if length == 0:
            break
        if dest + length > 256000:
            break
        pos += 5
        frame[dest:dest+length] = data[pos:pos+length]
        pos += length
    return bytes(frame)

def extract_palette(data):
    """Extract VGA palette"""
    palette = []
    for i in range(256):
        offset = 0x09 + i * 3
        palette.extend([data[offset]*4, data[offset+1]*4, data[offset+2]*4])
    return palette

def main():
    ssn_file = "files/ESCENAX.SSN"
    output_dir = "bedroom_complete"

    if not Path(ssn_file).exists():
        print(f"Error: {ssn_file} not found")
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(ssn_file, 'rb') as f:
        data = f.read()

    palette = extract_palette(data)

    print("="*80)
    print("EXTRACTING COMPLETE BEDROOM ANIMATION SEQUENCE")
    print("="*80)
    print()

    # Extract background (Chunk 0)
    print("Frame 0: Background at 0x00005000")
    chunk0_data = bytearray()
    for i in range(13):
        chunk0_data.extend(data[0x5000 + i*0x5000 : 0x5000 + (i+1)*0x5000])
    frame0 = decode_block_copy(chunk0_data, 0x0D)

    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(frame0)
    img.save(output_path / "frame_00_background.png")
    print("  → Saved: frame_00_background.png")

    # Store for XOR accumulation
    accumulated = bytearray(frame0)

    # Extract RLE frame (Chunk 1) - THE MISSING FRAME!
    print("\nFrame 1: RLE Delta at 0x00046000 (THE MISSING FRAME!)")
    chunk1_data = bytearray()
    for i in range(6):
        chunk1_data.extend(data[0x46000 + i*0x5000 : 0x46000 + (i+1)*0x5000])

    print("  → Decoding RLE data...")
    delta1 = decode_rle(chunk1_data, 0x0D)

    non_zero = sum(1 for b in delta1 if b != 0)
    print(f"  → Non-zero pixels: {non_zero} / 256000 ({non_zero/256000*100:.1f}%)")

    # Apply XOR
    print("  → Applying XOR with background...")
    for i in range(256000):
        accumulated[i] ^= delta1[i]

    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(accumulated)
    img.save(output_path / "frame_01_rle_delta.png")
    print("  → Saved: frame_01_rle_delta.png")
    print("  → THIS IS THE FRAME THAT CREATES THE 'SMOOTHING' EFFECT!")

    # Extract remaining 8 deltas (Chunks 2-9)
    delta_offsets = [
        0x64000,  # Chunk 2
        0x69000,  # Chunk 3
        0x6E000,  # Chunk 4
        0x73000,  # Chunk 5
        0x78000,  # Chunk 6
        0x7D000,  # Chunk 7
        0x82000,  # Chunk 8
        0x87000,  # Chunk 9
    ]

    for idx, offset in enumerate(delta_offsets, start=2):
        print(f"\nFrame {idx}: Delta at 0x{offset:08X}")
        delta = decode_block_copy(data, offset + 0x0D)

        # Apply XOR
        for i in range(256000):
            accumulated[i] ^= delta[i]

        img = Image.new('P', (640, 400))
        img.putpalette(palette)
        img.putdata(accumulated)
        img.save(output_path / f"frame_{idx:02d}_delta.png")
        print(f"  → Saved: frame_{idx:02d}_delta.png")

    print("\n" + "="*80)
    print("EXTRACTION COMPLETE!")
    print("="*80)
    print(f"""
Total frames extracted: 10
  - Frame 0: Clean background
  - Frame 1: RLE delta (the "smoothing" frame)
  - Frames 2-9: Animation deltas (torch flickering)

Output directory: {output_path.absolute()}

Now compare frame_00_background.png and frame_01_rle_delta.png
You should see the "smoothing" effect between them!
    """)

if __name__ == "__main__":
    main()
