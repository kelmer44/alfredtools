# F8 Action Handler Batch 7 (Final) - Decompilation Results

## Function Names (resolved via Ghidra + Capstone disassembly)

| Address | Name | Purpose |
|---------|------|---------|
| 0x2A218 | `get_current_room_number` | Returns current room number (saves context) |
| 0x2A258 | `wait_or_process_input` | Yield / process events |
| 0x1B666 | `update_conversation_state` | Write branch to conv state table (EAX=room, EDX=npc, EBX=branch) |
| 0x29037 | `init_or_stop_sound` | Start/stop sound (EBX=0 stops) |
| 0x2B12F | `random_number_generator` | Returns random value in EAX |
| 0x15DD4 | `copy_background_to_front_buffer` | Copy background layer to front buffer |
| 0x1625D | `present_frame_to_screen` | Push framebuffer to display |
| 0x1B1A2 | `display_npc_dialog_animation` | Display NPC talking animation with dialog (EAX=npc_idx, EDX=text_ptr) |
| 0x24157 | `process_inventory_action` | Give player an inventory item (EAX=item ID) |
| 0x1B723 | `setup_npc_conversation_text` | Setup NPC text pointer (EAX=room_idx, EDX=npc, ECX=flag, EBX=table_idx) |
| 0x25487 | `display_text_with_voice` | Display text with optional voice playback (EAX=text_ptr) |
| 0x27CE1 | `play_ambient_sound` | Play ambient/looping sound |
| 0x2A60D | `play_sound` | Play a sound effect |
| 0x19F2A | `render_menu_screen` | Render menu/overlay screen |
| 0x1B4A3 | `load_room_graphics_and_palette_dynamic` | Load room gfx + palette |
| 0x19DC8 | `draw_cursor_to_screen` | Draw mouse cursor |
| 0x15E4C | `render_scene` | Full scene render |
| 0x244E8 | `set_vga_palette` | Set VGA palette colors |
| 0x147C9 | `setup_alfred_frame_from_state` | Setup Alfred's sprite frame from animation state |
| 0x2A66B | `memcpy_wrapper` | Memory copy (EAX=dst, EDX=src, EBX=size) |
| 0x152F5 | `load_room_and_init_alfred` | Load room and initialize Alfred position |
| 0x26420 | `play_fight_animation` | Play fight/action animation sequence |
| 0x2A8A0 | `memset_or_init_buffer` | Initialize/clear a memory buffer (EAX=ptr, EBX=size, EDX=fill) |
| 0x18DCE | `check_sprite_hover_and_trigger_conversation` | Check sprite hover → trigger conversation |
| 0x1BA45 | `load_sticker_from_alfred6` | Load sticker/overlay from ALFRED.6 file |
| 0x29C34 | `draw_line` | Draw a line between two points on screen |
| 0x267DD | `load_sound_file` | Load a sound file into a sound slot |
| 0x28403 | `play_or_check_sound` | Play or check sound status |
| 0x27C2C | `sound_cleanup` | Clean up sound resources |

## Shared Code Blocks

### Shared conv tail at 0x222E3
```asm
222E3: call     update_conversation_state  ; EAX=room, EDX=npc, EBX=branch
222E8: pop      edx
222E9: pop      ebx
222EA: ret
```
Used by: actions 366, 369, 372, 373, 374, 377, 378, 383

### Shared conv tail at 0x20446
```asm
20446: call     update_conversation_state  ; EAX=room, EDX=npc, EBX=branch
2044B: pop      edx
2044C: pop      ecx
2044D: pop      ebx
2044E: ret
```
Used by: action 376 (pops 3 regs instead of 2)

### Shared conv tail at 0x21875 (room 0x1B = 27)
```asm
21875: mov      eax, 0x1B         ; room = 27
2187A: call     update_conversation_state
2187F: pop      edx
21880: pop      ebx
21881: ret
```
Used by: action 371

### Shared NPC text setup at 0x221E9 (room 25, NPC 0)
```asm
221E9: mov      ecx, 1            ; flag = 1
221EE: mov      ebx, 0x19         ; table_idx = 25
221F3: xor      edx, edx          ; npc = 0
221F5: mov      eax, ebx          ; room = 25
221F7: call     setup_npc_conversation_text
221FC: pop      edx
221FD: pop      ecx
221FE: pop      ebx
221FF: ret
```
Used by: actions 360, 361, 364

### Shared block at 0x221E3 (sets [0x95F2] then falls through to 0x221E9)
```asm
221E3: mov      byte ptr [0x95F2], ah   ; ah from caller
221E9: (falls into shared NPC text setup)
```
Used by: action 360

### Shared conv+sprite block at 0x219B9 (room 25 / NPC 0)
```asm
219B9: xor      edx, edx          ; npc = 0
219BB: mov      eax, 0x19         ; room = 25
219C0: call     update_conversation_state
219C5: xor      edx, edx          ; npc = 0 (sprite index 2)
219C7: mov      eax, 2
219CC: call     check_sprite_hover_and_trigger_conversation
219D1: pop      edx
219D2: pop      ebx
219D3: ret
```
Used by: action 367

### Shared conv block at 0x219D9 (room 25, NPC 0, branch 1 + set flag)
```asm
219D9: call     get_current_room_number
219DE: push     ebx
219DF: push     edx
219E0: mov      ebx, 1            ; branch = 1
219E5: xor      edx, edx          ; npc = 0
219E7: mov      eax, 0x19         ; room = 25
219EC: call     update_conversation_state
219F1: mov      byte ptr [0x95D0], 1   ; set flag
219F8: pop      edx
219F9: pop      ebx
219FA: ret
```
Used by: action 365

### Shared ambient sound block at 0x21BF4
```asm
21BF4: xor      eax, eax
21BF6: mov      al, byte ptr [0x13002]   ; volume
21BFB: push     eax
21BFC: mov      edx, dword ptr [0x13234] ; sound data ptr
21C02: push     edx
21C03: push     0x20                     ; flags
21C05: push     0x100                    ; pan
21C0A: push     0x100                    ; rate
21C0F: push     -1                       ; loop forever
21C11: mov      ebx, dword ptr [0x13204] ; sound handle
21C17: push     ebx
21C18: call     play_ambient_sound
21C1D: pop      edx
21C1E: pop      ecx
21C1F: pop      ebx
21C20: ret
```
Used by: action 381

---

## Handler Analysis

---

### ACTION 0x0168 (360) @ Ghidra 0x2222D

**Disassembly:**
```asm
2222D: push     0x10
22232: call     get_current_room_number
22237: push     ebx
22238: push     ecx
22239: push     edx
2223A: xor      ah, ah             ; ah = 0
2223C: jmp      0x221E3
  ; --- jump target at 0x221E3 ---
221E3: mov      byte ptr [0x95F2], ah   ; [0x95F2] = 0
221E9: mov      ecx, 1
221EE: mov      ebx, 0x19
221F3: xor      edx, edx
221F5: mov      eax, ebx           ; room = 25
221F7: call     setup_npc_conversation_text
221FC: pop      edx
221FD: pop      ecx
221FE: pop      ebx
221FF: ret
```

**What it does:** Clears flag [0x95F2] to 0, then sets up NPC conversation text for room 25, NPC 0, with flag=1 and table_idx=25.

**State flags:** Writes `[0x95F2]` = 0

**Chains to:** None

**Conversation updates:** `setup_npc_conversation_text(room=25, npc=0, flag=1, table_idx=25)`

**Items:** None

---

### ACTION 0x0169 (361) @ Ghidra 0x2223E

**Disassembly:**
```asm
2223E: push     0x10
22243: call     get_current_room_number
22248: push     ebx
22249: push     ecx
2224A: push     edx
2224B: jmp      0x221E9            ; shared NPC text setup (room 25)
```

**What it does:** Sets up NPC conversation text for room 25, NPC 0, with flag=1 and table_idx=25. Same as action 360 but without clearing [0x95F2].

**State flags:** None

**Chains to:** None

**Conversation updates:** `setup_npc_conversation_text(room=25, npc=0, flag=1, table_idx=25)`

**Items:** None

---

### ACTION 0x016A (362) @ Ghidra 0x2224D

**Disassembly:**
```asm
2224D: push     0x10
22252: call     get_current_room_number
22257: push     ebx
22258: push     ecx
22259: push     edx
2225A: mov      byte ptr [0x95F3], 1   ; set flag
22261: jmp      0x221E9            ; shared NPC text setup (room 25)
```

**What it does:** Sets flag [0x95F3] to 1, then sets up NPC conversation text for room 25, NPC 0, with flag=1 and table_idx=25.

**State flags:** Writes `[0x95F3]` = 1

**Chains to:** None

**Conversation updates:** `setup_npc_conversation_text(room=25, npc=0, flag=1, table_idx=25)`

**Items:** None

---

### ACTION 0x016C (364) @ Ghidra 0x22263

**Disassembly:**
```asm
22263: push     0x10
22268: call     get_current_room_number
2226D: push     ebx
2226E: push     ecx
2226F: push     edx
22270: mov      ecx, 0x1B          ; flag = 27
22275: mov      ebx, 0x2B          ; table_idx = 43
2227A: xor      edx, edx           ; npc = 0
2227C: mov      eax, 0x19          ; room = 25
22281: jmp      0x221F7            ; → call setup_npc_conversation_text; pop; ret
```

**What it does:** Sets up NPC conversation text for room 25, NPC 0, with flag=27 and table_idx=43. This is a different conversation branch than actions 360-362.

**State flags:** None

**Chains to:** None

**Conversation updates:** `setup_npc_conversation_text(room=25, npc=0, flag=27, table_idx=43)`

**Items:** None

---

### ACTION 0x016D (365) @ Ghidra 0x22286

**Disassembly:**
```asm
22286: push     0xC
2228B: jmp      0x219D9
  ; --- jump target at 0x219D9 ---
219D9: call     get_current_room_number
219DE: push     ebx
219DF: push     edx
219E0: mov      ebx, 1             ; branch = 1
219E5: xor      edx, edx           ; npc = 0
219E7: mov      eax, 0x19          ; room = 25
219EC: call     update_conversation_state
219F1: mov      byte ptr [0x95D0], 1   ; set flag
219F8: pop      edx
219F9: pop      ebx
219FA: ret
```

**What it does:** Updates conversation state for room 25, NPC 0 to branch 1, and sets flag [0x95D0] to 1.

**State flags:** Writes `[0x95D0]` = 1

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x016E (366) @ Ghidra 0x22290

**Disassembly:**
```asm
22290: push     0xC
22295: call     get_current_room_number
2229A: push     ebx
2229B: push     edx
2229C: mov      ebx, 1             ; branch = 1
222A1: xor      edx, edx           ; npc = 0
222A3: mov      eax, 0x19          ; room = 25
222A8: jmp      0x222E3            ; → call update_conversation_state; pop; ret
```

**What it does:** Updates conversation state for room 25, NPC 0 to branch 1. Same effect as action 365 but without setting [0x95D0].

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x016F (367) @ Ghidra 0x222AA

**Disassembly:**
```asm
222AA: push     0xC
222AF: call     get_current_room_number
222B4: push     ebx
222B5: push     edx
222B6: mov      ebx, 0x1B          ; branch = 27
222BB: jmp      0x219B9
  ; --- jump target at 0x219B9 ---
219B9: xor      edx, edx           ; npc = 0
219BB: mov      eax, 0x19          ; room = 25
219C0: call     update_conversation_state
219C5: xor      edx, edx           ; sprite index arg = 0
219C7: mov      eax, 2             ; mode = 2
219CC: call     check_sprite_hover_and_trigger_conversation
219D1: pop      edx
219D2: pop      ebx
219D3: ret
```

**What it does:** Updates conversation state for room 25, NPC 0 to branch 27, then calls `check_sprite_hover_and_trigger_conversation` which rechecks the sprite region and may trigger a new conversation tree.

**State flags:** None

**Chains to:** `check_sprite_hover_and_trigger_conversation(mode=2, sprite_idx=0)`

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=27)`

**Items:** None

---

### ACTION 0x0170 (368) @ Ghidra 0x222C0

**Disassembly:**
```asm
222C0: push     4
222C5: call     get_current_room_number
222CA: ret
```

**What it does:** No-op handler. Just calls `get_current_room_number` and returns immediately. Likely a placeholder or disabled action.

**State flags:** None

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

### ACTION 0x0171 (369) @ Ghidra 0x222CB

**Disassembly:**
```asm
222CB: push     0xC
222D0: call     get_current_room_number
222D5: push     ebx
222D6: push     edx
222D7: mov      ebx, 1             ; branch = 1
222DC: xor      edx, edx           ; npc = 0
222DE: mov      eax, 0x1A          ; room = 26
222E3: call     update_conversation_state
222E8: pop      edx
222E9: pop      ebx
222EA: ret
```

**What it does:** Updates conversation state for room 26, NPC 0 to branch 1.

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=26, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x0172 (370) @ Ghidra 0x222EB

**Disassembly:**
```asm
222EB: push     4
222F0: call     get_current_room_number
222F5: mov      eax, 0x6F          ; item = 111
222FA: jmp      process_inventory_action
```

**What it does:** Gives the player inventory item 0x6F (111). The `process_inventory_action` function adds it to the inventory array at [0xFC94].

**State flags:** Writes to inventory array `[0xFC94 + ...]`

**Chains to:** `process_inventory_action(item=111)`

**Conversation updates:** None

**Items:** **Gives item 111 (0x6F)**

---

### ACTION 0x0173 (371) @ Ghidra 0x222FF

**Disassembly:**
```asm
222FF: push     0xC
22304: call     get_current_room_number
22309: push     ebx
2230A: push     edx
2230B: mov      eax, 0x6F          ; item = 111
22310: call     process_inventory_action   ; give item 111
22315: mov      eax, 0x6E          ; item = 110
2231A: call     process_inventory_action   ; give item 110
2231F: mov      ebx, 2             ; branch = 2
22324: xor      edx, edx           ; npc = 0
22326: jmp      0x21875
  ; --- jump target at 0x21875 ---
21875: mov      eax, 0x1B          ; room = 27
2187A: call     update_conversation_state
2187F: pop      edx
21880: pop      ebx
21881: ret
```

**What it does:** Gives the player two inventory items (111 and 110), then updates conversation state for room 27, NPC 0 to branch 2.

**State flags:** Writes to inventory array

**Chains to:** `process_inventory_action(111)`, `process_inventory_action(110)`

**Conversation updates:** `update_conversation_state(room=27, npc=0, branch=2)`

**Items:** **Gives item 111 (0x6F) and item 110 (0x6E)**

---

### ACTION 0x0174 (372) @ Ghidra 0x2232B

**Disassembly:**
```asm
2232B: push     0xC
22330: call     get_current_room_number
22335: push     ebx
22336: push     edx
22337: mov      ebx, 2             ; branch = 2
2233C: xor      edx, edx           ; npc = 0
2233E: mov      eax, 0x22          ; room = 34
22343: jmp      0x222E3            ; → call update_conversation_state; pop; ret
```

**What it does:** Updates conversation state for room 34, NPC 0 to branch 2.

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=34, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x0175 (373) @ Ghidra 0x22345

**Disassembly:**
```asm
22345: push     0xC
2234A: call     get_current_room_number
2234F: push     ebx
22350: push     edx
22351: mov      ebx, 3             ; branch = 3
22356: jmp      0x2233C
  ; --- at 0x2233C ---
2233C: xor      edx, edx           ; npc = 0
2233E: mov      eax, 0x22          ; room = 34
22343: jmp      0x222E3            ; → call update_conversation_state; pop; ret
```

**What it does:** Updates conversation state for room 34, NPC 0 to branch 3.

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=34, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x0176 (374) @ Ghidra 0x22358

**Disassembly:**
```asm
22358: push     0xC
2235D: call     get_current_room_number
22362: push     ebx
22363: push     edx
22364: mov      ebx, 1             ; branch = 1
22369: jmp      0x2233C
  ; --- at 0x2233C ---
2233C: xor      edx, edx           ; npc = 0
2233E: mov      eax, 0x22          ; room = 34
22343: jmp      0x222E3            ; → call update_conversation_state; pop; ret
```

**What it does:** Updates conversation state for room 34, NPC 0 to branch 1.

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=34, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x0177 (375) @ Ghidra 0x2236B

**Disassembly (complex — multi-phase cutscene):**
```asm
; === Entry ===
2236B: push     0x38
22370: call     get_current_room_number
22375: push     ebx / ecx / edx / esi
22379: sub      esp, 8
2237C: mov      esi, [0xFA60]       ; save front buffer ptr
22382: xor      ah, ah
22384: mov      [esp+4], ah         ; loop counter = 0
22388: jmp      0x22440             ; → main loop

; === Inner sticker draw loop at 0x2238D ===
; For each sticker index 0..18:
2238D: push     0x12CFC             ; table base
22392: mov      al, [esp+8]         ; sticker_phase
22398: mov      dx, [eax*4 + 0xB842]  ; Y coord from table
223A2: push     edx
223A3: mov      cx, [eax*4 + 0xB840]  ; X offset from table
223AD: add      ecx, ebx
223AF: mov      bx, [eax*4 + 0xB82E]  ; endpoint X from table
223B9: mov      dx, [eax*4 + 0xB82C]  ; endpoint Y from table
223C3: mov      eax, [0xFADC]       ; back buffer
223C8: call     draw_line            ; draw line on back buffer
223CD: inc      [esp]               ; next sticker index
223D0: cmp      [esp], 0x13         ; loop 19 times
223D8: jl       0x2238D

; === After inner loop: render frame ===
223DA: call     setup_alfred_frame_from_state
223DF: call     render_scene(0)
223E6: memcpy(front_buffer ← [0xFADC], 0x3E800)  ; restore buffer from saved
223F7: xor      bl, bl
223F9: mov      bh, [esp+4]         ; outer counter

; === Sticker overlay loop at 0x223FF ===
; For each sticker 0..outer_counter:
223FF: mov      al, bl
22403: mov      cl, [eax + 0xB810]  ; sticker lookup table
2240B: compute file offset from table at 0xB2F1..0xB2F5
22421: call     load_sticker_from_alfred6   ; load & render sticker
22426: inc      bl
22428: cmp      bl, bh
2242A: jbe      0x223FF

; === Setup next outer iteration ===
2242C: call     setup_alfred_frame_from_state
22431: call     render_scene(0)
22438: inc      outer_counter ([esp+4])
2243C: mov      [esp+4], cl

; === Outer loop body at 0x22440 ===
22440: cmp      [esp+4], 5          ; 5 phases
22449: jge      0x224E2             ; done → exit sequence

; memcpy(back_buffer, front_buffer, 0x3E800) — save current scene
2245F: call     memcpy_wrapper

; Set sprite [ecx+3]*0x2C anim byte to 0xC8 (trigger animation)
2246F: mov      byte ptr [edx + eax + 0x21], 0xC8

; === Animation wait loop ===
22474: push     0x167               ; chain to action 359 (wait_or_process_input)
22479: call     wait_or_process_input
22481: call     setup_alfred_frame_from_state
22488: call     render_scene(0)
; Check if sprite animation finished ([sprite+0x21] == 0xFF)
224A8: cmp      eax, 0xFF
224AD: jne      0x22474             ; loop until done

; Play ambient sound after each phase
224B6..224D3: push sound params, call play_ambient_sound

; Clear inner sticker counter, loop back
224D8: mov      [esp], 0
224DD: jmp      0x223D0             ; → inner sticker loop check

; === Exit sequence at 0x224E2 (after 5 phases) ===
224E2: mov      edx, 0x2E5
224E7: mov      eax, 0x693C8
224EC: call     0x1BA45             ; load_sticker_from_alfred6 (final overlay)
224F1: mov      eax, [0xBBD4]
224F6: call     display_text_with_voice    ; display finale text
; Setup warp to room 48:
22506: call     0x2662D             ; render_scene_transition(eax=1,edx=1,ebx=0,ecx=0)
2250B: mov      byte ptr [0x9612], 1        ; set game progress flag
22512: mov      word ptr [0xFB96], 0x8A     ; Alfred X = 138
2251B: mov      word ptr [0xFB98], 0xFF     ; Alfred Y = 255
22524: mov      byte ptr [0xFB9A], 2        ; Alfred facing direction = 2
2252B: xor      edx, edx
2252D: mov      eax, 0x30           ; room = 48
22532: call     load_room_and_init_alfred
22537: add      esp, 8
2253A: pop      esi / edx / ecx / ebx
2253E: ret
```

**What it does:** Complex multi-phase cutscene animation. Loops 5 phases where each phase: (1) copies the scene buffer, (2) triggers a sprite animation and waits for it to complete, (3) draws lines on screen using coordinate tables, (4) overlays stickers loaded from ALFRED.6. After all 5 phases, loads a final sticker overlay, displays text with voice, sets game progress flag [0x9612]=1, then warps Alfred to room 48 at position (138, 255) facing direction 2.

**State flags:**
- Reads: `[0xFA60]` (front buffer), `[0xFADC]` (back buffer), `[0xFAC8]` (sprite data), `[0xBBD4]` (text ptr), `[0x13002]` (volume), `[0x13204]` (sound handle), `[0x13240]` (sound data)
- Writes: `[0x9612]` = 1 (game progress flag), `[0xFB96]` = 0x8A, `[0xFB98]` = 0xFF, `[0xFB9A]` = 2

**Chains to:** `wait_or_process_input(action=0x167/359)`, `load_room_and_init_alfred(room=48)`, `render_scene_transition`

**Conversation updates:** None

**Items:** None

---

### ACTION 0x0179 (377) @ Ghidra 0x2253F

**Disassembly:**
```asm
2253F: push     0xC
22544: call     get_current_room_number
22549: push     ebx
2254A: push     edx
2254B: mov      ebx, 3             ; branch = 3
22550: xor      edx, edx           ; npc = 0
22552: mov      eax, 0x2D          ; room = 45
22557: jmp      0x222E3            ; → call update_conversation_state; pop; ret
```

**What it does:** Updates conversation state for room 45, NPC 0 to branch 3.

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=45, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x017A (378) @ Ghidra 0x2255C

**Disassembly:**
```asm
2255C: push     0xC
22561: call     get_current_room_number
22566: push     ebx
22567: push     edx
22568: mov      ebx, 3             ; branch = 3
2256D: xor      edx, edx           ; npc = 0
2256F: mov      eax, 0x31          ; room = 49
22574: jmp      0x222E3            ; → call update_conversation_state; pop; ret
```

**What it does:** Updates conversation state for room 49, NPC 0 to branch 3.

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=49, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x0178 (376) @ Ghidra 0x22579

**Disassembly:**
```asm
22579: push     0x2C
2257E: call     get_current_room_number
22583: push     ebx / ecx / edx
22586: push     0 / 0 / 1 / 1 / 4 / 0x66 / 0x33   ; fight anim params
22594: mov      ax, [0xFB98]        ; Alfred Y
2259A: sub      eax, 0x66           ; Y offset = AlfredY - 102
2259D: xor      ecx, ecx
2259F: mov      cx, ax              ; height = Y offset
225A2: xor      ebx, ebx
225A4: mov      bx, [0xFB96]        ; Alfred X
225AB: mov      edx, 0x2070         ; anim data ptr offset
225B0: mov      eax, 0x2D5B98       ; anim base ptr
225B5: call     play_fight_animation
225BA: call     render_menu_screen
225BF: mov      eax, 0xC            ; room = 12
225C4: call     load_room_graphics_and_palette_dynamic
225C9: mov      eax, [0xFA7C]
225CE: call     draw_cursor_to_screen
225D3: push     0x168               ; chain to action 360
225D8: call     wait_or_process_input
225DD: add      esp, 4
225E0: mov      eax, 0xFF
225E5: call     render_scene         ; full render
225EA: cmp      byte ptr [0xFB8C], 0   ; check animation complete flag
225F1: je       0x225D3             ; loop until done
225F3: mov      eax, [0xFAB8]
225F8: call     set_vga_palette
225FD: mov      ebx, 2             ; branch = 2
22602: xor      edx, edx           ; npc = 0
22604: mov      eax, 0x2D          ; room = 45
22609: jmp      0x20446            ; → call update_conversation_state; pop ecx/edx/ebx; ret
```

**What it does:** Plays a fight animation sequence. Uses Alfred's position to calculate animation parameters (base at 0x2D5B98, data offset 0x2070). Then reloads room 12 graphics and enters a render loop waiting for animation to complete (polls [0xFB8C]). After the animation ends, restores the VGA palette and updates conversation state for room 45, NPC 0 to branch 2.

**State flags:**
- Reads: `[0xFB98]` (Alfred Y), `[0xFB96]` (Alfred X), `[0xFA7C]` (cursor data), `[0xFB8C]` (anim complete flag), `[0xFAB8]` (palette ptr)
- Writes: VGA palette restored

**Chains to:** `play_fight_animation(...)`, `wait_or_process_input(action=0x168/360)`, `load_room_graphics_and_palette_dynamic(room=12)`

**Conversation updates:** `update_conversation_state(room=45, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x017C (380) @ Ghidra 0x2260E

**Disassembly:**
```asm
2260E: push     0xC
22613: call     get_current_room_number
22618: push     ebx
22619: push     edx
; Clear/init multiple graphics buffers:
2261A: mov      eax, [0xFAB8]       ; palette buffer
2261F: mov      ebx, 0x300          ; size = 768 (full VGA palette)
22624: xor      edx, edx            ; fill = 0
22626: call     memset_or_init_buffer
; Clear back buffer 1
2262B: mov      eax, [0xFAD8]       ; buffer 1
22630: mov      ebx, 0x40000        ; 256KB
22635: xor      edx, edx
22637: call     memset_or_init_buffer
; Clear back buffer 2
2263C: mov      eax, [0xFADC]       ; buffer 2
22641: mov      ebx, 0x40000
22646: xor      edx, edx
22648: call     memset_or_init_buffer
; Clear buffer 3
2264D: mov      eax, [0xFA9C]
22652: mov      ebx, 0x40000
22657: xor      edx, edx
22659: call     memset_or_init_buffer
; Clear screen buffer
2265E: mov      eax, [0xFA94]
22663: mov      ebx, 0x4C339        ; ~312KB
22668: xor      edx, edx
2266A: call     memset_or_init_buffer
; Clear buffer 4
2266F: mov      eax, [0xFABC]
22674: mov      ebx, 0x6BAA8        ; ~441KB
22679: xor      edx, edx
2267B: call     memset_or_init_buffer
; Clear buffer 5
22680: mov      eax, [0xFAD0]
22685: mov      ebx, 0x2B1E2        ; ~176KB
2268A: xor      edx, edx
2268C: call     memset_or_init_buffer
; Apply blank palette (screen goes black)
22691: mov      eax, [0xFAB8]
22696: call     set_vga_palette
; Render (blank screen)
2269B: call     setup_alfred_frame_from_state
226A0: call     render_scene(0)
; Set custom palette entries:
226A7: mov      eax, [0xFAB8]
226AC: mov      byte ptr [eax + 0x2CA], 0x3C   ; palette[0xF2].R = 60
226B3: mov      eax, [0xFAB8]
226B8: mov      byte ptr [eax + 0x2CB], 0x39   ; palette[0xF2].G = 57
226BF: mov      eax, [0xFAB8]
226C4: mov      byte ptr [eax + 0x2CC], 0x39   ; palette[0xF2].B = 57
226CB: mov      eax, [0xFAB8]
226D0: mov      byte ptr [eax + 0x27], 0x3F    ; palette[0x0D].R = 63
226D4: mov      eax, [0xFAB8]
226D9: mov      byte ptr [eax + 0x28], 0x15    ; palette[0x0D].G = 21
226DD: mov      eax, [0xFAB8]
226E2: mov      byte ptr [eax + 0x29], 0x3F    ; palette[0x0D].B = 63
; Apply custom palette
226E6: mov      eax, [0xFAB8]
226EB: call     set_vga_palette
226F0: pop      edx
226F1: pop      ebx
226F2: ret
```

**What it does:** Clears all graphics buffers (palette, multiple back buffers, screen buffer) to zero, renders a blank frame, then sets two specific palette entries: index 0xF2 (242) to RGB(60,57,57) — a muted gray — and index 0x0D (13) to RGB(63,21,63) — bright magenta/purple. This creates a mostly-black screen with two specific colors available. Likely a screen transition or special effect setup (e.g., credits screen or death screen).

**State flags:**
- Writes: All graphics buffers cleared to 0, palette entries [0xF2] and [0x0D] modified

**Chains to:** `setup_alfred_frame_from_state`, `render_scene`

**Conversation updates:** None

**Items:** None

---

### ACTION 0x017D (381) @ Ghidra 0x226F3

**Disassembly:**
```asm
226F3: push     0x2C
226F8: call     get_current_room_number
226FD: push     ebx / ecx / edx
22700: jmp      0x21BF4
  ; --- jump target at 0x21BF4 ---
21BF4: xor      eax, eax
21BF6: mov      al, [0x13002]       ; volume
21BFB: push     eax
21BFC: mov      edx, [0x13234]      ; sound data ptr
21C02: push     edx
21C03: push     0x20                ; flags = 0x20
21C05: push     0x100               ; pan = 256 (center)
21C0A: push     0x100               ; rate = 256 (normal)
21C0F: push     -1                  ; loop = -1 (forever)
21C11: mov      ebx, [0x13204]      ; sound handle
21C17: push     ebx
21C18: call     play_ambient_sound
21C1D: pop      edx / ecx / ebx
21C20: ret
```

**What it does:** Starts playing the room's ambient sound in an infinite loop at normal rate, centered pan, with the current volume level.

**State flags:**
- Reads: `[0x13002]` (volume), `[0x13234]` (sound data), `[0x13204]` (sound handle)

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

### ACTION 0x017E (382) @ Ghidra 0x22705

**Disassembly:**
```asm
22705: push     0x30
2270A: call     get_current_room_number
2270F: push     ebx / ecx / edx / esi
22713: mov      edx, 6             ; slot = 6
22718: mov      eax, 0x169          ; sound file ID = 361
2271D: call     load_sound_file
; Play ambient sound (looping, rate 3)
22722: xor      eax, eax
22724: mov      al, [0x13002]       ; volume
22729: push     eax
2272A: mov      edx, [0x1322C]      ; sound data (slot-specific)
22730: push     edx
22731: push     0x20                ; flags
22733: push     0x100               ; pan
22738: push     0x100               ; rate
2273D: push     3                   ; loop count = 3
2273F: mov      ebx, [0x13204]      ; sound handle
22745: push     ebx
22746: call     play_ambient_sound
; Animation wait loop:
2274B: push     0x176               ; chain action = 0x176 (374)
22750: call     wait_or_process_input
22755: add      esp, 4
22758: call     setup_alfred_frame_from_state
2275D: call     render_scene(0)
; Check if sound finished playing
22764: mov      eax, [0x13204]      ; sound handle
22769: mov      edx, 3              ; check mode
2276E: call     play_or_check_sound
22773: test     al, al
22775: je       0x2274B             ; loop until sound done
; Clean up sound
22777: xor      eax, eax
22779: mov      al, [0x13002]       ; volume
2277E: push     eax
2277F: mov      ecx, [0x1322C]      ; sound data
22785: push     ecx
22786: mov      esi, [0x13204]      ; sound handle
2278C: push     esi
2278D: call     sound_cleanup
22792: mov      eax, [0x130B8]      ; final sound effect
22797: jmp      0x150EF
  ; --- jump target ---
150EF: call     play_sound          ; play final sound
150F4: pop      esi / edx / ecx / ebx
150F8: ret
```

**What it does:** Loads sound file ID 361 (0x169) into slot 6, plays it as ambient sound looping 3 times, then enters a render loop (chaining action 374 for input processing) waiting for the sound to finish. Once done, cleans up the sound resources and plays a final sound effect from [0x130B8]. This is likely a scripted sound event (e.g., a monster roar, thunder, etc.).

**State flags:**
- Reads: `[0x13002]` (volume), `[0x13204]` (sound handle), `[0x1322C]` (sound data), `[0x130B8]` (final SFX)
- Writes: Sound slot 6 loaded

**Chains to:** `wait_or_process_input(action=0x176/374)`, `load_sound_file(id=361, slot=6)`, `sound_cleanup`, `play_sound`

**Conversation updates:** None

**Items:** None

---

### ACTION 0x017F (383) @ Ghidra 0x2279C

**Disassembly:**
```asm
2279C: push     0xC
227A1: call     get_current_room_number
227A6: push     ebx
227A7: push     edx
227A8: mov      ebx, 2             ; branch = 2
227AD: jmp      0x222DC
  ; --- at 0x222DC ---
222DC: xor      edx, edx           ; npc = 0
222DE: mov      eax, 0x1A          ; room = 26
222E3: call     update_conversation_state
222E8: pop      edx
222E9: pop      ebx
222EA: ret
```

**What it does:** Updates conversation state for room 26, NPC 0 to branch 2.

**State flags:** None

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=26, npc=0, branch=2)`

**Items:** None

---

## Summary Table

| Action | Hex | Address | Type | Room | NPC | Branch | Notes |
|--------|-----|---------|------|------|-----|--------|-------|
| 360 | 0x0168 | 0x2222D | NPC text + flag | 25 | 0 | — | Clears [0x95F2]=0, setup_npc_text(25,0,1,25) |
| 361 | 0x0169 | 0x2223E | NPC text | 25 | 0 | — | setup_npc_text(25,0,1,25) |
| 362 | 0x016A | 0x2224D | NPC text + flag | 25 | 0 | — | Sets [0x95F3]=1, setup_npc_text(25,0,1,25) |
| 364 | 0x016C | 0x22263 | NPC text | 25 | 0 | — | setup_npc_text(25,0,27,43) — different branch |
| 365 | 0x016D | 0x22286 | Conv update + flag | 25 | 0 | 1 | Sets [0x95D0]=1 |
| 366 | 0x016E | 0x22290 | Conv update | 25 | 0 | 1 | |
| 367 | 0x016F | 0x222AA | Conv + sprite check | 25 | 0 | 27 | Then check_sprite_hover(mode=2) |
| 368 | 0x0170 | 0x222C0 | No-op | — | — | — | Placeholder/disabled |
| 369 | 0x0171 | 0x222CB | Conv update | 26 | 0 | 1 | |
| 370 | 0x0172 | 0x222EB | Give item | — | — | — | **Item 111 (0x6F)** |
| 371 | 0x0173 | 0x222FF | Give items + conv | 27 | 0 | 2 | **Items 111 + 110** |
| 372 | 0x0174 | 0x2232B | Conv update | 34 | 0 | 2 | |
| 373 | 0x0175 | 0x22345 | Conv update | 34 | 0 | 3 | |
| 374 | 0x0176 | 0x22358 | Conv update | 34 | 0 | 1 | |
| 375 | 0x0177 | 0x2236B | **Cutscene** | — | — | — | 5-phase animation, warp to room 48 |
| 376 | 0x0178 | 0x22579 | **Fight anim** + conv | 45 | 0 | 2 | Fight animation, reload room 12 |
| 377 | 0x0179 | 0x2253F | Conv update | 45 | 0 | 3 | |
| 378 | 0x017A | 0x2255C | Conv update | 49 | 0 | 3 | |
| 380 | 0x017C | 0x2260E | **Screen clear** | — | — | — | Clear all buffers, set palette entries 0x0D + 0xF2 |
| 381 | 0x017D | 0x226F3 | Ambient sound | — | — | — | Start looping ambient sound |
| 382 | 0x017E | 0x22705 | **Sound event** | — | — | — | Load+play sound 361, wait, cleanup, play SFX |
| 383 | 0x017F | 0x2279C | Conv update | 26 | 0 | 2 | |
