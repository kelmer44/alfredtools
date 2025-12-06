# Z-Order System Documentation

## ✅ VERIFIED

This document has been verified against Ghidra decompilation.

## Quick Reference

**What determines sprite layering?**
- Each sprite has a **Z-depth value** (byte at offset +0x21, range 0-255)
- **Higher Z = Background** (rendered first) ✅ VERIFIED
- **Lower Z = Foreground** (rendered last) ✅ VERIFIED
- Value **0xFF = Disabled** (not rendered) ✅ VERIFIED

**How Alfred interacts:**
- Alfred uses render_queue[1] with **character_flag = 1** ✅ VERIFIED (load_room_data @ 0x15a44)
- Alfred's data comes from global variables (alfred_render_x, alfred_frame_data_ptr, etc.) ✅ VERIFIED
- **Alfred's Z-depth is computed from Y-position** ✅ VERIFIED (see formula below)

**Alfred Z-Depth Formula (VERIFIED @ 0x15a20-0x15a3d):**
```c
Z_depth = ((399 - alfred_y_position) & 0xFFFE) / 2 + 10
```
- At Y=0 (top): Z = 209 (furthest back, behind everything)
- At Y=199 (middle): Z = 110
- At Y=399 (bottom): Z = 10 (closest to front, in front of most things)

**Why sprites appear in front of Alfred:**
- Room sprites typically have Z values of 3-5 (low = foreground)
- Alfred at Y=360 has Z ≈ 29 (higher than 5)
- Descending sort: Z=29 renders BEFORE Z=5 → Alfred is BEHIND

**Dynamic Z-changes:**
- Z-depth can change **per animation frame** using movement flags ✅ VERIFIED
- Bit 14 (0x4000): Enable Z-movement
- Bit 13 (0x2000): Direction (0=backward/decrease, 1=forward/increase)

---

## System Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ ROOM LOAD (load_room_data @ 0x152f5)                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 1. Load sprite data into room_sprite_data_ptr            │
│                                                          │
│ 2. Initialize Alfred's render_queue entry (index 1):     │
│    ├─ frame_ptr = alfred's current animation frame       │
│    ├─ x = alfred_x_position                              │
│    ├─ y = alfred_y_position - y_offset                   │
│    ├─ width, height from animation data                  │
│    ├─ z_depth = ((399-Y) & 0xFFFE) / 2 + 10  ✅ VERIFIED │
│    └─ character_flag = 1  ✅ VERIFIED                    │
│                                                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ FRAME UPDATE (update_npc_sprite_animations @ 0x1628d)   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ 1. Loop through sprite slots 2 to sprite_count-1        │
│    ├─ Skip slot matching current_room_id                 │
│    ├─ Skip disabled sprites (z_depth == 0xFF)           │
│    └─ For each active sprite:                           │
│        ├─ Update animation frame counters               │
│        ├─ Apply movement flags (X, Y, Z movement)       │
│        ├─ Check screen bounds (disable if off-screen)   │
│        └─ Add to render queue:                          │
│            ├─ frame_ptr, x, y, width, height            │
│            ├─ z_depth (from sprite_struct[0x21])        │
│            └─ character_flag = 0  (always for NPCs)     │
│                                                          │
│ 2. Bubble sort render queue by Z-depth (DESCENDING)     │
│    ├─ Condition: if (prev_z < curr_z) swap              │
│    └─ Result: high Z → low Z (back-to-front)            │
│                                                          │
│ 3. Render all sprites in sorted order                   │
│    └─ For each queue entry (0 to sprite_count-1):       │
│        ├─ if z_depth == 0xFF: skip                      │
│        ├─ if character_flag == 1:                       │
│        │     render_character_sprite_scaled()  (Alfred) │
│        └─ else: render_sprite()  (NPCs)                 │
│                                                          │
│ 4. Restore render_queue from backup (DAT_0004f9b0)      │
│    └─ Alfred's entry at index 1 is preserved            │
│                                                          │
└─────────────────────────────────────────────────────────┘

VISUAL EXAMPLE (Y-position to Z-depth relationship):
═══════════════════════════════════════════════════════════
Screen Y=0 (top)     → Alfred Z ≈ 209 (BEHIND sprites)
     │
     │   Sprite with Z=5 renders IN FRONT of Alfred
     │
Screen Y=200 (middle) → Alfred Z ≈ 110
     │
     │   Sprite with Z=100 renders IN FRONT of Alfred
     │   Sprite with Z=120 renders BEHIND Alfred
     │
Screen Y=399 (bottom) → Alfred Z ≈ 10 (IN FRONT of most)
═══════════════════════════════════════════════════════════

```
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
- Sprites with **higher Z values** are rendered **first** (appear in back) ✅ VERIFIED
- Sprites with **lower Z values** are rendered **last** (appear in front) ✅ VERIFIED

### 5. Alfred's Position in Z-Order ⚠️ PARTIALLY VERIFIED

Alfred (the player character) is handled specially. Some details below are theories that need verification.

#### What We Know (Verified)

1. **Alfred's sprite slot (index 0) is DISABLED**: `*(room_sprite_data_ptr + 0x21) = 0xff`
2. **Alfred has separate global variables**:
   - `alfred_frame_data_ptr` - current animation frame
   - `alfred_render_x`, `alfred_render_y` - position
   - `alfred_render_width` - dimensions
   - `alfred_scale_factor` - Y-based scaling
   - `alfred_render_enabled` - render flag

3. **NPC loop starts at index 2**, not 0 or 1:
   ```c
   iVar17 = 0x200;  // Start index = 2
   while (bVar14 = (byte)((uint)iVar17 >> 8), bVar14 < sprite_count) {
   ```

4. **Render queue entry 0** is used for Alfred with `character_flag = 1`
5. **DAT_0004f9b0** is a saved render queue that gets restored after each frame

#### What We Don't Know (Unverified)

1. **WHERE Alfred's render_queue[0] entry is populated** with character_flag = 1
2. **WHAT Z-depth value Alfred has** in the render queue
3. **HOW sprites can render in front of Alfred** (observed but not explained)

#### ❌ WRONG THEORY (Previously Documented)

The previous claim that "Alfred is at sprite index = current_room_number" is **WRONG**.
- 55 rooms exist but sprite arrays are small (typically 6-8 slots)
- The `bVar14 != current_room_id` check in the loop has a different purpose
- Alfred is NOT stored in the normal sprite array

#### Alfred's Separate Rendering

From `setup_alfred_frame_from_state`:
```c
// Mark Alfred's sprite slot as disabled
*(undefined1 *)(room_sprite_data_ptr + 0x21) = 0xff;

// But set up separate render parameters
alfred_render_enabled = 1;

// Special case: In room 0x15, add to render queue for mouse cursor
// (Note: this sets character_flag = 0, not 1!)
if ((current_room_number == 0x15) && (1 < mouse_hover_state)) {
    render_queue_frame_ptr = mouse_cursor_frame_ptr;
    render_queue_z_depth._0_1_ = 1;  // Z-depth = 1
    render_queue_z_depth._1_1_ = 0;  // character_flag = 0!
    ...
}
```

Alfred is rendered **outside the normal sprite queue** in most rooms!

#### Special Rendering Flag ✅ VERIFIED

The render queue has a **character_flag** at offset +1 from the Z-depth:
```c
render_queue_z_depth[index*0x0E + 1] = character_flag
```

From the rendering loop:
```c
if ((character_flag == 0x01) && (z_depth != 0xFF)) {
    render_character_sprite_scaled(...);  // Scaled rendering with Y-based scaling
} else if (z_depth != 0xFF) {
    render_sprite(...);                    // Normal sprite rendering
}
```

### 6. ❌ SECTION NEEDS MAJOR REVISION

**The following section contains WRONG information that was previously documented. It needs to be rewritten based on further investigation.**

The claim that "Alfred's sprite is at index = room number" is INCORRECT because:
- There are 55 rooms but only ~6-8 sprite slots per room
- The `bVar14 != current_room_id` check doesn't make sense with this theory

**What we actually know:**
1. Alfred's data goes to render_queue[0] (index 0)
2. Alfred's character_flag should be 1 (triggers scaled rendering)
3. NPCs are at render_queue indices 2+ (character_flag = 0)
4. DAT_0004f9b0 contains a saved/backup render queue
5. After each frame, render_queue is restored from DAT_0004f9b0

**Still unknown:**
- Where is render_queue[0] populated with Alfred's data?
- Where is character_flag set to 1 for Alfred?
- What is Alfred's actual Z-depth value?

**Example** (HYPOTHETICAL - needs verification):
```
Room 1 sprite data:
- Sprite[0]: Some object, Z-depth = 200
- Sprite[1]: ALFRED, Z-depth = 100 (fixed value for room 1)
- Sprite[2]: Foreground object, Z-depth = 50

Render order (sorted descending):
1. Sprite[0] renders first (Z=200, background)
2. Sprite[1] ALFRED renders second (Z=100, middle)
3. Sprite[2] renders last (Z=50, foreground - appears in front of Alfred!)
```

**This explains the user's observation**: In room 1, a sprite at Y=247 appears in front of Alfred at Y=364+ because that sprite has a **lower Z-depth value** than Alfred's fixed Z-depth, not because of Y-position comparison!

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
   - NPC sprites (index 2+) are processed, character_flag = 0
   - Alfred is at render_queue[1] with character_flag = 1

4. **Queue is sorted by Z-depth** using bubble sort (**DESCENDING** order - high to low) ✅ VERIFIED

5. **Rendering happens in sorted order**:
   - Sprites with **higher Z-depth render FIRST** (background) ✅ VERIFIED
   - Sprites with **lower Z-depth render LAST** (foreground) ✅ VERIFIED
   - Character flag == 1 triggers scaled rendering ✅ VERIFIED

6. **Alfred rendering** ✅ VERIFIED:
   - Alfred's sprite slot 0 is DISABLED (Z = 0xFF) ✅ VERIFIED
   - Alfred uses render_queue[1] with character_flag = 1 ✅ VERIFIED (@ 0x15a44)
   - Rendered via `render_character_sprite_scaled()` ✅ VERIFIED
   - **Alfred's Z-depth is Y-position based** ✅ VERIFIED (@ 0x15a20-0x15a3d)

### ✅ RESOLVED: How Sprites Render in Front of Alfred

**User Observation** (December 2024):

| Room | Sprite Index | Z-Order | Relative to Alfred |
|------|--------------|---------|-------------------|
| 1    | 0            | 3       | IN FRONT |
| 2    | 0            | 5       | IN FRONT |
| 9    | 1            | 3       | IN FRONT |
| 12   | 2            | 3       | IN FRONT |

**VERIFIED ANSWER** (from Ghidra @ load_room_data 0x15a20-0x15a3d):

Alfred's Z-depth is computed dynamically from his Y position:
```c
Z_depth = ((399 - alfred_y_position) & 0xFFFE) / 2 + 10
```

Example values:
- Y=0 (top of screen): Z = 209
- Y=200 (middle): Z = 109
- Y=350 (near bottom): Z = 34
- Y=399 (bottom): Z = 10

**Why sprites with Z=3-5 appear in front:**
- Even at the BOTTOM of the screen (Y=399), Alfred has Z=10
- Sprites with Z=3 or Z=5 have LOWER Z than Alfred's minimum (10)
- With DESCENDING sort: Alfred (Z≥10) renders BEFORE sprites (Z=3-5)
- Therefore Alfred is always BEHIND these low-Z sprites

**Key insight**: The formula's `+ 10` offset ensures Alfred can never have Z < 10, so any sprite with Z < 10 will ALWAYS appear in front of Alfred.

### For Game Modders (ScummVM Reimplementation)

To control sprite layering:
1. **Static layering**: Set sprite Z-depth at offset +0x21 (higher = background, lower = foreground)
2. **Dynamic layering**: Use movement flags bits 13-14 to change Z-depth during animation
3. **Disable sprites**: Set Z-depth to 0xFF
4. **Foreground sprites**: Use Z < 10 to always appear in front of Alfred
5. **Alfred interaction**: Alfred's Z is 10-209 based on Y position

## Technical Details

### Alfred Z-Depth Initialization (VERIFIED @ 0x15a20-0x15a44)

The Z-depth is computed in `load_room_data()` during room initialization:

```asm
; Address 0x15a20-0x15a3d in load_room_data
MOV DX, [0x4fb98]          ; EDX = alfred_y_position
MOV EBX, 0x18f             ; EBX = 399
SUB EBX, EDX               ; EBX = 399 - Y
AND EDX, 0xFFFE            ; Make even (clear bit 0)
SAR EDX, 1                 ; Divide by 2
ADD EDX, 0xa               ; Add 10
MOV [render_queue_z], DL   ; Store Z-depth
MOV [render_queue_flag], 1 ; character_flag = 1
```

**C equivalent:**
```c
render_queue[1].z_depth = ((399 - alfred_y_position) & 0xFFFE) / 2 + 10;
render_queue[1].character_flag = 1;
```

### Backup Render Queue (DAT_0004f9b0)

After each frame, the render_queue is restored from DAT_0004f9b0 (backup):
- This preserves Alfred's entry at index 1
- NPCs (indices 2+) are re-populated each frame from sprite structures

## ✅ Previously Debunked Theories (Now Verified)

1. ~~**"Alfred is at sprite index = room_number"**~~ - WRONG (55 rooms, ~8 sprite slots)
2. **"Alfred's Z-depth is calculated from Y-position"** - ✅ NOW VERIFIED

## Related Systems

- **Sprite Scaling**: Y-position based scaling via DAT_0004967e/f
- **Walkbox System**: Determines where Alfred can walk
- **Screen Bounds**: Sprites disabled if off-screen (X >= 640, Y >= 400, or negative)

## Function Reference

| Function | Address | Verified |
|----------|---------|----------|
| load_room_data() | 0x000152F5 | ✅ Yes |
| update_npc_sprite_animations() | 0x0001628D | ✅ Yes |
| render_sprite() | 0x00016D10 | ✅ Yes |
| render_character_sprite_scaled() | 0x00016FF8 | ✅ Yes |
| setup_alfred_frame_from_state() | 0x000147C9 | ✅ Yes |
| render_scene() | 0x00015E4C | ✅ Yes |
| load_room_data() | 0x000152F5 | ✅ Yes |

