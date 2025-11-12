#!/usr/bin/env python3
"""
Alfred Pelrock - Comprehensive Sprite/Animation Extractor
Extracts sprite metadata, positions, flags, and generates sprite sheets from ALFRED.1

This script combines:
- Sprite/animation metadata extraction from Pair 10
- Visual sprite sheet generation from Pair 8
- Hotspot flag analysis for interactive sprites

SPRITE STRUCTURE (44 bytes / 0x2C per sprite):
  +0x00-0x05: [Animation data pointer and counters]
  +0x06-0x09: [Unknown]
  +0x0A-0x0B: x (u16 LE) - Sprite X position
  +0x0C-0x0D: y (u16 LE) - Sprite Y position
  +0x0E:      width (u8) - Sprite width in pixels
  +0x0F:      height (u8) - Sprite height in pixels
  +0x10-0x11: stride (u16 LE) - Bytes per scanline
  +0x12:      total_frames (u8) - Number of animation frames
  +0x13:      current_seq (u8) - Current animation sequence
  +0x14-0x1F: [Frame counts per sequence]
  +0x20:      current_frame (u8) - Current frame in sequence
  +0x21:      z_index (i8) - Drawing order (-1 = hidden)
  +0x22-0x29: [Frame timing and loop data]
  +0x2A-0x2B: extra_data (u16 LE) - Context-specific flags
  +0x2C:      type_flags (u8) - Action bitmask for hotspot interactions
  +0x2D:      frame_counter (u8) - Animation timer
  +0x2E-0x2F: [Loop/repeat counters]
  +0x30:      interactive (u8) - Must be 0 for hotspot functionality
  +0x31:      [Additional flags]

ACTION BITMASK (type_flags at +0x2C):
  Bit 0 (0x01): Open action available
  Bit 1 (0x02): Close action available
  Bit 2 (0x04): Push action available
  Bit 3 (0x08): Pull action available
  Bit 4 (0x10): Pick up action available
  Bit 5 (0x20): Talk to action available
  Bit 6 (0x40): Use action available
  Bit 7 (0x80): Special action available
  Note: "Look" action is always available

SPRITE HOTSPOT CONDITIONS:
  A sprite becomes an interactive hotspot when:
  1. interactive_flag == 0 (offset 0x30)
  2. z_index != -1 (offset 0x21) - sprite must be visible
  3. type_flags != 0 (offset 0x2C) - has available actions
  4. Clicked pixel is not transparent

Usage:
    python extract_sprite_data.py <alfred.1> [output_dir] [--format json|txt|py|png|all]
"""

import struct
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# Action name mapping
ACTION_NAMES = {
    0x01: "Open",
    0x02: "Close",
    0x04: "Push",
    0x08: "Pull",
    0x10: "Pick up",
    0x20: "Talk to",
    0x40: "Use",
    0x80: "Special"
}


def decompress_rle(data, offset, size):
    """Decompress RLE data"""
    result = bytearray()
    pos = offset
    end = offset + size

    while pos + 2 <= end and pos + 2 <= len(data):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            break
        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2

    return bytes(result)


def extract_palette(data, room_offset):
    """Extract palette from Pair 11"""
    pair_offset = room_offset + (11 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size == 0x300:
        palette_data = data[offset:offset+768]
        palette = []
        for i in range(256):
            r = palette_data[i * 3] * 4
            g = palette_data[i * 3 + 1] * 4
            b = palette_data[i * 3 + 2] * 4
            palette.extend([r, g, b])
        return palette
    return None


def extract_sprite_pixel_data(data, room_offset):
    """Extract sprite pixel data from Pair 8"""
    pair_offset = room_offset + (8 * 8)
    offset = struct.unpack('<I', data[pair_offset:pair_offset+4])[0]
    size = struct.unpack('<I', data[pair_offset+4:pair_offset+8])[0]

    if offset > 0 and size > 0:
        return decompress_rle(data, offset, size), offset + size
    return None, None


def get_action_names(type_flags):
    """Get list of available actions from type flags bitmask"""
    actions = ["Look"]  # Look is always available
    for mask, name in ACTION_NAMES.items():
        if type_flags & mask:
            actions.append(name)
    return actions


def parse_sprite_structure(sprite_bytes, sprite_index):
    """Parse a 44-byte sprite structure into a dict"""
    if len(sprite_bytes) < 44:
        return None

    x = struct.unpack('<H', sprite_bytes[0x0A:0x0C])[0]
    y = struct.unpack('<H', sprite_bytes[0x0C:0x0E])[0]
    width = sprite_bytes[0x0E]
    height = sprite_bytes[0x0F]
    stride = struct.unpack('<H', sprite_bytes[0x10:0x12])[0]
    total_frames = sprite_bytes[0x12]
    current_seq = sprite_bytes[0x13]

    # Frame counts for sequences
    seq_frame_counts = []
    for i in range(12):  # Up to 12 sequences
        count = sprite_bytes[0x14 + i]
        if count > 0:
            seq_frame_counts.append(count)

    current_frame = sprite_bytes[0x20]
    z_index = struct.unpack('<b', sprite_bytes[0x21:0x22])[0]  # signed byte
    extra_data = struct.unpack('<H', sprite_bytes[0x2A:0x2C])[0]
    type_flags = sprite_bytes[0x2C] if len(sprite_bytes) > 0x2C else 0
    frame_counter = sprite_bytes[0x2D] if len(sprite_bytes) > 0x2D else 0
    interactive = sprite_bytes[0x30] if len(sprite_bytes) > 0x30 else 0xFF

    # Calculate total actual frames
    actual_frames = sum(seq_frame_counts) if seq_frame_counts else total_frames

    # Determine if sprite is a hotspot
    is_hotspot = (interactive == 0 and z_index != -1 and type_flags != 0)

    actions = get_action_names(type_flags) if is_hotspot else []

    sprite = {
        'index': sprite_index,
        'position': {'x': x, 'y': y},
        'size': {'width': width, 'height': height},
        'stride': stride,
        'animation': {
            'total_frames': total_frames,
            'actual_frames': actual_frames,
            'current_sequence': current_seq,
            'current_frame': current_frame,
            'sequence_frame_counts': seq_frame_counts
        },
        'visibility': {
            'z_index': z_index,
            'visible': z_index != -1
        },
        'hotspot': {
            'is_interactive': is_hotspot,
            'interactive_flag': interactive,
            'type_flags': type_flags,
            'type_flags_hex': f"0x{type_flags:02X}",
            'type_flags_binary': f"{type_flags:08b}",
            'available_actions': actions
        },
        'extra_data': extra_data,
        'frame_counter': frame_counter
    }

    return sprite


def extract_sprites_from_room(data, room_num):
    """Extract sprite metadata from Pair 10 for a specific room"""
    room_offset = room_num * 104
    pair10_offset = room_offset + (10 * 8)
    offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
    size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

    if size == 0 or offset >= len(data):
        return None

    pair10_data = data[offset:offset+size]

    # Sprite count at 0x05
    if 0x05 >= len(pair10_data):
        return None

    sprite_count = pair10_data[0x05]
    if sprite_count == 0:
        return []

    sprites = []
    sprite_base = 0x06  # Sprites start at offset 6

    for i in range(sprite_count):
        entry_base = sprite_base + (i * 44)

        if entry_base + 44 > len(pair10_data):
            break

        # Try to get extra bytes if available (for fields beyond 44 bytes)
        max_bytes = min(60, len(pair10_data) - entry_base)
        sprite_bytes = pair10_data[entry_base:entry_base+max_bytes]
        sprite = parse_sprite_structure(sprite_bytes, i)

        if sprite:
            # Skip completely empty sprites
            if sprite['size']['width'] > 0 or sprite['size']['height'] > 0:
                sprites.append(sprite)

    return sprites if sprites else None


def generate_sprite_sheet(data, room_num, output_path):
    """Generate sprite sheet image from Pair 8 data"""
    if not PIL_AVAILABLE:
        return 0

    room_offset = room_num * 104

    sprite_data, sprite_end = extract_sprite_pixel_data(data, room_offset)
    if not sprite_data or not sprite_end:
        return 0

    palette = extract_palette(data, room_offset)
    if not palette:
        return 0

    # Get sprite metadata to know dimensions
    sprites = extract_sprites_from_room(data, room_num)
    if not sprites:
        return 0

    room_dir = output_path / f"room{room_num:02d}"
    room_dir.mkdir(parents=True, exist_ok=True)

    offset = 0
    extracted = 0

    for sprite in sprites:
        w = sprite['size']['width']
        h = sprite['size']['height']
        frames = sprite['animation']['actual_frames']

        if w == 0 or h == 0 or frames == 0:
            continue

        needed = w * h * frames
        if offset + needed > len(sprite_data):
            break

        anim_data = sprite_data[offset:offset + needed]

        # Create sprite sheet with all frames in a row
        img = Image.new('P', (w * frames, h))
        img.putpalette(palette)

        for frame in range(frames):
            frame_offset = frame * w * h
            for y in range(h):
                for x in range(w):
                    pixel_idx = frame_offset + (y * w) + x
                    if pixel_idx < len(anim_data):
                        pixel_value = anim_data[pixel_idx]
                        img.putpixel((frame * w + x, y), pixel_value)

        output_file = room_dir / f"sprite{sprite['index']}.png"
        img.save(output_file)

        offset += needed
        extracted += 1

    return extracted


class SpriteDataWriter:
    """Handles writing sprite data in various formats"""

    def __init__(self, output_dir: str):
        self.output_path = Path(output_dir)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def write_json(self, rooms_data: List[Dict[str, Any]]):
        """Write sprite data as JSON"""
        json_file = self.output_path / "sprites.json"

        output = {
            'description': 'Alfred Pelrock sprite/animation data',
            'game': 'Alfred Pelrock (1997)',
            'source': 'ALFRED.1 Pair 10',
            'note': 'Sprites with is_interactive=true can be clicked for actions',
            'action_bitmask': {
                '0x01': 'Open',
                '0x02': 'Close',
                '0x04': 'Push',
                '0x08': 'Pull',
                '0x10': 'Pick up',
                '0x20': 'Talk to',
                '0x40': 'Use',
                '0x80': 'Special'
            },
            'rooms': rooms_data
        }

        with open(json_file, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"  JSON: {json_file}")
        return json_file

    def write_python(self, rooms_data: List[Dict[str, Any]]):
        """Write sprite data as Python module"""
        py_file = self.output_path / "sprites.py"

        with open(py_file, 'w') as f:
            f.write("# Alfred Pelrock - Sprite/Animation Data\n")
            f.write("# Auto-generated from ALFRED.1 Pair 10\n\n")

            f.write("SPRITES = {\n")
            for room in rooms_data:
                if room['sprites']:
                    f.write(f"    {room['room']}: [\n")
                    for sprite in room['sprites']:
                        f.write(f"        {sprite},\n")
                    f.write("    ],\n")
            f.write("}\n")

        print(f"  Python: {py_file}")
        return py_file

    def write_text(self, rooms_data: List[Dict[str, Any]]):
        """Write human-readable text summary"""
        txt_file = self.output_path / "sprites.txt"

        with open(txt_file, 'w') as f:
            f.write("Alfred Pelrock - Comprehensive Sprite/Animation Data\n")
            f.write("=" * 70 + "\n\n")

            for room in rooms_data:
                if not room['sprites']:
                    continue

                f.write(f"Room {room['room']}\n")
                f.write("-" * 70 + "\n")

                for sprite in room['sprites']:
                    idx = sprite['index']
                    pos = sprite['position']
                    size = sprite['size']
                    anim = sprite['animation']
                    vis = sprite['visibility']
                    hs = sprite['hotspot']

                    f.write(f"  Sprite {idx}:\n")
                    f.write(f"    Position: ({pos['x']}, {pos['y']})\n")
                    f.write(f"    Size: {size['width']}×{size['height']}\n")
                    f.write(f"    Frames: {anim['actual_frames']} ({anim['total_frames']} total)\n")
                    f.write(f"    Z-Index: {vis['z_index']} ({'visible' if vis['visible'] else 'hidden'})\n")

                    if hs['is_interactive']:
                        f.write(f"    🎯 INTERACTIVE HOTSPOT\n")
                        f.write(f"       Type flags: {hs['type_flags_hex']} ({hs['type_flags_binary']})\n")
                        f.write(f"       Actions: {', '.join(hs['available_actions'])}\n")
                    else:
                        if hs['type_flags'] != 0:
                            f.write(f"    Type flags: {hs['type_flags_hex']} (not interactive: flag={hs['interactive_flag']})\n")

                    if anim['sequence_frame_counts']:
                        f.write(f"    Sequences: {anim['sequence_frame_counts']}\n")

                    f.write("\n")

                f.write("\n")

        print(f"  Text: {txt_file}")
        return txt_file


def print_summary(rooms_data: List[Dict[str, Any]]):
    """Print extraction summary"""
    total_sprites = sum(len(r['sprites']) for r in rooms_data if r['sprites'])
    rooms_with_sprites = sum(1 for r in rooms_data if r['sprites'])

    total_hotspots = sum(
        sum(1 for s in r['sprites'] if s['hotspot']['is_interactive'])
        for r in rooms_data if r['sprites']
    )

    print("\nExtraction Summary:")
    print("=" * 70)
    print(f"  Rooms with sprites: {rooms_with_sprites}/56")
    print(f"  Total sprites: {total_sprites}")
    print(f"  Interactive hotspot sprites: {total_hotspots}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_sprite_data.py <alfred.1> [output_dir] [--format json|txt|py|png|all]")
        print("\nExamples:")
        print("  python extract_sprite_data.py ALFRED.1")
        print("  python extract_sprite_data.py ALFRED.1 sprites/")
        print("  python extract_sprite_data.py ALFRED.1 sprites/ --format json")
        print("  python extract_sprite_data.py ALFRED.1 sprites/ --format png")
        print("\nOutput formats:")
        print("  json - Sprite metadata as JSON")
        print("  py   - Sprite metadata as Python module")
        print("  txt  - Human-readable text summary")
        print("  png  - Sprite sheet images (requires PIL/Pillow)")
        print("  all  - All formats (default)")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = "sprites" if len(sys.argv) < 3 else sys.argv[2]

    # Parse format argument
    output_format = "all"
    if len(sys.argv) >= 4 and sys.argv[-2] == "--format":
        output_format = sys.argv[-1]
    elif len(sys.argv) >= 3 and sys.argv[-1].startswith("--format="):
        output_format = sys.argv[-1].split("=")[1]

    if output_format not in ['json', 'txt', 'py', 'png', 'all']:
        print(f"Error: Invalid format '{output_format}'. Must be json, txt, py, png, or all")
        sys.exit(1)

    if output_format in ['png', 'all'] and not PIL_AVAILABLE:
        print("Warning: PIL/Pillow not installed. Sprite sheets will not be generated.")
        print("Install with: pip install Pillow")
        if output_format == 'png':
            sys.exit(1)

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    print("Alfred Pelrock - Comprehensive Sprite/Animation Extractor")
    print("=" * 70)
    print(f"Source: {alfred1_path}")
    print(f"Output: {output_dir}/")
    print(f"Format: {output_format}")
    print()

    # Extract sprite metadata
    print("Extracting sprite metadata from Pair 10...")
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    rooms_data = []
    for room_num in range(56):
        sprites = extract_sprites_from_room(data, room_num)
        if sprites:
            rooms_data.append({
                'room': room_num,
                'sprites': sprites
            })

    print_summary(rooms_data)

    # Write metadata files
    if output_format in ['json', 'txt', 'py', 'all']:
        print("\nWriting metadata files:")
        print("-" * 70)
        writer = SpriteDataWriter(output_dir)

        if output_format in ['json', 'all']:
            writer.write_json(rooms_data)

        if output_format in ['py', 'all']:
            writer.write_python(rooms_data)

        if output_format in ['txt', 'all']:
            writer.write_text(rooms_data)

    # Generate sprite sheets
    if output_format in ['png', 'all'] and PIL_AVAILABLE:
        print("\nGenerating sprite sheets from Pair 8:")
        print("-" * 70)

        output_path = Path(output_dir) / "sprite_sheets"
        total_sheets = 0

        for room_num in range(56):
            extracted = generate_sprite_sheet(data, room_num, output_path)
            if extracted > 0:
                print(f"  Room {room_num:2d}: {extracted} sprite sheet(s)")
                total_sheets += extracted

        print(f"  Total sprite sheets: {total_sheets}")

    print("=" * 70)
    print(f"Extraction complete! Output saved to: {Path(output_dir).absolute()}")
    print("=" * 70)


if __name__ == "__main__":
    main()
