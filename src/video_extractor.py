#!/usr/bin/env python3
"""
CORRECT hybrid approach:
- Lines 0-101: Raw read with stride 652 (no markers)
- Lines 102-204: Remove markers, then stride 640
- Lines 205-399: Raw read with stride 652 (no markers)
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

print("Correct Hybrid Extraction")
print("=" * 80)

start_offset = 0x5010
result = bytearray(256000)

# REGION 1: Lines 0-101 (stride 652, no markers)
print("\nRegion 1: Lines 0-101 (stride 652)")
for y in range(102):
    src_offset = start_offset + (y * 652)
    dst_offset = y * 640

    if src_offset + 640 <= len(data):
        result[dst_offset:dst_offset + 640] = data[src_offset:src_offset + 640]

region1_end = start_offset + (102 * 652)
print(f"  Lines 0-101 done, ended at 0x{region1_end:08X}")

# REGION 2: Lines 102-204 (remove markers, then stride 640)
print("\nRegion 2: Lines 102-204 (marker region)")

# Start from where region 1 ended
marker_region_start = region1_end

# Build clean data for this region by removing ALL markers
pos = marker_region_start
clean_region2 = bytearray()
markers_removed = 0

# We need 103 lines * 640 pixels = 65,920 bytes after marker removal
target_clean_bytes = 103 * 640

while len(clean_region2) < target_clean_bytes and pos < len(data):
    # Check for marker
    if pos + 5 <= len(data) and data[pos+2:pos+5] == b'\x01\x00\xFF':
        # Skip marker
        pos += 5
        markers_removed += 1
    else:
        # Copy byte
        clean_region2.append(data[pos])
        pos += 1

print(f"  Removed {markers_removed} markers")
print(f"  Clean data: {len(clean_region2)} bytes")
print(f"  Ended at file offset: 0x{pos:08X}")

# Now read these 103 lines with stride 640 (no padding!)
for y in range(103):
    src_offset = y * 640
    dst_offset = (102 + y) * 640

    if src_offset + 640 <= len(clean_region2):
        result[dst_offset:dst_offset + 640] = clean_region2[src_offset:src_offset + 640]

# REGION 3: Lines 205-399 (stride 652, no markers)
print("\nRegion 3: Lines 205-399 (stride 652)")

region3_start = pos
for y in range(195):  # Lines 205-399
    src_offset = region3_start + (y * 652)
    dst_offset = (205 + y) * 640

    if src_offset + 640 <= len(data):
        result[dst_offset:dst_offset + 640] = data[src_offset:src_offset + 640]

region3_end = region3_start + (194 * 652) + 640
print(f"  Lines 205-399 done, ended at 0x{region3_end:08X}")

# Save
img = Image.new('P', (640, 400))
img.putpalette(palette)
img.putdata(result)
img.save('frame_CORRECT_HYBRID.png')

print("\n" + "=" * 80)
print("Saved frame_CORRECT_HYBRID.png")
print("This should have:")
print("  - Lines 0-101: Clean")
print("  - Lines 102-204: Unwarped (markers removed)")
print("  - Lines 205-399: Clean")
print("=" * 80)
