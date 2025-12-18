# Complete Game Mechanics Analysis via Ghidra

> **Last Updated**: Comprehensive MCP/Ghidra analysis session with function decompilation and data label renaming

## Table of Contents
1. [Action System Overview](#how-the-game-handles-actions-like-open-door)
2. [Text Response Selection](#text-response-selection-mechanism)
3. [Random Rejection Messages](#random-rejection-messages-no-puedo-hacer-eso)
4. [F8 Action Codes](#f8-action-codes-in-text-data)
5. [In-Memory State Storage](#in-memory-state-storage)
6. [Use Item X with Y](#how-use-item-x-with-y-works)
7. [Resource File (alfred.a)](#alfreds-resource-file-system)
8. [Key Data Addresses](#key-data-addresses-reference)

---

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
    if (room_flags & 0x20) execute_script_table_0x47c10();  // TAKE actions
    if (room_flags & 0x40) execute_script_table_0x47c18();  // PICK UP actions
    if (room_flags & 0x80) execute_script_table_0x47cbc();
    if (room_flags & 0x200) execute_complex_item_script_table();  // USE X WITH Y
}
```

**Room flags** determine which dispatch tables are active for each room.

#### 3. Action Dispatch Tables

The game uses **multiple dispatch tables** that map hotspot IDs to function pointers:

| Table Address | Structure | Purpose |
|--------------|-----------|---------|
| `0x00047bf0` | 6 bytes: `[uint16 id, ptr32 func]` | Main hotspot actions |
| `0x00047c10` | 6 bytes: `[uint16 id, ptr32 func]` | "Take" verb actions |
| `0x00047c18` | 6 bytes: `[uint16 id, ptr32 func]` | "Pick up" verb actions |
| `0x00047d24` | 6 bytes: `[uint16 id, ptr32 func]` | Room-specific scripts |
| `0x00047e58` | 6 bytes: `[uint16 id, ptr32 func]` | F8 action codes |
| `0x00048118` | 8 bytes: `[uint16 item1, uint16 item2, ptr32 func]` | Item combinations |

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

## Text Response Selection Mechanism

### How Specific Texts Like "Ya esta abierto" Are Selected

**Critical Finding**: Text is NOT hardcoded in the EXE. All game text is loaded dynamically from ALFRED.X resource files at runtime.

#### Text Pointer Table Construction (in `load_room_and_init_alfred` at 0x000152f5)

When a room loads, the game builds a **text pointer table** at `room_sprite_data_ptr + 0x3da`:

```c
// Scan room text data for 0xFF and 0xFE markers
text_scanner = room_text_data_ptr;
uVar8 = 0;   // Text index counter
uVar11 = 0;  // Conditional text counter

while (cVar6 != 0xF5) {  // End of text data marker
    cVar6 = *text_scanner;

    // 0xFF = Standard text entry
    if (cVar6 == 0xFF) {
        text_scanner = text_scanner + 2;  // Skip marker + item_id
        *(text_scanner**)(room_sprite_data_ptr + uVar8 * 4 + 0x3da) = text_scanner;
        uVar8 = uVar8 + 1;
    }

    // 0xFE = Conditional text entry (conversation branch dependent)
    if (cVar6 == 0xFE) {
        text_scanner = text_scanner + 2;

        // Check conversation state array for this branch
        if (conversation_branch_state_array[room_number * 4 + uVar11] != 0) {
            // Skip to alternate text if branch taken
            do {
                if (*text_scanner == 0xF9) {  // Branch marker
                    cVar7 = cVar7 + 1;
                }
                text_scanner++;
            } while (cVar7 != unaff_BL);
        }

        *(text_scanner**)(room_sprite_data_ptr + uVar8 * 4 + 0x3da) = text_scanner;
        uVar8 = uVar8 + 1;
        uVar11 = uVar11 + 1;  // Next conditional slot
    }

    text_scanner++;
}
```

#### How "Ya esta abierto" Gets Selected

When a door action is triggered:

1. **Handler function** looks up the hotspot's sprite index
2. Uses sprite index to calculate text pointer offset:
   ```c
   // In handle_dialog_interaction (0x00018f10):
   if (queued_mouse_hover_state == 0x01) {
       bVar4 = queued_hotspot_sprite_index - 2;
   } else {
       bVar4 = room_sprite_data_ptr[0x47b] - 1 + queued_hotspot_sprite_index;
   }

   // Get text pointer from table
   text_ptr = *(room_sprite_data_ptr + 0x3da + bVar4 * 4);
   display_text_description(text_ptr);
   ```

3. **Text data format** in ALFRED.X files:
   ```
   [0xFF][itemId][say][textColor][index][zero][text...][0xFD]

   0xFF    = Standard text marker
   itemId  = Object/action identifier
   say     = Voice file ID (high byte)
   textColor = Text color palette index
   index   = Original sprite/hotspot index (development metadata)
   zero    = Padding
   text    = ASCII text string
   0xFD    = End of text marker
   ```

4. **For doors with state**:
   - If door uses `0xFE` marker (conditional), the state check determines which text to show
   - "Already open" message is the alternate branch when door state == 1
   - "Cannot open" or action text is the default when door state == 0

---

## Random Rejection Messages ("No puedo hacer eso")

### Mechanism: Table-Based Selection (CONFIRMED)

**Data Address**: `0x0004bc1c` - renamed to `RANDOM_REJECTION_TEXT_PTRS`

The game stores **16 different rejection phrases** in a pointer table.

#### Code in `execute_complex_item_script_table` (0x000191e9):

```c
// When no valid item combination is found:
if (no_valid_combination) {
    alfred_facing_direction = 2;
    setup_alfred_frame_from_state();
    render_scene(0);

    // Select random rejection message
    uVar2 = random_number_generator();
    display_text_with_voice((&RANDOM_REJECTION_TEXT_PTRS)[uVar2 & 0xf]);  // 16 entries
}
```

#### Rejection Text Table Layout:

| Index | Address | Example Text (Spanish) |
|-------|---------|----------------------|
| 0 | 0x00042de5 | "No puedo hacer eso" |
| 1 | 0x00042df7 | "Eso no funciona" |
| 2 | 0x00042e06 | "No tiene sentido" |
| 3 | 0x00042e15 | ... |
| ... | ... | ... |
| 15 | 0x00042exx | (16th variation) |

**Key Points**:
- `uVar2 & 0xf` masks random number to 0-15 range
- All 16 texts are semantically equivalent ("can't do that" variations)
- This creates variety in Alfred's responses
- The pointer table is in the DATA segment, loaded at startup

---

## F8 Action Codes in Text Data

### What F8 Bytes Mean

The `0xF8` byte in text data is an **action trigger**. When encountered during text display, it executes a game function.

#### F8 Parsing in `handle_dialog_interaction` (0x00018f10):

```c
// After displaying text, check for F8 marker
if (cVar3 == 0xF8) {  // -8 in signed
    // Read uint16 action ID (little-endian)
    action_id = (uint)extraout_ECX_00[1] << 8 | *extraout_ECX_00;

    // Look up in F8_ACTION_DISPATCH_TABLE at 0x00047e58
    cVar3 = 0;
    while (true) {
        iVar6 = (extraout_EDX_00 & 0xff) * 6;

        // End of table marker
        if (*(short *)(&F8_ACTION_DISPATCH_TABLE + iVar6) == -1) break;

        // Check for matching action ID
        if ((ushort)(bVar4 + sVar1) == *(short *)(&F8_ACTION_DISPATCH_TABLE + iVar6)) {
            // Call the action function
            (**(code **)(&F8_ACTION_DISPATCH_TABLE + iVar6 + 2))();
            nop_stub_3();
            return;
        }
        cVar3++;
    }
}
```

#### F8 Action Table Structure (at 0x00047e58):

| Offset | Field | Size |
|--------|-------|------|
| +0x00 | Action ID (uint16) | 2 bytes |
| +0x02 | Function Pointer | 4 bytes |
| Total | | 6 bytes per entry |

**Example**: `F8 48 01` in text data:
- `F8` = Action trigger marker
- `48 01` = Action ID 0x0148 (little-endian)
- Game looks up 0x0148 in F8_ACTION_DISPATCH_TABLE
- Executes the associated function

#### Common F8 Actions:
- Enable/disable room exits
- Change sprite visibility (stickers)
- Update conversation state
- Trigger animations
- Add/remove inventory items
- Play sound effects

---

## In-Memory State Storage

### Detailed Memory Map

#### 1. Conversation Branch State Array

**Address**: `0x0004fba4` (renamed: `conversation_branch_state_array`)

**Structure**:
```
conversation_branch_state_array[room_id * 4 + branch_slot]
```

- 4 bytes allocated per room
- Each byte represents one conversation branch state
- Value 0 = branch not taken, Value N = branch N was selected

**Update Function** (`update_conversation_state` at 0x0001b666):
```c
void update_conversation_state(uint8 branch_slot, uint8 branch_value) {
    room_number = get_current_room_number();
    conversation_branch_state_array[branch_slot + room_number * 4] = branch_value;

    // If in current room, also update runtime text pointer
    if (room_number == current_room_number) {
        // Find the correct 0xF7 branch in text data
        // Update pointer table at room_sprite_data_ptr + 0x3da
    }
}
```

#### 2. Inventory Items

**Address**: `0x0004fc94` (renamed: `inventory_item_ids`)

**Structure**:
```c
uint16 inventory_item_ids[MAX_ITEMS];  // Array of item IDs
uint8  num_available_actions;          // Current item count
int16  DAT_0004fba0;                   // Currently selected item (-1 if none)
```

**Functions**:
- `process_inventory_action` (0x00024157): Adds item
- `remove_inventory_item` (0x0001b83a): Removes item by shifting array

#### 3. Sprite/Sticker Visibility

**Location**: `room_sprite_data_ptr + sprite_id * 0x2c + 0x21`

**Z-Depth Field** (offset +0x21 in 44-byte sprite structure):
- Value `0xFF` = sprite disabled/invisible
- Value `0x00-0xFE` = Z-depth layer for rendering

**To disable a sprite (sticker removed):**
```c
*(room_sprite_data_ptr + sprite_id * 0x2c + 0x21) = 0xFF;
```

**To enable a sprite (sticker placed):**
```c
*(room_sprite_data_ptr + sprite_id * 0x2c + 0x21) = z_depth_value;
```

#### 4. Exit Enable/Disable

**Location**: `room_sprite_data_ptr + 0x1bf + exit_id * 0x0E + 0x02`

**Exit Structure** (14 bytes each, starting at offset 0x1bf):
```c
struct RoomExit {
    uint16 target_room;      // +0x00: Destination room number
    uint8  enabled;          // +0x02: 0=disabled, 1=enabled
    uint16 trigger_x;        // +0x03: Trigger zone X
    uint16 trigger_y;        // +0x05: Trigger zone Y
    uint8  width;            // +0x07: Trigger zone width
    uint8  height;           // +0x08: Trigger zone height
    uint16 dest_x;           // +0x09: Destination X coordinate
    uint16 dest_y;           // +0x0B: Destination Y coordinate
    uint8  dest_facing;      // +0x0D: Alfred's facing direction
};
```

**Exit count** at: `room_sprite_data_ptr + 0x1be` (1 byte)

**Check code** (from `check_mouse_on_sprites_and_hotspots`):
```c
// Walk through all exits
exit_count = *(room_sprite_data_ptr + 0x1be);
for (i = 0; i < exit_count; i++) {
    exit_ptr = room_sprite_data_ptr + i * 0x0E;

    // Check if exit is enabled
    if (*(exit_ptr + 0x1c1) != 0) {  // 0x1bf + 0x02 = 0x1c1
        // Check if player in trigger zone
        if (target_x >= *(exit_ptr + 0x1c2) &&
            target_y >= *(exit_ptr + 0x1c4) &&
            target_x <= *(exit_ptr + 0x1c2) + *(exit_ptr + 0x1c6) &&
            target_y <= *(exit_ptr + 0x1c4) + *(exit_ptr + 0x1c7)) {
            exit_detected = 1;
            return;
        }
    }
}
```

#### 5. Hotspot State

**Location**: `room_sprite_data_ptr + 0x47b + hotspot_id * 9`

**Hotspot count** at: `room_sprite_data_ptr + 0x47a` (1 byte)

**Hotspot Structure** (9 bytes each):
```c
struct Hotspot {
    uint8  unknown;          // +0x00
    uint8  action_flags;     // +0x01 (high bit = enabled?)
    uint16 x;                // +0x02
    uint16 y;                // +0x04
    uint8  width;            // +0x06
    uint8  height;           // +0x07
    uint16 extra_id;         // +0x08: ID for dispatch table lookup
};
```

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
    display_text_with_voice(RANDOM_REJECTION_TEXT_PTRS[random() & 0xf]);
}
```

**Key Points**:
- Table at `0x00048118` contains all valid item combinations
- `DAT_0004fba0` stores currently held/selected inventory item
- `current_hotspot_extra_id` stores target object ID
- If no match found, Alfred says a random "I can't do that" phrase

---

## alfred.a Resource File System

### File: alfred.a (References at 0x00040048, 0x000400b7, 0x00040200)

**Purpose**: **Primary Resource Index/Archive** - Contains offset table for all game data

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
            // Error handling - "alfred.x no encontrado"
            FUN_0002a2d2(1);  // Exit program
        }
    }
}
```

### Resource File Organization

| File | Purpose |
|------|---------|
| `alfred.a` | Index file - contains offset table mapping |
| `alfred.1` - `alfred.b` | 12 numbered data files |
| `alfred.7` | Room graphics (background blocks, palettes) |

### alfred.a Structure

Based on usage in `load_room_and_init_alfred`:

```
+0x00: Resource count
+0x04: Offset table entries
       Each entry:
         - Resource file number (which alfred.X)
         - Offset within that file
         - Compressed size
         - Decompressed size
         - Compression type (RLE or raw)
```

### Room Data Loading (from alfred.7)

Each room has an entry (104 bytes = 0x68) containing:
```c
room_entry = DAT_0004fd28 + room_number * 0x68;

// 8 background blocks per room
for (block = 0; block < 8; block++) {
    offset = *(room_entry + block * 8);
    size = *(room_entry + block * 8 + 4);

    file_seek(file_handle_alfred1, offset);
    file_read(buffer, size, file_handle_alfred1);

    // Decompress if needed (sizes 0x8000 or 0x6800 are uncompressed)
    if (size != 0x8000 && size != 0x6800) {
        decompress_rle_block(temp_buffer, output_buffer);
    }
}

// Palette at offset +0x30
palette_offset = *(room_entry + 0x30);
```

---

## Key Data Addresses Reference

### Dispatch Tables (All 6-byte entries unless noted)

| Address | Ghidra Label | Purpose |
|---------|--------------|---------|
| `0x00047bf0` | `HOTSPOT_ACTION_DISPATCH_TABLE` | Main hotspot click actions |
| `0x00047c10` | `TAKE_ACTION_DISPATCH_TABLE` | "Take" verb actions |
| `0x00047c18` | `PICK_UP_ACTION_DISPATCH_TABLE` | "Pick up" verb actions |
| `0x00047cbc` | (unnamed) | Additional action table |
| `0x00047d24` | `ROOM_SCRIPT_DISPATCH_TABLE` | Room-specific scripts |
| `0x00047e58` | `F8_ACTION_DISPATCH_TABLE` | F8 text action codes |
| `0x00048118` | `ITEM_COMBINATION_TABLE` | "Use X with Y" (8-byte entries) |
| `0x000484e4` | (unnamed) | Room initialization hooks |
| `0x000485bc` | `ROOM_PERIODIC_UPDATE_TABLE` | Per-frame room update functions |
| `0x000486a4` | (unnamed) | Room animation hooks |

### State Variables

| Address | Ghidra Label | Type | Purpose |
|---------|--------------|------|---------|
| `0x0004fba4` | `conversation_branch_state_array` | byte[rooms*4] | Conversation branch states |
| `0x0004fc94` | `inventory_item_ids` | uint16[] | Player's inventory items |
| `0x0004fba0` | (unnamed) | int16 | Currently selected inventory item (-1 = none) |
| `0x0004bc1c` | `RANDOM_REJECTION_TEXT_PTRS` | ptr32[16] | "Can't do that" text pointers |

### Text System

| Address | Purpose |
|---------|---------|
| `room_sprite_data_ptr + 0x3da` | Text pointer table (runtime, 4 bytes per entry) |
| `room_text_data_ptr` | Raw text data loaded from ALFRED.X |
| `0x00042de5` - `0x00042exx` | Rejection text strings |

### Sprite/Room Data Offsets (relative to `room_sprite_data_ptr`)

| Offset | Size | Purpose |
|--------|------|---------|
| +0x05 | 1 byte | Sprite count (+2 for system sprites) |
| +0x1be | 1 byte | Exit count |
| +0x1bf | 14×exits | Exit data array |
| +0x217 | 1 byte | Scaling mode flag |
| +0x218 | 2 bytes | Alfred start X |
| +0x21a | 2 bytes | Alfred start Y |
| +0x3da | 4×texts | Text pointer table |
| +0x47a | 1 byte | Hotspot count |
| +0x47b | 9×hotspots | Hotspot data array |

### Per-Sprite Structure (44 bytes = 0x2C per sprite)

| Offset | Size | Purpose |
|--------|------|---------|
| +0x06 | 4 bytes | Pointer to graphic data |
| +0x0a | 2 bytes | X coordinate |
| +0x0c | 2 bytes | Y coordinate |
| +0x0e | 1 byte | Width |
| +0x0f | 1 byte | Height |
| +0x10 | 2 bytes | Stride (bytes per row) |
| +0x12 | 1 byte | Animation sequence count |
| +0x13 | 1 byte | Current sequence index |
| +0x14 | seq bytes | Frames per sequence |
| +0x18 | seq bytes | Loop count per sequence (0xFF = no loop) |
| +0x20 | 1 byte | Current frame index |
| +0x21 | 1 byte | Z-depth (0xFF = disabled) |
| +0x22 | 2×frames | Movement flags per frame |
| +0x2a | 2 bytes | Extra ID (dispatch table lookup) |
| +0x2c | 1 byte | Action flags |
| +0x2d | 1 byte | Frame delay counter |
| +0x31 | 1 byte | Disable after animation flag |

### Text Control Characters

| Byte | Meaning |
|------|---------|
| `0xFD` (-3) | End of text |
| `0xFE` (-2) | Conditional text (conversation branch) |
| `0xF8` (-8) | Action trigger (followed by uint16 action ID) |
| `0xF7` (-9) | Branch point marker |
| `0xF6` (-10) | Line break |
| `0xF5` (-11) | End of all text data |
| `0xF4` (-12) | Alternative end marker |
| `0xF0` (-16) | Control code |
| `0xFF` | Standard text marker |

---

## Summary

### Action System
- **Multi-tier dispatch** based on room flags and hotspot IDs
- **Multiple dispatch tables**: simple hotspots, room scripts, item combinations, F8 actions
- Actions map to function pointers in these tables
- Each table uses 6-byte entries: `[uint16 id, ptr32 function]`

### Text Responses
- **All text loaded from ALFRED.X files** - NOT hardcoded in EXE
- Text pointer table built at runtime (room_sprite_data_ptr + 0x3da)
- Voice files named `VOCxxxxx.WAV` with IDs embedded in text data
- Control characters: 0xFF (standard), 0xFE (conditional), 0xF8 (action), 0xFD (end)

### Random Rejection Messages
- **16 text pointers** at `0x0004bc1c`
- Selected via `random() & 0xf` for variety
- All semantically equivalent "can't do that" phrases

### F8 Action Codes
- Trigger special actions embedded in text data
- Format: `[0xF8][action_id_low][action_id_high]`
- Dispatch table at `0x00047e58`

### In-Memory State Storage
- **Conversation state**: `0x0004fba4` (4 bytes × rooms)
- **Inventory**: `0x0004fc94` (uint16 array)
- **Sprite visibility**: Z-depth at sprite+0x21 (0xFF = disabled)
- **Exit enable**: Flag at room_sprite_data_ptr + 0x1bf + exit_id × 0x0E + 0x02
- **Hotspot state**: At room_sprite_data_ptr + 0x47b + hotspot_id × 9

### alfred.a
- **Resource index/archive** for all game data
- Works with alfred.1-b numbered files
- Contains offset table for resource loading
- Room data in 104-byte entries (8 blocks + palette)

---

## Ghidra Labels Renamed During Analysis

The following data labels were renamed in Ghidra for clarity:

| Address | New Name |
|---------|----------|
| `0x0004bc1c` | `RANDOM_REJECTION_TEXT_PTRS` |
| `0x0004fba4` | `conversation_branch_state_array` |
| `0x0004fc94` | `inventory_item_ids` |
| `0x00047bf0` | `HOTSPOT_ACTION_DISPATCH_TABLE` |
| `0x00047c10` | `TAKE_ACTION_DISPATCH_TABLE` |
| `0x00047c18` | `PICK_UP_ACTION_DISPATCH_TABLE` |
| `0x00047d24` | `ROOM_SCRIPT_DISPATCH_TABLE` |
| `0x00047e58` | `F8_ACTION_DISPATCH_TABLE` |
