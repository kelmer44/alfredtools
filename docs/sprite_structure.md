# Sprite/Animation (Object) Structure

## Overview

Sprites and animations in Alfred Pelrock are stored as **object structures** at the beginning of each room's data. These are separate from static hotspots but serve a similar interactive purpose.

## Location

- **Base offset**: Immediately after room header (starting at `room_data_ptr + 0x00`)
- **Count**: Stored at `room_data_ptr + 0x05` (1 byte) - number of objects
- **Structure size**: `0x2C` (44 bytes) per object
- **First object starts at**: `room_data_ptr + 0x06` (or varies by room header)

## Object Structure (44 bytes - 0x2C)

Based on the decompiled code from `check_mouse_interactions`:

```
Offset  Size  Field                  Description
------  ----  ---------------------  ------------------------------------------
+0x00   4     graphics_data_ptr      Pointer to graphics data
+0x04   2     ?                      Unknown
+0x06   4     graphics_offset        Offset within graphics data
+0x0A   2     x                      X position on screen
+0x0C   2     y                      Y position on screen
+0x0E   1     width                  Sprite width
+0x0F   1     height                 Sprite height
+0x10   2     stride                 Graphics data stride/pitch
+0x12   1     ?                      Unknown
+0x13   1     animation_frame?       Current animation frame or index
+0x14   ?     ?                      Unknown fields
+0x20   1     ?                      Some kind of offset or index
+0x21   1     flags/state            State byte (-1 = disabled?)
+0x22   ?     ?                      Unknown fields
+0x2A   2     object_id              Object ID (the "extra" field, uint16 LE)
+0x2C   1     type                   **Object type byte** (determines behavior)
+0x2D   ?     ?                      Unknown remaining bytes
```

## Key Fields

### Object ID (offset +0x2A, 2 bytes)
- 16-bit identifier for this sprite/animation
- Used for script lookups (like hotspot's "extra" field)
- Example: `0x0126`, `0x0135`, etc.

### Type Byte (offset +0x2C, 1 byte)
- **Critical field** that determines object behavior
- Controls which actions are available when interacting with this sprite
- Same dispatch system as static hotspots (see `FUN_00018562`)

Known type values:
- `0x01` - Standard interactive object
- `0x02` - Dialog/conversation trigger
- `0x08` - Special behavior
- `0x10`, `0x20`, `0x40`, `0x80` - Other specialized types

### Flags/State (offset +0x21, 1 byte)
- Value of `-1` (0xFF) appears to disable the object
- Used to check if object is clickable

### Position & Size (offsets +0x0A to +0x0F)
- `x, y` - Screen position where sprite is drawn
- `width, height` - Dimensions for hit detection
- Game checks if mouse is within these bounds

## Click Detection

From `check_mouse_interactions`, the game:

1. **Iterates through all objects** in the room (count from `+0x05`)
2. **Checks if mouse is within bounds**:
   ```c
   if (object.x <= mouse_x <= object.x + object.width &&
       object.y <= mouse_y <= object.y + object.height)
   ```
3. **Performs pixel-perfect hit detection** using graphics data:
   - Calculates offset into sprite graphics
   - Checks if pixel at mouse position is NOT transparent (-1/0xFF)
4. **If hit detected**:
   - Sets `hover_state = 0x01` (or `0x03` for first object)
   - Stores `DAT_00051757 = object.type` (the type byte)
   - Stores `DAT_0005175a = object.object_id` (the object ID)
   - Stores `DAT_00051758 = object_index`

## Hover State Values

When hovering over objects:
- `hover_state = 0x01` - Normal object/sprite
- `hover_state = 0x03` - First object (index 0) - special case

## Action Determination

Just like static hotspots, the **type byte** determines available actions:

1. When you long-click the sprite, `FUN_00018562` is called
2. It reads the stored `DAT_00051757` (type byte)
3. Dispatches to appropriate handler based on type
4. Handler populates `num_available_actions` with valid actions
5. Action popup menu shows only those actions

## Comparison: Objects vs Static Hotspots

| Feature              | Objects/Sprites (0x00)      | Static Hotspots (0x47A)  |
|----------------------|-----------------------------|--------------------------|
| Location             | Start of room data          | Pair 10 at offset 0x47C  |
| Structure size       | 44 bytes (0x2C)             | 9 bytes                  |
| Type byte offset     | +0x2C                       | +0x00                    |
| ID/Extra offset      | +0x2A (2 bytes)             | +0x07 (2 bytes)          |
| Has graphics         | Yes (animated sprites)      | No (invisible regions)   |
| Hover state value    | 0x01 or 0x03                | 0x02                     |
| Pixel-perfect check  | Yes (uses graphics data)    | No (rectangle only)      |

## Animation Support

Objects support animation through:
- **Frame index** (possibly at +0x13)
- **Graphics offset** (+0x06) - may change per frame
- **Animation sequences** - stored elsewhere, references object by ID

The animation system updates these fields each frame to create movement.

## Usage in Game

Objects/sprites are used for:
- **Characters** - NPCs, enemies, moving objects
- **Interactive items** - Objects you can pick up or examine
- **Animated scenery** - Fires, water, moving decorations
- **The player character** - First object (index 0) in many rooms

All interactive sprites have a type byte that determines which verbs/actions work on them!
