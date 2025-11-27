#!/usr/bin/env python3
"""
Conservative SSN Frame Extractor

Only remove markers with confirmed pattern: XX XX 01 00 FF
(These match the original marker signature from the file)

Leave XX XX 00/02/03 00 FF alone - they might be image data
"""
from PIL import Image

with open('files/ESCENAX.SSN', 'rb') as f:
    data = f.read()

# Get palette
file_palette = data[9:9+768]
palette = []
for i in range(256):
    r = file_palette[i * 3] * 4
    g = file_palette[i * 3 + 1] * 4
    b = file_palette[i * 3 + 2] * 4
    palette.extend([r, g, b])

print("Conservative SSN Frame Extractor")
print("=" * 80)

# PASS 1: Extract with 255+5 pattern
print("\nPass 1: Removing primary markers (255+5 pattern)...")

start = 0x5012
pass1_data = bytearray()
pos = start
copied_bytes = 0

while pos < len(data) and len(pass1_data) < 300000:
    if copied_bytes >= 255:
        copied_bytes = 0
        pos += 5

    pass1_data.append(data[pos])
    pos += 1
    copied_bytes += 1

print(f"  Extracted: {len(pass1_data)} bytes")

# PASS 2: Remove ONLY markers with signature XX XX 01 00 FF
print("\nPass 2: Removing only XX XX 01 00 FF markers (confirmed pattern)...")

pass2_data = bytearray()
i = 0
markers_removed = 0

while i < len(pass1_data):
    # Check for SPECIFIC marker: ?? ?? 01 00 FF
    if ( i + 5 <= len(pass1_data) and (pass1_data[i+2:i+5] == b'\x01\x00\xFF')):
            # This is the confirmed marker pattern - skip it
            i += 5
            markers_removed += 1
    # if ( i + 5 <= len(pass1_data) and (pass1_data[i+2:i+5] == b'\x02\x00\xFF')):
    #         # This is the confirmed marker pattern - skip it
    #         i += 6
    #         markers_removed += 1
        # elif(pass1_data[i+2:i+5] == b'\x02\x00\xFF'):
        #     i += 5
        #     markers_removed += 1
    else:
        pass2_data.append(pass1_data[i])
        i += 1

    if len(pass2_data) >= 256000:
        break

print(f"  Removed {markers_removed} markers with 01 00 FF signature")
print(f"  Final data: {len(pass2_data)} bytes")

# Save frame
img = Image.new('P', (640, 400))
img.putpalette(palette)
img.putdata(pass2_data[:256000])
img.save('frame_CONSERVATIVE.png')

print("\n" + "=" * 80)
print("Saved: frame_CONSERVATIVE.png")
print("\nThis keeps potential image data with 00/02/03 signatures")
print("=" * 80)
