# Items 95 and 96 Investigation - Complete Analysis

## Overview

This document analyzes inventory items 95 (CD Player/Soundtrack) and 96 (Background Book) in Alfred Pelrock, including how they are added to inventory and what happens when used on Alfred.

## Item Descriptions

| Item ID | Spanish Name | English Translation |
|---------|--------------|---------------------|
| 95 | Banda sonora de Alfred Pelrock | Soundtrack of Alfred Pelrock |
| 96 | Un album con las pantallas de Alfred Pelrock | An album with the screens of Alfred Pelrock |

These are **bonus/extras** items — item 95 opens a CD audio player screen, item 96 opens a background art gallery viewer.

## CRITICAL DISCOVERY: LE Fixup Offset +0x10000

### The Problem

Handler pointers stored in the data section of JUEGO.EXE (item combination table, F8 action table, etc.) are stored as **raw offsets relative to the code object start**. At runtime, the DOS4GW LE loader applies a **fixup of +0x10000** (the code segment linear base address) to these values.

### Evidence

| Table | Total Entries | Valid at raw addr | Valid at addr + 0x10000 |
|-------|:------------:|:-----------------:|:----------------------:|
| Item Combination Table | 46 | 10 (22%) | **46 (100%)** |
| F8 Action Table | 116 | 19 (16%) | **116 (100%)** |

Every handler after fixup starts with `68 xx 00 00 00 e8` (Watcom C function prologue: `PUSH stack_size; CALL __STK`).

### Why Ghidra Shows Wrong Values

Ghidra correctly applies fixups to code instructions (e.g., `CALL dword ptr [EAX + 0x4811c]` — raw displacement 0x811c + data base 0x40000 = 0x4811c). However, the handler **pointers stored in the data section** appear to have missed their fixup. The raw values in the file (e.g., 0x146f4) need +0x10000 to get the real runtime address (0x246f4).

### Formula

```
real_handler_address = table_stored_value + 0x10000
```

This applies to ALL handler pointer tables:
- Item combination table at 0x48118
- F8 action table at 0x47e58
- Hotspot action table at 0x47bf0
- Room-specific script table at 0x47d24
- Main game loop table at 0x485bc

## Item Combination Table Entries

The table at `0x48118` has 8-byte entries: `[item1:2, item2:2, handler_ptr:4]`.

| Entry | Item1 | Item2 | Raw Handler | **Real Handler** | Purpose |
|-------|-------|-------|-------------|-----------------|---------|
| 43 | 95 | 95 | 0x146f4 | **0x246f4** | CD Player Screen |
| 44 | 96 | 96 | 0x14ed7 | **0x24ed7** | Background Art Gallery |

## Handler 0x246f4 — CD Player / Soundtrack Screen

### Function Prologue
```
0x246f4: PUSH 0x20          ; allocate 32 bytes stack
0x246f9: CALL __STK         ; Watcom stack check
0x246fe: PUSH EBX..EBP      ; save 6 registers
```

### Function Flow

1. **Load base screen**: `MOV EAX, 14; CALL load_room_graphics_and_palette_dynamic` — loads "room 14" as the CD player background
2. **Render UI**: `CALL draw_cursor_to_screen` + `CALL render_menu_screen`
3. **Load CD controls graphic from ALFRED.7**:
   - `file_seek(ALFRED.7, 0x21CB68)` — offset 2,214,760 (CD player controls RLE)
   - `file_read(buffer, 0x3172)` — read 12,658 bytes
   - `decompress_rle_block(...)` — decompress and draw
4. **Load second graphic from ALFRED.7**:
   - `file_seek(ALFRED.7, 0x2207E8)` — offset 2,230,248
   - `file_read(buffer, 0x12)` — read 18 bytes (header)
   - `decompress_rle_block(...)` — decompress
5. **Display track info**: `room_number_to_ascii(...)`, `blit_image_to_screen(...)`
6. **Setup graphics**: `memcpy_wrapper(...)`, `init_graphics_or_mode(...)`, `blit_image_to_screen(...)`
7. **Render character**: `render_character_to_screen(...)`
8. **Main input loop**: `wait_or_process_input(...)` with song selection and playback control
9. **Audio playback**: `play_cd_audio_track(...)`, `fade_cd_audio(...)`
10. **Cleanup**: `init_or_stop_sound(...)`, `set_vga_mode(...)`, `set_vga_palette(...)`
11. **Return**: `JMP 0x13a65` — shared function epilogue

### ALFRED.7 Resources Used

| Offset | Size | Description |
|--------|------|-------------|
| 0x21CB68 (2,214,760) | 12,658 bytes | CD player controls RLE graphic |
| 0x2207E8 (2,230,248) | ~18+ bytes | Additional graphic data |

### Data Table at 0x48BE8

The CD screen graphics (8 RLE chunks) and palette are stored in a data table at Ghidra address 0x48BE8:
- CD Screen RLE chunks: offset 2,727,564 (0x299E8C) in ALFRED.7
- CD Palette: offset 2,833,276 (0x2B3B7C) in ALFRED.7

## Handler 0x24ED7 — Background Art Gallery

### Function Prologue
```
0x24ed7: PUSH 0x20          ; allocate 32 bytes stack
0x24edc: CALL __STK         ; Watcom stack check
0x24ee1: PUSH EBX..EBP      ; save registers
```

### Function Flow

1. **Load base pointers** from globals at [0x4FA60]
2. **Load background data from ALFRED.7**:
   - `file_seek(ALFRED.7, 0x22DF86)` — offset 2,285,446
   - `file_read(...)` — read data
   - `decompress_rle_block(...)` — decompress
3. **Load additional data**:
   - `file_seek(ALFRED.7, 0x30A6E0)` — offset 3,188,448
   - `file_read(...)` — read data
4. **Display setup**: `load_room_graphics_and_palette_dynamic(...)`, `render_menu_screen(...)`
5. **Blit screens**: `blit_image_to_screen(...)` (×2)
6. **Render character**: `render_character_to_screen(...)`
7. **Main input loop**: `wait_or_process_input(...)` — browse through backgrounds
8. **On exit**: `load_room_and_init_alfred(...)` — restore normal game state
9. **Return**: `JMP 0x249a4` — cleanup/epilogue shared with CD handler

### ALFRED.7 Resources Used

| Offset | Size | Description |
|--------|------|-------------|
| 0x22DF86 (2,285,446) | ? | Background gallery data |
| 0x30A6E0 (3,188,448) | ? | Additional background/palette data |

## How Items 95/96 Are Granted

### Item Grant Code Stubs

Located in the unanalyzed code region:

| Address | Bytes | Meaning |
|---------|-------|---------|
| 0x21B80 | `b8 5f000000 e9 cd250000` | `MOV EAX, 95; JMP process_inventory_action` |
| 0x21B94 | `b8 60000000 e9 b9250000` | `MOV EAX, 96; JMP process_inventory_action` |

Both jump to `process_inventory_action` at 0x24157 which adds the item to Alfred's inventory.

### Source: Room 22 Merchants

The CD (item 95) is given by merchants in room 22. Room 22 has F8 actions 330-351:

| Action | Real Handler | Description |
|--------|-------------|-------------|
| 349 (0x015D) | 0x21FC8 | Toggles conversation flag at [0x495F0], calls `update_conversation_state` |
| 350 (0x015E) | 0x21FFB | Toggles conversation flag (XOR 2), may trigger merchant giving CD |
| 351 (0x015F) | 0x2202F | Sets up conversation topics — calls `play_get_naked_easter_egg` 8+ times with data from [0x4BB80..0x4BB9C] |

The merchant conversation system uses F8 actions 330-351 to manage the dialog flow. When certain conversation conditions are met (flags at [0x495F0] reach value 3), the merchant gives the CD.

## Key Functions Referenced

| Address | Name | Role |
|---------|------|------|
| 0x1B4A3 | `load_room_graphics_and_palette_dynamic` | Load room background |
| 0x19DC8 | `draw_cursor_to_screen` | Render mouse cursor |
| 0x19F2A | `render_menu_screen` | Render menu overlay |
| 0x2A342 | `file_seek` | Seek in open file |
| 0x2A43E | `file_read` | Read from open file |
| 0x14B6A | `decompress_rle_block` | Decompress RLE data |
| 0x16B00 | `blit_image_to_screen` | Copy image to display |
| 0x28D32 | `play_cd_audio_track` | Start CD audio playback |
| 0x2942D | `fade_cd_audio` | Fade audio volume |
| 0x29037 | `init_or_stop_sound` | Stop audio playback |
| 0x28FD5 | `set_vga_mode` | Set VGA display mode |
| 0x244E8 | `set_vga_palette` | Update VGA palette |
| 0x2A258 | `wait_or_process_input` | Wait for user input |
| 0x15E4C | `render_scene` | Full scene render |
| 0x2A66B | `memcpy_wrapper` | Memory copy |
| 0x1A9CF | `render_character_to_screen` | Draw character sprite |
| 0x152F5 | `load_room_and_init_alfred` | Restore room and character |
| 0x13BD0 | `room_number_to_ascii` | Convert room number to text |
| 0x1B666 | `update_conversation_state` | Update dialog state machine |
| 0x24157 | `process_inventory_action` | Add item to inventory |

## Complete Handler Call Map

### CD Player (0x246f4)
```
__STK → save_regs
  → load_room_graphics_and_palette_dynamic(14)
  → draw_cursor_to_screen
  → render_menu_screen
  → compute_scroll_values
  → load_base_pointers
  → file_seek(ALFRED.7, 0x21CB68) → file_read(12658) → decompress_rle_block
  → file_seek(ALFRED.7, 0x2207E8) → file_read(18)   → decompress_rle_block
  → blit_image_to_screen
  → room_number_to_ascii (track display)
  → memcpy_wrapper → init_graphics_or_mode
  → blit_image_to_screen
  → render_character_to_screen
  LOOP:
    → wait_or_process_input (user navigation)
    → render_scene
    → play_cd_audio_track / fade_cd_audio
  END LOOP
  → init_or_stop_sound
  → set_vga_mode → set_vga_palette
  → JMP shared_epilogue
```

### Background Viewer (0x24ed7)
```
__STK → save_regs
  → load_base_pointers
  → file_seek(ALFRED.7, 0x22DF86) → file_read → decompress_rle_block
  → file_seek(ALFRED.7, 0x30A6E0) → file_read
  → load_room_graphics_and_palette_dynamic
  → draw_cursor_to_screen → render_menu_screen
  → blit_image_to_screen (×2)
  → render_character_to_screen
  LOOP:
    → wait_or_process_input
    → render_scene / load_room_and_init_alfred
  END LOOP
  → JMP shared_epilogue
```

## Unanalyzed Code Region

The region 0x1EC00–0x3E097 (with fixup: 0x2EC00–0x3E097) contains ALL the game's item combination handlers, F8 action handlers, room-specific scripts, and many other gameplay functions. Ghidra has NO function definitions for this entire region.

The region contains:
- 46 item combination handler functions
- 116 F8 action handler functions
- Item grant stubs (34 items)
- Room-specific script handlers
- Shared function epilogues (e.g., 0x13A65 → real 0x23A65)

All of these are proper Watcom C functions with `PUSH stack_size; CALL __STK` prologues but were never analyzed by Ghidra because they lack direct CALL/JMP references from analyzed code — they're only reached via indirect calls through data table function pointers.
