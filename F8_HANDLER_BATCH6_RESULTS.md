# F8 Action Handler Batch 6 - Decompilation Results

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
| 0x152B6 | `check_keyboard_input` | Check keyboard input, returns nonzero in AL if key pressed |
| 0x2B11B | `outport_byte` | Write byte to I/O port (EAX=port, EDX=value) |
| 0x25487 | `display_text_with_voice` | Display text with optional voice playback (EAX=text_ptr) |

### Note on `play_get_naked_easter_egg` (0x1B1A2)
Despite the Ghidra label, this is actually a general NPC dialog animation function used throughout the game. It renders an NPC sprite talking animation synced to dialog text. Parameters: EAX = NPC index (0 or 1), EDX = text data pointer.

## Shared Code Blocks

### Shared conv tail at 0x21E61 (room 22, NPC 0)
```asm
21E61: xor      edx, edx         ; npc = 0
21E63: mov      eax, 0x16        ; room = 22
21E68: call     update_conversation_state
21E6D: pop      edx
21E6E: pop      ebx
21E6F: ret
```
Used by: actions 343, 344, 345, 346, 347 (jmp 0x21E61, different EBX branch values)

### Shared conv tail at 0x222E3 (generic)
```asm
222E3: call     update_conversation_state  ; EAX/EDX/EBX set by caller
222E8: pop      edx
222E9: pop      ebx
222EA: ret
```
Used by: actions 350 (room=22, npc=1, branch=1), 353 (room=23, npc=0, branch=2), 356 (room=23, npc=0, branch=3)

### Shared conv + NPC text tail at 0x2216F (room 23, NPC 0)
```asm
2216F: xor      edx, edx         ; npc = 0
22171: mov      eax, 0x17        ; room = 23
22176: jmp      0x222E3          ; → call update_conversation_state; pop edx, ebx; ret
```
Used by: actions 353 (branch=2, sets ebx before jmp 0x2216F), 356 (branch=3, jmp 0x2216F)

### Shared NPC text setup at 0x221E9 (room 25, NPC 0)
```asm
221E9: mov      ecx, 1           ; flag = 1
221EE: mov      ebx, 0x19        ; table_idx = 25
221F3: xor      edx, edx         ; npc = 0
221F5: mov      eax, ebx         ; room = 25
221F7: call     setup_npc_conversation_text
221FC: pop      edx
221FD: pop      ecx
221FE: pop      ebx
221FF: ret
```
Used by: actions 357, 358, 359

### Shared dialog+voice tail at 0x1D66A
```asm
1D66A: call     display_text_with_voice   ; EAX = text ptr
1D66F: pop      edx
1D670: ret
```
Used by: action 351 (final text after dialog sequence)

### Anti-piracy crash at 0x21FA1
```asm
21FA1: xor      ah, ah
21FA3: mov      byte ptr [0x1179E], ah    ; clear flag
21FA9: xor      ebx, ebx                  ; ebx = 0
21FAB: mov      eax, 1
21FB0: mov      edx, eax
21FB2: sar      edx, 0x1F                 ; edx = 0
21FB5: idiv     ebx                       ; *** DIVIDE BY ZERO - INTENTIONAL CRASH ***
```
Used by: action 348 (triggered when user presses key during anti-piracy check)

---

## Handler Analysis

---

### ACTION 0x0157 (343) @ Ghidra 0x21ECF

**Disassembly:**
```asm
21ECF: push     0xC
21ED4: call     get_current_room_number
21ED9: push     ebx
21EDA: push     edx
21EDB: mov      ebx, 8           ; branch = 8
21EE0: jmp      0x21E61          ; → edx=0, eax=0x16, call update_conversation_state
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/8);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 8.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 8

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=8)`

**Items:** None

---

### ACTION 0x0158 (344) @ Ghidra 0x21EE5

**Disassembly:**
```asm
21EE5: push     0xC
21EEA: call     get_current_room_number
21EEF: push     ebx
21EF0: push     edx
21EF1: mov      ebx, 9           ; branch = 9
21EF6: jmp      0x21E61          ; → edx=0, eax=0x16, call update_conversation_state
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/9);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 9.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 9

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=9)`

**Items:** None

---

### ACTION 0x0159 (345) @ Ghidra 0x21EFB

**Disassembly:**
```asm
21EFB: push     0xC
21F00: call     get_current_room_number
21F05: push     ebx
21F06: push     edx
21F07: mov      ebx, 0xA         ; branch = 10
21F0C: jmp      0x21E61          ; → edx=0, eax=0x16, call update_conversation_state
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/10);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 10.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 10

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=10)`

**Items:** None

---

### ACTION 0x015A (346) @ Ghidra 0x21F11

**Disassembly:**
```asm
21F11: push     0xC
21F16: call     get_current_room_number
21F1B: push     ebx
21F1C: push     edx
21F1D: mov      ebx, 0xB         ; branch = 11
21F22: jmp      0x21E61          ; → edx=0, eax=0x16, call update_conversation_state
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/11);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 11.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 11

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=11)`

**Items:** None

---

### ACTION 0x015B (347) @ Ghidra 0x21F27

**Disassembly:**
```asm
21F27: push     0xC
21F2C: call     get_current_room_number
21F31: push     ebx
21F32: push     edx
21F33: mov      ebx, 0xC         ; branch = 12
21F38: jmp      0x21E61          ; → edx=0, eax=0x16, call update_conversation_state
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/12);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 12.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 12

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=12)`

**Items:** None

---

### ACTION 0x015C (348) @ Ghidra 0x21F3D

**Disassembly:**
```asm
21F3D: push     0x14
21F42: call     get_current_room_number
21F47: push     ebx
21F48: push     edx
21F49: mov      eax, dword ptr [0xFAC8]    ; sprite data ptr
21F4E: mov      byte ptr [eax + 5], 2      ; set sprite state byte to 2
21F52: xor      ebx, ebx                   ; ebx = 0 (counter / data pointer)
21F54: call     init_or_stop_sound          ; stop all sound
; --- loop starts ---
21F59: push     0x163                       ; delay = 355 ticks
21F5E: call     wait_or_process_input
21F63: add      esp, 4
21F66: call     check_keyboard_input        ; check if key pressed
21F6B: test     al, al
21F6D: jne      0x21FA1                     ; if key → CRASH (divide by zero)
21F6F: call     random_number_generator
21F74: mov      edx, eax
21F76: and      edx, 0xF                    ; mask to 0-15
21F79: call     random_number_generator
21F7E: imul     eax, edx                    ; random * random
21F81: mov      dword ptr [0xFADC], eax     ; store as visual effect param
21F86: call     copy_background_to_front_buffer
21F8B: call     present_frame_to_screen     ; display garbage visuals
21F90: xor      edx, edx
21F92: mov      dl, byte ptr [ebx]          ; read byte from address [ebx]
21F94: mov      eax, 0x61                   ; port 0x61 = PC speaker
21F99: call     outport_byte                ; send garbage to speaker
21F9E: inc      ebx                         ; next byte
21F9F: jmp      0x21F59                     ; infinite loop
; --- crash branch ---
21FA1: xor      ah, ah
21FA3: mov      byte ptr [0x1179E], ah      ; clear flag
21FA9: xor      ebx, ebx
21FAB: mov      eax, 1
21FB0: mov      edx, eax
21FB2: sar      edx, 0x1F
21FB5: idiv     ebx                         ; DIVIDE BY ZERO → crash
```

**Code:**
```c
get_current_room_number();
sprite_data_ptr = *(byte**)0xFAC8;
sprite_data_ptr[5] = 2;  // set sprite state
init_or_stop_sound(0);    // silence

int counter = 0;
while (true) {
    wait_or_process_input(355);
    if (check_keyboard_input()) {
        *(byte*)0x1179E = 0;
        1 / 0;  // INTENTIONAL CRASH - anti-piracy
    }
    int r1 = random_number_generator() & 0xF;
    int r2 = random_number_generator();
    *(int*)0xFADC = r2 * r1;  // visual noise parameter
    copy_background_to_front_buffer();
    present_frame_to_screen();  // show visual noise
    outport(0x61, *(byte*)counter);  // PC speaker garbage
    counter++;
}
```

**What it does:** **ANTI-PIRACY HANDLER.** Enters an infinite loop that:
1. Shows random visual noise on screen (via randomized `[0xFADC]` parameter)
2. Plays garbage audio through the PC speaker (reading sequential memory bytes and sending to port 0x61)
3. If user presses any key, intentionally crashes the game with a divide-by-zero exception

The loop has NO normal exit. The game appears "broken" to discourage piracy reports. Room context 0x14 = room 20.

**State flags:** Reads/writes `[0xFAC8]+5`, `[0xFADC]`, `[0x1179E]`

**Chains to:** `init_or_stop_sound`, `wait_or_process_input`, `check_keyboard_input`, `random_number_generator`, `copy_background_to_front_buffer`, `present_frame_to_screen`, `outport_byte`

**Conversation updates:** None

**Items:** None

---

### ACTION 0x015D (349) @ Ghidra 0x21FC8

**Disassembly:**
```asm
21FC8: push     0xC
21FCD: call     get_current_room_number
21FD2: push     ebx
21FD3: push     edx
21FD4: xor      byte ptr [0x95F0], 1      ; toggle bit 0
21FDB: xor      eax, eax
21FDD: mov      al, byte ptr [0x95F0]     ; read counter
21FE2: cmp      eax, 3
21FE5: jne      0x21FF8                   ; if != 3, skip
21FE7: mov      ebx, 1                    ; branch = 1
21FEC: mov      edx, ebx                  ; npc = 1
21FEE: mov      eax, 0x16                 ; room = 22
21FF3: call     update_conversation_state
21FF8: pop      edx
21FF9: pop      ebx
21FFA: ret
```

**Code:**
```c
get_current_room_number();
*(byte*)0x95F0 ^= 1;  // toggle bit 0
if (*(byte*)0x95F0 == 3) {  // both bits set
    update_conversation_state(/*room=*/22, /*npc=*/1, /*branch=*/1);
}
```

**What it does:** Toggles bit 0 of the combination flag at `[0x95F0]`. When the value reaches 3 (both bit 0 and bit 1 set), advances conversation for NPC 1 in room 22 to branch 1. This is half of a two-action combination puzzle — paired with action 350.

**State flags:** XOR `[0x95F0]` bit 0. Conditionally writes conv state.

**Chains to:** None (conditionally calls `update_conversation_state`)

**Conversation updates:** `update_conversation_state(room=22, npc=1, branch=1)` — only when `[0x95F0]` == 3

**Items:** None

---

### ACTION 0x015E (350) @ Ghidra 0x21FFB

**Disassembly:**
```asm
21FFB: push     0xC
22000: call     get_current_room_number
22005: push     ebx
22006: push     edx
22007: xor      byte ptr [0x95F0], 2      ; toggle bit 1
2200E: xor      eax, eax
22010: mov      al, byte ptr [0x95F0]     ; read counter
22015: cmp      eax, 3
22018: jne      0x222E8                   ; if != 3, skip to cleanup
2201E: mov      ebx, 1                    ; branch = 1
22023: mov      edx, ebx                  ; npc = 1
22025: mov      eax, 0x16                 ; room = 22
2202A: jmp      0x222E3                   ; → call update_conversation_state; ret
; --- at 0x222E3 ---
222E3: call     update_conversation_state
222E8: pop      edx
222E9: pop      ebx
222EA: ret
```

**Code:**
```c
get_current_room_number();
*(byte*)0x95F0 ^= 2;  // toggle bit 1
if (*(byte*)0x95F0 == 3) {  // both bits set
    update_conversation_state(/*room=*/22, /*npc=*/1, /*branch=*/1);
}
```

**What it does:** Toggles bit 1 of the combination flag at `[0x95F0]`. When the value reaches 3 (both bits set), advances conversation for NPC 1 in room 22 to branch 1. This is the other half of the two-action combination puzzle — paired with action 349.

**State flags:** XOR `[0x95F0]` bit 1. Conditionally writes conv state.

**Chains to:** None (conditionally calls `update_conversation_state`)

**Conversation updates:** `update_conversation_state(room=22, npc=1, branch=1)` — only when `[0x95F0]` == 3

**Items:** None

---

### ACTION 0x015F (351) @ Ghidra 0x2202F

**Disassembly:**
```asm
2202F: push     8
22034: call     get_current_room_number
22039: push     edx
; --- 17 dialog lines, alternating NPC 0 and NPC 1 ---
2203A: mov      edx, [0xBB80]     ; text ptr 1
22040: xor      eax, eax          ; NPC 0
22042: call     display_npc_dialog_animation
22047: mov      edx, [0xBB84]     ; text ptr 2
2204D: mov      eax, 1            ; NPC 1
22052: call     display_npc_dialog_animation
22057: mov      edx, [0xBB88]     ; text ptr 3
2205D: xor      eax, eax          ; NPC 0
2205F: call     display_npc_dialog_animation
22064: mov      edx, [0xBB8C]     ; text ptr 4
2206A: mov      eax, 1            ; NPC 1
2206F: call     display_npc_dialog_animation
22074: mov      edx, [0xBB90]     ; text ptr 5
2207A: xor      eax, eax          ; NPC 0
2207C: call     display_npc_dialog_animation
22081: mov      edx, [0xBB94]     ; text ptr 6
22087: mov      eax, 1            ; NPC 1
2208C: call     display_npc_dialog_animation
22091: mov      edx, [0xBB98]     ; text ptr 7
22097: xor      eax, eax          ; NPC 0
22099: call     display_npc_dialog_animation
2209E: mov      edx, [0xBB9C]     ; text ptr 8
220A4: mov      eax, 1            ; NPC 1
220A9: call     display_npc_dialog_animation
220AE: mov      edx, [0xBBA0]     ; text ptr 9
220B4: xor      eax, eax          ; NPC 0
220B6: call     display_npc_dialog_animation
220BB: mov      edx, [0xBBA4]     ; text ptr 10
220C1: mov      eax, 1            ; NPC 1
220C6: call     display_npc_dialog_animation
220CB: mov      edx, [0xBBA8]     ; text ptr 11
220D1: xor      eax, eax          ; NPC 0
220D3: call     display_npc_dialog_animation
220D8: mov      edx, [0xBBAC]     ; text ptr 12
220DE: mov      eax, 1            ; NPC 1
220E3: call     display_npc_dialog_animation
220E8: mov      edx, [0xBBB0]     ; text ptr 13
220EE: xor      eax, eax          ; NPC 0
220F0: call     display_npc_dialog_animation
220F5: mov      edx, [0xBBB4]     ; text ptr 14
220FB: mov      eax, 1            ; NPC 1
22100: call     display_npc_dialog_animation
22105: mov      edx, [0xBBB8]     ; text ptr 15
2210B: xor      eax, eax          ; NPC 0
2210D: call     display_npc_dialog_animation
22112: mov      edx, [0xBBBC]     ; text ptr 16
22118: mov      eax, 1            ; NPC 1
2211D: call     display_npc_dialog_animation
22122: mov      edx, [0xBBC0]     ; text ptr 17
22128: xor      eax, eax          ; NPC 0
2212A: call     display_npc_dialog_animation
; --- final text ---
2212F: mov      eax, [0xBBC4]     ; text ptr 18
22134: jmp      0x1D66A           ; → call display_text_with_voice; pop edx; ret
```

**Code:**
```c
get_current_room_number();
// 17-line dialog alternating between NPC 0 and NPC 1
// Text pointers from table at 0xBB80 (9 pairs + 1 final)
for (int i = 0; i < 17; i++) {
    display_npc_dialog_animation(
        /*npc=*/ i % 2,
        /*text_ptr=*/ text_table[0xBB80 + i*4]
    );
}
// 18th text displayed with voice
display_text_with_voice(text_table[0xBBC4]);
```

**What it does:** Plays a long 18-line cutscene conversation in room 8 between two NPCs (indexes 0 and 1), alternating who speaks. Text data pointers are read from a table at `[0xBB80]` through `[0xBBC4]` (18 entries × 4 bytes = 72 bytes). The first 17 lines use animated NPC talking sprites; the last line uses text-with-voice display.

**State flags:** Reads text pointer table `[0xBB80]` - `[0xBBC4]`

**Chains to:** `display_npc_dialog_animation` ×17, `display_text_with_voice` ×1

**Conversation updates:** None

**Items:** None

---

### ACTION 0x0161 (353) @ Ghidra 0x2215E

**Disassembly:**
```asm
2215E: push     0xC
22163: call     get_current_room_number
22168: push     ebx
22169: push     edx
2216A: mov      ebx, 2           ; branch = 2
2216F: xor      edx, edx         ; npc = 0
22171: mov      eax, 0x17        ; room = 23
22176: jmp      0x222E3          ; → call update_conversation_state; pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/23, /*npc=*/0, /*branch=*/2);
```

**What it does:** Advances conversation tree for NPC 0 in room 23 to branch 2.

**State flags:** Writes `[0x4FBA4 + 23*4 + 0]` = 2

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=23, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x0162 (354) @ Ghidra 0x2217B

**Disassembly:**
```asm
2217B: push     4
22180: call     get_current_room_number
22185: mov      eax, 0x69        ; item = 105
2218A: jmp      process_inventory_action
```

**Code:**
```c
get_current_room_number();
process_inventory_action(105);  // tail call
```

**What it does:** Gives the player inventory item 105 (0x69).

**State flags:** Via `process_inventory_action` internals

**Chains to:** `process_inventory_action` (tail call)

**Conversation updates:** None

**Items:** Gives item 105 (0x69)

---

### ACTION 0x0164 (356) @ Ghidra 0x2218F

**Disassembly:**
```asm
2218F: push     0xC
22194: call     get_current_room_number
22199: push     ebx
2219A: push     edx
2219B: mov      ebx, 3           ; branch = 3
221A0: jmp      0x2216F          ; → edx=0, eax=0x17, jmp 0x222E3
; --- at 0x2216F ---
2216F: xor      edx, edx         ; npc = 0
22171: mov      eax, 0x17        ; room = 23
22176: jmp      0x222E3          ; → call update_conversation_state; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/23, /*npc=*/0, /*branch=*/3);
```

**What it does:** Advances conversation tree for NPC 0 in room 23 to branch 3.

**State flags:** Writes `[0x4FBA4 + 23*4 + 0]` = 3

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=23, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x0165 (357) @ Ghidra 0x221A2

**Disassembly:**
```asm
221A2: push     0x10
221A7: call     get_current_room_number
221AC: push     ebx
221AD: push     ecx
221AE: push     edx
221AF: mov      ah, byte ptr [0x95F2]     ; read counter
221B5: test     ah, ah
221B7: je       0x221E9                   ; if 0, skip decrement
221B9: mov      dl, ah
221BB: dec      dl                        ; counter - 1
221BD: mov      byte ptr [0x95F2], dl     ; store decremented
221C3: jmp      0x221E9
; --- shared NPC text setup ---
221E9: mov      ecx, 1                   ; flag = 1
221EE: mov      ebx, 0x19                ; table_idx = 25
221F3: xor      edx, edx                 ; npc = 0
221F5: mov      eax, ebx                 ; room = 25
221F7: call     setup_npc_conversation_text
221FC: pop      edx
221FD: pop      ecx
221FE: pop      ebx
221FF: ret
```

**Code:**
```c
get_current_room_number();
if (*(byte*)0x95F2 != 0) {
    (*(byte*)0x95F2)--;
}
setup_npc_conversation_text(/*room=*/25, /*npc=*/0, /*flag=*/1);
```

**What it does:** Decrements the counter at `[0x95F2]` by 1 (if nonzero), then refreshes NPC 0's conversation text in room 25. Part of a counter-based puzzle (see actions 358, 359). Room context = 0x10 (room 16).

**State flags:** Reads/writes `[0x95F2]` (decrement by 1)

**Chains to:** `setup_npc_conversation_text`

**Conversation updates:** `setup_npc_conversation_text(room=25, npc=0, flag=1)`

**Items:** None

---

### ACTION 0x0166 (358) @ Ghidra 0x221C5

**Disassembly:**
```asm
221C5: push     0x10
221CA: call     get_current_room_number
221CF: push     ebx
221D0: push     ecx
221D1: push     edx
221D2: xor      eax, eax
221D4: mov      al, byte ptr [0x95F2]     ; read counter
221D9: cmp      eax, 1
221DC: jle      0x221E9                   ; if <= 1, skip
221DE: mov      ah, al
221E0: sub      ah, 2                     ; counter - 2
221E3: mov      byte ptr [0x95F2], ah     ; store
221E9: mov      ecx, 1
221EE: mov      ebx, 0x19
221F3: xor      edx, edx
221F5: mov      eax, ebx
221F7: call     setup_npc_conversation_text
221FC: pop      edx
221FD: pop      ecx
221FE: pop      ebx
221FF: ret
```

**Code:**
```c
get_current_room_number();
if (*(byte*)0x95F2 > 1) {
    *(byte*)0x95F2 -= 2;
}
setup_npc_conversation_text(/*room=*/25, /*npc=*/0, /*flag=*/1);
```

**What it does:** Decrements the counter at `[0x95F2]` by 2 (only if > 1), then refreshes NPC 0's conversation text in room 25. A stronger version of action 357 (subtracts 2 instead of 1). Room context = 0x10 (room 16).

**State flags:** Reads/writes `[0x95F2]` (decrement by 2 if > 1)

**Chains to:** `setup_npc_conversation_text`

**Conversation updates:** `setup_npc_conversation_text(room=25, npc=0, flag=1)`

**Items:** None

---

### ACTION 0x0167 (359) @ Ghidra 0x22200

**Disassembly:**
```asm
22200: push     0x10
22205: call     get_current_room_number
2220A: push     ebx
2220B: push     ecx
2220C: push     edx
2220D: inc      byte ptr [0x95F2]         ; counter++
22213: xor      eax, eax
22215: mov      al, byte ptr [0x95F2]     ; read counter
2221A: cmp      eax, 0xF                  ; compare to 15
2221D: jne      0x221E9                   ; if != 15, just update NPC text
; --- counter reached 15 ---
2221F: mov      eax, 0x6A                 ; item = 106
22224: call     process_inventory_action   ; give item 106
22229: xor      dl, dl                    ; dl = 0
2222B: jmp      0x221BD                   ; → [0x95F2] = 0; jmp 0x221E9
; --- at 0x221BD ---
221BD: mov      byte ptr [0x95F2], dl     ; reset counter to 0
221C3: jmp      0x221E9                   ; → setup_npc_conversation_text(25, 0, 1); ret
```

**Code:**
```c
get_current_room_number();
(*(byte*)0x95F2)++;
if (*(byte*)0x95F2 == 15) {
    process_inventory_action(106);  // give item 106
    *(byte*)0x95F2 = 0;            // reset counter
}
setup_npc_conversation_text(/*room=*/25, /*npc=*/0, /*flag=*/1);
```

**What it does:** Increments the counter at `[0x95F2]`. When it reaches 15, gives the player item 106 (0x6A) and resets the counter to 0. Always refreshes NPC text afterward. Room context = 0x10 (room 16).

This forms a **collect-15 puzzle** with actions 357/358/359:
- Action 359 increments the counter (+1)
- Action 357 decrements the counter (-1)
- Action 358 decrements the counter (-2)
- When counter reaches exactly 15, player receives item 106

**State flags:** Reads/writes `[0x95F2]` (increment, check for 15, reset)

**Chains to:** `process_inventory_action` (conditionally), `setup_npc_conversation_text`

**Conversation updates:** `setup_npc_conversation_text(room=25, npc=0, flag=1)`

**Items:** Gives item 106 (0x6A) when counter reaches 15

---

## Summary Table

| Action | Dec | Room Context | Type | Key Operation |
|--------|-----|-------------|------|---------------|
| 0x0157 | 343 | 12 | Conv update | room 22, NPC 0, branch 8 |
| 0x0158 | 344 | 12 | Conv update | room 22, NPC 0, branch 9 |
| 0x0159 | 345 | 12 | Conv update | room 22, NPC 0, branch 10 |
| 0x015A | 346 | 12 | Conv update | room 22, NPC 0, branch 11 |
| 0x015B | 347 | 12 | Conv update | room 22, NPC 0, branch 12 |
| 0x015C | 348 | 20 | Anti-piracy | Infinite noise loop + div-by-zero crash |
| 0x015D | 349 | 12 | Combo flag | XOR bit 0 of [0x95F0]; if 3→conv(22,1,1) |
| 0x015E | 350 | 12 | Combo flag | XOR bit 1 of [0x95F0]; if 3→conv(22,1,1) |
| 0x015F | 351 | 8 | Dialog cutscene | 18-line NPC dialog from table [0xBB80-0xBBC4] |
| 0x0161 | 353 | 12 | Conv update | room 23, NPC 0, branch 2 |
| 0x0162 | 354 | 4 | Give item | item 105 (0x69) |
| 0x0164 | 356 | 12 | Conv update | room 23, NPC 0, branch 3 |
| 0x0165 | 357 | 16 | Counter puzzle | [0x95F2]-- then NPC text(25,0,1) |
| 0x0166 | 358 | 16 | Counter puzzle | [0x95F2]-=2 then NPC text(25,0,1) |
| 0x0167 | 359 | 16 | Counter puzzle | [0x95F2]++; if 15→give item 106, reset |

## State Variables

| Address | Type | Used By | Purpose |
|---------|------|---------|---------|
| `[0x95F0]` | byte | 349, 350 | Two-bit combination flag (bit 0 + bit 1 = 3 triggers conv) |
| `[0x95F2]` | byte | 357, 358, 359 | Counter for collect-15 puzzle (0-15 range) |
| `[0xFAC8]` | dword ptr | 348 | Sprite data pointer |
| `[0xFADC]` | dword | 348 | Visual effect parameter (randomized) |
| `[0x1179E]` | byte | 348 | Flag cleared before anti-piracy crash |
| `[0xBB80]-[0xBBC4]` | dword×18 | 351 | Dialog text pointer table for cutscene |

## Hidden Handler at 0x22139 (not in dispatch list)

Between actions 351 and 353, there's a handler at 0x22139 that was NOT in the batch list (likely action 0x0160 / 352):
```asm
22139: push     0xC
2213E: call     get_current_room_number
22143: push     ebx
22144: push     edx
22145: mov      ebx, 3                    ; branch = 3
2214A: xor      edx, edx                  ; npc = 0
2214C: mov      eax, 0x17                 ; room = 23
22151: call     update_conversation_state
22156: call     0x2151D                   ; complex room transition handler
2215B: pop      edx
2215C: pop      ebx
2215D: ret
```
This updates room 23 conv state then calls a complex handler at 0x2151D that:
- Calls `fade_palette_to_black`
- Sets screen coordinates `[0xFB96]`=0x156, `[0xFB98]`=0x115
- Sets `[0xFB9A]` = 2
- Calls `update_conversation_state(room=26, npc=1, branch=1)`
- Sets `[0x95C9]` = 1
- Calls `load_room_and_init_alfred(0x1F)` (room 31)
- Checks `[0x95E6]` and branches further
