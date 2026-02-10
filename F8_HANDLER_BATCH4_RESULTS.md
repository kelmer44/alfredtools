# F8 Action Handler Batch 4 - Decompilation Results

## New Function Names (resolved via Ghidra + disassembly)

| Address | Name | Purpose |
|---------|------|---------|
| 0x27CE1 | `play_ambient_sound` | Start ambient sound with params (stdcall, 7 params) |
| 0x25487 | `display_text_with_voice` | Display text with optional voice playback |
| 0x1BADF | `check_item_in_inventory` | Check if item (EAX) is in inventory; returns 1/0 in AH |
| 0x2A60D | `play_sound` | Sound/resource management (Ghidra name; possibly also frees buffer) |
| 0x1B723 | `setup_npc_conversation_text` | Scan conversation data, update NPC text pointer in room_data[0x3DA+idx*4] |

## Shared Code Blocks

### Shared tail at 0x21BC0 (reused from Batch 3)
```asm
21BC0: call update_conversation_state  ; EAX=room, EDX=npc, EBX=branch
21BC5: pop edx
21BC6: pop ebx
21BC7: ret
```
Used by: actions 313, 320 (via 0x21BB4)

### Shared inline at 0x21BB4 (sets branch=2 then hits 0x21BC0)
```asm
21BB4: mov ebx, 2          ; branch = 2
21BB9: xor edx, edx        ; npc = 0
21BBB: mov eax, 0x2b        ; room = 43
21BC0: call update_conversation_state
21BC5: pop edx
21BC6: pop ebx
21BC7: ret
```
Used by: action 319 (inline), action 320 (jmp 0x21BB4), action 323 (jmp 0x21BB9)

### Shared conv tail at 0x21E68
```asm
21E68: call update_conversation_state  ; EAX=room, EDX=npc, EBX=branch
21E6D: pop edx
21E6E: pop ebx
21E6F: ret
```
Used by: actions 325, 326

### Shared skip-conv return at 0x21E6D
```asm
21E6D: pop edx
21E6E: pop ebx
21E6F: ret
```
Used by: action 325 (when counter != 2)

### Shared setup_npc_text + return at 0x221F7
```asm
221E9: mov ecx, 1           ; new_val = 1 (default, overridden by caller)
221EE: mov ebx, 0x19         ; room = 25 (default, overridden by caller)
221F3: xor edx, edx
221F5: mov eax, ebx
221F7: call setup_npc_conversation_text
221FC: pop edx
221FD: pop ecx
221FE: pop ebx
221FF: ret
```
Action 308 jumps to 0x221F7 with its own ECX/EBX/EDX/EAX already set.

### Shared cleanup at 0x150ED
```asm
150ED: mov eax, esi
150EF: call play_sound       ; release/cleanup buffer in ESI
150F4: pop esi
150F5: pop edx
150F6: pop ecx
150F7: pop ebx
150F8: ret
```
Used by: action 324

---

## Handler Analysis

---

### ACTION 0x0134 (308) @ Ghidra 0x21B11

**Disassembly (0x21B11 - 0x21B2F → tail at 0x221F7):**
```asm
push 0x10
call get_current_room_number
push ebx
push ecx
push edx
mov ecx, 2              ; new_val = 2
mov ebx, 0x10           ; expected_val = 16
xor edx, edx            ; npc = 0
mov eax, 0x29           ; room = 41
jmp 0x221F7             ; → call setup_npc_conversation_text(room=41, npc=0, expected=16, new=2)
                        ; pop edx, ecx, ebx; ret
```

**Code:**
```c
get_current_room_number();
setup_npc_conversation_text(/*room=*/41, /*npc=*/0, /*expected=*/16, /*new=*/2);
```

**What it does:** Updates NPC conversation text pointer for room 41 (0x29). Scans the conversation data for NPC 0 in room 41, advancing past text sections. If the current conversation state value matches 16 (0x10), sets it to 2; otherwise increments it. Then stores the resolved text data pointer into `room_data[0x3DA + hotspot_idx * 4]`.

**State flags:** Reads/writes table at `0xFBA4 + room*4 + npc`, reads `room_data[0x47A]` (hotspot count), writes `room_data[0x3DA + idx*4]` (text pointer).

**Chains to:** `setup_npc_conversation_text` (0x1B723)

**Conversation updates:** None (indirect text pointer manipulation)

**Items:** None

---

### ACTION 0x0139 (313) @ Ghidra 0x21B34

**Disassembly (0x21B34 - 0x21B4C → tail at 0x21BC0):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 1              ; branch = 1
xor edx, edx            ; npc = 0
mov eax, 0x29           ; room = 41
jmp shared_conv_tail_21bc0  ; → call update_conversation_state; pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/41, /*npc=*/0, /*branch=*/1);
```

**What it does:** Advances conversation tree for NPC 0 in room 41 to branch 1.

**State flags:** Via `update_conversation_state` internals.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=41, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x013A (314) @ Ghidra 0x21B4E

**Disassembly (0x21B4E - 0x21B5D):**
```asm
push 4
call get_current_room_number
mov eax, 0x5d           ; item = 93
jmp process_inventory_action
```

**Code:**
```c
get_current_room_number();
process_inventory_action(93);
```

**What it does:** Gives player inventory item 93 (0x5D).

**State flags:** Via `process_inventory_action` internals.

**Chains to:** `process_inventory_action` (tail call)

**Conversation updates:** None

**Items:** Gives item 93 (0x5D)

---

### ACTION 0x013C (316) @ Ghidra 0x21B62

**Disassembly (0x21B62 - 0x21B71):**
```asm
push 4
call get_current_room_number
mov eax, 0x5e           ; item = 94
jmp process_inventory_action
```

**Code:**
```c
get_current_room_number();
process_inventory_action(94);
```

**What it does:** Gives player inventory item 94 (0x5E).

**State flags:** Via `process_inventory_action` internals.

**Chains to:** `process_inventory_action` (tail call)

**Conversation updates:** None

**Items:** Gives item 94 (0x5E)

---

### ACTION 0x013D (317) @ Ghidra 0x21B76

**Disassembly (0x21B76 - 0x21B85):**
```asm
push 4
call get_current_room_number
mov eax, 0x5f           ; item = 95
jmp process_inventory_action
```

**Code:**
```c
get_current_room_number();
process_inventory_action(95);
```

**What it does:** Gives player inventory item 95 (0x5F).

**State flags:** Via `process_inventory_action` internals.

**Chains to:** `process_inventory_action` (tail call)

**Conversation updates:** None

**Items:** Gives item 95 (0x5F)

---

### ACTION 0x013E (318) @ Ghidra 0x21B8A

**Disassembly (0x21B8A - 0x21B99):**
```asm
push 4
call get_current_room_number
mov eax, 0x60           ; item = 96
jmp process_inventory_action
```

**Code:**
```c
get_current_room_number();
process_inventory_action(96);
```

**What it does:** Gives player inventory item 96 (0x60).

**State flags:** Via `process_inventory_action` internals.

**Chains to:** `process_inventory_action` (tail call)

**Conversation updates:** None

**Items:** Gives item 96 (0x60)

---

### ACTION 0x013F (319) @ Ghidra 0x21B9E

**Disassembly (0x21B9E - 0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov eax, 0x61           ; item = 97
call process_inventory_action
mov ebx, 2              ; branch = 2
xor edx, edx            ; npc = 0
mov eax, 0x2b           ; room = 43
call update_conversation_state
pop edx
pop ebx
ret
```

**Code:**
```c
get_current_room_number();
process_inventory_action(97);
update_conversation_state(/*room=*/43, /*npc=*/0, /*branch=*/2);
```

**What it does:** Gives player inventory item 97 (0x61), then advances conversation tree for NPC 0 in room 43 to branch 2.

**State flags:** Via `process_inventory_action` and `update_conversation_state` internals.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=43, npc=0, branch=2)`

**Items:** Gives item 97 (0x61)

---

### ACTION 0x0140 (320) @ Ghidra 0x21BC8

**Disassembly (0x21BC8 - 0x21BD4 → tail at 0x21BB4):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
jmp 0x21BB4             ; → mov ebx, 2; xor edx, edx; mov eax, 0x2b
                        ;   call update_conversation_state; pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/43, /*npc=*/0, /*branch=*/2);
```

**What it does:** Advances conversation tree for NPC 0 in room 43 to branch 2. Identical effect to the second half of action 319.

**State flags:** Via `update_conversation_state` internals.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=43, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x0141 (321) @ Ghidra 0x21BD6

**Disassembly (0x21BD6 - 0x21C20):**
```asm
push 0x2c
call get_current_room_number
push ebx
push ecx
push edx
mov ebx, 1              ; branch = 1
xor edx, edx            ; npc = 0
mov eax, 0x2d           ; room = 45
call update_conversation_state
xor eax, eax
mov al, byte [0x13002]  ; sound_index = byte at 0x13002
push eax                ; param_7 = sound_index
mov edx, dword [0x13234]; param_2 (sound channel struct?)
push edx
push 0x20               ; param_3 = 32 (frequency multiplier?)
push 0x100              ; param_4 = 256 (volume left?)
push 0x100              ; param_5 = 256 (volume right?)
push -1                 ; param_6 = -1 (loop forever?)
mov ebx, dword [0x13204]; param_1 (sound buffer struct)
push ebx
call play_ambient_sound
pop edx
pop ecx
pop ebx
ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/45, /*npc=*/0, /*branch=*/1);
play_ambient_sound(
    /*buffer=*/mem[0x13204],
    /*channel=*/mem[0x13234],
    /*freq=*/32,
    /*vol_left=*/256,
    /*vol_right=*/256,
    /*loop=*/-1,
    /*index=*/mem[0x13002]
);
```

**What it does:** Advances conversation tree for NPC 0 in room 45 to branch 1, then starts a looping ambient sound using sound system parameters from memory.

**State flags:** Reads `[0x13002]` (sound index byte), `[0x13234]` (sound channel), `[0x13204]` (sound buffer). Via `update_conversation_state` internals.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=45, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x0142 (322) @ Ghidra 0x21C21

**Disassembly (0x21C21 - 0x21C32):**
```asm
push 8
call get_current_room_number
push edx
mov edx, dword [0xBB28] ; text_data_ptr = dword at 0xBB28
jmp shared_dialog_handler ; → 0x11E1D (display NPC dialog with EAX=1)
```

**Code:**
```c
get_current_room_number();
edx = mem[0xBB28];  // text data pointer
shared_dialog_handler(edx, /*mode=*/1);  // display NPC dialog
```

**What it does:** Displays NPC dialog text. Loads a text data pointer from `[0xBB28]` and jumps to the shared dialog handler at 0x11E1D, which renders the NPC talking animation with the text.

**State flags:** Reads `[0xBB28]` (text data pointer for dialog).

**Chains to:** `shared_dialog_handler` (0x11E1D) — tail call

**Conversation updates:** None

**Items:** None

---

### ACTION 0x0143 (323) @ Ghidra 0x21C37

**Disassembly (0x21C37 - 0x21C59 → tail at 0x21BB9):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 1              ; branch = 1
xor edx, edx            ; npc = 0
mov eax, 0x2f           ; room = 47
call update_conversation_state  ; update(room=47, npc=0, branch=1)
mov ebx, 3              ; branch = 3
jmp 0x21BB9             ; → xor edx, edx; mov eax, 0x2b (43)
                        ;   call update_conversation_state(room=43, npc=0, branch=3)
                        ;   pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/47, /*npc=*/0, /*branch=*/1);
update_conversation_state(/*room=*/43, /*npc=*/0, /*branch=*/3);
```

**What it does:** Updates two conversation trees: sets NPC 0 in room 47 to branch 1, and NPC 0 in room 43 to branch 3.

**State flags:** Via `update_conversation_state` internals.

**Chains to:** None

**Conversation updates:**
- `update_conversation_state(room=47, npc=0, branch=1)`
- `update_conversation_state(room=43, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x0144 (324) @ Ghidra 0x21C5E

**Disassembly (0x21C5E - 0x21D17 → tail at 0x150ED):**
```asm
push 0x14
call get_current_room_number
push ebx
push ecx
push edx
push esi
; --- conversation update ---
mov ebx, 2              ; branch = 2
xor edx, edx            ; npc = 0
mov eax, 0x2b           ; room = 43
call update_conversation_state
; --- allocate temp buffer ---
mov eax, 0x68           ; size = 104 bytes
call allocate_memory
mov esi, eax            ; esi = buffer_ptr
; --- read room data from file ---
mov eax, dword [0xF8F0] ; file_handle
xor ebx, ebx            ; whence = SEEK_SET
mov edx, 0x1318          ; offset = 0x1318
call file_seek
mov ecx, dword [0xF8F0]
mov ebx, 1
mov edx, 0x68           ; read 104 bytes
mov eax, esi
call file_read
; --- build save record ---
mov word [0xFB70], 0x2F  ; room_id = 47
mov word [0xFB72], 0x4A9 ; data_offset = 0x4A9
mov byte [0xFB74], 1     ; type/flags = 1
mov byte [0xFB75], 8     ; value = 8
; --- write save record to ALFRED.1 ---
mov ecx, dword [0xF914]  ; write file handle
mov ebx, 1
mov edx, 6               ; size = 6 bytes
mov eax, 0xFB70           ; src = save record
call write_data_to_alfred1
; --- write value at computed offset ---
mov edx, dword [esi + 0x50] ; dynamic offset from loaded data
add edx, 0x4A9
mov eax, dword [0xF8F0]  ; file_handle
xor ebx, ebx
call file_seek
mov ecx, dword [0xF8F0]
mov ebx, 1
mov edx, 1               ; write 1 byte
mov eax, 0xFB75           ; src = byte value 8
call write_data_to_alfred1
; --- cleanup ---
jmp 0x150ED              ; → mov eax, esi; call play_sound(esi); pop esi,edx,ecx,ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/43, /*npc=*/0, /*branch=*/2);

// Load 104 bytes of data from file at offset 0x1318
byte *buf = allocate_memory(0x68);
file_seek(file_handles[0xF8F0], 0x1318, SEEK_SET);
file_read(file_handles[0xF8F0], buf, 0x68);

// Build and write save record: room 47, offset 0x4A9, value 8
save_record = {room=47, offset=0x4A9, type=1, value=8};
write_data_to_alfred1(file_handles[0xF914], &save_record, 6);

// Write byte value 8 at dynamic offset (buf[0x50] + 0x4A9) in room data
uint32_t dyn_offset = *(uint32_t*)(buf + 0x50) + 0x4A9;
file_seek(file_handles[0xF8F0], dyn_offset, SEEK_SET);
write_data_to_alfred1(file_handles[0xF8F0], &value_8, 1);

cleanup(buf);  // free/release buffer
```

**What it does:** Complex handler that updates conversation state for room 43, then modifies persistent room data in ALFRED.1. Reads 104 bytes of reference data from file offset 0x1318, builds a save record targeting room 47's data at offset 0x4A9, writes value 8 there. Also writes byte 8 at a dynamic offset computed from the loaded data. This likely changes a room object state (e.g., unlocking/enabling something in room 47).

**State flags:** Reads `[0xF8F0]` (file handle), `[0xF914]` (write file handle). Writes to `[0xFB70-0xFB75]` (save record buffer). Modifies ALFRED.1 room data at offset 0x4A9 in room 47.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=43, npc=0, branch=2)`

**Items:** None (but modifies persistent room state in ALFRED.1)

---

### ACTION 0x0145 (325) @ Ghidra 0x21D1C

**Disassembly (0x21D1C - 0x21D4A → tails at 0x21E68 / 0x21E6D):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
inc byte [0x95D8]       ; counter++
xor eax, eax
mov al, byte [0x95D8]   ; eax = counter
cmp eax, 2
jne 0x21E6D             ; if counter != 2: pop edx, ebx; ret (no-op)
; counter == 2:
mov ebx, 1              ; branch = 1
xor edx, edx            ; npc = 0
mov eax, 0x31           ; room = 49
jmp 0x21E68             ; → call update_conversation_state(49, 0, 1); pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
mem[0x95D8]++;
if (mem[0x95D8] == 2) {
    update_conversation_state(/*room=*/49, /*npc=*/0, /*branch=*/1);
}
```

**What it does:** Increments a counter at `[0x95D8]`. Only on the second trigger (counter reaches 2) does it update the conversation tree for NPC 0 in room 49 to branch 1. On all other triggers, does nothing. This is a "do something only on Nth interaction" pattern.

**State flags:** Reads/writes `[0x95D8]` (interaction counter).

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=49, npc=0, branch=1)` — only when counter == 2

**Items:** None

---

### ACTION 0x0146 (326) @ Ghidra 0x21D4F

**Disassembly (0x21D4F - 0x21D60 → shared at 0x21D43 → 0x21E68):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 2              ; branch = 2
jmp 0x21D43             ; → xor edx, edx; mov eax, 0x31 (49)
                        ;   jmp 0x21E68 → call update_conversation_state; pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/49, /*npc=*/0, /*branch=*/2);
```

**What it does:** Advances conversation tree for NPC 0 in room 49 to branch 2. Shares code with action 325.

**State flags:** Via `update_conversation_state` internals.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=49, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x0147 (327) @ Ghidra 0x21D62

**Disassembly (0x21D62 - 0x21D73):**
```asm
push 4
call get_current_room_number
mov byte [0x95E5], 1    ; set flag
ret
```

**Code:**
```c
get_current_room_number();
mem[0x95E5] = 1;
```

**What it does:** Sets a boolean state flag at `[0x95E5]` to 1 (true). This is a simple flag-setter, likely marking that a specific game event has occurred.

**State flags:** Writes `[0x95E5]` = 1.

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

## Summary Table

| Action | Hex | Address | Type | Key Operation |
|--------|-----|---------|------|---------------|
| 308 | 0x0134 | 0x21B11 | NPC text | `setup_npc_conversation_text(room=41, npc=0, expected=16, new=2)` |
| 313 | 0x0139 | 0x21B34 | Conversation | `update_conversation_state(room=41, npc=0, branch=1)` |
| 314 | 0x013A | 0x21B4E | Inventory | Give item 93 (0x5D) |
| 316 | 0x013C | 0x21B62 | Inventory | Give item 94 (0x5E) |
| 317 | 0x013D | 0x21B76 | Inventory | Give item 95 (0x5F) |
| 318 | 0x013E | 0x21B8A | Inventory | Give item 96 (0x60) |
| 319 | 0x013F | 0x21B9E | Inventory + Conv | Give item 97 (0x61) + `update_conv(room=43, npc=0, branch=2)` |
| 320 | 0x0140 | 0x21BC8 | Conversation | `update_conversation_state(room=43, npc=0, branch=2)` |
| 321 | 0x0141 | 0x21BD6 | Conv + Sound | `update_conv(room=45, npc=0, branch=1)` + start ambient sound |
| 322 | 0x0142 | 0x21C21 | Dialog | Display NPC dialog from text ptr at `[0xBB28]` |
| 323 | 0x0143 | 0x21C37 | Conversation ×2 | `update_conv(room=47, npc=0, branch=1)` + `update_conv(room=43, npc=0, branch=3)` |
| 324 | 0x0144 | 0x21C5E | Conv + Persist | `update_conv(room=43, npc=0, branch=2)` + write room 47 state to ALFRED.1 |
| 325 | 0x0145 | 0x21D1C | Counter + Conv | Increment `[0x95D8]`; if ==2: `update_conv(room=49, npc=0, branch=1)` |
| 326 | 0x0146 | 0x21D4F | Conversation | `update_conversation_state(room=49, npc=0, branch=2)` |
| 327 | 0x0147 | 0x21D62 | Flag set | Set `[0x95E5]` = 1 |

## State Flag Memory Map (this batch)

| Address | Type | Used By | Purpose |
|---------|------|---------|---------|
| 0x95D8 | byte | Action 325 | Interaction counter (triggers conv at ==2) |
| 0x95E5 | byte | Action 327 | Boolean event flag |
| 0xBB28 | dword ptr | Action 322 | NPC dialog text data pointer |
| 0xFBA4 + room*4+npc | byte table | Action 308 | Conversation text state values per room/npc |
| 0xFB70-0xFB75 | struct | Action 324 | Save record buffer (room, offset, type, value) |
| 0x13002 | byte | Action 321 | Sound index for ambient sound |
| 0x13204 | dword | Action 321 | Sound buffer struct pointer |
| 0x13234 | dword | Action 321 | Sound channel struct pointer |

## Room Cross-Reference

| Room | Dec | Actions Affecting It |
|------|-----|---------------------|
| 0x29 (41) | 41 | 308 (NPC text), 313 (conv branch 1) |
| 0x2B (43) | 43 | 319 (conv branch 2), 320 (conv branch 2), 323 (conv branch 3), 324 (conv branch 2) |
| 0x2D (45) | 45 | 321 (conv branch 1) |
| 0x2F (47) | 47 | 323 (conv branch 1), 324 (ALFRED.1 state write) |
| 0x31 (49) | 49 | 325 (conv branch 1, conditional), 326 (conv branch 2) |
