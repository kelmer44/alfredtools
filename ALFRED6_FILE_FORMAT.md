# ALFRED.6 File Format Documentation

## Overview

The ALFRED.6 file contains a collection of sprite images called "pegatinas" (stickers) used throughout the game. These are indexed-color bitmap images with positioning metadata, organized sequentially in the file.

**File Size:** 531,053 bytes (0x81A6D)
**Total Sprites:** 137 sprites (indices 0-136)
**Access Method:** Direct offset table (no directory structure)

### How the Game Retrieves Specific Stickers

The game uses a **hardcoded offset table** to directly access each sprite. To retrieve sprite N (e.g., sprite 12):

1. **Look up the offset** in the pre-built offset table: `pegatina_offsets[12] = 0x0092C4`
2. **Seek to that offset** in ALFRED.6
3. **Read the 6-byte header** to get x, y, width, height
4. **Read width × height bytes** of pixel data
5. **Apply the room-specific palette** from the `tablapaletas` array

```c
// To load sprite 12:
unsigned int offset = pegatina_offsets[12];  // 0x0092C4
fseek(fp, offset, SEEK_SET);
fread(&header, 6, 1, fp);  // Read x=190, y=251, w=48, h=90
fread(pixels, 48 * 90, 1, fp);  // Read 4320 pixels
// Apply palette from room tablapaletas[12] = 4
```

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

## Sprite Offset Table

The game accesses sprites using a **pre-built offset table** stored in the executable. This table contains the file offset for each of the 137 sprites.

### Complete Offset Table

```c
unsigned int pegatina_offsets[137] = {
    0x000000, 0x00005B, 0x0000B6, 0x000298, 0x00047A, 0x0023C8,  // 0-5
    0x004316, 0x004376, 0x005119, 0x005EBC, 0x0083ED, 0x008529,  // 6-11
    0x0092C4, 0x00A3AA, 0x00B490, 0x00B6A6, 0x00C05A, 0x00CA0E,  // 12-17
    0x00D3D0, 0x00D46E, 0x00F036, 0x00FB8F, 0x00FC55, 0x0119D7,  // 18-23
    0x013759, 0x01391F, 0x014A9D, 0x015C1B, 0x017601, 0x018FE7,  // 24-29
    0x019048, 0x0190A9, 0x01910A, 0x0197F4, 0x019EDE, 0x01A7EC,  // 30-35
    0x01B0FA, 0x01B8C4, 0x01C644, 0x01D83A, 0x01E104, 0x01E8C6,  // 36-41
    0x01F45D, 0x01FBBB, 0x02011D, 0x02052F, 0x020A95, 0x020E5B,  // 42-47
    0x0210B3, 0x0216E6, 0x021D5E, 0x0233A3, 0x0249E8, 0x025777,  // 48-53
    0x026506, 0x028E2B, 0x02B82F, 0x02C9D7, 0x02E4CA, 0x02FFBD,  // 54-59
    0x03234A, 0x0346D7, 0x036A83, 0x038E2F, 0x03B18D, 0x03D4EB,  // 60-65
    0x03DEC9, 0x03F813, 0x04115D, 0x045303, 0x0494A9, 0x04955F,  // 66-71
    0x049615, 0x0496CB, 0x0499E1, 0x049EC7, 0x04A023, 0x04A447,  // 72-77
    0x04BA6D, 0x04BFA1, 0x04CE33, 0x04CF09, 0x04DB3B, 0x052885,  // 78-83
    0x0575CF, 0x05775B, 0x057D79, 0x058397, 0x058969, 0x058F50,  // 84-89
    0x05A9DB, 0x05C561, 0x05C72E, 0x05C8FB, 0x05EAC1, 0x060C87,  // 90-95
    0x060D19, 0x060E62, 0x061039, 0x0613C2, 0x061764, 0x061847,  // 96-101
    0x062535, 0x062D4B, 0x064F11, 0x0670D7, 0x067381, 0x0675A9,  // 102-107
    0x0677EF, 0x067A98, 0x067DDE, 0x068115, 0x0684E3, 0x068A76,  // 108-113
    0x068F30, 0x0693C8, 0x0696AD, 0x06C2C9, 0x06C84D, 0x07095D,  // 114-119
    0x071854, 0x07274B, 0x073642, 0x074539, 0x075454, 0x0791DA,  // 120-125
    0x07CF60, 0x07E4AB, 0x07ECED, 0x07F52F, 0x07FD71, 0x080591,  // 126-131
    0x080B24, 0x080B84, 0x080F39, 0x0812F5, 0x0816B1             // 132-136
};
```

### Special Offset Cases

Four sprites have non-sequential offsets that require special handling during sequential scanning:

| Sprite | Offset | Notes |
|--------|--------|-------|
| 37 | 0x1B8C4 | Gap after sprite 36 (0x1B0FA + size = 0x1B716) |
| 67 | 0x3F813 | Gap after sprite 66 (0x3DEC9 + size = 0x3E8B7) |
| 68 | 0x4115D | Gap after sprite 67 (0x3F813 + size = 0x3FD2D) |
| 88 | 0x58969 | Gap after sprite 87 (0x058397 + size = 0x058973) |

These gaps suggest embedded metadata, padding, or file restructuring during development.

## Extraction Process

### Algorithm Overview (Sequential Scanning Method)
This is the method used by the extraction code, which rebuilds the offset table by scanning:

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

### Direct Access Method (How the Game Does It)
The game uses a pre-built offset table for O(1) access:

```c
// To retrieve sprite 12:
unsigned int offset = get_pegatina_offset(12);  // Returns 0x0092C4
fseek(fp, offset, SEEK_SET);

// Read header
unsigned short x = read_word_le(fp);    // 190
unsigned short y = read_word_le(fp);    // 251
unsigned char w = read_byte(fp);        // 48
unsigned char h = read_byte(fp);        // 90

// Read pixel data
unsigned char *pixels = malloc(w * h);  // 4320 bytes
fread(pixels, w * h, 1, fp);

// Get palette
int room_num = tablapaletas[12];  // Room 4
unsigned char *palette = getRoomPalette(room_num);

// Render sprite at position (x, y) using palette
```

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
| File Size | 531,053 bytes (0x81A6D) |
| Total Sprites | 137 (indices 0-136) |
| Header Size | 6 bytes per sprite |
| Pixel Format | 8-bit indexed (palette reference) |
| Byte Order | Little-endian |
| Access Method | Direct offset table lookup |
| Padding | 0xBF marker bytes (variable, early sprites only) |
| Compression | None (raw pixel data) |

## Example: Retrieving Sprite 12

Let's walk through retrieving sprite 12 step by step:

### Step 1: Look Up Offset
```c
sprite_index = 12;
offset = pegatina_offsets[12];  // 0x0092C4 (37,572 bytes)
```

### Step 2: Seek and Read Header
```c
fseek(fp, 0x0092C4, SEEK_SET);
x = read_word_le();  // 190 (0xBE00)
y = read_word_le();  // 251 (0xFB00)
w = read_byte();     // 48
h = read_byte();     // 90
```

### Step 3: Read Pixel Data
```c
pixel_count = 48 * 90 = 4,320 bytes
pixels = fread(fp, 4320);
```

### Step 4: Get Room Palette
```c
room_num = tablapaletas[12];  // Room 4
palette = getRoomPalette(4);   // 256 colors × 4 bytes (RGBA)
```

### Step 5: Render
```c
// Blit the 48×90 sprite at screen position (190, 251)
// Each pixel is an index into the 256-color palette
for (int py = 0; py < 90; py++) {
    for (int px = 0; px < 48; px++) {
        int pixel_index = pixels[py * 48 + px];
        RGBA color = palette[pixel_index];
        screen_buffer[(y + py) * 640 + (x + px)] = color;
    }
}
```

### Memory Layout
```
File offset 0x0092C4:
  +0x00-0x01: BE 00           (x = 190, little-endian)
  +0x02-0x03: FB 00           (y = 251, little-endian)
  +0x04:      30              (width = 48)
  +0x05:      5A              (height = 90)
  +0x06-0x10E5: [4320 bytes]  (pixel data)

Next sprite (13) starts at: 0x0092C4 + 6 + 4320 = 0x00A3AA
```

## Ghidra Analysis Instructions

To find the offset table in the game executable using Ghidra:

1. **Search for the offset values** as 32-bit little-endian integers:
   - Search for `0x0092C4` (sprite 12 offset)
   - Search for `0x01B8C4` (sprite 37 offset - special case)
   - Search for `0x03F813` (sprite 67 offset - special case)

2. **Look for array patterns**:
   - 137 consecutive 32-bit values
   - Starting with `0x00000000`, `0x0000005B`, `0x000000B6`
   - May be in data section or initialized global data

3. **Find references** to this table:
   - Look for code that loads from `table[sprite_index * 4]`
   - Function signature: `load_pegatina(int sprite_index)`
   - May contain bounds check: `if (sprite_index >= 137)`

4. **Identify the loading function**:
   ```c
   void* load_pegatina(int sprite_index) {
       if (sprite_index < 0 || sprite_index >= 137) return NULL;

       unsigned int offset = pegatina_offsets[sprite_index];
       fseek(alfred6_handle, offset, SEEK_SET);

       // Read header
       unsigned short x = fread_word();
       unsigned short y = fread_word();
       unsigned char w = fread_byte();
       unsigned char h = fread_byte();

       // Read pixels
       void* pixels = malloc(w * h);
       fread(pixels, w * h, 1, alfred6_handle);

       return create_sprite(x, y, w, h, pixels);
   }
   ```

5. **Rename variables/functions** as you discover them:
   - `pegatina_offsets` → offset table array
   - `load_pegatina` → sprite loading function
   - `tablapaletas` → room palette mapping table
   - `alfred6_handle` → FILE* for ALFRED.6

## Revision History

- Initial documentation based on `alfred6.c` extraction code analysis
- Discovered hardcoded offset corrections for sprites 37, 67, 68, 88
- Identified 0xBF padding pattern for early sprites
- Mapped complete palette assignment table for 140 sprites
