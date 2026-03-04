# Room Animation Investigation: Rooms 5, 9, 19, 24

Investigation of 4 specific room animation behaviors through Ghidra disassembly of JUEGO.EXE and comparison with ScummVM implementation.

## Sprite Index Mapping

The original game stores sprite data in pair 10 of ALFRED.1. The layout is:

```
pair10_data + 0:    5-byte header
pair10_data + 5:    1-byte sprite count (includes 2 header entries)
pair10_data + 6:    44×2 = 88 bytes of header blocks
pair10_data + 94:   4 more bytes
pair10_data + 98:   First actual sprite (44 bytes each)
```

**Pointer `[0xFAC8]`** = `pair10_data` (start of pair 10 data).

The original accesses sprites as `base + originalIdx * 0x2C + fieldOffset`, where:
- **Original index N** → **ScummVM index (N − 2)** (the −2 accounts for the 2 header blocks)
- **Original field offset** = ScummVM field offset + 10 (the 10-byte gap from pair10 start to where field 0 would be)

### Sprite Struct Field Map (44 bytes)

| Original Offset | ScummVM Offset | Field | Type |
|-----------------|---------------|-------|------|
| 0x0A (10) | 0 | x | int16 |
| 0x0C (12) | 2 | y | int16 |
| 0x0E (14) | 4 | w | byte |
| 0x0F (15) | 5 | h | byte |
| 0x10 (16) | 6 | stride | uint16 |
| 0x12 (18) | 8 | numAnims | byte |
| 0x13 (19) | 9 | curAnimIndex | byte (runtime) |
| 0x14 (20) | 10 | nframes[0] | byte |
| 0x15 (21) | 11 | nframes[1] | byte |
| 0x16 (22) | 12 | nframes[2] | byte |
| 0x17 (23) | 13 | nframes[3] | byte |
| 0x18 (24) | 14 | loopCount[0] | byte |
| 0x19 (25) | 15 | loopCount[1] | byte |
| 0x1A (26) | 16 | loopCount[2] | byte |
| 0x1B (27) | 17 | loopCount[3] | byte |
| 0x1C (28) | 18 | speed[0] | byte |
| 0x1D (29) | 19 | speed[1] | byte |
| 0x1E (30) | 20 | speed[2] | byte |
| 0x1F (31) | 21 | speed[3] | byte |
| 0x20 (32) | 22 | curFrame | byte (runtime) |
| 0x21 (33) | 23 | zOrder | int8 |
| 0x22 (34) | 24 | movementFlags[0] | uint16 |
| 0x24 (36) | 26 | movementFlags[1] | uint16 |
| 0x26 (38) | 28 | movementFlags[2] | uint16 |
| 0x28 (40) | 30 | movementFlags[3] | uint16 |
| 0x2A (42) | 32 | extra | int16 |

### movementFlags Bit Layout

```
Bits  0-2:  X speed (pixels per frame)
Bit   3:    X direction (0=left, 1=right)
Bit   4:    X movement enabled
Bits  5-7:  Y speed (pixels per frame)
Bit   8:    Y direction (0=up, 1=down)
Bit   9:    Y movement enabled
Bits 10-12: Z speed
Bit  13:    Z direction
Bit  14:    Z movement enabled
```

Common values:
- `0x1F` = `0b0000000000011111` → X: 7px RIGHT
- `0x3FF` = `0b0000001111111111` → X: 7px RIGHT + Y: 7px DOWN
- `0x3E0` = `0b0000001111100000` → Y: 7px DOWN
- `0x3C0` = `0b0000001111000000` → Y: 6px DOWN

---

## Room 9: Library Interior — Passer-by Movement Path

### Original Behavior (Ghidra)

**Handler addresses:**
- Entry Init (table 4): `0x258BD` — Clears door state `[0x95BF]`, resets `room_data[0x1C1]`
- Entry Init (table 17): `0x25A7F` — Hides sprite 4 (original idx) = passer-by: `zOrder = 0xFF`
- **Render Scene Handler**: `0x1167A` (563 bytes) — Contains phone ring + passer-by movement

**Sprites involved:**
- Original index 4 / ScummVM index 2: the passer-by (mouse/rat running past window)
- Original index 5 / ScummVM index 3: phone animation (triggers ring sound)

### Phone Ring Logic (0x1167A–0x116FB)

1. Check sprite 5 `curAnimIndex == 1` AND `curFrame >= 1`
2. If `room9_phone_ring_played [0x964E] == 0`: play ambient sound, set flag to 1
3. When sprite 5 `curAnimIndex` returns to 0: reset flag to 0

### Passer-by Timer Trigger (0x116FB–0x11735)

1. When `(game_tick_counter [0x11738] & 0x3FF) == 0x3FF`:
   - If `room9_passerby_active_flag [0x95EB] == 0`:
     - Set flag to 1
     - Set sprite 4 `zOrder = 0xD2` (210 = visible)
2. If flag is 0, skip all movement logic

### Position-Based Movement Phases (0x11735–0x118AC)

**Starting position:** x=82 (0x52), y=315 (0x13B)

All phase checks run **every frame** with one-shot flags. The movement is applied by the engine's `applyMovement()` reading the sprite's movementFlags for the current animation slot.

| Phase | Condition | Flag | curAnimIndex | movementFlags | Direction |
|-------|-----------|------|-------------|---------------|-----------|
| 0 | x < 135 | `[0x95EF]` | 0 | `[0]=0x1F` | **RIGHT 7px** |
| 1 | x > 135 | `[0x95EE]` | 1 | `[1]=0x3FF` | **RIGHT+DOWN 7px** (diagonal) |
| 2 | y > 330 | `[0x95ED]` | 2 | `[2]=0x1F` | **RIGHT 7px** |
| 3 | x > 200 | `[0x95EC]` | 3 | `[3]=0x3E0` | **DOWN 7px** |

**Reset:** When y > 355: clear all 5 flags, reset position to (82, 315), set `zOrder = 0xFF` (hidden).

### Traced Movement Path

```
Start (82, 315) — sprite becomes visible
  ↓ Phase 0: Moving RIGHT at 7px/frame (anim 0)
  ↓ ~8 frames: x reaches 135
At x=136 — Phase 1: Switch to RIGHT+DOWN diagonal 7px each
  ↘ ~3 frames: y reaches 330 (while x ~= 157)
At y=331 — Phase 2: Switch to RIGHT only 7px
  → ~7 frames: x reaches 200 (y stays ~331)
At x=201 — Phase 3: Switch to DOWN only 7px
  ↓ ~4 frames: y reaches 355
At y=356 — RESET: position → (82,315), hidden
```

### Current ScummVM Implementation (room.cpp:665)

```cpp
mouse->animData[0].loopCount = 3;    // flags=0x0000 NO MOVEMENT
mouse->animData[1].loopCount = 1;    // flags=0x3FF  RIGHT+DOWN 7px
mouse->animData[2].loopCount = 1;    // flags=0x801F RIGHT 7px
mouse->animData[3].loopCount = 4;    // flags=0x3C0  DOWN 6px
```

ScummVM uses **loop-count-based** animation advancement: the sprite plays anim 0 for 3 loops (no movement), then auto-advances to anim 1 (diagonal), etc. The `passerByAnim()` function handles visibility/reset based on position.

### Differences (ScummVM vs Original)

| Aspect | Original | ScummVM |
|--------|----------|---------|
| Phase transitions | **Position-based** (x/y thresholds) | Loop-count-based (anim exhaustion) |
| Phase 0 | RIGHT 7px (anim 0, flags=0x1F) | NO MOVEMENT (anim 0, flags=0x0000) |
| Phase 3 speed | DOWN **7**px (flags=0x3E0) | DOWN **6**px (flags=0x3C0) |
| Timer mask | `0x3FF` (every 1024 ticks) | `0x3FF` (matches) |
| Reset trigger | y > 355 (position-based) | Sprite reaches blank sprite y coord |
| Path shape | RIGHT→DIAGONAL→RIGHT→DOWN | STILL→DIAGONAL→RIGHT→DOWN |

### Required Fix

The ScummVM implementation needs to be rewritten to use **position-based phase transitions** matching the original:
1. Start with `movementFlags[0] = 0x1F` (RIGHT 7px) instead of no movement
2. At x > 135: switch to anim 1 with `movementFlags[1] = 0x3FF` (RIGHT+DOWN)
3. At y > 330: switch to anim 2 with `movementFlags[2] = 0x1F` (RIGHT)
4. At x > 200: switch to anim 3 with `movementFlags[3] = 0x3E0` (DOWN 7px, not 6px)
5. At y > 355: reset position to (82, 315), hide sprite

This should be done in `frameTriggers()` or a new room-specific per-frame callback, NOT in `loadPasserByAnims()`.

---

## Room 19: Dog Peeing Animation

### Original Behavior (Ghidra)

**Handler addresses:**
- Entry Init (table 16): `0x25A68` — Sets sprite 4 `nframes[0] = 9`
- **Per-Frame Handler**: `0x115EF` (139 bytes) — Proximity-triggered animation

**Sprite involved:**
- Original index 4 / ScummVM index 2: dog sprite
- The dog sprite has 24 total frames in animation 0
- Frames 0–8: idle dog (stretching/sniffing)
- Frames 9–23: full peeing sequence

### Flow

1. **On room entry:** `nframes[0] = 9` — only first 9 frames play (idle dog loops)
2. **Per frame:** check `alfred_x_position [0xFB96] < 146 (0x92)`
   - If Alfred is too far (x ≥ 146): return (do nothing)
   - If Alfred is close enough (x < 146):
     a. Set `nframes[0] = 24` (enable full animation including peeing)
     b. **Blocking spin-wait loop:**
        - Call `process_game_state`, `setup_alfred_frame_from_state`, `render_scene`
        - Check `curFrame [base+0xD0] >= 23`
        - Repeat until the animation reaches the last frame
     c. Reset `nframes[0] = 9` (back to idle)
     d. Reset `curFrame = 0`
     e. Display text from pointer at `[0xBB70]` (dog reaction dialog)
     f. Set `alfred_target_x [0xFB9C] = 154 (0x9A)`
     g. Call `walk_to_target_and_execute_queued_action` with parameter 2

### ScummVM Implementation Status

**Not yet implemented.** Room 19 has no per-frame handler in the current ScummVM code. The dog sprite loadseloadedd with its full animation (all 24 frames). This means in ScummVM, the dog currently plays the full peeing animation on a loop, whereas in DOSBox only the 9-frame idle portion plays until Alfred walks close enough.

### Required Implementation

1. In `loadPasserByAnims()` or a room-specific init, set `sprite->animData[0].nframes = 9` for room 19's dog sprite (ScummVM index 2)
2. Implement a per-frame check: when `_alfredState.x < 146`:
   - Set `animData[0].nframes = 24`
   - Wait for `animData[0].curFrame >= 23` (blocking loop with renderScene)
   - Reset `animData[0].nframes = 9` and `animData[0].curFrame = 0`
   - Show dialog text
   - Walk Alfred to x=154

---

## Room 24: Bird Animation Control

### Original Behavior (Ghidra)

**Handler addresses:**
- Entry Init (table 18): `0x25A96` — Sets sprite 3 `numAnims = 1`
- **Per-Frame Handler**: `0x25CD7` (297 bytes) — Item-triggered animation

**Sprite involved:**
- Original index 3 / ScummVM index 1: birds sprite
- Has 4 sub-animations (numAnims could be up to 4)
- When numAnims=1, only the first animation plays (single bird idle)

### Flow

1. **On room entry:** `numAnims = 1` — only first bird animation plays
2. **Per frame:**
   a. Call `find_item_in_room_table(0x58)` — check if item 88 (spellbook) is in the room
   b. If not present: return
   c. If present AND `room24_bird_anim_done_flag [0x95F1] == 0`:
      1. Display first text from `[0xBBD8]`
      2. Call `remove_item_from_room_table(1)` — remove item from the table
      3. Set sprite 3 `numAnims = 4` — enable all bird animations
      4. **Blocking wait loop** (with delay 0x18A, render, check):
         - Wait until `curAnimIndex == 3` AND `curFrame == 3` (all anims completed)
      5. Set sprite 3 `zOrder = 0xFF` — hide birds
      6. Set `room24_bird_anim_done_flag [0x95F1] = 1`
      7. Display second text from `[0xBBDC]`
      8. **Persist state to ALFRED.1:** write 6 bytes at room entry offset + 0xA5
         - This saves the zOrder=0xFF (hidden state) back to the data file
      9. Read back from ALFRED.1 to sync runtime state
      10. Set `room24_birds_freed_flag [0xA433] = 1`

### ScummVM Implementation Status

**Partially implemented.** The spellbook (item 88) `useOnAlfred()` handler in actions.cpp opens the SpellBook UI, but there's no room 24 per-frame handler that checks for the spellbook presence and triggers the bird scatter animation. The user reports "in dosbox only the first animation is playing, in my implementation all of the animations are playing" — this is because the entry init that restricts `numAnims=1` is not implemented.

### Required Implementation

1. On room 24 load, set the birds sprite (index 1) `numAnims = 1`
2. Implement per-frame check: when item 88 (spellbook) is present in room table:
   - Show dialog
   - Remove item from table
   - Set `numAnims = 4`
   - Blocking wait until all 4 animations complete (curAnimIndex reaches 3, curFrame reaches 3)
   - Hide sprite (zOrder = -1 in ScummVM convention)
   - Show second dialog
   - Persist state change

---

## Room 5: Animation 2 (Likely Unused)

### Original Behavior (Ghidra)

**Handler addresses:**
- Entry Init (table 15): `0x25A3D` — Sets 5 conversation root flags only
- **No per-frame handler** in dispatch table at `0x485BC`
- **No render scene handler** in dispatch table at `0x48630`
- **No palette cycling handler** in dispatch table at `0x486A4`

### Entry Init Code

```asm
0x25A3D: mov ah, 1
0x25A49: mov [0x98D3], ah    ; conversation root 1
0x25A4F: mov [0x98DA], ah    ; conversation root 2
0x25A55: mov [0x98E1], ah    ; conversation root 3
0x25A5B: mov [0x98E8], ah    ; conversation root 4
0x25A61: mov [0x95EA], ah    ; conversation flag
0x25A67: ret
```

### Analysis

Room 5 has **no runtime animation control code** in any of the 4 dispatch tables. The entry init handler only enables conversation options. Animation 2 of any sprite in room 5 would only play if:

1. The animation engine automatically cycles through animations (numAnims > 1), OR
2. An action handler specifically triggers it (found no evidence of this), OR
3. Some other dispatch mechanism not found in the standard tables

Since the user confirms "animation 2 is never played either in dosbox or in my implementation," this is most likely **unused/cut content** — animation frames that exist in the data file but are never triggered by game logic.

---

## Ghidra Labels Applied

### Data Renames

| Address | Name | Purpose |
|---------|------|---------|
| 0x95EB | room9_passerby_active_flag | 1 when passer-by is visible |
| 0x95EC | room9_phase_down_only | One-shot: x > 200 triggered |
| 0x95ED | room9_phase_right_after_diag | One-shot: y > 330 triggered |
| 0x95EE | room9_phase_diagonal | One-shot: x > 135 triggered |
| 0x95EF | room9_phase_right_initial | One-shot: x < 135 triggered |
| 0x964E | room9_phone_ring_played | Prevents duplicate phone ring per anim cycle |
| 0x95F1 | room24_bird_anim_done_flag | Prevents re-triggering bird scatter |
| 0xA433 | room24_birds_freed_flag | Set after birds hidden |
| 0x95EA | room5_conversation_flag | Conversation enabled for room 5 |
| 0x98D3 | room5_conv_root_1 | Conversation root 1 |
| 0x98DA | room5_conv_root_2 | Conversation root 2 |
| 0x98E1 | room5_conv_root_3 | Conversation root 3 |
| 0x98E8 | room5_conv_root_4 | Conversation root 4 |
| 0x11738 | game_tick_counter | Frame counter used for timer triggers |
| 0xBB70 | room19_dog_text_ptr | Text pointer for dog dialog |
| 0xBBD8 | room24_bird_text_ptr_1 | First bird dialog text |
| 0xBBDC | room24_bird_text_ptr_2 | Second bird dialog text |
| 0xB854 | room_to_idle_sprite_index_table | Maps room_id → sprite index for idle NPC |
| 0x95F5 | idle_counter_spriteA | Counter for idle handler sprite A |
| 0x95F6 | idle_latch_spriteA | Latch flag for idle handler sprite A |
| 0x95F7 | idle_direction_toggle | Direction toggle for idle handler |

### Disassembly Comments Set

| Address | Summary |
|---------|---------|
| 0x115EF | Room 19 Per-Frame Handler entry |
| 0x1167A | Room 9 Render Scene Handler entry |
| 0x118AD | Shared Idle Animation Handler entry |
| 0x25CD7 | Room 24 Per-Frame Handler entry |
| 0x25A3D | Room 5 Entry Init |
| 0x25A68 | Room 19 Entry Init |
| 0x25A96 | Room 24 Entry Init |
| 0x258BD | Room 9 Entry Init |
| 0x11687 | Phone ring section start |
| 0x116FB | Passer-by timer trigger |
| 0x11735 | Phase checks begin |
| 0x11743 | Phase 3: x > 200 → DOWN |
| 0x1178A | Phase 2: y > 330 → RIGHT |
| 0x117D1 | Phase 1: x > 135 → DIAGONAL |
| 0x11818 | Phase 0: x < 135 → RIGHT (initial) |
| 0x1185E | Reset: y > 355 |
| 0x25CE9 | find_item_in_room_table call |
| 0x25D12 | remove_item_from_room_table call |
| 0x25D73 | Persist bird state to ALFRED.1 |
| 0x1BB21 | remove_item_from_room_table entry |

---

## Dispatch Table Reference

| Table | Address | Room 5 | Room 9 | Room 19 | Room 24 |
|-------|---------|--------|--------|---------|---------|
| Entry Init | 0x484E4 | #15: 0x25A3D | #4: 0x258BD, #17: 0x25A7F | #16: 0x25A68 | #18: 0x25A96 |
| Per-Frame | 0x485BC | — | — | 0x115EF | 0x25CD7 |
| Render Scene | 0x48630 | — | 0x1167A | — | — |
| Palette Cycling | 0x486A4 | — | — | — | — |
