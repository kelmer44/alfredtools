# Palette Cycling/Animation System Documentation

## Overview

Alfred Pelrock uses a palette cycling system to create animated visual effects without modifying pixel data. The game modifies VGA palette entries in real-time to create effects like:

- Fading neon signs (McDowells restaurant)
- Rotating/shimmering lights (city windows at night)
- Shiny/glowing objects (gems, buttons)
- Water/fire effects

This technique was common in DOS-era games as it's extremely efficient - only 3 bytes per color need to change rather than thousands of pixels.

## Data Structures

### Dispatch Table

**Location:**
- Memory address: `0x000486A4`
- File offset: `0x0004B8A4`
- Ghidra label: `palette_cycling_dispatch_table`

**Format:** Array of 6-byte entries terminated by `0xFFFF`

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0 | 2 | room_number | Room ID (little-endian word) |
| +2 | 4 | config_ptr | Pointer to 12-byte config structure |

**Terminator:** `0xFFFF` marks end of table

### Config Structure (12 bytes)

Two modes exist: FADE (mode=1) and ROTATE (mode>1)

#### FADE Mode (mode=1)
Smoothly transitions a single palette entry between two colors.

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0 | 1 | palette_index | VGA palette entry to animate (0-255) |
| +1 | 1 | mode | Always 1 for fade |
| +2 | 1 | current_r | Current red value (6-bit, 0-63) |
| +3 | 1 | current_g | Current green value (6-bit, 0-63) |
| +4 | 1 | current_b | Current blue value (6-bit, 0-63) |
| +5 | 1 | min_r | Minimum red value |
| +6 | 1 | min_g | Minimum green value |
| +7 | 1 | min_b | Minimum blue value |
| +8 | 1 | max_r | Maximum red value |
| +9 | 1 | max_g | Maximum green value |
| +10 | 1 | max_b | Maximum blue value |
| +11 | 1 | flags | Control flags (see below) |

**Flags byte:**
- Bits 0-5: Speed (steps per frame)
- Bit 6: Direction (0=fading toward min, 1=fading toward max)

#### ROTATE Mode (mode>1)
Cyclically rotates N consecutive palette entries.

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0 | 1 | start_index | First palette entry to rotate |
| +1 | 1 | count | Number of consecutive entries (2-10) |
| +2 | 1 | reserved | Usually 0 |
| +3 | 1 | delay | Frames between rotations |
| +4-11 | 8 | state_data | Runtime state/reserved |

## Rooms with Palette Animation

| Room | Mode | Palette Range | Delay | Effect Description |
|------|------|---------------|-------|-------------------|
| 0 | ROTATE-6 | 200-205 | 90 frames (~5 sec) | City window lights at night |
| 2 | FADE | 250 | - | McDowells neon sign (green glow) |
| 9 | ROTATE-4 | 252-255 | 4 frames | Shiny object effect |
| 17 | ROTATE-6 | 138-143 | 8 frames | Unknown |
| 18 | ROTATE-6 | 181-186 | 35 frames | Unknown |
| 19 | FADE | 37 | - | Red glow effect |
| 21 | ROTATE-3 | 148-150 | 10 frames | Unknown |
| 25 | ROTATE-4 | 224-227 | 4 frames | Unknown |
| 32 | ROTATE-2 | 203-204 | 2 frames | Unknown |
| 33 | ROTATE-2 | 214-215 | 2 frames | Unknown |
| 38 | ROTATE-7 | 103-109 | 1 frame | Fast shimmer |
| 39 | ROTATE-3 | 192-194 | 5 frames | Unknown |
| 46 | ROTATE-2 | 43-44 | 4 frames | Unknown |

## File Offsets

### Dispatch Table
- **File offset:** `0x0004B8A4`
- **Size:** 80 bytes (13 entries × 6 bytes + 2 byte terminator)

### Config Data Block
- **File offset:** `0x0004B860` to `0x0004B8A3`
- **Size:** 68 bytes
- **Note:** Configs overlap to save space - each room's 12-byte config shares bytes with adjacent configs

### Individual Config Offsets

| Room | File Offset | Memory Ptr |
|------|-------------|------------|
| 2 | 0x0004B860 | 0x00008660 |
| 17 | 0x0004B86C | 0x0000866C |
| 18 | 0x0004B870 | 0x00008670 |
| 9 | 0x0004B874 | 0x00008674 |
| 19 | 0x0004B878 | 0x00008678 |
| 21 | 0x0004B884 | 0x00008684 |
| 39 | 0x0004B888 | 0x00008688 |
| 0 | 0x0004B88C | 0x0000868C |
| 25 | 0x0004B890 | 0x00008690 |
| 38 | 0x0004B894 | 0x00008694 |
| 32 | 0x0004B898 | 0x00008698 |
| 33 | 0x0004B89C | 0x0000869C |
| 46 | 0x0004B8A0 | 0x000086A0 |

## Code References

### Main Functions

| Function | Address | Description |
|----------|---------|-------------|
| `update_palette_cycling` | 0x00016804 | Called every frame to process animation |
| `load_room_and_init_alfred` | 0x000152f5 | Looks up room in dispatch table |
| `outport_byte` | 0x0002b11b | Writes to VGA I/O port |

### Global Variables

| Variable | Address | Type | Description |
|----------|---------|------|-------------|
| `palette_cycling_enabled` | 0x0004f8ea | byte | 1 if current room has animation |
| `palette_cycling_config_ptr` | 0x0004f8ec | dword | Pointer to current 12-byte config |
| `palette_cycling_frame_counter` | 0x00051753 | byte | Frame counter for rotate delay |
| `current_room_palette_ptr` | 0x0004fab8 | dword | Pointer to loaded room palette (768 bytes) |
| `palette_cycling_dispatch_table` | 0x000486a4 | array | Room-to-config lookup table |

## Algorithm

### FADE Mode
```
every frame:
    if direction == UP:
        current_rgb += speed_per_channel
        if current_r >= max_r:
            direction = DOWN
    else:
        current_rgb -= speed_per_channel
        if current_r <= min_r:
            direction = UP

    outport(0x3C8, palette_index)  // Set palette index
    outport(0x3C9, current_r)      // Set R
    outport(0x3C9, current_g)      // Set G
    outport(0x3C9, current_b)      // Set B
```

### ROTATE Mode
```
every frame:
    frame_counter++
    if frame_counter >= delay:
        frame_counter = 0

        // Save last color
        saved = palette[start_index + count - 1]

        // Shift all colors down
        for i = count-1 to 1:
            palette[start_index + i] = palette[start_index + i - 1]
            outport(0x3C8, start_index + i)
            outport(0x3C9, palette[...])

        // Wrap first color
        palette[start_index] = saved
        outport(0x3C8, start_index)
        outport(0x3C9, saved.rgb)
```

## Memory-to-File Offset Mapping

For palette cycling data:
```
file_offset = memory_ptr + 0x43200
```

Example:
- Room 2 config at memory `0x00008660`
- File offset = `0x8660 + 0x43200 = 0x4B860`

## Raw Config Data

```hex
Offset    Data
0x4B860:  fa 01 24 2c 08 0c 14 08 24 2c 08 05  ; Room 2 - FADE
0x4B86C:  8a 06 00 08 b5 06 00 23 fc 04 00 04  ; Room 17 - ROTATE-6
0x4B870:  b5 06 00 23 fc 04 00 04 25 01 3e 08  ; Room 18 - ROTATE-6
0x4B874:  fc 04 00 04 25 01 3e 08 02 28 08 02  ; Room 9 - ROTATE-4
0x4B878:  25 01 3e 08 02 28 08 02 3e 08 02 01  ; Room 19 - FADE
0x4B884:  94 03 00 0a c0 03 00 05 c8 06 00 5a  ; Room 21 - ROTATE-3
0x4B888:  c0 03 00 05 c8 06 00 5a e0 04 00 04  ; Room 39 - ROTATE-3
0x4B88C:  c8 06 00 5a e0 04 00 04 67 07 00 01  ; Room 0 - ROTATE-6
0x4B890:  e0 04 00 04 67 07 00 01 cb 02 00 02  ; Room 25 - ROTATE-4
0x4B894:  67 07 00 01 cb 02 00 02 d6 02 00 02  ; Room 38 - ROTATE-7
0x4B898:  cb 02 00 02 d6 02 00 02 2b 02 00 04  ; Room 32 - ROTATE-2
0x4B89C:  d6 02 00 02 2b 02 00 04              ; Room 33 - ROTATE-2
0x4B8A0:  2b 02 00 04                          ; Room 46 - ROTATE-2 (partial)
```

Note: Configs overlap because they share trailing bytes with the next config's leading bytes.

## Dispatch Table Raw Data

```hex
0x4B8A4:  02 00 60 86 00 00   ; Room 2 -> 0x8660
0x4B8AA:  09 00 74 86 00 00   ; Room 9 -> 0x8674
0x4B8B0:  11 00 6c 86 00 00   ; Room 17 -> 0x866C
0x4B8B6:  12 00 70 86 00 00   ; Room 18 -> 0x8670
0x4B8BC:  13 00 78 86 00 00   ; Room 19 -> 0x8678
0x4B8C2:  15 00 84 86 00 00   ; Room 21 -> 0x8684
0x4B8C8:  27 00 88 86 00 00   ; Room 39 -> 0x8688
0x4B8CE:  00 00 8c 86 00 00   ; Room 0 -> 0x868C
0x4B8D4:  19 00 90 86 00 00   ; Room 25 -> 0x8690
0x4B8DA:  26 00 94 86 00 00   ; Room 38 -> 0x8694
0x4B8E0:  20 00 98 86 00 00   ; Room 32 -> 0x8698
0x4B8E6:  21 00 9c 86 00 00   ; Room 33 -> 0x869C
0x4B8EC:  2e 00 a0 86 00 00   ; Room 46 -> 0x86A0
0x4B8F2:  ff ff               ; Terminator
```
