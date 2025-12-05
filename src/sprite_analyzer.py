#!/usr/bin/env python3
"""
Sprite structure analyzer for ALFRED.1

Parses the 44-byte sprite structures from Pair 10 (sprite metadata).

File layout (44 bytes per sprite, after 98-byte header):
  0x00-01: X position (int16)
  0x02-03: Y position (int16)
  0x04:    Width (uint8)
  0x05:    Height (uint8)
  0x06-07: Stride (width * height) - overwritten at runtime with pixel pointer
  0x08:    Number of animation sequences (uint8)
  0x09:    Current sequence index (uint8)
  0x0A-0D: Frames per sequence [4] (uint8 each)
  0x0E-11: Loop counts [4] (uint8 each, 0xFF = no loop)
  0x12-15: Frame periods [4] (uint8 each, ticks per frame at 18.2 Hz)
  0x16:    Unknown
  0x17:    Z-depth (uint8) - render order AND visibility flag:
              0xFF (255) = HIDDEN - sprite not rendered, must be enabled by script
              Other values = visible, lower values render behind higher values
  0x18-1F: Movement flags [4] (uint16 each, one per sequence)
  0x20:    Current frame index (uint8)
  0x21:    Sprite type (uint8)
  0x22:    Action flags (uint8)
  0x23-25: Unknown
  0x26:    Is hotspot (uint8, 0x00 = clickable)
  0x27-2B: Unknown/reserved

Movement flags bitfield (16-bit):
  Bits 0-2:   X movement amount (0-7 pixels per frame)
  Bit 3:      X direction (0=left/subtract, 1=right/add)
  Bit 4:      X movement enable
  Bits 5-7:   Y movement amount (0-7 pixels per frame)
  Bit 8:      Y direction (0=up/subtract, 1=down/add)
  Bit 9:      Y movement enable
  Bits 10-12: Z movement amount
  Bit 13:     Z direction (0=back/subtract, 1=forward/add)
  Bit 14:     Z movement enable

Note: File offsets differ from runtime by +0x0A (runtime +0x0A = file 0x00).
"""

import sys
import struct

SPRITE_SIZE = 44
HEADER_SIZE = 98


def read_room_directory(f, room_num):
    """Read the room directory entry (104 bytes, 12 pairs of offset/size)."""
    f.seek(room_num * 104)
    room_data = f.read(104)

    pairs = []
    for i in range(12):
        offset = struct.unpack('<I', room_data[i*8:i*8+4])[0]
        size = struct.unpack('<I', room_data[i*8+4:i*8+8])[0]
        pairs.append((offset, size))

    return pairs


def decode_movement_flags(flags):
    """Decode 16-bit movement flags into human-readable components."""
    result = []

    # X movement
    if flags & 0x10:
        amount = flags & 0x07
        direction = "right" if flags & 0x08 else "left"
        result.append(f"X: {direction} {amount}px")

    # Y movement
    if flags & 0x200:
        amount = (flags >> 5) & 0x07
        direction = "down" if flags & 0x100 else "up"
        result.append(f"Y: {direction} {amount}px")

    # Z movement
    if flags & 0x4000:
        amount = (flags >> 10) & 0x07
        direction = "forward" if flags & 0x2000 else "back"
        result.append(f"Z: {direction} {amount}")

    return ", ".join(result) if result else "none"


def parse_sprite(data, file_offset):
    """Parse a 44-byte sprite structure."""
    if len(data) < SPRITE_SIZE:
        return None

    x = struct.unpack('<h', data[0:2])[0]
    y = struct.unpack('<h', data[2:4])[0]
    width = data[4]
    height = data[5]
    stride = struct.unpack('<H', data[6:8])[0]
    num_sequences = data[8]
    current_sequence = data[9]
    frames_per_seq = list(data[0x0A:0x0E])
    loop_counts = list(data[0x0E:0x12])
    frame_periods = list(data[0x12:0x16])
    z_depth = data[0x17]

    movement_flags = [
        struct.unpack('<H', data[0x18:0x1A])[0],
        struct.unpack('<H', data[0x1A:0x1C])[0],
        struct.unpack('<H', data[0x1C:0x1E])[0],
        struct.unpack('<H', data[0x1E:0x20])[0]
    ]

    current_frame = data[0x20]
    sprite_type = data[0x21]
    action_flags = data[0x22]
    is_hotspot = data[0x26]

    return {
        'file_offset': file_offset,
        'x': x,
        'y': y,
        'width': width,
        'height': height,
        'stride': stride,
        'num_sequences': num_sequences,
        'current_sequence': current_sequence,
        'frames_per_seq': frames_per_seq,
        'loop_counts': loop_counts,
        'frame_periods': frame_periods,
        'z_depth': z_depth,
        'movement_flags': movement_flags,
        'current_frame': current_frame,
        'sprite_type': sprite_type,
        'action_flags': action_flags,
        'is_hotspot': is_hotspot,
        'raw': data.hex()
    }


def analyze_room(filename, room_num):
    """Analyze all sprites in a room."""
    with open(filename, 'rb') as f:
        pairs = read_room_directory(f, room_num)
        metadata_offset, metadata_size = pairs[10]

        if metadata_size == 0:
            return None, []

        f.seek(metadata_offset)
        metadata = f.read(metadata_size)

        # Sprite count is at byte 5, actual count = value - 2
        sprite_count = metadata[5] - 2

        sprites = []
        for i in range(sprite_count):
            offset = HEADER_SIZE + (i * SPRITE_SIZE)
            file_offset = metadata_offset + offset
            sprite_data = metadata[offset:offset + SPRITE_SIZE]
            sprite = parse_sprite(sprite_data, file_offset)
            if sprite:
                sprites.append(sprite)

        return metadata_offset, sprites


def format_output(room_num, metadata_offset, sprites):
    """Format sprite analysis as text output."""
    lines = []
    lines.append(f"═══ ROOM {room_num} SPRITE ANALYSIS ═══\n")
    lines.append(f"Metadata offset: 0x{metadata_offset:08X}\n")
    lines.append(f"Sprite count: {len(sprites)}\n\n")

    for i, s in enumerate(sprites):
        # Check if sprite is hidden (z_depth = 0xFF)
        hidden_marker = " [HIDDEN]" if s['z_depth'] == 255 else ""
        lines.append(f"┌─ SPRITE {i} at 0x{s['file_offset']:08X}{hidden_marker} ─────────────────────────────┐\n")
        lines.append(f"│ Position: ({s['x']:4d}, {s['y']:4d})  Size: {s['width']:3d}×{s['height']:3d}\n")
        z_info = "HIDDEN (must be enabled by script)" if s['z_depth'] == 255 else str(s['z_depth'])
        lines.append(f"│ Z-depth: {z_info}\n")
        lines.append(f"│\n")
        lines.append(f"│ Sequences: {s['num_sequences']}  Current: {s['current_sequence']}\n")
        lines.append(f"│ Frames/seq: {s['frames_per_seq']}\n")
        lines.append(f"│ Loop counts: {s['loop_counts']}\n")
        lines.append(f"│ Frame periods: {s['frame_periods']} ticks\n")
        lines.append(f"│\n")

        # Movement flags
        for seq_idx, flags in enumerate(s['movement_flags']):
            if flags != 0:
                decoded = decode_movement_flags(flags)
                lines.append(f"│ Movement seq {seq_idx}: 0x{flags:04X} ({decoded})\n")

        lines.append(f"│\n")
        lines.append(f"│ Hotspot: {'yes' if s['is_hotspot'] == 0 else 'no'}\n")
        lines.append(f"│ Sprite type: {s['sprite_type']}  Action flags: 0x{s['action_flags']:02X}\n")
        lines.append(f"└────────────────────────────────────────────────────────┘\n\n")

        # Hex dump
        lines.append("Hex dump:\n")
        raw = s['raw']
        for j in range(0, len(raw), 32):
            row_offset = j // 2
            hex_part = raw[j:j+32]
            spaced = ' '.join([hex_part[k:k+2] for k in range(0, len(hex_part), 2)])
            lines.append(f"  0x{row_offset:02X}: {spaced}\n")
        lines.append("\n")

    return ''.join(lines)


def main():
    if len(sys.argv) < 3:
        print("Usage: python sprite_analyzer.py <ALFRED.1> <room#> [output.txt]")
        print("\nAnalyzes sprite structures from ALFRED.1 Pair 10 metadata.")
        sys.exit(1)

    filename = sys.argv[1]
    room_num = int(sys.argv[2])
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    metadata_offset, sprites = analyze_room(filename, room_num)

    if metadata_offset is None:
        print(f"No sprite metadata for room {room_num}")
        sys.exit(1)

    output = format_output(room_num, metadata_offset, sprites)
    print(output)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(output)
        print(f"✓ Written to {output_file}")


if __name__ == '__main__':
    main()
