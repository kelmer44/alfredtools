# Object ID, Icon, and Description Mapping

## Summary

The game uses the hotspot's `extra` field as the **object ID**. This object ID is used differently for descriptions and icons:

1. **Description**: Object ID appears to directly index into the description table
2. **Icon**: Object ID goes through a remapping formula before indexing into icons

## Data Structures

### Object Descriptions (JUEGO.EXE: 0x4715D - 0x49018)
- **Count**: 57 descriptions (IDs 0-56)
- **Format**: `FD 00 08 [color_byte] [text...] 00`
  - Signature: `FD 00 08`
  - Color byte: Text color for display
  - Text: CP850 encoded string
  - Null terminator: `00`

### Inventory Icons (ALFRED.4: offset 0xA57E)
- **Count**: 69 icons (IDs 0-68)
- **Format**: 60x60 pixels, paletted
- **Size per icon**: 0xE10 (3600) bytes
- **File offset formula**: `icon_id * 0xE10 + 0xA57E`

## Icon ID Remapping (from render_inventory_items @ 0x00012F06)

The game remaps object IDs to icon IDs using this algorithm:

```c
uint icon_id = object_id;  // Start with object ID from hotspot 'extra' field

if (icon_id < 0x3B) {  // If object_id < 59
    if ((icon_id > 10) && (icon_id < 0x3B)) {
        // For object IDs 11-58: remap to icons 11-14 (cycling pattern)
        icon_id = ((icon_id - 0x0B) & 3) + 0x0B;
    }
    // else: object IDs 0-10 map directly to icons 0-10
} else {
    // For object IDs >= 59: subtract 44
    icon_id = object_id - 0x2C;
}

// Now use icon_id to load from ALFRED.4
file_seek(icon_id * 0xE10 + 0xA57E);
```

### Remapping Table

| Object ID Range | Icon ID Formula | Result | Notes |
|-----------------|-----------------|---------|-------|
| 0-10 | direct | 0-10 | First 11 objects have unique icons |
| 11-58 | `((id - 11) & 3) + 11` | 11-14 (cycling) | **Books**: 48 objects share 4 book icons |
| 59+ | `id - 44` | 15-68 | Objects 59-112 map to icons 15-68 |

### Examples

- Object 0 → Icon 0 (Historia de la Princesa book)
- Object 1 → Icon 1 (Credit card)
- Object 2 → Icon 2 (Brick)
- Object 11 → Icon 11 (First book icon)
- Object 12 → Icon 12 (Second book icon)
- Object 13 → Icon 13 (Third book icon)
- Object 14 → Icon 14 (Fourth book icon)
- Object 15 → Icon 11 (Cycles back to first book icon)
- Object 16 → Icon 12 (Second book icon again)
- ...
- Object 59 → Icon 15
- Object 60 → Icon 16
- ...

## Book Objects (IDs 11-58)

The remapping formula `((id - 11) & 3) + 11` means:
- Objects 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55 → Icon 11
- Objects 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56 → Icon 12
- Objects 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57 → Icon 13
- Objects 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58 → Icon 14

This allows the library to have many different books (with unique titles/authors in descriptions) that all share 4 generic book icons.

## Description Mapping

Based on the description data, object IDs 0-56 have unique descriptions. Object IDs >= 57 may not have descriptions in the analyzed range, or there may be additional descriptions elsewhere.

Object IDs 6-29 (at least) are book descriptions with title/author format:
```
Titulo: [book title]
Autor: [author name]
Genero: [genre]
```

## Hotspot Structure (ALFRED.1)

Each hotspot in room data (9 bytes):
- Byte 0: Type flags
  - **Bit 3 (0x08)**: Pickable object flag
- Bytes 1-2: X coordinate (little-endian)
- Bytes 3-4: Y coordinate (little-endian)
- Byte 5: Width
- Byte 6: Height
- Bytes 7-8: **Extra field** = Object ID (little-endian)

## Inventory Array (DAT_0004fc94)

The game maintains an inventory array at runtime address 0x0004FC94. Each entry is the object ID of an item in the player's inventory. The `render_inventory_items` function reads from this array and applies the icon remapping formula to display the correct icon.

## Questions Answered

1. **How does the game map object IDs to icons?**
   - Through the remapping formula in `render_inventory_items`

2. **How do multiple books share icons?**
   - Objects 11-58 all remap to icons 11-14 using modulo 4 logic

3. **How are descriptions accessed?**
   - Appears to be direct indexing: object ID → description ID
   - Descriptions start at JUEGO.EXE offset 0x4715D
   - Each description begins with `FD 00 08` signature

4. **Why are there 69 icons but only 57 descriptions?**
   - Icons 11-14 are shared by many objects (books)
   - Some icons may be for objects without descriptions (or descriptions elsewhere)
   - The remapping formula creates this difference
