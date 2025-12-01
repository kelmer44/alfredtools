# Alfred Pelrock - Ghidra Scaling System Analysis

## Overview

This document summarizes the character scaling system as analyzed in Ghidra, including function names, variable names, and memory addresses.

## Functions

### init_character_scaling_tables (0x00011e28)
**Purpose:** Creates lookup tables for character scaling at game startup

**What it does:**
- Initializes `width_scaling_lookup_table` at 0x00053290 (51×51 bytes)
- Initializes `height_scaling_lookup_table` at 0x00053cbc (102×102 bytes)
- Creates mapping tables for selective pixel/scanline rendering during scaling

**Algorithm:**
```c
for each scale_factor from 0 to 50:
    step = dimension / (scale_factor + 1)
    index = 0
    while index < dimension:
        lookup_table[round(index)][scale_factor] = which_pixel_to_use
        index += step
```

This creates tables that determine which source pixels/scanlines to use when scaling.

---

### render_character_sprite_scaled (0x00016ff8)
**Purpose:** Renders character sprite with scaling applied

**Parameters:**
- `param_1`: Height (in_stack_00000004)
- `param_2`: scale_down offset (in_stack_00000008)
- `param_3`: scale_up offset (in_stack_0000000c)

**What it does:**
1. Uses `width_scaling_lookup_table` (DAT_00053290) to determine which horizontal pixels to draw
2. Uses `height_scaling_lookup_table` (DAT_00053cbc) to determine which scanlines to draw/duplicate
3. Iterates through sprite data, checking lookup tables:
   - If `width_scaling_lookup_table[scale_offset + pixel_x * 0x33] == 0`: draw pixel
   - If `height_scaling_lookup_table[scale_offset + scanline_y * 0x66] == 0`: advance to next scanline
   - Otherwise: duplicate current scanline

**Key lookup table accesses:**
```c
// Width scaling check
if (width_scaling_lookup_table[param_2 + (width - pixel_x) * 0x33] == 0)

// Height scaling check
if (height_scaling_lookup_table[param_3 + (height - scanline_y) * 0x66] == 0)
```

---

### load_room_data (0x00015340)
**Purpose:** Loads room data from ALFRED.1 and calculates initial scaling values

**Scaling Calculation (at ~0x15570):**

Reads scaling parameters from room data at offset 0x214 (within Pair 10):
- **+0x214**: `y_threshold` (uint16 LE) - Y coordinate where scaling begins
- **+0x216**: `scale_divisor` (uint8) - Controls rate of scaling
- **+0x217**: `scale_mode` (int8) - Scaling behavior mode

```c
if (room_data_ptr[0x217] == 0x00) {  // Normal scaling mode
    if (*(ushort*)(room_data_ptr + 0x214) < player_y) {
        // Player below threshold (foreground)
        scale_up = 0;
        scale_down = 0;
    } else {
        // Player above threshold (background) - apply scaling
        scale_delta = (y_threshold - player_y) / scale_divisor;
        scale_down = scale_delta;
        scale_up = scale_delta / 2;
    }
}
else if (room_data_ptr[0x217] == 0xFF) {  // Maximum scaling
    scale_up = 0x2f;    // 47
    scale_down = 0x5e;  // 94
}
else if (room_data_ptr[0x217] == 0xFE) {  // No scaling
    scale_up = 0;
    scale_down = 0;
}
```

**Final dimensions:**
```c
final_height = 102 - scale_down + scale_up;
final_width = 51 * (final_height / 102);
```

---

## Global Variables

### Scaling State Variables
- **scale_up** @ 0x0004967e (byte) - Number of scanlines to duplicate (adds height back)
- **scale_down** @ 0x0004967f (byte) - Number of scanlines to skip (reduces height)

### Lookup Tables
- **width_scaling_lookup_table** @ 0x00053290 (51×51 bytes)
  - Maps (scale_factor, pixel_x) → draw decision
  - Size: 0x33 × 0x33 = 2,601 bytes

- **height_scaling_lookup_table** @ 0x00053cbc (102×102 bytes)
  - Maps (scale_factor, scanline_y) → draw/duplicate decision
  - Size: 0x66 × 0x66 = 10,404 bytes

### Room Data Pointer
- **room_data_ptr** - Points to current room's Pair 10 data
  - Offset +0x214: y_threshold
  - Offset +0x216: scale_divisor
  - Offset +0x217: scale_mode

---

## Scaling Modes

### Mode 0x00 (Normal Scaling)
Characters scale dynamically based on Y position:
- **Above y_threshold**: Scale gets smaller as Y decreases (walking toward back)
- **Below y_threshold**: No scaling (foreground is normal size)

### Mode 0xFF (Maximum Scaling)
Character always rendered at maximum scale:
- scale_down = 94 (0x5e)
- scale_up = 47 (0x2f)
- Final size: 102 - 94 + 47 = 55 pixels tall (~54% of original)

### Mode 0xFE (No Scaling)
Character always rendered at normal size:
- scale_down = 0
- scale_up = 0
- Final size: 102 pixels tall (100% of original)

---

## Example: Room 6 Scaling

**Parameters** (from ALFRED.1 at room 6, offset 0x214):
- y_threshold: 370
- scale_divisor: 4
- scale_mode: 0x00 (normal)

**Scaling at different Y positions:**

| Y Pos | Calculation | scale_down | scale_up | Final Height |
|-------|-------------|------------|----------|--------------|
| 0     | (370-0)/4   | 92         | 46       | 56 pixels    |
| 100   | (370-100)/4 | 67         | 33       | 68 pixels    |
| 200   | (370-200)/4 | 42         | 21       | 81 pixels    |
| 370   | below threshold | 0      | 0        | 102 pixels   |
| 399   | below threshold | 0      | 0        | 102 pixels   |

---

## Memory Layout

```
Game Binary Memory Map (relevant sections):

0x00011e28  init_character_scaling_tables()
0x00015340  load_room_data()
0x00016ff8  render_character_sprite_scaled()

0x0004967e  scale_up (byte)
0x0004967f  scale_down (byte)

0x00053290  width_scaling_lookup_table[51×51]
            Size: 2,601 bytes
            End:  0x00053A39

0x00053cbc  height_scaling_lookup_table[102×102]
            Size: 10,404 bytes
            End:  0x00056560
```

---

## Comments Added to Ghidra

The following comments were added to improve code readability:

1. **@ 0x00053290** (width_scaling_lookup_table):
   > "Width scaling lookup table (51 pixels): Maps scaled width index to which horizontal pixels to draw. Used in render_character_sprite_scaled to skip pixels when scaling character width."

2. **@ 0x00053cbc** (height_scaling_lookup_table):
   > "Height scaling lookup table (102 pixels): Maps scaled height index to which scanlines to draw/duplicate. When scale_down > 0, scanlines are skipped. When scale_up > 0, some scanlines are duplicated. Final height = 102 - scale_down + scale_up."

3. **@ 0x00015340** (load_room_data):
   > "SCALING CALCULATION: At offset ~0x15570, reads scaling params from room_data_ptr+0x214: y_threshold (uint16), scale_divisor (uint8), scale_mode (int8). If scale_mode == 0 and player_y < y_threshold, calculates: scale_delta = (y_threshold - player_y) / scale_divisor, then scale_down = scale_delta, scale_up = scale_delta / 2."

---

## Files Generated

- `extract_scaling_lookup_tables.py` - Extracts lookup tables from game binary
- `verify_and_demo_scaling.py` - Demonstrates scaling at different heights
- `SPRITE_SCALING.md` - Complete documentation of scaling system

## Verification Status

✓ All addresses verified against Ghidra decompilation
✓ Algorithm matches assembly code behavior
✓ Scaling parameters confirmed in ALFRED.1 file format
✓ Lookup table addresses and sizes confirmed
✓ Variable names updated in Ghidra project
