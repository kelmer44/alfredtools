# Shadow System Documentation

## Overview

The game uses a sophisticated shadow/shading system to add depth to character sprites. When the character is positioned in shadowed areas of a room, their sprite colors are dynamically remapped to darker equivalents using a palette-based shading system.

## Data Sources

### 1. ALFRED.5 - Shadow Maps

**File Structure:**
- Size: ~1.7 MB
- Contains 55 shadow maps (one per room)
- Each map is 640×400 pixels (full screen size)
- Compressed with RLE encoding

**Directory Structure:**
```c
struct ShadowEntry {
    u32 offset;     // 24-bit little-endian (3 bytes)
    u8  padding[3]; // Unknown/padding
};
```

**Shadow Map Properties:**
- **Dimensions:** 640×400 (matches screen resolution)
- **Format:** 8-bit indexed values
- **Special Value:** 0xFF = no shadow (fully lit area)
- **Shadow Values:** 0-254 = shadow present (only one shadow level used in practice)

### 2. Character Shadow Palette Remap Tables (ALFRED.9)

**File Structure:**
- Size: 57,344 bytes (56 KB)
- Header: 512 bytes (0x000-0x1FF)
- Room data: 55 rooms × 1024 bytes (0x200-0xDDFF)
- Trailer: 512 bytes (0xDE00-0xDFFF)

**Room Block Structure (1024 bytes per room):**
```
Offset +0x000-0x0FF: Shadow remap table (256 bytes)
Offset +0x100-0x3FF: Unused/padding (768 bytes)
```

**Location Formula:**
```
remap_offset = 0x200 + (room_number * 1024)
```

**Examples:**
- Room 0: 0x200 (512)
- Room 5: 0x1600 (5632)
- Room 31: 0x7E00 (32256)
- Room 54: 0xDE00 (56832)

**Properties:**
- Each room has its own 256-byte remap table tailored to that room's palette
- Maps character palette index → darkened palette index
- Single shadow level (not multiple darkness levels)
- Loaded into memory at `DAT_00052bfc` during room initialization

**Remap Table Structure:**
- 256-byte lookup table
- Index = original palette index (0-255)
- Value = darkened palette index (0-255)
- Direct lookup: `shadowed_color = remap_table[original_color]`

**Example Mappings:**

Room 31 (offset 0x7E00):
```
Original Index → Shadow Index
      6        →    252
     11        →     72
     12        →      4
     13        →      5
```

Room 5 (offset 0x1600):
```
Original Index → Shadow Index
      6        →    103
     11        →     19
     12        →      4
     13        →      5
```

**Note:** Each room has unique mappings tailored to that room's specific palette colors.

## Loading Process

### In `load_room_data()` (Ghidra @ 0x000152f5)

```c
// 1. Load shadow map entry from directory
byte room_number = get_current_room_number();
file_seek(0, room_number * 6);
file_read(shadow_directory_entry, 6, 0);

// 2. Extract shadow offset (24-bit LE)
uint shadow_offset = shadow_directory_entry[0] |
                     (shadow_directory_entry[1] << 8) |
                     (shadow_directory_entry[2] << 16);

// 3. Load and decompress shadow data
file_seek(0, shadow_offset);
file_read(compressed_buffer, compressed_size, 0);
decompress_rle_block(compressed_buffer, DAT_0004fb24);
// DAT_0004fb24 now contains 256,000 bytes (640×400)

// 4. Load shadow remap table from ALFRED.9
uint remap_offset = 0x200 + (room_number * 1024);
file_seek(ALFRED_9, remap_offset);
file_read(DAT_00052bfc, 256, 0);
// DAT_00052bfc now contains 256-byte room-specific remap table
```

## Rendering Process

### Character Shadow Detection

**Function:** `render_character_sprite_scaled()` (Ghidra @ 0x00016ff8)

For each pixel position where the character sprite will be drawn, the game checks if that position is in shadow:

```c
// Calculate shadow map lookup position
// unaff_BX = character Y position on screen
// extraout_DX = character X position on screen
// bVar8 = current Y offset within character sprite (0 to height-1)

uint shadow_y = unaff_BX + 0x66;  // Add 102 (character height)
uint shadow_x = extraout_DX + bVar8;
byte* shadow_ptr = DAT_0004fb24 + (shadow_y * 640) + shadow_x;

byte shadow_value = *shadow_ptr;
if (shadow_value != 0xFF) {
    // Character is in shadow
    bVar2 = true;          // Enable shadow flag
    local_18 = shadow_value; // Store shadow intensity
}
```

### Pixel Rendering with Shadow

When rendering each pixel of the character sprite:

```c
// pbVar9 = pointer to character sprite pixel data
// DAT_0004fad8 = pointer to screen framebuffer

if (*pbVar9 != 0xFF) {  // If not transparent
    if (bVar2) {  // If shadow is active
        // Apply shadow by remapping color (single level)
        byte original_color = *pbVar9;
        byte shadowed_color = DAT_00052bfc[original_color];
        *DAT_0004fad8 = shadowed_color;
    } else {
        // No shadow, draw normally
        *DAT_0004fad8 = *pbVar9;
    }
}
```

## Algorithm Summary

### Shadow Detection Formula

```
For character at screen position (char_x, char_y):
  shadow_lookup_y = char_y + char_height (typically 102)
  shadow_lookup_x = char_x

  shadow_index = (shadow_lookup_y * 640) + shadow_lookup_x
  shadow_value = shadow_map[shadow_index]

  is_shadowed = (shadow_value != 0xFF)
```

### Color Remapping Formula

```
If character pixel is shadowed:
  original_color = sprite_pixel_value (0-255)
  new_color = shadow_remap_table[original_color]
  screen_pixel = new_color
Else:
  screen_pixel = original_color
```

## Key Observations

1. **Shadow Map Size:** Always 640×400, matching screen resolution exactly
2. **One Sample Point:** The game samples the shadow map at the character's base position (bottom of sprite), not per-pixel
3. **Single Shadow Level:** Binary shadow system (either shadowed or not), no multiple darkness levels
4. **Palette-Based:** Shadowing is achieved through palette remapping, not alpha blending
5. **Pre-calculated:** Shadow maps are pre-rendered and stored, not calculated at runtime
6. **Room-Specific Shadow Maps:** Each room has its own unique shadow map reflecting its lighting/geometry
7. **Room-Specific Remap Tables:** Each room has its own 256-byte remap table in ALFRED.9, tailored to that room's palette colors
8. **ALFRED.9 Structure:** 512-byte header + (55 rooms × 1024 bytes) + 512-byte trailer = 57,344 bytes total

## Implementation Notes

### For Extraction Tools

To extract and visualize shadow maps:

```python
def extract_shadow_map(alfred5_data, room_number):
    """Extract shadow map for a specific room from ALFRED.5"""
    # Read directory entry
    entry_offset = room_number * 6
    shadow_offset = (alfred5_data[entry_offset] |
                     (alfred5_data[entry_offset + 1] << 8) |
                     (alfred5_data[entry_offset + 2] << 16))

    # Decompress RLE data
    pixels = bytearray()
    offset = shadow_offset

    while offset < len(alfred5_data):
        if alfred5_data[offset:offset+4] == b'BUDA':
            break

        count = alfred5_data[offset]
        color = alfred5_data[offset + 1]
        pixels.extend([color] * count)
        offset += 2

    # Verify size
    assert len(pixels) == 640 * 400, f"Expected 256000 bytes, got {len(pixels)}"

    return pixels
```

### For Rendering Tools

To apply shadow to character sprites:

```python
def apply_shadow_to_sprite(sprite_pixels, char_x, char_y, shadow_map, palette_remap):
    """
    Apply shadow effect to character sprite

    Args:
        sprite_pixels: Character sprite pixel data (width * height)
        char_x, char_y: Character position on screen
        shadow_map: 640x400 shadow map for current room
        palette_remap: 1024-byte palette remapping table

    Returns:
        Modified sprite with shadow applied
    """
    # Sample shadow at character's foot position
    shadow_y = char_y + 102  # Character height
    shadow_x = char_x
    shadow_index = (shadow_y * 640) + shadow_x

    # Check if position is in shadow
    if shadow_index >= len(shadow_map):
        return sprite_pixels  # Out of bounds, no shadow

    shadow_value = shadow_map[shadow_index]

    if shadow_value == 0xFF:
        return sprite_pixels  # Not in shadow

    # Apply shadow by remapping colors
    shadowed_sprite = bytearray()
    for pixel in sprite_pixels:
        if pixel == 0xFF:  # Transparent
            shadowed_sprite.append(0xFF)
        else:
            # Remap to shadowed color
            remap_index = pixel + (shadow_value * 256)
            shadowed_color = palette_remap[remap_index]
            shadowed_sprite.append(shadowed_color)

    return shadowed_sprite
```

## Memory Layout

```
DAT_0004fb24:  Shadow map buffer (256,000 bytes)
               - Loaded from ALFRED.5
               - Decompressed RLE data
               - 640 × 400 = 256,000 bytes

DAT_00052bfc:  Palette remap table (1,024 bytes)
               - Loaded from ALFRED.1
               - 4 × 256 = 1,024 bytes
               - [0x000-0x0FF]: Shadow level 0
               - [0x100-0x1FF]: Shadow level 1
               - [0x200-0x2FF]: Shadow level 2
               - [0x300-0x3FF]: Shadow level 3
```

## Example Usage

For a character at position (320, 200) in a room where that position has shadow value 1:

```
1. Shadow lookup: shadow_map[(200 + 102) * 640 + 320] = 1
2. Character pixel color: 45
3. Remap lookup: palette_remap[45 + (1 * 256)] = palette_remap[301]
4. Result: pixel drawn with color from remap[301] instead of 45
```

## Related Files

- `RESOURCE_FILE_FORMAT_DOCUMENTATION.md` - ALFRED.5 file format
- `SCALING_WORK_SUMMARY.md` - Character rendering and scaling
- `load_room_data()` @ 0x000152f5 - Shadow loading code
- `render_character_sprite_scaled()` @ 0x00016ff8 - Shadow application code
