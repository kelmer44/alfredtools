# Hotspot Action Mapping System

## Summary
The game uses the **"extra" field** (offset +6 in the hotspot structure) to map hotspots to their hardcoded actions through a dispatch table.

## Key Findings

### Hotspot Structure (9 bytes per entry)

Located in room data starting at `room_sprite_data_ptr + 0x47a` (count) and `0x47d` (data):

```
Offset +0 (0x47d): X position      (2 bytes)
Offset +2 (0x47f): Y position      (2 bytes)
Offset +4 (0x481): Width           (1 byte)
Offset +5 (0x482): Height          (1 byte)
Offset +6 (0x483): EXTRA/ID field  (2 bytes) ⭐ THIS IS THE KEY!
Offset -1 (0x47c): Flags           (1 byte)
```

### How It Works

1. **Mouse Click Detection** (`check_mouse_on_sprites_and_hotspots` @ 0x00019879)
   - When the mouse is over a hotspot, the game reads the **extra field** at offset 0x483
   - This value is stored in `hotspot_id_or_data` (global @ 0x00051760)

2. **Action Dispatch** (`execute_hotspot_script_table` @ 0x00019041)
   - Searches through the **hotspot action dispatch table** at address `0x00047bf0`
   - Table structure: 6 bytes per entry
     - Bytes 0-1: Hotspot extra ID to match (2 bytes)
     - Bytes 2-5: Function pointer to execute (4 bytes)
   - Loops through entries comparing the extra ID until a match is found
   - Calls the corresponding function when matched

3. **Table Lookup Code** (simplified from disassembly @ 0x19082):
```assembly
MOV BX, word ptr [EAX + 0x47bf0]  ; Load extra ID from table
CMP EBX, 0xffff                    ; Check for end of table marker
JZ end
CMP BX, word ptr [0x00051760]      ; Compare with current hotspot extra
JNZ next_entry
CALL dword ptr [EAX + 0x47bf2]     ; Call the action function
```

## Example: Room 0 Drawer

**Hotspot Data:**
- Position: x=102, y=243
- Extra field: **261** (0x0105)
- Type: 3

**What happens:**
1. Player clicks on drawer hotspot
2. Game reads extra=261 from hotspot structure
3. Searches dispatch table at 0x47bf0 for entry with ID=261
4. Finds matching entry and calls the associated function
5. That function places **pegatina #91** into the scene

## Relevant Functions

| Address | Name | Purpose |
|---------|------|---------|
| 0x00019879 | `check_mouse_on_sprites_and_hotspots` | Detects mouse over hotspot, reads extra field |
| 0x00019041 | `execute_hotspot_script_table` | Searches dispatch table by extra ID |
| 0x00018562 | `room_specific_action_dispatcher` | Routes actions based on flags |
| 0x00017aaa | `handle_hotspot_action` | Handles pathfinding and action setup |

## Relevant Data

| Address | Name | Description |
|---------|------|-------------|
| 0x00047bf0 | `hotspot_action_dispatch_table` | Table mapping extra IDs to functions |
| 0x00051760 | `current_hotspot_extra_id` | Currently selected hotspot's extra field |

## Ghidra Annotations Added

1. Renamed `DAT_00047bf0` → `hotspot_action_dispatch_table`
2. Renamed `DAT_00051760` → `current_hotspot_extra_id`
3. Added comments at:
   - 0x19082: Table structure documentation
   - 0x19095: Comparison logic explanation

## Next Steps

To find what action is executed for a specific hotspot:
1. Identify the hotspot's **extra** field value
2. Search the dispatch table at 0x47bf0 for that value
3. Extract the function pointer from the matching entry
4. Decompile that function to understand the action

To map all hotspot actions:
1. Dump the entire dispatch table from 0x47bf0 (entries until 0xFFFF marker)
2. Extract each [extra_id, function_ptr] pair
3. Decompile each function to document what it does
