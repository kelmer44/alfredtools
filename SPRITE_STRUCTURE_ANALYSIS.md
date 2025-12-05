# SPRITE STRUCTURE - FINAL CORRECTED VERSION

## Based on Room 2, Sprite 0 Analysis

File offset: 0x000B187C

```
Hex: 48 00 FC 00 49 84 A4 25 02 00 03 0B 00 00 0F 02
     00 00 02 03 00 00 00 05 00 00 00 00 00 00 00 00
     17 01 10 00 00 01 00 00 00 00 00 00
```

## 44-Byte Structure Layout

| Offset | Bytes | Type | Name | Example Value | Notes |
|--------|-------|------|------|---------------|-------|
| 0x00 | 2 | short | X Position | 72 (0x0048) | Screen X coordinate |
| 0x02 | 2 | short | Y Position | 252 (0x00FC) | Screen Y coordinate |
| 0x04 | 1 | byte | Width | 73 | Sprite width in pixels |
| 0x05 | 1 | byte | Height | 132 | Sprite height in pixels |
| 0x06 | 2 | word | **Stride** | 9636 (0x25A4) | **Purpose TBD** - Related to frame layout? |
| 0x08 | 1 | byte | **Num Sequences** | 2 | Number of animation sequences |
| 0x09 | 1 | byte | Current Sequence | 0 | Runtime: active sequence index |
| 0x0A | 1 | byte | Frames in Seq 0 | 3 | Frame count for sequence 0 |
| 0x0B | 1 | byte | Frames in Seq 1 | 11 | Frame count for sequence 1 |
| 0x0C | 1 | byte | Frames in Seq 2 | 0 | Frame count for sequence 2 |
| 0x0D | 1 | byte | Frames in Seq 3 | 0 | Frame count for sequence 3 |
| 0x0E | 1 | byte | Loop Count Seq 0 | 15 | Loop iterations (0xFF = infinite) |
| 0x0F | 1 | byte | Loop Count Seq 1 | 2 | Loop iterations |
| 0x10 | 1 | byte | Loop Count Seq 2 | 0 | Loop iterations |
| 0x11 | 1 | byte | Loop Count Seq 3 | 0 | Loop iterations |
| 0x12 | 1 | byte | Num Sequences (dup?) | 2 | Duplicate of 0x08? |
| 0x13 | 1 | byte | Unknown | 3 | Possibly related to frame count? |
| 0x14 | N | bytes | **Frame Delays** | [varies] | **Variable length!** One byte per frame (sum of all sequences) |
| ... | ... | ... | ... | ... | Frame delays continue based on total frame count |
| 0x20 | 1 | byte | Current Frame | varies | Runtime: current frame in sequence |
| 0x21 | 1 | byte | **Z-Depth** | 1-5 | **Depth layer** (0xFF = disabled) |
| 0x22+ | varies | bytes | **Movement Flags?** | varies | Need more analysis |
| ... | ... | ... | ... | ... | ... |
| 0x2B | ... | byte | End | ... | Last byte of 44-byte structure |

**Total**: 44 bytes (0x2C)

---

## Key Findings

### 1. Stride Field (0x06-07)
- Sprite 0: stride = 9636, width = 73, total frames = 14 (3+11)
- Calculation: 73 × 132 = 9636 ✓
- **Stride = Width × Height** (total pixels per frame)
- This makes sense for pixel data layout!

### 2. Variable Frame Delay Array
- Starts at offset 0x14
- One byte per frame across ALL sequences
- For Sprite 0: 14 frames total (3 in seq0 + 11 in seq1)
- Frame delays: at offsets 0x14-0x21 (14 bytes)
- **This pushes everything else down!**

### 3. Z-Depth Location
- **Always at offset 0x21** (byte 33)
- Sprite 0: Z-depth = 1
- Sprite 1: Z-depth = 1  
- Sprite 2: Z-depth = 1
- Range: 0-255, where 0xFF = disabled

### 4. Movement Flags Location
- Start after frame delays
- For Sprite 0 with 14 frames:
  - Frame delays end at 0x21 (inclusive)
  - Movement flags start at 0x22
- **Per sequence** (2 bytes each)
  - Sequence 0 flags at 0x22-23
  - Sequence 1 flags at 0x24-25
  - etc.

---

## Corrected 44-Byte Layout (Fixed Offsets)

```
0x00  X Position (2 bytes)
0x02  Y Position (2 bytes)
0x04  Width (1 byte)
0x05  Height (1 byte)
0x06  Stride = Width × Height (2 bytes)
0x08  Num Sequences (1 byte)
0x09  Current Sequence Index (1 byte) [runtime]
0x0A  Frames in Sequence 0 (1 byte)
0x0B  Frames in Sequence 1 (1 byte)
0x0C  Frames in Sequence 2 (1 byte)
0x0D  Frames in Sequence 3 (1 byte)
0x0E  Loop Count Sequence 0 (1 byte)
0x0F  Loop Count Sequence 1 (1 byte)
0x10  Loop Count Sequence 2 (1 byte)
0x11  Loop Count Sequence 3 (1 byte)
0x12  Num Sequences (duplicate?) (1 byte)
0x13  Unknown byte (1 byte)
0x14  Frame Delay 0 (1 byte)
0x15  Frame Delay 1 (1 byte)
0x16  Frame Delay 2 (1 byte)
...   (continues for total_frames)
0x14+N-1  Last Frame Delay
0x14+N    Current Frame Index (1 byte) [runtime]
0x15+N    Z-Depth (1 byte) ⭐⭐⭐
0x16+N    Movement Flags Seq 0 Low (1 byte)
0x17+N    Movement Flags Seq 0 High (1 byte)
0x18+N    Movement Flags Seq 1 Low (1 byte)
0x19+N    Movement Flags Seq 1 High (1 byte)
...       (continues for num_sequences)
0x2B      End of 44-byte structure
```

**Where N = total frame count across all sequences**

---

## Wait, This Doesn't Work!

Looking at Sprite 0:
- Total frames = 14
- Frame delays at 0x14-0x21 (14 bytes)
- That puts us at offset 0x22 after the last delay
- But we saw data at 0x20 and 0x21 in the hex dump!

Let me recount. The hex dump shows:
```
0x10: 00 00 02 03  00 00 00 05  00 00 00 00  00 00 00 00
      |-----|----  |-----|----  |-----|----  |-----|----
      0x10-11     0x12-13       0x14-15      0x16-17
      
0x20: 17 01 10 00  00 01 00 00  00 00 00 00
      |--|--|----- -|----|----  |-----------|
      20 21 22-23  24-25         rest
```

At offset 0x20 we have: 0x17 (23)
At offset 0x21 we have: 0x01 (1) ← **This is Z-depth!**

So frame delays DON'T start at 0x14. Let me reanalyze...

Looking at the parse, it says:
- 0x12: Num Sequences = 2
- 0x13: Byte 13 = 3
- 0x14-17: Frames/seq = [0, 0, 0, 5]
- 0x18-1B: Loop counts = [0, 0, 0, 0]

But we know:
- Sequence 0 has 3 frames (byte 0x0A = 3)
- Sequence 1 has 11 frames (byte 0x0B = 11)

So the parser is reading the wrong offsets! The arrays at 0x14-17 and 0x18-1B are being read AFTER we already read them at 0x0A-0x11.

The structure must be that 0x0A-0x11 ARE the frame/loop arrays, and 0x14+ is frame delays!

Total frames = 3 + 11 = 14
Frame delays start at 0x14
Frame delays are bytes 0x14, 0x15, 0x16... up to 0x14+13 = 0x21

NO WAIT. Let me count bytes carefully:
- 0x14 is byte index 20
- 14 frame delays would occupy bytes 20-33
- Byte 20 = 0x14
- Byte 33 = 0x14 + 13 = 0x21

So frame delay 0 is at 0x14
Frame delay 13 is at 0x21

But looking at the hex, byte at 0x21 is 0x01, which is too small to be a frame delay (others are 0, 2, 3, 5 from what we've seen).

I think the issue is that not all frames have delays stored! Let me check Ghidra again for the access pattern.
