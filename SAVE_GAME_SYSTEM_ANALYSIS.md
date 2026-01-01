# Alfred Pelrock Save Game System Analysis

## Save File Structure

### File Location
- Path: `SALVAJOC.XXX` where XXX is 000-999 (save slot number)
- Files typically range from 9KB to 11.5KB depending on game progress

### Binary Structure

| Offset | Size | Description | Notes |
|--------|------|-------------|-------|
| 0x00-0x0F | 16 | Magic Header | ASCII "Tic-Tac-Toe 1995" |
| 0x10-0x25 | 22 | Save Name | User-defined, space-padded |
| 0x26 | 1 | Room Number | Current room (0-55) |
| 0x27 | 1 | Unknown | Usually 0x00 |
| 0x28-0x29 | 2 | Player X | Little-endian uint16 |
| 0x2A-0x2B | 2 | Player Y | Little-endian uint16 |
| 0x2C-0x33 | 8 | Unknown | Position-related? |
| 0x34-0xFF | ~204 | Game Flags | Sparse flag arrays |
| 0x100-0x25F0 | ~9KB | Game State | Core state data |
| 0x25F1+ | Variable | Walkbox Data | 9 bytes per walkbox |
| Variable | Variable | Additional State | Depends on progress |

### Walkbox Structure (9 bytes each, at offset 0x25F1)

```c
struct Walkbox {
    uint16_t x;      // +0: X position
    uint16_t y;      // +2: Y position
    uint16_t width;  // +4: Width
    uint16_t height; // +6: Height
    uint8_t flags;   // +8: Flags/type (usually 0)
};
```

Example from Room 14:
```
Walkbox 1: x=436, y=356, w=4,   h=14, flags=0  (B4 01 64 01 04 00 0E 00 00)
Walkbox 2: x=440, y=368, w=148, h=2,  flags=0  (B8 01 70 01 94 00 02 00 00)
```

## In-Game State Variables

### Core Memory Addresses (Virtual)

| Address | Name | Description |
|---------|------|-------------|
| 0x0004fb94 | current_room_number | Current room ID (byte) |
| 0x0004fba4 | conversation_branch_state_array | Conversation states (room*4 + slot) |
| 0x0004fc94 | inventory_item_ids | Array of item IDs in inventory |
| 0x0004fba0 | current_selected_item | Currently held inventory item (-1 if none) |
| 0x00038e38 | game_mode_or_chapter | Current chapter/game mode |

### Room Data Structure (in memory at room_sprite_data_ptr)

| Offset | Size | Description |
|--------|------|-------------|
| +0x05 | 1 | Sprite count |
| +0x06 | 44 each | Sprite headers |
| +0x1BE | 1 | Exit count |
| +0x1BF | 14 each | Exit array |
| +0x213 | 1 | Walkbox count |
| +0x218 | 9 each | Walkbox array |
| +0x47A | 1 | Hotspot count |
| +0x47C | 9 each | Hotspot array |
| +0x3DA | varies | Text pointer table |

## State That Needs Saving/Loading

### 1. Conversation States
- **Array**: `conversation_branch_state_array` at 0x0004fba4
- **Format**: `array[room_number * 4 + branch_slot]`
- **Purpose**: Tracks which conversation branches have been taken
- **Usage**: When value != 0, skip to alternate text branch

### 2. Hotspot Enable/Disable
- **Location**: `room_sprite_data_ptr + 0x47C + hotspot_id * 9 + 1`
- **Flag**: action_flags byte, high bit indicates enabled state
- **Triggered by**: F8 action codes in text data

### 3. Exit Enable/Disable
- **Location**: `room_sprite_data_ptr + 0x1BF + exit_id * 14 + 2`
- **Flag**: Byte at offset +0x02 in exit structure (0 = disabled, non-0 = enabled)

### 4. Walkbox Modifications (CRITICAL)
- **Count**: `room_sprite_data_ptr + 0x213`
- **Data**: `room_sprite_data_ptr + 0x218` (9 bytes each)
- **Room 14 Example**: Opens new walkboxes after certain actions
- **Save offset**: Fixed at 0x25F1 in save file

### 5. Sprite/Sticker Visibility
- **Pegatinas (stickers)**: Overlay sprites that can be shown/hidden
- **Triggered by**: Hotspot actions via dispatch table at 0x47bf0
- **Example**: Drawer in Room 0 (extra 261) places sticker #91

### 6. Inventory
- **Array**: `inventory_item_ids` at 0x0004fc94
- **Format**: Array of uint16 item IDs
- **Navigation**: 4 visible slots with scroll arrows

## Key Dispatch Tables

| Address | Purpose | Entry Size |
|---------|---------|------------|
| 0x00047bf0 | Hotspot action dispatch | 6 bytes (id:2 + func:4) |
| 0x00047e58 | F8 action dispatch | 6 bytes (id:2 + func:4) |
| 0x00048118 | Item combination table | Variable |
| 0x000484e4 | Room initialization | 6 bytes (room:2 + func:4) |
| 0x00048630 | Passing sprites (render_scene) | 6 bytes (room:2 + func:4) |
| 0x000486a4 | Palette cycling | 6 bytes (room:2 + config:4) |
| 0x000486fe | Menu slot actions | Variable |

## How State Changes Are Triggered

### F8 Action Codes
Found in text data, format: `F8 [id_low] [id_high]`
- Executed during text display/conversation
- Looks up action ID in F8_ACTION_DISPATCH_TABLE
- Actions include: enable/disable exits, show/hide stickers, update conversation state

### Hotspot Actions
- Player clicks hotspot → reads extra field (2 bytes at +0x06)
- Looks up in hotspot_action_dispatch_table at 0x47bf0
- Calls associated function to execute action

## ScummVM Implementation Notes

### Save/Load Functions to Implement

```cpp
class AlfredSaveManager {
    // Header
    static const char MAGIC[] = "Tic-Tac-Toe 1995";

    struct SaveHeader {
        char magic[16];
        char saveName[22];
        uint8 roomNumber;
        uint8 padding;
        uint16 playerX;
        uint16 playerY;
        // Additional fields...
    };

    // State arrays to save
    uint8 conversationStates[56 * 4];  // 224 bytes, one per room*4 slots
    uint16 inventoryItems[MAX_INVENTORY];

    // Per-room state
    struct RoomState {
        uint8 exitEnabled[MAX_EXITS];      // From offset 0x1BF + n*14 + 2
        uint8 hotspotEnabled[MAX_HOTSPOTS]; // From offset 0x47C + n*9 + 1
        uint8 walkboxCount;                 // From offset 0x213
        Walkbox walkboxes[MAX_WALKBOXES];   // From offset 0x218
        // Sticker visibility flags
    };
};
```

### Key Questions for Implementation

1. **Walkbox Persistence**: Are modified walkboxes saved per-room or globally?
   - Analysis shows: Fixed offset 0x25F1 suggests global storage

2. **State Size**: Why does file size vary (9KB-11.5KB)?
   - Likely: Additional progress-dependent data appended

3. **Magic String Location**: Where is "Tic-Tac-Toe 1995" stored?
   - Not in executable strings - likely in resource file or hardcoded in save function

4. **Save Slot UI**: How are slots selected?
   - Button coordinates: Save (132, 186, 81x34), Load (133, 222, 80x33)
   - Menu handler at ~0x12918 (needs verification)

## Files Involved

| File | Purpose |
|------|---------|
| JUEGO.EXE (alfred.x) | Main executable with all logic |
| SALVAJOC.XXX | Save game files |
| ALFRED.1-B | Resource files (room data, graphics) |
| PATH.DAT | Path configuration |

## Key Findings - Save/Load Implementation

### Save Filename Location
- **File Offset**: 0x43418 in JUEGO.EXE
- **String**: `salvajoc.xxx` (placeholder extension)
- **Context**: Found in filename table alongside ALFRED.* files
- **Header**: "Tic-Tac-Toe 1995" also hardcoded in executable

### File Operation Functions (DOS INT 21h wrappers)
- **FUN_0001c60a**: File read (INT 21h calls)
- **FUN_0001c6e1**: Buffer refill operation
- **FUN_0001c593**: File stream initialization
- **FUN_00014e37**: High-level file read function
- **set_state_flag @ 0x0001e512**: Sets file handle flags at DAT_000312e4

### Resource File Table
Located near 0x43418, contains in order:
```
alfred.3, alfred.4, alfred.5, alfred.6, alfred.7, alfred.8, alfred.9,
alfred.a, alfred.b, sound.cfg, salvajoc.xxx, kk.s3m, 1.s3m, 2.s3m...
```

## ALFRED.8 Default State System (VERIFIED)

### Overview
ALFRED.8 is a 649-byte file containing **default room state values** in a packed format. At game startup, the `apply_alfred8_room_defaults` function (VA 0x14a27) reads this file and patches the corresponding values into ALFRED.1.

### ALFRED.8 Format
```
[room:2 LE][offset:2 LE][type:1][data:varies]
...
Terminator: 0xFFFF (room) or 0xC9CA (alternate)
```

Type values:
- **0x01**: 1-byte value
- **0x04**: 4-byte value (two uint16 X,Y coordinates)
- **0x12**: 14-byte special data block

### Key Entries Found
| Room | Offset | Type | Value | Meaning |
|------|--------|------|-------|---------|
| 0 | 0x1c1 | byte | 0 | Exit disabled |
| 0 | 0x47d | 4byte | (191, 243) | Hotspot position |
| 14 | 0x213 | byte | 1 | Default walkbox count = 1 |
| 14 | 0x221 | 0x12 | ... | Walkbox modification data |
| 15 | 0x47d | 4byte | (414, 82) | Hotspot position |

### Hotspot Disable Pattern
Hotspots are disabled by setting their position to (640, 400) - offscreen. Several rooms have hotspots at these "disabled" coordinates in ALFRED.8.

### Function: apply_alfred8_room_defaults (VA 0x14a27)
Called during `load_dual_layer_data` (after "Actualizando ALFRED.1" message).
- Reads ALFRED.8 and ALFRED.9 into memory buffers
- Iterates through packed entries
- For each entry: seeks to room offset in ALFRED.1 and writes the data
- Uses `write_data_to_alfred1` function (VA 0x2a6b7) to perform the writes

## Save/Load Menu System

### Menu Button Table (VA 0x486f8)
Format: 10 bytes per entry - x:2, y:2, w:1, h:1, func_ptr:4

| Entry | Rect | Function | Purpose |
|-------|------|----------|---------|
| 0 | (140,115,60x60) | 0x12da7 | ? |
| 1 | (222,107,60x60) | 0x12e71 | ? |
| 2 | (304,99,60x60) | 0x12e87 | ? |
| 3 | (386,91,60x60) | 0x12e9d | ? |
| 4 | (132,188,75x23) | 0x132e4 | **SAVE** |
| 5 | (134,222,72x25) | 0x13002 | **LOAD** |
| 6 | (134,259,72x25) | 0x13c92 | ? |
| 7 | (134,294,70x25) | 0x12f3f | **QUIT?** |
| 8 | (217,293,32x32) | 0x141aa | ? |
| 9 | (468,88,22x32) | 0x12ee6 | ? |

### Conversation State Array
- Location: 0x4fba4 (224 bytes = 56 rooms × 4 slots)
- Indexed by: `room_number * 4 + branch_slot`
- Non-zero value = branch taken, affects text display in `load_room_and_init_alfred`

## Next Steps for Complete Analysis

1. Decompile save/load functions at 0x132e4 and 0x13002 (currently not recognized by Ghidra)

2. Map remaining F8 actions to state changes

3. Document full SALVAJOC.XXX format including all state sections

4. Test save/load cycle to verify state persistence
