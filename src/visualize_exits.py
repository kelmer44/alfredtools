from PIL import Image, ImageDraw
import struct

def get_room_exits(alfred1_path, room_num):
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    room_offset = room_num * 104
    pair10_offset = room_offset + (10 * 8)
    offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
    size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

    if size == 0 or offset >= len(data):
        return []

    pair10_data = data[offset:offset+size]

    if 0x1BE >= len(pair10_data):
        return []

    exit_count = pair10_data[0x1BE]
    exits = []
    exit_base = 0x1BF

    for i in range(exit_count):
        entry_base = exit_base + (i * 14)
        if entry_base + 14 > len(pair10_data):
            break

        trigger_x = struct.unpack('<H', pair10_data[entry_base+3:entry_base+5])[0]
        trigger_y = struct.unpack('<H', pair10_data[entry_base+5:entry_base+7])[0]
        trigger_w = pair10_data[entry_base+7]
        trigger_h = pair10_data[entry_base+8]

        exits.append({
            'x': trigger_x,
            'y': trigger_y,
            'width': trigger_w,
            'height': trigger_h
        })

    return exits

def visualize_exits(background_path, output_path):
    # Load the background image
    img = Image.open(background_path)
    # Convert to RGBA to support transparency
    img = img.convert('RGBA')

    # Create a transparent overlay
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Draw the cursor hotspot area (where cursor changes to exit cursor)
    hotspot_x = 231
    hotspot_y = 138
    hotspot_width = 65
    hotspot_height = 122
    print(f"Drawing hotspot area at ({hotspot_x}, {hotspot_y}) with size {hotspot_width}x{hotspot_height}")

    # Draw the hotspot with blue semi-transparent color
    hotspot_color = (0, 0, 255, 64)  # Blue with 25% opacity
    draw.rectangle([hotspot_x, hotspot_y, hotspot_x + hotspot_width, hotspot_y + hotspot_height],
                  outline=(0, 0, 255),
                  fill=hotspot_color)

    # Get and draw the actual exit trigger point from ALFRED.1
    exits = get_room_exits("files/ALFRED.1", 0)
    if exits:
        for exit_data in exits:
            trigger_x = exit_data['x']
            trigger_y = exit_data['y']
            trigger_width = exit_data['width']
            trigger_height = exit_data['height']
            print(f"Drawing trigger point at ({trigger_x}, {trigger_y}) with size {trigger_width}x{trigger_height}")

            # Draw trigger point with red semi-transparent color
            trigger_color = (255, 0, 0, 128)  # Red with 50% opacity
            draw.rectangle([trigger_x, trigger_y, trigger_x + trigger_width, trigger_y + trigger_height],
                         outline=(255, 0, 0),
                         fill=trigger_color)        # Draw the cursor hotspot area (where cursor changes to exit cursor)
    hotspot_x = 231
    hotspot_y = 138
    hotspot_width = 65
    hotspot_height = 122
    print(f"Drawing hotspot area at ({hotspot_x}, {hotspot_y}) with size {hotspot_width}x{hotspot_height}")

    # Draw the hotspot with blue semi-transparent color
    hotspot_color = (0, 0, 255, 64)  # Blue with 25% opacity
    draw.rectangle([hotspot_x, hotspot_y, hotspot_x + hotspot_width, hotspot_y + hotspot_height],
                  outline=(0, 0, 255),
                  fill=hotspot_color)

    # Get and draw the actual exit trigger point from ALFRED.1
    exits = get_room_exits("files/ALFRED.1", 0)
    if exits:
        for exit_data in exits:
            trigger_x = exit_data['x']
            trigger_y = exit_data['y']
            trigger_width = exit_data['width']
            trigger_height = exit_data['height']
            print(f"Drawing trigger point at ({trigger_x}, {trigger_y}) with size {trigger_width}x{trigger_height}")

            # Draw trigger point with red semi-transparent color
            trigger_color = (255, 0, 0, 128)  # Red with 50% opacity
            draw.rectangle([trigger_x, trigger_y, trigger_x + trigger_width, trigger_y + trigger_height],
                         outline=(255, 0, 0),
                         fill=trigger_color)

    # Combine the background with the overlay
    img = Image.alpha_composite(img, overlay)

    # Save the result
    img.save(output_path)

if __name__ == "__main__":
    visualize_exits("backgrounds_color/room_00.png", "exits/room00_exits.png")
