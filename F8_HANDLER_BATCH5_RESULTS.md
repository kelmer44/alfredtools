# F8 Action Handler Batch 5 - Decompilation Results

## New Function Names (resolved via Ghidra + disassembly)

| Address | Name | Purpose |
|---------|------|---------|
| 0x2A218 | `get_current_room_number` | Returns current room number (confirmed via Ghidra) |
| 0x1B666 | `update_conversation_state` | Write branch to conv state table, update NPC text pointer |
| 0x24157 | `process_inventory_action` | Give player an inventory item (EAX = item ID) |
| 0x25487 | `display_text_with_voice` | Display text with optional voice playback (EAX = text ptr) |
| 0x1BADF | `check_item_in_inventory` | Check if item (EAX) is in inventory; returns 1/0 in AL |

### Note on `update_conversation_state` Address
The user-provided address 0x2BA42 is **NOT** `update_conversation_state` — it is part of a sprite/animation command processor (`FUN_0002b9fe`). The real `update_conversation_state` confirmed in Ghidra is at **0x1B666**. It:
1. Writes `branch` (EBX) to `DAT_0004FBA4[npc + room*4]`
2. If room == current_room, scans conversation text data to resolve the NPC's text pointer
3. Stores the resolved pointer into `room_sprite_data_ptr[0x3DA + hotspot_idx*4]`

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
Used by: actions 337 (inline), 338, 339, 340, 341, 342 (jmp 0x21E61)

### Shared conv entry at 0x21E68 (call only, reuses caller's regs)
```asm
21E68: call     update_conversation_state
21E6D: pop      edx
21E6E: pop      ebx
21E6F: ret
```
Used by: action 328 (jmp 0x21E68, with eax=2, edx=0, ebx=1)

### Shared inventory + cleanup at 0x217A9
```asm
217A9: call     process_inventory_action  ; EAX = item ID
217AE: pop      edx
217AF: pop      ebx
217B0: ret
```
Used by: action 334 (jmp 0x217A9, with eax=0x4C)

---

## Handler Analysis

---

### ACTION 0x0148 (328) @ Ghidra 0x21D74

**Disassembly (0x21D74 → tail at 0x21E68):**
```asm
21D74: push     0xc
21D79: call     get_current_room_number
21D7E: push     ebx
21D7F: push     edx
21D80: mov      ebx, 1           ; branch = 1
21D85: xor      edx, edx         ; npc = 0
21D87: mov      eax, 2           ; room = 2
21D8C: jmp      0x21E68          ; → call update_conversation_state; pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/2, /*npc=*/0, /*branch=*/1);
```

**What it does:** Advances conversation tree for NPC 0 in room 2 to branch 1.

**State flags:** Writes `[0x4FBA4 + 2*4 + 0]` = 1 (conversation state for room 2, NPC 0).

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=2, npc=0, branch=1)`

**Items:** None

---

### ACTION 0x0149 (329) @ Ghidra 0x21D91

**Disassembly (0x21D91 - 0x21DA2):**
```asm
21D91: push     4
21D96: call     get_current_room_number
21D9B: mov      byte ptr [0x95E8], 1
21DA2: ret
```

**Code:**
```c
get_current_room_number();
*(byte*)0x95E8 = 1;
```

**What it does:** Sets the game state flag byte at `0x95E8` to 1. This is a runtime-only BSS variable (not in EXE file). Likely a one-shot event flag.

**State flags:** Writes `[0x95E8]` = 1.

**Chains to:** None

**Conversation updates:** None

**Items:** None

---

### ACTION 0x014A (330) @ Ghidra 0x21DA3

**Disassembly (0x21DA3 - 0x21DB6):**
```asm
21DA3: push     4
21DA8: call     get_current_room_number
21DAD: mov      eax, 0x66         ; item = 102
21DB2: jmp      process_inventory_action
```

**Code:**
```c
get_current_room_number();
process_inventory_action(102);
```

**What it does:** Gives player inventory item 102 (0x66).

**State flags:** Via `process_inventory_action` internals.

**Chains to:** `process_inventory_action` (tail call)

**Conversation updates:** None

**Items:** Gives item 102 (0x66)

---

### ACTION 0x014B (331) @ Ghidra 0x21DB7

**Disassembly (0x21DB7 - 0x21DCA):**
```asm
21DB7: push     4
21DBC: call     get_current_room_number
21DC1: mov      eax, dword ptr [0xBB74]
21DC6: jmp      display_text_with_voice
```

**Code:**
```c
get_current_room_number();
display_text_with_voice(*(uint32_t*)0xBB74);
```

**What it does:** Displays text/voice using a runtime text data pointer stored at `[0xBB74]`. This pointer is likely set during room/conversation initialization — it points to NPC dialog text for the current context.

**State flags:** Reads `[0xBB74]` (text data pointer, BSS).

**Chains to:** `display_text_with_voice` (tail call)

**Conversation updates:** None

**Items:** None

---

### ACTION 0x014C (332) @ Ghidra 0x21DCB

**Disassembly (0x21DCB - 0x21DEC):**
```asm
21DCB: push     4
21DD0: call     get_current_room_number
21DD5: mov      eax, 0x68         ; item = 104
21DDA: call     check_item_in_inventory
21DDF: test     al, al
21DE1: jne      0x21DA2           ; if already has item → ret (skip)
21DE3: mov      eax, 0x68         ; item = 104
21DE8: jmp      process_inventory_action
```

**Code:**
```c
get_current_room_number();
if (!check_item_in_inventory(104)) {
    process_inventory_action(104);
}
```

**What it does:** Checks if the player already has item 104 (0x68). If NOT in inventory, gives it. If already owned, does nothing. This prevents duplicate item acquisition.

**State flags:** Reads inventory array. Writes inventory via `process_inventory_action` if item not present.

**Chains to:** `check_item_in_inventory`, conditionally `process_inventory_action`

**Conversation updates:** None

**Items:** Conditionally gives item 104 (0x68) — only if not already owned

---

### ACTION 0x014D (333) @ Ghidra 0x21DED

**Disassembly (0x21DED - 0x21E00):**
```asm
21DED: push     4
21DF2: call     get_current_room_number
21DF7: mov      eax, dword ptr [0xBB78]
21DFC: jmp      display_text_with_voice
```

**Code:**
```c
get_current_room_number();
display_text_with_voice(*(uint32_t*)0xBB78);
```

**What it does:** Displays text/voice using a runtime text data pointer stored at `[0xBB78]`. Similar to action 331 but uses the next pointer in the BSS text pointer array.

**State flags:** Reads `[0xBB78]` (text data pointer, BSS).

**Chains to:** `display_text_with_voice` (tail call)

**Conversation updates:** None

**Items:** None

---

### ACTION 0x014E (334) @ Ghidra 0x21E01

**Disassembly (0x21E01 → tail at 0x217A9):**
```asm
21E01: push     0xc
21E06: call     get_current_room_number
21E0B: push     ebx
21E0C: push     edx
21E0D: mov      ebx, 1           ; branch = 1
21E12: xor      edx, edx         ; npc = 0
21E14: mov      eax, 0x16        ; room = 22
21E19: call     update_conversation_state
21E1E: mov      eax, 0x4C        ; item = 76
21E23: jmp      0x217A9          ; → call process_inventory_action; pop edx, ebx; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/1);
process_inventory_action(76);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 1, then gives player item 76 (0x4C).

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 1 (room 22, NPC 0 conv state). Writes inventory via `process_inventory_action`.

**Chains to:** `update_conversation_state`, `process_inventory_action`

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=1)`

**Items:** Gives item 76 (0x4C)

---

### ACTION 0x014F (335) @ Ghidra 0x21E28

**Disassembly (0x21E28 - 0x21E3B):**
```asm
21E28: push     4
21E2D: call     get_current_room_number
21E32: mov      eax, 0x67         ; item = 103
21E37: jmp      process_inventory_action
```

**Code:**
```c
get_current_room_number();
process_inventory_action(103);
```

**What it does:** Gives player inventory item 103 (0x67).

**State flags:** Via `process_inventory_action` internals.

**Chains to:** `process_inventory_action` (tail call)

**Conversation updates:** None

**Items:** Gives item 103 (0x67)

---

### ACTION 0x0150 (336) @ Ghidra 0x21E3C

**Disassembly (0x21E3C - 0x21E4F):**
```asm
21E3C: push     4
21E41: call     get_current_room_number
21E46: mov      eax, dword ptr [0xBB7C]
21E4B: jmp      display_text_with_voice
```

**Code:**
```c
get_current_room_number();
display_text_with_voice(*(uint32_t*)0xBB7C);
```

**What it does:** Displays text/voice using a runtime text data pointer stored at `[0xBB7C]`. Third entry in the BSS text pointer sequence (after 0xBB74, 0xBB78).

**State flags:** Reads `[0xBB7C]` (text data pointer, BSS).

**Chains to:** `display_text_with_voice` (tail call)

**Conversation updates:** None

**Items:** None

---

### ACTION 0x0151 (337) @ Ghidra 0x21E50

**Disassembly (0x21E50 - 0x21E6F):**
```asm
21E50: push     0xc
21E55: call     get_current_room_number
21E5A: push     ebx
21E5B: push     edx
21E5C: mov      ebx, 2           ; branch = 2
21E61: xor      edx, edx         ; npc = 0
21E63: mov      eax, 0x16        ; room = 22
21E68: call     update_conversation_state
21E6D: pop      edx
21E6E: pop      ebx
21E6F: ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/2);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 2.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 2.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=2)`

**Items:** None

---

### ACTION 0x0152 (338) @ Ghidra 0x21E70

**Disassembly (0x21E70 → jmp 0x21E61):**
```asm
21E70: push     0xc
21E75: call     get_current_room_number
21E7A: push     ebx
21E7B: push     edx
21E7C: mov      ebx, 3           ; branch = 3
21E81: jmp      0x21E61          ; → xor edx,edx; mov eax,0x16; call update_conversation_state; pop; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/3);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 3.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 3.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=3)`

**Items:** None

---

### ACTION 0x0153 (339) @ Ghidra 0x21E83

**Disassembly (0x21E83 → jmp 0x21E61):**
```asm
21E83: push     0xc
21E88: call     get_current_room_number
21E8D: push     ebx
21E8E: push     edx
21E8F: mov      ebx, 4           ; branch = 4
21E94: jmp      0x21E61          ; → xor edx,edx; mov eax,0x16; call update_conversation_state; pop; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/4);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 4.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 4.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=4)`

**Items:** None

---

### ACTION 0x0154 (340) @ Ghidra 0x21E96

**Disassembly (0x21E96 → jmp 0x21E61):**
```asm
21E96: push     0xc
21E9B: call     get_current_room_number
21EA0: push     ebx
21EA1: push     edx
21EA2: mov      ebx, 5           ; branch = 5
21EA7: jmp      0x21E61          ; → xor edx,edx; mov eax,0x16; call update_conversation_state; pop; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/5);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 5.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 5.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=5)`

**Items:** None

---

### ACTION 0x0155 (341) @ Ghidra 0x21EA9

**Disassembly (0x21EA9 → jmp 0x21E61):**
```asm
21EA9: push     0xc
21EAE: call     get_current_room_number
21EB3: push     ebx
21EB4: push     edx
21EB5: mov      ebx, 6           ; branch = 6
21EBA: jmp      0x21E61          ; → xor edx,edx; mov eax,0x16; call update_conversation_state; pop; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/6);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 6.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 6.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=6)`

**Items:** None

---

### ACTION 0x0156 (342) @ Ghidra 0x21EBC

**Disassembly (0x21EBC → jmp 0x21E61):**
```asm
21EBC: push     0xc
21EC1: call     get_current_room_number
21EC6: push     ebx
21EC7: push     edx
21EC8: mov      ebx, 7           ; branch = 7
21ECD: jmp      0x21E61          ; → xor edx,edx; mov eax,0x16; call update_conversation_state; pop; ret
```

**Code:**
```c
get_current_room_number();
update_conversation_state(/*room=*/22, /*npc=*/0, /*branch=*/7);
```

**What it does:** Advances conversation tree for NPC 0 in room 22 to branch 7.

**State flags:** Writes `[0x4FBA4 + 22*4 + 0]` = 7.

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=22, npc=0, branch=7)`

**Items:** None

---

## Summary Table

| Action | Decimal | Address | Type | Room | NPC | Branch | Item | Notes |
|--------|---------|---------|------|------|-----|--------|------|-------|
| 0x0148 | 328 | 0x21D74 | Conv update | 2 | 0 | 1 | — | |
| 0x0149 | 329 | 0x21D91 | Set flag | — | — | — | — | Sets [0x95E8]=1 |
| 0x014A | 330 | 0x21DA3 | Give item | — | — | — | 102 | |
| 0x014B | 331 | 0x21DB7 | Show text | — | — | — | — | Text ptr from [0xBB74] |
| 0x014C | 332 | 0x21DCB | Cond. give | — | — | — | 104 | Only if not already owned |
| 0x014D | 333 | 0x21DED | Show text | — | — | — | — | Text ptr from [0xBB78] |
| 0x014E | 334 | 0x21E01 | Conv + item | 22 | 0 | 1 | 76 | |
| 0x014F | 335 | 0x21E28 | Give item | — | — | — | 103 | |
| 0x0150 | 336 | 0x21E3C | Show text | — | — | — | — | Text ptr from [0xBB7C] |
| 0x0151 | 337 | 0x21E50 | Conv update | 22 | 0 | 2 | — | |
| 0x0152 | 338 | 0x21E70 | Conv update | 22 | 0 | 3 | — | |
| 0x0153 | 339 | 0x21E83 | Conv update | 22 | 0 | 4 | — | |
| 0x0154 | 340 | 0x21E96 | Conv update | 22 | 0 | 5 | — | |
| 0x0155 | 341 | 0x21EA9 | Conv update | 22 | 0 | 6 | — | |
| 0x0156 | 342 | 0x21EBC | Conv update | 22 | 0 | 7 | — | |

## Patterns Observed

1. **Room 22 conversation progression (actions 334, 337-342):** A long conversation tree for NPC 0 in room 22 (0x16) with 7 sequential branches. Action 334 starts it (branch 1 + gives item 76), then actions 337-342 advance branches 2-7. This is a multi-stage NPC dialog where each dialog option advances the conversation state.

2. **Text display trio (actions 331, 333, 336):** Three actions that display text from consecutive BSS pointers [0xBB74], [0xBB78], [0xBB7C]. These are likely dialog lines shown during a conversation sequence, with the pointers pre-loaded by the conversation system when the room initializes.

3. **Conditional item give (action 332):** Uses `check_item_in_inventory` guard to prevent giving duplicate item 104. This is the first conditional item give in the batch set.

4. **Code sharing:** Actions 338-342 all share the tail at 0x21E61, differing only in the branch number. Action 337 is the "canonical" version that includes the shared tail inline. This is classic compiler tail-call merging for nearly identical handlers.
