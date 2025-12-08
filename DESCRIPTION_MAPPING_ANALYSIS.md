# Inventory Object Description Mapping - FINDINGS

Based on Ghidra analysis, here's what we know about how inventory item descriptions work:

## Key Functions

### `main_menu_handler` @ 0x00012918
- Displays the settings/inventory menu accessed via right-click
- When an item is clicked, stores the item ID in `DAT_0004fba0`
- Calls function from table at `0x486fe` based on which slot was clicked

### `render_inventory_items` @ 0x00012F06
- Renders 4 inventory icon slots
- Reads from inventory array `DAT_0004fc94`
- Applies icon remapping formula for books (IDs 11-58)

### `render_action_popup_menu` @ 0x0001AD9A
- Renders the action popup menu (verb icons)
- When clicked, sets `DAT_0004fba0` and `DAT_0005177e` = 1
- Called from `render_scene` with parameter 0xFE

### `display_text_description` @ 0x0001A298
- Actually displays text on screen
- Reads description from: `get_current_room_number() + offset`
- Used for hotspot descriptions (not inventory directly)

## The Missing Link

**CRITICAL**: I need to find the function that:
1. Takes the clicked inventory item ID from `DAT_0004fba0`
2. Maps it to the corresponding description offset (0x4715D + offset)
3. Either:
   - Calls `display_text_description` with a fake "room pointer"
   - OR has its own text display logic

## Description Data

- **Location**: JUEGO.EXE @ 0x4715D - 0x49018
- **Count**: 113 descriptions
- **Format**: FD 00 08 [color] [text] [terminators]
- **Offsets**: Sequential, starting at 0x4715D

## What's Still Unknown

1. **Mapping table**: Is there a 113-entry table mapping object IDs to description offsets?
2. **Display function**: What function actually shows inventory item descriptions when clicked?
3. **Invocation**: How does the game call this function from the menu click handler?

## Next Steps for Complete Mapping

Need to find in Ghidra:
- Code that reads `DAT_0004fba0` after menu click
- Functions that take object ID and return/display description
- Possible description offset table (113 entries × 4 bytes = 452 bytes)
- Or code that calculates: `description_ptr = 0x4715D + lookup_table[object_id]`
