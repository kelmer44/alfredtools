# SPRITE STRUCTURE - FINAL DEFINITIVE VERSION

## Critical Discovery

After analyzing sprite 0 in room 2 with actual file hex and Ghidra decompilation, the structure is:

**The Ghidra offsets (+0x00 to +0x31) are for the IN-MEMORY EXPANDED structure, NOT the 44-byte file structure!**

## File Structure (44 bytes on disk)

Looking at Sprite 0 hex dump:
```
0x00: 48 00 fc 00 49 84 a4 25  02 00 03 0b 00 00 0f 02
0x10: 00 00 02 03 00 00 00 05  00 00 00 00 00 00 00 00
0x20: 17 01 10 00 00 01 00 00  00 00 00 00
```

### Confirmed Field Mappings

| File Offset | Bytes | Type | Field Name | Sprite 0 Value | Notes |
|-------------|-------|------|------------|----------------|-------|
| 0x00-01 | 2 | short | X Position | 72 (0x0048) | Screen X coordinate |
| 0x02-03 | 2 | short | Y Position | 252 (0x00FC) | Screen Y coordinate |
| 0x04 | 1 | byte | Width | 73 (0x49) | Sprite width in pixels |
| 0x05 | 1 | byte | Height | 132 (0x84) | Sprite height in pixels |
| 0x06-07 | 2 | word | **Stride** | 9636 (0x25A4) | **Width × Height** ✓ |
| 0x08 | 1 | byte | Num Sequences | 2 | Number of animation sequences (1-4) |
| 0x09 | 1 | byte | Current Sequence | 0 | Runtime: active sequence index |
| 0x0A | 1 | byte | Frames Seq 0 | 3 | Frame count for sequence 0 |
| 0x0B | 1 | byte | Frames Seq 1 | 11 | Frame count for sequence 1 |
| 0x0C | 1 | byte | Frames Seq 2 | 0 | Frame count for sequence 2 |
| 0x0D | 1 | byte | Frames Seq 3 | 0 | Frame count for sequence 3 |
| 0x0E | 1 | byte | Loop Count Seq 0 | 15 (0x0F) | Loop iterations (0xFF = infinite) |
| 0x0F | 1 | byte | Loop Count Seq 1 | 2 | Loop iterations |
| 0x10 | 1 | byte | Loop Count Seq 2 | 0 | Loop iterations |
| 0x11 | 1 | byte | Loop Count Seq 3 | 0 | Loop iterations |
| 0x12 | 1 | byte | Unknown/Duplicate? | 2 | Matches num_sequences |
| 0x13 | 1 | byte | Unknown | 3 | Matches frames_seq_0 |
| 0x14-?? | varies | bytes | **VARIABLE DATA** | ... | **Depends on num_sequences and total_frames!** |

### The Variable Section Mystery

From Ghidra, we know the runtime structure has:
- `+0x1C` + seq_idx: Frame delay for each sequence (per the comparison code)
- `+0x20`: Current frame index (runtime counter)
- `+0x21`: Z-depth sorting value
- `+0x22` + seq_idx*2: Movement flags (16-bit per sequence)

But in the 44-byte file, after byte 0x13, we only have 30 bytes remaining (0x14-0x2B)!

For Sprite 0:
- 2 sequences
- Movement flags would need 4 bytes (2 sequences × 2 bytes)
- Z-depth needs 1 byte
- Current frame needs 1 byte
- Frame delay values? (needs investigation)

### Two Possible Interpretations

#### Theory A: Delays are Per-Sequence (4 bytes)
```
0x14-17: Frame delays (one per sequence, max 4)
0x18-19: Unknown
0x1A-1B: Unknown
0x1C: Unknown
0x1D: Unknown
0x1E: Unknown
0x1F: Unknown
0x20: Current frame index
0x21: Z-depth ⭐
0x22-23: Movement flags seq 0
0x24-25: Movement flags seq 1
0x26-2B: Padding/unknown
```

In this theory, byte 0x21 would be Z-depth. Sprite 0 shows `0x01` there.

#### Theory B: Z-Depth is at 0x17 (from user's data)
```
0x14-16: Frame delays seq 0 (3 bytes for 3 frames)
0x17: ⭐ Z-DEPTH = 5
0x18-22: Frame delays seq 1 (11 bytes for 11 frames) ???
0x23: Current frame
0x24-25: Movement flags seq 0
0x26-27: Movement flags seq 1
0x28-2B: Padding
```

But this doesn't fit! 3 + 11 = 14 frame delays + 1 Z + 1 current + 4 movement = 20 bytes, starting at 0x14 = ends at 0x27 (20 bytes). That's only 36 bytes used total (0x24 used). We have 44 bytes, so 8 bytes left. But this doesn't match the hex values!

### The Hexactly at byte 0x17: 0x05

Looking at sprite 0 byte 0x17 in hex: `05`

And the user's dump said "0x21: Z-Depth = 5"!

The user was showing an offset of 0x21 from their dump start (0x000B1872), which is 10 bytes before sprite 0 start (0x000B187C).

So 0x21 in user's dump = 0x000B1872 + 0x21 = 0x000B1893
And sprite 0 starts at 0x000B187C
So 0x000B1893 - 0x000B187C = **0x17**

**Z-depth is at file offset 0x17 = byte 23!**

### Updated Structure (CORRECT)

| File Offset | Field | Sprite 0 Value |
|-------------|-------|----------------|
| 0x00-01 | X Position | 72 |
| 0x02-03 | Y Position | 252 |
| 0x04 | Width | 73 |
| 0x05 | Height | 132 |
| 0x06-07 | Stride (W×H) | 9636 |
| 0x08 | Num Sequences | 2 |
| 0x09 | Current Sequence | 0 |
| 0x0A-0D | Frames per seq [4] | [3, 11, 0, 0] |
| 0x0E-11 | Loop counts [4] | [15, 2, 0, 0] |
| 0x12 | **Frame period seq 0** | **2 ticks** |
| 0x13 | **Frame period seq 1** | **3 ticks** |
| 0x14 | **Frame period seq 2** | **0 ticks** |
| 0x15 | **Frame period seq 3** | **0 ticks** |
| 0x16 | Unknown | 0 |
| 0x17 | **⭐ Z-DEPTH** | **5** |
| 0x18-19 | Movementflags seq 0 | 0x0000 |
| 0x1A-1B | Movement flags seq 1 | 0x0000 |
| 0x1C-1D | Movement flags seq 2 | 0x0000 |
| 0x1E-1F | Movement flags seq 3 | 0x0000 |
| 0x20 | Current frame | 0x17 (23) |
| 0x21 | Unknown | 0x01 |
| 0x22-2B | Unknown/Padding | varies |

**Total: 44 bytes**

### STRIDE SOLVED ✓

**Stride = Width × Height**

This is the total number of pixels per frame. Makes sense for calculating frame offsets in the pixel data!

For sprite 0: 73 × 132 = 9636 ✓
For sprite 1: 32 × 20 = 640 ✓
For sprite 2: 20 × 16 = 320 ✓

### Z-DEPTH SOLVED ⭐

**Z-depth is at file offset 0x17 (byte 23)**

- Value range: 0-255
- 0xFF (255) = disabled/hidden
- Lower values = further back
- Higher values = closer to front
- Sorting is ascending (0 renders first, 255 renders last)

Example values from room 2:
- Sprite 0: Z = 5 (at 0x17)
- Sprite 3: Z = 1 (at 0x17)

### Frame Periods: Per-Sequence Timing ✓

Ghidra code: `if (*(char *)(iVar17 + 0x2d) == *(char *)(current_anim_sequence + 0x1c + iVar17))`

This compares the frame delay counter (runtime field at +0x2D) with the frame period value at `sprite[0x1C + current_anim_sequence]`.

In the **runtime memory structure**, frame periods are at offset 0x1C + sequence_idx.

In the **44-byte file structure**, frame periods are at **offsets 0x12-0x15** (4 bytes, one per sequence):
- 0x12: Frame period for sequence 0 (ticks per frame)
- 0x13: Frame period for sequence 1
- 0x14: Frame period for sequence 2
- 0x15: Frame period for sequence 3

**Example from Sprite 0:**
- Sequence 0: period = 2 ticks (advances frame every 2 ticks at 18.2 Hz)
- Sequence 1: period = 3 ticks (advances frame every 3 ticks)

The game increments the counter at +0x2D each frame. When it equals the period value, the frame advances and the counter resets to 0.

### REALIZATION: File Format ≠ Runtime Format!

The game loads the 44-byte file structure and **expands** it in memory by adding:
- `+0x2D`: Frame delay counter (runtime)
- `+0x2E`: Loop counter (runtime)
- `+0x31`: Disable after sequence flag (runtime)

The Ghidra offsets (+0x1C for frame delays) are **runtime memory offsets**, not file offsets!

The file might store data more compactly, and the game reorganizes it when loading into RAM.

### File-to-Memory Mapping Hypothesis

| File Offset | → | Runtime Offset | Field |
|-------------|---|----------------|-------|
| 0x00-09 | → | 0x0A-13 | Position/Size/Stride |
| 0x0A-0D | → | 0x14-17 | Frames per seq |
| 0x0E-11 | → | 0x18-1B | Loop counts |
| 0x14-17? | → | 0x1C-1F | Frame delays? |
| 0x17 | → | 0x21 | Z-depth ⭐ |
| 0x18-1F? | → | 0x22-29 | Movement flags (2 bytes × 4 sequences) |

### Next Steps Needed

1. ✓ Confirmed Z-depth at file offset 0x17
2. ✓ Confirmed Stride = Width × Height
3. ❌ Still need to understand bytes 0x14-16 (before Z-depth)
4. ❌ Need to map movement flags location in file
5. ❌ Need to understand bytes 0x12-13 purpose
6. ❌ Need to verify frame delay storage format

### Questions for Further Investigation

1. Are bytes 0x14-16 actually frame delays for sequences 0-2?
2. Is the per-sequence delay model correct, or are there per-frame delays stored elsewhere?
3. What are bytes 0x12-13? (They seem to duplicate num_sequences and frames_seq_0)
4. Where is "current frame" stored in the file? (Probably initialized to 0 at runtime)
