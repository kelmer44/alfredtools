# Sprite/Animation Structure - Complete Analysis

## Room 2, Sprite 2 (Animation 0) - Actual Byte-by-Byte Breakdown

Based on cross-referencing Ghidra decompilation with actual file data from ALFRED.1.

### File Location
- **Metadata block offset**: 0x000B181A (Pair 10 for room 2)
- **Sprite 2 offset**: 0x000B1872 (metadata_offset + sprite_index * 0x2C)
- **Structure size**: 44 bytes (0x2C)

### Actual Hex Dump
```
Offset: 00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F
0x00:   00 00 00 00 00 00 00 00  00 00 48 00 FC 00 49 84
0x10:   A4 25 02 00 03 0B 00 00  0F 02 00 00 02 03 00 00
0x20:   00 05 00 00 00 00 00 00  00 00 17 01
```

---

## Structure Definition (44 bytes total)

| Offset | Size | Type | Name | Value (Room 2, Sprite 2) | Notes |
|--------|------|------|------|---------------------------|-------|
| 0x00 | 4 | dword | Unknown header | 0x00000000 | Always zeros in file? |
| 0x04 | 2 | word | Unknown header | 0x0000 | Always zeros in file? |
| 0x06 | 4 | ptr | Sprite graphic data ptr | 0x00000000 | **Overwritten at runtime** with pointer to pixel data |
| 0x0A | 2 | short | X coordinate | 72 (0x0048) | Sprite X position on screen |
| 0x0C | 2 | short | Y coordinate | 252 (0x00FC) | Sprite Y position on screen |
| 0x0E | 1 | byte | Width | 73 (0x49) | Sprite width in pixels |
| 0x0F | 1 | byte | Height | 132 (0x84) | Sprite height in pixels |
| 0x10 | 2 | word | Stride | 9636 (0x25A4) | Bytes per row (width * frames_in_seq) |
| 0x12 | 1 | byte | Num sequences | 2 | Number of animation sequences |
| 0x13 | 1 | byte | Current sequence idx | 0 | Runtime: which sequence is playing |
| 0x14 | 1 | byte | Frames in sequence 0 | 3 | Number of frames in first sequence |
| 0x15 | 1 | byte | Frames in sequence 1 | 11 (0x0B) | Number of frames in second sequence |
| 0x16 | 1 | byte | Frames in sequence 2 | 0 | (unused - only 2 sequences) |
| 0x17 | 1 | byte | Frames in sequence 3 | 0 | (unused - only 2 sequences) |
| 0x18 | 1 | byte | Loop count sequence 0 | 15 (0x0F) | Times to loop, 0xFF = infinite |
| 0x19 | 1 | byte | Loop count sequence 1 | 2 | Times to loop |
| 0x1A | 1 | byte | Loop count sequence 2 | 0 | (unused) |
| 0x1B | 1 | byte | Loop count sequence 3 | 0 | (unused) |
| 0x1C | 1 | byte | Frame 0 delay | 2 | Frame duration in ticks (18.2 Hz) |
| 0x1D | 1 | byte | Frame 1 delay | 3 | |
| 0x1E | 1 | byte | Frame 2 delay | 0 | |
| 0x1F | 1 | byte | Frame 3 delay | 0 | |
| 0x20 | 1 | byte | **Current frame index** | 0 | Runtime: which frame is showing |
| 0x21 | 1 | byte | **Z-depth** | 5 | **Depth layer** (0-255, 0xFF=disabled) |
| 0x22 | 2 | word | Movement flags seq 0 | 0x0000 | Movement flags for sequence 0 |
| 0x24 | 2 | word | Movement flags seq 1 | 0x0000 | Movement flags for sequence 1 |
| 0x26 | 2 | word | Movement flags seq 2 | 0x0000 | (unused) |
| 0x28 | 2 | word | Movement flags seq 3 | 0x0000 | (unused) |
| 0x2A | 1 | byte | Unknown | 0x17 | ? |
| 0x2B | 1 | byte | Unknown | 0x01 | ? |

**Total**: 44 bytes (0x2C)

---

## Key Corrections from Previous Documentation

### 1. Movement Flags Are PER SEQUENCE, Not Per Frame
- **Location**: 0x22 + (sequence_index * 2)
- **Access**: `*(ushort *)(sprite_ptr + current_anim_sequence * 2 + 0x22)`
- **NOT** indexed by frame - all frames in a sequence share the same movement flags

### 2. Frame Delays Are Variable Length
- Start at offset 0x1C
- One byte per frame (total frames across ALL sequences)
- For this sprite: 14 frames total (3 + 11), so 14 delay bytes

### 3. The First 10 Bytes
- Bytes 0x00-0x05: Unknown header (all zeros in file)
- Bytes 0x06-0x09: Sprite graphic data pointer (zeros in file, **overwritten at runtime**)
- Bytes 0x0A+: Actual sprite metadata begins (X, Y, width, height, etc.)

### 4. Hydration at Runtime
From Ghidra `load_room_data`:
```c
*(int *)(room_sprite_data_ptr + iVar10 + 6) = iVar7;
```
The engine overwrites offset +0x06 with a pointer to the decompressed pixel data after loading.

---

## Movement Flags Bitfield (16 bits per sequence)

```
Bit 15 14 13 12 11 10 09 08  07 06 05 04 03 02 01 00
    ?  Z  Z  Z  Z  Z  Y  Y   Y  Y  Y  X  X  ?  ?  ?
       |  |  |__|__|  |  |   |__|__|  |  |  |__|__|
       |  |     |     |  |      |     |  |     |
       |  |  Z-amount |  |   Y-speed  |  |   X-amount
       |  |           |  |             |  |
       |  Z-enable    |  Y-enable      |  X-direction
       |              |                |
       Z-direction    Y-direction      X-enable
```

### Bits 0-2 (0x0007): X Movement Amount
- 0-7 pixels per frame

### Bit 3 (0x0008): X Movement Enable
- 0 = no X movement
- 1 = apply X movement

### Bit 4 (0x0010): X Direction
- 0 = left (subtract)
- 1 = right (add)

### Bits 5-7 (0x00E0): Y Movement Speed
- 0-7 pixels per frame

### Bit 8 (0x0100): Y Direction
- 0 = up (subtract)
- 1 = down (add)

### Bit 9 (0x0200): Y Movement Enable
- 0 = no Y movement
- 1 = apply Y movement

### Bits 10-12 (0x1C00): Z Movement Amount
- 0-7 depth units per frame

### Bit 13 (0x2000): Z Direction
- 0 = backward (decrease Z-depth)
- 1 = forward (increase Z-depth)

### Bit 14 (0x4000): Z Movement Enable
- 0 = no Z movement
- 1 = apply Z movement

### Bit 15 (0x8000): Unknown/Unused

---

## Runtime Fields vs File Fields

### Fields Stored in File (Static)
- X, Y position (0x0A, 0x0C)
- Width, height (0x0E, 0x0F)
- Stride (0x10)
- Number of sequences (0x12)
- Frames per sequence (0x14-0x17)
- Loop counts (0x18-0x1B)
- Frame delays (0x1C+)
- Z-depth (0x21) - **initial value**
- Movement flags (0x22-0x29)

### Fields Hydrated at Runtime (Dynamic)
- Sprite graphic data pointer (0x06) - overwritten by engine
- Current sequence index (0x13) - starts at 0, changes during playback
- Current frame index (0x20) - advances as animation plays
- Z-depth (0x21) - can be modified by movement flags
- Additional runtime fields beyond 0x2C (not in 44-byte file structure):
  - Frame delay counter (mentioned in Ghidra as +0x2D)
  - Loop counter (+0x2E)
  - Disable after sequence flag (+0x31)

**Note**: The Ghidra comments mention fields at offsets like +0x2D, +0x2E, +0x31 which are **beyond the 44-byte structure**. These are additional runtime fields allocated by the engine, not present in the file.

---

## Example: Sequence with Movement

If a sprite had movement flags `0x6418`:
```
0x6418 = 0110 0100 0001 1000
         ││││ ││││ ││││ ││││
         0110 0100 0001 1000

Bit 14 (Z enable): 1
Bit 13 (Z dir): 1 (forward)
Bits 10-12 (Z amount): 100 binary = 4

Bit 9 (Y enable): 0
Bit 8 (Y dir): 1
Bits 5-7 (Y speed): 000

Bit 4 (X dir): 1 (right)
Bit 3 (X enable): 1
Bits 0-2 (X amount): 000 binary = 0

Result: Move forward in Z-depth by 4 units per frame
        (No X or Y movement despite flags being partially set)
```

---

## Summary

The 44-byte structure in the file contains:
1. **6 bytes**: Unknown header (zeros)
2. **4 bytes**: Pointer placeholder (overwritten at runtime)
3. **10 bytes**: Position and dimensions (X, Y, W, H, stride)
4. **2 bytes**: Sequence metadata (count, current)
5. **4 bytes**: Frames per sequence array
6. **4 bytes**: Loop count array
7. **Variable bytes**: Frame delays (one per total frame)
8. **2 bytes**: Runtime state (current frame, Z-depth)
9. **8 bytes**: Movement flags (2 bytes × 4 sequences)
10. **Remaining bytes**: Unknown/padding

**Critical**: Movement flags are **per sequence**, not per frame. All frames in a sequence share the same movement behavior.
