# F8 Action Handler Batch 3 - Decompilation Results

## New Function Names (resolved via Ghidra + disassembly)

| Address | Name | Purpose |
|---------|------|---------|
| 0x18DCE | `check_sprite_hover_and_trigger_conversation` | Iterates room sprites, checks mouse hover/click, triggers conversation tree |

## Shared Code Blocks

### Shared tail at 0x20446 (used by action 293)
```asm
20446: call update_conversation_state  ; EAX=room, EDX=npc, EBX=branch
2044B: pop edx
2044C: pop ecx
2044D: pop ebx
2044E: ret
```

### Shared tail at 0x21BC0 (used by actions 296, 300, 301–306)
```asm
21BC0: call update_conversation_state  ; EAX=room, EDX=npc, EBX=branch
21BC5: pop edx
21BC6: pop ebx
21BC7: ret
```

### Shared code at 0x21A0C (used by actions 300–306)
```asm
21A0C: xor edx, edx          ; npc = 0
21A0E: mov eax, 0x19          ; room = 25
21A13: jmp 0x21BC0            ; → call update_conversation_state; pop edx; pop ebx; ret
```
All actions 300–306 set EBX (branch) then jump here, resulting in `update_conversation_state(room=25, npc=0, branch=EBX)`.

### Shared tail at 0x217A9 (used by action 295)
```asm
217A9: call process_inventory_action   ; EAX = item
217AE: pop edx
217AF: pop ebx
217B0: ret
```

### Shared persist-and-return tail at 0x21777 (used by actions 297, 307)
```asm
21777: mov ebx, 1             ; flag = 1
2177C: mov edx, ebx           ; size = 1
2177E: call write_data_to_alfred1     ; write 1 byte from EAX
21783: pop edx
21784: pop ecx
21785: pop ebx
21786: ret
```

---

## Handler Analysis

---

### ACTION 0x0125 (293) @ Ghidra 0x2163A

**Disassembly (0x2163A - 0x216F0):**
```asm
push 0x10
call get_current_room_number
push ebx
push ecx
push edx
mov eax, [0xFAC8]                    ; room_data_ptr
mov word [eax + 0x4C5], 0x280        ; room_data[0x4C5] = X = 640
mov eax, [0xFAC8]
mov word [eax + 0x4C7], 0x190        ; room_data[0x4C7] = Y = 400

; Build save record at [0xFB78]:
mov ax, [0xFB94]                     ; current room ID
mov [0xFB78], ax                     ; record[0] = room_id
mov word [0xFB7A], 0x4C5             ; record[2] = offset 0x4C5
mov byte [0xFB7C], 4                 ; record[4] = type/size = 4
mov word [0xFB7D], 0x280             ; record[5] = X = 640
mov word [0xFB7F], 0x190             ; record[7] = Y = 400

; Write 9-byte record to ALFRED.1
mov ecx, [0xF914]                    ; file handle
mov ebx, 1
mov edx, 9
mov eax, 0xFB78
call write_data_to_alfred1

; Seek to room data offset + 0x4C5
mov eax, [0xFAAC]
mov edx, [eax + 0x50]
add edx, 0x4C5
mov eax, [0xF8F0]
xor ebx, ebx
call file_seek

; Write 4 bytes (X,Y coords) to ALFRED.1
mov ecx, [0xF8F0]
mov eax, [0xFAC8]
add eax, 0x4C5
mov ebx, 1
mov edx, 4
call write_data_to_alfred1

; Update conversation state
mov ebx, 2             ; branch = 2
xor edx, edx           ; npc = 0
mov eax, 0x1F          ; room = 31
jmp shared_conv_tail_20446            ; → call update_conversation_state; pop edx/ecx/ebx; ret
```

**What it does:** Persists NPC/sprite position (640, 400) at room_data offset 0x4C5 to ALFRED.1, then advances conversation state for room 31, NPC 0, branch 2. This is a room data persistence handler — writes a 4-byte X/Y coordinate pair to the save file. Similar pattern to the first-arrest persistence in action 285.

**State flags:**
- Write: room_data[0x4C5] = 0x280 (640), room_data[0x4C7] = 0x190 (400)
- Write: [0xFB78..0xFB80] — save record buffer
- Read: [0xFAC8] (room data ptr), [0xFAAC] (sprite data ptr), [0xF914]/[0xF8F0] (file handles), [0xFB94] (room ID)

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=31, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x0126 (294) @ Ghidra 0x216F5

**Disassembly (0x216F5 - 0x21786):**
```asm
push 0x10
call get_current_room_number
push ebx
push ecx
push edx
mov edx, [0xFAC8]                    ; room_data_ptr
mov byte [edx + 0x527], 1            ; room_data[0x527] = 1 (set flag)

; Build save record at [0xFB70]:
mov ax, [0xFB94]                     ; current room ID
mov [0xFB70], ax                     ; record[0] = room_id
mov word [0xFB72], 0x527             ; record[2] = offset 0x527
mov ah, 1
mov [0xFB74], ah                     ; record[4] = 1
mov [0xFB75], ah                     ; record[5] = 1

; Write 6-byte record to ALFRED.1
mov ecx, [0xF914]
mov ebx, 1
mov edx, 6
mov eax, 0xFB70
call write_data_to_alfred1

; Seek to room data offset + 0x527
mov edx, [0xFAAC]
mov edx, [edx + 0x50]
add edx, 0x527
mov eax, [0xF8F0]
xor ebx, ebx
call file_seek

; Write 1 byte to ALFRED.1
mov ecx, [0xF8F0]
mov eax, [0xFAC8]
add eax, 0x527
mov ebx, 1
mov edx, ebx            ; size = 1
call write_data_to_alfred1
pop edx
pop ecx
pop ebx
ret
```

**What it does:** Sets a byte flag at room_data offset 0x527 to 1, then persists it to ALFRED.1. Uses a 6-byte save record format (room_id, offset, type, value). No conversation update — purely a state persistence handler.

**State flags:**
- Write: room_data[0x527] = 1
- Write: [0xFB70..0xFB76] — save record buffer
- Read: [0xFAC8] (room data ptr), [0xFAAC], [0xF914], [0xF8F0], [0xFB94]

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

### ACTION 0x0127 (295) @ Ghidra 0x218CC

**Disassembly (0x218CC - 0x218F2):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 3             ; branch = 3
xor edx, edx           ; npc = 0
mov eax, 0x1A          ; room = 26
call update_conversation_state
mov eax, 0x54          ; item = 84
jmp 0x217A9            ; → call process_inventory_action; pop edx; pop ebx; ret
```

**What it does:** Updates conversation state for room 26, NPC 0, branch 3, then processes inventory item 84 (0x54).

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=26, npc=0, branch=3)`

**Items:** process_inventory_action(84)

---

### ACTION 0x0128 (296) @ Ghidra 0x218F3

**Disassembly (0x218F3 - 0x2190B):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 1             ; branch = 1
mov edx, ebx           ; npc = 1
mov eax, 0x16          ; room = 22
jmp shared_conv_tail_21bc0  ; → call update_conversation_state; pop edx; pop ebx; ret
```

**What it does:** Advances conversation state for room 22, NPC 1, branch 1.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=1, branch=1)`

**Items:** None

---

### ACTION 0x0129 (297) @ Ghidra 0x21910

**Disassembly (0x21910 - 0x219A3):**
```asm
push 0x10
call get_current_room_number
push ebx
push ecx
push edx
mov ebx, 2             ; branch = 2
xor edx, edx           ; npc = 0
mov eax, 0x22          ; room = 34
call update_conversation_state

; Set room_data flag
mov edx, [0xFAC8]                    ; room_data_ptr
mov byte [edx + 0x1C1], 1            ; room_data[0x1C1] = 1

; Build save record at [0xFB70]:
mov ax, [0xFB94]                     ; current room ID
mov [0xFB70], ax
mov word [0xFB72], 0x1C1             ; offset 0x1C1
mov ah, 1
mov [0xFB74], ah                     ; = 1
mov [0xFB75], ah                     ; = 1

; Write 6-byte record to ALFRED.1
mov ecx, [0xF914]
mov ebx, 1
mov edx, 6
mov eax, 0xFB70
call write_data_to_alfred1

; Seek to room data offset + 0x1C1
mov edx, [0xFAAC]
mov edx, [edx + 0x50]
add edx, 0x1C1
mov eax, [0xF8F0]
xor ebx, ebx
call file_seek

; Write 1 byte to ALFRED.1 (via shared tail at 0x21777)
mov ecx, [0xF8F0]
mov eax, [0xFAC8]
add eax, 0x1C1
jmp 0x21777            ; → mov ebx,1; mov edx,ebx; call write_data_to_alfred1; pop edx/ecx/ebx; ret
```

**What it does:** Updates conversation state for room 34, NPC 0, branch 2, then sets byte flag at room_data offset 0x1C1 to 1 and persists it to ALFRED.1.

**State flags:**
- Write: room_data[0x1C1] = 1
- Write: [0xFB70..0xFB76] — save record buffer
- Read: [0xFAC8], [0xFAAC], [0xF914], [0xF8F0], [0xFB94]

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=34, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x012A (298) @ Ghidra 0x219A8

**Disassembly (0x219A8 - 0x219D3):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 3             ; branch = 3
xor edx, edx           ; npc = 0
mov eax, 0x19          ; room = 25
call update_conversation_state
xor edx, edx           ; param2 = 0
mov eax, 2             ; param1 = 2
call check_sprite_hover_and_trigger_conversation
pop edx
pop ebx
ret
```

**What it does:** Updates conversation state for room 25, NPC 0, branch 3, then calls `check_sprite_hover_and_trigger_conversation(2, 0)` — triggers a conversation/interaction with sprite index 2 in the current room.

**State flags:** None directly (conversation state modified by callee)

**Chains to:** `check_sprite_hover_and_trigger_conversation(2, 0)` at 0x18DCE

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x012B (299) @ Ghidra 0x219D4

**Disassembly (0x219D4 - 0x219FA):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 1             ; branch = 1
xor edx, edx           ; npc = 0
mov eax, 0x19          ; room = 25
call update_conversation_state
mov byte [0x95D0], 1   ; SET flag
pop edx
pop ebx
ret
```

**What it does:** Updates conversation state for room 25, NPC 0, branch 1, then sets global flag [0x95D0] to 1.

**State flags:**
- Write: [0x95D0] = 1

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x012C (300) @ Ghidra 0x219FB

**Disassembly (0x219FB - 0x21A13→0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 5             ; branch = 5
; falls through to shared code at 0x21A0C:
xor edx, edx           ; npc = 0
mov eax, 0x19          ; room = 25
jmp shared_conv_tail_21bc0  ; → call update_conversation_state; pop; ret
```

**What it does:** Advances conversation state for room 25, NPC 0, branch 5.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=5)`

**Items:** None

---

### ACTION 0x012D (301) @ Ghidra 0x21A18

**Disassembly (0x21A18 - 0x21A29→0x21A0C→0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 6             ; branch = 6
jmp 0x21A0C            ; → xor edx,edx; mov eax,0x19; jmp shared_conv_tail_21bc0
```

**What it does:** Advances conversation state for room 25, NPC 0, branch 6.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=6)`

**Items:** None

---

### ACTION 0x012E (302) @ Ghidra 0x21A2B

**Disassembly (0x21A2B - 0x21A3C→0x21A0C→0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 7             ; branch = 7
jmp 0x21A0C            ; → xor edx,edx; mov eax,0x19; jmp shared_conv_tail_21bc0
```

**What it does:** Advances conversation state for room 25, NPC 0, branch 7.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=7)`

**Items:** None

---

### ACTION 0x012F (303) @ Ghidra 0x21A3E

**Disassembly (0x21A3E - 0x21A4F→0x21A0C→0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 8             ; branch = 8
jmp 0x21A0C            ; → xor edx,edx; mov eax,0x19; jmp shared_conv_tail_21bc0
```

**What it does:** Advances conversation state for room 25, NPC 0, branch 8.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=8)`

**Items:** None

---

### ACTION 0x0130 (304) @ Ghidra 0x21A51

**Disassembly (0x21A51 - 0x21A62→0x21A0C→0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 9             ; branch = 9
jmp 0x21A0C            ; → xor edx,edx; mov eax,0x19; jmp shared_conv_tail_21bc0
```

**What it does:** Advances conversation state for room 25, NPC 0, branch 9.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=9)`

**Items:** None

---

### ACTION 0x0131 (305) @ Ghidra 0x21A64

**Disassembly (0x21A64 - 0x21A75→0x21A0C→0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 0xA           ; branch = 10
jmp 0x21A0C            ; → xor edx,edx; mov eax,0x19; jmp shared_conv_tail_21bc0
```

**What it does:** Advances conversation state for room 25, NPC 0, branch 10.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=10)`

**Items:** None

---

### ACTION 0x0132 (306) @ Ghidra 0x21A77

**Disassembly (0x21A77 - 0x21A88→0x21A0C→0x21BC7):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 3             ; branch = 3
jmp 0x21A0C            ; → xor edx,edx; mov eax,0x19; jmp shared_conv_tail_21bc0
```

**What it does:** Advances conversation state for room 25, NPC 0, branch 3.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=25, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x0133 (307) @ Ghidra 0x21A8A

**Disassembly (0x21A8A - 0x21B0C→0x21777→0x21786):**
```asm
push 0x10
call get_current_room_number
push ebx
push ecx
push edx
mov edx, [0xFAC8]                    ; room_data_ptr
mov byte [edx + 0x47C], 8            ; room_data[0x47C] = 8

; Build save record at [0xFB70]:
mov ax, [0xFB94]                     ; current room ID
mov [0xFB70], ax
mov word [0xFB72], 0x47C             ; offset 0x47C
mov ah, 1
mov [0xFB74], ah                     ; = 1
mov [0xFB75], ah                     ; = 1

; Write 6-byte record to ALFRED.1
mov ecx, [0xF914]
mov ebx, 1
mov edx, 6
mov eax, 0xFB70
call write_data_to_alfred1

; Seek to room data offset + 0x47C
mov edx, [0xFAAC]
mov edx, [edx + 0x50]
add edx, 0x47C
mov eax, [0xF8F0]
xor ebx, ebx
call file_seek

; Write 1 byte to ALFRED.1 (via shared tail at 0x21777)
mov ecx, [0xF8F0]
mov eax, [0xFAC8]
add eax, 0x47C
jmp 0x21777            ; → mov ebx,1; mov edx,1; call write_data_to_alfred1; pop edx/ecx/ebx; ret
```

**What it does:** Sets byte at room_data offset 0x47C to 8 (note: 0x47C is the hotspot count field!) and persists it to ALFRED.1. No conversation update. This likely modifies the room's hotspot count — setting it to 8 could enable or expose hotspots in the room.

**State flags:**
- Write: room_data[0x47C] = 8
- Write: [0xFB70..0xFB76] — save record buffer
- Read: [0xFAC8], [0xFAAC], [0xF914], [0xF8F0], [0xFB94]

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

## Summary Table

| Action | Dec | Handler Type | Room | NPC | Branch | Notes |
|--------|-----|-------------|------|-----|--------|-------|
| 0x0125 | 293 | Persist + conversation | 31 | 0 | 2 | Persist position (640,400) at room_data+0x4C5, update_conv(31,0,2) |
| 0x0126 | 294 | Persist flag | — | — | — | Set room_data[0x527]=1, persist to ALFRED.1 |
| 0x0127 | 295 | Conversation + inventory | 26 | 0 | 3 | update_conv(26,0,3), give item 84 |
| 0x0128 | 296 | Conversation advance | 22 | 1 | 1 | update_conv(22,1,1) |
| 0x0129 | 297 | Conversation + persist | 34 | 0 | 2 | update_conv(34,0,2), set room_data[0x1C1]=1, persist |
| 0x012A | 298 | Conversation + sprite trigger | 25 | 0 | 3 | update_conv(25,0,3), trigger sprite conv(2,0) |
| 0x012B | 299 | Conversation + flag | 25 | 0 | 1 | update_conv(25,0,1), set [0x95D0]=1 |
| 0x012C | 300 | Conversation advance | 25 | 0 | 5 | update_conv(25,0,5) |
| 0x012D | 301 | Conversation advance | 25 | 0 | 6 | update_conv(25,0,6) |
| 0x012E | 302 | Conversation advance | 25 | 0 | 7 | update_conv(25,0,7) |
| 0x012F | 303 | Conversation advance | 25 | 0 | 8 | update_conv(25,0,8) |
| 0x0130 | 304 | Conversation advance | 25 | 0 | 9 | update_conv(25,0,9) |
| 0x0131 | 305 | Conversation advance | 25 | 0 | 10 | update_conv(25,0,10) |
| 0x0132 | 306 | Conversation advance | 25 | 0 | 3 | update_conv(25,0,3) — same as 298's conv params |
| 0x0133 | 307 | Persist room data | — | — | — | Set room_data[0x47C]=8, persist to ALFRED.1 |

## Room 25 Conversation Branch Progression (Actions 298–306)

Actions 298–306 all operate on **room 25, NPC 0** with varying branch numbers. This appears to be a multi-step conversation/quest progression system:

| Action | Branch | Extra behavior |
|--------|--------|---------------|
| 298 | 3 | + triggers sprite conversation(2,0) |
| 299 | 1 | + sets flag [0x95D0]=1 |
| 300 | 5 | pure conversation advance |
| 301 | 6 | pure conversation advance |
| 302 | 7 | pure conversation advance |
| 303 | 8 | pure conversation advance |
| 304 | 9 | pure conversation advance |
| 305 | 10 | pure conversation advance |
| 306 | 3 | pure conversation advance (same branch as 298) |

Actions 300–305 are highly repetitive — they differ only in the branch number. They share code at 0x21A0C with just different EBX values.

## Data Persistence Handlers (Actions 293, 294, 297, 307)

Four handlers in this batch persist data to ALFRED.1 using a common pattern:

| Action | Offset | Data | Record Size | Purpose |
|--------|--------|------|-------------|---------|
| 293 | 0x4C5 | word 0x280, word 0x190 | 9 bytes (4-byte persist) | NPC position (640, 400) |
| 294 | 0x527 | byte 1 | 6 bytes (1-byte persist) | Flag set to 1 |
| 297 | 0x1C1 | byte 1 | 6 bytes (1-byte persist) | Flag set to 1 |
| 307 | 0x47C | byte 8 | 6 bytes (1-byte persist) | Hotspot count = 8 |

### Persistence Record Format

**9-byte record** (for word data, used by 293):
```
[0..1] room_id (word)
[2..3] offset (word)
[4]    type/size = 4
[5..6] value_lo (word)
[7..8] value_hi (word)
```
Written to buffer at [0xFB78].

**6-byte record** (for byte data, used by 294, 297, 307):
```
[0..1] room_id (word)
[2..3] offset (word)
[4]    type = 1
[5]    value (byte)
```
Written to buffer at [0xFB70].

## Key State Flags

| Address | Type | Purpose | Used by |
|---------|------|---------|---------|
| 0x95D0 | byte | Flag (set to 1) | 299 |

## Room Data Offsets Modified

| Room Data Offset | Value | Purpose | Action |
|-----------------|-------|---------|--------|
| 0x4C5 (word) | 0x280 (640) | NPC X position | 293 |
| 0x4C7 (word) | 0x190 (400) | NPC Y position | 293 |
| 0x527 (byte) | 1 | State flag | 294 |
| 0x1C1 (byte) | 1 | State flag | 297 |
| 0x47C (byte) | 8 | Hotspot count | 307 |

## File Offset Mapping

For reference: `file_offset = 0x14200 + (ghidra_addr - 0x10000)` (LE executable, Object 1 data pages start at 0x14200, reloc base 0x10000).
