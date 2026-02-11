# Brick + Window Combination Analysis

## Summary

When using the brick (inventory item 4) on the window (hotspot extra 294) in room 3:

### Exact Binary Behavior (handler at Ghidra 0x2284B)

#### Phase 1: Alfred Throwing Animation (4 frames)
- Character overlay sprite at fixed position **(71, 110)**
- Sprite data pointer starts at `[g_4FAD0]` (runtime-allocated animation buffer)
- Advances **7810 bytes (0x1E82)** per frame through animation data
- `[g_4F938]` decremented by 8 each frame (height offset)
- `[g_4F93F]` set to 0 (character overlay flag)
- Each frame: `process_game_state()` → `setup_alfred_frame_from_state()` → `render_scene()`

#### Phase 2: Brick Projectile Flight
- Uses **room sprite entry 9** in room buffer (`room_sprite_data_ptr + 9 * 0x2C`)
  - +0x0A = X position, +0x0C = Y position, +0x1C = enabled, +0x21 = z_depth
- **Start position**: X = **420** (0x1A4), Y = **241** (0xF1) — FIXED values, not relative to Alfred
- **Z-depth**: **10** (0x0A) — visible during flight
- **Movement**: Y decreases by **10** per `render_scene()` frame
- **Stop condition**: Y ≤ **70** (0x46)
- **Total frames**: ~18 frames (Y goes 241→231→...→71→61, exit when checking 61≤70)
- On exit: z_depth set to **0xFF** (-1) to hide sprite

#### Phase 3: Broken Window Sticker
- `load_sticker_offset_table_from_alfred2(0x8529, 0xD9B)` — sticker data from ALFRED.2
- Parameters from 7-byte state record at 0x4982B

#### Phase 4: Sound Effect (Breaking Glass)
- `play_ambient_sound(sound_handle, -1, 256, 256, 32, sound_data, sound_type)`
- Sound parameters read from globals at 0x53002, 0x5323C, 0x53204

#### Phase 5: State Persistence
- Three sticker state flags set to 1: `[0x49824]`, `[0x4982B]`, `[0x49832]`
- Two sticker entries (9 bytes each) written to ALFRED.1 at room offsets 0x4A1 and 0x4AA
- Both sticker coordinates: (640, 400)

#### Phase 6: NPC Dialog
- Text 1: "¡¡ QUE HA SIDO ESO !!" at position **(25, 340)** via `display_npc_text_at_position`
- Text 2: "¡¡ QUIEN ANDA AHI !!" at position **(58, 340)** via `display_npc_text_at_position`
- Text 3: "Yo me voy" via `display_text_with_voice`
- Text pointers from NPC dialog table: `[0x4B9E8]`, `[0x4B9EC]`, `[0x4B9F0]`

#### Phase 7: Cleanup
- `remove_inventory_item(4)` — remove brick
- Walk destination: **(630, 368)** via `[g_4FB9C]`, `[g_4FB9E]`
- Jump to common walk handler at 0x10D31

### ScummVM vs Binary Comparison
| Parameter | Binary (ground truth) | ScummVM (observation) | Match? |
|---|---|---|---|
| Brick start X | **420** (fixed) | `_alfredState.x - w/2` | **WRONG** |
| Brick start Y | **241** (fixed) | `_alfredState.y - kAlfredFrameHeight` | **WRONG** |
| Y step per frame | **-10** | **-40** per tick | **WRONG** |
| Target Y | **≤ 70** (fixed) | `hotspot.y + h/2` | **WRONG** |
| Sprite entry | **room buffer entry 9** (offset 0x18C) | `findSpriteByIndex(7)` | **WRONG** |
| Z-order | **10** | `20` | **WRONG** |
| Walk dest X | **630** | **639** | **WRONG** |
| Walk dest Y | **368** | `_alfredState.y` | **WRONG** |
| NPC text 1 pos | **(25, 340)** | `(639, y+22)` | **WRONG** |
| NPC text 2 pos | **(58, 340)** | `(639, y+22+fontH)` | **WRONG** |

## Original Code Analysis

### Memory Mapping (verified)
- Code segment: memory 0x10000+ → file offset 0x14200+ (formula: file = mem + 0x4200)
- Data segment: memory 0x40000+ → file offset 0x43200+ (formula: file = mem + 0x3200)

### Dispatch Table Entry
- Located at: memory 0x48118 (file 0x4B318)  
- Entry format: 8 bytes (item1:2, item2:2, func_ptr:4)
- Entry 1: item1=0x0126 (294=window), item2=0x0004 (4=brick), func_ptr=0x0001284B
- **Pointer fixup**: ghidra_addr = 0x1284B + 0x10000 = **0x2284B** ✓

### Dispatcher Function
The item combination table is processed by `execute_complex_item_script_table` at 0x191E9:
```c
// At 0x192FB: CALL dword ptr [EAX*0x8 + 0x4811c]
// This calls the function pointer from the table (after +0x10000 fixup)
```

### Handler Function: 0x2284B
- **Size**: 684 bytes, 136 instructions
- **Valid Watcom C prologue**: PUSH 0x30; CALL __STK (48 bytes stack frame)
- **Capstone disassembly**: See combo_handler_analysis_v2.txt line 163

### Dialog Text Locations (file offsets in ALFRED.1)
- 0x443A0: "¡¡ QUE HA SIDO ESO !!" (prefix: FD 00 08 07)
- 0x443BF: "¡¡ QUIEN ANDA AHI !!" (prefix: FD 00 08 07)
- 0x443DD: "Yo me voy" (prefix: FD 00 08 0D)
- Text pointers in data segment: 0x4B9E8, 0x4B9EC, 0x4B9F0

### Sticker 11
- Located in ALFRED.2 at offset 0xD9B (3483)
- Source parameter: 0x8529 (34089)
- Sticker state record at 0x4982B: [flag(1), src=0x8529(2), pad=0x0000(2), offset=0x0D9B(2)]
- Room 3 palette (tablapaletas[11] = 3)
- This is the "broken window" graphic that replaces the intact window

### Room Sprite Entry 9 (Brick Projectile)
- Located at `room_sprite_data_ptr + 0x18C` (entry 9 × 0x2C bytes)
- Field +0x0A (abs 0x196): X position (int16)
- Field +0x0C (abs 0x198): Y position (int16)
- Field +0x1C (abs 0x1A8): enabled flag (byte)
- Field +0x21 (abs 0x1AD): z_depth (int8, -1=hidden, 10=visible)

### Dispatch Table Entry
```cpp
// In combinationTable[]:
{4, 294, &PelrockEngine::useBrickWithWindow},  // Brick + Window
```

### Related Files
- `engines/pelrock/actions.cpp` - Implementation
- `engines/pelrock/pelrock.h` - Declaration (line 259)
- `engines/pelrock/actions.h` - CombinationEntry struct
- `alfredtools/combo_handler_analysis_v2.txt` - Full disassembly (line 163)
- `alfredtools/ITEM_COMBINATION_COMPLETE_REFERENCE.md` - Complete reference

## TODO Items
1. [x] Find/verify handler address via pointer fixup (+0x10000)
2. [x] Extract exact throwing animation parameters
3. [x] Extract exact brick projectile movement values
4. [x] Identify sprite structure layout (room_buf + entry*0x2C)
5. [ ] Fix ScummVM brick start position (420, 241 fixed, not relative to Alfred)
6. [ ] Fix ScummVM brick speed (-10/frame, not -40/tick)
7. [ ] Fix ScummVM target Y (≤70 fixed, not hotspot-relative)
8. [ ] Fix ScummVM sprite index (room entry 9, not global index 7)
9. [ ] Fix ScummVM NPC text positions ((25,340) and (58,340))
10. [ ] Fix ScummVM walk destination (630, 368)
11. [ ] Implement NPC walk-off animation after dialog
