# Room 39 PICKUP Hotspot 700 — "Girls in Pool" Sequence Analysis

## Overview

When the player executes PICKUP on hotspot 700 ("girls in pool") in room 39, a multi-phase
cutscene plays: the swimmers dive under water, an NPC walks in from the right side of the
screen, and a conversation triggers that spans rooms 39 → 40 → 41.

**Handler address:** Ghidra `0x20781` (not auto-defined as function), file offset `0x24981` in `JUEGO.EXE`  
**Dispatch table:** PICKUP table at `0x47D24`, entry 46: `extra_id=700`, `func_ptr=0x10781`  
**Handler size:** 1174 bytes (222 instructions), ends with `jmp 0x13A66` (shared register-restore epilog)

---

## Room 39 Sprite Layout (Before PICKUP)

Room 39 has **9 sprites** (raw count; 7 game sprites starting at index 2):

| Sprite | Position | Size | Frames | Z | Extra | Flags | Role |
|--------|----------|------|--------|---|-------|-------|------|
| 0 | (0,0) | 0×0 | — | 0 | 0 | — | System (unused) |
| 1 | (0,0) | 0×0 | — | 0 | 0 | — | System (unused) |
| **2** | **(640, 273)** | **43×117** | **8** | **200** | **650** | **0x10 (TALK)** | **NPC — starts OFF-SCREEN right** |
| 3 | (0, 212) | 99×188 | 2 | 250 | 700 | 0x00 | Pool girl (left, large) |
| 4 | (533, 126) | 99×125 | 2 | 250 | 700 | 0x00 | Pool girl (right) |
| **5** | **(130, 208)** | **107×78** | **1** | **250** | **700** | **0x08** | **Swimmer (overwritten by handler)** |
| **6** | **(201, 167)** | **68×38** | **[2,5,1]** | **250** | **700** | **0x08** | **Water effect (overwritten)** |
| **7** | **(317, 139)** | **66×67** | **4** | **250** | **700** | **0x08** | **Swimmer 2 (overwritten)** |
| **8** | **(280, 230)** | **42×36** | **2** | **250** | **700** | **0x08** | **Water effect 2 (overwritten)** |

Key observations:
- **Sprite 2** (the NPC, extra 650) has X=640 — exactly at the right screen edge, invisible until its movement flag is set.
- **Sprites 3–8** all share `extra_id=700` — the "girls in pool" hotspot.
- **Sprites 5–8** have `flags=0x08` and get completely reconfigured by the handler for the diving animation.

---

## Sequence of Events

### Phase 1: Audio Setup (0x20790–0x207C1)

1. **Stop current sound** — `init_or_stop_sound()` at `0x29037`
2. **Play CD audio track** — Track number = `cd_audio_track_base + 27`. Calls `play_cd_audio_track()` at `0x28d32`
3. **Fade CD audio** — Cross-fade transition via `0x2942d` and `0x28fd5`

### Phase 2: Load Animation Data from ALFRED.7 (0x207C6–0x20802)

```
Source: ALFRED.7 offset 0x1613CE
Read size: 26,330 bytes (RLE compressed)
Decompressed size: ~174,101 bytes
Destination: sprite_pixel_buffer + 0x18F4E
```

This loads **BUDA 107 "NADADORAS"** (swimmers), which consists of:
- Palette data at `0x1610CE` (768 bytes, valid VGA 6-bit palette) — loaded separately during room init if `DAT_0005178c == 0x1C`
- Compressed sprite data at `0x1613CE` (26,330 bytes) — decompressed via `decompress_rle_block()`

The decompressed data is placed at `sprite_pixel_buffer + 0x18F4E`, effectively overwriting the area used by sprites 5–8.

### Phase 3: Compute Sprite Data Pointers (0x20807–0x20846)

The handler chains sprite pixel data pointers based on sprite 5's existing pointer:

```
sprite6.pixel_data = sprite5.pixel_data + 0x11FB8   (73,656 bytes = 93×88×9 frames)
sprite7.pixel_data = sprite6.pixel_data + 0x39A4    (14,756 bytes = 68×31×7 frames)
sprite8.pixel_data = sprite7.pixel_data + 0x107D9   (67,545 bytes = 79×95×9 frames)
```

### Phase 4: Configure 4 Sprite Animations (0x20851–0x20AC4)

All four sprites are reconfigured with new dimensions, frame counts, and movement data.
All have `disable_after_sequence = 1` (auto-hide when complete).

#### Sprite 5 — Main Swimmer Diving (moves diagonally)

| Field | Struct Offset | Value | Notes |
|-------|--------------|-------|-------|
| x_pos | +0x0A | original **+3** | Slight rightward nudge |
| y_pos | +0x0C | original **−17** | Lifted upward |
| width | +0x0E | **93** | — |
| height | +0x0F | **88** | — |
| stride | +0x10 | **8,184** (93×88) | 1 byte/pixel uncompressed |
| num_sequences | +0x12 | **1** | Single animation sequence |
| frames_in_seq[0] | +0x14 | **9** | 9 frames of diving |
| frame_delay[0] | +0x1C | **1** | 1 tick per frame (fast) |
| movement_flags[0] | +0x22 | **0x02FF** | See below |
| disable_after | +0x31 | **1** | Auto-hide when done |

**Movement flags 0x02FF decoded:**
```
Bits 0-2  = 7    → movement_amount = 7 pixels
Bit  3    = 1    → X movement ENABLED
Bit  4    = 1    → X direction = RIGHT (+)
Bits 5-7  = 7    → Y movement speed = 7
Bit  8    = 0    → Y direction = UP (−)
Bit  9    = 1    → Y movement ENABLED
```
**Result:** Each frame, sprite moves **+7px right** and **−7px up**.  
Over 9 frames: **total displacement = +63px right, −63px up** (diagonal dive into water).

#### Sprite 6 — Water Splash / Ripples (stationary)

| Field | Value | Notes |
|-------|-------|-------|
| x_pos | original **+1** | Minimal adjustment |
| width × height | **68 × 31** | Small horizontal strip |
| stride | **2,108** (68×31) | — |
| frames | **7** | 7 frames of splash animation |
| frame_delay | **1** | — |
| movement_flags | **none set** | Stationary |
| disable_after | **1** | Auto-hide |

Original position: (201, 167) → adjusted to (202, 167). Plays near the water surface.

#### Sprite 7 — Second Swimmer (stationary, position adjusted)

| Field | Value | Notes |
|-------|-------|-------|
| x_pos | original **−14** | Shifted left |
| y_pos | original **−18** | Shifted up |
| width × height | **79 × 95** | Large swimmer sprite |
| stride | **7,505** (79×95) | — |
| frames | **9** | 9 frames |
| frame_delay | **1** | — |
| movement_flags | **none set** | Stationary (plays in place) |
| disable_after | **1** | Auto-hide |

Original position: (317, 139) → adjusted to **(303, 121)**. This is the second girl's diving animation, playing in place with frame-by-frame animation showing the dive motion.

#### Sprite 8 — Small Water Effect (stationary, position adjusted)

| Field | Value | Notes |
|-------|-------|-------|
| x_pos | original **−1** | Minimal adjustment |
| y_pos | original **−8** | Shifted up slightly |
| width × height | **54 × 42** | Small sprite |
| stride | **2,268** (54×42) | — |
| frames | **8** | 8 frames |
| frame_delay | **1** | — |
| movement_flags | **none set** | Stationary |
| disable_after | **1** | Auto-hide |

Original position: (280, 230) → adjusted to **(279, 222)**. Secondary water disturbance effect.

### Phase 5: Play Swimming Animation Loop (0x20ACB–0x20B2E)

```c
do {
    wait_or_process_input(0x15F);   // delay ~351
    setup_alfred_frame_from_state();
    render_scene(0);
    process_game_state(0);
} while (sprite5.z_depth != 0xFF ||    // sprite 5 still playing
         sprite6.z_depth != 0xFF ||    // sprite 6 still playing
         sprite7.z_depth != 0xFF ||    // sprite 7 still playing
         sprite8.z_depth != 0xFF);     // sprite 8 still playing
```

The render loop continues until **all four sprites** have auto-disabled (z_depth set to 0xFF by the animation engine when the last frame completes). With 7–9 frames at 1-tick delay each, the animation completes in ~9 render cycles.

During this phase, the `update_npc_sprite_animations()` function (called by `render_scene`) processes each sprite's movement flags, advancing frames and applying per-frame X/Y movement for sprite 5.

### Phase 6: NPC Walks Into Scene (0x20B30–0x20B6B)

After all swimming animations complete:

1. **Set sprite 2 movement:** `sprite2.movement_flags[0] = 0x14`

   ```
   0x14 = 0b 00010100
   Bit  4 = 1  → X movement ENABLED  
   Bit  3 = 0  → X direction = LEFT (−)
   Bits 0-2 = 4 → movement_amount = 4 pixels
   ```
   **Result:** Sprite 2 moves **−4px left per frame** (NPC walks in from right edge).

2. **Wait loop:**
   ```c
   target_x = alfred_x_position + 70;
   do {
       wait_or_process_input(0x160);    // delay ~352
       setup_alfred_frame_from_state();
       render_scene(0);                 // (which calls update_npc_sprite_animations → moves sprite 2)
       process_game_state(0);
   } while (sprite2.x_pos > target_x);  // wait until NPC reaches Alfred+70px
   ```

   Sprite 2 starts at X=640 (off the right edge of the 640px screen). It walks left at 4px/frame until reaching `alfred_x + 70`. For example, if Alfred is at X=200, the NPC stops at X=270.

3. **Stop NPC movement:** `sprite2.movement_flags[0] = 0` (clear all movement)

### Phase 7: Restore Data & Begin Conversation (0x20B6D–0x20BA6)

1. **Restore sprite pixel data:** `memcpy(sprite_pixel_buffer, sprite_data_backup_ptr, 5031)`.  
   5031 = sprite 2's stride (43×117 = one full frame). This restores sprite 2's pixel data to ensure correct rendering for the conversation.

2. **Reset sprite 2 for conversation pose:**
   - `sprite2.frames_in_seq[0] = 1` (reduce to 1 frame — standing still)
   - `sprite2.current_frame = 0` (reset to frame 0)

3. **Trigger conversation:** `trigger_conversation_with_sprite(mode=2, sprite_index=0)` at `0x18dce`.  
   This walks Alfred to the NPC's talk position (computed from the ALFRED.2 header data) and calls `handle_conversation_tree()`.

### Phase 8: Transition to Room 40 (0x20BA6–0x20BD7)

1. **Fade palette to black** — `fade_palette_to_black()` at `0x1b8b3`
2. **Set Alfred spawn position:**
   - `alfred_x_position = 271` (0x10F)
   - `alfred_y_position = 385` (0x181)
   - `alfred_facing_direction = 3` (facing away from camera)
3. **Load room 40** (0x28) — `load_room_and_init_alfred(40, 0)` at `0x152f5`
4. **Continue conversation:** `trigger_conversation_with_sprite(mode=2, sprite_index=0)`

### Phase 9: Transition to Room 41 (0x20BDC–0x20C12)

1. **Fade palette to black** again
2. **Set Alfred spawn position:**
   - `alfred_x_position = 208` (0xD0)
   - `alfred_y_position = 389` (0x185)
   - `alfred_facing_direction = 3` (facing away)
3. **Load room 41** (0x29) — `load_room_and_init_alfred(41, 0)`
4. **Continue conversation:** `trigger_conversation_with_sprite(mode=2, sprite_index=0)`
5. **Return** via shared epilog at `0x13A66` (POP EDI/ESI/EDX/ECX/EBX/RET)

---

## ALFRED.7 Data Source

**BUDA 107 — "NADADORAS" (Swimmers)**

| Component | ALFRED.7 Offset | Size | Purpose |
|-----------|----------------|------|---------|
| BUDA marker | 0x1610CA | 4 bytes | "BUDA" sentinel |
| VGA Palette | 0x1610CE | 768 bytes | 256-color palette (values 0–63) |
| RLE data | 0x1613CE | 26,330 bytes | Compressed animation frames |

Decompressed animation blocks (total ~174,101 bytes):

| Block | Sprite | Dimensions | Frames | Frame Size | Total Size |
|-------|--------|-----------|--------|------------|------------|
| 0 | 5 | 93 × 88 | 9 | 8,184 | 73,656 |
| 1 | 6 | 68 × 31 | 7 | 2,108 | 14,756 |
| 2 | 7 | 79 × 95 | 9 | 7,505 | 67,545 |
| 3 | 8 | 54 × 42 | 8 | 2,268 | 18,144 |

---

## Visual Summary

```
Before PICKUP:                          During swimming animation:

  ┌────────────────────────────┐         ┌────────────────────────────┐
  │        Pool Scene          │         │        Pool Scene          │
  │                            │         │    Spr7         Spr5 ↗    │
  │   Spr5  Spr6   Spr7       │    →    │   (303,121)  (133→196,    │
  │  (130,208) (201,167) (317,139)│      │    79×95     191→128)     │
  │        Spr8                │         │         Spr6  93×88       │
  │       (280,230)            │         │       (202,167) Spr8      │
  │  Spr3          Spr4       │         │        68×31  (279,222)   │
  │  (0,212)      (533,126)    │         │               54×42      │
  │                      Spr2→ │640      │                           │
  └────────────────────────────┘         └────────────────────────────┘

  After animations complete:              NPC arrives:

  ┌────────────────────────────┐         ┌────────────────────────────┐
  │        Pool Scene          │         │        Pool Scene          │
  │  (sprites 5-8 disabled)    │         │                            │
  │                            │         │                            │
  │                            │    →    │    Alfred    NPC           │
  │                            │         │      ↕70px↕               │
  │                       ←Spr2│         │             (walking, 4px/ │
  │                    walks in│         │              stops nearby) │
  │                            │         │                            │
  └────────────────────────────┘         └────────────────────────────┘

  Then: Conversation → Fade → Room 40 → Fade → Room 41 → Return
```

---

## Sprite Structure Reference

```
SPRITE STRUCTURE (44 bytes = 0x2C per sprite, at room_sprite_data_ptr + index×0x2C):
+0x00  (6 bytes)   Header / pointers
+0x06  (4 bytes)   Pixel data pointer
+0x0A  (2 bytes)   X position (signed short)
+0x0C  (2 bytes)   Y position (signed short)
+0x0E  (1 byte)    Width
+0x0F  (1 byte)    Height
+0x10  (2 bytes)   Stride (bytes per frame = width × height)
+0x12  (1 byte)    Number of animation sequences
+0x13  (1 byte)    Current animation sequence index
+0x14  (4 bytes)   Frames per sequence [4 max] (1 byte each)
+0x18  (4 bytes)   Loop count per sequence (0xFF = no loop)
+0x1C  (4 bytes)   Frame delays [4 max] (1 byte each)
+0x20  (1 byte)    Current frame index
+0x21  (1 byte)    Z-depth / visibility (0xFF = disabled/hidden)
+0x22  (8 bytes)   Movement flags per sequence [4 max] (2 bytes each)
+0x2A  (2 bytes)   Extra ID
+0x2C  (1 byte)    Action flags (0x10=TALK, 0x08=clickable, etc.)
+0x2D  (1 byte)    Frame delay counter
+0x2E  (1 byte)    Loop counter
+0x31  (1 byte)    Disable after sequence flag (1 = auto-set z_depth to 0xFF)

MOVEMENT FLAGS (16-bit, at +0x22 indexed by sequence):
Bits 0-2:   Movement amount (0–7 pixels per frame)
Bit 3:      X direction flag: 0=left/subtract, 1=right/add
Bit 4:      X movement ENABLE
Bits 5-7:   Y movement speed (0–7)
Bit 8:      Y direction flag: 0=up/subtract, 1=down/add
Bit 9:      Y movement ENABLE
Bits 10-12: (unused)
Bit 13:     Z-depth direction: 0=back, 1=forward
Bit 14:     Z-depth movement ENABLE
```

---

## Key Globals Referenced

| Address (Ghidra) | Name | Purpose |
|-------------------|------|---------|
| 0x4FAC8 | `room_sprite_data_ptr` | Pointer to room's sprite structure array |
| 0x4FABC | `sprite_pixel_buffer` | Base of decompressed sprite pixel data |
| 0x4FAD0 | `sprite_data_backup_ptr` | Backup copy for restoration |
| 0x4FB96 | `alfred_x_position` | Alfred's screen X coordinate |
| 0x4FB98 | `alfred_y_position` | Alfred's screen Y coordinate |
| 0x4FB9A | `alfred_facing_direction` | 0=right, 1=left, 2=toward cam, 3=away |
| 0x4C240 | `cd_audio_track_base` | Base offset for CD audio track number |
| 0x4F908 | `file_handle_alfred7` | File handle for ALFRED.7 |
