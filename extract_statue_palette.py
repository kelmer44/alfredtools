#!/usr/bin/env python3
"""
Extract statue palette fade data from JUEGO.EXE at offset 0x4C700
"""

import struct
import sys

def extract_statue_palette():
    exe_path = "files/JUEGO.EXE"
    file_offset = 0x4C700  # From documentation
    
    try:
        with open(exe_path, 'rb') as f:
            f.seek(file_offset)
            
            # Read the structure
            x_pos = struct.unpack('<H', f.read(2))[0]
            y_pos = struct.unpack('<H', f.read(2))[0]
            type_val = struct.unpack('<H', f.read(2))[0]
            padding = struct.unpack('<H', f.read(2))[0]
            
            print(f"Position: ({x_pos}, {y_pos})")
            print(f"Type: {type_val}")
            print(f"Padding: {padding:#x}")
            print()
            
            # Read palette indices (16 bytes)
            indices = list(f.read(16))
            print(f"Palette indices ({len(indices)}):")
            print(f"  {indices}")
            print()
            
            # Read source RGB values (16 colors × 3 bytes)
            source_colors = []
            print("Source colors (6-bit VGA):")
            for i in range(16):
                r, g, b = struct.unpack('BBB', f.read(3))
                source_colors.append((r, g, b))
                print(f"  Index {indices[i]:3d}: ({r:2d}, {g:2d}, {b:2d})")
            print()
            
            # Read target RGB values (16 colors × 3 bytes)
            target_colors = []
            print("Target colors (6-bit VGA):")
            for i in range(16):
                r, g, b = struct.unpack('BBB', f.read(3))
                target_colors.append((r, g, b))
                print(f"  Index {indices[i]:3d}: ({r:2d}, {g:2d}, {b:2d})")
            print()
            
            # Generate C++ code
            print("=" * 70)
            print("C++ Code for ScummVM:")
            print("=" * 70)
            print()
            print("// Palette indices to modify")
            print("static const byte kStatuePaletteIndices[] = {")
            print(f"    {', '.join(str(idx) for idx in indices)}")
            print("};")
            print()
            print("// Source colors (6-bit VGA)")
            print("static const byte kStatuePaletteSource[][3] = {")
            for r, g, b in source_colors:
                print(f"    {{{r:2d}, {g:2d}, {b:2d}}},")
            print("};")
            print()
            print("// Target colors (6-bit VGA)")
            print("static const byte kStatuePaletteTarget[][3] = {")
            for r, g, b in target_colors:
                print(f"    {{{r:2d}, {g:2d}, {b:2d}}},")
            print("};")
            
    except FileNotFoundError:
        print(f"Error: Could not find {exe_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    extract_statue_palette()
