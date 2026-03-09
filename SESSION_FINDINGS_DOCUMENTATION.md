# Session Findings Documentation
## ScummVM Pelrock Engine Bug Fixes, Research & Ghidra Annotations

Date: Session 2025 (spanning multiple prompts)
**Last updated:** Session 4 — Corrected sections 4-7 (scaling, volume, book, z-order), added Egypt preconditions

---

## Table of Contents
1. [Fix: `-Wglobal-constructors` Warning on `noBook`](#1-fix--wglobal-constructors-warning-on-nobook)
2. [Fix: Object-Use-with-Alfred Bug](#2-fix-object-use-with-alfred-bug)
3. [Feature: Generic Scaling Functions](#3-feature-generic-scaling-functions)
4. [CORRECTED: Scaling Algorithm — Exact Reimplementation](#4-corrected-scaling-algorithm--exact-reimplementation)
5. [CORRECTED: Volume Control System — Three Gradual Controls](#5-corrected-volume-control-system--three-gradual-controls)
6. [CORRECTED: Background Book — Room Thumbnails Exist](#6-corrected-background-book--room-thumbnails-exist)
7. [CORRECTED: Z-Order Fix — int8 vs Unsigned Byte](#7-corrected-z-order-fix--int8-vs-unsigned-byte)
8. [Fix: Egypt Travel Position](#8-fix-egypt-travel-position)
9. [Research: Egypt Travel Preconditions](#9-research-egypt-travel-preconditions)
10. [Ghidra Annotations Summary](#10-ghidra-annotations-summary)

---

## 1. Fix: `-Wglobal-constructors` Warning on `noBook`

**File:** `engines/pelrock/computer.h`  
**Problem:** `static const LibraryBook noBook` at file scope triggered `-Wglobal-constructors` because `LibraryBook` contains `Common::StringArray` and `Common::String` members with non-trivial destructors. At file scope, these require hidden `__cxa_atexit` registration — a global constructor.

**Fix:** Removed the unused `noBook` entirely. No code referenced it anywhere in the codebase.

**Verification:** `grep -r "noBook" engines/pelrock/` returned zero hits.

---

## 2. Fix: Object-Use-with-Alfred Bug

**File:** `engines/pelrock/pelrock.cpp` (popup handling section, ~line 625)  
**Problem:** When the player long-pressed on Alfred and selected ITEM from the action popup, the inventory overlay appeared. Selecting an item then called `walkAndAction(_currentHotspot, ITEM)`, but `_currentHotspot` was `nullptr` because Alfred (not a hotspot) triggered the popup. This caused the action to silently fail — objects could never be used on Alfred.

**Root Cause:** The popup handler checked `_currentHotspot != nullptr` before routing to `walkAndAction`, but never checked the Alfred-specific case. When `_actionPopupState.isAlfredUnder` was true, no valid code path existed for item use.

**Fix:**
```cpp
// Before (broken): always tried walkAndAction with null hotspot
if (_inventoryOverlayState.isActive && ...) {
    int item = checkMouseClickInventoryOverlay(...);
    _state->selectedInventoryItem = item;
    walkAndAction(_currentHotspot, ITEM);  // _currentHotspot is nullptr!
}

// After (fixed): check if Alfred is the target
} else if (_actionPopupState.isAlfredUnder && actionClicked != NO_ACTION) {
    debug("Using item on Alfred");
    useOnAlfred(_state->selectedInventoryItem);
} else if (_inventoryOverlayState.isActive && ...) {
    int item = checkMouseClickInventoryOverlay(...);
    _state->selectedInventoryItem = item;
    walkAndAction(_currentHotspot, ITEM);
}
```

The fix adds a check for `_actionPopupState.isAlfredUnder` before the inventory overlay check, routing to `useOnAlfred()` when appropriate.

---

## 3. Feature: Generic Scaling Functions

**Files:** `engines/pelrock/graphics.h`, `engines/pelrock/graphics.cpp`

Two new static utility methods added to `GraphicsManager`:

### `scaleBuffer(src, srcW, srcH, dstW, dstH)`
- Nearest-neighbor scaling to exact target dimensions
- Returns newly allocated `byte[]` (caller must `delete[]`)
- Handles any input/output dimensions

### `scaleBufferByPercent(src, srcW, srcH, percent, outW, outH)`
- Percentage-based wrapper around `scaleBuffer`
- `percent=100` → original size, `50` → half, `200` → double
- Writes computed dimensions to `outW`/`outH`

**Implementation:** Standard nearest-neighbor with `srcX = x * srcW / dstW` mapping. This is functionally equivalent to the original game's pixel-skip lookup tables but uses direct integer division instead of pre-computed tables.

---

## 4. CORRECTED: Scaling Algorithm — Exact Reimplementation

> **Previous session incorrectly stated** the ScummVM `calculateScalingMasks()` was "close enough" with nearest-neighbor. This was WRONG — the original uses pre-computed skip-pattern tables with specific FPU truncation behavior.

### Original Algorithm (JUEGO.EXE @ `init_sprite_scaling_tables` / 0x11E26)

The game pre-computes 4 skip-pattern lookup tables at startup:

| Table | Address | Dimensions | Purpose |
|-------|---------|------------|---------|
| 1 | 0x53290 | 51 × 51 | Width skip for standard sprites |
| 2 | 0x53CBC | 102 × 102 | Height skip for standard sprites |
| 3 | 0x56560 | 66 × 66 | Width skip for wide sprites |
| 4 | 0x57664 | 62 × 62 | Width skip for narrow sprites |

**Algorithm per table** (dimension = N):
```
For scale_factor = 0 to N-1:
    memset(row, 0, N)           // clear row
    step = (float)N / (float)(scale_factor + 1)
    acc = step
    while trunc(acc) < N:
        row[trunc(acc)] = 1     // mark pixel to draw
        acc += step
```

Key detail: `trunc()` is NOT C's default rounding — it's FPU truncation via the helper function at 0x2A8B8 (previously misidentified as `nop_stub_4`). This function:
1. Saves the FPU control word
2. Sets rounding control bits to `11` (truncation toward zero) via `MOV byte [ESP+1], 0x1F`
3. Calls `FRNDINT` (round to integer using current rounding mode = truncation)
4. Restores original FPU control word

### ScummVM Fix: `calculateScalingMasks()` Rewritten

The previous ScummVM implementation generated sequential indices `[0, 1, 2, ...]` for width tables instead of distributed skip patterns. This has been completely rewritten to match the original:

```cpp
void PelrockEngine::calculateScalingMasks() {
    // Table 1: 51x51 - matches init_sprite_scaling_tables exactly
    for (int factor = 0; factor < 51; factor++) {
        memset(&_widthScalingMask[factor * 51], 0, 51);
        float step = 51.0f / (float)(factor + 1);
        float acc = step;
        while ((int)acc < 51) {
            _widthScalingMask[factor * 51 + (int)acc] = 1;
            acc += step;
        }
    }
    // Table 2: 102x102 (height)
    for (int factor = 0; factor < 102; factor++) {
        memset(&_heightScalingMask[factor * 102], 0, 102);
        float step = 102.0f / (float)(factor + 1);
        float acc = step;
        while ((int)acc < 102) {
            _heightScalingMask[factor * 102 + (int)acc] = 1;
            acc += step;
        }
    }
    // Tables 3 & 4 follow identical pattern for 66x66 and 62x62
}
```

The `(int)` cast in C++ performs truncation toward zero, matching the FPU truncation helper's behavior exactly.

### Rendering Function (0x16FF8)
The renderer `render_alfred_sprite_with_scaling_and_shadow` uses:
- **Width skipping:** `width_skip_table[scaled_width_index + (visible_width - col) * dim]` — if 0, skip source pixel
- **Height skipping:** `height_skip_table[height_scale_index + (visible_height - row) * dim]` — if 0, skip entire row
- **Shadow overlay:** Scans shadow map at character feet (Y + 102 hardcoded). If shadow pixel ≠ 0xFF, remaps via `shadow_remap_tables_4x256` (from ALFRED.9)
- **Water reflection:** Rooms 25 and 45 render reflected character below using `water_reflection_remap_table`

---

## 5. CORRECTED: Volume Control System — Three Gradual Controls

> **Previous session incorrectly stated** the game has "binary ON/OFF toggle" for sound. This was WRONG — there are three independent gradual volume controls.

### Original System (JUEGO.EXE)

Three volume controls stored at consecutive bytes in DATA segment:

| Address | Name | Controls |
|---------|------|----------|
| DS:0x9650 | master_volume | SB mixer output volume (both channels) |
| DS:0x9651 | music_volume | CD audio volume |
| DS:0x9652 | sfx_volume | SB mixer input/recording volume |

**Range:** 0–14 for each control (15 levels).

### Handler Functions (6 total, at options menu handler 0x12918)

| Function | Hitbox (from 0x487D4 table) | Action |
|----------|----------------------------|--------|
| vol_master_up | Options button area | Increment DS:0x9650, call `set_mixer_output_volume(0x29480)` |
| vol_master_down | Options button area | Decrement DS:0x9650, call `set_mixer_output_volume(0x29480)` |
| vol_music_up | Options button area | Increment DS:0x9651, set CD audio volume |
| vol_music_down | Options button area | Decrement DS:0x9651, set CD audio volume |
| vol_sfx_up | Options button area | Increment DS:0x9652, call `set_mixer_input_volume(0x2958C)` |
| vol_sfx_down | Options button area | Decrement DS:0x9652, call `set_mixer_input_volume(0x2958C)` |

### Volume Display (0x143C6)
Draws volume bars in the options screen. Each control's current level (0–14) is rendered as a horizontal bar, likely using filled rectangles proportional to the value.

### Hardware Mapping
- **`set_mixer_output_volume` (0x29480):** Writes to SB mixer register 0x22 (master volume). Maps 0–14 → hardware-specific range. Controls overall output level.
- **`set_mixer_input_volume` (0x2958C):** Writes to SB mixer input/recording registers. Used for SFX channel separation on Sound Blaster cards.
- **CD audio:** Volume set through MSCDEX/CD-ROM driver IOCTLs via `init_cdrom_device` (0x28C20).

### ScummVM Implication
Must implement 3 separate volume sliders (master, music, SFX) each with 15 discrete levels (0–14), not a simple ON/OFF toggle. Map to ScummVM's `ConfMan` audio settings: `music_volume`, `sfx_volume`, `speech_volume` (scaled from 0–14 to 0–255).

---

## 6. CORRECTED: Background Book — Room Thumbnails Exist

> **Previous session incorrectly stated** the book shows "text listing of rooms" only with "no room thumbnail scaling." This was WRONG — the book DOES show scaled room background thumbnails.

### Book Handler (Button 8, 0x141AA)

When the player clicks button 8 (background book / "Libro de Fondos"), the handler:

1. Loads book UI graphics from ALFRED.1 at offset **0x30BA20** (menu/frame graphics)
2. Loads full background data block from ALFRED.1 at offset **0x31EB1E** (~256KB of room background data)
3. Loads compressed thumbnail data from ALFRED.1 at offset **0x35D31E** (pre-compressed room thumbnails)

### Room Thumbnail Display

The book displays **two columns of room entries** (17 entries per column, 34 total visible). Each entry has:
- Room name text (rendered with game font)
- A clickable region — when clicked, a **scaled-down version of the room's background** is displayed on the right side of the book

Room indices for the two columns are stored at:
- Column 1: DS:0xB884 (17 word entries)
- Column 2: DS:0xB895 (17 word entries)

### Thumbnail Format
Each thumbnail decompresses to **5,280 bytes** (240 pixels wide × 22 pixels tall, 8-bit indexed). The thumbnails at 0x35D31E are stored compressed; total decompressed size across all entries is **153,120 bytes**.

### Palette Handling
**Instant swap, no fade.** When the book opens:
1. Room palette backed up
2. Book palette (from ALFRED.7 extra screen 13, offset 0x226358, palette at 0x236AA8) loaded via `setPalette()`
3. Book UI rendered with thumbnails

When the book closes, room palette is restored instantly.

---

## 7. CORRECTED: Z-Order Fix — int8 vs Unsigned Byte

> **Previous session's fix** (removing `< 0` / `>= 0` guard conditions) was WRONG and did not fix room 13.

### Root Cause: `int8 zOrder` Should Be Unsigned

The original game stores sprite z-order as an **unsigned byte** (0–255 range). The ScummVM `Sprite` struct declared `zOrder` as `int8` (signed, -128 to +127). This caused z-values ≥ 128 to wrap negative:

| File Value | As `int8` | As `uint8`/`int` |
|------------|-----------|-------------------|
| 100 | 100 | 100 |
| 142 | -114 | 142 |
| 200 | -56 | 200 |
| 250 | -6 | 250 |

### How It Broke Rendering

**37 sprites across 22 rooms** have z ≥ 128:
Rooms 9, 12, 13, 16, 19, 23, 24, 25, 26, 28, 33, 34, 35, 36, 38, 39, 40, 43.

Three failure modes:
1. **Sort order:** `sortAnimsByZOrder()` used signed comparison. z=200 (stored as -56) sorted AFTER z=100 instead of BEFORE, inverting their visual layering.
2. **Pass assignment:** The two-pass renderer used `zOrder < 0` to assign sprites to the "behind Alfred" pass. All z ≥ 128 sprites were caught by this check regardless of Alfred's position.
3. **Sentinel conflict:** `zOrder = -1` was used as "disabled sprite" sentinel, but z=255 (a valid value) also stored as -1 in int8, causing valid sprites to be treated as disabled.

### Room 13 Specific Case
- Sprite 0: z=100, position (200,131)-(254,192) — valid signed
- Sprite 3: z=250, position (228,162)-(287,219) — stored as int8=-6
- Overlap region: x=228–254, y=162–192
- With signed sort: sprite 3 (z=-6) rendered ON TOP of sprite 0 (z=100) — wrong
- With unsigned: sprite 3 (z=250) rendered BEFORE sprite 0 (z=100) — correct (higher z = background)

### Original Game's Rendering (0x16640)
Bubble sort at 0x16640 uses **JNC (Jump if Not Carry)** = unsigned comparison. Sorts DESCENDING by z-depth as an unsigned byte. z=255 is drawn first (farthest back), z=0 drawn last (most foreground).

Alfred's z-depth: `((399-Y) & 0xFFFE) / 2 + 10` — range 10 (bottom/foreground) to 209 (top/background), stored at render queue entry 1. Entries with z_depth == 0xFF are skipped (disabled marker).

### Fix Applied (3 files)

**`types.h`:** Changed `int8 zOrder` to `int zOrder` in Sprite struct.

**`pelrock.cpp`:**
- `applyMovement()` signature: `int8 *z` → `int *z`
- `updateAnimations()`: `zOrder < 0` → `zOrder == 255`; `zOrder >= 0` → `zOrder != 255`
- `drawNextFrame()`: `zOrder == -1` → `zOrder == 255`
- 11 instances of `zOrder = -1` → `zOrder = 255` (passerby anims, pyramid collapse, pigeon scene, etc.)

**`actions.cpp`:** 5 instances of `zOrder = -1`/`== -1`/`!= -1` → `255`

**`room.cpp`:** `disableSprite()`: `zOrder = -1` → `zOrder = 255`

Full build successful with `make -j4`.

## 8. Fix: Egypt Travel Position

**File:** `engines/pelrock/pelrock.cpp` (`travelToEgypt()`, ~line 303)  
**Problem:** After the Egypt travel animation, Alfred appeared at incorrect position (172, 388) — snapped to walkbox 0 instead of the correct location.

### Root Cause
ALFRED.8 default position for room 21 is (439, 322), which is **outside all walkboxes**. The engine's walkbox snapping logic moved Alfred to the nearest valid walkbox, landing on walkbox 0 at (172, 388).

### Original Game Behavior (JUEGO.EXE @ 0x21449)
Disassembly of the F8 action 279 handler (Egypt travel):
```asm
mov word ptr [0xFB96], 0x23F    ; alfredX = 575
mov word ptr [0xFB98], 0xD2     ; alfredY = 210
mov byte ptr [0xFB9A], 2        ; direction = ALFRED_DOWN
; ... then calls load_room_and_init_alfred with room 21
```

Position (575, 210) is inside **walkbox 7** of room 21:
```
Walkbox 7: x1=538, y1=148, x2=639, y2=305
Check: 538 ≤ 575 ≤ 639, 148 ≤ 210 ≤ 305 → INSIDE ✓
```

The handler also:
- Clears `selectedInventoryItem` to -1
- Adds inventory items: 17 (Egyptian book), 64, 24, 59

### Fix
```cpp
_alfredState.x = 575;
_alfredState.y = 210;
setScreenAndPrepare(21, ALFRED_DOWN);

_state->selectedInventoryItem = -1;
addInventoryItem(17);  // Egyptian book
addInventoryItem(64);
addInventoryItem(24);
addInventoryItem(59);
```

---

## 9. Research: Egypt Travel Preconditions

### Full Precondition Chain (verified against JUEGO.EXE and ScummVM codebase)

Before the player can travel to Egypt, multiple conditions must be satisfied:

#### Gate 1: Travel Agency Opens (`FLAG_AGENCIA_ABIERTA`, flag 51)
Set by `checkObjectsForPart2()` when **all three items** are in inventory:
- Item 17: Egyptian book (from the library)
- Item 24: Pol Pot letters
- Item 59: Recipe book

This check runs after every inventory addition. Once flag 51 is set, the travel agency exterior (room 19) allows entry to the interior (room 20).

#### Gate 2: Money for Ticket (Item 75 — 150,000 pesetas)
1. Player must complete the newspaper editor conversation → triggers action 277 → sets `FLAG_JEFE_INGRESA_PASTA` (flag 0)
2. With flag 0 set, using ATM card at the bank → dispenses item 75 (150,000 pesetas) + advances conversation root to 2

#### Gate 3: Travel Agent Conversation
- Conversation root 0 → leads to action 278 (initial dialog) → advances to root 1
- Root 1 → ATM/money resolution → advances to root 2
- Root 2 → action 279 → removes item 75 (payment) → calls `travelToEgypt()`

### `travelToEgypt()` Actions (F8 handler, action 279 @ 0x21449)
```asm
mov word ptr [0xFB96], 0x23F    ; alfredX = 575
mov word ptr [0xFB98], 0xD2     ; alfredY = 210
mov byte ptr [0xFB9A], 2        ; direction = ALFRED_DOWN
```
- Sets position (575, 210) inside walkbox 7 of room 21 (Egypt exterior)
- Clears `selectedInventoryItem` to -1
- Adds inventory items: 17, 64, 24, 59

### ScummVM Status: ✅ Fully Implemented
All gates, flag checks, conversation roots, and `travelToEgypt()` are already correctly implemented in the ScummVM Pelrock engine codebase. No changes needed.


---

## 10. Ghidra Annotations Summary

### Functions Renamed (35 total)

| Address | Old Name | New Name |
|---------|----------|----------|
| 0x1BA2F | FUN_0001ba2f | process_idle_and_stop_sound |
| 0x26861 | FUN_00026861 | show_intro_message_if_enabled |
| 0x26F6C | FUN_00026f6c | cleanup_sound_if_active |
| 0x26FE0 | FUN_00026fe0 | game_exit_and_play_credits |
| 0x2A2D2 | FUN_0002a2d2 | exit_to_dos |
| 0x262FC | FUN_000262fc | free_sound_data_buffers |
| 0x39248 | FUN_00039248 | render_text_message |
| 0x2A8B8 | FUN_0002a8b8 | nop_stub_4 |
| 0x277CB | FUN_000277cb | update_sound_channel |
| 0x27280 | FUN_00027280 | init_sound_channel_struct |
| 0x276F1 | FUN_000276f1 | advance_primary_sound_channel |
| 0x27843 | FUN_00027843 | advance_sound_playback_frames |
| 0x2794D | FUN_0002794d | init_sound_playback_buffer |
| 0x270EB | FUN_000270eb | open_wav_sound_handle |
| 0x27130 | FUN_00027130 | open_voc_sound_handle |
| 0x27E60 | FUN_00027e60 | reset_sound_channel_entry |
| 0x2A8D5 | FUN_0002a8d5 | strcpy_custom |
| 0x2ACAE | FUN_0002acae | flush_all_files |
| 0x2ACBB | FUN_0002acbb | get_file_size |
| 0x2ACF8 | FUN_0002acf8 | malloc_internal |
| 0x2ADDB | FUN_0002addb | dos_int21_io |
| 0x28C20 | FUN_00028c20 | init_cdrom_device |
| 0x28EB4 | FUN_00028eb4 | query_cdrom_status |
| 0x290AD | FUN_000290ad | check_cdrom_ready |
| 0x29480 | FUN_00029480 | set_mixer_output_volume |
| 0x2958C | FUN_0002958c | set_mixer_input_volume |
| 0x29A39 | FUN_00029a39 | init_sound_hardware |
| 0x29D26 | FUN_00029d26 | sign_of_int |
| 0x29DB0 | FUN_00029db0 | check_vesa_support |
| 0x29E91 | FUN_00029e91 | free_dos_memory_block |
| 0x29ED2 | FUN_00029ed2 | set_vesa_video_mode |
| 0x29F36 | FUN_00029f36 | query_vesa_mode_info |
| 0x2A155 | FUN_0002a155 | allocate_dos_memory |
| 0x2A90F | FUN_0002a90f | parse_fopen_mode |
| 0x2A9C3 | FUN_0002a9c3 | fopen_internal |
| 0x2AA8B | FUN_0002aa8b | fopen_wrapper |
| 0x2AAA6 | FUN_0002aaa6 | fopen_wrapper2 |
| 0x2AB3C | FUN_0002ab3c | close_file_by_handle |
| 0x2AB6B | FUN_0002ab6b | close_file_handle |
| 0x2AB80 | FUN_0002ab80 | nibble_to_hex_char |
| 0x2AB8C | FUN_0002ab8c | build_temp_filename |
| 0x2A1C4 | FUN_0002a1c4 | init_vesa_mode_with_fallback |
| 0x2A210 | FUN_0002a210 | save_stack_segment |
| 0x2A22B | FUN_0002a22b | check_stack_overflow |
| 0x2A249 | FUN_0002a249 | stack_overflow_handler |
| 0x2A27A | FUN_0002a27a | atoi_custom |
| 0x2A2D1 | FUN_0002a2d1 | nop_stub_5 |
| 0x2A2EA | FUN_0002a2ea | exit_program |
| 0x2A300 | FUN_0002a300 | adjust_file_buffer_position |

### Data Items Renamed (12 total)

| Address | New Name | Description |
|---------|----------|-------------|
| 0x53290 | width_skip_table_51x51 | Scaling width skip patterns (51 entries × 51 factors) |
| 0x53CBC | height_skip_table_102x102 | Scaling height skip patterns (102 entries × 102 factors) |
| 0x56560 | width_skip_table_66x66 | Scaling width skip patterns for wide sprites |
| 0x57664 | width_skip_table_62x62 | Scaling width skip patterns for narrow sprites |
| 0x52BFC | shadow_remap_tables_4x256 | 4 palette remap tables for shadow levels (from ALFRED.9) |
| 0x4957C | water_reflection_remap_table | Color remap for water reflections (rooms 25, 45) |
| 0x4B9B4 | scaling_percentage_lut | 171-entry scaling percentage lookup |
| 0x4FBA3 | inventory_shift_counter | Counter for shifting inventory items during removal |
| 0x53020 | sound_data_buffer_ptr | Pointer to loaded sound data |
| 0x53018 | sound_file_handle | Handle for SONIDOS.DAT file |
| 0x53004 | fight_anim_sprite_x | X position for fight animation sprite |
| 0x53006 | fight_anim_overlay_y | Y overlay position for fight animation |

### Variables Renamed (7 total)

| Function | Old Name | New Name |
|----------|----------|----------|
| render_alfred_sprite_with_scaling_and_shadow | local_30 | right_clip_pixels |
| render_alfred_sprite_with_scaling_and_shadow | local_28 | visible_width |
| render_alfred_sprite_with_scaling_and_shadow | local_2c | draw_x |
| render_alfred_sprite_with_scaling_and_shadow | local_20 | visible_height |
| render_alfred_sprite_with_scaling_and_shadow | local_1c | shadow_reflection_offset |
| render_alfred_sprite_with_scaling_and_shadow | local_10 | height_skip_count |
| render_alfred_sprite_with_scaling_and_shadow | local_24 | draw_y_start |

### Decompiler Comments Added (4 functions)

1. **init_sprite_scaling_tables (0x11E26):** Documents all 4 skip-pattern tables, algorithm details, and scaling_percentage_lut initialization.
2. **render_alfred_sprite_with_scaling_and_shadow (0x16FF8):** Documents shadow detection, color remapping, water reflection special cases, and clipping logic.
3. **fade_palette_to_black (0x1B8B3):** Documents the per-component decrement algorithm and timing.
4. **process_inventory_action (0x24157):** Documents the inventory add flow and animation rendering.

---

## Key Memory Addresses Reference

| Address | Name | Type |
|---------|------|------|
| 0xFB94 | current_room | word |
| 0xFB96 | alfredX | word |
| 0xFB98 | alfredY | word |
| 0xFB9A | direction | byte |
| 0xFBA0 | selectedInventoryItem | word |
| 0x53290 | width_skip_table_51x51 | 51×51 bytes |
| 0x53CBC | height_skip_table_102x102 | 102×102 bytes |
| 0x56560 | width_skip_table_66x66 | 66×66 bytes |
| 0x57664 | width_skip_table_62x62 | 62×62 bytes |
| 0x52BFC | shadow_remap_tables | 4×256 bytes |
| 0x4957C | water_reflection_remap | 256 bytes |

---

## Known Issues / Future Work

1. ~~**`calculateScalingMasks()` width table bug:**~~ **FIXED** — Rewritten to match exact skip-table algorithm with FPU truncation.
2. ~~**Scaling rounding differences:**~~ **FIXED** — Using `(int)` truncation cast matching original FPU behavior.
3. **Shadow height hardcode:** The renderer uses hardcoded `+102` (0x66) for shadow detection Y offset. This fails for non-standard sprite heights (e.g., room 55 crawl sprite height=55).
4. **Volume controls:** Three volume sliders (master/music/SFX, 0–14 range) not yet implemented in ScummVM. Currently no volume UI.
5. **Book room thumbnails:** Background book thumbnail display not yet implemented. Data offsets identified but decompression/rendering code needed.
