# Complete Game Mechanics Analysis via Ghidra

## How the Game Handles Actions Like "Open Door"

### Action System Architecture

The game uses a **multi-tier dispatch system** based on room types and action contexts:

#### 1. Main Action Entry Point: `handle_hotspot_interaction` (0x000124ad)

When the player clicks on a hotspot:
1. The game displays an **action menu** with available verbs (look, take, use, etc.)
2. Creates a visual popup with action icons from `action_text_table_ptr`
3. Waits for the player to select an action
4. Calls `room_specific_action_dispatcher` with the selected action

#### 2. Room-Specific Action Dispatcher (0x00018562)

This is the **central routing function** that determines how to handle each action:

```c
void room_specific_action_dispatcher(void) {
    get_current_room_number();
    action_pending_flag = 0;

    if (room_flags & 0x01) execute_room_specific_script();
    if (room_flags & 0x02) handle_conversation_tree();
    if (room_flags & 0x08) handle_dialog_interaction();
    if (room_flags & 0x10) dispatch_hotspot_action_by_extra_id();
    if (room_flags & 0x20) execute_script_table_0x47c10();
    if (room_flags & 0x40) execute_script_table_0x47c18();
    if (room_flags & 0x80) execute_script_table_0x47cbc();
    if (room_flags & 0x200) execute_complex_item_script_table();
}
```

**Room flags** determine which dispatch tables are active for each room.

#### 3. Action Dispatch Tables

The game uses **multiple dispatch tables** that map hotspot IDs to function pointers:

##### Table 1: Simple Hotspot Actions (0x00047bf0)
- **Structure**: 6 bytes per entry `[2-byte hotspot_extra_id, 4-byte function_ptr]`
- Used by `dispatch_hotspot_action_by_extra_id`
- Example: Clicking on room0 drawer (hotspot_extra_id=261) triggers a specific function

##### Table 2: Room-Specific Scripts (0x00047d24)
- **Structure**: 6 bytes per entry `[2-byte hotspot_extra_id, 4-byte function_ptr]`
- Used by `execute_room_specific_script`
- Handles room-specific object interactions

##### Table 3: Complex Item Combinations (0x00048118)
- **Structure**: 8 bytes per entry `[2-byte item1_id, 2-byte item2_id, 4-byte function_ptr]`
- Used by `execute_complex_item_script_table`
- Handles "use item X with Y" scenarios

### Example Flow: "Open Door"

1. Player clicks on door hotspot
2. `handle_hotspot_interaction` displays action menu
3. Player selects "open" action
4. `room_specific_action_dispatcher` is called with action code
5. Based on room flags, appropriate dispatch function is called
6. Dispatch function looks up door's `hotspot_extra_id` in its table
7. Associated function pointer is called (e.g., `open_door_function`)
8. Function modifies game state (door opened, exit enabled)

---

## How "Use Item X with Y" Works

### Inventory System

**Inventory Storage**: Array at `0x0004fc94`
- Each item is a 2-byte ID
- `num_available_actions` (at various locations) tracks count
- `DAT_0004fba0` stores currently selected item (-1 if none)

### Item Combination Logic in `execute_complex_item_script_table` (0x000191e9)

```c
void execute_complex_item_script_table(void) {
    get_current_room_number();
    current_hotspot_extra_id = hotspot_id_or_data;

    // First pass: Check for exact matches (item1 + item2 on hotspot0)
    for (i = 0; table[i].item1 != -1; i++) {
        if (table[i].item1 == table[i].item2 &&
            table[i].item1 == DAT_0004fba0 &&
            current_hotspot_extra_id == 0) {
            // Execute action function
            table[i].function();
            return;
        }
    }

    // Second pass: Check item+hotspot or hotspot+item combinations
    for (i = 0; table[i].item1 != -1; i++) {
        if ((table[i].item1 == current_hotspot_extra_id &&
             table[i].item2 == DAT_0004fba0) ||
            (table[i].item1 == DAT_0004fba0 &&
             table[i].item2 == current_hotspot_extra_id)) {
            // Walk to target
            if (walk_to_target_and_execute_queued_action()) {
                animate_talk_bubble();
                table[i].function();
                return;
            }
        }
    }

    // No match found: Play random "can't do that" response
    alfred_facing_direction = 2;
    setup_alfred_frame_from_state();
    render_scene(0);
    display_text_with_voice(random_rejection_message[random() & 0xf]);
}
```

**Key Points**:
- Table at `0x00048118` contains all valid item combinations
- `DAT_0004fba0` stores currently held/selected inventory item
- `current_hotspot_extra_id` stores target object ID
- If no match found, Alfred says a random "I can't do that" phrase

---

## How Alfred's Responses Map to Actions

### Text Response System

#### Text Storage and Extraction

Text responses are stored in **ALFRED.X files** and loaded into memory buffers.

The function `display_text_description` (0x0001a298) handles text rendering:

1. **Text Pointer**: Each action/object has a pointer to its text description
2. **Text Format**: Encoded with special control characters:
   - `0xfd` (253/-3): End of text
   - `0xf4` (244/-12): Alternative end marker
   - `0xf8` (248/-8): Extended text marker
   - `0xf0` (240/-16): Another control code
   - `0xf6` (246): Line break within text block
   - `0xf9` (249): Page break (multiple text screens)
   - `0xf7` (247): Conversation branch marker

3. **Voice File Mapping**: The function `trigger_dialog_or_action` (0x0001a683) builds voice filenames:
   ```c
   // Constructs filename like "VOC00XXX.WAV"
   room_number_to_ascii(text_id_high);
   s_VOC00000_WAV[3] = digit1;
   s_VOC00000_WAV[4] = digit2;
   room_number_to_ascii_alt(text_id_low);
   s_VOC00000_WAV[5] = digit3;
   s_VOC00000_WAV[6] = digit4;
   s_VOC00000_WAV[7] = digit5;

   if (sound_enabled && frame_toggle_flag && text_id != 0xff) {
       load_sound_file("VOC00000.WAV", 6);
   }
   ```

#### Action → Text Mapping

**Direct Mapping**:
- Each hotspot has a `description_offset` field pointing to text data
- When action is performed, text at that offset is displayed
- Voice file ID is embedded in the text data structure

**Example from your `extract_text_properly.py`**:
- Text marker: `\xfd\x00\x08\x02` followed by text
- The `08 02` bytes likely encode text ID for voice file lookup
- Your script extracts these to correlate with voice files

---

## Game State Persistence

### How Stickers, Exits, Hotspots, and Conversation Branches Are Saved

#### 1. Conversation State Array (0x0004fba4)

**Structure**: 4 bytes per room × number of rooms
```c
void update_conversation_state(void) {
    room_number = get_current_room_number();
    conversation_state_array[dialog_id + room_number*4] = branch_index;

    // Also updates in-memory conversation pointer table
    if (room_number == current_room_number) {
        // Find the Nth dialog branch marker (0xf7)
        // Update pointer at room_sprite_data_ptr+0x3da
        room_sprite_data_ptr->dialog_pointers[dialog_id] = new_branch_ptr;
    }
}
```

**What it stores**:
- Which conversation branches have been taken
- Which dialog options are no longer available
- Indexed by: `room_id * 4 + dialog_slot`

#### 2. Inventory Items (0x0004fc94)

**Structure**: Array of 2-byte item IDs
```c
// Max items tracked by num_available_actions
undefined2 inventory_items[MAX_INVENTORY];
byte num_available_actions;  // Current item count
short DAT_0004fba0;          // Currently selected item (-1 if none)
```

**Functions**:
- `process_inventory_action` (0x00024157): Adds item to inventory
- `remove_inventory_item` (0x0001b83a): Removes item from inventory

#### 3. Room State (exits, hotspots, stickers)

The game uses **room-specific data structures** loaded from ALFRED.X files:

**Exit Table** (in room_sprite_data_ptr):
- Located at offset `0x1be` in room data
- Each exit: 14 bytes (0xe)
  ```c
  struct Exit {
      byte enabled;              // +0x1c1: 0=disabled, 1=enabled
      ushort trigger_x;          // +0x1c2: Trigger zone X
      ushort trigger_y;          // +0x1c4: Trigger zone Y
      byte width;                // +0x1c6: Trigger width
      byte height;               // +0x1c7: Trigger height
      ushort dest_x;             // +0x1c8: Destination X in new room
      ushort dest_y;             // +0x1ca: Destination Y
      byte dest_direction;       // +0x1cc: Alfred's facing direction
      ushort dest_room;          // +0x1bf: Target room number
  };
  ```

**Hotspot/Sprite Table** (in room_sprite_data_ptr):
- Up to 20 sprites per room (0x14)
- Each sprite: 44 bytes (0x2c)
  ```c
  struct Sprite {
      ushort x, y;               // +0x00: Position
      ushort width, height;      // +0x04: Dimensions
      byte visible;              // +0x08: Visibility flag
      byte extra_id;             // +0x06: Hotspot identifier for dispatch tables
      byte z_depth;              // +0x21: Rendering order
      // ... animation frames, etc.
  };
  ```

**Sticker System**:
- Likely stored in sprite slots (sprites 0-19)
- When a sticker is "placed", its `visible` flag is set to 1
- Position data determines where it appears in the room

#### 4. Where Is This State Saved to Disk?

**Critical Finding**: I did NOT find traditional save/load game functions in Ghidra!

**Possible explanations**:
1. **No Save System**: The game may not have save/load functionality (only checkpoints/restart)
2. **External Save System**: Save functionality might be in a different executable or overlay
3. **Memory-Only State**: State persists only during current play session
4. **DOS TSR or Driver**: State could be saved via DOS-level calls not visible in decompilation

**Evidence**:
- No file operations with names like "save", "load", "savegame", etc.
- No serialization of the state arrays found
- The file `salvajoc.xxx` (found at 0x0004021c) might be related ("salva" = "save" in Spanish)

**Recommendation**: Check if `salvajoc.xxx` is created during gameplay. Also search for DOS INT 21h file write calls in the binary.

---

## What is alfred.a Used For?

### File: alfred.a (Multiple References at 0x00040048, 0x000400b7, 0x00040200)

**Purpose**: **Primary Resource Archive** - Main data container for the game

### Analysis from `open_all_resource_files` (0x000148f2)

```c
void open_all_resource_files(void) {
    get_current_room_number();

    // Open alfred.a (appears to be opened via FUN_0002acae)
    FUN_0002acae("alfred.a", 0x180);

    // Then open all numbered ALFRED.X files
    for (i = 0; i < 12; i++) {
        file_handle = FUN_0002aaa6(alfred_filenames[i], &DAT_000400c0, i, ...);
        file_handle_alfred[i] = file_handle;

        if (file_handle == 0) {
            // Error handling
            memcpy_wrapper("alfred.x no encontrado", alfred_filenames[i]);
            FUN_00039057(0xc);
            FUN_00039248("alfred.x no encontrado");
            FUN_0002a2d2(1);  // Exit program
        }
    }
}
```

**File Structure**:
- `alfred.a`: Primary archive/index file
- `alfred.1` through `alfred.b`: 12 numbered resource files
- Files opened during `game_initialization` (0x00010010)

**What alfred.a Contains**:
Based on the file open mode (0x180) and context:
1. **File Table/Index**: Points to data in alfred.1-b files
2. **Offsets and Sizes**: Each entry maps to resources in numbered files
3. **Resource Metadata**: Types, compression info, etc.

**Related Files**:
```
alfred.1 - alfred.b   : Numbered data files (graphics, sounds, etc.)
alfred.7              : Room graphics (see load_room_graphics_and_palette_dynamic)
sound.cfg             : Sound configuration
```

**How It's Used**:
1. Game opens `alfred.a` first to read the resource index
2. Opens all 12 numbered files (alfred.1-b)
3. When loading rooms/objects, uses offsets from alfred.a to read from appropriate numbered file
4. ALFRED.7 specifically contains:
   - Room background blocks (8 blocks per room, offset table at 0x000488f4)
   - Palette data (offset +0x30 per room entry)
   - Compressed with RLE encoding

---

## Summary

### Action System
- **Multi-tier dispatch** based on room flags and hotspot IDs
- **Three main dispatch tables**: simple hotspots, room scripts, item combinations
- Actions map to function pointers in these tables

### Text Responses
- Stored in ALFRED.X files with control character encoding
- Voice files named `VOCxxxxx.WAV` with IDs embedded in text data
- Your `extract_text_properly.py` correctly identifies text markers

### State Management
- **Conversation state**: Array at 0x0004fba4 (4 bytes × rooms)
- **Inventory**: Array at 0x0004fc94 (2 bytes per item)
- **Room state**: In-memory structures loaded from ALFRED.X files
  - Exits with enable/disable flags
  - Sprite visibility flags (for stickers)
  - Hotspot extra_id for dispatch lookups
- **No persistent save system found** - may be session-only or external

### alfred.a
- **Resource index/archive** for all game data
- Works with alfred.1-b numbered files
- Contains offset table for resource loading
- ALFRED.7 specifically holds room graphics and palettes

### Key Data Addresses
```
0x0004fba4  : Conversation state array
0x0004fc94  : Inventory items array
0x0004fba0  : Currently selected item
0x00047bf0  : Hotspot action dispatch table
0x00047d24  : Room script dispatch table
0x00048118  : Item combination dispatch table
0x000488f4  : ALFRED.7 room graphics offset table
```
