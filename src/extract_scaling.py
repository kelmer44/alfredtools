#!/usr/bin/env python3
"""
Alfred Pelrock - Character Scaling Extractor

Extracts character scaling parameters from ALFRED.1.

The character scales based on Y position to create depth perspective.
Scaling data is stored in Pair 10 at offset 0x214-0x217:
  +0x214-0x215: y_threshold (uint16 LE) - Y coordinate for scaling reference
  +0x216:       scale_divisor (uint8) - Divisor for scaling calculation
  +0x217:       scale_mode (int8) - Scaling mode:
                  0x00 = Normal scaling (character scales with depth)
                  0xFF = Maximum scaling (character always at max size)
                  0xFE = No scaling (character always at min size)

Scaling formula (from load_room_data at offset ~0x15570):
  If scale_mode == 0:
    If y_threshold < player_y:
      scale_down = 0
      scale_up = 0
    Else:
      scale_delta = (y_threshold - player_y) / scale_divisor
      scale_down = scale_delta
      scale_up = scale_delta / 2

  If scale_mode == 0xFF:
    scale_down = 0x5E (94)
    scale_up = 0x2F (47)

  If scale_mode == 0xFE:
    scale_down = 0
    scale_up = 0

Final character size:
  final_height = original_height - scale_down + scale_up

The scale values are used by render_character_sprite_scaled() to adjust
the character sprite during rendering. Characters are SMALLER when further
back (lower Y values) and NORMAL SIZE in the foreground (higher Y values).
"""

import struct
import sys
from pathlib import Path
import json

def extract_scaling_for_room(data, room_num):
    """Extract scaling parameters for a specific room"""
    room_offset = room_num * 104
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
    scale_mode = struct.unpack('<b', data[scale_offset+3:scale_offset+4])[0]  # signed byte

    return {
        'y_threshold': y_threshold,
        'scale_divisor': scale_divisor,
        'scale_mode': scale_mode,
        'mode_description': get_scale_mode_description(scale_mode)
    }

def get_scale_mode_description(mode):
    """Get human-readable description of scale mode"""
    if mode == 0:
        return "Normal scaling (character scales with depth)"
    elif mode == -1:  # 0xFF
        return "Maximum scaling (character always at max size)"
    elif mode == -2:  # 0xFE
        return "No scaling (character always at min size)"
    else:
        return f"Unknown mode (0x{mode & 0xFF:02X})"

def calculate_scale_values(y_pos, y_threshold, scale_divisor, scale_mode):
    """Calculate scale_down and scale_up values for a given Y position"""
    if scale_mode == -1:  # 0xFF
        return 0x5E, 0x2F
    elif scale_mode == -2:  # 0xFE
        return 0, 0
    elif scale_mode == 0:
        if y_threshold < y_pos:
            return 0, 0
        else:
            if scale_divisor == 0:
                return 0, 0
            scale_delta = (y_threshold - y_pos) // scale_divisor
            scale_down = scale_delta
            scale_up = scale_delta // 2
            return scale_down, scale_up
    else:
        return 0, 0

def extract_all_scaling(alfred1_path, output_dir=None):
    """Extract scaling parameters from all rooms"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - Character Scaling Extractor")
    print("=" * 70)
    print()

    NUM_ROOMS = 56
    all_rooms = []

    for room_num in range(NUM_ROOMS):
        scaling = extract_scaling_for_room(data, room_num)

        if scaling:
            all_rooms.append({
                'room': room_num,
                'scaling': scaling
            })

            print(f"Room {room_num:2d}: Y={scaling['y_threshold']:3d} "
                  f"divisor={scaling['scale_divisor']:2d} "
                  f"mode=0x{scaling['scale_mode'] & 0xFF:02X} "
                  f"({scaling['mode_description']})")

            # Show some example scaling values
            if scaling['scale_mode'] == 0 and scaling['scale_divisor'] > 0:
                print(f"         Examples:")
                test_y_values = [
                    scaling['y_threshold'],
                    scaling['y_threshold'] + scaling['scale_divisor'] * 2,
                    scaling['y_threshold'] + scaling['scale_divisor'] * 5,
                    399  # Bottom of screen
                ]
                for y in test_y_values:
                    if y <= 399:
                        down, up = calculate_scale_values(
                            y, scaling['y_threshold'],
                            scaling['scale_divisor'], scaling['scale_mode']
                        )
                        print(f"           Y={y:3d} â†' scale_down={down:2d} scale_up={up:2d}")
        else:
            print(f"Room {room_num:2d}: No scaling data")

    print()
    print("=" * 70)
    print(f"Total: {len(all_rooms)} rooms with scaling parameters")

    # Save to files if output directory specified
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save as JSON
        json_file = output_path / "scaling.json"
        with open(json_file, 'w') as f:
            json.dump({
                'description': 'Alfred Pelrock character scaling parameters',
                'note': 'Character scales based on Y position for depth perspective',
                'formula': 'scale_delta = (player_y - y_threshold) / scale_divisor',
                'rooms': all_rooms
            }, f, indent=2)

        print(f"Saved to: {json_file}")

        # Save as Python
        py_file = output_path / "scaling.py"
        with open(py_file, 'w') as f:
            f.write("# Alfred Pelrock - Character Scaling Parameters\n\n")
            f.write("SCALING = {\n")
            for room_data in all_rooms:
                f.write(f"    {room_data['room']}: {room_data['scaling']},\n")
            f.write("}\n")

        print(f"Saved to: {py_file}")

        # Save as text with explanation
        txt_file = output_path / "scaling.txt"
        with open(txt_file, 'w') as f:
            f.write("Alfred Pelrock - Character Scaling System\n")
            f.write("=" * 70 + "\n\n")

            f.write("HOW IT WORKS:\n")
            f.write("-" * 70 + "\n")
            f.write("The character sprite scales based on Y position to simulate depth.\n")
            f.write("As the character walks 'back' (up the screen), they get smaller.\n")
            f.write("As they walk 'forward' (down the screen), they stay normal size.\n\n")

            f.write("SCALING FORMULA:\n")
            f.write("-" * 70 + "\n")
            f.write("  if (y_threshold < player_y):\n")
            f.write("    scale_down = 0, scale_up = 0  (no scaling)\n")
            f.write("  else:\n")
            f.write("    scale_delta = (y_threshold - player_y) / scale_divisor\n")
            f.write("    scale_down = scale_delta\n")
            f.write("    scale_up = scale_delta / 2\n\n")
            f.write("  final_height = original_height - scale_down + scale_up\n\n")

            f.write("These values are used by the rendering engine to:\n")
            f.write("  - Remove scanlines (scale_down) to shrink the sprite\n")
            f.write("  - Add scanlines (scale_up) to partially restore size\n")
            f.write("  - Net effect: character is smaller when further back\n\n")

            f.write("ROOM DATA:\n")
            f.write("=" * 70 + "\n\n")

            for room_data in all_rooms:
                scaling = room_data['scaling']
                f.write(f"Room {room_data['room']:2d}:\n")
                f.write(f"  Y Threshold: {scaling['y_threshold']}\n")
                f.write(f"  Scale Divisor: {scaling['scale_divisor']}\n")
                f.write(f"  Scale Mode: 0x{scaling['scale_mode'] & 0xFF:02X} - {scaling['mode_description']}\n")

                if scaling['scale_mode'] == 0 and scaling['scale_divisor'] > 0:
                    f.write(f"  Example scaling at Y=399: ")
                    down, up = calculate_scale_values(
                        399, scaling['y_threshold'],
                        scaling['scale_divisor'], scaling['scale_mode']
                    )
                    f.write(f"scale_down={down}, scale_up={up}\n")

                f.write("\n")

        print(f"Saved to: {txt_file}")

    return all_rooms

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_scaling.py <alfred.1> [output_dir]")
        print("\nExample:")
        print("  python extract_scaling.py ALFRED.1 scaling/")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "scaling"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    extract_all_scaling(alfred1_path, output_dir)

if __name__ == "__main__":
    main()
