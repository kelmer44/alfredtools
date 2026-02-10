# F8 Action Handler Batch 2 - Decompilation Results

## New Function Names (resolved via Ghidra + disassembly)

| Address | Name | Purpose |
|---------|------|---------|
| 0x1B83A | `remove_inventory_item` | Remove item from inventory list (EAX = item to search/remove) |
| 0x1B8B3 | `fade_palette_to_black` | Gradually fades VGA palette to black, calling wait_or_process_input each frame |
| 0x1B94C | `play_arrest_cutscene` | Loads room 5 graphics, plays CD audio (track [0xC240]+25), sets VGA mode — arrest/transition cutscene |
| 0x152F5 | `load_room_and_init_alfred` | Full room load: reads ALFRED.1 data, decompresses backgrounds/sprites, sets Alfred position, inits palette, renders scene (EAX=room, EDX=load_mode) |
| 0x2A6B7 | `write_data_to_alfred1` | Write data to ALFRED.1 file (EAX=src_buf, EDX=size, EBX=flag, ECX=file_handle) |
| 0x2A342 | `file_seek` | Seek in file (EAX=handle, EDX=offset, EBX=whence) |

## Shared Code Blocks

### Shared tail at 0x213CC (used by actions 275, 276)
```asm
213CC: xor edx, edx           ; npc = 0
213CE: mov eax, 0x12          ; room = 18
213D3: call update_conversation_state  ; EAX=room, EDX=npc, EBX=branch (set by caller)
213D8: pop edx
213D9: pop ebx
213DA: ret
```

### Shared tail at 0x213D3 (used by actions 278, 292)
```asm
213D3: call update_conversation_state  ; EAX=room, EDX=npc, EBX=branch (all set by caller)
213D8: pop edx
213D9: pop ebx
213DA: ret
```

### Shared dialog handler at 0x11E1D (used by actions 280, 281, 282)
```asm
11E1D: xor eax, eax                       ; param = 0
11E1F: call play_get_naked_easter_egg      ; display NPC dialog (EDX = data ptr)
11E24: pop edx
11E25: ret
```

### Shared conv tail at 0x21BC0 (used by action 290)
```asm
21BC0: call update_conversation_state      ; EAX/EDX/EBX set by caller
21BC5: pop edx
21BC6: pop ebx
21BC7: ret
```

### Shared conv tail at 0x20446 (used by extended handlers)
```asm
20446: call update_conversation_state
2044B: pop edx
2044C: pop ecx
2044D: pop ebx
2044E: ret
```

---

## Handler Analysis

---

### ACTION 0x0113 (275) @ Ghidra 0x213DB

**Disassembly (0x213DB - 0x213ED):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 2             ; branch = 2
jmp 0x213CC            ; → xor edx,edx; mov eax,0x12; call update_conversation_state; pop; ret
```

**What it does:** Advances conversation state for room 18, NPC 0, branch 2.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=18, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x0114 (276) @ Ghidra 0x213EE

**Disassembly (0x213EE - 0x21400):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 3             ; branch = 3
jmp 0x213CC            ; → xor edx,edx; mov eax,0x12; call update_conversation_state; pop; ret
```

**What it does:** Advances conversation state for room 18, NPC 0, branch 3.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=18, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x0115 (277) @ Ghidra 0x21401

**Disassembly (0x21401 - 0x2142E):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 5             ; branch = 5
xor edx, edx           ; npc = 0
mov eax, 0x12          ; room = 18
call update_conversation_state
mov ah, 1
mov byte [0x95b9], ah  ; SET [0x95B9] = 1
add byte [0x95c4], ah  ; INCREMENT [0x95C4] += 1
pop edx
pop ebx
ret
```

**What it does:** Advances conversation state for room 18, NPC 0, branch 5. Then sets flag [0x95B9] = 1 and increments counter [0x95C4] by 1.

**State flags:**
- Write: [0x95B9] = 1 (set flag)
- Write: [0x95C4] += 1 (increment counter)

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=18, npc=0, branch=5)`

**Items:** None

---

### ACTION 0x0116 (278) @ Ghidra 0x2142F

**Disassembly (0x2142F - 0x21448):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 1             ; branch = 1
xor edx, edx           ; npc = 0
mov eax, 0x14          ; room = 20
jmp 0x213d3            ; → call update_conversation_state; pop edx; pop ebx; ret
```

**What it does:** Advances conversation state for room 20, NPC 0, branch 1.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=20, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x0117 (279) @ Ghidra 0x21449

**Disassembly (0x21449 - 0x214DA):**
```asm
push 8
call get_current_room_number
push edx
mov eax, 0x4b                   ; item = 75 (0x4B)
call remove_inventory_item       ; remove item 75 from inventory
call fade_palette_to_black       ; screen fade out
call play_arrest_cutscene        ; play arrest cutscene (room 5 gfx + CD audio)
mov word [0xfb96], 0x23f        ; Alfred X = 575
mov word [0xfb98], 0xd2         ; Alfred Y = 210
mov byte [0xfb9a], 2            ; Alfred direction = 2 (facing left)
xor edx, edx                    ; load_mode = 0
mov eax, 0x15                   ; room = 21
call load_room_and_init_alfred   ; load room 21 with Alfred at (575, 210)
mov word [0xfba0], 0xffff       ; clear selected action
xor dl, dl
mov byte [0xfba2], dl           ; clear [0xFBA2] = 0
mov byte [0xfba3], dl           ; clear [0xFBA3] = 0
mov byte [0x117a4], 1           ; set temp "batch inventory" flag
mov eax, 0x11                   ; item 17
call process_inventory_action
mov eax, 0x40                   ; item 64
call process_inventory_action
mov eax, 0x18                   ; item 24
call process_inventory_action
mov eax, 0x3b                   ; item 59
call process_inventory_action
mov byte [0x117a4], dl          ; clear temp flag
pop edx
ret
```

**What it does:** Full "arrest" sequence — confiscates item 75, fades screen to black, plays the arrest cutscene, then loads room 21 (jail cell) with Alfred at position (575, 210) facing left. Processes 4 inventory actions (items 17, 64, 24, 59) with a batch flag enabled, then clears the flag.

**State flags:**
- Write: [0xFB96] = 0x23F (Alfred X position = 575)
- Write: [0xFB98] = 0xD2 (Alfred Y position = 210)
- Write: [0xFB9A] = 2 (Alfred direction = left)
- Write: [0xFBA0] = 0xFFFF (no selected action)
- Write: [0xFBA2] = 0, [0xFBA3] = 0
- Write: [0x117A4] = 1 then 0 (batch inventory flag)

**Chains to:** None

**Conversation updates:** None

**Items:**
- REMOVE: item 75 (0x4B) via `remove_inventory_item`
- PROCESS: items 17, 64, 24, 59 via `process_inventory_action`

---

### ACTION 0x0118 (280) @ Ghidra 0x214DB

**Disassembly (0x214DB - 0x214F0):**
```asm
push 8
call get_current_room_number
push edx
mov edx, [0xbacc]      ; load NPC dialog data pointer
jmp 0x11e1d            ; → xor eax,eax; call play_get_naked_easter_egg; pop edx; ret
```

**What it does:** Displays NPC dialog using data pointer from [0xBACC].

**State flags:**
- Read: [0xBACC] — NPC dialog data pointer

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

### ACTION 0x0119 (281) @ Ghidra 0x214F1

**Disassembly (0x214F1 - 0x21506):**
```asm
push 8
call get_current_room_number
push edx
mov edx, [0xbad0]      ; load NPC dialog data pointer
jmp 0x11e1d            ; → xor eax,eax; call play_get_naked_easter_egg; pop edx; ret
```

**What it does:** Displays NPC dialog using data pointer from [0xBAD0].

**State flags:**
- Read: [0xBAD0] — NPC dialog data pointer

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

### ACTION 0x011A (282) @ Ghidra 0x21507

**Disassembly (0x21507 - 0x2151C):**
```asm
push 8
call get_current_room_number
push edx
mov edx, [0xbad4]      ; load NPC dialog data pointer
jmp 0x11e1d            ; → xor eax,eax; call play_get_naked_easter_egg; pop edx; ret
```

**What it does:** Displays NPC dialog using data pointer from [0xBAD4].

**State flags:**
- Read: [0xBAD4] — NPC dialog data pointer

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

### ACTION 0x011D (285) @ Ghidra 0x2151D — SHARED "GO TO JAIL" HANDLER

**Also used by:** actions 0x0123 (291), 0x0160 (352), 0x0163 (355), 0x016B (363)

**Disassembly (0x2151D - 0x21786):**
```asm
push 0x10
call get_current_room_number
push ebx
push ecx
push edx
call fade_palette_to_black           ; fade screen to black
mov word [0xfb96], 0x156             ; Alfred X = 342
mov word [0xfb98], 0x115             ; Alfred Y = 277
mov byte [0xfb9a], 2                 ; Alfred direction = 2 (left)
mov ebx, 1                           ; branch = 1
mov edx, ebx                         ; npc = 1
mov eax, 0x1a                        ; room = 26
call update_conversation_state        ; update_conv(26, 1, 1)
mov byte [0x95c9], 1                 ; SET arrest flag
xor edx, edx                         ; load_mode = 0
mov eax, 0x1f                        ; room = 31
call load_room_and_init_alfred        ; load room 31 (jail)
cmp byte [0x95e6], 0                 ; already done first-arrest persistence?
jne 0x21783                          ; if yes, skip to exit

; --- FIRST TIME ARREST: persist NPC position to ALFRED.1 ---
mov byte [0x95e6], 1                 ; mark first-arrest done
mov eax, [0xfac8]
mov word [eax + 0x504], 0x1bc        ; room_data[0x504] = X=444
mov eax, [0xfac8]
mov word [eax + 0x506], 0xa6         ; room_data[0x506] = Y=166

; Build save record at [0xFB78]:
mov ax, [0xfb94]                     ; room ID
mov [0xfb78], ax                     ; record[0] = room_id
mov word [0xfb7a], 0x504             ; record[2] = offset 0x504
mov byte [0xfb7c], 4                 ; record[4] = type/size = 4
mov word [0xfb7d], 0x1bc             ; record[5] = X = 444
mov word [0xfb7f], 0xa6              ; record[7] = Y = 166

; Write 9-byte record to ALFRED.1
mov ecx, [0xf914]                    ; file handle
mov ebx, 1
mov edx, 9                           ; size = 9
mov eax, 0xfb78                      ; source
call write_data_to_alfred1

; Seek to room data offset + 0x504
mov eax, [0xfaac]
mov edx, [eax + 0x50]                ; room sprite data base offset
add edx, 0x504
mov eax, [0xf8f0]
xor ebx, ebx
call file_seek

; Write 4 bytes (the X,Y coords) to file
mov ecx, [0xf8f0]
mov eax, [0xfac8]
add eax, 0x504                       ; source = room_data + 0x504
mov ebx, 1
mov edx, 4                           ; size = 4
jmp 0x2177e                          ; → call write_data_to_alfred1; pop regs; ret

; --- EXIT (already arrested before) ---
21783: pop edx
       pop ecx
       pop ebx
       ret
```

**What it does:** The shared "go to jail / arrest" handler. Fades screen to black, updates conversation state for room 26 NPC 1 branch 1, sets arrest flag [0x95C9]=1, then loads room 31 (jail) with Alfred at (342, 277) facing left. On first arrest (when [0x95E6]==0), it also persists NPC sprite position (444, 166) at room_data offset 0x504 to the ALFRED.1 file, and marks [0x95E6]=1. Subsequent arrests skip the file persistence.

**State flags:**
- Write: [0xFB96] = 0x156, [0xFB98] = 0x115, [0xFB9A] = 2 (Alfred position for room 31)
- Write: [0x95C9] = 1 (arrest flag)
- Read: [0x95E6] — first-arrest persistence check
- Write: [0x95E6] = 1 (first time only)
- Write: room_data[0x504] = (0x1BC, 0xA6) = (444, 166) — NPC position
- Write: [0xFB78..0xFB80] — save record buffer
- Read: [0xFAC8] (room data ptr), [0xFAAC] (sprite data ptr), [0xF914]/[0xF8F0] (file handles), [0xFB94] (room ID)

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=26, npc=1, branch=1)`

**Items:** None

---

### ACTION 0x011E (286) @ Ghidra 0x21787

**Disassembly (0x21787 - 0x217B0):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 2             ; branch = 2
xor edx, edx           ; npc = 0
mov eax, 0x1b          ; room = 27
call update_conversation_state
mov eax, 0x53          ; item = 83 (0x53)
call process_inventory_action
pop edx
pop ebx
ret
```

**What it does:** Updates conversation state for room 27, NPC 0, branch 2, then processes inventory item 83.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=27, npc=0, branch=2)`

**Items:** process_inventory_action(83)

---

### ACTION 0x011F (287) @ Ghidra 0x217B1

**Disassembly (0x217B1 - 0x217F9):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov eax, 0x4d          ; item = 77
call process_inventory_action
mov eax, 0x6b          ; item = 107
call process_inventory_action
inc byte [0x95f4]      ; increment evidence counter
xor eax, eax
mov al, [0x95f4]
cmp eax, 4             ; all 4 evidence items collected?
jne skip
  mov ebx, 2           ; branch = 2
  mov edx, 1           ; npc = 1
  mov eax, 0x1b        ; room = 27
  call update_conversation_state
skip:
pop edx
pop ebx
ret
```

**What it does:** Processes two inventory items (77 and 107), then increments evidence counter [0x95F4]. If counter reaches 4, updates conversation state for room 27, NPC 1, branch 2.

**State flags:**
- Write: [0x95F4] += 1 (evidence counter)
- Read: [0x95F4] — check if == 4

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=27, npc=1, branch=2)` — only when [0x95F4] reaches 4

**Items:** process_inventory_action(77), process_inventory_action(107)

---

### ACTION 0x0120 (288) @ Ghidra 0x217FA

**Disassembly (0x217FA - 0x21838):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov eax, 0x4e          ; item = 78
call process_inventory_action
inc byte [0x95f4]      ; increment evidence counter
xor eax, eax
mov al, [0x95f4]
cmp eax, 4             ; all 4 collected?
jne skip
  mov ebx, 2           ; branch = 2
  mov edx, 1           ; npc = 1
  mov eax, 0x1b        ; room = 27
  call update_conversation_state
skip:
pop edx
pop ebx
ret
```

**What it does:** Processes inventory item 78, increments evidence counter [0x95F4]. If counter reaches 4, updates conversation for room 27, NPC 1, branch 2.

**State flags:**
- Write: [0x95F4] += 1 (evidence counter)

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=27, npc=1, branch=2)` — only when [0x95F4] reaches 4

**Items:** process_inventory_action(78)

---

### ACTION 0x0121 (289) @ Ghidra 0x21839

**Disassembly (0x21839 - 0x21881):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov eax, 0x4f          ; item = 79
call process_inventory_action
mov eax, 0x6c          ; item = 108
call process_inventory_action
inc byte [0x95f4]      ; increment evidence counter
xor eax, eax
mov al, [0x95f4]
cmp eax, 4
jne skip
  mov ebx, 2           ; branch = 2
  mov edx, 1           ; npc = 1
  mov eax, 0x1b        ; room = 27
  call update_conversation_state
skip:
pop edx
pop ebx
ret
```

**What it does:** Processes two inventory items (79 and 108), increments evidence counter [0x95F4]. If counter reaches 4, updates conversation for room 27, NPC 1, branch 2.

**State flags:**
- Write: [0x95F4] += 1

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=27, npc=1, branch=2)` — only when [0x95F4] reaches 4

**Items:** process_inventory_action(79), process_inventory_action(108)

---

### ACTION 0x0122 (290) @ Ghidra 0x21882

**Disassembly (0x21882 - 0x218CB):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov eax, 0x50          ; item = 80
call process_inventory_action
mov eax, 0x6d          ; item = 109
call process_inventory_action
inc byte [0x95f4]      ; increment evidence counter
xor eax, eax
mov al, [0x95f4]
cmp eax, 4
jne 0x21bc5            ; skip to pop/ret if not 4
  mov ebx, 2           ; branch = 2
  mov edx, 1           ; npc = 1
  mov eax, 0x1b        ; room = 27
  jmp 0x21bc0          ; → call update_conversation_state; pop; ret
; else: jmp to 0x21BC5 → pop edx; pop ebx; ret
```

**What it does:** Processes two inventory items (80 and 109), increments evidence counter [0x95F4]. If counter reaches 4, updates conversation for room 27, NPC 1, branch 2. This is the **last** of the 4 evidence handlers (287–290) — when all 4 have been triggered, the counter reaches 4.

**State flags:**
- Write: [0x95F4] += 1

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=27, npc=1, branch=2)` — only when [0x95F4] reaches 4

**Items:** process_inventory_action(80), process_inventory_action(109)

---

### ACTION 0x0124 (292) @ Ghidra 0x2161D

**Disassembly (0x2161D - 0x2163A):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 1             ; branch = 1
xor edx, edx           ; npc = 0
mov eax, 0x1f          ; room = 31
jmp 0x213d3            ; → call update_conversation_state; pop edx; pop ebx; ret
```

**What it does:** Advances conversation state for room 31, NPC 0, branch 1.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=31, npc=0, branch=1)`

**Items:** None

---

## Summary Table

| Action | Dec | Handler Type | Room | NPC | Branch | Notes |
|--------|-----|-------------|------|-----|--------|-------|
| 0x0113 | 275 | Conversation advance | 18 | 0 | 2 | update_conv(18,0,2) |
| 0x0114 | 276 | Conversation advance | 18 | 0 | 3 | update_conv(18,0,3) |
| 0x0115 | 277 | Conversation advance + flags | 18 | 0 | 5 | update_conv(18,0,5), set [0x95B9]=1, inc [0x95C4] |
| 0x0116 | 278 | Conversation advance | 20 | 0 | 1 | update_conv(20,0,1) |
| 0x0117 | 279 | ARREST → Room 21 | — | — | — | Remove item 75, fade, cutscene, load room 21 at (575,210), give items 17/64/24/59 |
| 0x0118 | 280 | NPC dialog | — | — | — | Dialog from [0xBACC] |
| 0x0119 | 281 | NPC dialog | — | — | — | Dialog from [0xBAD0] |
| 0x011A | 282 | NPC dialog | — | — | — | Dialog from [0xBAD4] |
| 0x011D | 285 | SHARED ARREST → Room 31 | 26 | 1 | 1 | Fade, conv(26,1,1), set [0x95C9]=1, load room 31 at (342,277). First time: persist NPC pos (444,166) at room_data+0x504 |
| 0x011E | 286 | Conversation + inventory | 27 | 0 | 2 | update_conv(27,0,2), give item 83 |
| 0x011F | 287 | Evidence collection | 27 | 1 | 2* | Items 77+107, inc counter; conv update only when counter=4 |
| 0x0120 | 288 | Evidence collection | 27 | 1 | 2* | Item 78, inc counter; conv update only when counter=4 |
| 0x0121 | 289 | Evidence collection | 27 | 1 | 2* | Items 79+108, inc counter; conv update only when counter=4 |
| 0x0122 | 290 | Evidence collection | 27 | 1 | 2* | Items 80+109, inc counter; conv update only when counter=4 |
| 0x0124 | 292 | Conversation advance | 31 | 0 | 1 | update_conv(31,0,1) |

\* Conversation update is conditional — only fires when evidence counter [0x95F4] reaches 4.

## Data Address Table (NPC Dialog Pointers)

| Address | Used by Action | Purpose |
|---------|---------------|---------|
| 0xBACC | 0x0118 (280) | NPC dialog data ptr |
| 0xBAD0 | 0x0119 (281) | NPC dialog data ptr |
| 0xBAD4 | 0x011A (282) | NPC dialog data ptr |

## Key State Flags

| Address | Type | Purpose | Used by |
|---------|------|---------|---------|
| 0x95B9 | byte | Flag (set to 1) | 277 |
| 0x95C4 | byte | Counter (incremented) | 277 |
| 0x95C9 | byte | Arrest flag (set to 1) | 285 |
| 0x95E6 | byte | First-arrest persistence flag (0→1) | 285 |
| 0x95F4 | byte | Evidence collection counter (0→4) | 287, 288, 289, 290 |
| 0x117A4 | byte | Batch inventory processing flag (temp) | 279 |

## Evidence Collection System (Actions 287–290)

Actions 287, 288, 289, 290 form a **4-piece evidence collection system** in room 27:
- Each action gives 1–2 inventory items and increments counter [0x95F4]
- When counter reaches **exactly 4** (all evidence collected), conversation state for room 27, NPC 1, branch 2 is unlocked
- Action 287: items 77 + 107
- Action 288: item 78 only
- Action 289: items 79 + 108
- Action 290: items 80 + 109

## Arrest System (Actions 279, 285)

Two distinct arrest handlers:
- **Action 279** — specific arrest: removes item 75, plays cutscene, sends Alfred to room 21 (jail) at (575, 210) with items 17/64/24/59
- **Action 285** — shared/general arrest: fades, updates room 26 conversation, sends Alfred to room 31 (different jail?) at (342, 277). Persists NPC position on first occurrence. Used by 5 different action IDs (285, 291, 352, 355, 363).

## File Offset Mapping

For reference: `file_offset = 0x14200 + (ghidra_addr - 0x10000)` (LE executable, Object 1 data pages start at 0x14200, reloc base 0x10000).
