# Action 375 — Endgame Cutscene (Handler at 0x2236B)

## Overview

Action 375 (0x0177) is triggered from a description in **room 52**. It runs a **5-phase cutscene sequence** where each phase animates a sprite, draws decorative lines, and overlays cumulative stickers. After all 5 phases, it displays text, runs a final animation, and warps the player to **room 48**.

- **Dispatch table entry**: Action ID `0x0177`, stored pointer `0x0001236B`, handler at Ghidra `0x2236B`
- **Handler size**: ~467 bytes (0x2236B–0x2253E)

---

## Pseudocode

```c
handler_action_375() {
    // === INIT ===
    saved_bg = copy of background buffer      // [0xfa60]
    phase = 0;

    while (phase < 5) {
        // --- Phase setup ---
        memcpy(background_buffer, front_buffer);  // save current screen as bg

        // Start sprite animation for this phase
        sprite_slot = phase + 3;                  // uses sprite slots 3, 4, 5, 6, 7
        sprite_table[sprite_slot].byte_0x21 = 0xC8;  // trigger animation start

        // Wait for sprite animation to complete
        do {
            wait_or_process_input(0x167);         // process events + render frame
            setup_alfred_frame();
            render_scene();
        } while (sprite_table[sprite_slot].byte_0x21 != 0xFF);

        // Play ambient sound effect
        play_ambient_sound(...);

        // --- Line drawing sub-phase (19 lines) ---
        for (line = 0; line < 19; line++) {
            x1 = line_table_x1[phase];            // table at 0xb82c (from room data)
            y1 = line_table_y1[phase];            // table at 0xb82e
            x2 = line_table_x2[phase] + line;     // table at 0xb840 + line offset
            y2 = line_table_y2[phase];            // table at 0xb842
            draw_line(front_buffer, x1, y1, x2, y2);
        }

        setup_alfred_frame();
        render_scene();                           // lines visible momentarily

        // --- Restore background and overlay stickers ---
        memcpy(front_buffer, saved_bg);           // wipe lines off screen

        for (sticker_idx = 0; sticker_idx <= phase; sticker_idx++) {
            // cumulative: phase 0 → 1 sticker, phase 4 → 5 stickers
            lookup = sticker_index_table[sticker_idx];  // table at 0xb810
            load_and_render_sticker_from_alfred6(lookup);
        }

        setup_alfred_frame();
        render_scene();                           // stickers visible
        phase++;
    }

    // === EXIT SEQUENCE (phase == 5) ===

    // 1. Render final sticker (pegatina[115] = 0x693C8, 741 bytes)
    load_and_render_sticker_from_alfred6(offset=0x693C8, size=0x2E5);

    // 2. Display text with voice
    display_text_with_voice(text_ptr=[0xbbd4]);

    // 3. Play 12-frame animation sequence (function at 0x2662d)
    //    params: sprite=1, variant=1, animByte=0, stickerFlag=0
    play_animation_sequence(1, 1, 0, 0);

    // 4. Set game completion flag
    game_state[0x9612] = 1;

    // 5. Warp to room 48
    alfred.x = 138;           // [0xfb96]
    alfred.y = 255;           // [0xfb98]
    alfred.direction = 2;     // [0xfb9a]
    load_room(48);            // 0x30
}
```

---

## Phase-by-Phase Breakdown

### Per-Phase Flow (repeated 5 times, phase 0–4)

1. **Save screen**: `memcpy(bg ← front)` — captures current state (with stickers from prior phases baked in)
2. **Sprite animation**: Sets byte at offset `0x21` in sprite struct (slot `phase + 3`) to `0xC8` (200), which triggers the animation system. The handler polls this byte until it becomes `0xFF` (animation complete).
3. **Ambient sound**: Plays an ambient sound via `play_ambient_sound()` with auto-assign channel (`-1`).
4. **Line drawing**: Draws **19 line segments** fanning out from a fixed point. Coordinates come from 4 lookup tables indexed by `phase * 4`:
   - Start point `(x1, y1)` is constant for all 19 lines within a phase
   - End x-coordinate = `base_x2 + line_counter` (0–18), creating a fan effect
   - Each phase uses different coordinates (different part of screen)
5. **Render with lines**: Lines are briefly visible on screen.
6. **Restore background**: `memcpy(front ← saved_bg)` — wipes the lines off, restoring clean background.
7. **Render stickers**: Overlays stickers **cumulatively** (phase 0 renders sticker 0; phase 4 renders stickers 0–4). Sticker indices come from a lookup table at `0xb810`.
8. **Render final**: Scene now shows accumulated stickers without lines.

### Exit Sequence (after phase 4 completes)

1. **Final sticker**: Loads and renders sticker index **111** (`pegatina_offsets[111] = 0x693C8`, size 741 bytes)
2. **Text display**: Shows endgame text with voice via `display_text_with_voice()`
3. **Animation**: Calls the animation sequence function at `0x2662d` which plays a **12-frame** animation (see below)
4. **Game flag**: Sets `[0x9612] = 1` — marks game completion
5. **Room warp**: Loads room **48** with Alfred at position **(138, 255)**, facing direction **2**

---

## Called Functions

| Address | Name | Purpose in Handler |
|---------|------|-------------------|
| `0x2A218` | `__STK` | Watcom stack overflow check (prologue) |
| `0x29C34` | `draw_line` | Bresenham line drawing, calls `draw_pixel` per step |
| `0x2A66B` | `memcpy_wrapper` | Memory copy (eax=dest, edx=src, ebx=size) |
| `0x1BA45` | `load_and_render_sticker_from_alfred6` | Reads sticker from ALFRED.6, decodes header (x,y,w,h), renders pixel data |
| `0x2A258` | `wait_or_process_input` | Yields to game loop — processes events, updates animations, renders frame |
| `0x147C9` | `setup_alfred_frame_from_state` | Updates Alfred's sprite frame based on current state |
| `0x15E4C` | `render_scene` | Full scene render to display |
| `0x27CE1` | `play_ambient_sound` | Starts ambient sound on specified channel |
| `0x25487` | `display_text_with_voice` | Shows text with voice playback |
| `0x152F5` | `load_room_and_init_alfred` | Loads room and places Alfred at specified position |
| `0x2662D` | *(unnamed — animation player)* | Plays 12-frame cutscene animation sequence |

---

## Animation Sequence Function (0x2662D)

Called during exit with parameters `(al=1, dl=1, bl=0, cl=0)`. This is a general-purpose cutscene animation player:

1. Allocates **162,288 bytes** (`0x279F0`) for animation buffer
2. Loads graphics data into buffer
3. Saves current sprite position (x, y from sprite struct)
4. Runs **12 iterations**, each:
   - Calls `wait_or_process_input(0x19C)` (412 — likely frame delay)
   - Updates animation frame data with complex offset calculations
   - Conditionally renders stickers (based on iteration count and flags)
5. Frees allocated memory

---

## Data Tables (Initialized Data in EXE)

**Important**: The raw disassembly shows unrelocated addresses (e.g., `0xb82c`). The actual runtime addresses are `+0x40000` (data segment base), so `0xb82c` → `0x4b82c`. These are **initialized data** baked into `JUEGO.EXE`, not BSS.

### Line Drawing Coordinates (virtual `0x4b82c`)

Each phase draws 19 lines from `(x1, y1)` to `(x2_base + line_index, y2)`:

| Phase | x1  | y1  | x2_base | y2  | Sprite Animated |
|-------|-----|-----|---------|-----|-----------------|
| 0     | 57  | 176 | 301     | 322 | Sprite 1 (slot 3) |
| 1     | 138 | 159 | 283     | 292 | Sprite 2 (slot 4) |
| 2     | 213 | 156 | 325     | 277 | Sprite 3 (slot 5) |
| 3     | 460 | 163 | 370     | 292 | Sprite 4 (slot 6) |
| 4     | 530 | 167 | 353     | 320 | Sprite 5 (slot 7) |

Line `n` (0–18) draws from `(x1, y1)` to `(x2_base + n, y2)`, creating a fan effect.

### Sticker Phase Mapping (virtual `0x4b810`)

The lookup table maps each phase to a **local sticker index** within room 52's sticker set (pegatina indices 105–115):

| Phase | Local Index | Global Pegatina | ALFRED.6 Offset |
|-------|-------------|-----------------|-----------------|
| 0     | 8           | 113             | `0x068A76`      |
| 1     | 9           | 114             | `0x068F30`      |
| 2     | 5           | 110             | `0x067DDE`      |
| 3     | 6           | 111             | `0x068115`      |
| 4     | 7           | 112             | `0x0684E3`      |
| Final | 10          | 115             | `0x0693C8`      |

Stickers are rendered **cumulatively**: phase 0 shows sticker 113, phase 4 shows stickers 113+114+110+111+112, then the final sticker 115 is added in the exit sequence.

### Sticker File Offset Table (virtual `0x4b2f1`, stride 7)

This is a sub-table for room 52 containing 11 entries (one per room 52 sticker):

| Local | Global | Offset     | Size  |
|-------|--------|------------|-------|
| 0     | 105    | `0x0670D7` | 682   |
| 1     | 106    | `0x067381` | 552   |
| 2     | 107    | `0x0675A9` | 582   |
| 3     | 108    | `0x0677EF` | 681   |
| 4     | 109    | `0x067A98` | 838   |
| 5     | 110    | `0x067DDE` | 823   |
| 6     | 111    | `0x068115` | 974   |
| 7     | 112    | `0x0684E3` | 1427  |
| 8     | 113    | `0x068A76` | 1210  |
| 9     | 114    | `0x068F30` | 1176  |
| 10    | 115    | `0x0693C8` | 741   |

---

## Key Game State Addresses

| Address | Type | Value Set | Meaning |
|---------|------|-----------|---------|
| `[0xfa60]` | ptr | — | Background buffer pointer |
| `[0xfadc]` | ptr | — | Front/screen buffer pointer |
| `[0xfac8]` | ptr | — | Sprite table base pointer |
| `[0x9612]` | byte | `1` | Game completion flag |
| `[0xfb96]` | word | `0x8A` (138) | Alfred X position for room 48 |
| `[0xfb98]` | word | `0xFF` (255) | Alfred Y position for room 48 |
| `[0xfb9a]` | byte | `2` | Alfred facing direction for room 48 |

---

## Sprite Struct Layout (44 bytes / 0x2C per entry)

The handler accesses byte at offset **0x21** (33 decimal) within the sprite struct:

| Offset | Size | Field |
|--------|------|-------|
| 0x00 | 2 | x position |
| 0x02 | 2 | y position |
| 0x04 | 1 | width |
| 0x05 | 1 | height |
| 0x06 | 2 | stride |
| 0x08 | 1 | numAnims |
| 0x0A | 13 | animation sub-data (nframes, loopCount, speed, movementFlags) |
| 0x17 | 1 | zOrder |
| 0x20 | 2 | extra |
| **0x21** | **1** | **Animation trigger byte** — set to `0xC8` to start, becomes `0xFF` on completion |
| 0x22 | 1 | actionFlags |
| 0x26 | 1 | isHotspotDisabled |
| 0x27 | 1 | disableAfterSequence |

---

## ScummVM Mapping

| Original Concept | ScummVM Equivalent |
|-----------------|-------------------|
| Sprite slots 3–7 animated | Room 52 sprites (indices 105–115 in pegatina tables). Use existing sprite animation system |
| `draw_line()` Bresenham | `Graphics::drawLine()` or manual Bresenham on `ManagedSurface` |
| `load_and_render_sticker_from_alfred6()` | `_res->getSticker(index)` — already implemented |
| Final sticker (offset `0x693C8`) | `_res->getSticker(115)` — `pegatina_offsets[115] = 0x693C8` |
| `memcpy_wrapper()` 256KB | `Surface::copyFrom()` or `memcpy()` on the 640×400 buffer |
| `play_ambient_sound()` | `_sound->playSound(...)` |
| `wait_or_process_input(0x167)` | Game loop iteration — process events, update animations, render |
| `setup_alfred_frame()` + `render_scene()` | Existing render pipeline |
| `load_room_and_init_alfred(48)` | `loadRoom(48)` with Alfred at (138, 255) direction 2 |
| `game_state[0x9612] = 1` | `_state->setFlag(FLAG_GAME_COMPLETE, true)` |
| Animation function `0x2662D` | `_res->loadAlfredSpecialAnim()` + `waitForSpecialAnimation()` pattern |

---

## Room 52 Sprite Info

Room 52 has **8 sprites** (pair 10 data). The cutscene animates sprites at **slots 3–7** (real sprite indices 1–5):

| Slot | Index | x   | y   | w   | h   | Frames | Speed | zOrder | Role in Cutscene |
|------|-------|-----|-----|-----|-----|--------|-------|--------|------------------|
| 2    | 0     | 50  | 240 | 102 | 118 | 13     | 2     | 255    | Main scene sprite |
| **3** | **1** | **41** | **143** | **46** | **72** | **3** | **3** | **255** | **Phase 0** |
| **4** | **2** | **108** | **135** | **53** | **49** | **3** | **3** | **255** | **Phase 1** |
| **5** | **3** | **193** | **139** | **41** | **36** | **3** | **3** | **255** | **Phase 2** |
| **6** | **4** | **440** | **142** | **53** | **58** | **3** | **3** | **255** | **Phase 3** |
| **7** | **5** | **499** | **142** | **72** | **58** | **3** | **3** | **255** | **Phase 4** |
| 8    | 6     | 83  | 57  | 147 | 88  | 3      | 1     | 10     | Background detail |
| 9    | 7     | 438 | 56  | 114 | 93  | 3      | 1     | 10     | Background detail |

## Room 52 Sticker Info

Room 52 owns stickers **105–115** (11 stickers). The cutscene uses 5 during phases (113, 114, 110, 111, 112) and sticker **115** as the final overlay.

| Sticker Index | ALFRED.6 Offset | Size  | Role |
|--------------|-----------------|-------|------|
| 105 | `0x0670D7` | 682   | |
| 106 | `0x067381` | 552   | |
| 107 | `0x0675A9` | 582   | |
| 108 | `0x0677EF` | 681   | |
| 109 | `0x067A98` | 838   | |
| 110 | `0x067DDE` | 823   | Phase 2 sticker |
| 111 | `0x068115` | 974   | Phase 3 sticker |
| 112 | `0x0684E3` | 1427  | Phase 4 sticker |
| 113 | `0x068A76` | 1210  | Phase 0 sticker |
| 114 | `0x068F30` | 1176  | Phase 1 sticker |
| **115** | **`0x0693C8`** | **741** | **Final sticker** |
