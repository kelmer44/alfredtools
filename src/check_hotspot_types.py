#!/usr/bin/env python3
"""
Check for overlapping exit areas and hotspots to determine cursor type
"""

import struct
from pathlib import Path

def get_room_exits(data, room_num):
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

    # Get exit hover areas at 0x2BE (256 bytes after exit triggers)
    hover_base = exit_base + 256

    for i in range(exit_count):
        entry_base = exit_base + (i * 14)
        hover_entry = hover_base + (i * 14)  # Corresponding hover area

        if entry_base + 14 > len(pair10_data) or hover_entry + 14 > len(pair10_data):
            break

        # Get trigger point
        trigger_x = struct.unpack('<H', pair10_data[entry_base+3:entry_base+5])[0]
        trigger_y = struct.unpack('<H', pair10_data[entry_base+5:entry_base+7])[0]
        trigger_w = pair10_data[entry_base+7]
        trigger_h = pair10_data[entry_base+8]

        # Get hover area (same structure as trigger, 256 bytes later)
        hover_x = struct.unpack('<H', pair10_data[hover_entry+3:hover_entry+5])[0]
        hover_y = struct.unpack('<H', pair10_data[hover_entry+5:hover_entry+7])[0]
        hover_w = pair10_data[hover_entry+7]
        hover_h = pair10_data[hover_entry+8]

        exits.append({
            'trigger': {
                'x': trigger_x,
                'y': trigger_y,
                'width': trigger_w,
                'height': trigger_h
            },
            'hover': {
                'x': hover_x,
                'y': hover_y,
                'width': hover_w,
                'height': hover_h
            }
        })

    return exitsdef get_room_hotspots(data, room_num):
    room_offset = room_num * 104
    pair10_offset = room_offset + (10 * 8)
    offset = struct.unpack('<I', data[pair10_offset:pair10_offset+4])[0]
    size = struct.unpack('<I', data[pair10_offset+4:pair10_offset+8])[0]

    if size == 0 or offset >= len(data):
        return []

    pair10_data = data[offset:offset+size]

    count_offset = 0x47a
    if count_offset >= len(pair10_data):
        return []

    count = pair10_data[count_offset]
    hotspots = []
    hotspot_data_start = 0x47c

    for i in range(count):
        obj_offset = hotspot_data_start + i * 9
        if obj_offset + 9 > len(pair10_data):
            break

        type_byte = pair10_data[obj_offset]
        x = pair10_data[obj_offset+1] | (pair10_data[obj_offset+2] << 8)
        y = pair10_data[obj_offset+3] | (pair10_data[obj_offset+4] << 8)
        w = pair10_data[obj_offset+5]
        h = pair10_data[obj_offset+6]
        extra = pair10_data[obj_offset+7] | (pair10_data[obj_offset+8] << 8)

        hotspots.append({
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'type': type_byte,
            'extra': extra
        })

    return hotspots

def check_overlap(rect1, rect2):
    """Check if two rectangles overlap"""
    return not (rect1['x'] + rect1['width'] <= rect2['x'] or
               rect2['x'] + rect2['width'] <= rect1['x'] or
               rect1['y'] + rect1['height'] <= rect2['y'] or
               rect2['y'] + rect2['height'] <= rect1['y'])

def determine_cursor_type(data, room_num, x, y):
    """Determine which cursor should be shown at given coordinates"""

    hotspots = get_room_hotspots(data, room_num)
    exits = get_room_exits(data, room_num)

    # Define test point as 1x1 rectangle
    point = {'x': x, 'y': y, 'width': 1, 'height': 1}

    # Check if point is in any exit area
    in_exit = False
    for exit_area in exits:
        if check_overlap(point, exit_area):
            in_exit = True
            break

    # Check hotspots
    in_hotspot = False
    for hotspot in hotspots:
        if check_overlap(point, hotspot):
            print(f"Found hotspot at ({hotspot['x']}, {hotspot['y']}) size {hotspot['width']}x{hotspot['height']} - Type: {hotspot['type']:02X}h Extra: {hotspot['extra']:04X}h")
            in_hotspot = True
            break

    if in_exit and in_hotspot:
        return "cursor5_combination"
    elif in_exit:
        return "cursor3_exit_hover"
    elif in_hotspot:
        return "cursor1_hotspot_hover"
    else:
        return "cursor2_default"

def main():
    with open("files/ALFRED.1", 'rb') as f:
        data = f.read()

    room_num = 1  # Check room 1
    test_points = [
        (21, 216),  # The hotspot you mentioned
        (231, 138),  # The exit area we found earlier
        (247, 266),  # Another hotspot from room 1
    ]

    print(f"Checking cursor types in Room {room_num}:")
    print("=" * 50)

    for x, y in test_points:
        print(f"\nChecking point ({x}, {y}):")
        cursor = determine_cursor_type(data, room_num, x, y)
        print(f"Should show: {cursor}")

if __name__ == "__main__":
    main()
