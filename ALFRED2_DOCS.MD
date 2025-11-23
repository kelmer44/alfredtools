# ALFRED.2 - Talking/Mouth Animation Resource File

## Overview

ALFRED.2 contains talking animations for characters in the game. These are typically mouth/lip-sync animations shown when characters speak. Each animation set contains two animation sequences (often representing different mouth positions like closed/open or different phoneme shapes).

## File Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                     ALFRED.2 File Layout                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Header Block 0 (55 bytes) - may be empty (offset = 0)    │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Header Block 1 (55 bytes) - may be empty                 │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ ...                                                       │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │ Header Block N (55 bytes) - First valid header           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   RLE Compressed Pixel Data               │  │
│  │                                                            │  │
│  │  Animation Set 0, Anim A pixel data (RLE pairs)          │  │
│  │  Animation Set 0, Anim B pixel data (RLE pairs)          │  │
│  │  "BUDA" marker (4 bytes)                                  │  │
│  │                                                            │  │
│  │  Animation Set 1, Anim A pixel data (RLE pairs)          │  │
│  │  Animation Set 1, Anim B pixel data (RLE pairs)          │  │
│  │  "BUDA" marker (4 bytes)                                  │  │
│  │                                                            │  │
│  │  ...                                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Header Block Structure (55 bytes)

Each animation set has a 55-byte header that describes two animation sequences:

```c
struct AnimationSetHeader {
    uint16_t data_offset;        // +0x00: Offset to start of pixel data (little-endian)
    uint8_t  unknown1;           // +0x02: Unknown
    uint8_t  unknown2[6];        // +0x03-0x08: Unknown fields

    // Animation A (typically mouth position 1 or closed mouth)
    uint8_t  anim_a_width;       // +0x09: Width in pixels
    uint8_t  anim_a_height;      // +0x0A: Height in pixels
    uint16_t unknown3;           // +0x0B-0x0C: Unknown
    uint8_t  anim_a_frames;      // +0x0D: Number of animation frames
    uint8_t  unknown4[7];        // +0x0E-0x14: Unknown fields

    // Animation B (typically mouth position 2 or open mouth)
    uint8_t  anim_b_width;       // +0x15: Width in pixels
    uint8_t  anim_b_height;      // +0x16: Height in pixels
    uint16_t unknown5;           // +0x17-0x18: Unknown
    uint8_t  anim_b_frames;      // +0x19: Number of animation frames
    uint8_t  unknown6[24];       // +0x1A-0x36: Unknown/padding fields
};
```

### Key Header Fields

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0x00 | 2 | data_offset | Offset to pixel data (uint16 LE). If 0, header is empty/invalid |
| 0x09 | 1 | anim_a_width | Width of animation A in pixels |
| 0x0A | 1 | anim_a_height | Height of animation A in pixels |
| 0x0D | 1 | anim_a_frames | Number of frames in animation A |
| 0x15 | 1 | anim_b_width | Width of animation B in pixels |
| 0x16 | 1 | anim_b_height | Height of animation B in pixels |
| 0x19 | 1 | anim_b_frames | Number of frames in animation B |

### Palette Association

Each animation set uses a specific palette determined by:

```
palette_id = (header_offset / 55) * 13 + 11
```

For example:
- Header at offset 0: palette_id = 11
- Header at offset 55: palette_id = 24
- Header at offset 110: palette_id = 37

## Pixel Data Format

### RLE Compression

Pixel data is compressed using simple Run-Length Encoding (RLE):

```
Compressed: [count] [color_index] [count] [color_index] ...
```

Each RLE pair consists of:
- **1 byte**: Count (number of times to repeat the color)
- **1 byte**: Color index (palette index 0-255)

Example:
```
0x10 0x00 → 16 pixels of color 0 (often background/transparent)
0x01 0x3F → 1 pixel of color 63
0x08 0x12 → 8 pixels of color 18
```

### Data Layout

For each animation set:

1. **Animation A frames** (all frames sequentially)
   - Frame 0: `width × height` pixels (RLE compressed)
   - Frame 1: `width × height` pixels (RLE compressed)
   - ...
   - Frame N-1: `width × height` pixels (RLE compressed)

2. **Animation B frames** (all frames sequentially)
   - Frame 0: `width × height` pixels (RLE compressed)
   - Frame 1: `width × height` pixels (RLE compressed)
   - ...
   - Frame N-1: `width × height` pixels (RLE compressed)

3. **"BUDA" marker** (4 bytes: 0x42 0x55 0x44 0x41)
   - Marks the end of this animation set's data

### Frame Storage

Frames within each animation are stored as horizontal strips. The extraction code arranges them as:

```
┌───────┬───────┬───────┬─────────┐
│Frame 0│Frame 1│Frame 2│  ...   │
└───────┴───────┴───────┴─────────┘
  width   width   width
```

## Palette Format

Palettes are stored in separate files (likely in ALFRED.1 or external palette files) with filename pattern `out_XXX` where XXX is the palette_id.

**Palette Structure:**
- 768 bytes total (256 colors × 3 bytes RGB)
- VGA 6-bit color format (values 0-63)
- Must be converted to 8-bit by multiplying by 4 (or left-shifting by 2)

```c
struct Palette {
    uint8_t entries[256][3];  // [R, G, B] for each of 256 colors
};

// Conversion to 8-bit RGB:
uint8_t r8 = palette.entries[i][0] * 4;  // or << 2
uint8_t g8 = palette.entries[i][1] * 4;
uint8_t b8 = palette.entries[i][2] * 4;
```

## Usage in Game

Based on the sprite animation system in Ghidra:

```c
// Sprite structure (0x2C = 44 bytes each)
struct Sprite {
    // ... other fields ...
    uint32_t sprite_data_ptr;      // +0x00: Pointer to pixel data
    int16_t  x;                     // +0x0A: X coordinate
    int16_t  y;                     // +0x0C: Y coordinate
    uint8_t  width;                 // +0x0E: Width
    uint8_t  height;                // +0x0F: Height
    uint16_t stride;                // +0x10: Bytes per scanline
    uint8_t  num_sequences;         // +0x12: Number of animation sequences
    uint8_t  current_sequence;      // +0x13: Current sequence index
    uint8_t  frames_per_sequence[]; // +0x14: Frames in each sequence
    // ... more fields ...
    uint8_t  current_frame;         // +0x20: Current frame in sequence
    int8_t   z_depth;              // +0x21: Z-depth (-1 = disabled)
    uint16_t movement_flags[];      // +0x22: Movement flags per frame
    uint8_t  frame_delay_counter;   // +0x2D: Frame timing counter
    uint8_t  loop_counter;          // +0x2E: Loop counter
    uint8_t  disable_after_sequence; // +0x31: Disable flag
};
```

Talking animations from ALFRED.2 are likely loaded into sprite structures and animated during dialogue sequences.

## Extraction Algorithm

```python
def extract_animation(data, header_offset):
    # Parse header
    header = data[header_offset:header_offset + 55]
    data_offset = struct.unpack('<H', header[0:2])[0]

    anim_a_w = header[9]
    anim_a_h = header[10]
    anim_a_frames = header[13]

    anim_b_w = header[21]
    anim_b_h = header[22]
    anim_b_frames = header[25]

    # Decompress animation A
    pixels_a = decompress_rle(
        data,
        data_offset,
        anim_a_w * anim_a_h * anim_a_frames
    )

    # Decompress animation B (starts after animation A)
    # Note: Need to track actual RLE byte position, not pixel count
    pixels_b = decompress_rle(
        data,
        data_offset + compressed_size_a,
        anim_b_w * anim_b_h * anim_b_frames
    )

    return pixels_a, pixels_b

def decompress_rle(data, start, max_pixels):
    result = []
    pos = start

    while len(result) < max_pixels:
        if data[pos:pos+4] == b'BUDA':
            break

        count = data[pos]
        color = data[pos + 1]
        result.extend([color] * count)
        pos += 2

    return result
```

## Related Files

- **ALFRED.1**: Room backgrounds, sprites, palettes
- **ALFRED.3-9**: Other game resources (audio, objects, etc.)
- **Palette files**: `out_XXX` format containing 768-byte VGA palettes

## Notes

1. The first few headers in the file may have `data_offset = 0`, indicating they are unused/empty slots
2. The "BUDA" marker (ASCII: "BUDA") is used as a sentinel between animation sets
3. Animation A and B are typically alternated during dialogue to create lip-sync effect
4. Some animation sets may have 0 frames, indicating they are not used
5. The compression ratio is typically 2-5x depending on the content

## Tools

- `analyze_alfred2.py`: Analyze file structure and list all animation sets
- `extract_alfred2.py`: Extract all animations to PNG files
- Original `main2.cpp`: Reference Qt/C++ extractor by original author
