#!/usr/bin/env python3
"""
Alfred Pelrock Character Scaling Algorithm
==========================================

Reverse-engineered from the original DOS game binary.

The game uses lookup tables for pixel skipping to achieve scaling.
This module generates those tables and implements the exact scaling algorithm.

Key findings from Ghidra analysis:
- init_character_scaling_tables() @ 0x00011e26 generates 4 lookup tables
- render_character_sprite_scaled() @ 0x00016ff8 uses these tables to scale sprites
- Scale parameters (alfred_scale_x, alfred_scale_y) are computed from Y-position in load_room_data()

Memory addresses:
- scale_table_x_51:  0x00053290  (51x51 bytes = 2601 bytes)
- scale_table_y_102: 0x00053cbc  (102x102 bytes = 10404 bytes)
- scale_table_66:    0x00056560  (66x66 bytes = 4356 bytes)
- scale_table_62:    0x00057664  (62x62 bytes = 3844 bytes)

Author: Reverse engineered from JUEGO.EXE
"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass


# =============================================================================
# SCALE TABLE GENERATION (from init_character_scaling_tables @ 0x00011e26)
# =============================================================================

def generate_scale_table_51() -> np.ndarray:
    """
    Generate the 51x51 X-axis scaling table.

    Used for horizontal pixel skipping when scaling Alfred's sprite width.
    Alfred's unscaled width is 51 pixels (0x33).

    Algorithm from disassembly @ 0x00011e93:
        for scale_factor in range(0x33):  # 0 to 50
            step = 51.0 / (scale_factor + 1.0)
            pos = step
            while pos < 51.0:
                table[round(pos)][scale_factor] = 1  # skip this pixel
                pos += step

    Returns:
        51x51 numpy array where table[output_x][scale_factor] = 1 means skip this source pixel
    """
    table = np.zeros((51, 51), dtype=np.uint8)

    for scale_factor in range(51):
        step = 51.0 / (scale_factor + 1.0)
        pos = step
        while pos < 51.0:
            output_idx = int(round(pos))
            if output_idx < 51:
                table[output_idx][scale_factor] = 1
            pos += step

    return table


def generate_scale_table_102() -> np.ndarray:
    """
    Generate the 102x102 Y-axis scaling table.

    Used for vertical pixel skipping when scaling Alfred's sprite height.
    Alfred's unscaled height is 102 pixels (0x66).

    Algorithm from disassembly @ 0x00011ed6:
        for scale_factor in range(0x66):  # 0 to 101
            step = 102.0 / (scale_factor + 1.0)
            pos = step
            while pos < 102.0:
                table[round(pos)][scale_factor] = 1  # skip this row
                pos += step

    Returns:
        102x102 numpy array where table[output_y][scale_factor] = 1 means skip this source row
    """
    table = np.zeros((102, 102), dtype=np.uint8)

    for scale_factor in range(102):
        step = 102.0 / (scale_factor + 1.0)
        pos = step
        while pos < 102.0:
            output_idx = int(round(pos))
            if output_idx < 102:
                table[output_idx][scale_factor] = 1
            pos += step

    return table


def generate_scale_table_66() -> np.ndarray:
    """
    Generate the 66x66 scaling table.

    Used for alternate sprite dimensions (possibly talking animations).

    Returns:
        66x66 numpy array
    """
    table = np.zeros((66, 66), dtype=np.uint8)

    for scale_factor in range(66):
        step = 66.0 / (scale_factor + 1.0)
        pos = step
        while pos < 66.0:
            output_idx = int(round(pos))
            if output_idx < 66:
                table[output_idx][scale_factor] = 1
            pos += step

    return table


def generate_scale_table_62() -> np.ndarray:
    """
    Generate the 62x62 scaling table.

    Used for alternate sprite dimensions.

    Returns:
        62x62 numpy array
    """
    table = np.zeros((62, 62), dtype=np.uint8)

    for scale_factor in range(62):
        step = 62.0 / (scale_factor + 1.0)
        pos = step
        while pos < 62.0:
            output_idx = int(round(pos))
            if output_idx < 62:
                table[output_idx][scale_factor] = 1
            pos += step

    return table


# =============================================================================
# SCALE FACTOR CALCULATION (from load_room_data @ 0x0001585c)
# =============================================================================

@dataclass
class RoomScalingConfig:
    """Room-specific scaling configuration from sprite data."""
    scaling_mode: int      # Byte at room_sprite_data_ptr + 0x217
    reference_y: int       # Word at room_sprite_data_ptr + 0x214
    scale_divisor: int     # Byte at room_sprite_data_ptr + 0x216


def compute_scale_factors(alfred_y: int, config: RoomScalingConfig) -> Tuple[int, int]:
    """
    Compute Alfred's X and Y scale factors based on his Y position.

    From disassembly @ 0x0001585c - 0x00015909:

    if scaling_mode == 0:
        if alfred_y > reference_y:
            scale_x = 0
            scale_y = 0
        else:
            scale_y = (reference_y - alfred_y) / scale_divisor
            scale_x = scale_y / 2
    elif scaling_mode == 0xFF:
        scale_x = 0x2F  # 47
        scale_y = 0x5E  # 94
    elif scaling_mode == 0xFE:
        scale_x = 0
        scale_y = 0

    Args:
        alfred_y: Alfred's Y position on screen (0-399)
        config: Room's scaling configuration

    Returns:
        Tuple of (scale_x, scale_y) factors (0-50 for X, 0-101 for Y)
    """
    if config.scaling_mode == 0:
        # Normal perspective scaling
        if alfred_y > config.reference_y:
            return (0, 0)
        else:
            scale_y = (config.reference_y - alfred_y) // config.scale_divisor
            scale_x = scale_y // 2
            return (min(scale_x, 50), min(scale_y, 101))

    elif config.scaling_mode == 0xFF:
        # Fixed small scale (far away)
        return (0x2F, 0x5E)  # 47, 94

    elif config.scaling_mode == 0xFE:
        # No scaling (full size)
        return (0, 0)

    else:
        # Unknown mode, default to no scaling
        return (0, 0)


def compute_z_depth_from_y(alfred_y: int) -> int:
    """
    Compute Alfred's Z-depth for render queue sorting based on Y position.

    From disassembly @ 0x00015a20 - 0x00015a3d:
        z_depth = ((399 - alfred_y) & 0xFFFE) / 2 + 10

    Args:
        alfred_y: Alfred's Y position (0-399)

    Returns:
        Z-depth value (10-209)
    """
    return ((399 - alfred_y) & 0xFFFE) // 2 + 10


# =============================================================================
# SPRITE SCALING RENDERER (from render_character_sprite_scaled @ 0x00016ff8)
# =============================================================================

class AlfredScaler:
    """
    Implements the exact scaling algorithm from the original game.

    The algorithm uses pre-computed lookup tables to determine which
    pixels/rows to skip when scaling down a sprite.
    """

    # Screen dimensions (VGA 640x400)
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 400
    SCREEN_STRIDE = 640  # bytes per row

    # Alfred's unscaled sprite dimensions
    ALFRED_WIDTH = 51   # 0x33
    ALFRED_HEIGHT = 102  # 0x66

    def __init__(self):
        """Initialize scaling tables."""
        self.table_x = generate_scale_table_51()
        self.table_y = generate_scale_table_102()
        self.table_66 = generate_scale_table_66()
        self.table_62 = generate_scale_table_62()

    def scale_sprite(
        self,
        sprite_data: np.ndarray,
        dest_x: int,
        dest_y: int,
        scale_x: int,
        scale_y: int,
        screen_buffer: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Scale and render Alfred's sprite using the original algorithm.

        The algorithm works by iterating through output pixels and using
        lookup tables to determine which source pixels to skip.

        Args:
            sprite_data: Source sprite as 2D numpy array (height x width),
                        value 0xFF = transparent
            dest_x: Destination X coordinate on screen
            dest_y: Destination Y coordinate on screen
            scale_x: X scale factor (0 = full size, higher = smaller)
            scale_y: Y scale factor (0 = full size, higher = smaller)
            screen_buffer: Optional output buffer (creates new if None)

        Returns:
            Screen buffer with rendered sprite
        """
        if screen_buffer is None:
            screen_buffer = np.full((self.SCREEN_HEIGHT, self.SCREEN_WIDTH), 0xFF, dtype=np.uint8)

        src_height, src_width = sprite_data.shape

        # Clamp scale factors
        scale_x = min(scale_x, src_width - 1)
        scale_y = min(scale_y, src_height - 1)

        # Calculate output dimensions
        # Output width = source width - number of skipped columns
        out_width = src_width - scale_x
        out_height = src_height - scale_y

        # Clip to screen bounds
        clip_left = max(0, -dest_x)
        clip_top = max(0, -dest_y)
        clip_right = max(0, (dest_x + out_width) - self.SCREEN_WIDTH)
        clip_bottom = max(0, (dest_y + out_height) - self.SCREEN_HEIGHT)

        # Render sprite using lookup tables
        src_y = 0
        out_y = 0

        for table_y_idx in range(src_height):
            # Check if this source row should be skipped
            if scale_y > 0 and self.table_y[table_y_idx][scale_y] != 0:
                src_y += 1
                continue

            # Check vertical bounds
            screen_y = dest_y + out_y
            if screen_y < 0:
                src_y += 1
                out_y += 1
                continue
            if screen_y >= self.SCREEN_HEIGHT:
                break

            src_x = 0
            out_x = 0

            for table_x_idx in range(src_width):
                # Check if this source column should be skipped
                if scale_x > 0 and self.table_x[table_x_idx][scale_x] != 0:
                    src_x += 1
                    continue

                # Check horizontal bounds
                screen_x = dest_x + out_x
                if screen_x < 0:
                    src_x += 1
                    out_x += 1
                    continue
                if screen_x >= self.SCREEN_WIDTH:
                    break

                # Copy pixel if not transparent
                pixel = sprite_data[src_y, src_x]
                if pixel != 0xFF:
                    screen_buffer[screen_y, screen_x] = pixel

                src_x += 1
                out_x += 1

            src_y += 1
            out_y += 1

        return screen_buffer

    def get_scaled_dimensions(self, scale_x: int, scale_y: int) -> Tuple[int, int]:
        """
        Get the output dimensions for given scale factors.

        Args:
            scale_x: X scale factor (0 = full size)
            scale_y: Y scale factor (0 = full size)

        Returns:
            Tuple of (width, height) in pixels
        """
        return (self.ALFRED_WIDTH - scale_x, self.ALFRED_HEIGHT - scale_y)


# =============================================================================
# DEMONSTRATION / TESTING
# =============================================================================

def print_scale_table_sample(table: np.ndarray, name: str, size: int = 10):
    """Print a sample of a scale table for verification."""
    print(f"\n{name} (showing {size}x{size} corner):")
    print("    ", end="")
    for i in range(size):
        print(f"{i:3}", end="")
    print()
    for row in range(size):
        print(f"{row:3}:", end="")
        for col in range(size):
            print(f"{table[row][col]:3}", end="")
        print()


def demo_scaling():
    """Demonstrate the scaling system."""
    print("=" * 70)
    print("ALFRED PELROCK SCALING SYSTEM")
    print("=" * 70)

    scaler = AlfredScaler()

    # Show scale table samples
    print_scale_table_sample(scaler.table_x, "scale_table_x_51 (width scaling)")
    print_scale_table_sample(scaler.table_y, "scale_table_y_102 (height scaling)")

    # Show scale factor examples
    print("\n" + "=" * 70)
    print("SCALE FACTOR EXAMPLES")
    print("=" * 70)
    print("\nFor a room with reference_y=350, scale_divisor=5:")

    config = RoomScalingConfig(scaling_mode=0, reference_y=350, scale_divisor=5)

    print(f"\n{'Y Position':<12} {'Scale X':<10} {'Scale Y':<10} {'Output Size':<15} {'Z-Depth':<10}")
    print("-" * 60)

    for y in [100, 150, 200, 250, 300, 350, 399]:
        scale_x, scale_y = compute_scale_factors(y, config)
        z_depth = compute_z_depth_from_y(y)
        width, height = scaler.get_scaled_dimensions(scale_x, scale_y)
        print(f"{y:<12} {scale_x:<10} {scale_y:<10} {width}x{height:<10} {z_depth:<10}")

    # Show how the lookup tables work
    print("\n" + "=" * 70)
    print("HOW PIXEL SKIPPING WORKS")
    print("=" * 70)

    print("""
The scaling uses lookup tables to determine which pixels to skip.

For scale_x = 25 (skip 25 of 51 pixels = output 26 pixels wide):
    - table_x[pixel_index][25] = 1 means skip this pixel
    - table_x[pixel_index][25] = 0 means draw this pixel

Example for scale_x = 25:""")

    scale_x = 25
    drawn = []
    skipped = []
    for i in range(51):
        if scaler.table_x[i][scale_x] == 0:
            drawn.append(i)
        else:
            skipped.append(i)

    print(f"  Pixels drawn:  {drawn[:15]}... (total: {len(drawn)})")
    print(f"  Pixels skipped: {skipped[:15]}... (total: {len(skipped)})")
    print(f"  Output width: {len(drawn)} pixels")

    print("\n" + "=" * 70)
    print("INTEGRATION WITH SCUMMVM")
    print("=" * 70)
    print("""
To implement in ScummVM:

1. Generate scale tables at engine init (once):
   - scale_table_x_51[51][51]
   - scale_table_y_102[102][102]

2. When loading a room, get scaling config:
   - scaling_mode = room_data[0x217]
   - reference_y = *(uint16*)(room_data + 0x214)
   - scale_divisor = room_data[0x216]

3. Each frame, compute Alfred's scale factors:
   - (scale_x, scale_y) = compute_scale_factors(alfred_y, config)

4. Render Alfred using the lookup tables:
   - Skip source pixels where table[idx][scale_factor] == 1
   - Copy pixels where table[idx][scale_factor] == 0

5. Compute Z-depth for sorting:
   - z_depth = ((399 - alfred_y) & 0xFFFE) / 2 + 10
""")


if __name__ == "__main__":
    demo_scaling()
