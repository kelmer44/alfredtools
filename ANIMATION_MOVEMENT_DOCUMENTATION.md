# Animation Movement System Documentation

## Overview
Based on analysis of the decompiled code in Ghidra, animations in the game can not only display sprites in succession but also move them across the screen. This movement is controlled by **movement flags** stored in the animation structure.

## Animation Structure Location
- Room 21 animations start at offset: **0x3B6181**
- Each sprite/animation has a structure of **0x2C (44) bytes**
- Structure is located at: `room_data_ptr + sprite_id * 0x2C`

## Sprite/Animation Structure (In-Memory Runtime Structure)

The game uses a DIFFERENT structure at runtime than what's in the file. Based on Ghidra analysis:

```
Offset | Size | Description
-------|------|-------------
+0x00  | 6B   | Unknown header data
+0x06  | 4B   | Pointer to sprite graphic data
+0x0A  | 2B   | X coordinate (signed short) - UPDATED BY MOVEMENT
+0x0C  | 2B   | Y coordinate (signed short) - UPDATED BY MOVEMENT
+0x0E  | 1B   | Sprite width (byte)
+0x0F  | 1B   | Sprite height (byte)
+0x10  | 2B   | Stride/bytes per row (ushort)
+0x12  | 1B   | Number of animation sequences (byte)
+0x13  | 1B   | Current animation sequence index (byte)
+0x14  | []   | Array: Number of frames per sequence (indexed by sequence)
+0x18  | []   | Array: Loop count per sequence (0xFF = infinite loop)
+0x1C  | []   | Array: Frame delay/duration (indexed by frame)
+0x20  | 1B   | Current frame index in sequence (byte)
+0x21  | 1B   | Current Z-depth/layer (0xFF = disabled) - UPDATED BY MOVEMENT
+0x22  | []   | Array: Movement flags (16-bit per frame, indexed by frame)
+0x2D  | 1B   | Frame delay counter (byte)
+0x2E  | 1B   | Loop counter (byte)
+0x31  | 1B   | Disable after sequence flag (byte)
```

**IMPORTANT**: The file format structure (44 bytes) is DIFFERENT from the runtime structure.
The movement flags in the file are stored AFTER all sprite headers, not within each header.

## Movement Flags Structure (16-bit value)

The movement flags are stored at offset `+0x22 + (frame_index * 2)` in the sprite structure. Each frame can have its own movement parameters.

### Bit Layout

```
Bit(s)  | Mask   | Description
--------|--------|-------------
0-2     | 0x0007 | Movement amount (0-7 pixels per frame)
3       | 0x0008 | Enable flag for X-axis movement
4       | 0x0010 | X direction: 0=left/subtract, 1=right/add
5-7     | 0x00E0 | Movement speed/amount for Y-axis
8       | 0x0100 | Y direction: 0=up/subtract, 1=down/add
9       | 0x0200 | Enable flag for Y-axis movement
10-12   | 0x1C00 | Z-depth movement amount (bits 10-12)
13      | 0x2000 | Z direction: 0=back, 1=forward
14      | 0x4000 | Enable Z-depth movement
15      | 0x8000 | (Reserved/unused)
```

### Examples

**Move right by 3 pixels per frame:**
```
Flags: 0x0018
- Bits 0-2 = 3 (amount)
- Bit 3 = 1 (enable X)
- Bit 4 = 1 (direction right)
Binary: 0000 0000 0001 1000
```

**Move left by 2 pixels per frame:**
```
Flags: 0x000A
- Bits 0-2 = 2 (amount)
- Bit 3 = 1 (enable X)
- Bit 4 = 0 (direction left)
Binary: 0000 0000 0000 1010
```

**Move down by 4 pixels per frame:**
```
Flags: 0x0380
- Bits 5-7 = 4 (amount, shifted left by 5)
- Bit 8 = 1 (direction down)
- Bit 9 = 1 (enable Y)
Binary: 0000 0011 1000 0000
```

**Move diagonally (right 2, down 3):**
```
Flags: 0x037A
- Bits 0-2 = 2 (X amount)
- Bit 3 = 1 (enable X)
- Bit 4 = 1 (right)
- Bits 5-7 = 3 (Y amount)
- Bit 8 = 1 (down)
- Bit 9 = 1 (enable Y)
Binary: 0000 0011 0111 1010
```

## Code Location

The movement logic is in the function `render_and_update_animated_sprites` (formerly `update_and_sort_sprites`) at address **0x0001628D**.

### Key Code Sections

**Reading movement flags (0x0001631E):**
```c
movement_flags = *(ushort *)(sprite_ptr + anim_frame_index * 2 + 0x22);
```

**X-axis movement (0x000163B5 - 0x000163EA):**
```c
if (movement_flags & 0x10) {  // Bit 4: X-axis enabled
    short amount = movement_flags & 0x07;  // Bits 0-2
    if (movement_flags & 0x08) {  // Bit 3: direction
        x_coord += amount;  // Move right
    } else {
        x_coord -= amount;  // Move left
    }
}
```

**Y-axis movement (0x000163EA - 0x00016404):**
```c
if (movement_flags & 0x200) {  // Bit 9: Y-axis enabled
    int movement_type = (movement_flags & 0xE0) >> 5;  // Bits 5-7
    if (movement_flags & 0x100) {  // Bit 8: direction
        y_coord += movement_type;  // Move down
    } else {
        y_coord -= movement_type;  // Move up
    }
}
```

**Z-depth movement (0x00016404 - 0x0001641E):**
```c
if (movement_flags & 0x4000) {  // Bit 14: Z-depth enabled
    int z_amount = (movement_flags & 0x1C00) >> 10;  // Bits 10-12
    if (movement_flags & 0x2000) {  // Bit 13: direction
        z_depth += z_amount;  // Move forward
    } else {
        z_depth -= z_amount;  // Move back
    }
}
```

**Storing updated coordinates (0x0001642B - 0x00016441):**
```c
*(short *)(sprite_ptr + 0x0A) = x_coord;  // Store X
*(short *)(sprite_ptr + 0x0C) = y_coord;  // Store Y
*(byte *)(sprite_ptr + 0x21) = z_depth;   // Store Z
```

## Animation 3 in Room 21

Animation 3 in room 21 demonstrates this movement system by:
1. Displaying sprites in succession (normal animation)
2. Using movement flags for each frame to move the sprite across the screen
3. The movement flags are checked and applied every frame in the render loop

The data for these movement flags starts at offset 0x3B6181 + (sprite_offset), specifically at the `+0x22` offset within the sprite structure.

## Extracting Movement Data

To extract the movement data for a specific animation:

1. Locate the sprite structure: `0x3B6181 + (sprite_id * 0x2C)`
2. Read the number of frames: byte at `+0x14 + sequence_index`
3. For each frame index (0 to num_frames-1):
   - Read 2 bytes at `+0x22 + (frame_index * 2)`
   - Parse the bits according to the movement flags structure above

## Implementation Notes

- Movement is applied **per frame** during the animation
- Screen bounds checking is performed at 0x00016461-0x00016487
- If sprite moves out of bounds (x > 640 or y > 400), it's disabled (z_depth set to 0xFF)
- The movement system allows complex sprite paths by varying flags per frame
- Z-depth affects rendering order (higher values render on top)
