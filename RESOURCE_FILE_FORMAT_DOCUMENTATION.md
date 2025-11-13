# Alfred Pelrock (1997) - Resource File Format Documentation

Complete documentation of all resource file formats for Alfred Pelrock, a DOS point-and-click adventure game developed in 1997.

## Table of Contents

1. [File Overview](#file-overview)
2. [ALFRED.1 - Main Game Data](#alfred1---main-game-data)
3. [ALFRED.2 - Character Talking Animations](#alfred2---character-talking-animations)
4. [ALFRED.3 - Character Movement Animations](#alfred3---character-movement-animations)
5. [ALFRED.4 - UI Graphics](#alfred4---ui-graphics)
6. [ALFRED.5 - Shadow Layers](#alfred5---shadow-layers)
7. [ALFRED.6 - Overlay Graphics (Pegatinas)](#alfred6---overlay-graphics-pegatinas)
8. [ALFRED.7 - Sprites and Cursors](#alfred7---sprites-and-cursors)
9. [ALFRED.9 - Fonts and Remap Tables](#alfred9---fonts-and-remap-tables)
10. [Common Structures](#common-structures)

---

## File Overview

| File | Size | Purpose | Primary Contents |
|------|------|---------|------------------|
| **ALFRED.1** | ~12.9 MB | Main game data | Backgrounds, room data, sprites, animations, palettes, text |
| **ALFRED.2** | ~2.1 MB | Character animations | Talking animations, character sprites (RLE compressed) |
| **ALFRED.3** | ~311 KB | Character animations | Character movement animations (walking, actions) |
| **ALFRED.4** | ~43 KB | UI graphics | Popup icons, speech balloons |
| **ALFRED.5** | ~1.7 MB | Shadow layers | Character shadow sprites for all rooms |
| **ALFRED.6** | ~700 KB | Overlay graphics | "Pegatinas" (stickers/overlays) for room decorations |
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
| **10** | varies | varies | **Room data** | varies | Hotspots, walkboxes, exits, sprites |
| **11** | varies | 0x300 | **Palette** | Raw | 256-color VGA palette (768 bytes) |
| **12** | varies | varies | **Text data** | Special | Descriptions and conversations with control codes |

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

#### Text System (Pair 10 - Legacy, see Pair 12 for actual text)

**NOTE:** Text data is actually stored in **Pair 12**, not Pair 10. Pair 10 only contains sprite/hotspot metadata.

**Text Pointer Table:**
- **Location:** Offset `0x3DA` in Pair 10
- **Format:** Array of `u32` absolute file pointers pointing to **Pair 12** data
- **Building:** Scanned dynamically by searching for control code markers in Pair 12

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

### Pair 12: Text Data (Descriptions and Conversations)

**Purpose:** All text data for room including descriptions and conversations
**Format:** ASCII text with embedded control codes
**Structure:** Two sections - Descriptions followed by Conversations
**Encoding:** Latin-1 or DOS Code Page 437

#### Section 1: Item/Hotspot Descriptions

**Format:**
```
FF [ITEM_ID] 08 0D [INDEX] 00 [TEXT...] FD
```

**Structure Breakdown:**
- `FF` (0xFF): Start of description marker
- `ITEM_ID`: Hotspot/sprite identifier (0x21, 0x22, 0x23, etc.)
- `08 0D`: Standard separator bytes
- `INDEX`: Sequential text index (0x00, 0x01, 0x02...)
- `00`: Null byte separator
- `[TEXT...]`: ASCII text content
- `FD` (0xFD): End of description marker

**Example (Room 2, Description 0):**
```
Offset 0xB204A:
FF 21 08 0D 00 00  4E 6F 20 65 73 74 7B ...
|  |  |  |  |  |   |  |  |  |  |  |
|  |  |  |  |  |   N  o     e  s  t  {
|  |  |  |  |  |
|  |  |  |  |  +--- Null separator
|  |  |  |  +------ Text index: 0x00
|  |  |  +--------- 0x0D separator
|  |  +------------ 0x08 separator
|  +--------------- Item ID: 0x21 (ASCII '!')
+------------------ Description start marker
```

#### Section 2: Conversations

**Format:** Complex dialogue system with speaker identification and line management.

**Basic Structure:**
```
[CHARACTER_PREFIX] [TEXT...] FD [SPEAKER_CHANGE] [SPEAKER_ID] 08 [SEPARATOR] [INDEX] 00 [NEXT_TEXT...]
```

**Control Codes:**

| Code | Hex | Description | Format |
|------|-----|-------------|--------|
| **Line Terminators** |
| `FD` | 0xFD | End of line/dialogue segment | Standalone byte |
| | | |
| **Speaker Control** |
| `FC` | 0xFC | Speaker change (protagonist) | `FD FC [SPEAKER] 08 20 [INDEX] 00` |
| `FB` | 0xFB | Continue same speaker (NPC) | `FD FB [SPEAKER] 08 0D [INDEX] 00` |
| `F1` | 0xF1 | Special speaker marker | `FD F1 [SPEAKER] 08 0D [INDEX] 00` |
| | | |
| **Formatting** |
| `F4` | 0xF4 | Paragraph break/end | Often followed by FB/FC/F1 |
| `F8` | 0xF8 | Special formatting | `F8 [PARAM1] [PARAM2]` (skip 3 bytes total) |
| `F7` | 0xF7 | Unknown formatting | Appears with F4 |
| `F5` | 0xF5 | End of conversation | Usually at very end |
| | | |
| **Character Indicators** |
| `82` | 0x82 | Character voice/style marker | Appears before some dialogue |
| `83` | 0x83 | Character voice/style marker | Appears before some dialogue |
| | | |
| **Special Characters** |
| `7F` | 0x7F | Accented 'ú' (u-acute) | Spanish text encoding |
| `80` | 0x80 | Accented 'ñ' (n-tilde) | Spanish text encoding |

**Speaker ID Values:**
- `0x41` (ASCII 'A'): Alfred (protagonist) - uses 0x20 (space) separator
- `0x01-0x09`: Other character IDs - use 0x0D separator
- `0x0A-0x1F`: Extended character range

**Separator Differences:**
- **0x20 (space)**: Used after `FC` for protagonist (Alfred)
- **0x0D (carriage return)**: Used after `FB`/`F1` for NPCs

**Example (Room 2, Conversation Start):**
```
Offset 0xB21E6:
83 20 54 65 20 61 70 65 63 65 ...
|  |  |  |  |  |  |  |  |  |
|  |  T  e     a  p  e  c  e
|  +--- Space separator
+------ Character prefix 0x83
```

**Speaker Change Example:**
```
FD FC 41 08 20 0C 00  43 6F 6D 70 ...
|  |  |  |  |  |  |   |  |  |  |
|  |  |  |  |  |  |   C  o  m  p
|  |  |  |  |  |  +--- Null separator
|  |  |  |  |  +------ Text index 0x0C
|  |  |  |  +--------- Space separator (0x20)
|  |  |  +------------ 0x08 separator
|  |  +--------------- Speaker: 0x41 ('A' = Alfred)
|  +------------------ Speaker change marker
+---------------------- Line end

Result: Switch to Alfred (protagonist), display text index 12
```

**Continue Same Speaker Example:**
```
FD FB 02 08 0D 0D 00  83 20 4E 6F ...
|  |  |  |  |  |  |   |  |  |  |
|  |  |  |  |  |  |   |  |  N  o
|  |  |  |  |  |  +--- Null separator
|  |  |  |  |  +------ Text index 0x0D
|  |  |  |  +--------- 0x0D separator (NPC indicator)
|  |  |  +------------ 0x08 separator
|  |  +--------------- Speaker: 0x02 (NPC character 2)
|  +------------------ Continue same speaker
+---------------------- Line end

Result: Continue with NPC #2, display text index 13
```

**Paragraph Break Example:**
```
F4 FB 05 08 0D 23 00  45 73 20 ...
|  |  |  |  |  |  |   |  |  |
|  |  |  |  |  |  |   E  s  (space)
|  |  |  |  |  |  +--- Null separator
|  |  |  |  |  +------ Text index 0x23
|  |  |  |  +--------- 0x0D separator
|  |  |  +------------ 0x08 separator
|  |  +--------------- Speaker: 0x05
|  +------------------ Continue speaker marker
+---------------------- Paragraph end

Result: End paragraph, then continue with NPC #5
```

#### Text Data Location (Room 2 Example)

| Section | Start Offset | End Offset | Size | Content |
|---------|--------------|------------|------|---------|
| **Descriptions** | 0xB204A | 0xB21E4 | 410 bytes | 10 hotspot/sprite descriptions |
| **Conversations** | 0xB21E6 | 0xB3078 | 3,730 bytes | Multi-speaker dialogue tree |

**Note:** These are Pair 12 offsets in ALFRED.1. Access via room directory → Room 2 → Pair 12.

#### Conversation Tree Structure

**Important:** Conversations use an **implicit tree structure** without explicit choice markers.

**Tree Navigation System:**

1. **No Explicit Choice Markers**
   - There is NO special control code to indicate "present choices here"
   - Choices are determined by the game engine based on dialogue line structure

2. **Index-Based Branching**
   - Each dialogue line has an INDEX byte (in `08 0D [INDEX] 00` pattern)
   - Indices are NOT always sequential
   - **Gap in indices = branching point**

3. **Choice Identification**
   - When multiple PLAYER lines (speaker 0x41) exist with non-sequential indices
   - Example: Lines with indices 0x18, 0x1A, 0x1C = three player choices
   - The engine presents all player lines in the current branch as selectable options

4. **Dialogue Flow Example (Room 2):**

```
Index 0x0A: NPC says "Te apecete pasar un buen rato, guapo ?"
            ↓
Index 0x0B: PLAYER choice 1: "No se, Cuanto cobras ?"
            ↓
Index 0x0C: NPC responds: "Completo, 25000"
            ↓
Index 0x0D: PLAYER responds: "No me puedes hacer una tarifa especial?..."
            ↓
Index 0x0E: NPC responds: "Bueno ... Si prescindimos de la lencería..."
            ↓
Index 0x0F: PLAYER choice 1: "Todavía es muy caro para mi..."
Index 0x10: PLAYER choice 2: "Yo no uso ese tipo de ropa..."
            ↓ (player selects one)
Index 0x10: (branch continues from choice)
```

5. **Choice Presentation Logic**
   - Game engine scans forward from current position
   - Collects all PLAYER (0x41) lines until hitting NPC response
   - Non-sequential indices indicate alternative dialogue branches
   - Player selection jumps to corresponding index and continues

6. **Line Continuation (Long Text)**
   - Same speaker can have multiple consecutive entries
   - Uses `FD FB [SPEAKER]` for same speaker continuation
   - OR text flows directly without `FD` between parts
   - Example: Long NPC monologues split across multiple entries with same speaker ID

**Display Timing and Formatting:**

1. **Text Display Duration**
   - Calculated based on character count
   - Estimated formula: `display_time = (text_length / chars_per_second) + base_delay`
   - Typical reading speed: 20-30 characters per second
   - Base delay: ~1-2 seconds minimum

2. **Line Wrapping**
   - Maximum line width: **47 characters** (0x2F in Ghidra code)
   - Wraps at word boundaries (space character)
   - Breaks on control codes: `FD`, `F4`, `F8`

3. **Screen Layout**
   - Maximum lines per screen: **4-5 lines**
   - Based on DAT_0005856b counter in `display_dialog_text()` function
   - When screen fills, displays "continue" indicator (0xF6 code)
   - Player must click to see next screen

4. **Paragraph Breaks**
   - `F4` code forces new paragraph/screen
   - Often followed by speaker continuation: `F4 FB [SPEAKER]`
   - Clears previous text before showing next section

**Tree Structure Summary:**

```
Conversation Structure:
├─ Opening line (NPC)
├─ Branch 1: Player choice A
│  ├─ NPC response to A
│  ├─ Sub-branch 1.1: Player choice A1
│  │  └─ NPC response to A1
│  └─ Sub-branch 1.2: Player choice A2
│     └─ NPC response to A2
└─ Branch 2: Player choice B
   └─ NPC response to B
      └─ (continues...)

Implementation:
- All dialogue lines stored sequentially in Pair 12
- INDEX byte determines position in tree
- Engine tracks current index
- Presents all player lines with valid indices as choices
- Selection advances to chosen branch
```

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

## ALFRED.2 - Character Talking Animations

**Size:** ~2.1 MB (approximate)
**Purpose:** Character talking/dialogue animations with lip-sync frames
**Palette:** Uses room-specific palettes from ALFRED.1
**Compression:** RLE with BUDA markers

### File Structure

ALFRED.2 stores character talking animations organized in **55-byte directory entries**.

#### Directory Entry Structure (55 bytes / 0x37)

```c
struct AnimEntry {
    // First animation (e.g., mouth movements)
    u16 offset_anim_a;      // +0x00-0x01: File offset for animation A (LE)
    u8  padding1[7];        // +0x02-0x08: Padding/unknown
    u8  width_a;            // +0x09: Width of animation A frames
    u8  height_a;           // +0x0A: Height of animation A frames
    u8  padding2[2];        // +0x0B-0x0C: Padding/unknown
    u8  num_frames_a;       // +0x0D: Number of frames in animation A
    u8  padding3[7];        // +0x0E-0x14: Padding/unknown

    // Second animation (e.g., eye blinks, expressions)
    u16 offset_anim_b;      // +0x15-0x16: File offset for animation B (LE)
    u8  padding4[7];        // +0x17-0x1D: Padding/unknown
    u8  width_b;            // +0x1E: Width of animation B frames
    u8  height_b;           // +0x1F: Height of animation B frames
    u8  padding5[2];        // +0x20-0x21: Padding/unknown
    u8  num_frames_b;       // +0x22: Number of frames in animation B
    u8  padding6[19];       // +0x23-0x35: Padding/unknown
    u8  terminator;         // +0x36: Entry terminator (usually 0x00)
};
```

### Data Organization

**Directory Phase:**
- Iterate through 55-byte entries from file start
- Skip entries where `offset_anim_a == 0` (empty slots)
- Each valid entry points to two animation sets (A and B)

**Animation Data:**
- Located at offsets specified in directory entries
- RLE-compressed with BUDA markers
- Each animation contains N frames of W×H pixels
- Frames stored sequentially after decompression

### Decompression Algorithm

```python
def decompress_rle(data, start_offset):
    """Decompress RLE data until BUDA marker"""
    output = bytearray()
    offset = start_offset

    while offset < len(data):
        # Check for BUDA marker (end of compressed section)
        if data[offset:offset+4] == b'BUDA':
            break

        # Read RLE pair
        count = data[offset]
        color = data[offset + 1]
        output.extend([color] * count)
        offset += 2

    return output
```

### Frame Extraction

**Animation A Layout:**
```
Total pixels = width_a × height_a × num_frames_a
Frame 0: pixels[0 : width_a × height_a]
Frame 1: pixels[width_a × height_a : 2 × width_a × height_a]
...
Frame N: pixels[(N-1) × width_a × height_a : N × width_a × height_a]
```

**Animation B Layout:**
```
Starts at offset: width_a × height_a × num_frames_a
Total pixels = width_b × height_b × num_frames_b
Frames indexed same as Animation A
```

### Usage Notes

- **Animation A:** Typically mouth/lip-sync movements
- **Animation B:** Typically eye blinks, facial expressions, or secondary motions
- **Palette Index:** Entry index ÷ 55 determines which ALFRED.1 room palette to use
- **Naming Convention:** `anim_{entry_index}_a.png` and `anim_{entry_index}_b.png`

---

## ALFRED.3 - Character Movement Animations

**Size:** ~311 KB (approximate)
**Purpose:** Character walking animations and movement cycles
**Palette:** Uses default palette from ALFRED.1
**Compression:** RLE with BUDA markers

### File Structure

ALFRED.3 contains sequential animation sets with different dimensions and frame counts. No directory structure—animations are stored one after another.

#### Animation Sets

| Set | Width | Height | Frames | Total Pixels | Description |
|-----|-------|--------|--------|--------------|-------------|
| **0** | 51 | 102 | 60 | 312,120 | Main character walking cycle (all directions) |
| **1** | 130 | 55 | 18 | 128,700 | Wide character animation (possibly outro/cutscene) |
| **2** | 51 | 100 | 25 | 127,500 | Character action animation |
| **3** | 51 | 100 | 10 | 51,000 | Short character action |
| **4-12** | 51 | 100 | 1 | 5,100 each | Static poses or single-frame actions |

**Hardcoded Dimensions:**
```c
int nFrames[] = {60, 18, 25, 10, 1, 1, 1, 1, 1, 1, 1, 1, 1};
int dimensions[10][2] = {
    {51, 102},  // Set 0
    {130, 55},  // Set 1
    {51, 100},  // Sets 2-9
    // ... remaining sets all {51, 100}
};
```

### Data Organization

**Single Compressed Block:**
- Entire file is one RLE-compressed data stream
- Decompression continues until BUDA marker or EOF
- Frame boundaries calculated from dimensions and frame counts

**Offset Calculation:**
```python
offset = 0
for set_index in range(num_sets):
    if set_index > 0:
        prev_frames = nFrames[set_index - 1]
        prev_width = dimensions[set_index - 1][0]
        prev_height = dimensions[set_index - 1][1]
        offset += prev_frames * prev_width * prev_height

    # Extract this animation set starting at 'offset'
```

### Frame Layout

Each animation set is a horizontal sprite sheet:

```
Set 0 (60 frames, 51×102):
┌─────┬─────┬─────┬─────┬ ... ─────┐
│Frame│Frame│Frame│Frame│ ... │Frame│
│  0  │  1  │  2  │  3  │ ... │ 59  │
│51×102│51×102│51×102│51×102│...│51×102│
└─────┴─────┴─────┴─────┴ ... ─────┘
Total width: 51 × 60 = 3,060 pixels
Total height: 102 pixels
```

### Extraction Process

1. **Decompress entire file:** RLE → raw pixel buffer
2. **For each animation set:**
   - Calculate byte offset from previous sets
   - Extract width × height × frames pixels
   - Arrange as horizontal sprite sheet
3. **Export as PNG:** With palette from ALFRED.1

### Usage Notes

- **Set 0 (60 frames):** Complete walking cycle with 8 directions + transitions
- **Set 1 (18 frames):** Special cutscene or large character animation
- **Sets 2-3:** Action animations (picking up objects, interacting)
- **Sets 4-12:** Static poses or idle states

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

## ALFRED.5 - Shadow Layers

**Size:** ~1.7 MB (approximate)
**Purpose:** Character shadow sprites for all 55 rooms
**Palette:** Uses room-specific palettes from ALFRED.1
**Compression:** RLE with BUDA markers

### File Structure

ALFRED.5 contains a directory of shadow sprites, one for each of the 55 rooms in the game.

#### Directory Structure (6 bytes per entry)

```c
struct ShadowEntry {
    u32 offset;     // +0x00-0x02: File offset (24-bit LE, 3 bytes)
    u8  padding[3]; // +0x03-0x05: Padding/unknown
};
```

**Total Entries:** 55 (one per room)
**Directory Size:** 330 bytes (55 × 6)

### Shadow Data Format

Each shadow is a full-screen (640×400) overlay with RLE compression.

#### Compressed Data Structure

```
[offset]:        Start of RLE compressed data
    [count, color] pairs...
    [count, color] pairs...
    ...
[offset+N]:      BUDA marker (0x42 0x55 0x44 0x41)
```

**Decompression:**
```python
def extract_shadow(data, entry_index):
    # Read directory entry
    entry_offset = entry_index * 6
    shadow_offset = (data[entry_offset] |
                     (data[entry_offset + 1] << 8) |
                     (data[entry_offset + 2] << 16))

    # Decompress RLE until BUDA marker
    pixels = bytearray()
    offset = shadow_offset

    while offset < len(data):
        if data[offset:offset+4] == b'BUDA':
            break

        count = data[offset]
        color = data[offset + 1]
        pixels.extend([color] * count)
        offset += 2

    return pixels  # Should be 640 × 400 = 256,000 bytes
```

### Usage Notes

- **Dimensions:** Always 640×400 (full screen)
- **Purpose:** Dynamic shadow overlay for character position
- **Blending:** Likely uses palette darkening or alpha compositing
- **Room Mapping:** Entry index directly corresponds to room number (0-54)
- **Palette:** Uses the same palette as corresponding ALFRED.1 room

### Visual Properties

- Shadows are typically dark/semi-transparent colors (low palette indices)
- Used to give depth perception to character in environment
- May include ambient occlusion or environmental shadows

---

## ALFRED.6 - Overlay Graphics (Pegatinas)

**Size:** ~700 KB (approximate)
**Purpose:** "Pegatinas" (stickers/overlays) - decorative graphics layered on rooms
**Palette:** Uses room-specific palettes based on lookup table
**Compression:** Uncompressed raw bitmaps

### File Structure

ALFRED.6 contains variable-sized overlay graphics stored sequentially with metadata headers.

#### Entry Header (6 bytes)

```c
struct PegatinaHeader {
    u16 screen_x;   // +0x00-0x01: X position on screen (LE)
    u16 screen_y;   // +0x02-0x03: Y position on screen (LE)
    u8  width;      // +0x04: Width in pixels
    u8  height;     // +0x05: Height in pixels
    // Immediately followed by pixel data (width × height bytes)
};
```

### Data Organization

**Sequential Storage:**
```
[Entry 0 Header: 6 bytes][Entry 0 Pixels: w0×h0 bytes][Separator: 0xBF bytes]
[Entry 1 Header: 6 bytes][Entry 1 Pixels: w1×h1 bytes][Separator: 0xBF bytes]
...
```

**Entry Separator:**
- One or more `0xBF` bytes between entries
- Skip all consecutive `0xBF` bytes to find next entry
- Entries with `width == 0` or `height == 0` are skipped

**Special Offsets:**
Some entries have hardcoded offsets (non-sequential):
```c
if (entry == 37) offset = 0x1B8C4;
if (entry == 67) offset = 0x3F813;
if (entry == 68) offset = 0x4115D;
if (entry == 88) offset = 0x58969;
```

### Palette Mapping Table

**Location:** Hardcoded in `alfred6.c`
**Size:** 140 entries mapping pegatina index → palette number

```c
int tablapaletas[140] = {
    0,0,0,0,0,0,0,       // Entries 0-6   → Palette 0
    2,2,                 // Entries 7-8   → Palette 2
    3,3,3,3,3,3,3,3,     // Entries 9-16  → Palette 3
    4,4,4,4,4,           // Entries 17-21 → Palette 4
    5,5,                 // Entries 22-23 → Palette 5
    7,                   // Entry 24      → Palette 7
    8,8,                 // Entries 25-26 → Palette 8
    9,9,9,9,9,           // Entries 27-31 → Palette 9
    12,12,               // Entries 32-33 → Palette 12
    13,13,13,            // Entries 34-36 → Palette 13
    12,                  // Entry 37      → Palette 12
    15,15,15,15,15,15,15,15,15,15,15,15,  // Entries 38-49 → Palette 15
    16,16,               // Entries 50-51 → Palette 16
    17,17,               // Entries 52-53 → Palette 17
    19,19,19,19,19,      // Entries 54-58 → Palette 19
    // ... more entries
};
```

**Palette Selection:**
```python
palette_index = tablapaletas[pegatina_index]
palette_room = palette_index // 55  # Room number
palette_pair = (palette_room * 13) + 11  # Pair 11 = palette
```

### Extraction Process

1. **Read header:** 6 bytes (x, y, width, height)
2. **Skip if empty:** `width == 0` or `height == 0`
3. **Read pixels:** `width × height` bytes (raw indexed bitmap)
4. **Select palette:** Use `tablapaletas` lookup
5. **Output files:**
   - `pegatina{NN}.png` - Image with palette
   - `pegatina{NN}.txt` - Metadata (x, y, width, height)

### Usage Notes

- **Purpose:** Decorative overlays, furniture, objects on room backgrounds
- **Layering:** Applied after background, before character sprites
- **Positioning:** Absolute screen coordinates (x, y)
- **Variable Size:** Each pegatina has individual dimensions
- **Palette Context:** Different pegatinas use different room palettes for proper color matching

### Metadata Format

**Text File (`.txt`):**
```
<screen_x>
<screen_y>
<width>
<height>
```

**Example (`pegatina00.txt`):**
```
120
85
64
48
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

### ALFRED.2 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `alfred2.c` | Character talking animations (A/B sets) | PNG sprite sheets |

### ALFRED.3 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `alfred3.c` | Character movement/walking animations | PNG sprite sheets |

### ALFRED.4 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `extract_balloons.py` | Popup icons and speech balloons | PNG files (with palette) |
| `extract_popup.py` | UI popup graphics | PNG files |
| `alfred4.c` | UI graphics (alternate implementation) | PNG files |

### ALFRED.5 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `alfred5.c` | Character shadow layers for all rooms | PNG files (640×400) |

### ALFRED.6 Extractors

| Script | Extracts | Output |
|--------|----------|--------|
| `alfred6.c` | Pegatinas (overlay graphics) | PNG + TXT metadata |

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
| ALFRED.2 | ~2,100,000 | ~2,050 | ~2.00 |
| ALFRED.3 | ~311,000 | ~304 | ~0.30 |
| ALFRED.4 | 43,866 | 42.8 | 0.04 |
| ALFRED.5 | ~1,700,000 | ~1,660 | ~1.62 |
| ALFRED.6 | ~700,000 | ~683 | ~0.67 |
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
**Version 1.1** - Added ALFRED.2, 3, 5, 6 documentation from C extractors
**Version 1.2** - Decoded Pair 12 text system with complete control code documentation
**Date:** November 12, 2025
**Author:** Reverse engineering analysis of Alfred Pelrock (1997)

---

## Notes

1. **Hotspot System Discovery:** The sprite hotspot system uses byte offsets +33 (sprite_type), +34 (action_flags), and +38 (is_hotspot) to determine interactivity. Confirmed through Ghidra analysis of `check_mouse_on_sprites_and_hotspots()` function.

2. **Text Storage Location:** Text data is stored in **Pair 12**, not Pair 10. Pair 10 contains only metadata (sprites, hotspots, walkboxes, exits) and a pointer table at offset 0x3DA that references the actual text in Pair 12. This was confirmed through pattern analysis of control codes and cross-referencing with Ghidra's `display_dialog_text()` function.

3. **Text Control Codes:** The text system uses a sophisticated set of control codes for dialogue management:
   - `0xFD`: Line terminator
   - `0xFC`: Speaker change to protagonist (uses 0x20 separator)
   - `0xFB`: Continue same NPC speaker (uses 0x0D separator)
   - `0xF4`: Paragraph break
   - `0xF8`: Special formatting (skip 3 bytes)
   - `0x82/0x83`: Character voice/style indicators
   These codes control speaker transitions, text formatting, and animation selection during conversations.

4. **Speaker Identification:** In conversations, speaker 0x41 ('A') represents Alfred the protagonist and uses a space (0x20) separator, while NPCs use IDs 0x01-0x1F and a carriage return (0x0D) separator. This difference allows the engine to distinguish between player dialogue and NPC responses.

5. **Text Indexing:** Text descriptions are indexed implicitly by position in the combined list of `[selectable_sprites] + [static_hotspots]`. Each entry uses the format `FF [ID] 08 0D [INDEX] 00 [TEXT...] FD` where INDEX increments sequentially.

6. **BUDA Markers:** The "BUDA" signature appears throughout the data files as a compression marker. Origin of the name is unknown but likely related to the game's development environment or internal tools.

7. **Palette Sharing:** ALFRED.4 uses the palette from ALFRED.1 Room 0, Pair 11. This indicates a centralized palette management system for UI consistency.

8. **Coordinate Validation:** The game validates coordinates against screen bounds (640×400) when loading exits and hotspots, suggesting runtime safety checks in the engine.

---

*End of Documentation*
