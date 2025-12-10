# ALFRED.6 File Format Documentation

## Overview

The ALFRED.6 file contains a collection of sprite images called "pegatinas" (stickers) used throughout the game. These are indexed-color bitmap images with positioning metadata, organized sequentially in the file.

## File Structure

The file consists of a series of sprite records, each containing:
- Header with positioning and dimension data
- Raw indexed pixel data
- Optional padding bytes (0xBF separators)

### Sprite Record Structure

Each sprite ("pegatina") has the following binary structure:

```
Offset  Size  Type     Description
------  ----  -------  -----------
0x00    2     WORD     X position (little-endian)
0x02    2     WORD     Y position (little-endian)
0x04    1     BYTE     Width (in pixels)
0x05    1     BYTE     Height (in pixels)
0x06    W*H   BYTES    Raw indexed pixel data (row-major order)
```

### Total Record Size
```
Record Size = 6 + (Width × Height) bytes
```

## Data Layout

### Header (6 bytes)
- **X Position** (offset+0, offset+1): 16-bit little-endian value for horizontal screen position
- **Y Position** (offset+2, offset+3): 16-bit little-endian value for vertical screen position
- **Width** (offset+4): 8-bit value, sprite width in pixels
- **Height** (offset+5): 8-bit value, sprite height in pixels

### Pixel Data
- Starts immediately after the 6-byte header
- Organized in row-major order (left-to-right, top-to-bottom)
- Each pixel is a single byte representing a palette index (0-255)
- Total pixels = Width × Height

## Padding and Separators

### 0xBF Marker Bytes
- Used as separators between sprite records (primarily for the first 6 sprites)
- The extraction code skips over consecutive 0xBF bytes after each sprite
- For sprites 0-5: the code searches for the next 0xBF marker, then skips all consecutive 0xBF bytes
- For sprites 6+: no 0xBF scanning is performed

### Padding Logic
```c
offset += (width * height) + 6;  // Move past current sprite

if (j < 6) {
    // Find next 0xBF separator
    while (buffer[offset] != 0xBF)
        offset++;
}

// Skip all consecutive 0xBF bytes
while (buffer[offset] == 0xBF)
    offset++;
```

## Palette Mapping

Each sprite is associated with a room-specific palette through the `tablapaletas` lookup table.

### Palette Assignment Table
The file contains 140 sprite entries, each mapped to a room palette ID:

```c
int tablapaletas[140] = {
    0,0,0,0,0,0,0,          // Sprites 0-6: Room 0
    2,2,                     // Sprites 7-8: Room 2
    3,3,3,3,3,3,3,3,        // Sprites 9-16: Room 3
    4,4,4,4,4,               // Sprites 17-21: Room 4
    5,5,                     // Sprites 22-23: Room 5
    7,                       // Sprite 24: Room 7
    8,8,                     // Sprites 25-26: Room 8
    9,9,9,9,9,               // Sprites 27-31: Room 9
    12,12,                   // Sprites 32-33: Room 12
    13,13,13,                // Sprites 34-36: Room 13
    12,                      // Sprite 37: Room 12
    15,15,15,15,15,15,15,15,15,15,15,15,  // Sprites 38-49: Room 15
    16,16,                   // Sprites 50-51: Room 16
    17,17,                   // Sprites 52-53: Room 17
    19,19,19,19,19,          // Sprites 54-58: Room 19

    0,0,0,0,0,0,0,           // Sprites 59-65: Room 0
    33,33,                   // Sprites 66-67: Room 33
    29,29,                   // Sprites 68-69: Room 29
    0,0,0,                   // Sprites 70-72: Room 0

    34,35,31,25,             // Sprites 73-76: Various rooms
    31,                      // Sprite 77: Room 31
    32,                      // Sprite 78: Room 32
    21,25,                   // Sprites 79-80: Rooms 21, 25
    0,                       // Sprite 81: Room 0
    0,0,0,0,0,               // Sprites 82-86: Room 0
    4,4,4,4,                 // Sprites 87-90: Room 4
    0,0,0,0,                 // Sprites 91-94: Room 0
    0,0,0,0,0,0,             // Sprites 95-100: Room 0
    33,33,                   // Sprites 101-102: Room 33
    47,47,                   // Sprites 103-104: Room 47
    52,52,52,52,52,          // Sprites 105-109: Room 52
    52,52,52,52,52,52,       // Sprites 110-115: Room 52
    41,                      // Sprite 116: Room 41
    0,                       // Sprite 117: Room 0
    30,                      // Sprite 118: Room 30
    44,44,44,44,             // Sprites 119-122: Room 44
    31,                      // Sprite 123: Room 31
    46,46,                   // Sprites 124-125: Room 46
    31,                      // Sprite 126: Room 31
    51,52,53,54              // Sprites 127-130: Various rooms
};
```

### Palette Usage
- Each sprite index in the file corresponds to an index in `tablapaletas`
- The value at `tablapaletas[sprite_index]` indicates which room palette to use
- Room palettes are retrieved via the `getRoomPalette(room_num)` function
- Palettes are 256-color RGBA format (256 × 4 = 1024 bytes)

## Special Offset Corrections

Some sprites require manual offset corrections due to non-sequential data:

```c
if (j == 37)  offset = 0x1b8c4;  // Sprite 37 at offset 113,860
if (j == 67)  offset = 0x3f813;  // Sprite 67 at offset 260,115
if (j == 68)  offset = 0x4115d;  // Sprite 68 at offset 266,589
if (j == 88)  offset = 0x58969;  // Sprite 88 at offset 362,857
```

These hardcoded offsets suggest the file may have been manually edited or contains embedded metadata at certain positions.

## Extraction Process

### Algorithm Overview
1. Start at offset 0
2. For each sprite index (j = 0 to file end):
   - Apply special offset if needed (sprites 37, 67, 68, 88)
   - Read 6-byte header (x, y, width, height)
   - If width > 0 and height > 0:
     - Look up room palette ID from `tablapaletas[j]`
     - Read width × height bytes of pixel data
     - Convert to PNG using room-specific palette
     - Save metadata (x, y, width, height, room) to text file
     - Increment sprite counter
   - Advance offset by (width × height + 6)
   - Handle 0xBF padding (for first 6 sprites)
   - Skip consecutive 0xBF bytes
   - Stop if offset >= file size

### Output Files
For each sprite `N`:
- **pegatinaN.png**: Indexed-color PNG image with room palette
- **pegatinaN.txt**: Metadata file containing:
  ```
  x=<X position>
  y=<Y position>
  width=<Width>
  height=<Height>
  room=<Room number>
  ```

## Data Characteristics

### Valid Sprite Detection
- Sprites are considered valid if both width > 0 AND height > 0
- Invalid entries (width=0 or height=0) are skipped

### Image Format
- **Color depth**: 8-bit indexed color (palette-based)
- **Typical dimensions**: Variable, determined by width/height fields
- **Encoding**: Raw uncompressed pixel data
- **Byte order**: Little-endian for multi-byte values

### File Boundaries
- Extraction continues until `offset >= file_size`
- Total sprite count: up to 140 sprites (based on palette table size)
- Actual sprite count may be fewer depending on file content

## Implementation Notes

### Memory Handling
- The extraction allocates a large buffer (10000 × 10000 × 4 bytes)
- Each sprite's pixel data is allocated separately based on actual dimensions
- Palettes are dynamically retrieved and freed after use

### Error Handling
- Palette retrieval failures skip the sprite
- Memory allocation failures skip the sprite
- Invalid dimensions (0 width or height) skip the sprite
- PNG encoding errors are reported but don't halt extraction

## Use Case

These "pegatinas" are likely used for:
- UI elements and overlays
- Room decorations and props
- Interactive objects
- Character sprites or animations
- Text boxes or dialog elements

The positioning metadata (x, y) suggests these are screen-space sprites blitted directly at specific coordinates, rather than world-space objects.

## Related Files

- **Palette files**: Room-specific color palettes (referenced via `getRoomPalette()`)
- **ALFRED.7**: Possibly contains sprite animations or additional graphics
- **Room files**: May reference these sprites by index for placement

## Technical Specifications Summary

| Property | Value |
|----------|-------|
| File Format | Binary, sequential sprite records |
| Header Size | 6 bytes per sprite |
| Pixel Format | 8-bit indexed (palette reference) |
| Byte Order | Little-endian |
| Max Sprites | 140 (based on palette table) |
| Padding | 0xBF marker bytes (variable) |
| Compression | None (raw pixel data) |

## Revision History

- Initial documentation based on `alfred6.c` extraction code analysis
- Discovered hardcoded offset corrections for sprites 37, 67, 68, 88
- Identified 0xBF padding pattern for early sprites
- Mapped complete palette assignment table for 140 sprites
