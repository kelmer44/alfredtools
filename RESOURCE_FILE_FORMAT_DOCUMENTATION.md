# Alfred Pelrock (1997) - Resource File Format Documentation

Complete documentation of all resource file formats for Alfred Pelrock, a DOS point-and-click adventure game developed in 1997.

## Table of Contents

1. [File Overview](#file-overview)
2. [ALFRED.1 - Main Game Data](#alfred1---main-game-data)
3. [ALFRED.4 - UI Graphics](#alfred4---ui-graphics)
4. [ALFRED.7 - Sprites and Cursors](#alfred7---sprites-and-cursors)
5. [ALFRED.9 - Fonts and Remap Tables](#alfred9---fonts-and-remap-tables)
6. [Common Structures](#common-structures)

---

## File Overview

| File | Size | Purpose | Primary Contents |
|------|------|---------|------------------|
| **ALFRED.1** | ~12.9 MB | Main game data | Backgrounds, room data, sprites, animations, palettes, text |
| **ALFRED.4** | ~43 KB | UI graphics | Popup icons, speech balloons |
| **ALFRED.7** | ~3.6 MB | Additional sprites | Sprite data, cursor graphics |
| **ALFRED.9** | ~146 KB | System data | Fonts, color remap tables, room configuration |
| **JUEGO.EXE** | - | Game executable | Game logic, rendering engine |

---

## ALFRED.1 - Main Game Data

**Size:** 12,915,352 bytes (12.32 MB)
**Format:** Binary data file with directory structure
**Endianness:** Little-endian (Intel x86)

### File Structure

ALFRED.1 is organized as a **room-based file system** with 56 rooms, each described by 13 data pairs (offset + size).

```
Offset 0x0000: Room Directory (56 rooms × 104 bytes = 5,824 bytes)
    Room 0:  13 pairs (104 bytes)
    Room 1:  13 pairs (104 bytes)
    ...
    Room 55: 13 pairs (104 bytes)

Offset 0x16C0+: Actual Data (referenced by directory)
```

### Room Directory Structure

Each room entry is **104 bytes** (13 pairs of `<u32 offset, u32 size>`):

```c
struct RoomEntry {
    struct Pair {
        u32 offset;  // Absolute file offset
        u32 size;    // Size in bytes
    } pairs[13];
} rooms[56];
```

### Room Data Pairs

| Pair | Offset | Size | Purpose | Compression | Notes |
|------|--------|------|---------|-------------|-------|
| **0-7** | varies | varies | **Background blocks** | RLE or raw | 8 blocks combined for 640×400 bg |
| **8** | varies | varies | **Sprite pixel data** | RLE | Raw indexed bitmap data for sprites |
| **9** | varies | varies | **Room objects** | varies | Object/animation definitions |
| **10** | varies | varies | **Room data** | varies | Hotspots, walkboxes, exits, text, sprites |
| **11** | varies | 0x300 | **Palette** | Raw | 256-color VGA palette (768 bytes) |
| **12** | varies | varies | **Additional data** | varies | Unknown/unused in most rooms |

### Pair 0-7: Background Blocks

**Purpose:** Store the 640×400 pixel room background in 8 segments
**Total Size:** 256,000 bytes (640 × 400) uncompressed
**Format:** Indexed color (8-bit per pixel)
**Compression:** RLE (Run-Length Encoding) or raw

**Special Size Markers:**
- `size == 0x8000` (32,768): Uncompressed 32KB block
- `size == 0x6800` (26,624): Uncompressed ~26KB block (only Pair 7)
- Other sizes: RLE compressed

**Extraction:**
```python
# Decompress all 8 blocks and concatenate
background = bytearray()
for pair_idx in range(8):
    block_data = decompress_rle_or_raw(data, pair_offset, pair_size)
    background.extend(block_data)

# Should total 256,000 bytes
assert len(background) == 640 * 400
```

### Pair 8: Sprite Pixel Data

**Purpose:** Raw pixel data for all sprite/animation frames in the room
**Format:** Indexed color bitmap data
**Compression:** RLE compressed
**Layout:** Sequential frames with no separators

Sprite dimensions and frame counts are defined in **Pair 10** (sprite headers).

```
[Frame 0: W×H pixels] [Frame 1: W×H pixels] ... [Frame N: W×H pixels]
```

### Pair 10: Room Data Structure

**Purpose:** Core room gameplay data including sprites, hotspots, walkboxes, exits, and text
**Format:** Complex binary structure with multiple sections
**Size:** Varies per room (typically 1,000-2,000 bytes)

#### Pair 10 Memory Map

| Offset | Size | Type | Description |
|--------|------|------|-------------|
| `0x00-0x01` | 2 | u16 | Unknown header data |
| `0x02-0x04` | 3 | bytes | Unknown |
| `0x05` | 1 | u8 | **Sprite count** (total sprites in room) |
| `0x06+` | varies | - | **Sprite headers** (44 bytes each, see below) |
| `0x1BE` | 1 | u8 | **Exit count** |
| `0x1BF+` | varies | - | **Exit array** (14 bytes each) |
| `0x213` | 1 | u8 | **Walkbox count** |
| `0x218+` | varies | - | **Walkbox array** (9 bytes each) |
| `0x47A` | 1 | u8 | **Static hotspot count** |
| `0x47C+` | varies | - | **Static hotspot array** (9 bytes each) |
| `0x3DA+` | varies | - | **Text pointer table** (4 bytes per pointer) |
| varies | varies | - | **Text data** (null-terminated strings with 0xFF markers) |

#### Sprite Header Structure (44 bytes / 0x2C)

Sprites are stored in Pair 10 starting at offset `sprite_index * 0x2C` (index starts at 1, not 0).

```c
struct SpriteHeader {
    u16 x;                      // +0x00: Screen X position
    u16 y;                      // +0x02: Screen Y position
    u8  width;                  // +0x04: Sprite width in pixels
    u8  height;                 // +0x05: Sprite height in pixels
    u8  extra;                  // +0x06: Unknown
    u8  unknown1;               // +0x07: Unknown
    u8  num_anims;              // +0x08: Number of animation sequences
    u8  unknown3;               // +0x09: Unknown
    u8  num_frames_anim1;       // +0x0A: Frames in animation 1
    u8  num_frames_anim2;       // +0x0B: Frames in animation 2
    u8  num_frames_anim3;       // +0x0C: Frames in animation 3
    u8  num_frames_anim4;       // +0x0D: Frames in animation 4
    u8  repeat_anim1;           // +0x0E: Repeat count for anim 1
    u8  repeat_anim2;           // +0x0F: Repeat count for anim 2
    u8  repeat_anim3;           // +0x10: Repeat count for anim 3
    u8  repeat_anim4;           // +0x11: Repeat count for anim 4
    u8  speed_anim1;            // +0x12: Speed/delay for anim 1
    u8  speed_anim2;            // +0x13: Speed/delay for anim 2
    u8  speed_anim3;            // +0x14: Speed/delay for anim 3
    u8  speed_anim4;            // +0x15: Speed/delay for anim 4
    u8  unknown_22_to_32[11];   // +0x16-0x20: Unknown bytes

    // HOTSPOT IDENTIFICATION FIELDS
    u8  sprite_type;            // +0x21 (33): Type/layer (0xFF = not hotspot eligible)
    u8  action_flags;           // +0x22 (34): Action bitmask (see below)
    u8  unknown_35_to_37[3];    // +0x23-0x25: Unknown
    u8  is_hotspot;             // +0x26 (38): 0x00 = clickable, 0x01+ = not clickable
    u8  unknown_39_to_43[5];    // +0x27-0x2B: Unknown/reserved
};
```

**Hotspot Conditions:**
A sprite becomes a clickable hotspot when ALL of these are true:
1. `sprite_type != 0xFF` (byte +33)
2. `is_hotspot == 0x00` (byte +38)
3. `action_flags != 0x00` (byte +34) - has available actions
4. Sprite is visible (z-index != -1 in runtime memory)

**Action Flags Bitmask (byte +34):**
```
Bit 0 (0x01): Open action
Bit 1 (0x02): Close action
Bit 2 (0x04): Push action
Bit 3 (0x08): Pull action
Bit 4 (0x10): TALK action (confirmed)
Bit 5 (0x20): Unknown action
Bit 6 (0x40): Unknown action
Bit 7 (0x80): Unknown action

Note: LOOK action is always available on all hotspots
```

#### Static Hotspot Structure (9 bytes)

Static hotspots are rectangular trigger zones (not sprites).

```c
struct StaticHotspot {
    u8  type;       // +0x00: Hotspot type/flags
    u16 x;          // +0x01-0x02: X position (LE)
    u16 y;          // +0x03-0x04: Y position (LE)
    u8  width;      // +0x05: Width in pixels
    u8  height;     // +0x06: Height in pixels
    u16 extra;      // +0x07-0x08: Extra data/flags (LE)
};
```

**Location:** Offset `0x47C` in Pair 10
**Count:** Byte at offset `0x47A`

#### Walkbox Structure (9 bytes)

Walkboxes define walkable areas for character pathfinding.

```c
struct Walkbox {
    u16 x;          // +0x00-0x01: X position (LE)
    u16 y;          // +0x02-0x03: Y position (LE)
    u16 width;      // +0x04-0x05: Width (LE)
    u16 height;     // +0x06-0x07: Height (LE)
    u8  flags;      // +0x08: Flags/properties
};
```

**Location:** Offset `0x218` in Pair 10
**Count:** Byte at offset `0x213`

#### Exit Structure (14 bytes)

Exits are trigger zones that transition between rooms.

```c
struct Exit {
    u16 destination_room;   // +0x00-0x01: Target room number (LE)
    u8  flags;              // +0x02: Flags (usually 0x00)
    u16 trigger_x;          // +0x03-0x04: Trigger zone X (LE)
    u16 trigger_y;          // +0x05-0x06: Trigger zone Y (LE)
    u8  trigger_width;      // +0x07: Trigger zone width
    u8  trigger_height;     // +0x08: Trigger zone height
    u16 destination_x;      // +0x09-0x0A: Player X in new room (LE)
    u16 destination_y;      // +0x0B-0x0C: Player Y in new room (LE)
    u8  destination_dir;    // +0x0D: Facing direction (0=right, 1=left, 2=down, 3=up)
};
```

**Location:** Offset `0x1BF` in Pair 10
**Count:** Byte at offset `0x1BE`

#### Text System

**Text Pointer Table:**
- **Location:** Offset `0x3DA` in Pair 10
- **Format:** Array of `u32` absolute file pointers
- **Building:** Scanned dynamically by searching for `0xFF` markers in text data

**Text Data Format:**
- Text strings are stored with `0xFF` byte markers
- Each `0xFF` marker indicates the start of a new text entry
- Text pointer = 2 bytes after the `0xFF` marker
- Strings are null-terminated or terminated by next `0xFF`

**Text Indexing:**
Text descriptions are assigned to sprites/hotspots by **position in combined list**:

```
Text Index 0: First selectable sprite (is_hotspot=0x00)
Text Index 1: Second selectable sprite
...
Text Index N: First static hotspot
Text Index N+1: Second static hotspot
...
```

**Order:** `[selectable_sprites_in_order] + [static_hotspots_in_order]`

**No Text ID in Sprite Structure:** Text index is implicit from sprite/hotspot position.

**Example (Room 2):**
- 4 selectable sprites → Text indices 0, 1, 2, 3
- 6 static hotspots → Text indices 4, 5, 6, 7, 8, 9
- Total: 10 text entries in pointer table

### Pair 11: VGA Palette

**Size:** Always 0x300 (768 bytes)
**Format:** 256 colors × 3 bytes (RGB)
**Color Depth:** 6-bit per channel (0-63 range)

```c
struct VGAPalette {
    struct Color {
        u8 r;  // 0-63 (multiply by 4 for 8-bit)
        u8 g;  // 0-63
        u8 b;  // 0-63
    } colors[256];
};
```

**Conversion to 8-bit:**
```python
r8 = r6 * 4
g8 = g6 * 4
b8 = b6 * 4
```

### RLE Compression Format

**Algorithm:** Simple run-length encoding
**Format:** Pairs of `<count, value>` bytes

```
while not end_of_data:
    count = read_byte()
    value = read_byte()
    output.extend([value] * count)
```

**Termination:** Data ends when encountering:
- `BUDA` marker (0x42 0x55 0x44 0x41)
- End of declared size
- End of file

**Example:**
```
Input:  [05 FF 03 00 02 A5]
Output: [FF FF FF FF FF 00 00 00 A5 A5]
```

---

## ALFRED.4 - UI Graphics

**Size:** 43,866 bytes (~43 KB)
**Purpose:** User interface graphics including popup icons and speech balloons
**Palette:** Uses Palette 11 from ALFRED.1 (Room 0)

### File Structure

| Offset | Size | Type | Description |
|--------|------|------|-------------|
| `0x000000` | 32,400 | Raw | **Popup Icons** (9 icons, 60×60 each) |
| `0x008F2E` | ~5.7 KB | RLE | **Speech Balloon Set 0** (4 frames) |
| `0x00A57A` | ~38 KB | RLE | **Speech Balloon Set 1** (4 frames) |

### Popup Icons

**Location:** Offset `0x000000`
**Format:** Raw indexed bitmap (no compression)
**Dimensions:** 60×60 pixels per icon
**Count:** 9 icons
**Total Size:** 32,400 bytes (9 × 60 × 60)

**Layout:**
```
Icon 0: bytes 0-3599      (Open action icon)
Icon 1: bytes 3600-7199   (Close action icon)
Icon 2: bytes 7200-10799  (Push action icon)
Icon 3: bytes 10800-14399 (Pull action icon)
Icon 4: bytes 14400-17999 (Pick up action icon)
Icon 5: bytes 18000-21599 (Talk action icon)
Icon 6: bytes 21600-25199 (Use action icon)
Icon 7: bytes 25200-28799 (Look action icon)
Icon 8: bytes 28800-32399 (Walk action icon)
```

### Speech Balloons

**Dimensions:** 247×112 pixels per frame
**Frames per Set:** 4 frames (animation)
**Format:** RLE compressed with BUDA markers

**Set 0:**
- **Offset:** `0x008F2E`
- **Compressed Size:** ~5,700 bytes
- **Purpose:** Character speech balloon (animation)

**Set 1:**
- **Offset:** `0x00A57A`
- **Compressed Size:** ~38,000 bytes
- **Purpose:** Alternative speech balloon or narrator text

**Frame Layout (after decompression):**
```
Frame 0: 0-27663        (247×112 = 27,664 bytes)
Frame 1: 27664-55327
Frame 2: 55328-82991
Frame 3: 82992-110655
```

---

## ALFRED.7 - Sprites and Cursors

**Size:** 3,637,248 bytes (~3.5 MB)
**Purpose:** Additional sprite data and mouse cursor graphics
**Format:** Mixed raw and RLE-compressed data

### Mouse Cursors

**Dimensions:** 16×18 pixels each
**Format:** Raw indexed bitmap
**Transparent Color:** Index 255 (0xFF)
**Count:** 5 cursors

#### Cursor Locations

| Cursor | Offset | Decimal | Variable Name | Usage |
|--------|--------|---------|---------------|-------|
| **1** | `0x0FDCDD` | 1,039,581 | `cursor_hotspot_ptr` | Hovering over interactive objects/sprites |
| **2** | `0x0FDDFD` | 1,039,869 | `cursor_default_ptr` | Default pointer (menus, inventory, verb panel) |
| **3** | `0x0FDF1D` | 1,040,157 | `cursor_exit_ptr` | Hovering over room exits/doorways |
| **4** | `0x0FE33D` | 1,041,213 | `cursor_animation_ptr` | Hovering over special animations |
| **5** | `0x367EF0` | 3,571,440 | `cursor_combination_ptr` | Exit + hotspot overlap |

**Data Format:**
```
288 bytes = 16 width × 18 height
Each byte = palette index (0-255)
Index 255 = transparent pixel
```

### Sprite Data Sections

ALFRED.7 contains additional sprite frames organized in BUDA-marked sections. These are typically accessed by the game engine based on room number and animation needs.

**Organization:**
- Multiple BUDA markers throughout file
- Each section contains RLE-compressed sprite data
- Indexed by room number or sprite ID in game logic

---

## ALFRED.9 - Fonts and Remap Tables

**Size:** 149,772 bytes (~146 KB)
**Purpose:** Bitmap fonts and color remap tables for sprite recoloring
**Format:** Mixed binary data

### Small Font (8×8)

**Location:** Offset `0x8F32`
**Size:** 2,048 bytes (0x800)
**Dimensions:** 8×8 pixels per character
**Characters:** 256 (full ASCII + extended)
**Format:** 1-bit bitmap (monochrome)

**Structure:**
```c
struct SmallFont {
    u8 chars[256][8];  // 256 characters, 8 bytes each
};
```

**Character Data:**
```
Each character = 8 bytes (one per scanline)
Each byte = 8 pixels (bit 7 = leftmost pixel)

Example: Letter 'A' (ASCII 65)
  Byte 0: 00111100  (  ####  )
  Byte 1: 01100110  ( ##  ## )
  Byte 2: 11000011  (##    ##)
  Byte 3: 11111111  (########)
  Byte 4: 11000011  (##    ##)
  Byte 5: 11000011  (##    ##)
  Byte 6: 11000011  (##    ##)
  Byte 7: 00000000  (        )
```

### Large Font (12×24)

**Location:** Offset `0x7DC8`
**Size:** 4,800 bytes (0x12C0)
**Dimensions:** 12×24 pixels per character
**Characters:** 96 (ASCII 32-127, printable only)
**Format:** 1-bit bitmap (monochrome)

**Structure:**
```c
struct LargeFont {
    u8 chars[96][48];  // 96 characters, 48 bytes each (0x30)
};
```

**Character Data:**
```
Each character = 48 bytes (24 rows × 2 bytes)
Each row = 2 bytes (16 bits), upper 12 bits used

Row encoding:
  Byte 0: xxxxxxxx (bits 15-8)
  Byte 1: xxxx0000 (bits 7-4 used, bits 3-0 unused)

Bit 15 = leftmost pixel
Bit 4 = rightmost pixel (12 pixels total)
```

**Character Index:**
```
Character 0 = ASCII 32 (space)
Character 1 = ASCII 33 (!)
...
Character 95 = ASCII 127 (~)
```

### Color Remap Tables

**Purpose:** Dynamic sprite recoloring for different character states, lighting, etc.
**Location:** Various offsets (room-specific)
**Format:** 256-byte lookup tables

**Structure:**
```c
struct RemapTable {
    u8 color_map[256];  // Input color → Output color
};
```

**Usage:**
```python
# Apply remap to sprite
for pixel in sprite_data:
    remapped_pixel = remap_table[pixel]
```

**Common Uses:**
- Character palette swaps (different NPCs)
- Lighting effects (dark rooms, shadows)
- Special visual effects
- Item color variations

---

## Common Structures

### BUDA Marker

**Signature:** `0x42 0x55 0x44 0x41` (ASCII "BUDA")
**Purpose:** Section marker and compression identifier
**Usage:** Appears before RLE-compressed data blocks

**Format:**
```
[0x42 0x55 0x44 0x41] [compressed_data_follows]
 B    U    D    A
```

**Detection:**
```python
def find_buda_markers(data):
    markers = []
    for i in range(len(data) - 3):
        if data[i:i+4] == b'BUDA':
            markers.append(i)
    return markers
```

### Screen Dimensions

**Resolution:** 640×400 pixels
**Color Depth:** 8-bit indexed (256 colors)
**Aspect Ratio:** 16:10
**Video Mode:** VGA Mode 13h-derived

### Coordinate System

```
Origin (0,0) = Top-left corner
X-axis: Left to right (0-639)
Y-axis: Top to bottom (0-399)

┌───────────────────┐  (639, 0)
│  (0,0)            │
│                   │
│                   │
│                   │
│                   │
└───────────────────┘  (639, 399)
```

### Color Index Special Values

| Index | Usage | Notes |
|-------|-------|-------|
| `0x00` | Black | Often used for outlines |
| `0xFF` | Transparent | Used in sprites, cursors |
| `0xFE` | Special marker | Used in some text encoding |
| Other | Palette color | 0-254 reference palette |

---

## Extraction Tools

The following Python scripts can extract data from these files:

### ALFRED.1 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `extract_backgrounds.py` | Background images with palettes | PNG files (640×400) |
| `extract_animations.py` | All sprite animations | PNG sprite sheets |
| `extract_sprite_data.py` | Sprite metadata, hotspot flags | JSON, Python, text |
| `extract_room_data.py` | Hotspots, walkboxes, exits | JSON, Python, text |
| `extract_hotspots.py` | Static hotspot rectangles | Text files |
| `extract_walkboxes.py` | Walkable area definitions | JSON, Python |
| `extract_exits.py` | Room connections/transitions | JSON, Python, text |

### ALFRED.4 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `extract_balloons.py` | Popup icons and speech balloons | PNG files (with palette) |
| `extract_popup.py` | UI popup graphics | PNG files |

### ALFRED.7 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `extract_cursors.py` | Mouse cursor sprites | PNG files (16×18) |
| `extract_alfred7_bruteforce.py` | Additional sprite data | Various formats |

### ALFRED.9 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `extract_font.py` | Bitmap fonts (8×8 and 12×24) | PNG font sheets |
| `extract_large_font.py` | Large dialog font | PNG font sheet |

---

## Reference Information

### Game Information

**Title:** Alfred Pelrock
**Release Year:** 1997
**Developer:** Unknown
**Platform:** MS-DOS
**Genre:** Point-and-click adventure
**Engine:** Custom (reverse-engineered)
**Executable:** JUEGO.EXE

### File Sizes

| File | Size (bytes) | Size (KB) | Size (MB) |
|------|-------------|-----------|-----------|
| ALFRED.1 | 12,915,352 | 12,613 | 12.32 |
| ALFRED.4 | 43,866 | 42.8 | 0.04 |
| ALFRED.7 | 3,637,248 | 3,552 | 3.47 |
| ALFRED.9 | 149,772 | 146.3 | 0.14 |

### Technical Details

**Binary Format:** Little-endian (Intel x86)
**Text Encoding:** Latin-1 (ISO-8859-1) or DOS Code Page 437
**Graphics Format:** Indexed color (8-bit palette)
**Compression:** Custom RLE (Run-Length Encoding)
**Resolution:** 640×400 (VGA)

### Reverse Engineering Tools Used

- **Ghidra:** Code analysis and decompilation of JUEGO.EXE
- **ImHex:** Binary data structure visualization (with custom patterns)
- **Python 3:** Extraction scripts and data processing
- **PIL/Pillow:** Image manipulation and PNG export

---

## Credits

Documentation compiled through reverse engineering analysis using:
- Ghidra SRE framework for executable analysis
- ImHex pattern language for binary structure definition
- Python extraction scripts for data validation
- Manual hex editing and pattern recognition

---

## Version History

**Version 1.0** - Initial comprehensive documentation
**Date:** November 12, 2025
**Author:** Reverse engineering analysis of Alfred Pelrock (1997)

---

## Notes

1. **Hotspot System Discovery:** The sprite hotspot system uses byte offsets +33 (sprite_type), +34 (action_flags), and +38 (is_hotspot) to determine interactivity. Confirmed through Ghidra analysis of `check_mouse_on_sprites_and_hotspots()` function.

2. **Text Indexing:** Text descriptions are NOT stored in sprite structures. They're indexed implicitly by the position in the combined list of selectable sprites and static hotspots. This was discovered through analysis of the `load_room_data()` function's text pointer table building mechanism.

3. **BUDA Markers:** The "BUDA" signature appears throughout the data files as a compression marker. Origin of the name is unknown but likely related to the game's development environment or internal tools.

4. **Palette Sharing:** ALFRED.4 uses the palette from ALFRED.1 Room 0, Pair 11. This indicates a centralized palette management system for UI consistency.

5. **Coordinate Validation:** The game validates coordinates against screen bounds (640×400) when loading exits and hotspots, suggesting runtime safety checks in the engine.

---

*End of Documentation*
