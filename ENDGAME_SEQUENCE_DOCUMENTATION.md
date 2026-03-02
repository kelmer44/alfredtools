# Endgame Sequence — Room 48 Through Credits

## Overview

After Action 375 warps Alfred to room 48, the room 48 per-frame handler at Ghidra `0x10D4C` controls the remainder of the game. The handler checks `game_completion_flag` (`[0x9612]`, ScummVM `FLAG_END_OF_GAME 42`) to determine whether to run the ending sequence (PATH C). The complete endgame sequence flows:

1. **Interactive princess conversation** (with humor, references to Monkey Island)
2. **"Going dark"** — ACTION 380 fires mid-conversation, screen goes black
3. **Dark dialog** — conversation continues on black screen, player text visible, NPC text invisible
4. **Ending title scene** — room 16 background + 4 animated sprites + "ALFRED PELROCK" title text
5. **25-page credits slideshow** — each page shows a game room as background with centered credits text

---

## 1. Room 48 Per-Frame Handler (PATH C)

**Ghidra**: `0x10D4C` (per-frame dispatch table, called every frame)
**Entry condition**: `[0x9612] != 0` (game_completion_flag set by Action 375)

### Flow (Ghidra addresses):

| Step | Address | Action |
|------|---------|--------|
| 1 | `0x10FAC` | `update_conversation_state(room=48, npc=0, branch=1)` → set ROOT #1 |
| 2 | `0x10FC4` | `trigger_conversation_with_sprite(2, 0)` → **BLOCKING** interactive dialog |
| 3 | `0x10FC9` | `[0x9626] = 1` (endgame credits played flag) |
| 4 | `0x10FD0` | `init_or_stop_sound()` — stop current audio |
| 5 | `0x10FE2` | `play_cd_audio_track(CD_track + 2)` — credits music |
| 6 | `0x10FF1` | `fade_cd_audio()` |
| 7 | `0x1100B` | `load_room_graphics_and_palette_dynamic(16)` — credits background |
| 8 | `0x11021` | Load sprite animations from ALFRED.7 at `0x312AEA` |
| 9 | `0x11062` | Set up 4 animated sprites |
| 10 | `0x11381` | **Title animation loop** — infinite, exits on keypress |
| 11 | `0x113D2` | **25-page credits slideshow** (`0x29AA0`) |
| 12 | `0x113D7` | Return to main game loop → handler re-enters PATH C → dialog loops forever |

---

## 2. The "Going Dark" Mechanism

### How it works: Conversation control code 0xEB triggers ACTION 380

The conversation system recognizes two action-dispatch control codes:
- **0xF8** — Trigger action and **EXIT** conversation
- **0xEB** — Trigger action and **CONTINUE** conversation

Both use the same dispatch table at `0x47E58` (6 bytes/entry: `uint16 action_id, uint32 function_ptr`). The only difference is in `handle_conversation_tree` (Ghidra `0x18690`):

```c
if ((uVar5 == 0xf8) || (uVar5 == 0xeb)) {
    // Dispatch action from table at 0x47E58
    lookup_and_call_action_handler(action_code);
    
    if ((controlByte & 0xff) == 0xf8)
        break;    // ← ONLY 0xF8 exits the conversation
}
// 0xEB falls through here — conversation continues
```

### Conversation data triggering the dark effect

In room 48's text data (ALFRED.1 pair 12), the relevant sequence:

```
Player choice:  [FB][03][08][0D]"Pues apaga la luz..."[FD]
NPC response:   [FC][41][08][EE]"Buena idea..."[EB][7C][01]
                                                ^^^ ^^^^^^^^
                                                0xEB + ACTION 0x017C (380)
Next choice:    [FB][04][08][0D]"Oye, ¿dónde estás?"
NPC response:   [FC][41][08][EE]"Aquí. Ven. Ten cuidado..."
```

When the player selects "Pues apaga la luz..." (Turn off the light), the NPC responds "Buena idea..." (Good idea), then **ACTION 380 fires** but the conversation **continues**.

### ACTION 380 — Screen Clear Handler

**Ghidra**: `0x2260E` (468 bytes)

```
1. Zero ALL graphics buffers:
   - [0xFAB8] palette buffer (768 bytes)
   - [0xFAD8] back buffer 1 (256KB)
   - [0xFADC] front buffer / composite (256KB)
   - [0xFA9C] saved background (256KB)
   - [0xFA94] screen composition (312KB)
   - [0xFABC] sprite data backup (441KB)
   - [0xFAD0] ALFRED.2 anim buffer (176KB)

2. Apply blank palette → screen goes solid black

3. Set exactly TWO palette entries:
   - palette[0xF2] (242) = RGB(60, 57, 57) → VGA 8-bit ≈ (242, 230, 230) — muted gray
   - palette[0x0D] (13)  = RGB(63, 21, 63) → VGA 8-bit ≈ (255, 85, 255)  — bright magenta

4. Apply updated palette → text-only colors visible on black
```

### How text renders in the dark

The conversation data embeds speaker color bytes via `[08][XX]` sequences:
- Player text: `[08][0D]` → palette index **13** → **magenta** (visible in dark)
- NPC text: `[08][EE]` → palette index **238** → **black** (invisible — palette[0xEE] = 0,0,0)
- Dialog frame/highlight: uses palette index **0xF2** → **gray** (visible)

**Result**: After ACTION 380, only the player's text (Alfred) is readable against the black background. The NPC's responses are black-on-black — invisible. You're literally talking in the dark.

### ScummVM Impact

**Current state**: ScummVM's dialog.cpp treats `0xEB` as `CTRL_ALT_END_MARKER_2` and **skips it entirely**. It is never dispatched as an action trigger. This means:
1. ACTION 380 never fires → screen never goes dark
2. The conversation doesn't execute the action but continues normally
3. The dark-room comedy effect is completely missing

**Required fix**: The conversation parser must handle 0xEB like 0xF8 (dispatch via `dialogActionTrigger`) but **NOT** exit the conversation afterward. The 2 bytes following 0xEB are the action code (little-endian uint16).

---

## 3. Ending Title Scene

### Background: Room 16

Room 16 is not a playable room — it exists only in ALFRED.7's room graphics table (at file offset `0x488F4`, 0x36 bytes per room entry). It's loaded via `load_room_graphics_and_palette_dynamic(16)` at Ghidra `0x1B4A3`, which reads 8 background blocks (some RLE-compressed) and applies the palette.

### Animation Data

**Source**: ALFRED.7 at file offset `0x312AEA` (3,222,250 decimal)
**Compressed**: 0xC05C bytes (49,244) — RLE compressed
**Decompressed**: Into sprite data buffer, partitioned by offset for 4 sprites

### 4 Animated Sprites

| # | GFX Offset | Position | Size (W×H) | Frame Data | Anim Speed | Visible | Notes |
|---|-----------|----------|-------------|------------|------------|---------|-------|
| 1 | base+0x0000 | (426, 211) | 114×189 | 21,546 | 10 | 1 (always) | Main character — legs animation |
| 2 | base+0xA854 | (287, 68) | 42×26 | 1,092 | 10 | 2 (dynamic) | Small element — eyes blinking |
| 3 | base+0xB520 | (172, 174) | 93×71 | 6,603 | 10 | 2 (dynamic) | Second character — hand wave |
| 4 | base+0x10281 | (241, 334) | 55×66 | 3,630 | 10 | 1 (always) | Bottom element — hand animation |

Sprite visibility mode:
- **1** = always visible, simple loop
- **2** = dynamic — has idle frame + triggered animation (alternates between idle at one speed and active animation at another)

### Title Text Overlay

**Source**: Room 48 text data pointer at `[0xBC5C]` — points to "ALFRED PELROCK" + "En busca de un sueño"
**Position**: X=176 (0xB0), Y=200 (0xC8) — rendered via `render_text_overlay` at `0x18502`
**Visible**: Frames 21–149 only (exclusive: `frame > 20 && frame < 150`)
**Frame delay**: 106 ticks per frame (0x6A pushed as arg to `wait_or_process_input`)

### Animation Loop Structure

```
frame_counter = 0
LOOP:
    wait_or_process_input(0x6A)         // 106 tick delay
    update_sprite_animations()
    
    if (frame_counter > 20 AND frame_counter < 150):
        render_text_overlay([0xBC5C], x=176, y=200)
        set text_active_flag = 0xFF
    
    render_scene()
    
    if check_keyboard_input():
        GOTO credits_slideshow           // any keypress skips to credits
    
    frame_counter++
    GOTO LOOP                            // INFINITE — no upper bound!
```

**Key**: The loop runs **forever** until user input. There is NO automatic progression to credits — the player must press a key to advance.

### ScummVM Comparison

The current `endingScene()` has several differences:

| Aspect | Original | ScummVM Current |
|--------|----------|----------------|
| Frame count | **Infinite** (until keypress) | Fixed at 200 ticks |
| Title text timing | Frames 21–149 | Ticks 30–180 |
| Title text position | X=176, Y=200 | Centered calculation |
| Sprite count | 4 | 4 (but configured differently) |
| Sprite anim speed | All 10 | Mixed (2, 1, 1, 2) |
| Loop exit | Keypress only | tick > 200 auto-exit |
| Frame delay | 106 ticks via `wait_or_process_input` | `delayMillis(10)` per `_chrono` tick |

---

## 4. Credits Room Slideshow

### Function: `0x29AA0` (400 bytes)

Called from room 48 handler at `0x113D2` — the ONLY caller in the entire binary.

### Structure: Two-Phase

**Phase 1** (0x29AA0–0x29B91): Pre-calculate text centering for all 25 pages

```
for page = 0 to 24:
    text = pointer_table[page]              // table at 0xC2CC
    count chars to 0xFD delimiter
    lines = (char_count / 44) + 1           // 44 chars per line max
    max_line_width = scan for longest line   // 0xB1 = line break marker
    
    x = 310 - (max_line_width * 12 / 2)    // 12 px/char, centered on X=310
    y = 200 - (lines * 24 / 2)              // 24 px/line, centered on Y=200
    
    store x → page_x_table[page]            // array at 0x1864C
    store y → page_y_table[page]            // array at 0x18668
```

**Phase 2** (0x29B93–0x29C30): Display slideshow

```
OUTER_RESTART:
for page = 0 to 24:
    room_id = room_table[page]              // table at 0xC29A
    load_room_and_init_alfred(room_id, mode=2)  // load room as background only
    
    for frame = 0 to 34:                    // *** 35 FRAMES PER PAGE ***
        setup_alfred_frame()
        render_text_overlay(text_ptr[page], x[page], y[page])
        render_scene()
        
        if check_keyboard_input():
            skip_flag = 1
            break
    
    if skip_flag:
        break

if skip_flag:
    skip_flag = 0
    GOTO OUTER_RESTART                      // restart from page 0!

// Only reaches here when all 25 pages displayed without skip
return
```

### Key Constants

| Constant | Value | Meaning |
|----------|-------|---------|
| Total pages | **25** | Credit page count |
| Frames per page | **35** (0x23) | How long each page is displayed |
| Characters per line | **44** (0x2C) | Max chars before word-wrap |
| Pixels per character | **12** (0x0C) | Character glyph width |
| Pixels per line height | **24** (0x18) | Line spacing |
| Screen center X | **310** (0x136) | Centering reference |
| Screen center Y | **200** (0xC8) | Centering reference |
| Text end marker | **0xFD** | End of text delimiter |
| Line break marker | **0xB1** | Section/line break in credits text |
| Skip behavior | Restart from page 0 | Pressing any key restarts the entire slideshow |

### 25 Credits Pages

| Page | Room | Credit Text |
|------|------|-------------|
| 0 | 22 | A partir de un sueño de Juan José Gil |
| 1 | 27 | Programación Juan José Gil |
| 2 | 36 | Con la inestimable ayuda de... Jose Vicente Pons, Luisfer Fernández |
| 3 | 23 | Gráficos de Jose Luis Queral, Ana María Polo, Juan Arocas, Eva Astorga, Santi Sanz... |
| 4 | 24 | Música y efectos por Rufino Acosta (chunda-chunda) |
| 5 | 37 | Rutinas de sonido por Juan Carlos Arévalo |
| 6 | 25 | Guión por Juan José Gil |
| 7 | 26 | Diálogos por Juan José Gil y Raúl Arnau |
| 8 | 49 | Intro por Jose Luis Queral, Santi Sanz y Eva Astorga |
| 9 | 43 | Traductores... Britta Hoppe, Joel Escribano, Susan |
| 10 | 35 | Censora principal (existe una versión dura) Marisa Fernández |
| 11 | 52 | Coordinados por Luisfer Fernández (con sus bermudas) |
| 12 | 29 | Probadores: David Burgos, Alberto León, Carles... |
| 13 | 39 | Producido por DDM |
| 14 | 40 | Agradecimientos: |
| 15 | 41 | A mis gatos Prince y Aristóteles por sus prudentes consejos... |
| 16 | 45 | Al desodorante de Javi y David... |
| 17 | 47 | A Mar, Silvia, Elvira, Julia, María José... |
| 18 | 21 | Al Monkey Island, por su constante inspiración |
| 19 | 50 | Al espíritu de Rimbaud, Baudelaire, Nietzsche... |
| 20 | 46 | A LA MARXA Bar de copes (Valencia) |
| 21 | 42 | A Alberto Trobo por el diseño del billete de 100... |
| 22 | 34 | A Jose Antonio Schez (Chemy) tratamiento psicológico |
| 23 | 30 | A la revista FACULTAS |
| 24 | 14 | A ti !!!! Solo en el caso que no lo hayas pir... |

### Room Background for Each Page

Each credit page loads the **full room background** (from ALFRED.7, not ALFRED.1) for the listed room, including palette. Room animations play during the 35-frame display via `setup_alfred_frame()`. This creates a slideshow of memorable game locations with credits overlaid.

### Credits text data location

**EXE offset**: `0x49F60` (ScummVM: `kCreditsOffset`)
**Size**: 2540 bytes (ScummVM: `kCreditsSize`)
**Runtime address**: Data segment at `0x40000` + offset = pointers in table at `0xC2CC`
**Format**: 0xFD-terminated strings, 0xB1 as line break separator

### Room ID table location

**Runtime address**: `0xC29A` (25 × uint16, little-endian)
**This table is NOT currently in the ScummVM codebase** — only the text data is loaded via `getCredits()`.

---

## 5. Endgame Loop Behavior

After the credits slideshow returns, the handler returns to `main_game_loop` via `jmp 0x13A66`. On the **next frame**:

1. Per-frame handler fires again for room 48
2. `[0x9612]` still set → enters PATH C again
3. `trigger_conversation_with_sprite(2, 0)` fires again — conversation OPTIONS that were already used are disabled (FB-ONCE markers), so the player sees **new dialog options** they haven't explored
4. After conversation → screen goes dark again (if not already) → title scene → credits slideshow
5. This loops **forever** — the player explores dialog tree branches across multiple cycles

**The game never ends**. The player must quit manually. Each cycle through the dialog tree reveals new options until all are exhausted, at which point the conversation auto-completes to the title scene.

---

## 6. ScummVM Implementation Plan

### Required Changes

#### A. Dialog System — 0xEB as Action-Continue (HIGH PRIORITY)

In `dialog.cpp`, `0xEB` (currently `CTRL_ALT_END_MARKER_2`) must be recognized as an action dispatch code that does NOT exit the conversation. When encountered:
1. Read the 2-byte action code following it
2. Call `g_engine->dialogActionTrigger(actionCode, room, rootIndex)`
3. **Do NOT** set `shouldEnd = true` — conversation continues from next text segment

#### B. ACTION 380 Handler (HIGH PRIORITY)

In `dialogActionTrigger()` (actions.cpp), add `case 380`:
1. Clear `_compositeBuffer`, `_currentBackground`, `_screen` to black (memset 0)
2. Set palette to all zeros
3. Set palette[242] = RGB(242, 230, 230) — muted gray (VGA 6-bit 60,57,57 × 4.047)
4. Set palette[13] = RGB(255, 85, 255) — bright magenta (VGA 6-bit 63,21,63 × 4.047)
5. Apply palette via `g_system->getPaletteManager()->setPalette()`

#### C. Ending Title Scene Fixes (MEDIUM)

In `endingScene()`:
1. Change animation loop to **infinite** (until keypress), not tick-limited
2. Change title text visibility to frames 21–149
3. Set all 4 sprite animation speeds to 10
4. Set frame delay to match original (106 ticks via `wait_or_process_input`)

#### D. Credits Slideshow Implementation (HIGH PRIORITY)

In `credits()`:
1. Define room ID table: `{22, 27, 36, 23, 24, 37, 25, 26, 49, 43, 35, 52, 29, 39, 40, 41, 45, 47, 21, 50, 46, 42, 34, 30, 14}`
2. Load credits text via `_res->getCredits()` (already implemented)
3. Phase 1: Pre-calculate text centering per page (12 px/char, 24 px/line, wrap at 44 chars)
4. Phase 2: For each of 25 pages:
   - Load room background via `load_room_graphics_and_palette_dynamic(room_id)` equivalent
   - Display for **35 frames** with credits text overlaid
   - Check for keypress → if pressed, restart from page 0 (don't exit!)
5. Only exit when all 25 pages display without interruption

#### E. Endgame Loop (LOW PRIORITY)

After credits, return to room 48 conversation → allow re-entry into dialog tree with previously-used options disabled. This is the natural game behavior and should work automatically if PATH C in the room 48 entry handler is correct.

---

## 7. Data Reference Tables

### Graphics Buffers (ACTION 380 clears all)

| Pointer | ScummVM Equivalent | Size |
|---------|-------------------|------|
| [0xFAB8] | `_room->_roomPalette` | 768 bytes |
| [0xFAD8] | `_currentBackground` | 256KB |
| [0xFADC] | `_compositeBuffer` | 256KB |
| [0xFA9C] | `_savedBackground`? | 256KB |
| [0xFA94] | `_screen->getPixels()` | 312KB |
| [0xFABC] | sprite backup buffer | 441KB |
| [0xFAD0] | ALFRED.2 anim buffer | 176KB |

### Ghidra Functions Referenced

| Address | Name | Purpose |
|---------|------|---------|
| `0x10D4C` | room_48_perframe_handler | Main handler — dispatches A/B/C |
| `0x18690` | handle_conversation_tree | Conversation loop — handles 0xEB/0xF8 |
| `0x18DCE` | trigger_conversation_with_sprite | Sets up and enters conversation |
| `0x2260E` | action_380_screen_clear | Clears screen + sets 2 palette colors |
| `0x1B4A3` | load_room_graphics_and_palette_dynamic | Loads room bg from ALFRED.7 |
| `0x29AA0` | credits_room_slideshow | 25-page credits with room backgrounds |
| `0x152B6` | check_keyboard_input | Returns non-zero on keypress |
| `0x18502` | render_text_overlay | Renders text at specified position |
| `0x1BFBA` | update_sprite_animations | Sprite animation tick/vsync |
