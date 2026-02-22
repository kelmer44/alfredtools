# Room Entry Dispatch Tables Documentation

## Overview

When the player enters a room, the game engine calls several dispatch tables to execute room-specific initialization logic. This document covers all four room-related dispatch tables, their entries, and what each handler does.

All tables use the same 6-byte entry format: `[uint16 room_id][uint32 func_ptr]`, terminated by `0xFFFF`.

Function pointers stored in the table need `+0x10000` to get the runtime/Ghidra address.

---

## Table 1: Room Init Dispatch Table

| Property | Value |
|----------|-------|
| Ghidra Address | `0x484E4` |
| File Offset | `0x4B6E4` |
| Label | `ROOM_INIT_DISPATCH_TABLE` |
| # Entries | 35 |
| Called from | `load_room_and_init_alfred()` at `0x152F5` |
| When | On room load, when `room_load_mode != 2` (normal entry and mode 1, but not mode 2 = reload) |

This table is scanned linearly. On match, the handler is called once and the scan stops (`break`).

### Entry Summary

| # | Room | Handler | Description |
|---|------|---------|-------------|
| 0 | 0 | `0x2561F` | **Shared with room 4.** If room==4 and `FLAG_ELECTROCUTACION` set: hide sprites #7 and #9 (z=100→hidden). If `FLAG_PUESTA_SALSA_PICANTE` set and `FLAG_JEFE_ENCARCELADO` not set: play **boss arrested cutscene** (extra screen #3, fade to black, load room graphics for room 12, display two speech bubbles, set `FLAG_JEFE_ENCARCELADO=1`). If `FLAG_CHEAT_CODE_ENABLED` set: display cheat code input. |
| 1 | 3 | `0x25889` | If `[0x9840]==1`: call function at `0x1C716` (unknown, possibly shop init). If `[0x9824]==1`: hide sprite #12 (z=100→hidden). |
| 2 | 4 | `0x2561F` | Same handler as room 0 (see above). |
| 3 | 7 | `0x2587A` | Calls `init_or_stop_sound()` — plays CD audio track (room 7 = Egypt). |
| 4 | 9 | `0x258BD` | Clears `[0x95BF]` (door state = closed). Calls shared handler (rooms 17/13/19/49/50: NPC sprite blit). Sets `room_data[0x1C1]=0` (resets door open state). |
| 5 | 12 | `0x25C49` | Clears `[0x95C0]` (kitchen door state = closed). Sets `room_data[0x1CF]=0`. |
| 6 | 13 | `0x25C68` | Clears `[0x95C1]` (kitchen inner door = closed). Sets `room_data[0x1C1]=0`. If `[0x9DA3]==1`: modifies sprite #3's position (x=0x78, y=0xFC), walkbox start=(0x18), and facing direction=2 — **sets up NPC position based on game progress**. |
| 7 | 28 | `0x258E1` | If `FLAG_CROCODILLO_ENCENDIDO`: loads alternate palette from ALFRED.5 at offset `0x1610CE` (768 bytes), applying red-tinted crocodile lighter palette. |
| 8 | 36 | `0x2592B` | Sets sprite #3 frame to 1 (z=1). If `[0x1176A]!=0`: clears it and sets `[0x95CE]=1` — **triggers cutscene flag for room 36 revisit**. |
| 9 | 30 | `0x25959` | If item 99 (wig) is in inventory and `[0x95E3]==0`: shows sprite #3 (z=100→visible), sets `[0x95E3]=1` and `goodbye_disabled=1` — **Roba Pelo Princesa encounter (princess hair thief confrontation)**. |
| 10 | 48 | `0x25994` | Sets `goodbye_disabled=1`. Checks `[0x11778]` (timer/counter) against 282: if >282 and `[0x95D6]==0`, or <282 and `[0x95D6]==0`, sets `[0x95D7]=1` — **pyramid construction progress check**. |
| 11-14 | 51-54 | `0x259E9` | **Shared handler for all flight rooms.** Sets flight animation flags: `[0x95DE]=1`, `[0x95D9]=0x40`, clears `[0x95E0]`, `[0x95DA]`, `[0x95DD]`. Looks up NPC sprite index from table at `[room_id + 0xB7E9]` and enables it (frame=1). Calls shared handler for rooms 17/49/50. |
| 15 | 5 | `0x25A3D` | Sets 5 conversation root flags to 1: `[0x98D3]`, `[0x98DA]`, `[0x98E1]`, `[0x98E8]` (4 conversation roots), plus `[0x95EA]=1`. **Enables all conversations for room 5 (seller's shop).** |
| 16 | 19 | `0x25A68` | Sets sprite #4's animation frame byte to 9 (`room_data[0xC4]=9`). |
| 17 | 9 | `0x25A7F` | **Second entry for room 9** (scanned after entry 4). Sets sprite #5 hidden (`room_data[0xD1]=0xFF`). Note: this entry is never reached because entry 4 also matches room 9 and the scan breaks. **This appears to be dead code or a bug in the original table.** |
| 18 | 24 | `0x25A96` | Sets sprite #3's animation state to 1 (`room_data[0x96]=1`). |
| 19 | 38 | `0x25AAD` | Plays fight/special animation: `play_fight_animation(0x182A56, 0x4366, 0x8B, 0xC6, 0x71, 0x67, 0xC, 2, 1, 1, 0)` then jumps to `0x1C251` with params (0x74539, 0xF1B) — **arrival animation from desert (climbing down/jumping)**. |
| 20 | 41 | `0x25AF0` | Sets sprite #3's walking frame to 3 (`room_data[0x98]=3`). **Initializes slaves animation state in pyramid room.** |
| 21 | 32 | `0x25B07` | If `alfred_y_prev < 200`: plays fight/special animation at (0x1ADFD2, 0x1418, 0x134, 0x38, 0x21, 0x48, 0xB, 2, 1, 1, 0) — **arrival animation from room 31** (exiting corridors). Then jumps to `0x23307` with (room=31, 3, 0). |
| 22 | 27 | `0x25B5B` | If `alfred_x_prev < 320`: plays fight/special animation at (0x1B02D4, 0x46FA0, 0xC, 0x109, 0x9E, 0x73, 0x10, 2, 0, 1, 0) — **arrival animation from room 33** (descending/sliding). |
| 23-24 | 39, 40 | `0x25BA5` | Sets `goodbye_disabled=1`. **Pharaoh's guard/throne room — no voluntary exit.** |
| 25 | 26 | `0x25BB7` | If `[0xFC0D]==1`: sets `goodbye_disabled=1`. **Prison room, guard encounter — disables goodbye when jailed.** |
| 26 | 2 | `0x25C22` | **Shared with room 37.** Clears `[0x961D]=0` (room-load temp flag). |
| 27-29, 31-32 | 17, 13, 19, 49, 50 | `0x25BEC` | **Shared NPC sprite blit handler.** Sets `[0x961D]=1`. Reads NPC overlay data from `[0x13002]` (transparency) and `[0x13254]` (data pointer), blits 256×256 NPC overlay with 32-byte header, 2 layers — **sets up walking character sprites (e.g., passing pedestrians)**. |
| 30 | 37 | `0x25C22` | Same handler as room 2 (clears `[0x961D]=0`). |
| 33-34 | 22, 34 | `0x25C35` | Sets `room_data[0x21]=0xFF` — **hides the character overlay (disables Alfred rendering) for cutscene rooms.** |

---

## Table 2: Per-Frame Update Table

| Property | Value |
|----------|-------|
| Ghidra Address | `0x485BC` |
| File Offset | `0x4B7BC` |
| Label | `ROOM_PER_FRAME_UPDATE_TABLE` |
| # Entries | 18 |
| Called from | `main_game_loop()` |
| When | Every frame while in matched room |

### Entry Summary

| # | Room | Handler | Description |
|---|------|---------|-------------|
| 0 | 26 | `0x1087C` | **Prison guard patrol timer.** Increments counter `[0x95FA]`; at 100: if `[0x95FB]==0`, shows guard sprite (z=5), sets `[0x95FB]=1`. Also checks guard X position (sprite offset +0x112): if >40 and <60000, resets counter and repositions guard to (-40, 43). If `[0x95C9]` set (guard bribed) and `[0x95CA]==0`: plays dialogue sequence, sets flag. |
| 1 | 30 | `0x1094B` | If item 99 (wig) in inventory and `[0x95E4]==0`: sets `[0x95E4]=1`, plays dialogue `[0xBB00]`, triggers sound effect type 2 — **one-time wig pickup dialogue**. |
| 2 | 36 | `0x1098F` | **Pyramid construction cutscene.** Complex multi-phase handler: if `[0x95CE]` and not `[0x95CC]`: init phase. Then enters main animation loop: plays ambient sound, waits for sprite frame #5, copies & modifies background tiles, renders stickers, moves sprite through waypoints (x≥0x153, y≥0xCE, x≤0x133, etc.), adds conversation state, marks `[0x95CD]=1`. |
| 3 | 48 | `0x10D4C` | **Swimming pool / guard room per-frame logic.** |
| 4 | 19 | `0x115EF` | **Travel agency per-frame update.** |
| 5 | 24 | `0x25CD7` | **Room 24 sprite animation update.** |
| 6-9 | 51-54 | `0x113DC` | **Shared flight animation per-frame handler.** Updates airplane animation across map screens. |
| 10-16 | 1,2,3,8,17,14,12 | `0x118AD` | **Shared idle animation handler** for most outdoor/indoor rooms — handles passing pedestrians, ambient movement, periodic sprite updates. |
| 17 | 15 | `0x11DE5` | **Room 15 (seller's shop) per-frame handler.** |

---

## Table 3: Render Scene Dispatch Table

| Property | Value |
|----------|-------|
| Ghidra Address | `0x48630` |
| File Offset | `0x4B830` |
| Label | `ROOM_RENDER_SCENE_TABLE` |
| # Entries | 7 |
| Called from | `render_scene()` |
| When | Every frame during scene rendering |

### Entry Summary

| # | Room | Handler | Description |
|---|------|---------|-------------|
| 0 | 21 | `0x107C2` | Background character walking animation (passing by). |
| 1 | 9 | `0x1167A` | Library interior — character passing by window. |
| 2 | 29 | `0x11919` | Desert corridor — NPC passing. |
| 3 | 46 | `0x11A29` | Corridor room — NPC passing. |
| 4 | 47 | `0x11B41` | Corridor room — NPC passing. |
| 5 | 50 | `0x11C4E` | Corridor room — NPC passing. |
| 6 | 31 | `0x11D66` | Corridor room — NPC passing. |

---

## Table 4: Palette Cycling Config Table

| Property | Value |
|----------|-------|
| Ghidra Address | `0x486A4` |
| File Offset | `0x4B8A4` |
| Label | `PALETTE_CYCLING_CONFIG_TABLE` |
| # Entries | 13 |
| Called from | `load_room_and_init_alfred()` |
| When | After room graphics loaded; sets `palette_cycling_enabled=1` and stores config pointer |

Unlike the other tables, the function pointer here points to a **palette cycling configuration data block**, not executable code. The config specifies which palette indices to cycle and the cycling parameters.

### Entry Summary

| # | Room | Config Ptr | Description |
|---|------|-----------|-------------|
| 0 | 2 | `0x18660` | McDowell's restaurant — neon signs |
| 1 | 9 | `0x18674` | Library interior — lamp flicker |
| 2 | 17 | `0x1866C` | Boss office — monitor glow |
| 3 | 18 | `0x18670` | Unknown room — ambient lighting |
| 4 | 19 | `0x18678` | Travel agency — sign animation |
| 5 | 21 | `0x18684` | Street scene — traffic lights |
| 6 | 39 | `0x18688` | Guard's room — torchlight |
| 7 | 0 | `0x1868C` | Alfred's bedroom — clock/lamp |
| 8 | 25 | `0x18690` | Desert marketplace — heat shimmer |
| 9 | 38 | `0x18694` | Cave/tunnel — light effects |
| 10 | 32 | `0x18698` | Pyramid entrance — torchlight |
| 11 | 33 | `0x1869C` | Pyramid interior — torchlight |
| 12 | 46 | `0x186A0` | Corridor — torch/ambient |

---

## Detailed Handler: Item 91/92 + Hotspot 601 in Room 41

### Context

- **Room 41**: Pyramid construction site (exterior)
- **Hotspot 601**: The slave workers building the pyramid
- **Item 91**: "Una piedra egipcia" (an Egyptian stone)
- **Item 92**: "Un poco de barro" (a bit of mud/clay)
- **Handler**: `0x239DD` (via `ITEM_COMBINATION_TABLE` entries [30] and [31])
- **Flag**: `FLAG_DA_PIEDRA` (flag #31, address `0x495D2`) — stone delivery counter (0→3)

### Execution Flow (from binary at `0x239DD`)

Both items trigger the **exact same handler**. Here is the complete sequence:

#### Phase 1: Remove Items and Save Background

```
1. find_item_in_room_table(0x5B)  → check if item 91 exists
2. If found: remove_inventory_item(0x5B)  → remove item 91
3. find_item_in_room_table(0x5C)  → check if item 92 exists
4. If found: remove_inventory_item(0x5C)  → remove item 92
5. allocate_memory(0x158F8)  → buffer1 for background backup (88312 bytes)
6. allocate_memory(0xC180)  → buffer2 for background backup (49536 bytes)
7. file_seek(ALFRED.5, 0x167B54)  → seek to shadow/overlay data
8. file_read(buffer_temp, 0x9728)  → read 38,696 bytes from ALFRED.5
9. decompress_rle_block(buffer_temp, buffer1)  → decompress into buffer1
10. file_seek(ALFRED.5, 0x17127C)
11. file_read(buffer_temp, 0x3824)  → read 14,372 bytes
12. decompress_rle_block(buffer_temp, buffer2)  → decompress into buffer2
```

#### Phase 2: Stone Delivery Animation

```
13. Set sprite #3 parameters:
    - room_data[0x93] = 0x70  (frame offset)
    - room_data[0x98] = 1     (animation sequence = "take stone")
    - room_data[0x94] = 0x43D0 (animation data pointer, 16-bit)
    - room_data[0xA4] = 0     (animation counter reset)

14. play_fight_animation(0x186DBC, 0x24420, 0, 0x12A, 0xD0, 0x66, 7, 2, 0, 0, 0)
    → Plays "slaves receive stone" animation
    → Source data at ALFRED.7 offset 0x186DBC, size 0x24420 (148,512 bytes)
    → Displayed at screen position (208, 102), 7 frames
```

#### Phase 3: Drinking Animation

```
15. Set sprite #3 parameters:
    - room_data[0x94] = 0x6BC6 (new animation pointer)
    - room_data[0x98] = 3      (animation = "drinking")
    - room_data[0x93] = 0xB2   (new frame offset)
    - room_data[0xA4] = 0      (reset counter)

16. play_ambient_sound([0x13204], 3)  → start drinking sound effect
17. play_or_check_sound([0x13204], 3) → wait for sound to reach state 3

18. Animation rendering loop:
    while (sound not finished):
        process_game_state()
        setup_alfred_frame_from_state()
        render_scene(0)
    → Renders scene while sound plays
```

#### Phase 4: Dialogue

```
19. play_ambient_sound([0x13238], -1)  → play "celebration" ambient
20. display_text_with_character_animation([0xBB10], 0)
    → NPC says dialogue (likely "¡Hay que celebrarlo!" / "Let's celebrate!")
```

#### Phase 5: Walking Animation with Celebration

```
21. Save sprite #3's current animation data pointer (ebx = room_data[0x5E])
22. Set sprite #3:
    - room_data[0x6C] = 7      (animation type = walking)
    - room_data[0x5E] = buffer1 (use backup frames)
    - room_data[0x78] = 0      (frame counter reset)
    - room_data[0x62] -= 5     (adjust X position left by 5)
    - room_data[0x64] -= 1     (adjust Y position up by 1)
    - room_data[0x66] = 0x98   (width = 152)
    - room_data[0x67] = 0x53   (height = 83)
    - room_data[0x68] = 0x3148 (animation data size = 12616)

23. play_ambient_sound([0x13238], -1)  → sound effect continues
24. Wait loop: render until sprite #3 frame counter reaches 6
    → NPC walks carrying stone to pyramid position
```

#### Phase 6: Return Walk and Counter Update

```
25. Restore sprite #3:
    - room_data[0x6C] = 4      (animation type = different walk)
    - room_data[0x5E] = saved pointer (restore original anim data)
    - room_data[0x78] = 0      (reset frame)
    - room_data[0x62] += 5     (X back right by 5)
    - room_data[0x64] += 1     (Y back down by 1)
    - room_data[0x66] = 0x90   (width = 144)
    - room_data[0x67] = 0x51   (height = 81)
    - room_data[0x68] = 0x2D90 (anim data size = 11664)

26. Increment FLAG_DA_PIEDRA counter:
    if counter < 3: counter++
    Store to [0x95D2]
```

#### Phase 7: Conditional — Second Delivery (counter == 2)

```
27. If FLAG_DA_PIEDRA == 2:
    update_conversation_state(room=0x29, root=2, edx=0)
    → Sets conversation root 2 for room 41
    → Slaves start singing: "¡Deesde Santuurce a Bilbaooo...!"
```

#### Phase 8: Conditional — Third Delivery (counter == 3)

This is the **pyramid completion** sequence:

```
28. Set sprite #3:
    - room_data[0x6C] = 3      (construction animation)
    - room_data[0x5E] = buffer2 (construction frame data)
    - room_data[0x78] = 0
    - room_data[0x62] -= 0x1C  (X -= 28)
    - room_data[0x64] -= 6     (Y -= 6)
    - room_data[0x66] = 0xAC   (width = 172)
    - room_data[0x67] = 0x60   (height = 96)
    - room_data[0x68] = 0x4080 (anim data size = 16512)

29. Wait loop: render until sprite #3 frame counter reaches 2
    → Construction animation plays

30. Hide sprite #3: room_data[0x79] = 0xFF

31. Write to ALFRED.1 (persistent save):
    write_data_to_alfred1(room_41, offset=0x79, size=1, value=0xFF)
    → Permanently hides slave sprite

32. Set [0xACEC] = 1

33. load_and_render_sticker_from_alfred6(0x696AD, 0x2C1C)
    → Renders sticker #116: completed pyramid overlay
    → ALFRED.6 offset = 0x696AD, size = 0x2C1C (11,292 bytes)

34. Set walkbox count: room_data[0x213] = 5
    → Changes from 3 walkboxes to 5 walkboxes (new pyramid layout)

35. Write to ALFRED.1 (persistent save):
    write_data_to_alfred1(room_41, offset=0x213, size=1, value=5)
    → Permanently updates walkbox count
```

#### Phase 9: Cleanup

```
36. free_memory(buffer1)
37. free_memory(buffer2)  → via jmp to 0x143B9 which calls free + stack cleanup
```

### Summary Table

| Delivery # | FLAG_DA_PIEDRA | What Happens |
|------------|---------------|--------------|
| 1st | 0 → 1 | Slaves take stone, drink, celebrate. Animation plays. |
| 2nd | 1 → 2 | Same as above + slaves start singing (conversation root 2 enabled). |
| 3rd | 2 → 3 | Same drinking + **pyramid construction animation**. Sprite hidden permanently. Sticker #116 (completed pyramid) rendered. Walkbox count increased 3→5. ALFRED.1 updated on disk (persistent). `FLAG_PIEDRAS_COGIDAS` is NOT set here — it's likely set elsewhere (conversation resolution or a separate check). |

### Key Addresses

| Address | Description |
|---------|-------------|
| `0x495D2` | `FLAG_DA_PIEDRA` — stone delivery counter (0-3) |
| `0x186DBC` | ALFRED.7 offset: slave "receive stone" animation (148,512 bytes) |
| `0x167B54` | ALFRED.5 offset: carry-stone walk frames (38,696 bytes compressed) |
| `0x17127C` | ALFRED.5 offset: construction animation frames (14,372 bytes compressed) |
| `0x696AD` | ALFRED.6 offset: sticker #116 — completed pyramid (11,292 bytes) |
| `0xBB10` | Dialogue text pointer: celebration line |
| `0x13204` | Sound effect pointer (drinking sound) |
| `0x13238` | Sound effect pointer (celebration ambient) |
| Room 41, offset `0x79` | Sprite #3 z-order (0xFF = hidden) |
| Room 41, offset `0x213` | Walkbox count (3→5 after completion) |

---

## Cross-Reference: ScummVM Implementation Status

The ScummVM `doExtraActions()` function in `pelrock.cpp` implements a subset of the room init dispatch table. Currently implemented:

| Room | ScummVM Status | Notes |
|------|---------------|-------|
| 4 | ✅ Implemented | Boss arrested cutscene |
| 15 | ✅ Implemented | First time entering shop |
| 38 | ✅ Implemented | Arrival from desert animation |
| 32 | ✅ Implemented | Arrival from room 31 |
| 27 | ✅ Implemented | Arrival from room 33 |
| 28 | ✅ Implemented | Alternate palette for crocodile lighter |
| 26 | ✅ Implemented | Prison guard encounter |
| 30 | ✅ Implemented | Princess hair thief confrontation |
| 39, 40 | ✅ Implemented | Goodbye disabled |
| 48 | ✅ Implemented | Goodbye disabled |
| 0 | ❌ Missing | Boss cutscene (shared handler with 4) |
| 3 | ❌ Missing | Shop conversation init |
| 7 | ❌ Missing | CD audio for Egypt |
| 9 | ❌ Missing | Door state reset + NPC overlay |
| 12 | ❌ Missing | Kitchen door state reset |
| 13 | ❌ Missing | Kitchen door reset + NPC position adjust |
| 36 | ❌ Missing | Sprite frame init + cutscene flag |
| 51-54 | ❌ Missing | Flight animation init |
| 5 | ❌ Missing | Enable seller conversations |
| 19 | ❌ Missing | Sprite frame init |
| 24 | ❌ Missing | Sprite animation state |
| 41 | ❌ Missing | Slave animation state init |
| 17, 49, 50 | ❌ Missing | NPC sprite overlay blit |
| 2, 37 | ❌ Missing | Clear room-load temp flag |
| 22, 34 | ❌ Missing | Disable Alfred overlay for cutscene |
| `giveStoneToSlaves` | ⚠️ Partial | Counter logic present but conditional branches (counter==2, counter==3) are commented out/incomplete |

---

## Raw Table Data

### Room Init Dispatch Table (0x484E4)

```
Entry  Room   Handler
[00]   0      0x2561F  (shared: 0, 4)
[01]   3      0x25889
[02]   4      0x2561F  (shared: 0, 4)
[03]   7      0x2587A
[04]   9      0x258BD
[05]   12     0x25C49
[06]   13     0x25C68
[07]   28     0x258E1
[08]   36     0x2592B
[09]   30     0x25959
[10]   48     0x25994
[11]   51     0x259E9  (shared: 51-54)
[12]   52     0x259E9
[13]   53     0x259E9
[14]   54     0x259E9
[15]   5      0x25A3D
[16]   19     0x25A68
[17]   9      0x25A7F  (DEAD: never reached, room 9 matched by entry [04])
[18]   24     0x25A96
[19]   38     0x25AAD
[20]   41     0x25AF0
[21]   32     0x25B07
[22]   27     0x25B5B
[23]   39     0x25BA5  (shared: 39, 40)
[24]   40     0x25BA5
[25]   26     0x25BB7
[26]   2      0x25C22  (shared: 2, 37)
[27]   17     0x25BEC  (shared: 17, 13, 19, 49, 50)
[28]   13     0x25BEC
[29]   19     0x25BEC
[30]   37     0x25C22
[31]   49     0x25BEC
[32]   50     0x25BEC
[33]   22     0x25C35  (shared: 22, 34)
[34]   34     0x25C35
```

### Per-Frame Update Table (0x485BC)

```
Entry  Room   Handler
[00]   26     0x1087C
[01]   30     0x1094B
[02]   36     0x1098F
[03]   48     0x10D4C
[04]   19     0x115EF
[05]   24     0x25CD7
[06]   51     0x113DC  (shared: 51-54)
[07]   52     0x113DC
[08]   53     0x113DC
[09]   54     0x113DC
[10]   1      0x118AD  (shared: 1,2,3,8,17,14,12)
[11]   2      0x118AD
[12]   3      0x118AD
[13]   8      0x118AD
[14]   17     0x118AD
[15]   14     0x118AD
[16]   12     0x118AD
[17]   15     0x11DE5
```

### Render Scene Dispatch Table (0x48630)

```
Entry  Room   Handler
[00]   21     0x107C2
[01]   9      0x1167A
[02]   29     0x11919
[03]   46     0x11A29
[04]   47     0x11B41
[05]   50     0x11C4E
[06]   31     0x11D66
```

### Palette Cycling Config Table (0x486A4)

```
Entry  Room   Config Ptr
[00]   2      0x18660
[01]   9      0x18674
[02]   17     0x1866C
[03]   18     0x18670
[04]   19     0x18678
[05]   21     0x18684
[06]   39     0x18688
[07]   0      0x1868C
[08]   25     0x18690
[09]   38     0x18694
[10]   32     0x18698
[11]   33     0x1869C
[12]   46     0x186A0
```
