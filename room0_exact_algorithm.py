#!/usr/bin/env python3
"""
Room 0 Palette Cycling - Exact Game Algorithm

This implements the actual game algorithm for MODE 6 (ROTATE).
Uses 6-bit CLUT colors (0-63) exactly as the game does, not 8-bit RGB.

Config at 0x4B88C:
  c8 06 00 5a e0 04 00 04 67 07 00 01

  Byte 0: palette_start_index = 200 (0xC8)
  Byte 1: count = 6 (rotate 6 consecutive palette entries)
  Byte 2: unknown = 0x00 (possibly current rotation position)
  Byte 3: delay = 90 (0x5A) frames between rotations (~5 seconds at 18 FPS)
  Bytes 4-10: unknown (may store color data or state)
  Byte 11: flags = 0x01
"""

class PaletteCyclingMode6:
    """
    Implements MODE 6 (ROTATE) palette cycling exactly as the game does.
    
    The game algorithm for rotation mode:
    1. Each frame, decrement the delay counter
    2. When counter reaches 0:
       - Save the RGB values of all N palette entries
       - Rotate them: entry[i] = saved[i+1], entry[N-1] = saved[0]
       - Write all rotated values to VGA
       - Reset delay counter
    3. The visual effect is that colors shift through the palette indices,
       making pixels appear to change color even though pixel data is static
    """
    
    def __init__(self, config_bytes, initial_palette):
        """
        Initialize from 12-byte config and initial palette.
        
        Args:
            config_bytes: 12-byte config from JUEGO.EXE
            initial_palette: Full 256-entry palette (768 bytes, 6-bit RGB values)
        """
        self.palette_start = config_bytes[0]
        self.count = config_bytes[1]  # Number of palette entries to rotate
        self.delay_frames = config_bytes[3]
        self.flags = config_bytes[11]
        
        # Frame counter
        self.current_delay = 0  # Start immediately for demo purposes
        
        # Extract the rotating colors from initial palette (6-bit values)
        self.colors = []
        for i in range(self.count):
            idx = self.palette_start + i
            # Palette is 6-bit, stored as-is
            r = initial_palette[idx * 3]
            g = initial_palette[idx * 3 + 1]
            b = initial_palette[idx * 3 + 2]
            self.colors.append((r, g, b))
    
    def update(self):
        """
        Update palette for one frame.
        Returns True if rotation happened this frame, False if still waiting.
        """
        self.current_delay += 1
        
        if self.current_delay >= self.delay_frames:
            # Time to rotate!
            self.current_delay = 0
            
            # Rotate the colors: shift all forward, wrap last to first
            # colors[0] gets colors[1], colors[1] gets colors[2], ..., colors[N-1] gets colors[0]
            rotated = self.colors[1:] + [self.colors[0]]
            self.colors = rotated
            
            return True
        
        return False
    
    def get_current_palette_entries(self):
        """
        Get current palette entries (6-bit CLUT format).
        Returns list of (index, r, g, b) tuples.
        """
        entries = []
        for i, (r, g, b) in enumerate(self.colors):
            palette_idx = self.palette_start + i
            entries.append((palette_idx, r, g, b))
        return entries
    
    def get_current_8bit(self):
        """
        Get current palette entries in 8-bit RGB format.
        Returns list of (index, r, g, b) tuples.
        """
        entries = []
        for i, (r, g, b) in enumerate(self.colors):
            palette_idx = self.palette_start + i
            entries.append((palette_idx, r*4, g*4, b*4))
        return entries


def main():
    """Demonstrate the exact game algorithm for Room 0"""
    import struct
    
    # Load Room 0 config from JUEGO.EXE
    with open('files/JUEGO.EXE', 'rb') as f:
        f.seek(0x4B88C)
        config_bytes = f.read(12)
    
    print("Room 0 - City Lights Palette Cycling")
    print("=" * 60)
    print()
    print("Config bytes:", ' '.join(f'{b:02x}' for b in config_bytes))
    print()
    
    # Load initial palette from Room 0 in ALFRED.1
    with open('files/ALFRED.1', 'rb') as f:
        room_offset = 0 * 104  # Room 0
        pair_11_offset = room_offset + (11 * 8)
        f.seek(pair_11_offset)
        palette_offset = struct.unpack('<I', f.read(4))[0]
        palette_size = struct.unpack('<I', f.read(4))[0]
        
        f.seek(palette_offset)
        palette_6bit = list(f.read(768))  # 256 * 3 bytes, already in 6-bit format
    
    # Create cycling engine
    cycling = PaletteCyclingMode6(config_bytes, palette_6bit)
    
    print(f"Palette start index: {cycling.palette_start}")
    print(f"Count: {cycling.count} (rotate {cycling.count} consecutive entries)")
    print(f"Delay: {cycling.delay_frames} frames (~{cycling.delay_frames/18:.1f} seconds at 18 FPS)")
    print(f"Flags: 0x{cycling.flags:02X}")
    print()
    
    print("Initial palette entries (6-bit CLUT):")
    for idx, r, g, b in cycling.get_current_palette_entries():
        print(f"  Index {idx}: ({r:2d}, {g:2d}, {b:2d}) = RGB({r*4:3d}, {g*4:3d}, {b*4:3d}) in 8-bit")
    print()
    
    # Simulate frames
    print("=" * 60)
    print("SIMULATING GAME FRAMES")
    print("=" * 60)
    print()
    print(f"Each rotation happens every {cycling.delay_frames} frames")
    print()
    
    rotation_count = 0
    for frame in range(cycling.delay_frames * 7):  # Show ~7 rotations
        rotated = cycling.update()
        
        if rotated:
            rotation_count += 1
            print(f"Frame {frame:4d}: ROTATION #{rotation_count}")
            print("  Updated palette entries (6-bit):")
            for idx, r, g, b in cycling.get_current_palette_entries():
                print(f"    Index {idx}: ({r:2d}, {g:2d}, {b:2d})")
            print()
    
    print("=" * 60)
    print("ALGORITHM SUMMARY")
    print("=" * 60)
    print()
    print("What the game does every frame:")
    print("  1. Increment delay counter")
    print(f"  2. If counter >= {cycling.delay_frames}:")
    print("     a. Save current RGB values of all N palette entries")
    print("     b. Rotate: entry[i] = saved[(i+1) % N]")
    print("     c. For each rotated entry:")
    print("        - OUT 0x3C8, palette_index")
    print("        - OUT 0x3C9, r (6-bit)")
    print("        - OUT 0x3C9, g (6-bit)")
    print("        - OUT 0x3C9, b (6-bit)")
    print("     d. Reset counter to 0")
    print()
    print("Visual effect:")
    print("  - Building windows drawn with palette indices 200-205")
    print("  - Each index has a different brightness (dark to bright)")
    print("  - By rotating the colors, windows appear to turn on/off")
    print("  - Pixels don't change, only the palette colors shift")
    print()
    print("Example rotation sequence:")
    print("  Initial: idx[200]=color_0, idx[201]=color_1, ..., idx[205]=color_5")
    print("  After 1: idx[200]=color_1, idx[201]=color_2, ..., idx[205]=color_0")
    print("  After 2: idx[200]=color_2, idx[201]=color_3, ..., idx[205]=color_1")
    print(f"  After {cycling.count}: back to initial (full cycle)")


if __name__ == '__main__':
    main()
