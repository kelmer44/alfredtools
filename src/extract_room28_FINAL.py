#!/usr/bin/env python3
"""
Extract room 28 with the CORRECT lit palette at 0x001610CE
"""
import struct
from PIL import Image
from pathlib import Path

def decompress_rle(data, offset, end_offset):
    result = bytearray()
    pos = offset
    while pos + 2 <= min(end_offset, len(data)):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break
        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2
    return bytes(result)

# Read room 28 background
alfred1_path = 'files/ALFRED.1'
room_28_offset = 28 * 104

with open(alfred1_path, 'rb') as f:
    f.seek(room_28_offset)
    pair_data = f.read(64)

pairs = []
for i in range(8):
    offset = struct.unpack('<I', pair_data[i*8:i*8+4])[0]
    size = struct.unpack('<I', pair_data[i*8+4:i*8+8])[0]
    pairs.append((offset, size))

bg_data = bytearray()
for i, (offset, size) in enumerate(pairs):
    if size == 0 or offset == 0:
        continue
    with open(alfred1_path, 'rb') as f:
        f.seek(offset)
        raw = f.read(size)
    decompressed = decompress_rle(raw, 0, len(raw))
    bg_data.extend(decompressed)

print(f"Background: {len(bg_data)} bytes")

# Read the CORRECT lit palette at 0x001610CE
with open('files/ALFRED.7', 'rb') as f:
    f.seek(0x001610CE)
    pal_data = f.read(768)

# Convert to 8-bit RGB
palette = []
for i in range(256):
    r = min(255, pal_data[i * 3] * 4)
    g = min(255, pal_data[i * 3 + 1] * 4)
    b = min(255, pal_data[i * 3 + 2] * 4)
    palette.extend([r, g, b])

# Create image
size = 640 * 400
img_data = bytes(bg_data[:size])
if len(img_data) < size:
    img_data += bytes([0] * (size - len(img_data)))

img = Image.new('P', (640, 400))
img.putpalette(palette)
img.putdata(img_data)

output_path = Path('room28_CORRECT_LIT.png')
img.save(output_path)

print(f"\n✓ Saved {output_path}")
print(f"\nLit palette location: ALFRED.7 at 0x001610CE")
print(f"Dark palette location: ALFRED.1 at 0x00585350 (room 28 pair 11)")
print(f"\nFirst 16 colors of lit palette:")
for i in range(16):
    r = pal_data[i*3]
    g = pal_data[i*3+1]
    b = pal_data[i*3+2]
    print(f"  {i:2d}: ({r:2d},{g:2d},{b:2d})", end="")
    if (i+1) % 4 == 0:
        print()
