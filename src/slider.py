#!/usr/bin/env python3
"""
Alfred Pelrock - Apply Slider Puzzle to Scene
Takes a game screenshot and creates a shuffled tile puzzle
"""

import sys
from PIL import Image
import random

# Puzzle configuration (from Ghidra analysis)
PUZZLE_WIDTH = 8   # columns
PUZZLE_HEIGHT = 5  # rows
TILE_WIDTH = 80    # pixels
TILE_HEIGHT = 80   # pixels
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

def init_puzzle():
    """Initialize puzzle in solved state (39 tiles, position 39 is empty)"""
    # Only tiles 0-38, position 39 (bottom-right) stays empty
    total_tiles = PUZZLE_WIDTH * PUZZLE_HEIGHT - 1
    return list(range(total_tiles))

def shuffle_puzzle(tile_positions, num_swaps=100):
    """Shuffle puzzle by swapping random pairs of tiles"""
    print(f"Shuffling puzzle with {num_swaps} random swaps...")

    for i in range(num_swaps):
        pos1 = random.randint(0, len(tile_positions) - 1)
        pos2 = random.randint(0, len(tile_positions) - 1)

        if pos1 != pos2:
            tile_positions[pos1], tile_positions[pos2] = tile_positions[pos2], tile_positions[pos1]

    return tile_positions

def extract_tiles(image):
    """Extract all tiles from the original image (excluding bottom-right which will be empty)"""
    tiles = []

    total_tiles = PUZZLE_WIDTH * PUZZLE_HEIGHT
    empty_tile_pos = total_tiles - 1  # Bottom-right tile

    for row in range(PUZZLE_HEIGHT):
        for col in range(PUZZLE_WIDTH):
            tile_idx = row * PUZZLE_WIDTH + col

            # Skip the bottom-right tile (will be empty/black)
            if tile_idx == empty_tile_pos:
                continue

            x = col * TILE_WIDTH
            y = row * TILE_HEIGHT

            tile = image.crop((x, y, x + TILE_WIDTH, y + TILE_HEIGHT))
            tiles.append(tile)

    print(f"Extracted {len(tiles)} tiles ({TILE_WIDTH}x{TILE_HEIGHT} each), 1 tile empty")
    return tiles

def create_shuffled_image(tiles, tile_positions):
    """Create shuffled image based on tile positions"""
    result = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Bottom-right tile position (last tile)
    empty_tile_pos = PUZZLE_WIDTH * PUZZLE_HEIGHT - 1

    for pos_idx, tile_id in enumerate(tile_positions):
        # Calculate destination position
        dest_row = pos_idx // PUZZLE_WIDTH
        dest_col = pos_idx % PUZZLE_WIDTH
        dest_x = dest_col * TILE_WIDTH
        dest_y = dest_row * TILE_HEIGHT

        # Leave bottom-right tile empty (black)
        if pos_idx == empty_tile_pos:
            # Fill with black
            from PIL import ImageDraw
            draw = ImageDraw.Draw(result)
            draw.rectangle([dest_x, dest_y, dest_x + TILE_WIDTH, dest_y + TILE_HEIGHT], fill=(0, 0, 0))
        else:
            # Paste the tile
            result.paste(tiles[tile_id], (dest_x, dest_y))

    return result

def draw_grid(image):
    """Draw grid lines on the puzzle"""
    from PIL import ImageDraw

    draw = ImageDraw.Draw(image)

    # Vertical lines
    for col in range(1, PUZZLE_WIDTH):
        x = col * TILE_WIDTH
        draw.line([(x, 0), (x, SCREEN_HEIGHT)], fill=(255, 0, 0), width=2)

    # Horizontal lines
    for row in range(1, PUZZLE_HEIGHT):
        y = row * TILE_HEIGHT
        draw.line([(0, y), (SCREEN_WIDTH, y)], fill=(255, 0, 0), width=2)

    return image

def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_puzzle_to_scene.py <input_image> [num_swaps] [--grid]")
        print("\nExample:")
        print("  python apply_puzzle_to_scene.py juego_032.png 100 --grid")
        sys.exit(1)

    input_file = sys.argv[1]
    num_swaps = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] != '--grid' else 100
    draw_grid_lines = '--grid' in sys.argv

    print("Alfred Pelrock - Slider Puzzle Generator")
    print("=" * 70)
    print()

    # Load image
    print(f"Loading image: {input_file}")
    image = Image.open(input_file)

    if image.size != (SCREEN_WIDTH, SCREEN_HEIGHT):
        print(f"Warning: Image size is {image.size}, expected {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print("Resizing...")
        image = image.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.Resampling.LANCZOS)

    # Convert to RGB if needed
    if image.mode != 'RGB':
        image = image.convert('RGB')

    print(f"Image size: {image.size}")
    print(f"Puzzle configuration: {PUZZLE_WIDTH}x{PUZZLE_HEIGHT} tiles")
    print()

    # Extract tiles
    tiles = extract_tiles(image)

    # Initialize and shuffle puzzle
    tile_positions = init_puzzle()
    print(f"Initial state: {tile_positions}")
    print()

    tile_positions = shuffle_puzzle(tile_positions, num_swaps)
    print(f"Shuffled state: {tile_positions}")
    print()

    # Create shuffled image
    shuffled_image = create_shuffled_image(tiles, tile_positions)

    # Add grid if requested
    if draw_grid_lines:
        print("Adding grid lines...")
        shuffled_image = draw_grid(shuffled_image)

    # Save result
    import os
    output_file = os.path.join('/mnt/user-data/outputs',
                               os.path.basename(input_file).rsplit('.', 1)[0] + '_puzzle.png')
    shuffled_image.save(output_file)

    print()
    print("=" * 70)
    print(f"Puzzle created successfully!")
    print(f"Output: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()
