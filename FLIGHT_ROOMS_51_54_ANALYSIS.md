# Flight Rooms 51-54: Sorcerer Spell Teleportation System

## Overview

Rooms 51, 52, 53, and 54 all share **identical handler code**. When Alfred enters any of them, a sorcerer NPC appears after a short delay, casts a spell animation, and teleports Alfred to **room 49**.

---

## Architecture

Two dispatch table entries cover all four rooms, pointing to shared functions:

| Table | Ghidra Address | Handler | Purpose |
|-------|---------------|---------|---------|
| Room Init Dispatch (`0x484E4`) | Entries 11–14 | `0x259E9` | One-time setup on room entry |
| Per-Frame Update (`0x485BC`) | Entries 6–9 | `0x113DC` | Runs every frame; manages timing and spell |

Both handlers live in unanalyzed gaps in Ghidra (no function defined — they are only reached via indirect dispatch pointer tables and were missed by auto-analysis). Disassembly comments have been set at all key addresses.

---

## Per-Room Configuration

All room-specific parameters come from a byte table at data address `0x4B7E9`, indexed by `room_id` with three sub-offsets:

| Offset | Meaning |
|--------|---------|
| `[room_id + 0xB7E9]` | NPC sprite index to enable |
| `[room_id + 0xB7ED]` | Frame count for NPC appearance animation |
| `[room_id + 0xB7F1]` | Frame count for spell cast animation |

| Room | NPC Sprite Index | Appear Anim Frames | Spell Anim Frames |
|:----:|:----------------:|:-----------------:|:-----------------:|
| 51   | 3                | 31                | 17                |
| 52   | 2                | 30                | 13                |
| 53   | 3                | 30                | 13                |
| 54   | 3                | 38                | 11                |

---

## State Variables

| Ghidra Address | Name | Description |
|---------------|------|-------------|
| `0x495DE` | `flight_active_flag` | Set to 1 on room entry. Read by `update_npc_sprite_animations`. |
| `0x495D9` | `flight_appearance_delay` | Frame threshold for NPC appearance (always **64**). |
| `0x495E0` | `flight_frame_counter` | Increments each frame; drives phase transitions. |
| `0x495DA` | `spell_animation_active` | Set to 1 when spell animation phase begins. |
| `0x495DD` | `spell_cast_triggered` | Set to 1 once spell is triggered; prevents re-entry. |
| `0x495DB` | `spell_frame_rate` | Frames between spell animation advances (always **40**). |
| `0x495DC` | `spell_frame_counter` | Counts frames within spell phase; resets each advance. |

---

## Phase-by-Phase Execution

### Phase 0 — Room Init  (`0x259E9`)

Called once when Alfred enters the room.

```
1. flight_active_flag     = 1
2. flight_appearance_delay = 0x40 (64)
3. flight_frame_counter   = 0
4. spell_animation_active = 0
5. spell_cast_triggered   = 0
6. sprite_idx = table[room_id + 0xB7E9]      ; look up NPC sprite for this room
7. sprite[sprite_idx].visible_flag = 1       ; enable the NPC
8. call 0x25BEC  (shared NPC blit handler)   ; blit 256×256 NPC overlay from [0x13254]
```

---

### Phase 1 — Wait, then NPC Appears (~64 frames ≈ 0.9 s)

Each game frame the per-frame handler runs:

```
if [room_id + 0x95D1] == 0:       ; not in dialog/conversation
    flight_frame_counter++

if flight_frame_counter >= flight_appearance_delay (64)  AND
   NOT [room_id + 0x95D1]         AND
   NOT spell_cast_triggered        AND
   sprite[sprite_idx].hidden == 0xFF:   ; sprite is still hidden
       play_ambient_sound([0x13238])           ; ambient sound for NPC entry
       call 0x2662D (appear_anim_frames, sprite_idx)  ; ← BLOCKING
```

**`0x2662D` — NPC Appearance Animation Player:**
- Allocates 162,288 byte buffer
- Reads compressed animation data from ALFRED.7 at offset `0x2DE14A` (~30 KB)
- RLE-decompresses it
- Plays `appear_anim_frames` frames (31 / 30 / 30 / 38) in a blocking loop using `render_scene` + `setup_alfred_frame_from_state`

---

### Phase 2 — Spell Trigger (~40 frames ≈ 0.6 s after appearance)

```
if flight_frame_counter >= flight_appearance_delay + 40 (= 104)  AND
   NOT spell_cast_triggered:
       spell_cast_triggered   = 1
       spell_animation_active = 1
       spell_frame_rate       = 40
       spell_frame_counter    = 0
```

---

### Phase 3 — Spell Animation

Each frame while `spell_animation_active == 1` and Alfred is not in dialog:

```
spell_frame_counter++
if spell_frame_counter >= spell_frame_rate (40):
    ; enter blocking spell animation loop:
    set sprite animation state = spell_anim_frames (17/13/13/11)
    loop:
        wait 107 game-ticks
        setup_alfred_frame_from_state()
        render_scene()
        if sprite.current_frame >= spell_anim_frames - 1: break
```

Total blocking frames: ~17 steps × 107 ticks for room 51, ~13 for 52/53, ~11 for 54.

---

### Phase 4 — Teleportation

After the spell animation completes:

```
1. Reset NPC sprite (frame=1, animation counter=0)
2. play_ambient_sound([0x1323C])                    ; second sound/anim effect
3. call 0x2662D (nframes=0, sprite_idx=1)           ; "teleport flash" effect
4. spell_animation_active = 0
5. spell_frame_counter    = 0
6. spell_cast_triggered   = 0
7. alfred_spawn_x         = 0x126 (294)
8. alfred_spawn_y         = 0x183 (387)
9. alfred_facing          = 3
10. load_room_and_init_alfred(49)                   ; teleport to room 49
```

Alfred spawns at coordinates (294, 387) facing direction 3 (down-left) in room 49.

---

## Timing Summary

Approximate timings at ~70 FPS:

| Event | Frame | Time |
|-------|:-----:|:----:|
| Enter room | 0 | 0 s |
| NPC appearance animation starts | 64 | ~0.9 s |
| NPC appearance animation (blocking) | 64+ | ~1–2 s depending on room |
| Spell flag triggers | 104 | ~0.5 s after appearance ends |
| Spell frame rate counter fills | 144 | ~0.6 s later |
| Spell animation (blocking) | 144+ | ~1–2 s depending on room |
| **Teleport to room 49** | — | immediately after spell |

Total from room entry to teleport: **~4–6 seconds** depending on room.

---

## Called Functions

| Address | Name | Role |
|---------|------|------|
| `0x259E9` | *(unnamed — flight_room_init_handler)* | Room entry init |
| `0x113DC` | *(unnamed — flight_room_perframe_handler)* | Per-frame driver |
| `0x25BEC` | *(unnamed — shared_npc_blit_handler)* | Blits NPC overlay on room entry |
| `0x2662D` | *(unnamed — load_and_play_npc_animation)* | Blocking NPC animation player |
| `0x27CE1` | `play_ambient_sound` | Plays ambient/NPC sound |
| `0x147C9` | `setup_alfred_frame_from_state` | Updates Alfred render state |
| `0x15E4C` | `render_scene` | Full scene render (called per animation frame) |
| `0x152F5` | `load_room_and_init_alfred` | Room loader / teleporter |

---

## Ghidra Annotations Added

- **Disassembly comments** at: `0x259E9`, `0x113DC`, `0x2662D`, `0x113FE`, `0x11439`, `0x11499`, `0x114B9`, `0x114D2`, `0x11526`, `0x1156D`, `0x115C5`, `0x115E0`
- **Decompiler comments** at: `0x495DA`, `0x495DB`, `0x495DC`, `0x495DD`, `0x495DE`, `0x495D9`, `0x495E0`, `0x4B7E9`
- **Renamed** `display_alfred_talking` → `shared_epilogue_pop_esi_edx_ecx_ebx` (it is a shared stack cleanup epilogue, not an Alfred dialogue function)
