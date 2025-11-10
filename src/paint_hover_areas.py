"""
paint_hover_areas.py

Paint hover areas as colored rectangles over a room background image.
Usage: python3 src/paint_hover_areas.py <room_image.png> --room 1 --out output/painted_room1.png
"""

import json
import argparse
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


def load_hover_data(json_path, room_num):
    """Load hover area data for a specific room."""
    with open(json_path, 'r') as f:
        data = json.load(f)

    for room in data:
        if room['room'] == room_num:
            return room
    return None


def paint_areas(image_path, room_data, output_path, filter_regions=None, min_size=10):
    """Paint hover areas on the image."""
    img = Image.open(image_path).convert('RGBA')

    # Create overlay layer
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Color mapping for regions
    colors = {
        'left': (255, 0, 0, 80),      # Red with alpha
        'center': (0, 255, 0, 80),    # Green with alpha
        'right': (0, 0, 255, 80),     # Blue with alpha
    }

    border_colors = {
        'left': (255, 0, 0, 200),
        'center': (0, 255, 0, 200),
        'right': (0, 0, 255, 200),
    }

    # Filter and deduplicate areas
    seen = set()
    painted_count = 0

    for area in room_data['areas']:
        # Apply filters
        if filter_regions and area['region'] not in filter_regions:
            continue

        # Skip very small areas (likely noise)
        if area['w'] < min_size or area['h'] < min_size:
            continue

        # Deduplicate by coordinates
        key = (area['x'], area['y'], area['w'], area['h'])
        if key in seen:
            continue
        seen.add(key)

        x, y, w, h = area['x'], area['y'], area['w'], area['h']
        region = area['region']

        # Draw filled rectangle
        draw.rectangle(
            [(x, y), (x + w, y + h)],
            fill=colors.get(region, (128, 128, 128, 80)),
            outline=border_colors.get(region, (128, 128, 128, 200)),
            width=2
        )

        painted_count += 1

    # Composite the overlay onto the original image
    result = Image.alpha_composite(img, overlay)
    result = result.convert('RGB')

    # Save result
    result.save(output_path)
    print(f"Painted {painted_count} unique hover areas to {output_path}")
    print(f"Room {room_data['room']}: {len(seen)} total areas")

    # Print legend
    print("\nColor legend:")
    print("  Red = Left side areas")
    print("  Green = Center areas")
    print("  Blue = Right side areas")


def main():
    parser = argparse.ArgumentParser(description='Paint hover areas over a room image')
    parser.add_argument('image', help='Input room image (PNG)')
    parser.add_argument('--room', type=int, default=1, help='Room number to paint')
    parser.add_argument('--json', default='output/hover_areas.json', help='Hover areas JSON file')
    parser.add_argument('--out', default='output/painted_room.png', help='Output image path')
    parser.add_argument('--regions', nargs='+', choices=['left', 'center', 'right'],
                        help='Filter to specific regions only')
    parser.add_argument('--min-size', type=int, default=10,
                        help='Minimum width/height to paint (default: 10)')

    args = parser.parse_args()

    # Load room data
    room_data = load_hover_data(args.json, args.room)
    if not room_data:
        print(f"Error: Room {args.room} not found in {args.json}")
        return 1

    # Ensure output directory exists
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)

    # Paint areas
    paint_areas(args.image, room_data, args.out, args.regions, args.min_size)

    return 0


if __name__ == '__main__':
    exit(main())
