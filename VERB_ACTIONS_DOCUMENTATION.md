# Verb Action System Documentation

## Overview

The game uses a verb-based interaction system where clicking a hotspot with a specific verb (PICKUP, OPEN, PULL, LOOK, etc.) dispatches to a handler function. The dispatcher is at Ghidra address `0x18562` (`room_specific_action_dispatcher`).

## Architecture

### Verb Code Mapping

| Verb Code | Verb | Dispatch Table | Table Address (mem) | Entries |
|-----------|------|----------------|---------------------|---------|
| 0x01 | PICKUP | `execute_room_specific_script` | 0x47D24 | 48 |
| 0x02 | TALK | `handle_conversation_tree` | (direct) | - |
| 0x08 | CLOSE | `handle_dialog_interaction` | (direct) | - |
| 0x10 | LOOK | `dispatch_hotspot_action_by_extra_id` | 0x47BF0 | 4 |
| 0x20 | PUSH | `execute_script_table_0x47c10` | 0x47C10 | 0 |
| 0x40 | OPEN | `execute_script_table_0x47c18` | 0x47C18 | 26 |
| 0x80 | PULL | `execute_script_table_0x47cbc` | 0x47CBC | 16 |
| 0x200 | ITEM | `execute_complex_item_script_table` | (combinations) | 98 tables |

### Dispatch Table Format

Each dispatch table is an array of 6-byte entries terminated by `0xFFFF`:

```c
struct DispatchEntry {
    uint16 extra_id;         // +0x00: Hotspot extra ID to match
    uint32 function_ptr;     // +0x02: Handler function pointer (needs +0x10000 fixup for entries 0-33)
};
// Terminated by uint16 = 0xFFFF
```

### Address Mapping (LE Executable)

| Object | Purpose | Base Address | File Offset Start | Delta (ghidra = file - delta) |
|--------|---------|-------------|-------------------|-------------------------------|
| 1 | Code | 0x10000 | 0x14200 | 0x4200 |
| 2 | Data | 0x40000 | 0x43200 | 0x3200 |

**Unfixed function pointers** (entries 0-33 in PICKUP table): add `0x10000` (Object 1 base).
**Already-fixed pointers** (entries 34+): already include `0x10000` base.

Data addresses in unfixed code regions: add `0x40000` (Object 2 base).

### Static Hotspot Structure (9 bytes)

```c
struct StaticHotspot {
    u8  type;       // +0x00: Hotspot type/flags
    u16 x;          // +0x01-0x02: X position (LE)
    u16 y;          // +0x03-0x04: Y position (LE)
    u8  width;      // +0x05: Width in pixels
    u8  height;     // +0x06: Height in pixels
    u16 extra;      // +0x07-0x08: Extra ID (LE)
};
```

**Location:** `room_data + 0x47C`, count at `room_data + 0x47A` (1 byte).

### Common Patterns in Handlers

1. **Show hotspot**: Set `[room_data_ptr + hotspot_offset + 1] = X`, `[room_data_ptr + hotspot_offset + 3] = Y` to on-screen coordinates
2. **Hide hotspot**: Set X=640, Y=400 (off-screen coordinates)
3. **Persist state**: Write hotspot data to state buffer at `0x4FB78` and call `write_data_to_alfred1` (0x2A6B7)
4. **Set flag**: Write 1 to a game state byte (e.g., `[0x495CB]` = FLAG_CROCODILLO_ENCENDIDO)
5. **Display sticker**: Call `load_and_render_sticker_from_alfred6` (0x1BA45) with ALFRED.6 offset and size
6. **Palette fade**: Allocate 768-byte buffer, seek/read palette from ALFRED.7, call fade function, copy to active palette

### Key Global Variables (Data Segment, +0x40000 fixup)

| Address | Name | Description |
|---------|------|-------------|
| 0x4FAC8 | `room_data_ptr` | Pointer to current room's Pair 10 data |
| 0x4FAB8 | `palette_buffer_ptr` | Pointer to current active palette |
| 0x4FB94 | `current_room_id` | Current room number (uint16) |
| 0x4FB78 | `hotspot_state_buffer` | Temp buffer for hotspot state writes (9 bytes) |
| 0x4FB70 | `flag_state_buffer` | Temp buffer for flag state writes (6 bytes) |
| 0x4F908 | `file_handle_alfred7` | File handle for ALFRED.7 |
| 0x4F914 | `file_handle_alfred1_write` | File handle for ALFRED.1 (write) |
| 0x4F8F0 | `file_handle_alfred1_seek` | File handle for ALFRED.1 (seek) |
| 0x4FAAC | `room_struct_ptr` | Pointer to room metadata structure |

### Key Functions

| Address | Name | Parameters |
|---------|------|------------|
| 0x2A342 | `file_seek` | EAX=file_handle, EDX=offset, EBX=whence |
| 0x2A43E | `file_read` | EAX=buffer, EDX=size, ECX=file_handle, EBX=count |
| 0x2A6B7 | `write_data_to_alfred1` | EAX=buffer, EDX=size, ECX=file_handle, EBX=count |
| 0x2A66B | `memcpy_wrapper` | EAX=dst, EDX=src, EBX=size |
| 0x25E90 | `allocate_memory` | EAX=size → returns EAX=ptr |
| 0x2A60D | `free_memory` | EAX=ptr |
| 0x1BA45 | `load_and_render_sticker_from_alfred6` | EAX=offset, EDX=size |
| 0x1BD53 | `fade_palette_to_target` | EAX=dst, EDX=src, EBX=ncolors, ECX=map, stack=mode |

---

## State Persistence Pattern

When a handler modifies hotspot positions or flags, it persists the changes in two ways:

### 1. Hotspot Position Persistence (9-byte buffer at 0x4FB78)

```
[0x4FB78] = current_room_id (uint16)
[0x4FB7A] = hotspot_data_offset (uint16) - offset within room data
[0x4FB7C] = data_size (uint8) - always 4 for position data
[0x4FB7D] = new_X (uint16)
[0x4FB7F] = new_Y (uint16)
```

Then: `write_data_to_alfred1(buffer=0x4FB78, size=9, file=alfred1_write, count=1)`

Followed by: seek to `room_struct[0x50] + hotspot_offset` in ALFRED.1, then write 4 bytes (X,Y) from `room_data + offset`.

### 2. Flag Persistence (6-byte buffer at 0x4FB70)

```
[0x4FB70] = current_room_id (uint16)
[0x4FB72] = flag_offset (uint16) - offset within room data
[0x4FB74] = data_size (uint8) - 1 for byte flags
[0x4FB75] = flag_value (uint8)
```

Then: `write_data_to_alfred1(buffer=0x4FB70, size=6, file=alfred1_write, count=1)`

---

## Complete Verb Dispatch Tables

### LOOK Table (4 entries at 0x47BF0)

| # | Extra | Ghidra Addr | Notes |
|---|-------|-------------|-------|
| 0 | 435 | 0x1C065 | |
| 1 | 436 | 0x1C098 | |
| 2 | 437 | 0x1C0CB | |
| 3 | 438 | 0x1C0FE | |

### OPEN Table (26 entries at 0x47C18)

| # | Extra | Ghidra Addr | Notes |
|---|-------|-------------|-------|
| 0 | 261 | 0x1C25A | |
| 1 | 268 | 0x1C339 | |
| 2 | 263 | 0x1C423 | |
| 3 | 277 | 0x1C437 | |
| 4 | 282 | 0x1C44B | |
| 5 | 290 | 0x1C535 | |
| 6 | 288 | 0x1C632 | |
| 7 | 315 | 0x1C789 | |
| 8 | 312 | 0x1C7B5 | |
| 9 | 355 | 0x1C8E3 | |
| 10 | 9 | 0x1C9D5 | |
| 11 | 363 | 0x1C9E9 | |
| 12 | 370 | 0x1CAD3 | |
| 13 | 374 | 0x1CBBD | |
| 14 | 375 | 0x1CCA7 | |
| 15 | 388 | 0x1CD06 | |
| 16 | 393 | 0x1CDF0 | |
| 17 | 400 | 0x1CEDA | |
| 18 | 434 | 0x1CFD1 | |
| 19 | 462 | 0x1D0BB | |
| 20 | 465 | 0x1D17C | |
| 21 | 473 | 0x1D266 | Room 28: hide hotspot after opening |
| 22 | 613 | 0x1D31C | |
| 23 | 621 | 0x1D330 | |
| 24 | 651 | 0x1D41A | |
| 25 | 800 | 0x1D54D | |

### PULL Table (16 entries at 0x47CBC)

| # | Extra | Ghidra Addr | Notes |
|---|-------|-------------|-------|
| 0 | 261 | 0x1D638 | |
| 1 | 268 | 0x1D671 | |
| 2 | 282 | 0x1D75D | |
| 3 | 290 | 0x1D849 | |
| 4 | 312 | 0x1D935 | |
| 5 | 355 | 0x1DA21 | |
| 6 | 363 | 0x1DB0D | |
| 7 | 370 | 0x1DBF9 | |
| 8 | 374 | 0x1DCE5 | |
| 9 | 388 | 0x1DDD1 | |
| 10 | 393 | 0x1DEBD | |
| 11 | 400 | 0x1DFA9 | |
| 12 | 434 | 0x1E095 | |
| 13 | 465 | 0x1E181 | |
| 14 | 621 | 0x1E26D | |
| 15 | 800 | 0x1E359 | |

### PICKUP Table (48 entries at 0x47D24)

| # | Extra | Ghidra Addr | Notes |
|---|-------|-------------|-------|
| 0 | 0 | 0x1E444 | |
| 1 | 1 | 0x1E4FA | |
| 2 | 2 | 0x1E59A | |
| 3 | 3 | 0x1E63A | |
| 4 | 4 | 0x1E757 | |
| 5 | 273 | 0x1E81B | |
| 6 | 283 | 0x1E82F | |
| 7 | 284 | 0x1E82F | Shares handler with 283 |
| 8 | 316 | 0x1E843 | |
| 9 | 310 | 0x1EB8A | |
| 10 | 311 | 0x1EB8A | Shares handler with 310 |
| 11 | 357 | 0x1EB9E | |
| 12 | 360 | 0x1EC30 | |
| 13 | 361 | 0x1EC44 | |
| 14 | 362 | 0x1EC57 | |
| 15 | 60 | 0x1EE31 | |
| 16 | 62 | 0x1EEE7 | |
| 17 | 61 | 0x1EF81 | |
| 18 | 65 | 0x1F01B | |
| 19 | 66 | 0x1F111 | |
| 20 | 67 | 0x1F207 | |
| 21 | 68 | 0x1F2FD | |
| 22 | 69 | 0x1F3F3 | |
| 23 | 70 | 0x1F573 | |
| 24 | 71 | 0x1F669 | |
| 25 | 72 | 0x1F75F | |
| 26 | 73 | 0x1F855 | |
| 27 | 74 | 0x1F94B | |
| 28 | 6 | 0x1FA41 | |
| 29 | 7 | 0x1FB37 | |
| 30 | 81 | 0x1FC2D | |
| 31 | 100 | 0x1FCEB | |
| 32 | 609 | 0x1FD8B | |
| 33 | **472** | **0x1FED8** | **Room 28: Matches pickup** (analyzed below) |
| 34 | 87 | 0x2030C | Room 28: lit-room item 1 |
| 35 | 88 | 0x2032F | Room 28: lit-room item 2 |
| 36 | 89 | 0x20357 | Room 28: lit-room item 3 |
| 37 | 90 | 0x2044F | |
| 38 | 605 | 0x204CC | |
| 39 | 606 | 0x204CC | Shares handler with 605 |
| 40 | 607 | 0x204CC | Shares handler with 605 |
| 41 | 608 | 0x20528 | |
| 42 | 628 | 0x20566 | |
| 43 | 99 | 0x205FE | |
| 44 | 101 | 0x20682 | |
| 45 | 112 | 0x2037A | Room 28: lit-room item 4 |
| 46 | 700 | 0x20781 | |
| 47 | 308 | 0x20C17 | |

---

## Detailed Handler Analysis

### Room 28: PICKUP Extra 472 — "Pick Up Matches"

**Handler address:** Ghidra 0x1FED8 (file 0x240D8), 1399 bytes
**Ends with:** `JMP 0x14A1B` (jumps into `free_memory(palette_buffer); return`)

#### Room 28 Default Hotspot Data

| Index | Offset | Type | X | Y | W | H | Extra | Default State |
|-------|--------|------|---|---|---|---|-------|---------------|
| 0 | 0x47C | 0x08 | 640 | 400 | 52 | 24 | 87 | Hidden (off-screen) |
| 1 | 0x485 | 0x08 | 640 | 400 | 18 | 19 | 88 | Hidden (off-screen) |
| 2 | 0x48E | 0x08 | 640 | 400 | 31 | 34 | 89 | Hidden (off-screen) |
| 3 | 0x497 | 0x08 | 312 | 234 | 22 | 10 | 472 | **Visible (THE MATCHES)** |
| 4 | 0x4A0 | 0x08 | 640 | 400 | 17 | 13 | 112 | Hidden (off-screen) |

#### Handler Operations (in order)

1. **Play ambient sound** (0x1FEEF-0x1FF0B)
   - Calls `play_ambient_sound` (0x27CE1) with params from [0x53204], [0x53234]
   - Parameters: slot=-1, size=256, count=256, flags=0x20

2. **Load alternate palette from ALFRED.7** (0x1FF10-0x1FF68)
   - Allocate 768-byte (0x300) temporary buffer
   - Seek to offset **0x1610CE** in ALFRED.7
   - Read 768 bytes (256 colors × 3 bytes RGB, 6-bit VGA values)
   - Call `fade_palette_to_target` (0x1BD53): smooth palette transition
   - Call `memcpy_wrapper` (0x2A66B): copy new palette to active palette buffer
   - **Effect:** Room "lights up" — dark room becomes visible

3. **Set game flag** (0x1FF6D)
   - `[0x495CB] = 1` → FLAG_CROCODILLO_ENCENDIDO
   - **Effect:** Game remembers the room has been lit

4. **Show hotspot[0] / extra 87** (0x1FF74-0x2000C)
   - Move from (640, 400) → **(415, 171)** — now clickable
   - Persist position to ALFRED.1 state file

5. **Show hotspot[1] / extra 88** (0x20016-0x200A9)
   - Move from (640, 400) → **(305, 217)** — now clickable
   - Persist position to ALFRED.1

6. **Show hotspot[2] / extra 89** (0x200AE-0x20146)
   - Move from (640, 400) → **(201, 239)** — now clickable
   - Persist position to ALFRED.1

7. **Show hotspot[4] / extra 112** (0x2014B-0x201E4)
   - Move from (640, 400) → **(261, 259)** — now clickable
   - Persist position to ALFRED.1

8. **Hide hotspot[3] / extra 472** (0x201E9-0x20282)
   - Move from (312, 234) → **(640, 400)** — removed from screen (matches consumed)
   - Persist position to ALFRED.1

9. **Set room state** (0x20287-0x20302)
   - `room_data[0xA5] = 2` — room state flag (was 0xFF default)
   - Persist via 6-byte flag buffer to ALFRED.1

10. **Cleanup** (0x20307)
    - `JMP 0x14A1B` → `free_memory(palette_buffer)` → return

#### Visual Summary

```
BEFORE (dark room):
  Hotspot 472 (matches) visible at (312, 234)
  Hotspots 87, 88, 89, 112 hidden at (640, 400)

PICKUP matches →
  Palette fades from dark to lit
  Sound effect plays

AFTER (lit room):
  Hotspot 472 (matches) hidden at (640, 400) — consumed
  Hotspot 87 visible at (415, 171)
  Hotspot 88 visible at (305, 217)
  Hotspot 89 visible at (201, 239)
  Hotspot 112 visible at (261, 259)
  FLAG_CROCODILLO_ENCENDIDO = 1
  room_data[0xA5] = 2
```

---

### Room 28: PICKUP Extra 87 — "Pick Up Item in Lit Room"

**Handler address:** Ghidra 0x2030C

#### Operations

1. Set flag `[0x4A5D0] = 1`
2. Call `load_and_render_sticker_from_alfred6(offset=0x613C2, size=0x3A2)`
3. **JMP 0x1D284** → falls into OPEN 473 handler which:
   - Hides hotspot[0] (extra 87) → (640, 400)
   - Persists state

---

### Room 28: PICKUP Extra 88 — "Pick Up Item in Lit Room"

**Handler address:** Ghidra 0x2032F

#### Operations

1. Set flag `[0x4A5D7] = 1`
2. Call `load_and_render_sticker_from_alfred6(offset=0x60E62, size=0x1D7)`
3. **JMP 0x1FCF8** → additional processing

---

### Room 28: PICKUP Extra 89 — "Pick Up Item in Lit Room"

**Handler address:** Ghidra 0x20357

#### Operations

1. Set flag `[0x4A5DE] = 1`
2. Call `load_and_render_sticker_from_alfred6(offset=0x61039, size=0x389)`
3. **JMP 0x1EE4F** → additional processing

---

### Room 28: PICKUP Extra 112 — "Pick Up Item in Lit Room"

**Handler address:** Ghidra 0x2037A

#### Operations

1. Set flag `[0x4A5EC] = 1`
2. Call `load_and_render_sticker_from_alfred6(offset=0x61764, size=0xE3)`
3. Hide hotspot[4] (extra 112) → (640, 400)
4. Persist state
5. Call `update_conversation_state(room=0x17, param2=0, param3=1)` (0x1B666)
6. **RET**

---

### Room 28: OPEN Extra 473 — "Open Door/Container"

**Handler address:** Ghidra 0x1D266

#### Operations

1. Set flag `[0x4A800] = 1`
2. Call `load_and_render_sticker_from_alfred6(offset=0x4BA6D, size=0x534)`
3. **Hide hotspot[0] (extra 87)** → (640, 400)
4. Persist state to ALFRED.1
5. **JMP 0x1E808** → cleanup/return

---

## Systematic Extraction Approach

### How to Analyze Any Handler

1. **Find the handler address** from the dispatch table:
   - Raw pointer + 0x10000 (if in entries 0-33 of PICKUP table)
   - File offset = Ghidra address + 0x4200

2. **Disassemble** from the handler start until RET or JMP to epilogue

3. **Apply fixups** to data references: add 0x40000 to all memory operand addresses

4. **Identify the pattern** — most handlers follow one or more of these templates:

   **Template A: Show/Hide Hotspot**
   ```asm
   mov eax, [room_data_ptr]      ; 0x4FAC8
   mov word [eax + OFFSET], X    ; set hotspot X
   mov eax, [room_data_ptr]
   mov word [eax + OFFSET+2], Y  ; set hotspot Y
   ; ... persist to state buffer and ALFRED.1
   ```

   **Template B: Set Flag**
   ```asm
   mov byte [FLAG_ADDR], VALUE
   ; ... persist via 6-byte buffer at 0x4FB70
   ```

   **Template C: Display Sticker**
   ```asm
   mov edx, SIZE               ; sticker data size
   mov eax, OFFSET             ; offset in ALFRED.6
   call load_and_render_sticker_from_alfred6
   ```

   **Template D: Palette Change**
   ```asm
   ; allocate buffer, seek ALFRED.7, read palette, fade, copy
   ```

5. **Map hotspot offsets to extras**: Read room's Pair 10 data from ALFRED.1 at offset 0x47C

### Automated Extraction

The handler code lives in a ~35KB unanalyzed gap in Ghidra (0x1BA2F to 0x24157). To systematically extract all actions:

1. Use the dispatch tables (already extracted in `verb_tables_output.txt`) to get all handler addresses
2. For each handler, disassemble from start to RET/JMP-to-epilogue
3. Parse the instruction stream for known patterns (hotspot moves, flag sets, sticker displays)
4. Cross-reference hotspot offsets with room data to get extra IDs

A Python script using capstone can automate this — see `disasm_room28_handler.py` for the template.

---

## ScummVM Implementation Notes

### Current Implementation (actions.cpp)

The `pickUpMatches()` function at line 1272 already handles:
- Palette loading from ALFRED.7 at 0x1610CE ✓
- Palette fade ✓
- FLAG_CROCODILLO_ENCENDIDO ✓
- `disableHotspot(hotspot)` to hide matches ✓
- `moveHotspot(findHotspotByExtra(87), 415, 171)` ✓
- `moveHotspot(findHotspotByExtra(88), 305, 217)` ✓
- `moveHotspot(findHotspotByExtra(89), 201, 239)` ✓
- `moveHotspot(findHotspotByExtra(112), 261, 259)` ✓

### Missing from ScummVM

1. **Room state byte**: `room_data[0xA5] = 2` — may affect background sprite rendering
2. **Ambient sound**: The original handler starts an ambient sound before the palette fade
3. **State persistence to ALFRED.1**: Handled differently in ScummVM via save/load system

### Extras 87/88/89/112 PICKUP handlers

These need ScummVM implementations:
- Each sets a game state flag, displays a sticker from ALFRED.6, and hides itself
- Extra 112 additionally calls `update_conversation_state(room=0x17)`
- Extra 87 shares code with the OPEN 473 handler for hiding

### OPEN Extra 473

Needs ScummVM implementation:
- Sets flag, displays sticker, hides extra 87
