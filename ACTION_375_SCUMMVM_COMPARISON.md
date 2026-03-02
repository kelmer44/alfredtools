# Action 375 — Endgame Cutscene: Original vs ScummVM Comparison

## Handler Location
- **Ghidra address**: `0x2236B` (not auto-discovered — indirect call via dispatch table at `0x47D24`)
- **File offset**: `0x2656B` (Ghidra + 0x4200)
- **Size**: 468 bytes (0x2236B–0x2253E)
- **Dispatch**: Extra ID `0x0177` (375), function pointer `0x0001236B` in OPEN verb table

---

## Execution Flow Comparison

### Original Game (per phase, 5 phases):

```
1. memcpy(bg_buffer, front_buffer, 256000)    — save current screen to background
2. sprite_table[phase+3].byte_0x21 = 0xC8     — trigger statue sprite animation
3. LOOP: wait_or_process_input(0x167)          — wait ~359 ticks per frame
         setup_alfred_frame()
         render_scene(0)                        — full composite + present
   UNTIL sprite_table[phase+3].byte_0x21 == 0xFF
4. play_ambient_sound(slot_11, ch=-1, vol=256, pan=256, flags=0x20)  — electric zap
5. line_counter = 0
6. LOOP (19 times):
     draw_line(front_buffer, x1, y1, x2_base+i, y2, REMAP_TABLE)   — palette remap!
7. setup_alfred_frame() + render_scene(0)      — lines visible for ONE frame
8. memcpy(front_buffer, saved_bg_ptr, 256000)  — restore from initial save
9. FOR s = 0 TO phase:
     load_and_render_sticker(sticker_phase_table[s])  — cumulative stickers
10. setup_alfred_frame() + render_scene(0)     — stickers visible, lines gone
11. phase++
```

### ScummVM (`teletransportToPrincess`):

```
1. sprite->animData[0].curFrame = 0; sprite->zOrder = 200  — trigger animation
2. LOOP: pollEvent() + renderScene() + update() + delay(10)
   UNTIL sprite->zOrder == -1
3. playSound(roomSfx[3], 0)                   — electric zap ✓
4. copyBackgroundToBuffer() + placeStickers() + updateAnimations() + presentFrame()
5. LOOP (19 times):
     drawLine(x1, y1, x2+i, y2, 255)          — WHITE color! ✗
6. markAllDirty() + update() + delay(10)       — no sprites rendered with lines
7. addSticker(stickers[phase])
8. copyBackgroundToBuffer() + placeStickers() + updateAnimations() + presentFrame()
9. phase++
```

---

## Issue #1: Ray Rendering (CRITICAL — visual difference)

### Original: Palette Remap Table (Semi-Transparent)
The handler pushes `0x12CFC` as the last parameter to `draw_line`. This is a **palette remap table pointer**.

**Address calculation**:
- `0x12CFC + 0x40000` (data segment base) = `0x52CFC`
- `shadow_palette_remap_tables` base = `0x52BFC`
- Offset: `0x52CFC - 0x52BFC = 0x100 = 256`
- **= `_paletteRemaps[1]`** (second shadow remap table from ALFRED.9)

The `draw_pixel_with_remap` function (0x29D49) works as:
```c
pixel_address = buffer + x + y * 640;
old_color = *pixel_address;
new_color = remap_table[old_color];    // remap_table = shadow_palette_remap_tables[1]
*pixel_address = new_color;.

For each pixel the line passes through, it reads the existing color and remaps it through the table, creating a **semi-transparent tinted ray** that blends with the background.

### ScummVM: Flat White Color
```cpp
_screen->drawLine(x1, y1, x2, y2, 255);  // solid white
```

### Fix
Draw lines on `_compositeBuffer` using `_room->_paletteRemaps[1]` as a remap table:
```cpp
// Instead of _screen->drawLine(x1, y1, x2, y2, 255);
// Use Bresenham with palette remap on _compositeBuffer
drawRemappedLine(_compositeBuffer, x1, y1, x2, y2, _room->_paletteRemaps[1]);
```

---

## Issue #2: Line Rendering Context (Medium — sprites missing during line flash)

### Original
After drawing 19 lines on the background buffer, calls full `render_scene(0)` which:
1. Copies background (with lines) to composition buffer
2. Draws NPC sprites on top
3. Presents to VGA

So the lines appear WITH sprites visible on screen.

### ScummVM
After drawing lines, calls just `_screen->markAllDirty()` + `_screen->update()`. No sprites are rendered in this frame — just raw lines on the display surface.

### Fix
Lines should be drawn on `_compositeBuffer`, then a full `presentFrame()` should be called (which will include sprites). Or do the full render pipeline: `copyBackgroundToBuffer()`, `placeStickersFirstPass()`, draw lines on buffer, `updateAnimations()`, `presentFrame()`.

---

## Issue #3: Exit Animation Offset (CRITICAL — wrong animation)

### Original
Calls `play_cutscene_overlay_animation(1, 1, 0, 0)` at 0x2662D:
- **ALFRED.7 offset**: `0x2DE14A` (3,006,794)
- **Compressed size**: `0x7606` (30,214 bytes)
- **Decompressed**: 12 frames × 98 × 138 = 162,288 bytes
- **Frame delay**: `0x19C` ticks (412)
- After frame 5: sets `sticker_render_active = 0xFF`

### ScummVM
Calls `smokeAnimation(-1, true)`:
- **ALFRED.7 offset**: `1526432` (`0x174AA0`)
- **Frame count**: 11 frames
- After frame 5: hides Alfred

### Problem
`smokeAnimation` loads a DIFFERENT animation (smoke/poof at 0x174AA0) than what the original endgame uses (teleport overlay at 0x2DE14A). The correct animation is 1,480,362 bytes further in ALFRED.7.

Additionally:
- Frame count: 12 (original) vs 11 (ScummVM)
- The original positions the overlay at the sprite's saved x,y, not Alfred's position
- The original doesn't hide Alfred; it sets a sticker overlay flag after frame 5

### Fix
Either create a new function or parameterize `smokeAnimation` to accept:
- Offset `0x2DE14A` for the endgame animation
- 12 frame count
- Sprite-based positioning (sprite index 1)
- Sticker overlay flag behavior instead of hiding Alfred

---

## Issue #4: Game Completion Flag (Missing)

### Original
```asm
0x2250B: mov byte ptr [0x9612], 1   ; game_completion_flag = 1
```

### ScummVM
No equivalent flag is set in `teletransportToPrincess`.

### Fix
Add `_state->setFlag(FLAG_GAME_COMPLETE, true)` (or create the flag if it doesn't exist). Address maps to game state offset `0x9612 - 0x9578 = 0x9A` relative to state base.

---

## Issue #5: Background Buffer Management (Subtle)

### Original
The original game has THREE buffers:
- `[0xFA60]` — saved/backup buffer (stores initial clean state)
- `[0xFADC]` — background buffer (room bg + stickers, used as source for composition)
- `[0xFA9C]` — composition buffer (bg + sprites → VGA)

Flow:
1. ESI = pointer to [0xFA60] saved at init
2. Each phase: copy front→bg (save current state with accumulated stickers)
3. Sprite animation runs (render_scene composites from bg each frame)
4. Lines drawn on bg buffer [0xFADC]
5. render_scene composites bg (with lines) + sprites → VGA
6. Restore bg from ESI (the INITIAL state, not per-phase state)
7. Stickers rendered on bg buffer
8. render_scene composites bg (with stickers) → VGA

### ScummVM
Uses `_currentBackground` and `_compositeBuffer`:
- `copyBackgroundToBuffer()` = `memcpy(_compositeBuffer, _currentBackground)`
- `presentFrame()` = `memcpy(_screen, _compositeBuffer)`

The ScummVM approach of calling `copyBackgroundToBuffer()` + `placeStickersFirstPass()` before each update is roughly equivalent, since `addSticker()` persists stickers in the list and they get re-rendered each call. However, lines are drawn on `_screen` instead of `_compositeBuffer`, bypassing the composition pipeline.

---

## Issue #6: Order of Operations (Minor)

### Original
1. Sprite animation completes
2. Play sound
3. Draw lines
4. Show lines (one frame)
5. Remove lines + render stickers

### ScummVM
1. Sprite animation completes
2. Play sound
3. **Copy background + place stickers + update animations + present** (extra render)
4. Draw lines
5. Show lines
6. Add sticker + copy background + place stickers + update animations + present

The ScummVM version has an extra full render (step 3) between sound and lines that the original doesn't have. The original goes directly from sound to line drawing.

---

## Data Tables (Verified from EXE)

### Line Coordinates (5 phases × 4 values, stride 4 words)

| Phase | x1  | y1  | x2_base | y2  | Description |
|-------|-----|-----|---------|-----|-------------|
| 0     | 57  | 176 | 301     | 322 | Left-innermost statue |
| 1     | 138 | 159 | 283     | 292 | Left-middle statue |
| 2     | 213 | 156 | 325     | 277 | Center-left statue |
| 3     | 460 | 163 | 370     | 292 | Center-right statue |
| 4     | 530 | 167 | 353     | 320 | Right statue |

Lines fan from `(x1,y1)` to `(x2_base+i, y2)` for i=0..18.

### Sticker Phase Mapping

| Phase | Table Value | Global Sticker ID |
|-------|-------------|-------------------|
| 0     | 8           | 113 |
| 1     | 9           | 114 |
| 2     | 5           | 110 |
| 3     | 6           | 111 |
| 4     | 7           | 112 |
| Final | 10          | 115 |

---

## Ghidra Labels Added

### Functions Renamed
| Address | Name |
|---------|------|
| 0x29D49 | `draw_pixel_with_remap` |
| 0x29D78 | `calculate_pixel_address` |

### Data Labels
| Address | Name |
|---------|------|
| 0x4FA60 | `saved_background_buffer_ptr` |
| 0x4FA9C | `composition_buffer_ptr` |
| 0x4FADC | `background_buffer_ptr` |
| 0x4FAC8 | `sprite_table_base_ptr` |
| 0x4FB96 | `alfred_x_position` |
| 0x4FB98 | `alfred_y_position` |
| 0x4FB9A | `alfred_facing_direction` |
| 0x49612 | `game_completion_flag` |
| 0x4B82C | `endgame_line_x1_table` |
| 0x4B82E | `endgame_line_y1_table` |
| 0x4B840 | `endgame_line_x2_base_table` |
| 0x4B842 | `endgame_line_y2_table` |
| 0x4B810 | `endgame_sticker_phase_table` |

### Comments Set
- Handler entry (0x2236B): Full handler description
- Line draw loop (0x2238D): Remap table explanation
- Sprite trigger (0x2246F): Animation byte 0x21 = 0xC8 mechanism
- Exit sequence (0x224E2): Final sticker + text + animation + warp
- Exit animation call (0x22506): ALFRED.7 offset 0x2DE14A, 12 frames
- Completion flag (0x2250B): game_completion_flag = 1
- play_cutscene_overlay_animation (0x2662D): Full function description
- draw_line (0x29C34): Bresenham with palette remap
- draw_pixel_with_remap (0x29D49): Remap table lookup mechanism

---

## Summary of Required Fixes

| Priority | Issue | Description |
|----------|-------|-------------|
| **HIGH** | Ray rendering | Use `_paletteRemaps[1]` remap table instead of flat white 255 |
| **HIGH** | Exit animation | Load from ALFRED.7 offset `0x2DE14A`, 12 frames (not smoke at `0x174AA0`) |
| **MEDIUM** | Game completion flag | Set game_completion_flag after cutscene |
| **LOW** | Line rendering context | Draw on composite buffer through full render pipeline, not directly on screen |
| **LOW** | Extra render before lines | Remove the extra render cycle between sound and line drawing |
