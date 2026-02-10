# F8 Action Handler Batch 1 - Decompilation Results

## Function Name Key (resolved via Ghidra)

| Address | Name | Purpose |
|---------|------|---------|
| 0x2A218 | `get_current_room_number` | Prologue wrapper (saves context, gets room#) |
| 0x2A258 | `wait_or_process_input` | Yield / process events, may chain F8 action |
| 0x1B666 | `update_conversation_state` | Update conversation tree (EAX=room, EDX=npc, EBX=branch) |
| 0x1B1A2 | `play_get_naked_easter_egg` | Display NPC talking animation with dialog text |
| 0x19F2A | `render_menu_screen` | Render menu/overlay screen |
| 0x1B4A3 | `load_room_graphics_and_palette_dynamic` | Load room gfx + palette |
| 0x19DC8 | `draw_cursor_to_screen` | Draw mouse cursor |
| 0x28D32 | `play_cd_audio_track` | Play CD audio |
| 0x2942D | `fade_cd_audio` | Fade CD audio volume |
| 0x28FD5 | `set_vga_mode` | Set VGA display mode |
| 0x15E4C | `render_scene` | Full scene render |
| 0x244E8 | `set_vga_palette` | Set VGA palette colors |
| 0x29037 | `init_or_stop_sound` | Start/stop sound |
| 0x24157 | `process_inventory_action` | Process inventory item action |
| 0x1625D | `present_frame_to_screen` | Push framebuffer to display |
| 0x15258 | `wait_for_input_buffer_clear` | Wait for keyboard input |
| 0x25E90 | `allocate_memory` | Allocate memory buffer |
| 0x2A342 | `file_seek` | Seek in file handle |
| 0x2A43E | `file_read` | Read from file |
| 0x2A66B | `memcpy_wrapper` | Memory copy |
| 0x2A6B7 | `write_data_to_alfred1` | Write data to ALFRED.1 |
| 0x1A9CF | `render_character_to_screen` | Render character sprite |
| 0x1BD53 | (undefined) | Unknown - called by 0x010B with anim params |
| 0x26FAB | (undefined) | Unknown - cleanup after inventory action |
| 0x21008 | (undefined) | Unknown - used by library computer handler |

## Shared Code Blocks

### Shared tail at 0x213D3
```asm
213D3: call update_conversation_state  ; EAX=room, EDX=npc, EBX=branch
213D8: pop edx
213D9: pop ebx
213DA: ret
```
Used by: 0x0102, 0x0108, 0x0110, 0x0112 (which jumps directly here)

### Shared tail at 0x20D46
```asm
20D46: mov eax, 1
20D4B: jmp 0x11e1f   ; tail call to conversation display/exit handler
```
Used by: 0x0105, 0x0106, 0x0107 (via jmp short)

### Jump target 0x11E1D / 0x11E1F
This is inside the main handler dispatch area (unanalyzed). Based on context:
- EDX = data pointer loaded from 0xBA** table
- EAX = 1 (or 0 for 0x0103)
- Likely calls `play_get_naked_easter_egg` (display NPC dialog) then returns

---

## Handler Analysis

---

### ACTION 0x0101 (257) @ Ghidra 0x20C76

**Disassembly (0x20C76 - 0x20D03):**
```asm
push 0xc
call get_current_room_number
push edx
call render_menu_screen
mov eax, 0x9
call load_room_graphics_and_palette_dynamic  ; load room 9 graphics
mov eax, [0xfa7c]
call draw_cursor_to_screen
xor eax, eax
mov al, [0xc240]
add eax, 0x18          ; eax = byte[0xc240] + 24
cwde
call play_cd_audio_track   ; play CD track (byte[0xc240] + 24)
mov edx, 0x1309c
mov eax, 0x13098
call fade_cd_audio
mov edx, [0x1309c]
mov eax, [0x13098]
call set_vga_mode
; --- loop ---
push 0x161             ; action 0x161 = 353
call wait_or_process_input  ; chain to action 353
add esp, 4
mov eax, 0xff
call render_scene      ; render scene (full)
cmp byte [0xfb8c], 0   ; check flag
jz loop                ; loop back if flag not set
; --- flag set, exit ---
mov eax, [0xfab8]
call set_vga_palette
call init_or_stop_sound
mov eax, [0xb9d4]
jmp 0x1d66a            ; exit handler
```

**What it does:** Transition handler — loads room 9 graphics/palette, starts CD audio (track based on byte at 0xC240 + 24), sets up VGA mode, then enters a loop that chains to action 353 and renders the scene. Waits for flag byte [0xFB8C] to become non-zero, then restores the palette, stops sound, and exits.

**State flags:**
- Read: [0xFA7C], [0xC240], [0x13098], [0x1309C], [0xFB8C] (loop condition), [0xFAB8], [0xB9D4]
- Write: none directly

**Chains to:** Action 0x161 (353) via `wait_or_process_input` in a loop

**Conversation updates:** None

---

### ACTION 0x0102 (258) @ Ghidra 0x20D04

**Disassembly (0x20D04 - 0x20D27):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
or byte [0x95b8], 0x1   ; SET bit 0 of flag byte
mov ebx, 0x2             ; branch = 2
xor edx, edx             ; npc = 0
mov eax, 0x4             ; room = 4
jmp 0x213d3              ; → update_conversation_state(4, 0, 2)
```

**What it does:** Sets flag bit 0 at [0x95B8], then advances conversation state for room 4, NPC 0, branch 2.

**State flags:**
- Read/Write: [0x95B8] — OR with 0x01 (set bit 0)

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=4, npc=0, branch=2)`

---

### ACTION 0x0103 (259) @ Ghidra 0x20D28

**Disassembly (0x20D28 - 0x20D4F):**
```asm
push 0x8
call get_current_room_number
push edx
mov edx, [0xba2c]       ; load data pointer
xor eax, eax             ; param = 0
call play_get_naked_easter_egg  ; display NPC dialog
mov edx, [0xba30]       ; load next data pointer
mov eax, 0x1             ; param = 1
jmp 0x11e1f              ; tail-call to shared dialog handler
```

**What it does:** Plays two NPC talking animations in sequence. First with data from [0xBA2C] (param 0), then with data from [0xBA30] (param 1). These are likely character dialog sequences.

**State flags:**
- Read: [0xBA2C], [0xBA30] — NPC animation/dialog data pointers

**Chains to:** Shared exit at 0x11E1F (dialog display)

**Conversation updates:** None

---

### ACTION 0x0104 (260) @ Ghidra 0x20D50

**Disassembly (0x20D50 - 0x20D75):**
```asm
push 0x8
call get_current_room_number
push edx
mov edx, [0xba34]
mov eax, 0x1
call play_get_naked_easter_egg  ; display NPC dialog
mov edx, [0xba38]
jmp 0x11e1d              ; tail-call (slightly different entry than 0x11e1f)
```

**What it does:** Plays two NPC dialog sequences using data from [0xBA34] and [0xBA38]. Same pattern as 0x0103 but with different data pointers. The jump to 0x11E1D (vs 0x11E1F) suggests a slightly different parameter setup.

**State flags:**
- Read: [0xBA34], [0xBA38]

**Chains to:** Shared exit at 0x11E1D

**Conversation updates:** None

---

### ACTION 0x0105 (261) @ Ghidra 0x20D76

**Disassembly (0x20D76 - 0x20D88):**
```asm
push 0x8
call get_current_room_number
push edx
mov edx, [0xba3c]
jmp short 0x20d46        ; → mov eax, 1; jmp 0x11e1f
```

**What it does:** Simple NPC dialog display using data pointer from [0xBA3C]. Jumps to shared code that sets EAX=1 and enters the dialog handler.

**State flags:**
- Read: [0xBA3C]

**Chains to:** Shared tail at 0x20D46 → 0x11E1F

**Conversation updates:** None

---

### ACTION 0x0106 (262) @ Ghidra 0x20D89

**Disassembly (0x20D89 - 0x20D9B):**
```asm
push 0x8
call get_current_room_number
push edx
mov edx, [0xba40]
jmp short 0x20d46        ; → mov eax, 1; jmp 0x11e1f
```

**What it does:** Same pattern as 0x0105 — NPC dialog using data from [0xBA40].

**State flags:**
- Read: [0xBA40]

**Chains to:** Shared tail at 0x20D46 → 0x11E1F

**Conversation updates:** None

---

### ACTION 0x0107 (263) @ Ghidra 0x20D9C

**Disassembly (0x20D9C - 0x20DAE):**
```asm
push 0x8
call get_current_room_number
push edx
mov edx, [0xba44]
jmp short 0x20d46        ; → mov eax, 1; jmp 0x11e1f
```

**What it does:** Same pattern as 0x0105/0x0106 — NPC dialog using data from [0xBA44].

**State flags:**
- Read: [0xBA44]

**Chains to:** Shared tail at 0x20D46 → 0x11E1F

**Conversation updates:** None

---

### ACTION 0x0108 (264) @ Ghidra 0x20DAF

**Disassembly (0x20DAF - 0x20DCB):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 0x2             ; branch = 2
xor edx, edx             ; npc = 0
mov eax, 0x7             ; room = 7
jmp 0x213d3              ; → update_conversation_state(7, 0, 2)
```

**What it does:** Advances conversation state for room 7, NPC 0, branch 2. Identical structure to 0x0102 but targeting room 7.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=7, npc=0, branch=2)`

---

### ACTION 0x010B (267) @ Ghidra 0x20DCC

**Disassembly (0x20DCC - 0x20E17):**
```asm
push 0x14
call get_current_room_number
push ebx
push ecx
push edx
push 0x0                 ; stack param = 0
mov ecx, 0x9508          ; param: buffer at 0x9508
mov ebx, 0x10            ; param: count/size = 16
mov edx, 0x9518          ; param: dest at 0x9518
mov eax, 0x9548          ; param: source at 0x9548
call FUN_0001bd53        ; animate/transfer sprite data
mov ebx, 0x3             ; branch = 3
xor edx, edx             ; npc = 0
mov eax, 0x7             ; room = 7
call update_conversation_state  ; update(7, 0, 3)
mov eax, 0x8
call process_inventory_action   ; process inventory for item 8
call FUN_00026fab        ; cleanup/finalize
pop edx
pop ecx
pop ebx
ret
```

**What it does:** Complex handler that: (1) performs a sprite/animation transfer using data buffers at 0x9508/0x9518/0x9548 with 16 entries, (2) advances conversation in room 7 to branch 3, and (3) processes inventory action for item 8 (gives or takes an inventory item). This likely triggers a scene where the player receives item 8 after a conversation.

**State flags:** None directly (data at 0x9508/0x9518/0x9548 are buffers, not simple flags)

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=7, npc=0, branch=3)`

**Inventory:** `process_inventory_action(8)` — item 8

---

### ACTION 0x010C (268) @ Ghidra 0x20E18

**Disassembly (0x20E18 - 0x20E2D):**
```asm
push 0x8
call get_current_room_number
push edx
mov edx, [0xba58]
jmp 0x11e1d              ; tail-call to dialog handler
```

**What it does:** Simple NPC dialog display using data from [0xBA58]. Same pattern as 0x0105-0x0107 but without setting EAX first (EAX preserved from get_current_room_number).

**State flags:**
- Read: [0xBA58]

**Chains to:** Shared exit at 0x11E1D

**Conversation updates:** None

---

### ACTION 0x010E (270) @ Ghidra 0x20E2E

**Disassembly (0x20E2E - very long, extends past 60 instructions):**
```asm
push 0x1c
call get_current_room_number
push ebx/ecx/edx/esi/edi
mov eax, 0x3584
call allocate_memory     ; allocate 0x3584 (13700) bytes
mov esi, eax             ; save buffer ptr
mov edi, eax
xor ah, ah
mov byte [0x11754], ah   ; clear flag byte
mov eax, 0x1
call load_room_graphics_and_palette_dynamic  ; load room 1 gfx
mov eax, [0xf908]
xor ebx, ebx
mov edx, 0x309e0         ; *** LIBRARY BOOKS DATA OFFSET ***
call file_seek           ; seek to books data in ALFRED.7
mov ecx, [0xf908]
mov ebx, 0x1
mov edx, 0x3529
mov eax, esi             ; read into buffer
call file_read           ; read 0x3529 bytes of book data
mov esi, edi
push 0x162               ; action 0x162 = 354
call wait_or_process_input  ; chain to action 354
add esp, 4
call FUN_00021008        ; render library computer UI
mov eax, [0xc030]
mov ebx, 0x61            ; x=97
mov edx, 0xe1            ; y=225
call render_character_to_screen
call present_frame_to_screen
; --- keyboard input loop ---
xor cl, cl
.loop:
xor eax, eax
mov al, cl
cmp eax, 0x31            ; key '1'
jz .process_key
cmp eax, 0x32            ; key '2'
jz .process_key
cmp eax, 0x33            ; key '3'
jz .process_key
call wait_for_input_buffer_clear
mov cl, al
jmp .loop
; --- process key ---
cmp eax, 0x31
jnz .check_key2
; key '1' handler: render another screen...
call FUN_00021008
mov eax, [0xc034]
mov ebx, 0x102
mov edx, 0xaa
call render_character_to_screen
call present_frame_to_screen
call wait_for_input_buffer_clear
; ... (continues with more key handling)
```

**What it does:** This is the **LIBRARY COMPUTER** handler! It:
1. Allocates a 13,700-byte buffer
2. Clears a flag at [0x11754]
3. Loads room 1 graphics
4. Seeks to offset 0x309E0 in ALFRED.7 (the library books database)
5. Reads 0x3529 bytes of book data
6. Chains to action 354 (library computer intro)
7. Renders the library computer UI
8. Enters a keyboard input loop accepting keys '1', '2', '3' (menu choices)
9. Each key triggers different screens (search, browse, etc.)

This is clearly the library/computer interactive system documented in LIBRARY_COMPUTER_DOCUMENTATION.md.

**State flags:**
- Write: [0x11754] = 0 (clear computer active flag)
- Read: [0xF908] (file handle), [0xC030], [0xC034], [0xC058] (screen buffer ptrs)

**Chains to:** Action 0x162 (354) via `wait_or_process_input`

**Conversation updates:** None

---

### ACTION 0x010F (271) @ Ghidra 0x21221

**Disassembly (0x21221 - 0x21236):**
```asm
push 0x8
call get_current_room_number
push edx
mov edx, [0xba78]
jmp 0x11e1d              ; tail-call to dialog handler
```

**What it does:** Simple NPC dialog display using data from [0xBA78]. Same short pattern as 0x010C.

**State flags:**
- Read: [0xBA78]

**Chains to:** Shared exit at 0x11E1D

**Conversation updates:** None

---

### ACTION 0x0110 (272) @ Ghidra 0x21237

**Disassembly (0x21237 - 0x21253):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 0x1             ; branch = 1
xor edx, edx             ; npc = 0
mov eax, 0xe             ; room = 14
jmp 0x213d3              ; → update_conversation_state(14, 0, 1)
```

**What it does:** Advances conversation state for room 14 (0xE), NPC 0, branch 1.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=14, npc=0, branch=1)`

---

### ACTION 0x0111 (273) @ Ghidra 0x21254

**Disassembly (0x21254 - continues for 60+ insns, complex):**
```asm
push 0x14
call get_current_room_number
push ebx/ecx/edx/esi
mov eax, [0xfac8]
add eax, 0x221           ; offset into room data
mov ebx, 0x12            ; size = 18
mov edx, 0x94f5          ; destination buffer
call memcpy_wrapper      ; copy 18 bytes from room data + 0x221
mov ecx, [0xf914]        ; file handle
mov ebx, 0x1
mov edx, 0x17            ; size = 23
mov eax, 0x94f0          ; source buffer
call write_data_to_alfred1  ; write to ALFRED.1
mov esi, [0xfaac]        ; room sprite data
; ... read offset at esi+0x50 (SIB addressing) ...
; ... load from [0xf8f0] ...
call file_seek
; ... more write_data_to_alfred1 calls ...
mov byte [0xfb70], val
; ... set up conversation record at 0xfb70-0xfb75 ...
mov byte [0xfb74], 0x1
mov byte [0xfb75], 0x3
; ... write conversation data ...
call write_data_to_alfred1
; ... more file operations ...
```

**What it does:** This is a **save/persist conversation state** handler. It:
1. Copies data from room structures to temporary buffers
2. Writes conversation state data to ALFRED.1 file (persistent save)
3. Sets up a conversation record structure at 0xFB70-0xFB75 with values including branch=1 and branch=3
4. Multiple file seek/write operations to persist game state

This handler appears to save conversation progress to the game data file, ensuring the player's dialog choices are preserved.

**State flags:**
- Read: [0xFAC8], [0xFAAC], [0xF914], [0xF8F0], [0xF908]
- Write: [0xFB70] (conversation record), [0xFB74] = 0x01, [0xFB75] = 0x03

**Chains to:** None visible in first 60 instructions

**Conversation updates:** Writes conversation data to ALFRED.1 via `write_data_to_alfred1`

---

### ACTION 0x0112 (274) @ Ghidra 0x213BB

**Disassembly (0x213BB - 0x213DA):**
```asm
push 0xc
call get_current_room_number
push ebx
push edx
mov ebx, 0x1             ; branch = 1
xor edx, edx             ; npc = 0
mov eax, 0x12            ; room = 18
call update_conversation_state  ; update(18, 0, 1)
pop edx
pop ebx
ret
```

**What it does:** Advances conversation state for room 18 (0x12), NPC 0, branch 1. This is the simplest handler — just a direct call to `update_conversation_state` and return.

**State flags:** None directly

**Chains to:** None

**Conversation updates:** `update_conversation_state(room=18, npc=0, branch=1)`

---

## Summary Table

| Action | Dec | Handler Type | Room | NPC | Branch | Notes |
|--------|-----|-------------|------|-----|--------|-------|
| 0x0101 | 257 | Room transition + CD audio + loop | 9 | - | - | Loads room 9, plays CD track, loops on action 353, waits for flag [0xFB8C] |
| 0x0102 | 258 | Set flag + conversation | 4 | 0 | 2 | Sets [0x95B8] bit 0, then update_conversation_state(4,0,2) |
| 0x0103 | 259 | NPC dialog sequence | - | - | - | Two dialog sequences from [0xBA2C] and [0xBA30] |
| 0x0104 | 260 | NPC dialog sequence | - | - | - | Two dialog sequences from [0xBA34] and [0xBA38] |
| 0x0105 | 261 | NPC dialog (short) | - | - | - | Single dialog from [0xBA3C] |
| 0x0106 | 262 | NPC dialog (short) | - | - | - | Single dialog from [0xBA40] |
| 0x0107 | 263 | NPC dialog (short) | - | - | - | Single dialog from [0xBA44] |
| 0x0108 | 264 | Conversation advance | 7 | 0 | 2 | update_conversation_state(7,0,2) |
| 0x010B | 267 | Animation + conv + inventory | 7 | 0 | 3 | Animate, update_conv(7,0,3), give/take item 8 |
| 0x010C | 268 | NPC dialog (short) | - | - | - | Single dialog from [0xBA58] |
| 0x010E | 270 | LIBRARY COMPUTER | - | - | - | Full interactive library computer system |
| 0x010F | 271 | NPC dialog (short) | - | - | - | Single dialog from [0xBA78] |
| 0x0110 | 272 | Conversation advance | 14 | 0 | 1 | update_conversation_state(14,0,1) |
| 0x0111 | 273 | Save conversation data | - | - | - | Writes conv state to ALFRED.1 file |
| 0x0112 | 274 | Conversation advance | 18 | 0 | 1 | update_conversation_state(18,0,1) |

## Data Address Table (0xBA2C - 0xBA78)

These addresses form a table of NPC animation/dialog data pointers used by the dialog display handlers:

| Address | Used by Action | Purpose |
|---------|---------------|---------|
| 0xBA2C | 0x0103 | Dialog data ptr 1 |
| 0xBA30 | 0x0103 | Dialog data ptr 2 |
| 0xBA34 | 0x0104 | Dialog data ptr 1 |
| 0xBA38 | 0x0104 | Dialog data ptr 2 |
| 0xBA3C | 0x0105 | Dialog data ptr |
| 0xBA40 | 0x0106 | Dialog data ptr |
| 0xBA44 | 0x0107 | Dialog data ptr |
| 0xBA58 | 0x010C | Dialog data ptr |
| 0xBA78 | 0x010F | Dialog data ptr |
