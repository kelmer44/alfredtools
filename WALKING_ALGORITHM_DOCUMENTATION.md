# Walking Algorithm Documentation

## Overview

The walking system in Alfred Pelrock uses a pathfinding algorithm based on walkboxes (rectangular walkable areas) to move the character around the screen. The system handles collision detection, path calculation between walkboxes, and smooth movement along the calculated path.

## Data Structures

### Walkbox Structure (9 bytes each)

Located at offset `0x218` in pair 10 (room data), with count at `0x213`:

```
Offset  Size  Description
------  ----  -----------
0x00    2     X position (left edge)
0x02    2     Y position (top edge)
0x04    2     Width
0x06    2     Height
0x08    1     Flags/visited marker
```

**Memory Layout in Room Data:**
- `room_data_ptr + 0x213`: Walkbox count (byte)
- `room_data_ptr + 0x218`: Start of walkbox array
- Each walkbox: `room_data_ptr + 0x218 + (walkbox_index * 9)`

### Walkbox Coordinates

```python
# Walkbox bounds
x_min = walkbox[0:2]       # Left edge
y_min = walkbox[2:4]       # Top edge
x_max = x_min + walkbox[4:6]  # Right edge = left + width
y_max = y_min + walkbox[6:8]  # Bottom edge = top + height
```

### Pathfinding Data Structures

**Path Buffer (`DAT_0004fae0`)**: Array of walkbox indices (up to 100 bytes)
- Stores the sequence of walkboxes to traverse
- Terminated with `0xFF`

**Movement Buffer (`DAT_0004fae4`)**: Array of movement steps (up to 500 bytes, 5 bytes per step)
- Each step contains direction and distance information
- Format: `[flags][distance_x_low][distance_x_high][distance_y_low][distance_y_high]`

**Final Path (`DAT_0004fae8`)**: Compressed movement commands
- Format: `[0xFE][packed_direction_and_distance]...`
- Terminated with `0xFF`

## Key Functions

### 1. `find_walkbox_for_point(x, y)` @ 0x000178E6

Determines which walkbox contains a given point.

**Algorithm:**
```c
for (each walkbox in room) {
    if (x >= walkbox.x_min && x <= walkbox.x_max &&
        y >= walkbox.y_min && y <= walkbox.y_max) {
        return walkbox_index;
    }
}
return 0xFF;  // Not found
```

**Returns:**
- Walkbox index (0-255) if point is inside a walkbox
- `0xFF` if point is not in any walkbox

### 2. `get_adjacent_walkbox(current_walkbox)` @ 0x00017973

Finds a walkbox adjacent to the current one.

**Algorithm:**
```c
current_box = walkbox[current_walkbox];
mark_visited(current_walkbox);  // Set flags to 0x01

for (each other_walkbox in room) {
    if (other_walkbox == current_walkbox) continue;
    if (is_marked_visited(other_walkbox)) continue;
    
    // Check if walkboxes overlap or are adjacent
    if (boxes_overlap_or_touch(current_box, other_walkbox)) {
        return other_walkbox_index;
    }
}
return 0xFF;  // No adjacent walkbox found
```

**Adjacency Check:**
Two walkboxes are adjacent if:
1. Their X ranges overlap: `(box1.x_min <= box2.x_max) && (box2.x_min <= box1.x_max)`
2. Their Y ranges overlap: `(box1.y_min <= box2.y_max) && (box2.y_min <= box1.y_max)`
3. They touch or overlap by at least 1 pixel

### 3. `calculate_pathfinding(start_x, start_y, dest_x, dest_y)` @ 0x0001749A

Main pathfinding function that calculates the path from start to destination.

## Pathfinding Algorithm (Detailed)

### Step 1: Initialization

```c
// Allocate buffers
path_buffer = allocate_memory(100);      // DAT_0004fae0
movement_buffer = allocate_memory(500);  // DAT_0004fae4

// Clear visited flags for all walkboxes
for (i = 0; i < walkbox_count; i++) {
    walkbox[i].flags = 0;
}

// Find starting and destination walkboxes
start_box = find_walkbox_for_point(start_x, start_y);
dest_box = find_walkbox_for_point(dest_x, dest_y);

// Initialize path with start walkbox
path_buffer[0] = start_box;
path_index = 1;
```

### Step 2: Build Walkbox Path

Uses a breadth-first search to find sequence of walkboxes:

```c
current_box = start_box;

while (current_box != dest_box) {
    // Find next adjacent walkbox
    next_box = get_adjacent_walkbox(current_box);
    
    if (next_box == 0xFF) {
        // Dead end - backtrack
        path_index--;
        current_box = path_buffer[path_index - 1];
    } else if (next_box == dest_box) {
        // Found destination
        path_buffer[path_index++] = dest_box;
        break;
    } else {
        // Continue searching
        path_buffer[path_index++] = next_box;
        current_box = next_box;
    }
}

// Terminate path
path_buffer[path_index] = 0xFF;
```

### Step 3: Calculate Movement Steps

For each walkbox in the path, calculate entry/exit points:

```c
current_x = start_x;
current_y = start_y;
movement_index = 0;

for (each walkbox in path_buffer) {
    movement_step = {0, 0, 0, 0, 0};  // [flags, dx_low, dx_high, dy_low, dy_high]
    
    // Calculate horizontal movement
    if (current_x < walkbox.x_min) {
        movement_step.dx = walkbox.x_min - current_x;
        movement_step.flags |= 0x03;  // Move right
        current_x = walkbox.x_min;
    } else if (current_x > walkbox.x_max) {
        movement_step.dx = current_x - walkbox.x_max;
        movement_step.flags |= 0x02;  // Move left
        current_x = walkbox.x_max;
    }
    
    // Calculate vertical movement
    if (current_y < walkbox.y_min) {
        movement_step.dy = walkbox.y_min - current_y;
        movement_step.flags |= 0x0C;  // Move down
        current_y = walkbox.y_min;
    } else if (current_y > walkbox.y_max) {
        movement_step.dy = current_y - walkbox.y_max;
        movement_step.flags |= 0x08;  // Move up
        current_y = walkbox.y_max;
    }
    
    movement_buffer[movement_index++] = movement_step;
}

// Final step to exact destination
final_step = calculate_final_movement(current_x, current_y, dest_x, dest_y);
movement_buffer[movement_index++] = final_step;
movement_buffer[movement_index].flags = 0xFF;  // Terminate
```

### Step 4: Compress Movement Commands

Convert movement steps into compact format:

```c
compressed_path_index = 0;

for (each movement_step in movement_buffer) {
    flags = movement_step.flags;
    dx = movement_step.dx;
    dy = movement_step.dy;
    
    // Break large movements into smaller chunks (max 6 pixels horizontal, 5 vertical)
    while (dx > 6) {
        add_compressed_step(flags & 0x03, 6, 0);
        dx -= 6;
    }
    
    while (dy > 5) {
        add_compressed_step(flags & 0x0C, 0, 5);
        dy -= 5;
    }
    
    // Add remaining movement
    if (dx > 0 || dy > 0) {
        // Pack direction and distance into 2 bytes
        packed = pack_movement(flags, dx, dy);
        compressed_path[compressed_path_index++] = 0xFE;  // Movement marker
        compressed_path[compressed_path_index++] = packed_low;
        compressed_path[compressed_path_index++] = packed_high;
    }
}

compressed_path[compressed_path_index] = 0xFF;  // Terminate
```

## Movement Direction Flags

```c
// Horizontal movement (bits 0-1)
0x01 = Moving right (positive X)
0x02 = Moving left (negative X)
0x03 = Move to right edge

// Vertical movement (bits 2-3)
0x04 = Moving down (positive Y)
0x08 = Moving up (negative Y)
0x0C = Move to bottom edge

// Combined examples:
0x05 = Right + Down (diagonal)
0x09 = Right + Up (diagonal)
0x06 = Left + Down (diagonal)
0x0A = Left + Up (diagonal)
```

## Movement Execution

The compressed path is executed frame-by-frame in the game loop:

```c
void execute_walking() {
    if (path_index >= path_length) return;
    
    current_command = compressed_path[path_index];
    
    if (current_command == 0xFF) {
        // Path complete
        walking_active = false;
        return;
    }
    
    if (current_command == 0xFE) {
        // Unpack movement
        packed_data = compressed_path[path_index + 1];
        direction = (packed_data >> 4) & 0x0F;
        distance_x = (packed_data >> 0) & 0x07;
        distance_y = (packed_data >> 3) & 0x07;
        
        // Apply movement to character position
        if (direction & 0x01) alfred_x += distance_x;
        if (direction & 0x02) alfred_x -= distance_x;
        if (direction & 0x04) alfred_y += distance_y;
        if (direction & 0x08) alfred_y -= distance_y;
        
        path_index += 3;  // Skip command + 2 data bytes
    }
}
```

## Character Animation During Walking

The character sprite is updated based on movement direction:

```c
void update_walk_animation() {
    direction = get_current_walk_direction();
    
    // Animation frames based on direction
    if (direction & 0x01) {
        // Walking right
        animation_set = WALK_RIGHT_FRAMES;
    } else if (direction & 0x02) {
        // Walking left
        animation_set = WALK_LEFT_FRAMES;
    }
    
    if (direction & 0x04) {
        // Walking down (away from camera)
        animation_set = WALK_DOWN_FRAMES;
    } else if (direction & 0x08) {
        // Walking up (toward camera)
        animation_set = WALK_UP_FRAMES;
    }
    
    // Cycle through animation frames
    frame_counter++;
    if (frame_counter >= animation_speed) {
        current_frame = (current_frame + 1) % frame_count;
        frame_counter = 0;
    }
}
```

## Walking Speed

Movement speed is controlled by:
1. **Pixels per frame**: Typically 1-2 pixels per frame
2. **Frame rate**: ~18 FPS (DOS timing)
3. **Maximum step size**: 6 pixels horizontal, 5 pixels vertical per movement command

## Edge Cases and Special Handling

### 1. Unreachable Destination

If `dest_box == 0xFF` (destination not in any walkbox):
- Pathfinding fails
- Character doesn't move
- No path is generated

### 2. Same Walkbox

If `start_box == dest_box`:
- Generate single direct movement
- Skip walkbox pathfinding
- Move straight to destination

### 3. No Path Exists

If pathfinding exhausts all walkboxes without finding destination:
- Backtrack to previous walkbox
- Try alternative routes
- If all routes fail, character stays in place

### 4. Diagonal Movement

When both X and Y movement needed:
- Flags combine horizontal and vertical bits
- Movement occurs simultaneously
- Creates smooth diagonal motion

## Memory Locations

| Address    | Purpose |
|------------|---------|
| 0x0004fae0 | Path buffer (walkbox sequence) |
| 0x0004fae4 | Movement buffer (step-by-step movements) |
| 0x0004fae8 | Compressed path (final walking commands) |
| room_data_ptr + 0x213 | Walkbox count |
| room_data_ptr + 0x218 | Walkbox array base |
| room_data_ptr + 0x220 + (walkbox_index * 9) | Visited flag for walkbox |

## Example Walkbox Layout

Room 2 walkbox example:
```
Walkbox 0: x=0,   y=0,   w=640, h=200  (main floor area)
Walkbox 1: x=50,  y=200, w=200, h=50   (platform/stairs)
Walkbox 2: x=400, y=200, w=150, h=50   (another platform)
```

If Alfred is at (100, 100) and clicks (500, 220):
1. Start box: 0 (contains 100, 100)
2. Dest box: 2 (contains 500, 220)
3. Path: [0] → [1] → [2]
4. Movements:
   - Move to walkbox 1 entry point
   - Move across walkbox 1
   - Move to walkbox 2 entry point
   - Move to final destination (500, 220)

## Integration with Click Handling

When player clicks on screen:

```c
void handle_screen_click(click_x, click_y) {
    if (is_walkable_area(click_x, click_y)) {
        alfred_dest_x = click_x;
        alfred_dest_y = click_y;
        calculate_pathfinding(alfred_x, alfred_y, click_x, click_y);
        walking_active = true;
    }
}
```

## Optimization Notes

1. **Visited Flags**: Prevent infinite loops in walkbox search
2. **Buffer Sizes**: Limited to 100 walkbox steps, 500 movement steps
3. **Step Chunking**: Large movements split into smaller steps for smooth animation
4. **Direction Packing**: Efficient bit-packing reduces memory usage

## Tools for Analysis

### Extract Walkbox Data

Use `src/extract_room_data.py`:
```bash
python3 src/extract_room_data.py
```

Outputs walkbox coordinates for all rooms in JSON format.

### Visualize Walkboxes

The walkboxes can be overlaid on background images to show walkable areas visually.

## Future Enhancements

Potential improvements to document:
- A* pathfinding instead of breadth-first
- Smooth path interpolation
- Dynamic obstacle avoidance
- Character-specific walk speeds
- Terrain-based movement costs
