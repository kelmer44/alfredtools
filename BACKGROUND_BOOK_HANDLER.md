# Background Book Handler (Libro de Fondos) - Complete Analysis

## Overview

The **Background Book** ("Un album de pantallas" / "Libro de Fondos") is a photobook-style UI showing thumbnail previews of all game rooms. It's accessed via **button 8** in the right-click inventory/menu screen.

## Entry Point

- **Ghidra address**: `0x141AA` (NOT defined as a function in Ghidra due to LE relocation indirection)
- **Ghidra shows**: Located in gap between `book_nav_stub_1` (0x140CD) and `background_book_handler_tail` (0x143BE)
- **Called from**: `main_menu_handler` (0x12918) via button handler table at `DAT_000486f8`
- **Button entry**: Index 8, hitbox (217, 293) size 32x32, raw pointer `0x041AA` + LE reloc `+0x10000` = `0x141AA`
- **Function span**: 0x141AA - 0x143C1 (JMP 0x13A65 tail call to init_palette area)

## Button Handler Table (DAT_000486f8)

10-byte entries: `[x:u16][y:u16][w:u8][h:u8][func_ptr:u32]`

| Idx | Hitbox (x,y,w,h) | Raw Ptr | Relocated | Purpose |
|-----|-------------------|---------|-----------|---------|
| 0 | 140,115 60x60 | 0x12DA7 | 0x12DA7 | Inventory slot 0 |
| 1 | 222,107 60x60 | 0x12E71 | 0x12E71 | Inventory slot 1 |
| 2 | 304,99 60x60 | 0x12E87 | 0x12E87 | Inventory slot 2 |
| 3 | 386,91 60x60 | 0x12E9D | 0x12E9D | Inventory slot 3 |
| 4 | 132,188 75x23 | 0x132E4 | 0x132E4 | Menu button |
| 5 | 134,222 72x25 | 0x13002 | 0x13002 | Menu button |
| 6 | 134,259 72x25 | 0x13C92 | 0x13C92 | Menu button |
| 7 | 134,294 70x25 | 0x12F3F | 0x12F3F | Menu button |
| **8** | **217,293 32x32** | **0x041AA** | **0x141AA** | **Background Book** |
| 9 | 468,88 22x32 | 0x12EE6 | 0x12EE6 | Scroll up |
| 10 | 463,132 22x30 | 0x12EB3 | 0x12EB3 | Scroll down |

> Note: Raw pointer values for button 8 required LE relocation (+0x10000 code base). Other buttons appear to already have correct addresses.

## ALFRED.1 Data Offsets

| Offset | Size | Description |
|--------|------|-------------|
| `0x30BA20` | `0x70CA` (28,874 bytes) | Menu/book UI frame graphics |
| `0x31EB1E` | `0x3E800` (256,000 bytes) | Room background composition data |
| `0x35D31E` | `0xABD2` (43,986 bytes) | RLE-compressed room thumbnails |

Decompressed thumbnail buffer: `0x25620` (153,120 bytes) = 29 rooms × 5,280 bytes each.

## Thumbnail Format

- **Size**: 240 × 22 pixels = 5,280 bytes per thumbnail
- **Color depth**: 8-bit indexed (1 byte/pixel)
- **Transparency**: Color index `0xFF`
- **Compression**: RLE compressed in ALFRED.1 (43,986 → 153,120 bytes)
- **Offset formula**: `room_index * 5280` into the decompressed buffer

## Column Layout

The book displays **2 columns of 17 entries each** (34 total thumbnail slots):

- **Column 1**: x=39 (0x27), room indices from `DAT_0004B884` (17 bytes)
- **Column 2**: x=359 (0x167), room indices from `DAT_0004B895` (17 bytes)
- **Y spacing**: Each entry at `y = entry_index * 23 + 3`

### Column 1 Room Indices (DAT_0004B884)
```
[5, 8, 20, 24, 22, 7, 12, 14, 18, 16, 26, 28, 2, 11, 12, 26, 28]
```

### Column 2 Room Indices (DAT_0004B895)
```
[9, 6, 13, 8, 19, 4, 8, 21, 0, 10, 1, 3, 25, 27, 23, 15, 17]
```

> Note: Value `0` at col2[8] means empty slot. Some room IDs repeat (12, 26, 28 in col1; 8 in col2).

## Full Disassembly (annotated)

```asm
; === BACKGROUND BOOK HANDLER ===
; Entry: called from main_menu_handler button 8 dispatch
; Effect: Shows 2-column book of room background thumbnails

141AA: push     0x2c                    ; stack frame size
141AF: call     __STK                   ; stack check
141B4: push     ebx
141B5: push     ecx
141B6: push     edx
141B7: push     esi
141B8: push     edi
141B9: push     ebp
141BA: sub      esp, 8                  ; 2 local vars on stack

; --- Render menu screen background ---
141BD: call     render_menu_screen

; --- Allocate buffers ---
141C2: mov      eax, 0x25620            ; 153,120 bytes (decompressed thumbnails)
141C7: call     allocate_memory
141CC: mov      ebp, eax                ; EBP = thumbnail buffer
141CE: mov      esi, eax                ; ESI = same (kept for free later)
141D0: mov      eax, 0x70CA             ; 28,874 bytes (menu UI graphics)
141D5: call     allocate_memory
141DA: mov      edi, eax                ; EDI = menu gfx buffer
141DC: mov      [esp], eax              ; save on stack

; --- Load menu/book frame graphics from ALFRED.1 ---
141DF: mov      eax, [file_handle_alfred1]
141E4: xor      ebx, ebx               ; SEEK_SET
141E6: mov      edx, 0x30BA20           ; offset: menu graphics
141EB: call     file_seek
141F0: mov      ecx, [file_handle_alfred1]
141F6: mov      ebx, 1
141FB: mov      edx, 0x70CA             ; size
14200: mov      eax, edi                ; dest buffer
14202: call     file_read

; --- Load room background composition data ---
14207: mov      edi, [saved_background_buffer_ptr]  ; backup pointer
1420D: mov      eax, [file_handle_alfred1]
14212: xor      ebx, ebx
14214: mov      edx, 0x31EB1E           ; offset: room BG data (256KB)
14219: call     file_seek
1421E: mov      ecx, [file_handle_alfred1]
14224: mov      eax, [composition_buffer_ptr]
14229: mov      ebx, 1
1422E: mov      edx, 0x3E800            ; 256,000 bytes
14233: call     file_read

; --- Load and decompress thumbnails ---
14238: mov      eax, [file_handle_alfred1]
1423D: xor      ebx, ebx
1423F: mov      edx, 0x35D31E           ; offset: compressed thumbnails
14244: call     file_seek
14249: mov      ecx, [file_handle_alfred1]
1424F: mov      ebx, 1
14254: mov      edx, 0xABD2             ; 43,986 bytes compressed
14259: mov      eax, edi                ; temp buffer
1425B: call     file_read
14260: mov      edx, ebp                ; dest = thumbnail buffer
14262: mov      eax, edi                ; src = temp buffer
14264: call     decompress_rle_block

; === COLUMN 1 LOOP (17 entries) ===
14269: xor      ah, ah
1426B: mov      [esp+4], ah             ; loop counter = 0
1426F: jmp      0x142B5                 ; jump to loop test

; --- Column 1 body ---
14271: push     0xFF                    ; transparency color
14276: push     0x16                    ; height = 22 pixels
14278: xor      dh, dh
1427A: mov      dl, al                  ; DL = loop counter
1427C: imul     edx, edx, 0x17          ; EDX = counter * 23
1427F: add      edx, 3                  ; EDX = counter * 23 + 3 (y position)
14282: xor      ebx, ebx
14284: mov      bx, dx                  ; EBX = y position
14287: xor      edx, edx
14289: mov      dl, [eax + 0xB884]      ; room_index = col1_table[counter] (RELOCATED to 0x4B884)
1428F: mov      eax, edx                ; EAX = room_index
14291: shl      eax, 2                  ; EAX = room_index * 4
14294: add      eax, edx                ; EAX = room_index * 5
14296: shl      eax, 5                  ; EAX = room_index * 160
14299: mov      edx, eax
1429B: shl      eax, 5                  ; EAX = room_index * 5120
1429E: add      eax, edx                ; EAX = room_index * 5280 (= 240 * 22)
142A0: add      eax, esi                ; EAX = &thumbnail_data[room_index * 5280]
142A2: mov      ecx, 0xF0               ; width = 240 pixels
142A7: mov      edx, 0x27               ; x = 39 (column 1)
142AC: call     blit_with_transparency_check

; --- Column 1 loop test ---
142B1: inc      [esp+4]                 ; counter++
142B5: xor      eax, eax
142B7: mov      al, [esp+4]             ; AL = counter
142BB: cmp      eax, 0x11               ; 17 entries
142BE: jl       0x14271                 ; loop while counter < 17

; === COLUMN 2 LOOP (17 entries) ===
142C0: xor      dl, dl
142C2: mov      [esp+4], dl             ; counter = 0
142C6: jmp      0x1430C

; --- Column 2 body ---
142C8: push     0xFF                    ; transparency color
142CD: push     0x16                    ; height = 22
142CF: xor      dh, dh
142D1: mov      dl, al
142D3: imul     edx, edx, 0x17          ; y = counter * 23
142D6: add      edx, 3                  ; y = counter * 23 + 3
142D9: xor      ebx, ebx
142DB: mov      bx, dx
142DE: xor      edx, edx
142E0: mov      dl, [eax + 0xB895]      ; room_index = col2_table[counter] (RELOCATED to 0x4B895)
142E6: mov      eax, edx
142E8: shl      eax, 2
142EB: add      eax, edx
142ED: shl      eax, 5
142F0: mov      edx, eax
142F2: shl      eax, 5
142F5: add      eax, edx                ; EAX = room_index * 5280
142F7: add      eax, esi
142F9: mov      ecx, 0xF0               ; width = 240
142FE: mov      edx, 0x167              ; x = 359 (column 2)
14303: call     blit_with_transparency_check

; --- Column 2 loop test ---
14308: inc      [esp+4]
1430C: xor      eax, eax
1430E: mov      al, [esp+4]
14312: cmp      eax, 0x11               ; 17 entries
14315: jl       0x142C8

; === WAIT FOR MOUSE CLICK (input loop) ===
14317: mov      eax, [cursor_sprite_ptr]
1431C: call     draw_cursor_to_screen
14321: call     present_frame_to_screen
14326: cmp      byte [mouse_click_flag], 0   ; wait for click
1432D: je       0x1433B
1432F: mov      eax, 0xFF
14334: call     render_scene             ; re-render while button held
14339: jmp      0x14326

; --- Wait for release ---
1433B: cmp      byte [mouse_click_flag], 0
14342: jne      0x14350
14344: mov      eax, 0xFF
14349: call     render_scene
1434E: jmp      0x1433B

; === CLEANUP AND RESTORE ===
14350: mov      edx, [DAT_0004fb28]
14356: mov      eax, [composition_buffer_ptr]
1435B: mov      ebx, 0x3E800
14360: call     memcpy_wrapper           ; restore original background

; --- Blit menu return graphics ---
14365: xor      eax, eax
14367: mov      al, [0x87B5]             ; height from table
1436C: push     eax
1436D: xor      ecx, ecx
1436F: mov      cl, [0x87B4]             ; width from table
14375: xor      ebx, ebx
14377: mov      bx, [0x87B2]             ; y from table
1437E: xor      edx, edx
14380: mov      dx, [0x87B0]             ; x from table
14387: mov      eax, [0x87A8]            ; source offset
1438C: sub      eax, 0x30BA20            ; relative to menu gfx start
14391: mov      edi, [esp+4]             ; menu gfx buffer
14395: add      eax, edi                 ; absolute pointer
14397: call     blit_image_to_screen

; --- Final render and cleanup ---
1439C: mov      eax, [cursor_sprite_ptr]
143A1: call     draw_cursor_to_screen
143A6: call     amulet_statue_handler    ; 0x12F06
143AB: call     present_frame_to_screen

; --- Free allocated buffers ---
143B0: mov      eax, esi                 ; thumbnail buffer
143B2: call     free_memory
143B7: mov      eax, edi                 ; menu gfx buffer / backup ptr
143B9: call     free_memory

; --- Epilogue (shared with init_palette) ---
143BE: add      esp, 8
143C1: jmp      0x13A65                  ; tail call
```

## Related Functions (0x140D5 - 0x14621)

### Navigation Handlers (0x140D5 - 0x141A9)
6 small functions for scrolling the book columns. Each modifies byte indices at data addresses `0x9650`, `0x9651`, `0x9652` (after relocation). Bounds: 0 to 14.

### render_book_room_preview (0x143C6 - 0x14476)
Takes params in registers:
- Reads position data from lookup table at `[EAX*2 + 0x8880]` / `[EAX*2 + 0x8882]` (x,y word pairs after relocation)
- Computes thumbnail buffer offset: `index * 10000 + 30000` 
- Calls `blit_image_to_screen` (width=66) and another blit at 0x16B61
- **Purpose**: Renders larger preview when a thumbnail is selected

### clear_text_input_area (0x14477 - 0x144C1)
- Calls `backup_screen_under_cursor` (0x15DF8) at position (227, 188)
- Fills 205×93 pixel rectangle with color `0xC3`
- Stride = 640 (VGA Mode-X)
- **Purpose**: Clears a text input field area

### text_input_handler (0x144C2 - 0x145C4)
Keyboard input loop with character-by-character display:
- Calls `wait_or_process_input(0xB5)` then `wait_for_input_buffer_clear` (0x15258)
- Key handling:
  - `0x1C` (Enter) → exit, accept input
  - `0x01` (Escape) → exit, cancel
  - `0x0E` (Backspace) → delete last char, redraw
  - Other → append char, render via `render_character_to_screen` (0x1A9CF)
- Input string stored at `[EBP]`, copy at `0x9578`
- Max x position: 419 (0x1A3), min: 251 (0xFB)
- **Purpose**: General text input handler (possibly shared with library computer search)

### draw_char_to_screen_buffer (0x145C5 - 0x1461F)
- Calls `backup_screen_under_cursor` (0x15DF8) for positioning
- Writes character bytes to screen buffer at `[0xFAD8]`
- Stride = 640 (0x280) per scanline
- Calls `present_frame_to_screen` at end
- Returns with `RET 4` (callee cleanup, 1 stack param)

## Item Combination Table Entry

The item combination table (at `DAT_00048118`) has entry [44] for item 96:
- `item1 = 96, item2 = 96, handler = 0x14ED7`
- This address falls mid-instruction in `init_memory_buffers` and decodes as `MOV AL, 1; POP EDX; POP EBX; RET` — a trivial no-op returning true.
- **This is intentional** - "using" the background book on generic hotspots via `execute_complex_item_script_table` succeeds with no effect. The real UI is opened through the menu button, not the item system.

## LE Executable Address Mapping

| Section | Object | Ghidra Base | File Offset Formula |
|---------|--------|-------------|---------------------|
| Code | 1 | 0x10000 | file = ghidra + 0x4200 |
| Data | 2 | 0x40000 | file = ghidra + 0x3200 |

The button handler table stores **unrelocated** pointers. Button 8's raw value `0x041AA` gets the code base added (`+0x10000`) at load time to become `0x141AA`.

Data references in the handler (e.g., `[EAX + 0xB884]`) get the data base added (`+0x40000`) at load time, making the runtime address `0x4B884`.

## Thumbnail Rendering Math

For each of the 17 entries per column:
```
y_position = entry_index * 23 + 3
thumbnail_offset = room_index * (4+1) * 32 * (32+1) = room_index * 5280
                 = room_index * 5280 (= 240 width * 22 height)
source_ptr = decompressed_buffer + thumbnail_offset
blit_with_transparency_check(source_ptr, width=240, x=col_x, y=y_position, height=22, transparency=0xFF)
```

Column 1: x=39, Column 2: x=359.

## Pseudocode

```c
void background_book_handler() {
    render_menu_screen();
    
    byte *thumb_buf = allocate_memory(0x25620);  // 153,120 bytes
    byte *gfx_buf = allocate_memory(0x70CA);     // 28,874 bytes
    
    // Load menu frame graphics
    file_seek(alfred1_handle, 0x30BA20, SEEK_SET);
    file_read(gfx_buf, 0x70CA, alfred1_handle);
    
    byte *backup_ptr = saved_background_buffer_ptr;
    
    // Load 256KB room background data into composition buffer
    file_seek(alfred1_handle, 0x31EB1E, SEEK_SET);
    file_read(composition_buffer_ptr, 0x3E800, alfred1_handle);
    
    // Load and decompress thumbnails 
    file_seek(alfred1_handle, 0x35D31E, SEEK_SET);
    file_read(backup_ptr, 0xABD2, alfred1_handle);  // compressed into temp
    decompress_rle_block(backup_ptr, thumb_buf);     // 43KB → 153KB
    
    // Draw Column 1 (17 room thumbnails)
    for (int i = 0; i < 17; i++) {
        int room_idx = col1_room_table[i];  // DAT_0004B884
        int y = i * 23 + 3;
        byte *src = thumb_buf + room_idx * 5280;
        blit_with_transparency_check(src, 240, 39, y, 22, 0xFF);
    }
    
    // Draw Column 2 (17 room thumbnails)  
    for (int i = 0; i < 17; i++) {
        int room_idx = col2_room_table[i];  // DAT_0004B895
        int y = i * 23 + 3;
        byte *src = thumb_buf + room_idx * 5280;
        blit_with_transparency_check(src, 240, 359, y, 22, 0xFF);
    }
    
    // Wait for mouse click (show cursor, present frame)
    do {
        draw_cursor_to_screen(cursor_sprite_ptr);
        present_frame_to_screen();
        while (mouse_click_flag != 0) render_scene(0xFF);
        while (mouse_click_flag == 0) render_scene(0xFF);
    } while (0);  // single click exits
    
    // Restore original background
    memcpy_wrapper(composition_buffer_ptr, DAT_0004FB28, 0x3E800);
    
    // Blit menu return graphics from offset table at 0x87A8
    blit_image_to_screen(gfx_buf + (offset_87A8 - 0x30BA20), 
                         x_87B0, y_87B2, width_87B4, height_87B5);
    
    draw_cursor_to_screen(cursor_sprite_ptr);
    amulet_statue_handler();  // 0x12F06
    present_frame_to_screen();
    
    free_memory(thumb_buf);
    free_memory(backup_ptr);
}
```

## ScummVM Implementation Notes

### Current State (extrascreens.cpp `BackgroundBook` class)
The existing ScummVM implementation is a **rough placeholder** that diverges significantly from the original:
- Uses **text-based room name list** instead of graphical thumbnails
- Reads room names from JUEGO.EXE at offset 0x49315 (1,335 bytes, FD-00-08-02 delimited)
- Uses "extra screen 13" (0x226358) as background
- Has PREVIOUS/NEXT text page navigation buttons
- `kItemsPerPage = 22` text entries per page
- Button rects are wrong: uses (238,104 28x44) and (238,178 28x44) — these are placeholder coordinates

### What Needs to Change
1. **Replace text list with graphical thumbnails** - decompress RLE data from ALFRED.1 at 0x35D31E
2. **Two columns of 17 thumbnails** at x=39 and x=359, y spacing = 23 pixels
3. **Room index tables** from DAT_0004B884 and DAT_0004B895 (hardcode or extract from EXE)
4. **Simple click-to-exit** - original has no per-thumbnail click detection in the main handler
5. **Menu frame gfx** from 0x30BA20 provides the book's border/decorations
6. **Navigation scroll handlers** at 0x140D5-0x141A9 suggest scrollable pages (bounds 0-14 = 15 pages)
7. The 0x31EB1E data (256KB) is loaded into the composition buffer for room preview via `render_book_room_preview` (0x143C6)
