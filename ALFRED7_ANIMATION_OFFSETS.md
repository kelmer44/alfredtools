# ALFRED.7 Animation Loading Analysis

## Overview

Analysis of how the Alfred Pelrock game executable (JUEGO.EXE) loads animations and resources from ALFRED.7.

**Key Finding: NO MASTER LOOKUP TABLE FOR ANIMATIONS**

The game uses **hardcoded byte offsets** in the executable to access most ALFRED.7 resources. There is no centralized BUDA index table that maps animation IDs to file offsets.

## Loading Patterns

### 1. Room Background Graphics - TABLE LOOKUP
The only resource type that uses a proper lookup table.

- **Table Location**: `0x488f4` in JUEGO.EXE
- **Table Size**: 0x36 (54) bytes per room × 56 rooms = 3,024 bytes
- **Structure per room**:
  - Bytes 0-47: 8 pairs of (u32 offset, u16 size) for background blocks
  - Bytes 48-53: Palette offset and metadata

**Code pattern** (from `load_room_graphics_and_palette_dynamic`):
```c
IMUL ECX, room_number, 0x36
MOV EDX, [ECX + 0x488f4]  // Load offset from table
file_seek(file_handle_alfred7, EDX)
```

### 2. Special Animations - HARDCODED OFFSETS
Most animations use immediate values in the code.

| Animation | Offset | Size | Function | Notes |
|-----------|--------|------|----------|-------|
| Idle comb hair (right) | 0x108C2 | 0x5596 | idle_action_handler | Room 0 variant |
| Idle comb hair (left) | 0x15958 | 0x5596 | idle_action_handler | Room 1 variant |
| Debug fight animation | 0x2207FA | 0x5B5E | play_fight_animation | Spacebar in debug mode |

### 3. UI Resources - HARDCODED OFFSETS

| Resource | Offset | Size | Function |
|----------|--------|------|----------|
| Large dialog font (12×24) | 0x7DC8 | 0x12C0 | load_fonts_and_graphics |
| Cursor - hotspot | 0xFDCDD | 0x120 | load_fonts_and_graphics |
| Cursor - default | 0xFDDFD | 0x120 | load_fonts_and_graphics |
| Cursor - exit | 0xFDF1D | 0x120 | load_fonts_and_graphics |
| Cursor - animation | 0xFE33D | 0x120 | load_fonts_and_graphics |
| Cursor - combination | 0x367EF0 | varies | load_fonts_and_graphics |
| RLE compressed data | 0xFE945 | varies | load_fonts_and_graphics |
| Action text table | 0x2137A8 | 0x6172 | load_fonts_and_graphics |

## File Handle

The file handle for ALFRED.7 is stored at:
- **Address**: `0x4f908` (named `file_handle_alfred7`)
- **Part of file handle array** starting at `0x4f8f0`:
  - +0x00: alfred.1
  - +0x04: alfred.2  
  - +0x08: alfred.3
  - +0x0C: alfred.4
  - +0x10: alfred.5
  - +0x14: alfred.6
  - +0x18: alfred.7 (0x4f908)
  - +0x1C: alfred.8
  - +0x20: alfred.9
  - +0x24: alfred.a
  - +0x28: alfred.b

## BUDA Markers

BUDA markers appear in ALFRED.7 as section delimiters between compressed data blocks:
- They are 4-byte markers (`"BUDA"`)
- They do NOT correspond to a lookup table
- The game ignores them during loading - it uses direct byte offsets

## Implications

1. **Adding new animations**: Would require patching the executable with new offsets
2. **Moving animations**: Would break hardcoded references
3. **BUDA numbers in file names**: Are for human reference only, not used by game logic
4. **Room backgrounds**: Only these use flexible table-based lookup

## Key Ghidra Labels Added

| Address | Name | Purpose |
|---------|------|---------|
| 0x4f908 | file_handle_alfred7 | File handle for ALFRED.7 |
| 0x488f4 | room_graphics_offset_table | Background graphics lookup table |
| 0x48924 | room_palette_offset_table | Palette offset by room |
| 0x485bc | room_script_dispatch_table | Room handler functions |
| 0x1be8d | idle_action_handler | Plays idle comb animation |
| 0x14ee3 | load_fonts_and_graphics | Loads UI resources |
| 0x26420 | play_fight_animation | Debug fight animation |

## Functions That Access ALFRED.7

From xrefs to file_handle_alfred7:
1. `main_menu_handler` - Menu graphics
2. `load_fonts_and_graphics` (15 refs) - Fonts, cursors, UI
3. `load_room_data` - Room background/palette
4. `load_room_graphics_and_palette_dynamic` - Dynamic room loading
5. `idle_action_handler` - Idle animations
6. `free_memory` - Cleanup
7. `play_fight_animation` - Debug mode fight
