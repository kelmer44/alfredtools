# SPRITE STRUCTURE - FINAL ANALYSIS
## 44-Byte Format (as stored in ALFRED.1 file)

Based on cross-referencing:
1. Actual file data from ALFRED.1
2. Ghidra decompilation (update_npc_sprite_animations, load_room_data)
3. Runtime behavior observations

---

## Room 2 Examples

### Sprite 2 (First Real Sprite):
```
Offset: 00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F
0x00:   00 00 00 00 00 00 00 00  00 00 48 00 FC 00 49 84
0x10:   A4 25 02 00 03 0B 00 00  0F 02 00 00 02 03 00 00
0x20:   00 05 00 00 00 00 00 00  00 00 17 01
```

### Sprite 3:
```
Offset: 00 01 02 03 04 05 06 07  08 09 0A 0B 0C 0D 0E 0F
0x00:   10 00 00 01 00 00 00 00  00 00 E5 00 04 01 20 14
0x10:   80 02 01 00 04 00 00 00  00 00 00 00 1B 00 00 00
0x20:   00 64 00 00 00 00 00 00  00 00 17 01
```

---

## Structure Layout (44 bytes, 0x2C)

| Offset | Size | Type | Name | Sprite 2 Value | Sprite 3 Value | Notes |
|--------|------|------|------|----------------|----------------|-------|
| **0x00-09: Unknown/Reserved Block** |
| 0x00 | 2 | short | Unknown | 0x0000 | 0x0010 | Sprite 3 has 16 here |
| 0x02 | 2 | short | Unknown | 0x0000 | 0x0100 | Sprite 3 has 256 here |
| 0x04 | 1 | byte | Unknown | 0x00 | 0x00 | |
| 0x05 | 1 | byte | Unknown | 0x00 | 0x00 | |
| 0x06 | 4 | dword | **Sprite ptr** | 0x00000000 | 0x00000000 | **Overwritten at runtime** |
| **0x0A-11: Position and Dimensions** |
| 0x0A | 2 | short | **X Position** | 72 (0x0048) | 229 (0x00E5) | Screen X coordinate |
| 0x0C | 2 | short | **Y Position** | 252 (0x00FC) | 260 (0x0104) | Screen Y coordinate |
| 0x0E | 1 | byte | **Width** | 73 (0x49) | 32 (0x20) | Sprite width in pixels |
| 0x0F | 1 | byte | **Height** | 132 (0x84) | 20 (0x14) | Sprite height in pixels |
| 0x10 | 2 | short | **Stride** | 9636 (0x25A4) | 640 (0x0280) | Bytes per row? |
| **0x12-1B: Animation Metadata** |
| 0x12 | 1 | byte | **Num Sequences** | 2 | 1 | Number of animation sequences |
| 0x13 | 1 | byte | Current Seq Idx | 0 | 0 | Runtime: which sequence playing |
| 0x14 | 1 | byte | Frames in Seq 0 | 3 | 4 | Number of frames |
| 0x15 | 1 | byte | Frames in Seq 1 | 11 (0x0B) | 0 | Number of frames |
| 0x16 | 1 | byte | Frames in Seq 2 | 0 | 0 | (unused) |
| 0x17 | 1 | byte | Frames in Seq 3 | 0 | 0 | (unused) |
| 0x18 | 1 | byte | Loop Count Seq 0 | 15 (0x0F) | 0 | 0xFF = infinite |
| 0x19 | 1 | byte | Loop Count Seq 1 | 2 | 0 | |
| 0x1A | 1 | byte | Loop Count Seq 2 | 0 | 0 | (unused) |
| 0x1B | 1 | byte | Loop Count Seq 3 | 0 | 0 | (unused) |
| **0x1C-1F: Frame Delays (variable length)** |
| 0x1C | 1 | byte | Frame 0 Delay | 2 | 27 (0x1B) | Ticks @ 18.2 Hz |
| 0x1D | 1 | byte | Frame 1 Delay | 3 | 0 | |
| 0x1E | 1 | byte | Frame 2 Delay | 0 | 0 | |
| 0x1F | 1 | byte | Frame 3 Delay | 0 | 0 | |
| **0x20-21: Runtime State** |
| 0x20 | 1 | byte | Current Frame | 0 | 0 | Runtime: which frame showing |
| 0x21 | 1 | byte | **Z-DEPTH** | **5** | **100 (0x64)** | **Depth layer, 0xFF=disabled** |
| **0x22-29: Movement Flags (per sequence)** |
| 0x22 | 2 | word | Seq 0 Flags | 0x0000 | 0x0000 | Movement bitfield |
| 0x24 | 2 | word | Seq 1 Flags | 0x0000 | 0x0000 | Movement bitfield |
| 0x26 | 2 | word | Seq 2 Flags | 0x0000 | 0x0000 | (unused) |
| 0x28 | 2 | word | Seq 3 Flags | 0x0000 | 0x0000 | (unused) |
| **0x2A-2B: Unknown** |
| 0x2A | 2 | word | Unknown | 0x0117 | 0x0117 | Both sprites have same value |

---

## Key Findings

### 1. Z-Depth Location: **CONFIRMED at offset 0x21**
- Sprite 2: Z-depth = 5
- Sprite 3: Z-depth = 100
- This matches Ghidra's reference: `*(char *)(iVar17 + 0x21)`

### 2. Position Fields
From Ghidra:
```c
sVar23 = *(short *)(iVar17 + 10);        // X at 0x0A
uVar20 = (uint)*(ushort *)(iVar17 + 0xc); // Y at 0x0C
```
**Confirmed: X at 0x0A, Y at 0x0C**

### 3. The Mystery of 0x00-03
- Sprite 2: All zeros
- Sprite 3: Contains 0x0010 (16) and 0x0100 (256)

**Hypothesis**: These might be:
- Bounding box origin?
- Initial position vs current position?
- Parent container offset?

Need to check Ghidra for references to offset +0 and +2.

### 4. Stride Field (0x10-11)
- Sprite 2: 9636 = 73 (width) × 132 (height)? No, that's 9636 ≠ width*height
- Sprite 3: 640 = 32 (width) × 20 (height) = 640 ✓ **Matches!**

Wait, for Sprite 3, stride = width * height = total pixels per frame!

Let me check Sprite 2: It has 2 sequences (3 frames + 11 frames = 14 total)
- 9636 / 73 (width) = 132... but height is also 132
- Maybe: 9636 / 132 (height) = 73 = width ✓

**Hypothesis**: Stride = width (for row-major pixel data layout)? Or stride = width * some_frames?

Looking at the Ghidra code:
```c
iVar15 = iVar15 + (uint)*(ushort *)(iVar17 + 0x10) *
                  (uint)*(byte *)(iVar17 + 0x14 + (uVar10 & 0xff));
```
This reads stride at +0x10 and multiplies by frames in sequence. So stride is used to calculate frame offsets in the sprite data.

**Conclusion**: Stride = bytes per row = width (since 1 byte per pixel in 256-color mode)

But wait, Sprite 2 stride is 9636, not 73. Let me recalculate:
- Sprite 2: width=73, height=132, seq0=3 frames, seq1=11 frames
- 73 × 132 = 9636 ✓

So stride = width × height? That doesn't make sense for "bytes per row"...

Let me check Sprite 3: width=32, height=20, stride=640
- 32 × 20 = 640 ✓

**REVISED**: Stride appears to be width × height (total pixels per frame), not bytes per row!

This makes sense if the sprite data is stored as contiguous frames, and "stride" is used to skip to the next frame.

---

## Movement Flags (confirmed per sequence)

From Ghidra:
```c
movement_flags = *(ushort *)(iVar17 + (uint)current_anim_sequence * 2 + 0x22);
```

Confirms: Movement flags at 0x22, indexed by sequence (not frame).

Bitfield (16 bits):
```
Bit  15 14 13 12 11 10 09 08  07 06 05 04 03 02 01 00
     ?  Z  Z  Z  Z  Z  Y  Y   Y  Y  Y  X  X  ?  ?  ?
```

See previous documentation for detailed bit breakdown.

---

## Runtime vs File

### Stored in File (Static):
- 0x00-09: Unknown block (mostly zeros, some sprites have data at 0x00-03)
- 0x0A-0F: Position and dimensions
- 0x10-11: Stride
- 0x12: Number of sequences
- 0x14-1B: Sequence metadata (frames, loops)
- 0x1C+: Frame delays (variable length)
- 0x21: **Z-depth** (initial value, can be modified at runtime)
- 0x22-29: Movement flags per sequence

### Hydrated at Runtime:
- 0x06-09: Overwritten with pointer to decompressed sprite pixel data
- 0x13: Current sequence index (starts at 0, changes during playback)
- 0x20: Current frame index
- 0x21: Z-depth (can be modified by movement flags)

### Additional Runtime Fields (NOT in 44-byte file):
The engine allocates MORE memory beyond the 44 bytes:
- +0x2D: Frame delay counter
- +0x2E: Loop counter
- +0x31: Disable after sequence flag

These are mentioned in Ghidra but don't exist in the file structure.

---

## Questions Remaining

1. **What are bytes 0x00-03?** (Sprite 3 has 16, 256 there)
2. **What is byte 0x2A-2B?** (Both sprites have 0x0117)
3. **What is the format of 0x00-05 header?** (mostly zeros except sprite 0 has 0x06 at offset 5)
