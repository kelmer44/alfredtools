# Pyramid Collapse Sequence Analysis

Complete reverse-engineering analysis of the Room 37 stone pickup → earthquake cutscene → Room 36 pyramid collapse animation sequence.

## Overview

When Alfred picks up the stone (hotspot 90) in Room 37, three things happen in sequence:
1. **Room 37**: Stone is visually removed (sticker overlay), ingredient counter incremented, earthquake cutscene plays, Alfred walks to exit
2. **Room 36 init**: Collapse trigger flag is set when entering room 36 after stone pickup
3. **Room 36 per-frame**: Full collapse animation plays — background tiles rearranged, NPC sprite walks away, persistent changes saved

## Address Conventions

| Convention | Formula |
|---|---|
| Code: EXE file offset | `ghidra_addr + 0x4200` |
| Data: EXE file offset | `data_addr + 0x3200` (for data segment addresses ≥ 0x40000) |
| Text index from BSS pointer | `(bss_addr - 0xB9B4) / 4` |

---

## Part 1: Room 37 — Stone Pickup (Hotspot 90)

### Handler at Ghidra 0x2044F

**Trigger**: PICKUP action on hotspot 90 (stone on pyramid in room 37)

**Sequence**:
1. Render sticker overlay (ALFRED.6 sticker index **116**, offset 0x6C2C9, size 0x584) — visually removes the stone from the pyramid
2. Set flag `[0x1176A] = 1` → pyramid collapse trigger (FLAG_PIRAMIDE_JODIDA)
3. Set flag `[0x961D] = 1` → temporary flag cleared on room re-entry
4. Increment `[0x964F]` → ingredient counter (FLAG_INGREDIENTES_CONSEGUIDOS)
5. Display ingredient text: `_ingameTexts[NOERAAUTENTICO + counter]` (table at BSS `[eax*4 + 0xBC64]`)
6. Call **FUN_26fab** (earthquake cutscene trigger)
7. Display text `AYAYAY` (BSS 0xBAFC, index 82)
8. Display text `NADIELOHAVISTO` (BSS 0xBAF8, index 81)
9. Set Alfred direction = LEFT (2), walk target = (592, 306)
10. Jump to shared walk-and-return epilogue at 0x11662

### FUN_26fab at Ghidra 0x26FAB — Earthquake Cutscene Trigger

**Purpose**: Plays the CD earthquake cutscene if CD audio is available

**Sequence**:
1. Check `[0x13015]` (CD audio flag, default 92 = nonzero → CD present)
2. If nonzero:
   - Render current frame
   - Display text `DEMO_FINAL` (BSS 0xBC8C, index 182) — note: this text says "Bien... Hasta aquí puedes ver del fantástico juego ALFRED PELROCK..." which is the demo end message. This seems like a demo-only path.
   - Fall through to cleanup code at 0x26FE0: close file handles, cleanup room audio, init/stop sound
   - Call `play_cd_cutscene_by_index(3)` → **FUN_38a84** with parameter 3
   - Wait using table value at `[0xC224 + 6*4]`
   - Wait 400 ticks
   - Call FUN_2a2d2(0) → return
3. If zero (no CD): skip cutscene entirely

**Key insight**: The "earthquake effect" in the original game is a **prerendered CD cutscene** (index 3), not programmatic screen shaking. This cutscene uses VESA BIOS extensions (`INT 10h` calls: `0x1000` Return SuperVGA Mode, `0x1001` Get SuperVGA Mode Info, `0x1010` Get/Set Display Start) to play back a fullscreen video.

### play_cd_cutscene_by_index (FUN_38a84, renamed in Ghidra)

- Calls `resolve_cutscene_track_index` (FUN_38b6e) — for param=3, returns 3 directly
- Searches cutscene table at `CUTSCENE_TRACK_TABLE` (DAT_0004c344)
- Calls `init_cutscene_playback_state` (FUN_38d03) — sets width/height, IEEE 754 scaling (0x3F800000 = 1.0)
- Calls `init_cutscene_display_mode` (FUN_38eb5) — VESA mode setup, palette initialization

---

## Part 2: Room 36 Init — Collapse Trigger Setup

### Handler at Ghidra 0x2592B (room 36 entry handler)

**Sequence**:
1. Set sprite z-order: `sprite[0x6C] = 1`
2. If `[0x1176A] != 0` (FLAG_PIRAMIDE_JODIDA set):
   - Clear `[0x1176A] = 0`
   - Set `[0x95CE] = 1` → collapse animation trigger

This converts the persistent "stone was taken" flag into the runtime "play collapse" signal.

---

## Part 3: Room 36 Per-Frame — Collapse Animation

### Handler at Ghidra 0x1098F (room 36 per-frame handler)

This handler runs every frame while in room 36. It implements a multi-phase collapse sequence using state flags.

### Phase 0: Initialization (runs once)

**Condition**: `[0x95CE] != 0 && [0x95CC] == 0`

**Actions**:
- Clear `[0x1176A] = 0`
- Set `[0x95CC] = 1` (init done flag)
- Set `sprite[0xD1] = 0xFE` (sprite animation heading)

### Phase 1: Main Animation (runs once)

**Condition**: `[0x95CC] != 0 && [0x95CD] == 0`

**Actions**:

1. **Hide Alfred**: `sprite[0x79] = 0xFF` (make invisible). In ScummVM: `_alfredState.setState(ALFRED_SKIP_DRAWING)`
2. **Play ambient sound**: from room SFX data
3. **Wait for sprite frame**: Loop `process_game_state + setup_frame + render_scene` until NPC sprite frame == 5
4. **Background tile copy 1** (rubble falls onto pyramid):
   - Source: `buffer[FADC] + 0x16B70` → pixel (240, 145) in some buffer
   - Destination: `buffer[FABC] + 0x547E` → pixel (510, 33) in background
   - Size: 99 × 45 pixels, stride 640
   - Effect: copies a rubble texture patch onto the pyramid top area
5. **Background tile copy 2** (additional rubble shift):
   - Source: `buffer[FABC] + 0x65E5` → pixel (485, 40)
   - Destination: `buffer[FABC] + 0x0EE2` → pixel (610, 5)
   - Size: 4455 bytes (memcpy, ~7 rows)
   - Effect: shifts rubble data within the background buffer
6. **Set NPC sprite animation**: heading = 0xC8, visibility = 1, frame = 0
7. **Set completion flags**: `[0x95CD] = 1`, `[0xA1FC] = 1`
8. **Display dialogue**: text from `YANOSEHACEONCOMOANTES` (BSS 0xBAF4, index 80): *"Hay que ver... Ya no se hacen las cosas como antes"*

### Phase 2: NPC 3-Phase Walk

After the collapse animation, the NPC (guard/worker) walks away in three segments:

| Segment | Heading | Condition | Movement |
|---------|---------|-----------|----------|
| 1 | 0x1C (28) | Until X ≥ 339 | subtract 25 from Y each frame |
| 2 | 0x340 (832 → ~112° mod 360) | Until Y ≥ 206 | sprite walks on its own |
| 3 | 0x14 (20) | Until X ≤ 307 | sprite walks on its own |

After walk completes:
- Set heading = 0 (stopped)
- Display text `POR5MINUTOS` (BSS 0xBB54, index 104): *"¿Será posible? Por 5 minutos que dejo libre el puesto..."*

### Phase 3: Persistent Changes to ALFRED.1

These writes permanently modify the room data file so the collapse state persists across saves/loads:

1. **Hide NPC sprite** — write 6 bytes at room_data + 0x1C1:
   - Effectively disables the sprite at index referenced by `[0xFB70]`

2. **Modify exit data** — write 6 bytes at room_data + 0x1DD:
   - Purpose: likely modifies exit properties (within exit data at 0x1BF)

3. **Hide hotspot** — write 9 bytes at room_data + 0x48F:
   - Sets hotspot type = 4, position = (640, 400) — moves it offscreen
   - This hides the "stone" hotspot permanently

### Phase 4: Final Dialogue and Exit

- Display text `TALUEGOLUCAS` (BSS 0xBB58, index 105): *"Hasta luego, Lucas"*
- Set walk target = (603, 212)
- Render scene + walk to target

---

## Room 37/2 Shared Handler at 0x25C22

On re-entering room 37 (or room 2), this handler clears `[0x961D] = 0`.

---

## Flag Summary

| Address | ScummVM Flag | Purpose |
|---------|-------------|---------|
| `[0x1176A]` | FLAG_PIRAMIDE_JODIDA (23) | Stone taken → triggers collapse on next room 36 entry |
| `[0x95CE]` | FLAG_PIRAMIDE_JODIDA2 (24) | Runtime: collapse animation should start |
| `[0x95CC]` | (local/temp) | Collapse init done |
| `[0x95CD]` | (local/temp) | Collapse animation done |
| `[0x964F]` | FLAG_INGREDIENTES_CONSEGUIDOS (48) | Ingredient counter |
| `[0x961D]` | (local/temp) | Cleared on room 37 re-entry |
| `[0x13015]` | (system) | CD audio available flag |
| `[0xA1FC]` | (unknown) | Set after collapse — purpose unknown |

---

## Sound Effects

| Sound | File | Index | Usage |
|-------|------|-------|-------|
| Earthquake rumble | QUAKE2ZZ.SMP | 81 | Play during earthquake/collapse |
| Rocks falling | ROCKSZZZ.SMP | 82 | Play during rubble animation |

---

## Sticker Data

- **Sticker index**: 116
- **ALFRED.6 offset**: 0x6C2C9
- **Size**: 0x584 (1412 bytes including 6-byte header: x, y, w, h)
- **Purpose**: Overlayed on room 37 to visually remove the stone from the pyramid surface
- **Room assignment in pegatina_rooms**: Currently 41 (may need to be corrected to 37)

---

## ScummVM Implementation Proposal

### 1. Expand `pickUpStone()` (actions.cpp)

```cpp
void PelrockEngine::pickUpStone(HotSpot *hotspot) {
    // 1. Render stone removal sticker
    _room->addSticker(116, PERSIST_BOTH);

    // 2. Set pyramid collapse trigger
    _state->setFlag(FLAG_PIRAMIDE_JODIDA, true);

    // 3. Increment ingredient and show text
    checkIngredients();

    // 4. Play earthquake effect
    //    Original game plays CD cutscene #3 via play_cd_cutscene_by_index(3)
    //    For ScummVM: simulate with screen shake + sound
    _sound->playSound(81); // QUAKE2ZZ.SMP - earthquake rumble

    // Screen shake effect (alternating offsets for ~2 seconds)
    for (int i = 0; i < 40 && !shouldQuit(); i++) {
        int shakeX = (i % 4 < 2) ? 3 : -3;
        int shakeY = (i % 2 == 0) ? 2 : -2;
        g_system->setShakePos(shakeX, shakeY);
        renderScene(OVERLAY_NONE);
        _screen->update();
        g_system->delayMillis(50);
    }
    g_system->setShakePos(0, 0); // Reset shake

    // 5. Post-earthquake dialogue
    _dialog->say(_res->_ingameTexts[AYAYAY]);       // "Ay, ay, ay!"
    _dialog->say(_res->_ingameTexts[NADIELOHAVISTO]); // "Bueno...Nadie lo ha visto"

    // 6. Walk Alfred to exit
    _alfredState.direction = ALFRED_LEFT;
    walkTo(592, 306);
}
```

### 2. Add Room 36 Entry Handler in `doExtraActions()`

```cpp
case 36: {
    // Set NPC sprite z-order
    Sprite *npcSprite = _room->findSpriteByIndex(0); // NPC guard
    if (npcSprite) {
        npcSprite->zOrder = 1;
    }

    // If stone was just taken, trigger collapse
    if (_state->getFlag(FLAG_PIRAMIDE_JODIDA)) {
        _state->setFlag(FLAG_PIRAMIDE_JODIDA, false);
        _state->setFlag(FLAG_PIRAMIDE_JODIDA2, true);
        pyramidCollapseAnimation();
    }
    break;
}
```

### 3. Implement `pyramidCollapseAnimation()` — New Function

```cpp
void PelrockEngine::pyramidCollapseAnimation() {
    Sprite *npcSprite = _room->findSpriteByIndex(0); // The NPC guard

    // --- Phase 1: Wait for sprite frame 5 while playing sound ---
    _alfredState.setState(ALFRED_SKIP_DRAWING); // Hide Alfred
    _sound->playSound(_room->_roomSfx[0]); // Ambient/earthquake sound

    // Wait for NPC animation to reach frame 5
    while (!shouldQuit()) {
        _events->pollEvent();
        bool didRender = renderScene(OVERLAY_NONE);
        if (didRender && npcSprite->animData[0].curFrame >= 5) {
            break;
        }
        _screen->update();
        g_system->delayMillis(10);
    }

    // --- Phase 2: Background tile copy (rubble collapse visual) ---
    // Copy 1: 99x45 block from (240,145) to (510,33)
    // In original: source buffer[FADC] is a secondary buffer, dest [FABC] is background
    // In ScummVM: modify _currentBackground directly
    {
        const int srcX = 240, srcY = 145;
        const int dstX = 510, dstY = 33;
        const int copyW = 99, copyH = 45;
        for (int row = 0; row < copyH; row++) {
            memcpy(
                _currentBackground + (dstY + row) * 640 + dstX,
                _currentBackground + (srcY + row) * 640 + srcX,
                copyW
            );
        }
    }

    // Copy 2: 4455 bytes from offset 0x65E5 to 0x0EE2
    // (485,40) → (610,5)
    {
        // Note: memmove since regions may overlap
        memmove(
            _currentBackground + 0x0EE2,
            _currentBackground + 0x65E5,
            4455
        );
    }

    // --- Phase 3: NPC sprite collapse reaction animation ---
    if (npcSprite) {
        npcSprite->animData[0].movementFlags = 0xC8; // heading
        npcSprite->zOrder = 1;
        npcSprite->animData[0].curFrame = 0;
    }

    _alfredState.setState(ALFRED_IDLE); // Show Alfred again

    // Display collapse dialogue
    _dialog->say(_res->_ingameTexts[YANOSEHACEONCOMOANTES]);
    // "Hay que ver... Ya no se hacen las cosas como antes"

    // --- Phase 4: NPC 3-phase walk ---
    // Phase 4a: heading 0x1C, subtract 25 from Y, until X >= 339
    if (npcSprite) {
        npcSprite->animData[0].movementFlags = 0x1C;
        while (!shouldQuit() && npcSprite->x < 339) {
            _events->pollEvent();
            bool didRender = renderScene(OVERLAY_NONE);
            if (didRender) {
                npcSprite->y -= 25;
            }
            _screen->update();
            g_system->delayMillis(10);
        }

        // Phase 4b: heading 0x340, until Y >= 206
        npcSprite->animData[0].movementFlags = 0x340;
        while (!shouldQuit() && npcSprite->y < 206) {
            _events->pollEvent();
            renderScene(OVERLAY_NONE);
            _screen->update();
            g_system->delayMillis(10);
        }

        // Phase 4c: heading 0x14, until X <= 307
        npcSprite->animData[0].movementFlags = 0x14;
        while (!shouldQuit() && npcSprite->x > 307) {
            _events->pollEvent();
            renderScene(OVERLAY_NONE);
            _screen->update();
            g_system->delayMillis(10);
        }

        // Stop NPC
        npcSprite->animData[0].movementFlags = 0;
    }

    // NPC dialogue
    _dialog->say(_res->_ingameTexts[POR5MINUTOS]);
    // "¿Será posible? Por 5 minutos que dejo libre el puesto..."

    // --- Phase 5: Persist changes ---
    // Hide NPC sprite permanently
    _room->disableSprite(36, 0, PERSIST_BOTH);

    // Hide stone hotspot (move to offscreen 640,400)
    // Find the hotspot and modify it
    for (uint i = 0; i < _room->_currentRoomHotspots.size(); i++) {
        HotSpot &hs = _room->_currentRoomHotspots[i];
        // The hotspot at room_data+0x48F corresponds to a specific hotspot
        // Check by extra ID or position
        if (hs.extra == /* stone hotspot extra */ -1) {
            hs.x = 640;
            hs.y = 400;
            _room->changeHotspot(36, hs, PERSIST_BOTH);
            break;
        }
    }

    // Final dialogue
    _dialog->say(_res->_ingameTexts[TALUEGOLUCAS]);
    // "Hasta luego, Lucas"

    // Walk Alfred to exit position
    walkTo(603, 212);
}
```

### 4. Add Room 37 Re-entry Handler

```cpp
case 37: {
    // Clear temporary flag on room re-entry (original: [0x961D] = 0)
    // This is handled by the shared room 37/2 handler at 0x25C22
    break;
}
```

### 5. Header Declaration (pelrock.h)

Add to the `PelrockEngine` class:
```cpp
void pyramidCollapseAnimation();
```

### Notes and Open Questions

1. **Background copy source buffer**: The original uses two separate buffers (`[FADC]` and `[FABC]`). Buffer `[FADC]` might be a secondary/shadow buffer. In ScummVM, we might need to use `_currentBackground` as the main buffer and load the room's shadow layer from ALFRED.5 as the source for Copy 1. This needs verification.

2. **Sticker room assignment**: Sticker 116 is assigned to room 41 in `pegatina_rooms[]`. If it should be room 37 for persistent display, the table entry needs correction.

3. **NPC sprite index**: Sprite 0 in room 36 is the NPC guard. The ScummVM code already has a special case at `room.cpp:984` that caps sprite 0's animation to 1 frame on load (keeps it static until the collapse triggers it). This confirms sprite 0 is the correct target.

4. **Hotspot identification**: The stone hotspot at room_data+0x48F needs to be identified by its extra ID in the ScummVM room data.

5. **Second background copy**: The `memmove` of 4455 bytes between buffer offsets 0x65E5 and 0x0EE2 might cause visual artifacts if the source is actually from ALFRED.5 shadow data. The exact buffer identities at `[FADC]` and `[FABC]` should be verified in Ghidra.

6. **CD cutscene path**: The FUN_26fab path with `[0x13015]!=0` appears to be the demo-only path (shows DEMO_FINAL text). In the full game, the earthquake may be handled differently, or the CD cutscene plays the quake effect. The flag check and the DEMO_FINAL text coexistence needs further investigation.

---

## Ghidra Annotations Made

### Functions Renamed
| Address | Old Name | New Name |
|---------|----------|----------|
| 0x38a84 | FUN_38a84 | play_cd_cutscene_by_index |
| 0x38b6e | FUN_38b6e | resolve_cutscene_track_index |
| 0x38d03 | FUN_38d03 | init_cutscene_playback_state |
| 0x38eb5 | FUN_38eb5 | init_cutscene_display_mode |
| 0x39aa4 | FUN_39aa4 | setup_cutscene_display_scaling |

### Data Labels Renamed
| Address | Old Name | New Name |
|---------|----------|----------|
| 0x4c344 | DAT_0004c344 | CUTSCENE_TRACK_TABLE |
| 0x4c348 | DAT_0004c348 | CUTSCENE_TRACK_TABLE_END |
| 0x4c34c | DAT_0004c34c | CUTSCENE_DISPLAY_WIDTH |
| 0x4c350 | DAT_0004c350 | CUTSCENE_DISPLAY_HEIGHT |
| 0x4c358 | DAT_0004c358 | CUTSCENE_SCALE_X |
| 0x4c35c | DAT_0004c35c | CUTSCENE_SCALE_Y |

### Comments Added
- 8 decompiler/disassembly comments at key decision points in renamed functions
