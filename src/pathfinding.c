/**
 * Alfred Pelrock - Character Walking/Pathfinding Algorithm
 * ==========================================================
 *
 * Implements the pathfinding system used in Alfred Pelrock (1997)
 * Based on reverse engineering of the original DOS executable.
 *
 * This algorithm uses walkboxes (rectangular walkable areas) and breadth-first
 * search to calculate paths between two points on the screen.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>

/* ============================================================================
 * Data Structures
 * ============================================================================ */

/**
 * Walkbox structure (9 bytes)
 * Defines a rectangular walkable area in the room
 */
typedef struct {
    uint16_t x;           // Left edge
    uint16_t y;           // Top edge
    uint16_t width;       // Width of walkable area
    uint16_t height;      // Height of walkable area
    uint8_t flags;        // Visited flag (0x00 = unvisited, 0x01 = visited)
} Walkbox;

/**
 * Movement step (5 bytes)
 * Represents a single movement command
 */
typedef struct {
    uint8_t flags;        // Direction flags (see MOVE_* constants)
    uint16_t distance_x;  // Horizontal distance to move
    uint16_t distance_y;  // Vertical distance to move
} MovementStep;

/**
 * Room data structure
 */
typedef struct {
    uint8_t walkbox_count;
    Walkbox walkboxes[32];  // Maximum 32 walkboxes per room
    uint8_t *room_data_ptr;
} RoomData;

/**
 * Pathfinding context
 */
typedef struct {
    uint8_t *path_buffer;           // Sequence of walkbox indices
    MovementStep *movement_buffer;  // Array of movement steps
    uint8_t *compressed_path;       // Final compressed path
    uint16_t path_length;
    uint16_t movement_count;
    uint16_t compressed_length;
} PathContext;

/* ============================================================================
 * Constants
 * ============================================================================ */

// Direction flags (bit-packed)
#define MOVE_RIGHT      0x01  // Move right (positive X)
#define MOVE_LEFT       0x02  // Move left (negative X)
#define MOVE_HORIZ      0x03  // Horizontal movement mask
#define MOVE_DOWN       0x04  // Move down (positive Y)
#define MOVE_UP         0x08  // Move up (negative Y)
#define MOVE_VERT       0x0C  // Vertical movement mask

// Special markers
#define PATH_END        0xFF  // End of path marker
#define MOVEMENT_MARKER 0xFE  // Movement command marker

// Buffer sizes
#define MAX_PATH_LENGTH     100
#define MAX_MOVEMENT_STEPS  100  // 500 bytes / 5 bytes per step
#define MAX_COMPRESSED_PATH 300

// Movement chunking limits
#define MAX_STEP_X 6
#define MAX_STEP_Y 5

/* ============================================================================
 * Helper Functions
 * ============================================================================ */

/**
 * Check if a point is inside a walkbox
 */
bool point_in_walkbox(Walkbox *box, uint16_t x, uint16_t y) {
    return (x >= box->x &&
            x <= box->x + box->width &&
            y >= box->y &&
            y <= box->y + box->height);
}

/**
 * Check if two walkboxes overlap or touch (are adjacent)
 */
bool walkboxes_adjacent(Walkbox *box1, Walkbox *box2) {
    uint16_t box1_x_max = box1->x + box1->width;
    uint16_t box1_y_max = box1->y + box1->height;
    uint16_t box2_x_max = box2->x + box2->width;
    uint16_t box2_y_max = box2->y + box2->height;

    // Check if X ranges overlap
    bool x_overlap = (box1->x <= box2_x_max) && (box2->x <= box1_x_max);

    // Check if Y ranges overlap
    bool y_overlap = (box1->y <= box2_y_max) && (box2->y <= box1_y_max);

    return x_overlap && y_overlap;
}

/**
 * Clear all visited flags in walkboxes
 */
void clear_visited_flags(RoomData *room) {
    for (int i = 0; i < room->walkbox_count; i++) {
        room->walkboxes[i].flags = 0;
    }
}

/* ============================================================================
 * Core Pathfinding Functions
 * ============================================================================ */

/**
 * Find which walkbox contains a given point
 * Returns: walkbox index (0-255) or 0xFF if not found
 */
uint8_t find_walkbox_for_point(RoomData *room, uint16_t x, uint16_t y) {
    for (uint8_t i = 0; i < room->walkbox_count; i++) {
        if (point_in_walkbox(&room->walkboxes[i], x, y)) {
            return i;
        }
    }
    return 0xFF;  // Not found
}

/**
 * Find an adjacent walkbox to the current one
 * Returns: walkbox index or 0xFF if no adjacent walkbox found
 */
uint8_t get_adjacent_walkbox(RoomData *room, uint8_t current_box_index) {
    Walkbox *current_box = &room->walkboxes[current_box_index];

    // Mark current walkbox as visited
    current_box->flags = 0x01;

    // Search for adjacent unvisited walkbox
    for (uint8_t i = 0; i < room->walkbox_count; i++) {
        // Skip current walkbox
        if (i == current_box_index) {
            continue;
        }

        // Skip already visited walkboxes
        if (room->walkboxes[i].flags == 0x01) {
            continue;
        }

        // Check if walkboxes are adjacent
        if (walkboxes_adjacent(current_box, &room->walkboxes[i])) {
            return i;
        }
    }

    return 0xFF;  // No adjacent walkbox found
}

/**
 * Build path of walkbox indices from start to destination
 * Returns: path length (number of walkboxes in path)
 */
uint16_t build_walkbox_path(RoomData *room,
                            uint8_t start_box,
                            uint8_t dest_box,
                            uint8_t *path_buffer) {
    uint16_t path_index = 0;
    uint8_t current_box = start_box;

    // Initialize path with start walkbox
    path_buffer[path_index++] = start_box;

    // Clear visited flags
    clear_visited_flags(room);

    // Breadth-first search through walkboxes
    while (current_box != dest_box && path_index < MAX_PATH_LENGTH - 1) {
        uint8_t next_box = get_adjacent_walkbox(room, current_box);

        if (next_box == 0xFF) {
            // Dead end - backtrack
            if (path_index > 1) {
                path_index--;
                current_box = path_buffer[path_index - 1];
            } else {
                // No path exists
                return 0;
            }
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
    path_buffer[path_index] = PATH_END;

    return path_index;
}

/**
 * Calculate movement needed to reach a target within a walkbox
 */
void calculate_movement_to_target(uint16_t current_x, uint16_t current_y,
                                 uint16_t target_x, uint16_t target_y,
                                 Walkbox *box,
                                 MovementStep *step) {
    step->flags = 0;
    step->distance_x = 0;
    step->distance_y = 0;

    // Calculate horizontal movement
    if (current_x < box->x) {
        // Need to move right to enter walkbox
        step->distance_x = box->x - current_x;
        step->flags |= MOVE_RIGHT;
    } else if (current_x > box->x + box->width) {
        // Need to move left to enter walkbox
        step->distance_x = current_x - (box->x + box->width);
        step->flags |= MOVE_LEFT;
    }

    // Calculate vertical movement
    if (current_y < box->y) {
        // Need to move down to enter walkbox
        step->distance_y = box->y - current_y;
        step->flags |= MOVE_DOWN;
    } else if (current_y > box->y + box->height) {
        // Need to move up to enter walkbox
        step->distance_y = current_y - (box->y + box->height);
        step->flags |= MOVE_UP;
    }
}

/**
 * Generate movement steps from walkbox path
 * Returns: number of movement steps generated
 */
uint16_t generate_movement_steps(RoomData *room,
                                uint8_t *path_buffer,
                                uint16_t path_length,
                                uint16_t start_x, uint16_t start_y,
                                uint16_t dest_x, uint16_t dest_y,
                                MovementStep *movement_buffer) {
    uint16_t current_x = start_x;
    uint16_t current_y = start_y;
    uint16_t movement_index = 0;

    // Generate movements for each walkbox in path
    for (uint16_t i = 0; i < path_length && path_buffer[i] != PATH_END; i++) {
        uint8_t box_index = path_buffer[i];
        Walkbox *box = &room->walkboxes[box_index];

        MovementStep step;
        calculate_movement_to_target(current_x, current_y,
                                    dest_x, dest_y,
                                    box, &step);

        if (step.distance_x > 0 || step.distance_y > 0) {
            movement_buffer[movement_index++] = step;

            // Update current position
            if (step.flags & MOVE_RIGHT) {
                current_x = box->x;
            } else if (step.flags & MOVE_LEFT) {
                current_x = box->x + box->width;
            }

            if (step.flags & MOVE_DOWN) {
                current_y = box->y;
            } else if (step.flags & MOVE_UP) {
                current_y = box->y + box->height;
            }
        }
    }

    // Final movement to exact destination
    MovementStep final_step;
    final_step.flags = 0;

    if (current_x < dest_x) {
        final_step.distance_x = dest_x - current_x;
        final_step.flags |= MOVE_RIGHT;
    } else if (current_x > dest_x) {
        final_step.distance_x = current_x - dest_x;
        final_step.flags |= MOVE_LEFT;
    } else {
        final_step.distance_x = 0;
    }

    if (current_y < dest_y) {
        final_step.distance_y = dest_y - current_y;
        final_step.flags |= MOVE_DOWN;
    } else if (current_y > dest_y) {
        final_step.distance_y = current_y - dest_y;
        final_step.flags |= MOVE_UP;
    } else {
        final_step.distance_y = 0;
    }

    if (final_step.distance_x > 0 || final_step.distance_y > 0) {
        movement_buffer[movement_index++] = final_step;
    }

    return movement_index;
}

/**
 * Pack movement direction and distance into 2 bytes
 * Format: [direction_flags:4][distance_x:3][distance_y:3][padding:6]
 */
uint16_t pack_movement(uint8_t flags, uint8_t dx, uint8_t dy) {
    uint16_t packed = 0;

    // Pack direction in upper nibble
    packed |= (flags & 0x0F) << 12;

    // Pack X distance (3 bits)
    packed |= (dx & 0x07) << 9;

    // Pack Y distance (3 bits)
    packed |= (dy & 0x07) << 6;

    return packed;
}

/**
 * Compress movement steps into efficient format
 * Returns: compressed path length in bytes
 */
uint16_t compress_movement_path(MovementStep *movement_buffer,
                               uint16_t movement_count,
                               uint8_t *compressed_path) {
    uint16_t compressed_index = 0;

    for (uint16_t i = 0; i < movement_count; i++) {
        MovementStep *step = &movement_buffer[i];
        uint8_t flags = step->flags;
        uint16_t dx = step->distance_x;
        uint16_t dy = step->distance_y;

        // Break large horizontal movements into chunks
        while (dx > MAX_STEP_X) {
            compressed_path[compressed_index++] = MOVEMENT_MARKER;
            uint16_t packed = pack_movement(flags & MOVE_HORIZ, MAX_STEP_X, 0);
            compressed_path[compressed_index++] = (uint8_t)(packed >> 8);
            compressed_path[compressed_index++] = (uint8_t)(packed & 0xFF);
            dx -= MAX_STEP_X;
        }

        // Break large vertical movements into chunks
        while (dy > MAX_STEP_Y) {
            compressed_path[compressed_index++] = MOVEMENT_MARKER;
            uint16_t packed = pack_movement(flags & MOVE_VERT, 0, MAX_STEP_Y);
            compressed_path[compressed_index++] = (uint8_t)(packed >> 8);
            compressed_path[compressed_index++] = (uint8_t)(packed & 0xFF);
            dy -= MAX_STEP_Y;
        }

        // Add remaining movement
        if (dx > 0 || dy > 0) {
            compressed_path[compressed_index++] = MOVEMENT_MARKER;
            uint16_t packed = pack_movement(flags, dx, dy);
            compressed_path[compressed_index++] = (uint8_t)(packed >> 8);
            compressed_path[compressed_index++] = (uint8_t)(packed & 0xFF);
        }
    }

    // Terminate path
    compressed_path[compressed_index++] = PATH_END;

    return compressed_index;
}

/* ============================================================================
 * Main Pathfinding Function
 * ============================================================================ */

/**
 * Calculate complete pathfinding from start to destination
 *
 * @param room      Room data with walkboxes
 * @param start_x   Starting X coordinate
 * @param start_y   Starting Y coordinate
 * @param dest_x    Destination X coordinate
 * @param dest_y    Destination Y coordinate
 * @param context   Pathfinding context (output)
 * @return          true if path found, false otherwise
 */
bool calculate_pathfinding(RoomData *room,
                          uint16_t start_x, uint16_t start_y,
                          uint16_t dest_x, uint16_t dest_y,
                          PathContext *context) {
    // Allocate buffers if not already allocated
    if (context->path_buffer == NULL) {
        context->path_buffer = (uint8_t*)malloc(MAX_PATH_LENGTH);
    }
    if (context->movement_buffer == NULL) {
        context->movement_buffer = (MovementStep*)malloc(MAX_MOVEMENT_STEPS * sizeof(MovementStep));
    }
    if (context->compressed_path == NULL) {
        context->compressed_path = (uint8_t*)malloc(MAX_COMPRESSED_PATH);
    }

    // Find starting and destination walkboxes
    uint8_t start_box = find_walkbox_for_point(room, start_x, start_y);
    uint8_t dest_box = find_walkbox_for_point(room, dest_x, dest_y);

    // Check if both points are in valid walkboxes
    if (start_box == 0xFF || dest_box == 0xFF) {
        printf("Error: Start or destination not in any walkbox\n");
        return false;
    }

    // Special case: same walkbox
    if (start_box == dest_box) {
        // Generate direct movement
        MovementStep direct_step;
        direct_step.flags = 0;

        if (start_x < dest_x) {
            direct_step.distance_x = dest_x - start_x;
            direct_step.flags |= MOVE_RIGHT;
        } else {
            direct_step.distance_x = start_x - dest_x;
            direct_step.flags |= MOVE_LEFT;
        }

        if (start_y < dest_y) {
            direct_step.distance_y = dest_y - start_y;
            direct_step.flags |= MOVE_DOWN;
        } else {
            direct_step.distance_y = start_y - dest_y;
            direct_step.flags |= MOVE_UP;
        }

        context->movement_buffer[0] = direct_step;
        context->movement_count = 1;
    } else {
        // Build walkbox path
        context->path_length = build_walkbox_path(room, start_box, dest_box,
                                                  context->path_buffer);

        if (context->path_length == 0) {
            printf("Error: No path found\n");
            return false;
        }

        // Generate movement steps
        context->movement_count = generate_movement_steps(room,
                                                         context->path_buffer,
                                                         context->path_length,
                                                         start_x, start_y,
                                                         dest_x, dest_y,
                                                         context->movement_buffer);
    }

    // Compress path
    context->compressed_length = compress_movement_path(context->movement_buffer,
                                                       context->movement_count,
                                                       context->compressed_path);

    return true;
}

/**
 * Free pathfinding context buffers
 */
void free_path_context(PathContext *context) {
    if (context->path_buffer) {
        free(context->path_buffer);
        context->path_buffer = NULL;
    }
    if (context->movement_buffer) {
        free(context->movement_buffer);
        context->movement_buffer = NULL;
    }
    if (context->compressed_path) {
        free(context->compressed_path);
        context->compressed_path = NULL;
    }
}

/* ============================================================================
 * Debug/Visualization Functions
 * ============================================================================ */

/**
 * Print walkbox information
 */
void print_walkbox(Walkbox *box, int index) {
    printf("Walkbox %d: x=%d, y=%d, w=%d, h=%d (x_max=%d, y_max=%d)\n",
           index, box->x, box->y, box->width, box->height,
           box->x + box->width, box->y + box->height);
}

/**
 * Print path information
 */
void print_path(PathContext *context) {
    printf("\nPath Information:\n");
    printf("================\n");

    printf("Walkbox path (%d boxes): ", context->path_length);
    for (int i = 0; i < context->path_length && context->path_buffer[i] != PATH_END; i++) {
        printf("%d ", context->path_buffer[i]);
    }
    printf("\n\n");

    printf("Movement steps (%d steps):\n", context->movement_count);
    for (int i = 0; i < context->movement_count; i++) {
        MovementStep *step = &context->movement_buffer[i];
        printf("  Step %d: ", i);

        if (step->flags & MOVE_RIGHT) printf("RIGHT ");
        if (step->flags & MOVE_LEFT) printf("LEFT ");
        if (step->flags & MOVE_DOWN) printf("DOWN ");
        if (step->flags & MOVE_UP) printf("UP ");

        printf("(dx=%d, dy=%d)\n", step->distance_x, step->distance_y);
    }

    printf("\nCompressed path (%d bytes): ", context->compressed_length);
    for (int i = 0; i < context->compressed_length; i++) {
        printf("%02X ", context->compressed_path[i]);
    }
    printf("\n");
}

/* ============================================================================
 * Example Usage
 * ============================================================================ */

int main() {
    // Example: Room 2 with 3 walkboxes
    RoomData room;
    room.walkbox_count = 3;

    // Walkbox 0: Main floor area
    room.walkboxes[0].x = 0;
    room.walkboxes[0].y = 0;
    room.walkboxes[0].width = 640;
    room.walkboxes[0].height = 200;
    room.walkboxes[0].flags = 0;

    // Walkbox 1: Left platform/stairs
    room.walkboxes[1].x = 50;
    room.walkboxes[1].y = 200;
    room.walkboxes[1].width = 200;
    room.walkboxes[1].height = 50;
    room.walkboxes[1].flags = 0;

    // Walkbox 2: Right platform
    room.walkboxes[2].x = 400;
    room.walkboxes[2].y = 200;
    room.walkboxes[2].width = 150;
    room.walkboxes[2].height = 50;
    room.walkboxes[2].flags = 0;

    printf("Room Walkboxes:\n");
    printf("===============\n");
    for (int i = 0; i < room.walkbox_count; i++) {
        print_walkbox(&room.walkboxes[i], i);
    }
    printf("\n");

    // Example pathfinding: from (100, 100) to (500, 220)
    PathContext context = {NULL, NULL, NULL, 0, 0, 0};

    uint16_t start_x = 100, start_y = 100;
    uint16_t dest_x = 500, dest_y = 220;

    printf("Calculating path from (%d, %d) to (%d, %d)...\n",
           start_x, start_y, dest_x, dest_y);

    if (calculate_pathfinding(&room, start_x, start_y, dest_x, dest_y, &context)) {
        printf("Path found!\n");
        print_path(&context);
    } else {
        printf("No path found!\n");
    }

    // Cleanup
    free_path_context(&context);

    return 0;
}
