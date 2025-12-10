#!/usr/bin/env python3
"""
Room 2 Palette Cycling - Exact Game Algorithm

This implements the actual game algorithm as found in JUEGO.EXE at 0x00016804.
Uses 6-bit CLUT colors (0-63) exactly as the game does, not 8-bit RGB.

Config at 0x4B860:
  fa 01 24 2c 08 0c 14 08 24 2c 08 05

  Byte 0: palette_index = 250 (0xFA)
  Byte 1: mode = 1 (FADE)
  Bytes 2-4: current_rgb = (36, 44, 8) in 6-bit
  Bytes 5-7: min_rgb = (12, 20, 8) in 6-bit
  Bytes 8-10: max_rgb = (36, 44, 8) in 6-bit
  Byte 11: flags = 0x05
    - Bit 6 (0x40): direction (0 = incrementing toward max, 1 = decrementing toward min)
    - Bits 0-5: step value (0x05 = increment/decrement by 5 each frame)
"""

class PaletteCyclingMode1:
    """
    Implements MODE 1 (FADE) palette cycling exactly as the game does.

    The game algorithm (from Ghidra decompilation):
    1. Check bit 6 of flags to determine direction
    2. If direction = 0 (incrementing):
       - Add step value (lower 5 bits of flags) to each RGB component
       - If any component >= max, clamp to max and flip direction bit
    3. If direction = 1 (decrementing):
       - Subtract step value from each RGB component
       - If any component <= min, clamp to min and flip direction bit
    4. Write to VGA: OUT 0x3C8 (index), then OUT 0x3C9 (R,G,B in 6-bit)
    """

    def __init__(self, config_bytes):
        """Initialize from 12-byte config"""
        self.palette_index = config_bytes[0]
        self.mode = config_bytes[1]

        # Current RGB (6-bit CLUT)
        self.current_r = config_bytes[2]
        self.current_g = config_bytes[3]
        self.current_b = config_bytes[4]

        # Min RGB (6-bit CLUT)
        self.min_r = config_bytes[5]
        self.min_g = config_bytes[6]
        self.min_b = config_bytes[7]

        # Max RGB (6-bit CLUT)
        self.max_r = config_bytes[8]
        self.max_g = config_bytes[9]
        self.max_b = config_bytes[10]

        # Flags
        self.flags = config_bytes[11]
        self.step = self.flags & 0x3F  # Lower 6 bits
        self.direction_down = bool(self.flags & 0x40)  # Bit 6

    def update(self):
        """
        Update palette for one frame - this is what the game calls each frame.
        Returns the new 6-bit RGB values.
        """
        if self.direction_down:
            # Decrementing toward min
            new_r = max(self.min_r, self.current_r - self.step)
            new_g = max(self.min_g, self.current_g - self.step)
            new_b = max(self.min_b, self.current_b - self.step)

            # Check if we hit minimum
            if new_r == self.min_r and new_g == self.min_g and new_b == self.min_b:
                self.direction_down = False  # Start incrementing

        else:
            # Incrementing toward max
            new_r = min(self.max_r, self.current_r + self.step)
            new_g = min(self.max_g, self.current_g + self.step)
            new_b = min(self.max_b, self.current_b + self.step)

            # Check if we hit maximum
            if new_r == self.max_r and new_g == self.max_g and new_b == self.max_b:
                self.direction_down = True  # Start decrementing

        self.current_r = new_r
        self.current_g = new_g
        self.current_b = new_b

        return (self.current_r, self.current_g, self.current_b)

    def get_current_6bit(self):
        """Get current color in 6-bit CLUT format (0-63)"""
        return (self.current_r, self.current_g, self.current_b)

    def get_current_8bit(self):
        """Convert current 6-bit to 8-bit RGB (multiply by 4)"""
        return (self.current_r * 4, self.current_g * 4, self.current_b * 4)


def main():
    """Demonstrate the exact game algorithm"""
    import struct

    # Load Room 2 config from JUEGO.EXE
    with open('files/JUEGO.EXE', 'rb') as f:
        f.seek(0x4B860)
        config_bytes = f.read(12)

    print("Room 2 - McDowells Sign Palette Cycling")
    print("=" * 60)
    print()
    print("Config bytes:", ' '.join(f'{b:02x}' for b in config_bytes))
    print()

    # Create cycling engine
    cycling = PaletteCyclingMode1(config_bytes)

    print(f"Palette index: {cycling.palette_index}")
    print(f"Mode: {cycling.mode} (FADE)")
    print(f"Step value: {cycling.step} (increment/decrement per frame)")
    print(f"Initial direction: {'DOWN (toward min)' if cycling.direction_down else 'UP (toward max)'}")
    print()
    print(f"Min RGB (6-bit): ({cycling.min_r}, {cycling.min_g}, {cycling.min_b})")
    print(f"Max RGB (6-bit): ({cycling.max_r}, {cycling.max_g}, {cycling.max_b})")
    print(f"Current RGB (6-bit): ({cycling.current_r}, {cycling.current_g}, {cycling.current_b})")
    print()
    print("8-bit equivalents (multiply by 4):")
    print(f"  Min: ({cycling.min_r*4}, {cycling.min_g*4}, {cycling.min_b*4})")
    print(f"  Max: ({cycling.max_r*4}, {cycling.max_g*4}, {cycling.max_b*4})")
    print(f"  Current: ({cycling.current_r*4}, {cycling.current_g*4}, {cycling.current_b*4})")
    print()

    # Simulate frames
    print("=" * 60)
    print("SIMULATING GAME FRAMES (first 50 frames)")
    print("=" * 60)
    print()
    print("Frame | Dir | 6-bit RGB          | 8-bit RGB")
    print("------|-----|--------------------|-----------------")

    for frame in range(50):
        dir_str = "DN" if cycling.direction_down else "UP"
        rgb6 = cycling.get_current_6bit()
        rgb8 = cycling.get_current_8bit()
        print(f" {frame:4d} | {dir_str}  | ({rgb6[0]:2d}, {rgb6[1]:2d}, {rgb6[2]:2d}) | ({rgb8[0]:3d}, {rgb8[1]:3d}, {rgb8[2]:3d})")

        # Update for next frame (this is what the game does)
        cycling.update()

    print()
    print("=" * 60)
    print("ALGORITHM SUMMARY")
    print("=" * 60)
    print()
    print("What the game does every frame:")
    print("  1. Check direction bit (bit 6 of flags byte)")
    print("  2. If UP: current_rgb += step, clamp to max, flip if reached")
    print("  3. If DOWN: current_rgb -= step, clamp to min, flip if reached")
    print("  4. OUT 0x3C8, palette_index  (select VGA palette entry)")
    print("  5. OUT 0x3C9, r (6-bit)")
    print("  6. OUT 0x3C9, g (6-bit)")
    print("  7. OUT 0x3C9, b (6-bit)")
    print()
    print("The VGA hardware converts 6-bit (0-63) to analog voltages.")
    print("Modern displays show this as 8-bit (multiply by 4).")


if __name__ == '__main__':
    main()
