#!/usr/bin/env python3
"""
Shadow System Implementation

Extracts shadow maps from ALFRED.5 and demonstrates how to apply
shadow effects to character sprites using palette remapping.

Based on reverse engineering of the game's shadow rendering system.
See SHADOW_SYSTEM_DOCUMENTATION.md for detailed algorithm explanation.
"""

import struct
from pathlib import Path
from PIL import Image
import numpy as np


class ShadowSystem:
    """Manages shadow maps and shadow application for character rendering"""

    SHADOW_MAP_WIDTH = 640
    SHADOW_MAP_HEIGHT = 400
    SHADOW_MAP_SIZE = SHADOW_MAP_WIDTH * SHADOW_MAP_HEIGHT
    SHADOW_LEVELS = 4
    PALETTE_SIZE = 256
    REMAP_TABLE_SIZE = PALETTE_SIZE * SHADOW_LEVELS

    NO_SHADOW_VALUE = 0xFF

    def __init__(self):
        self.shadow_maps = {}  # room_number -> shadow_map
        self.palette_remaps = {}  # room_number -> remap_table

    def extract_shadow_map(self, alfred5_data: bytes, room_number: int) -> bytearray:
        """
        Extract shadow map for a specific room from ALFRED.5

        Args:
            alfred5_data: Raw bytes from ALFRED.5 file
            room_number: Room number (0-54)

        Returns:
            Shadow map as bytearray (640×400 = 256,000 bytes)
        """
        # Read directory entry (6 bytes per room)
        entry_offset = room_number * 6

        if entry_offset + 6 > len(alfred5_data):
            raise ValueError(f"Room {room_number} directory entry out of bounds")

        # Extract 24-bit little-endian offset
        shadow_offset = (alfred5_data[entry_offset] |
                        (alfred5_data[entry_offset + 1] << 8) |
                        (alfred5_data[entry_offset + 2] << 16))

        print(f"Room {room_number}: Shadow offset = 0x{shadow_offset:06X}")

        # Decompress RLE data
        pixels = bytearray()
        offset = shadow_offset

        while offset < len(alfred5_data) - 1:
            # Check for BUDA terminator
            if alfred5_data[offset:offset+4] == b'BUDA':
                print(f"  Found BUDA marker at 0x{offset:06X}")
                break

            # Read RLE pair: [count, color]
            count = alfred5_data[offset]
            color = alfred5_data[offset + 1]
            pixels.extend([color] * count)
            offset += 2

            # Safety check
            if len(pixels) > self.SHADOW_MAP_SIZE:
                print(f"  Warning: Exceeded expected size, truncating")
                pixels = pixels[:self.SHADOW_MAP_SIZE]
                break

        # Verify size
        if len(pixels) != self.SHADOW_MAP_SIZE:
            print(f"  Warning: Expected {self.SHADOW_MAP_SIZE} bytes, got {len(pixels)}")
            # Pad or truncate to correct size
            if len(pixels) < self.SHADOW_MAP_SIZE:
                pixels.extend([self.NO_SHADOW_VALUE] * (self.SHADOW_MAP_SIZE - len(pixels)))
            else:
                pixels = pixels[:self.SHADOW_MAP_SIZE]

        self.shadow_maps[room_number] = pixels
        return pixels

    def extract_all_shadow_maps(self, alfred5_path: Path, output_dir: Path = None):
        """
        Extract all 55 shadow maps from ALFRED.5

        Args:
            alfred5_path: Path to ALFRED.5 file
            output_dir: Optional directory to save visualizations
        """
        print(f"Loading ALFRED.5 from: {alfred5_path}")

        with open(alfred5_path, 'rb') as f:
            alfred5_data = f.read()

        print(f"File size: {len(alfred5_data):,} bytes ({len(alfred5_data) / 1024 / 1024:.2f} MB)")
        print()

        total_rooms = 55
        for room_num in range(total_rooms):
            try:
                shadow_map = self.extract_shadow_map(alfred5_data, room_num)

                # Analyze shadow values
                unique_values = set(shadow_map)
                non_shadow_pixels = sum(1 for v in shadow_map if v == self.NO_SHADOW_VALUE)
                shadow_pixels = len(shadow_map) - non_shadow_pixels

                print(f"  Unique values: {sorted(unique_values)}")
                print(f"  Shadow coverage: {shadow_pixels}/{len(shadow_map)} pixels ({shadow_pixels/len(shadow_map)*100:.1f}%)")

                # Save visualization if output directory specified
                if output_dir:
                    self.save_shadow_visualization(shadow_map, room_num, output_dir)

                print()

            except Exception as e:
                print(f"  Error: {e}")
                print()

    def save_shadow_visualization(self, shadow_map: bytearray, room_number: int,
                                  output_dir: Path):
        """
        Save shadow map as PNG image for visualization

        Args:
            shadow_map: Shadow map data (256,000 bytes)
            room_number: Room number for filename
            output_dir: Directory to save PNG
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Convert to numpy array
        shadow_array = np.array(shadow_map, dtype=np.uint8)
        shadow_array = shadow_array.reshape(self.SHADOW_MAP_HEIGHT, self.SHADOW_MAP_WIDTH)

        # Create visualization
        # 0xFF (no shadow) -> white
        # Other values -> shades of gray based on value
        vis_array = np.zeros_like(shadow_array)

        # Map shadow values to visible range
        mask_no_shadow = (shadow_array == self.NO_SHADOW_VALUE)
        mask_shadow = ~mask_no_shadow

        vis_array[mask_no_shadow] = 255  # White for no shadow
        vis_array[mask_shadow] = 255 - (shadow_array[mask_shadow] * 64)  # Darker for shadow

        # Create and save image
        img = Image.fromarray(vis_array, mode='L')
        output_path = output_dir / f"shadow_room_{room_number:02d}.png"
        img.save(output_path)
        print(f"  Saved: {output_path}")

    def load_palette_remap_table(self, alfred1_data: bytes, room_number: int) -> bytearray:
        """
        Load palette remapping table for a room from ALFRED.1

        The table is 1024 bytes: 256 colors × 4 shadow levels

        Args:
            alfred1_data: Raw bytes from ALFRED.1 file
            room_number: Room number (0-54)

        Returns:
            Remap table as bytearray (1024 bytes)
        """
        # Each room has a 1024-byte remap table
        offset = room_number * self.REMAP_TABLE_SIZE

        if offset + self.REMAP_TABLE_SIZE > len(alfred1_data):
            raise ValueError(f"Room {room_number} remap table out of bounds")

        remap_table = bytearray(alfred1_data[offset:offset + self.REMAP_TABLE_SIZE])
        self.palette_remaps[room_number] = remap_table

        return remap_table

    def apply_shadow_to_sprite(self, sprite_pixels: bytearray, sprite_width: int,
                               sprite_height: int, char_x: int, char_y: int,
                               room_number: int) -> bytearray:
        """
        Apply shadow effect to character sprite based on position

        Args:
            sprite_pixels: Character sprite pixel data (width * height)
            sprite_width: Sprite width in pixels
            sprite_height: Sprite height in pixels
            char_x: Character X position on screen
            char_y: Character Y position on screen
            room_number: Current room number

        Returns:
            Modified sprite with shadow applied
        """
        # Get shadow map and palette remap for this room
        if room_number not in self.shadow_maps:
            raise ValueError(f"Shadow map for room {room_number} not loaded")

        if room_number not in self.palette_remaps:
            raise ValueError(f"Palette remap for room {room_number} not loaded")

        shadow_map = self.shadow_maps[room_number]
        palette_remap = self.palette_remaps[room_number]

        # Sample shadow at character's foot position
        # Game uses character height (102) but we use actual sprite height
        shadow_y = char_y + sprite_height
        shadow_x = char_x

        # Check bounds
        if shadow_y >= self.SHADOW_MAP_HEIGHT or shadow_x >= self.SHADOW_MAP_WIDTH:
            print(f"Warning: Shadow lookup position ({shadow_x}, {shadow_y}) out of bounds")
            return sprite_pixels  # No shadow

        if shadow_x < 0 or shadow_y < 0:
            return sprite_pixels  # No shadow

        # Look up shadow value
        shadow_index = (shadow_y * self.SHADOW_MAP_WIDTH) + shadow_x
        shadow_value = shadow_map[shadow_index]

        # Check if in shadow
        if shadow_value == self.NO_SHADOW_VALUE:
            return sprite_pixels  # Not in shadow, return unchanged

        print(f"Character at ({char_x}, {char_y}) is in shadow (level {shadow_value})")

        # Apply shadow by remapping colors
        shadowed_sprite = bytearray()
        for pixel in sprite_pixels:
            if pixel == 0xFF:  # Transparent
                shadowed_sprite.append(0xFF)
            else:
                # Remap to shadowed color
                remap_index = pixel + (shadow_value * self.PALETTE_SIZE)

                if remap_index >= len(palette_remap):
                    # Out of bounds, use original color
                    shadowed_sprite.append(pixel)
                else:
                    shadowed_color = palette_remap[remap_index]
                    shadowed_sprite.append(shadowed_color)

        return shadowed_sprite

    def get_shadow_at_position(self, x: int, y: int, room_number: int) -> int:
        """
        Get shadow value at a specific screen position

        Args:
            x, y: Screen coordinates
            room_number: Room number

        Returns:
            Shadow value (0xFF = no shadow, 0-254 = shadow level)
        """
        if room_number not in self.shadow_maps:
            raise ValueError(f"Shadow map for room {room_number} not loaded")

        if x < 0 or x >= self.SHADOW_MAP_WIDTH or y < 0 or y >= self.SHADOW_MAP_HEIGHT:
            return self.NO_SHADOW_VALUE

        shadow_map = self.shadow_maps[room_number]
        shadow_index = (y * self.SHADOW_MAP_WIDTH) + x

        return shadow_map[shadow_index]

    def analyze_shadow_coverage(self, room_number: int):
        """Print detailed analysis of shadow coverage for a room"""
        if room_number not in self.shadow_maps:
            raise ValueError(f"Shadow map for room {room_number} not loaded")

        shadow_map = self.shadow_maps[room_number]

        # Count pixels per shadow level
        shadow_counts = {}
        for value in shadow_map:
            shadow_counts[value] = shadow_counts.get(value, 0) + 1

        print(f"\nShadow Analysis - Room {room_number}")
        print("=" * 50)

        total_pixels = len(shadow_map)
        for value in sorted(shadow_counts.keys()):
            count = shadow_counts[value]
            percentage = (count / total_pixels) * 100

            if value == self.NO_SHADOW_VALUE:
                label = "No Shadow"
            else:
                label = f"Shadow Level {value}"

            print(f"{label:20s}: {count:6d} pixels ({percentage:5.2f}%)")

        print("=" * 50)


def main():
    """Demonstration of shadow system usage"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python shadow_system.py <path_to_ALFRED.5> [output_dir]")
        print()
        print("This will extract all shadow maps and save visualizations.")
        return

    alfred5_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("shadow_maps")

    if not alfred5_path.exists():
        print(f"Error: File not found: {alfred5_path}")
        return

    # Create shadow system
    shadow_system = ShadowSystem()

    # Extract all shadow maps
    shadow_system.extract_all_shadow_maps(alfred5_path, output_dir)

    print("\n" + "=" * 60)
    print("Shadow extraction complete!")
    print(f"Visualizations saved to: {output_dir}")
    print()
    print("To use shadow system in your code:")
    print("  1. Load shadow map with extract_shadow_map()")
    print("  2. Load palette remap with load_palette_remap_table()")
    print("  3. Apply shadow with apply_shadow_to_sprite()")
    print("=" * 60)


if __name__ == '__main__':
    main()
