# Water Reflection Effect Documentation

## Overview

The game implements a water reflection effect visible in **Room 25 (0x19)** and **Room 45 (0x2D)**. This effect creates a mirrored reflection of Alfred's sprite on the water surface, visible only where water pixels exist.

## How It Works

### Trigger Condition

The reflection effect is activated when:
1. `current_room_number == 0x19` (Room 25) OR `current_room_number == 0x2D` (Room 45)
2. Alfred's Y position + sprite height > 0x129 (297 decimal)

This means the reflection only appears when Alfred is standing near the bottom of the screen (in the water area).

### Reflection Offset Calculation

The reflection vertical offset (`local_1c` in decompiled code) is calculated differently per room:

```c
// For Room 25 (0x19):
offset = ((current_room_number - 0x15) * 8) + 3;
// = (0x19 - 0x15) * 8 + 3 = 4 * 8 + 3 = 35

// For Room 45 (0x2D):
offset = 0x19 = 25  // Hardcoded override
```

This offset determines how far below Alfred's feet the reflection appears.

### Water Pixel Detection (Masking)

The key insight is that the reflection uses **palette index checking** as a mask:

```c
// From render_alfred_sprite_scaled at 0x17401-0x1740f:
if ((screen_buffer_ptr[reflection_offset] >= 0xDF) &&
    (screen_buffer_ptr[reflection_offset] < 0xE4)) {
    // This pixel is water - draw reflection
    screen_buffer_ptr[reflection_offset] = remap_table[sprite_pixel];
}
```

**Water is identified by palette indices 0xDF to 0xE3 (223-227 decimal).**

Only pixels in this palette range receive the reflection. This means the water area in the room background uses these specific palette indices.

### Palette Remapping Table

The reflection uses a color remapping table at `DAT_0004957c` (offset `0x4957c` in the EXE data segment). This creates the "underwater" tinted appearance:

```c
screen_buffer_ptr[reflection_position] = remap_table[source_sprite_pixel];
```

This maps each original sprite color to a water-tinted equivalent (likely more blue/cyan tinted).

### Reflection Position Calculation

For each pixel drawn:
1. The normal sprite pixel is drawn at `screen_buffer_ptr`
2. The reflection pixel is calculated at:
   ```c
   reflection_y = (offset + (current_row - start_row) * 2) * 0x280;
   // 0x280 = 640 = screen width
   ```

The `* 2` factor creates the mirror effect - for each row down in the source sprite, the reflection goes 2 rows down from the reflection start point.

### Additional Check in render_alfred_sprite_scaled

There's also a check for sprite pixels themselves:
```c
if ((*sprite_pixel != 0xFF) &&  // Not transparent
    (background_pixel >= 0xDF) && (background_pixel < 0xE4)) {  // Is water
    // Draw reflection
}
```

## Code Locations

| Function | Address | Purpose |
|----------|---------|---------|
| `render_alfred_sprite_scaled` | 0x00016ff8 | Main Alfred rendering with reflection |
| `render_sprite` | 0x00016d10 | Generic sprite rendering with reflection |

### Key Addresses in render_alfred_sprite_scaled

- **0x171D0-0x171DA**: Room number check (`current_room_number == 0x19 || current_room_number == 0x2D`)
- **0x171E7-0x171EC**: Y threshold check (`> 0x12A` = 298)
- **0x1730D-0x1732A**: Offset calculation
- **0x17401-0x17417**: Water check and reflection write

## Data Structures

### Palette Remap Table

Location: `0x0004957c` (256 bytes)

Maps original sprite palette indices to water-tinted versions.

### Water Palette Range

| Index | Hex | Purpose |
|-------|-----|---------|
| 223 | 0xDF | Water start |
| 224 | 0xE0 | Water |
| 225 | 0xE1 | Water |
| 226 | 0xE2 | Water |
| 227 | 0xE3 | Water end |

## Implementation Notes for ScummVM

To recreate this effect:

1. **Check room number**: Only apply for rooms 25 and 45
2. **Check Y position**: Only when Alfred is below Y=297
3. **Calculate offset**: Use the formula `(room - 0x15) * 8 + 3` or hardcode 25 for room 45
4. **For each sprite pixel**:
   - Draw the normal pixel
   - Calculate reflection position: `y_reflect = alfred_feet_y + offset + (row * 2)`
   - Check if background at reflection position is water (palette 0xDF-0xE3)
   - If water, write remapped color from the remap table

### Pseudo-code

```cpp
void renderAlfredWithReflection(int x, int y, byte *spriteData, int width, int height) {
    // Normal rendering
    for (int row = 0; row < height; row++) {
        for (int col = 0; col < width; col++) {
            byte pixel = spriteData[row * width + col];
            if (pixel != 0xFF) {
                drawPixel(x + col, y + row, pixel);
            }
        }
    }

    // Reflection (rooms 25 and 45 only)
    if ((currentRoom == 25 || currentRoom == 45) && (y + height > 297)) {
        int offset = (currentRoom == 45) ? 25 : ((currentRoom - 0x15) * 8 + 3);

        for (int row = 0; row < height; row++) {
            int reflectY = y + height + offset + (row * 2);
            if (reflectY >= 400) break;  // Screen boundary

            for (int col = 0; col < width; col++) {
                byte pixel = spriteData[(height - 1 - row) * width + col];  // Read from bottom up for mirror
                if (pixel != 0xFF) {
                    byte bgPixel = getPixel(x + col, reflectY);
                    if (bgPixel >= 0xDF && bgPixel < 0xE4) {  // Is water
                        drawPixel(x + col, reflectY, waterRemapTable[pixel]);
                    }
                }
            }
        }
    }
}
```

## Visual Representation

```
    +------------------+
    |    Room 25       |
    |                  |
    |    [Alfred]      |  <- Normal sprite
    |       |          |
    |       v          |  <- Y > 297 threshold
    |~~~~~~~|~~~~~~~~~~|  <- Water surface (palette 0xDF-0xE3)
    |   [Reflection]   |  <- Mirrored, only on water pixels
    |                  |
    +------------------+
```

## Rooms with Water Reflection

| Room | Hex | Description |
|------|-----|-------------|
| 25 | 0x19 | Offset = 35 pixels |
| 45 | 0x2D | Offset = 25 pixels |
