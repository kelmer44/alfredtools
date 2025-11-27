#!/usr/bin/env python3
"""
Alfred Pelrock - Character Scaling Calculator

Generic script to calculate character scaling for any room at any Y position.

Scaling Formula (from load_room_data at offset ~0x15570):
  if (y_threshold < player_y):
      scale_down = 0
      scale_up = 0
  else:
      scale_delta = (y_threshold - player_y) / scale_divisor
      scale_down = scale_delta
      scale_up = scale_delta / 2

  final_height = original_height - scale_down + scale_up

The scale values are used by render_character_sprite_scaled() to adjust
the character sprite during rendering.
"""

import struct
import sys
from pathlib import Path

def load_scaling_params(alfred1_path, room_num):
    """Load scaling parameters for a specific room from ALFRED.1"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    # Room structure at offset room_num * 104
    room_offset = room_num * 104

    # Pair 10 contains scaling parameters
    pair10_offset = room_offset + (10 * 8)
    offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
    size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

    if size == 0 or offset >= len(data):
        return None

    # Scaling parameters at offset 0x214 in Pair 10
    scale_offset = offset + 0x214

    if scale_offset + 4 > len(data):
        return None

    y_threshold = struct.unpack('<H', data[scale_offset:scale_offset+2])[0]
    scale_divisor = data[scale_offset + 2]
    scale_mode = struct.unpack('<b', data[scale_offset+3:scale_offset+4])[0]

    return {
        'y_threshold': y_threshold,
        'scale_divisor': scale_divisor,
        'scale_mode': scale_mode
    }

def calculate_character_scale(y_pos, y_threshold, scale_divisor, scale_mode):
    """
    Calculate character scaling for a given Y position.

    Args:
        y_pos: Player Y coordinate (0-399)
        y_threshold: Y coordinate where scaling begins
        scale_divisor: Controls rate of scaling
        scale_mode: Scaling mode (0=normal, -1=max, -2=none)

    Returns:
        (scale_down, scale_up, final_height, final_width) tuple
    """
    original_height = 102
    original_width = 51

    # Special scale modes
    if scale_mode == -1:  # 0xFF - maximum scaling
        scale_down = 0x5e
        scale_up = 0x2f
    elif scale_mode == -2:  # 0xFE - no scaling
        scale_down = 0
        scale_up = 0
    elif scale_mode == 0:  # Normal scaling
        if y_threshold < y_pos:
            # Below threshold: no scaling
            scale_down = 0
            scale_up = 0
        else:
            # Above threshold: apply scaling
            if scale_divisor == 0:
                scale_down = 0
                scale_up = 0
            else:
                scale_delta = (y_threshold - y_pos) // scale_divisor
                scale_down = scale_delta
                scale_up = scale_delta // 2
    else:
        # Unknown mode
        scale_down = 0
        scale_up = 0

    # Calculate final dimensions
    final_height = original_height - scale_down + scale_up
    if final_height <= 0:
        final_height = 1

    # Maintain aspect ratio
    final_width = int(original_width * (final_height / original_height))
    if final_width <= 0:
        final_width = 1

    return scale_down, scale_up, final_height, final_width

def print_room_scaling_info(alfred1_path, room_num):
    """Print scaling information for a room"""
    params = load_scaling_params(alfred1_path, room_num)

    if not params:
        print(f"Room {room_num}: No scaling data available")
        return

    print(f"Room {room_num} Scaling Parameters:")
    print(f"  Y Threshold: {params['y_threshold']}")
    print(f"  Scale Divisor: {params['scale_divisor']}")
    print(f"  Scale Mode: 0x{params['scale_mode'] & 0xFF:02X}")

    if params['scale_mode'] == -1:
        print(f"  Mode: Maximum scaling (always large)")
    elif params['scale_mode'] == -2:
        print(f"  Mode: No scaling (always normal size)")
    elif params['scale_mode'] == 0:
        print(f"  Mode: Normal scaling (varies with Y position)")

    print()

    # Show example positions
    if params['scale_mode'] == 0:
        print("Example Y positions:")
        print("  Y    | scale_down | scale_up | Final Size | Description")
        print("  -----|------------|----------|------------|------------------")

        test_positions = [
            (0, "Top of screen"),
            (100, "Upper area"),
            (200, "Mid-upper"),
            (params['y_threshold'], "At threshold"),
            (params['y_threshold'] + 20, "Below threshold"),
            (399, "Bottom of screen")
        ]

        for y_pos, desc in test_positions:
            scale_down, scale_up, final_h, final_w = calculate_character_scale(
                y_pos, params['y_threshold'], params['scale_divisor'], params['scale_mode']
            )
            print(f"  {y_pos:3d}  |    {scale_down:3d}     |   {scale_up:3d}    | "
                  f"{final_w:2d}x{final_h:3d}    | {desc}")

    print()

def calculate_for_position(alfred1_path, room_num, y_pos):
    """Calculate scaling for a specific position"""
    params = load_scaling_params(alfred1_path, room_num)

    if not params:
        print(f"Error: Could not load scaling data for room {room_num}")
        return None

    scale_down, scale_up, final_h, final_w = calculate_character_scale(
        y_pos, params['y_threshold'], params['scale_divisor'], params['scale_mode']
    )

    return {
        'y_pos': y_pos,
        'scale_down': scale_down,
        'scale_up': scale_up,
        'final_width': final_w,
        'final_height': final_h,
        'original_width': 51,
        'original_height': 102
    }

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nUsage:")
        print("  python calculate_character_scale.py <alfred.1> <room_num>")
        print("  python calculate_character_scale.py <alfred.1> <room_num> <y_pos>")
        print()
        print("Examples:")
        print("  python calculate_character_scale.py ALFRED.1 6")
        print("  python calculate_character_scale.py ALFRED.1 6 100")
        print("  python calculate_character_scale.py ALFRED.1 6 394")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    room_num = int(sys.argv[2])

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    if room_num < 0 or room_num > 55:
        print(f"Error: Room number must be 0-55")
        sys.exit(1)

    if len(sys.argv) >= 4:
        # Calculate for specific position
        y_pos = int(sys.argv[3])

        if y_pos < 0 or y_pos > 399:
            print(f"Error: Y position must be 0-399")
            sys.exit(1)

        result = calculate_for_position(alfred1_path, room_num, y_pos)

        if result:
            print(f"Room {room_num}, Y position {y_pos}:")
            print(f"  scale_down: {result['scale_down']}")
            print(f"  scale_up: {result['scale_up']}")
            print(f"  Original size: {result['original_width']}x{result['original_height']}")
            print(f"  Final size: {result['final_width']}x{result['final_height']}")

            if result['final_height'] < result['original_height']:
                percent = ((result['original_height'] - result['final_height']) /
                          result['original_height'] * 100)
                print(f"  Character is {percent:.1f}% smaller")
            elif result['final_height'] > result['original_height']:
                percent = ((result['final_height'] - result['original_height']) /
                          result['original_height'] * 100)
                print(f"  Character is {percent:.1f}% larger")
            else:
                print(f"  Character is normal size (no scaling)")
    else:
        # Print room info
        print_room_scaling_info(alfred1_path, room_num)

if __name__ == "__main__":
    main()
