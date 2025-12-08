# Complete Inventory System Extraction

## Summary

Successfully extracted all inventory objects from Alfred Pelrock game:

- **69 inventory icons** (60x60 pixels, 16-color VGA palette)
- **113 object descriptions** (Spanish text with control codes)
- **Icon-to-object mapping** via remapping formula

## Files Generated

### Output Structure: `inventory_complete/`

Each icon has its own folder: `icon_00/` through `icon_68/`

Each folder contains:
- `icon.png` - The 60x60 pixel inventory icon
- `description_objXXX.txt` - Description file(s) for objects using this icon
- `metadata.json` - JSON with icon ID, object IDs, and offsets

## Key Findings

### Description Display System

When you click an inventory item in the settings menu (accessed via right-click):

1. **`render_action_popup_menu`** @ 0x0001AD9A sets `DAT_0004fba0` to the clicked object ID
2. **`main_menu_handler`** @ 0x00012918 calls a function from table @ 0x486fe
3. That function displays the description using the object ID as index

**Mapping**: Object ID (0-112) → Description at offset: `0x4715D + description_offsets[ID]`

The descriptions are stored sequentially starting at 0x4715D. Each description begins with the pattern `FD 00 08 [color]`.

### Icon Remapping Formula

Found in `render_inventory_items` @ 0x00012F06:

```c
if (obj_id < 59) {
    if (11 < obj_id < 59) {
        icon_id = ((obj_id - 11) & 3) + 11;  // Books cycle through icons 11-14
    } else {
        icon_id = obj_id;  // Direct mapping for IDs 0-11
    }
} else {
    icon_id = obj_id - 44;  // Offset for high IDs (59+)
}
```

### Shared Icons (Books)

Four icons are shared by multiple objects (library books):

- **Icon 11**: Objects 11, 15, 19, 23, 27, 31, 35, 39, 43, 47, 51, 55 (12 books)
- **Icon 12**: Objects 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56 (12 books)
- **Icon 13**: Objects 13, 17, 21, 25, 29, 33, 37, 41, 45, 49, 53, 57 (12 books)
- **Icon 14**: Objects 14, 18, 22, 26, 30, 34, 38, 42, 46, 50, 54, 58 (12 books)

This allows 48 different books (objects 11-58) to share only 4 icon graphics using modulo 4 arithmetic.

## Data Locations

### ALFRED.4
- **Offset**: 0xA57E
- **Count**: 69 icons
- **Size per icon**: 0xE10 (3600 bytes) = 60×60 pixels
- **Format**: Raw 4-bit palette indices (16-color VGA)

### JUEGO.EXE
- **Offset**: 0x4715D - 0x49018
- **Count**: 113 descriptions
- **Format**: FD 00 08 [color] [text] [terminator]
- **Encoding**: CP850 (DOS Spanish)

### Control Characters in Text

- `0xFD` - Description header (FD 00 08)
- `0xF4`, `0xF8`, `0xF0` - End markers
- `0xF6` - Line continuation
- `0xF9` - Page break
- `0x08` - Start marker (third byte of header)
- `0xC9` (╚) - Line break character in CP850

## Object Categories

Based on descriptions, objects include:

1. **Books** (IDs 11-58): 48 different books cycling through 4 icons
2. **Documents**: ID cards, library cards, photos, letters
3. **Money**: Credit card (ID 2), 1000 pesetas (ID 5)
4. **Tools**: Brick (ID 4), extension cord (ID 6), patches, glue
5. **Mystical**: Egyptian amulet (ID 7), magic lamp cloth, mantra card
6. **Food**: Oranges from Nules
7. **Miscellaneous**: Condoms, Elvis tape, Alfred replica doll, pin, etc.

## Code References

### Key Functions (in JUEGO.EXE)

- **render_inventory_items** @ 0x00012F06
  - Displays inventory in 4-slot right-click menu
  - Applies icon remapping formula
  - Reads from runtime array at DAT_0004fc94

- **display_text_description** @ 0x0001a298
  - Used for hotspot descriptions (not inventory)
  - Different from inventory item descriptions

- **handle_object_click** @ 0x00018502
  - Handles object interaction in rooms

- **load_room_objects** @ 0x00016a17
  - Loads pickable objects from rooms

- **remove_inventory_item** @ 0x0001b83a
  - Removes item from inventory array

## Extraction Scripts

### Final Script: `extract_complete_inventory.py`

Complete extraction of all 69 icons with 113 descriptions:

```bash
python3 extract_complete_inventory.py
```

Output:
- Creates `inventory_complete/` directory
- 69 folders (icon_00 through icon_68)
- PNG icons with VGA palette
- Text descriptions for each object
- JSON metadata with mappings

### Helper Scripts

- `parse_descriptions_properly.py` - Parses all 113 descriptions from JUEGO.EXE
- `search_entire_exe.py` - Finds all FD 00 08 patterns in executable
- `find_all_patterns.py` - Pattern analysis for control codes

## Verification

Confirmed 113 descriptions in range 0x4715D - 0x49018:

```bash
python3 search_entire_exe.py
# Output: Range 0x4715D - 0x49018 contains: 113
```

All 69 icons extracted successfully with correct VGA palette.

## Usage Example

To get an object's description:

1. Determine object ID (0-112)
2. Calculate icon ID using remapping formula
3. Look in `inventory_complete/icon_XX/`
4. Read `description_objYYY.txt`

Example for book ID 15:
- Icon = ((15-11) & 3) + 11 = (4 & 3) + 11 = 0 + 11 = 11
- File: `inventory_complete/icon_11/description_obj015.txt`

## Notes

- Pickable objects use bit 3 (0x08) in hotspot type byte
- Not all objects are pickable hotspots (e.g., library computer gives books via script)
- Inventory displayed via right-click menu with 4 slots and navigation
- Some object IDs may not have room hotspots (obtained through other means)

---

Generated: 2024
Game: Alfred Pelrock (DOS)
