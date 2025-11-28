"""
COMPLETE SSN Frame Extractor - Variable Length Markers

BREAKTHROUGH: Last byte of marker = number of DATA bytes to next marker
Total distance = last_byte + 5 (marker size)

Marker format: [countdown] [countup] [type] 00 [length]
  - Most markers: ?? ?? ?? 00 FF (255 data bytes)
  - Variable markers: ?? ?? ?? 00 XX (XX data bytes)
"""

from PIL import Image
import sys
from pathlib import Path

def extract_frame_variable_markers(ssn_path, output_path):
    """Extract complete frame using variable-length markers"""

    with open(ssn_path, 'rb') as f:
        data = f.read()

    # Get palette
    file_palette = data[9:9+768]
    palette = []
    for i in range(256):
        r = file_palette[i * 3] * 4
        g = file_palette[i * 3 + 1] * 4
        b = file_palette[i * 3 + 2] * 4
        palette.extend([r, g, b])

    frame_data = bytearray()
    frame_start = 0x5012
    pos = frame_start

    print("="*80)
    print("SSN FRAME EXTRACTOR - Variable Length Markers")
    print("="*80)
    print()
    print("Discovery: Last marker byte = number of data bytes")
    print("           Total distance = data_bytes + 5")
    print()

    block_num = 0
    total_markers = 0
    variable_markers = 0

    target_pixels = 640 * 400
    first_marker = 0x5012 + 255
    while len(frame_data) < target_pixels and pos + 5 < len(data):
        # Read marker (we're positioned AT the marker)

        marker = data[pos:pos+5]
        if(pos == frame_start):
            data_length = 255  # First marker is always 255
        else:
            data_length = marker[4]  # Last byte = data length

        # if(data_length > 0):
        print(f"  Marker found at source offset: {pos}, marker bytes: {data[pos:pos+5].hex(" ")}, length: {data_length}")

        # Move past marker
        if(pos != frame_start):
            pos += 5

        # Read data bytes
        if pos + data_length > len(data):
            print(f"\n⚠️  End of file reached")
            break

        pixels = data[pos:pos+data_length]
        frame_data.extend(pixels)
        pos += data_length

        # Track statistics
        total_markers += 1
        if data_length != 255:
            variable_markers += 1

        # Progress display
        if block_num % 100 == 0 or data_length != 255:
            progress = len(frame_data) / target_pixels * 100
            marker_hex = ' '.join(f'{b:02X}' for b in marker)
            length_note = f" ← Variable ({data_length} bytes)" if data_length != 255 else ""
            # print(f"  Block {block_num:4d}: {len(frame_data):6d} pixels ({progress:5.2f}%) - {marker_hex}{length_note}")

        block_num += 1

        # Safety check
        if block_num > 2000:
            print(f"\n⚠️  Safety limit reached (2000 blocks)")
            break

    print()
    print("="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print(f"  Total markers: {total_markers}")
    print(f"  Variable-length markers: {variable_markers}")
    print(f"  Standard markers (255): {total_markers - variable_markers}")
    print(f"  Pixels extracted: {len(frame_data)}")
    print(f"  Target pixels: {target_pixels}")
    print(f"  Final position: 0x{pos:06X}")
    print()

    if len(frame_data) < target_pixels:
        shortage = target_pixels - len(frame_data)
        print(f"  ⚠️  Short by: {shortage} pixels")
        print(f"     Padding with black...")
        frame_data.extend([0] * shortage)
    elif len(frame_data) > target_pixels:
        excess = len(frame_data) - target_pixels
        print(f"  ⚠️  Excess: {excess} pixels")
        print(f"     Trimming...")
        frame_data = frame_data[:target_pixels]
    else:
        print(f"  ✅ Perfect! Exactly {target_pixels} pixels")

    # Save image
    img = Image.new('P', (640, 400))
    img.putpalette(palette)
    img.putdata(frame_data[:target_pixels])
    img.save(output_path)

    print()
    print(f"Saved: {output_path}")
    print(f"Resolution: 640 × 400 pixels")
    print("="*80)

    return len(frame_data) == target_pixels

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_variable_markers.py <ESCENAX.SSN> [output.png]")
        print()
        print("This extractor uses variable-length markers where:")
        print("  Last byte = number of data bytes")
        print("  Distance to next marker = last_byte + 5")
        sys.exit(1)

    ssn_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "frame_complete_variable.png"

    if not Path(ssn_path).exists():
        print(f"Error: File not found: {ssn_path}")
        sys.exit(1)

    success = extract_frame_variable_markers(ssn_path, output_path)

    if success:
        print("\n🎉 SUCCESS! Frame extracted perfectly!")
    else:
        print("\n⚠️  Frame extracted with padding/trimming")

if __name__ == "__main__":
    main()
