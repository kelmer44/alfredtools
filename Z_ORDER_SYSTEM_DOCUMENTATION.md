# Z-Order System Documentation

## Quick Reference

**What determines sprite layering?**
- Each sprite has a **Z-depth value** (byte at offset +0x21, range 0-255)
- **Higher Z = Background** (rendered first)
- **Lower Z = Foreground** (rendered last)
- Value **0xFF = Disabled** (not rendered)

**How Alfred interacts:**
- Alfred is **excluded from normal sprite queue**
- His **Y-position determines his effective Z-depth**
- Lower Y (higher on screen) = lower Z = in front of objects
- Higher Y (lower on screen) = higher Z = behind objects

**Dynamic Z-changes:**
- Z-depth can change **per animation frame** using movement flags
- Bit 14 (0x4000): Enable Z-movement
- Bit 13 (0x2000): Direction (0=backward, 1=forward)

---

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ FRAME UPDATE (update_npc_sprite_animations)             │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 1. Loop through all sprite slots                        │
│    ├─ Skip Alfred (sprite index 0 / current_room)       │
│    ├─ Skip disabled sprites (z_depth == 0xFF)           │
│    └─ For each active sprite:                           │
│        ├─ Update animation frame counters               │
│        ├─ Apply movement flags (X, Y, Z movement)       │
│        ├─ Check screen bounds (disable if off-screen)   │
│        └─ Add to render queue:                          │
│            ├─ frame_ptr (sprite graphic data)           │
│            ├─ x, y (position)                           │
│            ├─ width, height                             │
│            ├─ z_depth (from sprite_struct[0x21])        │
│            └─ character_flag (0 = normal sprite)        │
│                                                          │
│ 2. Sort render queue by Z-depth (bubble sort)           │
│    ├─ Descending order: high Z → low Z                  │
│    └─ Result: back-to-front rendering order             │
│                                                          │
│ 3. Render all sprites in sorted order                   │
│    └─ For each queue entry:                             │
│        ├─ if z_depth == 0xFF: skip                      │
│        ├─ if character_flag == 1: render_scaled()       │
│        └─ else: render_sprite()                         │
│                                                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ ALFRED RENDERING (separate path)                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ - Alfred's sprite slot is DISABLED (z_depth = 0xFF)     │
│ - Rendered via setup_alfred_frame_from_state()          │
│ - Y-position determines effective Z-depth                │
│ - Uses render_character_sprite_scaled()                 │
│                                                          │
│ Comparison logic (inferred):                             │
│   if alfred_y_position < sprite_y_position:              │
│       Alfred renders behind sprite                       │
│   else:                                                  │
│       Alfred renders in front of sprite                  │
│                                                          │
└─────────────────────────────────────────────────────────┘

VISUAL EXAMPLE:
═══════════════════════════════════════════════════════════
Screen Y=0 (top)
     │
     ├─ Sprite A (Y=100, Z=50) ───┐
     │                             │ Alfred Y=150
     ├─ Sprite B (Y=200, Z=100) ──┼─ appears between
     │                             │ these sprites
     │  [Alfred at Y=150]          │
     │                             │
     ├─ Sprite C (Y=250, Z=150) ──┘
     │
Screen Y=400 (bottom)

Render order: Background → Sprite A → Alfred → Sprite B → Sprite C → Foreground
═══════════════════════════════════════════════════════════
```

---

## Overview

The game uses a **Z-depth sorting system** to determine which sprites are drawn in front of or behind other sprites, including the player character Alfred. This is a critical system for creating the illusion of depth in the 2D game world.

## Key Findings

### 1. Z-Depth Value Storage

Each sprite has a **Z-depth value** stored in its sprite structure:
- **Location**: `sprite_struct[0x21]` (byte offset 0x21 in the sprite data structure)
- **Value Range**: 0-255 (byte value)
- **Special Value**: `0xFF` = sprite is disabled/not rendered
- **Higher values** = further back in the scene (background)
- **Lower values** = closer to the front/camera (foreground)

### 2. Sprite Data Structure

```
SPRITE/ANIMATION STRUCTURE (room_data_ptr + sprite_id * 0x2C):
File format (44 bytes as stored in ALFRED.1):

+0x00-0x05: Unknown header (zeros in file)
+0x06-0x09: Sprite graphic data pointer (zeros in file, overwritten at runtime)
+0x0A: X coordinate (short)
+0x0C: Y coordinate (short)
+0x0E: Sprite width (byte)
+0x0F: Sprite height (byte)
+0x10: Stride/bytes per row (short)
+0x12: Number of animation sequences (byte)
+0x13: Current animation sequence index (byte) - runtime
+0x14-0x17: Number of frames in each sequence (4 bytes, one per sequence)
+0x18-0x1B: Loop count for each sequence (4 bytes, 0xFF = infinite)
+0x1C+: Frame delay/duration array (variable length, 1 byte per total frame)
+0x20: Current frame index in sequence (byte) - runtime
+0x21: Current Z-depth layer (byte, 0xFF = disabled) ⭐ KEY FIELD
+0x22-0x29: Movement flags (16-bit per sequence, NOT per frame) ⭐ CORRECTED
+0x2A-0x2B: Unknown (2 bytes)

Runtime-only fields (not in 44-byte file structure):
+0x2D: Frame delay counter (byte) - engine adds this
+0x2E: Loop counter (byte) - engine adds this
+0x31: Disable after sequence flag (byte) - engine adds this
```

**Note**: The structure is 44 bytes in the file, but the engine allocates additional runtime fields beyond offset 0x2B for animation state tracking.

### 3. Z-Depth Modification During Animation

The Z-depth value can **change dynamically** during sprite animation through movement flags:

#### Movement Flags Structure (16-bit value at sprite_struct[0x22 + sequence_index*2])

**CRITICAL**: Movement flags are stored **per sequence**, not per frame!
- `movement_flags = *(ushort *)(sprite_ptr + current_anim_sequence * 2 + 0x22)`
- All frames in a sequence share the same movement behavior

```
Bits 0-2:    X movement amount (0-7 pixels per frame)
Bit 3:       Enable flag for X-axis movement (0x08)
Bit 4:       X direction flag (0x10): 0=left/subtract, 1=right/add
Bits 5-7:    Y movement type/speed (0xE0)
Bit 8:       Y direction flag (0x100): 0=up/subtract, 1=down/add
Bit 9:       Enable flag for Y-axis movement (0x200)
Bits 10-12:  Z movement amount (0x1C00): 0-7 depth units per frame
Bit 13:      Z-depth direction (0x2000): 0=back, 1=forward ⭐
Bit 14:      Enable Z-depth movement (0x4000) ⭐
Bit 15:      Unused/Unknown
```

**Z-Depth Movement Code** (from `update_npc_sprite_animations`):
```c
local_3c = (bVar11 & 0x1c) << 8;         // Extract bits for Z movement amount
local_64 = local_3c >> 10;                // Shift to get movement delta
local_44 = (bVar11 & 0x40) << 8;          // Check if Z movement enabled (0x4000)
local_58 = (bVar11 & 0x20) << 8;          // Check Z direction (0x2000)

if ((short)local_44 != 0) {               // If Z movement is enabled
    if ((short)local_58 == 0) {
        z_depth = z_depth - movement_delta;  // Move backward
    } else {
        z_depth = z_depth + movement_delta;  // Move forward
    }
}
```

### 4. Render Queue and Sorting

The game uses a **render queue system** with bubble sort to order sprites by Z-depth:

#### Render Queue Structure

Each entry in the render queue contains:
- `render_queue_frame_ptr`: Pointer to sprite frame data
- `render_queue_x`: X coordinate (2 bytes)
- `render_queue_y`: Y coordinate (stored as part of position data)
- `render_queue_width`: Sprite width (2 bytes)
- `render_queue_height`: Sprite height (2 bytes)
- `render_queue_z_depth`: **Z-depth value** (byte) + special flag

#### Sorting Algorithm

After all sprites are added to the queue, the game performs a **bubble sort**:

```c
// Bubble sort by Z-depth (DESCENDING order - high to low)
for (pass = sprite_count; pass != 1; pass--) {
    for (i = sprite_count - 1; i > 0; i--) {
        // Compare Z-depth values: if previous < current, SWAP
        // This moves HIGHER values toward the START of the array
        if (render_queue[i-1].z_depth < render_queue[i].z_depth) {
            // Swap entries if out of order
            swap(render_queue[i-1], render_queue[i]);
        }
    }
}
```

**Sorting Order**: Sprites are sorted in **DESCENDING Z-depth order** (highest to lowest), meaning:
- Sprites with **higher Z values** are rendered **first** (appear in back)
- Sprites with **lower Z values** are rendered **last** (appear in front)

### 5. Alfred's Position in Z-Order

Alfred (the player character) is handled specially:

#### Alfred's Sprite Structure
- Alfred is stored at **sprite index 0** (first sprite slot: `local_1c`)
- His sprite data is at `room_sprite_data_ptr + 0x00`
- His Z-depth is at `room_sprite_data_ptr + 0x21`

#### Sprite Loop and Alfred Exclusion

The key code in `update_npc_sprite_animations`:
```c
bVar14 = (byte)((uint)iVar17 >> 8);
while (bVar14 < bVar16) {  // Loop through all sprite slots
    // KEY CHECK: Skip Alfred's sprite slot (local_1c = current room/alfred index)
    if ((bVar14 != local_1c) &&
        (iVar19 = room_sprite_data_ptr + (uint)bVar14 * 0x2c,
         *(char *)(iVar19 + 0x21) != -1)) {
        // Process sprite animation and add to render queue
        ...
    }
    bVar14 = bVar14 + 1;
}
```

**Critical Insight**: The condition `bVar14 != local_1c` **excludes Alfred's sprite slot** from the normal sprite processing loop. Alfred is NOT added to the render queue during sprite animation updates.

#### Alfred's Separate Rendering

From `setup_alfred_frame_from_state`:
```c
// Mark Alfred's sprite slot as disabled
*(undefined1 *)(room_sprite_data_ptr + 0x21) = 0xff;

// But set up separate render parameters
alfred_render_enabled = 1;

// Special case: In room 0x15, add to render queue
if ((current_room_number == 0x15) && (1 < mouse_hover_state)) {
    render_queue_frame_ptr = mouse_cursor_frame_ptr;
    render_queue_z_depth._0_1_ = 1;
    render_queue_width._0_2_ = mouse_cursor_width;
    ...
}
```

Alfred is rendered **outside the normal sprite queue** in most rooms!

#### Special Rendering Flag

The render queue has a **special flag** at offset +1 from the Z-depth:
```c
render_queue_z_depth + 0x01 = character_flag (0x01 = Alfred/character sprite)
```

From the rendering loop:
```c
if ((character_flag == 0x01) && (z_depth != 0xFF)) {
    render_character_sprite_scaled(...);  // Render Alfred with scaling
} else if (z_depth != 0xFF) {
    render_sprite(...);                    // Render normal sprite
}
```

### 6. How Alfred Actually Interacts with Sprites - THE ANSWER

**MAJOR DISCOVERY**: Looking at the code more carefully, Alfred is **NOT in the sorted sprite queue**. Instead:

1. **All room sprites** are processed, sorted by Z-depth, and added to render queue
2. **Alfred is skipped** during sprite queue building (`bVar14 != local_1c`)
3. Sprites are **rendered in sorted order** (back to front by Z-depth)
4. **Alfred must be rendered at a specific point** in the sprite rendering loop

The key is in `update_npc_sprite_animations` rendering section:
```c
for (local_28 = 0; local_28 < local_34; local_28 = local_28 + 1) {
    // Get sprite at this queue position
    iVar17 = (uint)local_28 * 0xe;

    if ((character_flag == 0x01) && (z_depth != 0xFF)) {
        // Render scaled character sprite (Alfred or NPCs)
        render_character_sprite_scaled(...);
    } else if (z_depth != 0xFF) {
        // Render normal sprite
        render_sprite(...);
    }
}
```

**The character_flag mechanism**: Certain sprites in the queue are marked with `character_flag = 0x01`. These are rendered with scaling. But where is Alfred inserted?

#### The Real Z-Order Mechanism

After more analysis, the system works like this:

1. **Sprites are added to queue** with their Z-depth values from `sprite_struct[0x21]`
2. **Queue is sorted** by Z-depth (ascending = back to front)
3. **During rendering**, sprites marked with character_flag use scaled rendering
4. **Alfred's Y-position determines his effective Z-depth** for comparison with sprite Y-positions

#### Y-Position Based Z-Ordering

From the code analysis:

```c
// In update_npc_sprite_animations, render queue entries are populated:
*(char *)(&render_queue_z_depth + uVar4 * 7) = (char)uVar10;  // Z-depth
*(undefined1 *)((int)&render_queue_z_depth + uVar4 * 0xe + 1) = 0;  // Normal sprite flag
```

Each sprite entry has:
- **Z-depth byte** at `render_queue_z_depth + index * 7` (or `index * 0xe` depending on access)
- **Character flag byte** at `render_queue_z_depth + index * 0xe + 1`

The character flag is set to `0` for normal sprites during sprite animation updates.

**Key Discovery About Alfred**: Looking at `setup_alfred_frame_from_state`, in room 0x15 (inventory screen):
```c
if ((current_room_number == 0x15) && (1 < mouse_hover_state)) {
    render_queue_frame_ptr = mouse_cursor_frame_ptr;
    render_queue_z_depth._0_1_ = 1;  // Character flag = 1!
    ...
}
```

This shows the character_flag (`render_queue_z_depth + 1`) is set to `1` for character/Alfred rendering.

**The Z-Order Mechanism**:

1. **Sprites store static Z-depth** in their data structure at offset +0x21
2. **Sprites can modify Z-depth dynamically** via movement flags during animation
3. **Sprites are sorted by Z-depth** (back to front) before rendering
4. **Alfred's Y-position likely maps to a Z-depth value** for comparison
5. In pseudo-3D games: **higher Y coordinate** (lower on screen) = **higher Z-depth** = **closer to camera**

**Expected formula**:
```
alfred_z_depth ≈ alfred_y_position / scale_factor
```

This allows Alfred to:
- Walk **behind** sprites when he's "above" them (lower Y, lower Z-depth)
- Walk **in front of** sprites when "below" them (higher Y, higher Z-depth)

### 7. Per-Sequence Z-Depth Changes

**Critical Discovery**: The Z-depth can change **per animation sequence** (not per frame!) through the movement flags. This allows:

- **Animated sprites to move between depth layers** when switching sequences
- **Characters/NPCs to walk "around" objects** by using different sequences for different depth
- **Dynamic depth transitions** (e.g., a character switching from "walking behind" to "walking in front" sequence)

**Correction**: Movement flags are per-sequence, so all frames in a sequence share the same movement behavior. To create complex depth transitions, use multiple sequences with different movement flags.

## Practical Applications

### For Game Developers
1. Set sprite Z-depth values at design time for static depth
2. Use movement flags (bits 13-14) for dynamic Z changes during animation
3. Lower Z = background, Higher Z = foreground
4. Value 0xFF disables the sprite completely

### For Modders

#### Example 1: Making a Sprite Always In Front
```
Offset +0x21: Set to 0 or 1 (low value)
Result: Sprite will always render in front of everything
```

#### Example 2: Making a Sprite Always In Back
```
Offset +0x21: Set to 254 or 0xFE (0xFF is disabled, so use 254)
Result: Sprite will always render behind everything
```

#### Example 3: Animated Depth Change
To make a sprite move from background to foreground during animation:

```
Frame 0: Z-depth = 50, Movement flags = 0x6000
         (Bits 13-14 = 11 binary = move forward, Z enabled)

Frame 1-10: Z-depth automatically increments by movement amount

Frame 11: Z-depth = ~60+, Movement flags = 0x0000
         (Stop Z movement)
```

Movement flag bit pattern:
```
0x6000 = 0110 0000 0000 0000 binary
         ││└─ Bit 13: Z direction (1 = forward)
         │└── Bit 14: Z movement enabled
         └─── Bits 10-12: Movement amount (configurable)
```

#### Example 4: Character Walking Behind Then In Front of Object
```
Sprite (table) at Y=200, Z=100

Alfred walks from Y=150 → Y=250:
- At Y=150: Alfred Z≈75 (lower Y = lower Z) → appears IN FRONT of table
- At Y=200: Alfred Z≈100 → same depth as table
- At Y=250: Alfred Z≈125 (higher Y = higher Z) → appears BEHIND table

No code change needed - automatic based on Y-position!
```

### For Reverse Engineers
1. The sorting happens in `update_npc_sprite_animations` @ 0x0001628D
2. Render queue is at memory locations starting with `render_queue_frame_ptr`
3. Each queue entry is 0x0E (14) bytes
4. Z-depth sorting uses simple bubble sort (O(n²) but fine for small sprite counts)
5. Sprite structure is 0x2C (44) bytes per sprite
6. Z-depth comparison in bubble sort:
   ```c
   if (render_queue[i-1].z_depth < render_queue[i].z_depth) {
       swap(render_queue[i-1], render_queue[i]);
   }
   ```

## Summary: Complete Z-Order System

### How It Works

1. **Each sprite has a Z-depth byte** at offset +0x21 in its structure (0-255, 0xFF = disabled)

2. **Sprites are updated every frame**:
   - Position (X, Y) can change via movement flags
   - Z-depth can change via movement flags (bits 13-14)
   - Animation frames advance based on timers

3. **Render queue is built**:
   - All active sprites (Z-depth ≠ 0xFF) are added to queue
   - Alfred's sprite slot (index 0 = current room number) is **skipped**
   - Each queue entry contains: frame_ptr, x, y, width, height, z_depth, character_flag

4. **Queue is sorted by Z-depth** using bubble sort (ascending order = back to front)

5. **Rendering happens in sorted order**:
   - Sprites with lower Z-depth render first (background)
   - Sprites with higher Z-depth render last (foreground)
   - Character flag determines if scaled rendering is used

6. **Alfred is rendered separately**:
   - His sprite slot is disabled (0xFF) in normal sprite array
   - He's rendered via `render_character_sprite_scaled()`
   - **His Y-position likely determines where he renders relative to other sprites**
   - This allows him to walk behind/in front of objects naturally

### The Key Insight

**Sprites with lower Y-coordinates** (higher on screen) are typically **further away** (lower Z-depth).
**Sprites with higher Y-coordinates** (lower on screen) are typically **closer** (higher Z-depth).

This creates a pseudo-3D depth effect where:
- Characters walking "up" the screen appear to go behind objects
- Characters walking "down" the screen appear to come in front of objects

### For Game Modders

To control sprite layering:
1. **Static layering**: Set sprite Z-depth at offset +0x21 (0=back, 255=front)
2. **Dynamic layering**: Use movement flags bits 13-14 to change Z-depth during animation
3. **Disable sprites**: Set Z-depth to 0xFF

## Open Questions

1. **Exact calculation of Alfred's Z-depth**: Need to find the specific function that converts Alfred's Y-position to Z-depth for comparison
2. **Default Z-depth values**: What are typical Z-depth ranges used in different room types?
3. **Room-specific rules**: Are there any room-specific Z-ordering overrides or special cases?
4. **Scaling relationship**: How does sprite scaling factor relate to Z-depth? (Likely: closer = bigger = higher Z-depth)
5. **Alfred insertion point**: Where exactly is Alfred inserted into the rendering sequence? Is there a comparison loop?

## Related Systems

- **Sprite Scaling**: Sprites can be scaled based on Y-position (see `render_character_sprite_scaled`)
- **Walkbox System**: Determines where Alfred can walk, may influence Z-depth
- **Screen Bounds**: Sprites are disabled if they move off-screen (X >= 640, Y >= 400, or negative)

## Function Reference

- `update_npc_sprite_animations()` @ 0x0001628D - Main sprite update and Z-sorting
- `render_sprite()` @ 0x00016D10 - Renders normal sprites
- `render_character_sprite_scaled()` @ 0x00016FF8 - Renders Alfred with scaling
- `setup_alfred_frame_from_state()` @ 0x000147C9 - Sets up Alfred's render parameters
- `render_scene()` @ 0x00015E4C - Main scene rendering coordinator
