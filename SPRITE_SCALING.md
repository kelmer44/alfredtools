# Alfred Pelrock - Character Scaling System

## Overview

Alfred Pelrock uses a Y-position based character scaling system to create depth perspective. Characters appear smaller when walking toward the back of rooms (lower Y values) and normal size in the foreground (higher Y values).

## Key Functions (Ghidra)

- **init_character_scaling_tables** (0x00011e28): Creates lookup tables for perspective scaling at game startup
- **render_character_sprite_scaled** (0x00016ff8): Renders character with scaling applied
- **render_sprite** (0x00016d10): Renders sprites without scaling
- **load_room_data** (0x00015340): Loads room data and calculates initial scale values

## Scaling Parameters (ALFRED.1)

Located in each room's Pair 10 at offset **0x214** (4 bytes):

```
+0x214-0x215: y_threshold (uint16 LE) - Y coordinate where scaling begins
+0x216:       scale_divisor (uint8) - Controls rate of scaling
+0x217:       scale_mode (int8) - Scaling behavior mode
```

### Scale Modes

- **0x00**: Normal scaling (varies with Y position)
- **0xFF**: Maximum scaling (character always large)
- **0xFE**: No scaling (character always normal size)

## Scaling Algorithm

```c
// From load_room_data at offset ~0x15570
if (scale_mode == 0x00) {
    if (y_threshold < player_y) {
        // Player is below threshold (foreground)
        scale_down = 0;
        scale_up = 0;
    } else {
        // Player is above threshold (background)
        scale_delta = (y_threshold - player_y) / scale_divisor;
        scale_down = scale_delta;
        scale_up = scale_delta / 2;
    }
}

// Calculate final sprite dimensions
final_height = original_height - scale_down + scale_up;
final_width = original_width * (final_height / original_height);
```

### Original Character Size
- Width: 51 pixels
- Height: 102 pixels

## Example: Room 6

**Parameters:**
- y_threshold: 370
- scale_divisor: 4
- scale_mode: 0x00 (normal)

**Scaling at different Y positions:**

| Y Position | scale_down | scale_up | Final Size | Description |
|------------|------------|----------|------------|-------------|
| 0          | 92         | 46       | 28×56      | Far back (smallest) |
| 100        | 67         | 33       | 34×68      | Back area (33% smaller) |
| 200        | 42         | 21       | 40×81      | Mid area (21% smaller) |
| 370        | 0          | 0        | 51×102     | At threshold (normal) |
| 394        | 0          | 0        | 51×102     | Foreground (normal) |
| 399        | 0          | 0        | 51×102     | Bottom (normal) |

## How It Works

1. **Initialization**: `init_character_scaling_tables()` creates lookup tables mapping Y positions to scanline indices for scaling

2. **Room Loading**: `load_room_data()` reads scaling parameters and calculates initial scale values based on player position

3. **Rendering**: `render_character_sprite_scaled()` uses scale values to:
   - Skip `scale_down` scanlines (reduces height)
   - Duplicate some scanlines based on `scale_up` (partially restores height)
   - Net effect: `final_height = 102 - scale_down + scale_up`

4. **Visual Result**: Characters smoothly scale as they move:
   - Walking UP (toward y=0): Character gets progressively smaller
   - Walking DOWN (toward y=399): Character stays normal size below threshold

## Usage

### Calculate scaling for any room/position:

```bash
python calculate_character_scale.py ALFRED.1 <room_num> [y_pos]

# Show all scaling info for room 6
python calculate_character_scale.py ALFRED.1 6

# Calculate scaling at specific position
python calculate_character_scale.py ALFRED.1 6 100
```

### Extract all scaling data:

```bash
python extract_scaling.py ALFRED.1 output_dir/
```

## Notes

- Not all rooms use scaling (some have mode 0xFE = no scaling)
- The threshold is typically set where the "floor" begins in the room's perspective
- Rooms with unusual perspective (like Room 21) use special modes
- The system creates believable depth without needing 3D graphics
