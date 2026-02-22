# Item Combination Table — Complete Reference

## Overview

This document catalogs **all 113 item combination entries** found in the dispatch table of `JUEGO.EXE`, mapping to **42 unique handler functions**. These handle the results of combining inventory items with hotspots (or using items on themselves).

### Dispatch Architecture

The **dispatcher function** `execute_complex_item_script_table` at Ghidra `0x191E9` performs a two-pass table search:

1. **Pass 1 (Self-use)**: Scans for entries where `item1 == item2 == selected_inventory_item` and `current_hotspot_extra_id == 0` (using item on itself from inventory)
2. **Pass 2 (Item + Hotspot)**: Scans for entries where either `(item1 == hotspot_extra_id AND item2 == selected_item)` OR `(item1 == selected_item AND item2 == hotspot_extra_id)` — the table is direction-agnostic

If no match is found, Alfred says a random rejection line from `RANDOM_REJECTION_TEXT_PTRS` (text indices 154-169).

### Table Location
- **File offset**: `0x4B318` in JUEGO.EXE
- **Ghidra address**: `0x48118` (data section base `0x40000` + raw offset `0x8118`)
- **Format**: 113 entries × 8 bytes (`[uint16 item1][uint16 item2][uint32 func_ptr]`)
- **Pointer fixup**: `ghidra_address = stored_pointer + 0x10000`
- **Terminator**: `0xFFFF` sentinel after last entry

### How Handlers Are Called

```
CALL dword ptr [EAX*0x8 + 0x4811C]
```

The function pointer at offset +4 from each 8-byte entry is called indirectly. Before calling, the dispatcher calls `walk_to_target_and_execute_queued_action` to walk Alfred to the hotspot, then `animate_talk_bubble` (unless in rooms 0x19/0x29 = Egypt rooms 25/41).

### Handler Code Region

All 42 handler functions are in the **unanalyzed code region** `0x227B2–0x25525` (Ghidra addresses). They are proper Watcom C functions with `PUSH stack_size; CALL __STK` prologues but Ghidra has no function boundaries defined there — they're only reached via indirect calls through the data table.

### Common Handler Patterns

| Pattern | Description |
|---------|-------------|
| **Dialog only** | Calls `display_text_with_voice(text_ptr)` to show Alfred speaking |
| **Remove item** | Calls `remove_inventory_item()` to take item from inventory |
| **Add item** | Calls `process_inventory_action(item_id)` to give new item |
| **Conversation** | Calls `update_conversation_state(room, npc, branch)` |
| **NPC talk** | Calls `play_get_naked_easter_egg()` to run NPC dialog sequence |
| **Animation** | Loops with `render_scene()` + `setup_alfred_frame_from_state()` |
| **Room change** | Calls `load_room_and_init_alfred()` to switch rooms |
| **File I/O** | Reads from/writes to ALFRED resource files (stickers, sprites) |
| **Audio** | Plays sound effects or CD audio tracks |
| **Fight** | Calls `play_fight_animation()` for combat sequences |
| **Graphics load** | Calls `load_room_graphics_and_palette_dynamic()` for cutscene backgrounds |

### Address Computation

```
file_offset_of_handler = ghidra_address - 0x10000 + 0x14200
data_segment_address = raw_address_in_instruction + 0x40000  (for MOV [addr] fixup)
```

---

## Complete Combination Table

| # | Item1 | Item2 | Handler | Type | Description |
|---|-------|-------|---------|------|-------------|
| 0 | 281 (ATM) | 2 (credit_card) | 0x227B2 | HOTSPOT+ITEM | Use credit card on ATM |
| 1 | 294 (shop_window) | 4 (brick) | 0x2284B | HOTSPOT+ITEM | Throw brick at shop window |
| 2 | 295 (shop_storefront) | 4 (brick) | 0x22AF7 | HOTSPOT+ITEM | Use brick on shop storefront (rejected) |
| 3 | 315 (electric_plug) | 6 (cord) | 0x22B0B | HOTSPOT+ITEM | Plug cord into electrical socket |
| 4 | 309 (museum_guard) | 5 (money) | 0x22C58 | HOTSPOT+ITEM | Bribe museum guard |
| 5 | 309 (museum_guard) | 1 (ID_card) | 0x22BF9 | HOTSPOT+ITEM | Show ID to museum guard |
| 6 | 353 (statue) | 7 (amulet) | 0x22CC1 | HOTSPOT+ITEM | Place amulet on statue |
| 7 | 347 (librarian) | 8 (secret_code) | 0x22E10 | HOTSPOT+ITEM | Give secret code book to librarian |
| 8 | 9+9 (letter) | — | 0x22E3D | SELF-USE | Read letter |
| 9 | 358 (merchant) | 8 (secret_code) | 0x22E51 | HOTSPOT+ITEM | Trade secret code book at merchant stand |
| 10 | 358 (merchant) | 4 (brick) | 0x22EA1 | HOTSPOT+ITEM | Use brick on merchant (rejected) |
| 11 | 63+63 (recipe) | — | 0x22FF7 | SELF-USE | Use recipe (cooking cutscene) |
| 12 | 373 (counter) | 60 (orange_soda) | 0x22EB5 | HOTSPOT+ITEM | Give orange soda at counter |
| 13 | 373 (counter) | 61 (cola) | 0x22EB5 | HOTSPOT+ITEM | Give cola at counter (same handler) |
| 14 | 373 (counter) | 62 (spicy_sauce) | 0x22EC0 | HOTSPOT+ITEM | Give spicy sauce at counter |
| 15 | 0+0 | — | 0x22F07 | SELF-USE | Use "nothing" item (guard check?) |
| 16 | 24+24 (ketchup) | — | 0x22F22 | SELF-USE | Use ketchup on hamburger |
| 17 | 34+34 | — | 0x22F7B | SELF-USE | Use item 34 on itself |
| 18 | 59+59 (recipe) | — | 0x22F96 | SELF-USE | Use recipe (get recipe book) |
| 19 | 17+17 | — | 0x22FD5 | SELF-USE | Use item 17 (talk with boss) |
| 20 | 64+64 (hamburger) | — | 0x23088 | SELF-USE | Use hamburger (feeding cutscene) |
| 21 | 83 (newspaper) + 461 (desk) | — | 0x23108 | ITEM+HOTSPOT | Give newspaper at desk (fight sequence) |
| 22 | 469 (travel_agency) + 76 | — | 0x231C9 | HOTSPOT+ITEM | Use item 76 at travel agency |
| 23 | 88+88 (computer) | — | 0x23310 | SELF-USE | Use computer (library computer screen) |
| 24 | 87+87 (museum_pass) | — | 0x2387E | SELF-USE | Look at museum pass |
| 25 | 84 (photo) + 503 | — | 0x23892 | ITEM+HOTSPOT | Use photo at Egypt photo spot |
| 26-28 | 85/86/90 + 506 (temple) | — | 0x2395D | ITEM+HOTSPOT | Give items at Egypt temple entrance |
| 29 | 99 + 506 (temple) | — | 0x2446C | ITEM+HOTSPOT | Use item 99 at Egypt temple |
| 30-31 | 91/92 + 601 (slave_1) | — | 0x239DD | ITEM+HOTSPOT | Give stone/mud (item 91=Egyptian stone, 92=mud) to first slave (room 41 pyramid). Animated stone-pass sequence. Counter [0x95D2] 0→3: at 2 slave sings (conv root 2), at 3 pyramid sticker + walkbox change (→5) written to disk. |
| 32 | 97+97 (fight_item) | — | 0x23F03 | SELF-USE | Use fight item (fight cutscene) |
| 33 | 614 (bazaar) + 86 (orange) | — | 0x23F83 | HOTSPOT+ITEM | Give oranges at bazaar |
| 34 | 617 (pyramid) + 76 | — | 0x2413E | HOTSPOT+ITEM | Use item 76 at pyramid |
| 35 | 98+98 | — | 0x241E8 | SELF-USE | Use item 98 on itself |
| 36 | 86 (orange) + 500 (egypt_merch) | — | 0x24245 | ITEM+HOTSPOT | Trade oranges with Egypt merchant |
| 37 | 81 + 506 (temple) | — | 0x2395D | ITEM+HOTSPOT | Give item 81 at Egypt temple |
| 38 | 84+84 (photo) | — | 0x2448A | SELF-USE | Look at Egypt photo |
| 39 | 650 (final) + 100 | — | 0x2454C | HOTSPOT+ITEM | Use item 100 at final location |
| 40 | 101+101 | — | 0x2462B | SELF-USE | Use item 101 on itself |
| 41 | 108+108 | — | 0x2464E | SELF-USE | Use item 108 (mini-game/screen) |
| 42 | 109+109 | — | 0x246BA | SELF-USE | Use item 109 (mini-game/screen) |
| 43 | 95+95 (CD_player) | — | 0x246F4 | SELF-USE | CD Player / Soundtrack screen |
| 44 | 96+96 (art_gallery) | — | 0x24ED7 | SELF-USE | Background Art Gallery viewer |
| 45-78 | 11-47 self-use (store items) | — | 0x25471 | SELF-USE | Store-bought item descriptions |
| 79-112 | 11-47 + 358 (merchant) | — | 0x25525 | ITEM+HOTSPOT | Give store items to Egypt merchant |

---

## Handler Details

### 0x227B2 — Use Credit Card on ATM (281+2)
**Size**: 35 bytes, 12 instructions | **Tags**: DIALOG, SIMPLE

**Behavior**: Checks flag at `[0x495C4]`. If flag is not set, reads text pointer from `[0x4B9E0]` and calls `display_text_with_voice`. This is the ATM withdrawal — when the boss has deposited money, Alfred gets a special withdrawal; otherwise, he gets 1000 pesetas bills (up to 13 max).

**Call flow**:
```
if (flag_0x495C4 == 0):
    display_text_with_voice(text_at_0x4B9E0)
```

**ScummVM**: Implemented as `useCardWithATM` — checks `FLAG_JEFE_INGRESA_PASTA`, adds item 75 or item 5 (1000 pts bill).

---

### 0x2284B — Throw Brick at Shop Window (294+4) ⭐
**Size**: 684 bytes, 136 instructions | **Tags**: DIALOG, REMOVE_ITEM, ANIMATION, AUDIO, COMPLEX

**Behavior**: This is the most extensively analyzed combination. Alfred throws the brick at the window, breaking it:

1. `process_game_state` — prepares game state
2. `setup_alfred_frame_from_state` — position Alfred for throw
3. **Brick throw animation loop**: `render_scene` in loop, moving sprite 7 (brick projectile) upward toward window
4. `load_sticker_offset_table_from_alfred2` — load sticker data for broken window
5. `play_ambient_sound` — play glass breaking sound effect
6. File I/O: writes sticker data to ALFRED.1 (broken window graphics, sticker 11)
7. Two calls to `sub_1846A` — likely `display_npc_text_at_position` (NPC shouts from inside)
8. `display_text_with_voice` — Alfred's response ("Yo me voy")
9. `remove_inventory_item` — removes brick from inventory

**Constants**: 71 (sticker), 70 (sticker), 3483 (ALFRED.7 offset?), 25 (target Y?), 340 (text index), 58 (sprite)

**ScummVM**: Implemented as `useBrickWithWindow` — plays throwing animation, adds sticker 11 (broken window), plays SFX, shows dialog sequence (QUEHASIDOESO, QUIENANDAAHI, YOMEVOY), sets `FLAG_TIENDA_ABIERTA`, removes brick.

---

### 0x22AF7 — Use Brick on Storefront (295+4)
**Size**: 14 bytes, 6 instructions | **Tags**: SIMPLE

**Behavior**: Very short handler. Just calls `display_text_with_voice` (window is too thick / wouldn't notice from outside).

**ScummVM**: Implemented as `useBrickWithShopWindow` — says `NOSE_ENTERARIA`.

---

### 0x22B0B — Plug Cord into Socket (315+6)
**Size**: 38 bytes, 14 instructions | **Tags**: DIALOG, SIMPLE

**Behavior**: Checks a flag. If not set, shows dialog text. Otherwise proceeds with plugging the cord.

**Call flow**:
```
display_text_with_voice(text)  // conditional
```

**ScummVM**: Implemented as `useCordWithPlug` — checks sticker 18 (plug cover open), then checks `FLAG_CABLES_PUESTOS`.

---

### 0x22BF9 — Show ID to Museum Guard (309+1)
**Size**: 95 bytes, 27 instructions | **Tags**: DIALOG, CONVERSATION, NPC_DIALOG

**Behavior**: Multi-step guard interaction. Checks conversation state, calls dialog sequence:

**Call flow**:
```
play_get_naked_easter_egg(...)     // NPC dialog
display_text_with_voice(text)      // Alfred's line
update_conversation_state(room, npc, branch)
```

**ScummVM**: Implemented as `giveIdToGuard` — checks `FLAG_GUARDIA_PIDECOSAS` and `FLAG_GUARDIA_DNI_ENTREGADO`.

---

### 0x22C58 — Bribe Museum Guard (309+5)
**Size**: 105 bytes, 32 instructions | **Tags**: DIALOG, REMOVE_ITEM, CONVERSATION, NPC_DIALOG

**Behavior**: Similar to showing ID. Checks flags, shows dialog, removes 1000 pts bill, updates conversation state.

**Call flow**:
```
play_get_naked_easter_egg(...)     // NPC dialog
display_text_with_voice(text)      // Alfred's line  
remove_inventory_item()            // remove money
update_conversation_state(room, npc, branch)
```

**ScummVM**: Implemented as `giveMoneyToGuard` — checks `FLAG_SOBORNO_PORTERO`, removes item 5.

---

### 0x22CC1 — Place Amulet on Statue (353+7) ⭐
**Size**: 335 bytes, 79 instructions | **Tags**: DIALOG, REMOVE_ITEM, ANIMATION, CONVERSATION, AUDIO

**Behavior**: Complex cutscene. Places amulet on statue base, triggers palette fade effect, NPC conversation:

**Call flow**:
```
setup_alfred_frame_from_state()
render_scene()
load_sticker_offset_table_from_alfred2()  // sticker 24 (amulet on statue)
play_ambient_sound()           // atmospheric sound
remove_inventory_item()        // remove amulet
update_conversation_state()    // trigger statue dialog
init_or_stop_sound()
set_vga_mode()
play_dialog_sound_effect()     // sub_1BD53 (unknown)
display_text_with_voice()
update_conversation_state()
```

**ScummVM**: Implemented as `useAmuletWithStatue` — adds sticker 24, removes item 7, updates root disable states, calls `animateStatuePaletteFade()`.

---

### 0x22E10 — Give Secret Code to Librarian (347+8)
**Size**: 45 bytes, 15 instructions | **Tags**: DIALOG, NPC_DIALOG, SIMPLE

**Behavior**: Gives the secret code book to the librarian. Shows dialog, librarian gives recipe book in return.

**Call flow**:
```
play_get_naked_easter_egg(...)     // librarian speaks
display_text_with_voice(text)      // Alfred's line
```

**ScummVM**: Implemented as `giveSecretCodeToLibrarian` — says `REGALO_LIBRO_RECETAS`, removes item 8, adds item 59.

---

### 0x22E3D — Read Letter (9+9)
**Size**: 14 bytes, 6 instructions | **Tags**: SIMPLE

**Behavior**: Self-use of letter. Very short — reads text pointer and calls display. Shows the letter contents.

---

### 0x22E51 — Trade Secret Code at Merchant (358+8)
**Size**: 80 bytes, 28 instructions | **Tags**: REMOVE_ITEM, ADD_ITEM, NPC_DIALOG

**Behavior**: Egypt merchant trade sequence. Removes secret code book and adds new item:

**Call flow**:
```
load_sticker_offset_table_from_alfred2()
remove_inventory_item()
play_get_naked_easter_egg(...)    // merchant dialog
process_inventory_action(item)    // get new item
play_get_naked_easter_egg(...)    // more dialog
```

---

### 0x22EA1 — Use Brick on Merchant (358+4)
**Size**: 14 bytes, 6 instructions | **Tags**: SIMPLE

**Behavior**: Alfred tries to use brick on Egypt merchant. Short rejection text.

---

### 0x22EB5 — Give Drink at Counter (373+60, 373+61)
**Size**: 11 bytes, 5 instructions | **Tags**: SIMPLE

**Behavior**: Shared handler for giving orange soda or cola at McDonald's counter. Very short — just a text display.

---

### 0x22EC0 — Give Spicy Sauce at Counter (373+62)
**Size**: 71 bytes, 19 instructions | **Tags**: AUDIO

**Behavior**: Uses spicy sauce on the hamburger at the counter. Involves sound effect playback.

**Call flow**:
```
play_ambient_sound()
file_seek() / file_write()    // persist state changes
```

**ScummVM**: Related to `useSpicySauceWithBurger` — sets `FLAG_PUESTA_SALSA_PICANTE`.

---

### 0x22F07 — Self-use Item 0 (0+0)
**Size**: 27 bytes, 9 instructions | **Tags**: SIMPLE

**Behavior**: Placeholder entry for "no item". Calls `sub_1BB21` — possibly checks guard state or runs a default interaction.

---

### 0x22F22 — Use Ketchup (24+24)
**Size**: 91 bytes, 25 instructions | **Tags**: DIALOG, CONVERSATION

**Behavior**: Uses ketchup on the hamburger. Checks conditions and may advance conversation state:

**Call flow**:
```
sub_1BB21(...)                     // unknown check
display_text_with_voice(text)
sub_1BB21(...)
update_conversation_state()
```

---

### 0x22F7B — Self-use Item 34 (34+34)
**Size**: 27 bytes, 9 instructions | **Tags**: SIMPLE

**Behavior**: Short handler for self-examining item 34 (keys?). Calls `sub_1BB21`.

---

### 0x22F96 — Use Recipe (59+59)
**Size**: 62 bytes, 18 instructions | **Tags**: ADD_ITEM, SIMPLE

**Behavior**: Uses the recipe (recipe book) on itself. Adds a new item — likely converting recipe to usable form:

**Call flow**:
```
process_inventory_action(item)    // add derived item
sub_1BB21(...)
```

---

### 0x22FD5 — Self-use Item 17 (17+17)
**Size**: 34 bytes, 10 instructions | **Tags**: SIMPLE

**Behavior**: Uses item 17 (talk with boss) on itself. Short handler with one unknown call.

---

### 0x22FF7 — Use Recipe for Cooking (63+63) ⭐
**Size**: 145 bytes, 42 instructions | **Tags**: ANIMATION, CONVERSATION, LOAD_GRAPHICS

**Behavior**: Major cutscene — Alfred uses the recipe from the kitchen drawer. Loads special graphics, plays cooking animation, advances conversation:

**Call flow**:
```
draw_cursor_to_screen()
render_menu_screen()
load_room_graphics_and_palette_dynamic(room)    // cooking scene bg
wait_or_process_input()
setup_alfred_frame_from_state()
render_scene()
update_conversation_state()
set_vga_palette()
sub_1BC3A(...)                // display animation/dialog
```

---

### 0x23088 — Use Hamburger (64+64)
**Size**: 128 bytes, 37 instructions | **Tags**: ANIMATION, LOAD_GRAPHICS

**Behavior**: Uses the hamburger on itself — feeding sequence. Loads special graphics:

**Call flow**:
```
draw_cursor_to_screen()
render_menu_screen()
load_room_graphics_and_palette_dynamic(room)
wait_or_process_input()
setup_alfred_frame_from_state()
render_scene()
set_vga_palette()
sub_1BC3A(...)
```

---

### 0x23108 — Give Newspaper at Desk (83+461) ⭐
**Size**: 193 bytes, 43 instructions | **Tags**: REMOVE_ITEM, ANIMATION, FIGHT, WALK

**Behavior**: Gives newspaper at the newspaper desk, triggering a fight sequence:

**Call flow**:
```
remove_inventory_item()
play_fight_animation()         // fight with boss
play_fight_animation()         // second round?
walk_to_target_and_execute_queued_action()
setup_alfred_frame_from_state()
render_scene()
load_sticker_offset_table_from_alfred2()
```

---

### 0x231C9 — Travel Agency Sequence (469+76) ⭐
**Size**: 351 bytes, 85 instructions | **Tags**: DIALOG, REMOVE_ITEM, ADD_ITEM, ROOM_CHANGE, CONVERSATION, NPC_DIALOG, FADE, AUDIO, FIGHT

**Behavior**: Complex multi-phase travel sequence at the travel agency. This is one of the most involved handlers with nearly every game mechanic:

**Call flow**:
```
display_text_with_voice()
remove_inventory_item()
process_inventory_action(item)
fade_palette_to_black()
play_fight_animation()
play_cd_audio_track()
play_ambient_sound()            // travel music
init_or_stop_sound()
fade_cd_audio()
load_room_and_init_alfred()     // arrive at destination
update_conversation_state()
play_get_naked_easter_egg(...)
sub_26FAB(...)                  // unknown
```

---

### 0x23310 — Library Computer Screen (88+88) ⭐⭐
**Size**: 1375 bytes, 334 instructions | **Tags**: DIALOG, ROOM_CHANGE, ANIMATION, FADE, AUDIO, LOAD_GRAPHICS, COMPLEX

**Behavior**: The **largest handler** — the entire library computer system. Loads the computer interface, handles book search, memorization, and return:

**Call flow** (key calls only):
```
load_room_graphics_and_palette_dynamic()      // computer UI background
draw_cursor_to_screen()
render_menu_screen()
blit_image_to_screen() × many
file_seek() → file_read() → decompress_rle_block()   // load UI graphics from ALFRED.7
wait_or_process_input()         // main input loop
render_scene()
display_text_with_voice()       // search results
set_vga_palette()
present_frame_to_screen()
blit_with_transparency_check()
allocate_memory() / play_sound()
fade_palette_to_black()
load_room_and_init_alfred()     // exit computer
```

**See also**: `LIBRARY_COMPUTER_DOCUMENTATION.md` for complete system analysis.

---

### 0x2387E — Look at Museum Pass (87+87)
**Size**: 14 bytes, 6 instructions | **Tags**: SIMPLE

**Behavior**: Very short — displays text describing the museum pass.

---

### 0x23892 — Use Photo at Egypt Spot (84+503)
**Size**: 128 bytes, 30 instructions | **Tags**: REMOVE_ITEM, ANIMATION, CONVERSATION

**Behavior**: Takes a photo at the Egypt photo spot. Involves animation and conversation state change:

**Call flow**:
```
remove_inventory_item()
check_sprite_hover_and_trigger_conversation()
setup_alfred_frame_from_state()
render_scene()
update_conversation_state()
```

---

### 0x2395D — Give Egyptian Offering (85/86/90/81 + 506) 
**Size**: 128 bytes, 31 instructions | **Tags**: REMOVE_ITEM, ADD_ITEM

**Behavior**: Shared handler for giving various items at the Egypt temple entrance. Removes the given item and may add a new one:

**Call flow**:
```
remove_inventory_item()
sub_23E74(...)                 // unknown (in handler region)
sub_2662D(...)                 // unknown
process_inventory_action(item) // receive new item
```

Used by 5 different item+temple combinations (items 85, 86, 90, 81 + hotspot 506).

---

### 0x239DD — Give Stone to First Slave (Items 91/92 → Extra 601, Room 41) ⭐
**Size**: 1175 bytes, 282 instructions | **Tags**: REMOVE_ITEM, ANIMATION, CONVERSATION, NPC_DIALOG, AUDIO, FIGHT, COMPLEX

**Items**: 91 = "Una piedra egipcia para construir piramides" (Egyptian stone), 92 = "Un poco de barro" (mud/clay) — both treated identically.
**Hotspot**: Extra 601 = first slave in room 41 (pyramid construction scene).

**Behavior**: Complete pyramid stone-passing puzzle. Player gives a stone to the first slave, triggering an animated stone-passing sequence tracked by a delivery counter.

**Phase 1 — Item removal**:
- Checks for item 91 via `find_item_in_room_table(91)` → removes if found
- Checks for item 92 via `find_item_in_room_table(92)` → removes if found

**Phase 2 — Sprite loading**:
- Allocate 0x158F8-byte buffer → decompress sprite from ALFRED.1 offset `0x167B54` (0x9728 bytes) via `decompress_rle_block` → stone-catch animation
- Allocate 0xC180-byte buffer → decompress sprite from ALFRED.1 offset `0x17127C` (0x3824 bytes) → secondary slave animation

**Phase 3 — Fight/pass animation**:
- `play_fight_animation(file_offset=0x186DBC, size=0x24420, alfred_x=0, overlay_h=0x12A, w=0xD0, h=0x66, frames=7, mode=2, compressed=0, fullscreen=0, callback=0)` — 7-frame 208×102 stone-passing animation

**Phase 4 — Sound loop**:
- `play_ambient_sound` with handle from `[0x13204]` (channel 3), loop until `play_or_check_sound` returns done
- `render_scene` + `process_game_state` + `setup_alfred_frame_from_state` each iteration

**Phase 5 — Text and slave animation**:
- `play_ambient_sound` (channel -1, vol 0x20)
- `display_text_with_character_animation([0xBB10])` — slave's reaction text
- Modify `room_sprite_data_ptr+0x5E` = new sprite data (stone-passing), animate until frame counter (`+0x78`) reaches 6

**Phase 6 — Post-animation & counter**:
- Stone delivery counter `[0x95D2]`:
  - If `< 3`: increment
  - If `== 2` after increment: `update_conversation_state(room=41, arg2=0, branch=2)` → slave advances to conversation root #2 (starts singing: "¡ Deesde Santuurce a Bilbaooo...!")
  - If `== 3` after increment: **permanent state changes** (see below)

**Phase 7 — Third stone (count=3, permanent)**:
- Second slave animation until frame counter (`+0x78`) reaches 2
- Set `room_sprite_data_ptr[+0x79] = 0xFF` (hide/complete slave sprite)
- `write_data_to_alfred1` — persist slave "done" state
- Set `[0xACEC] = 1` (global pyramid_stone_quest_complete flag)
- `load_and_render_sticker_from_alfred6(offset=0x696AD, pos=0x2C1C)` — render pyramid sticker
- Set `room_sprite_data_ptr[+0x213] = 5` — change walkbox count to 5 (new pyramid layout)
- `write_data_to_alfred1` — persist walkbox count

**Call flow** (key calls):
```
find_item_in_room_table(91) → remove_inventory_item(91)
find_item_in_room_table(92) → remove_inventory_item(92)
allocate_memory(0x158F8) + allocate_memory(0xC180)
file_seek/file_read + decompress_rle_block ×2   // load stone-pass sprites from ALFRED.1
play_fight_animation(0x186DBC, 7 frames, 208×102)  // stone-toss animation
play_ambient_sound ×2
display_text_with_character_animation([0xBB10])   // slave reaction
render_scene loop (wait for anim frame==6)
update_conversation_state(41, 0, 2)               // if counter==2: slave sings
// if counter==3:
load_and_render_sticker_from_alfred6(0x696AD)     // pyramid grows
write_data_to_alfred1 ×4                          // persist slave state + walkbox count
```

---

### 0x23F03 — Fight Sequence (97+97)
**Size**: 128 bytes, 29 instructions | **Tags**: ANIMATION, CONVERSATION, LOAD_GRAPHICS

**Behavior**: Uses the fight item — triggers a fight cutscene:

**Call flow**:
```
draw_cursor_to_screen()
render_menu_screen()
load_room_graphics_and_palette_dynamic()
wait_or_process_input()
setup_alfred_frame_from_state()
render_scene()
update_conversation_state()
sub_1BC3A(...)
```

---

### 0x23F83 — Give Oranges at Bazaar (614+86)
**Size**: 443 bytes, 97 instructions | **Tags**: REMOVE_ITEM, ADD_ITEM, AUDIO

**Behavior**: Gives oranges at the Egypt bazaar fruit stand. Gets a new item in return:

**Call flow**:
```
remove_inventory_item()
process_inventory_action(item)
play_ambient_sound() × multiple
file_seek() / file_write()     // persist sticker changes
```

---

### 0x2413E — Use Item at Pyramid (617+76)
**Size**: 90 bytes, 22 instructions | **Tags**: REMOVE_ITEM

**Behavior**: Uses item 76 at the pyramid entrance. Removes the item and modifies game state.

**Call flow**:
```
remove_inventory_item()
```

---

### 0x241E8 — Self-use Item 98 (98+98)
**Size**: 93 bytes, 22 instructions | **Tags**: (state change)

**Behavior**: Uses item 98 on itself. Modifies memory and calls `memcpy_wrapper`.

---

### 0x24245 — Trade Oranges with Egypt Merchant (86+500) ⭐
**Size**: 551 bytes, 125 instructions | **Tags**: REMOVE_ITEM, ADD_ITEM, ANIMATION, CONVERSATION, NPC_DIALOG, COMPLEX

**Behavior**: Multi-phase trade with the Egypt merchant:

**Call flow**:
```
remove_inventory_item()
play_get_naked_easter_egg(...)    // merchant negotiation
process_inventory_action(item)    // get new item
setup_alfred_frame_from_state()
render_scene() × loop
update_conversation_state()
play_get_naked_easter_egg(...)    // more dialog
```

---

### 0x2446C — Use Item 99 at Temple (99+506)
**Size**: 30 bytes, 12 instructions | **Tags**: REMOVE_ITEM, SIMPLE

**Behavior**: Short handler. Removes item 99 at the Egypt temple entrance.

---

### 0x2448A — Look at Egypt Photo (84+84)
**Size**: 403 bytes, 97 instructions | **Tags**: ANIMATION, LOAD_GRAPHICS

**Behavior**: Views the Egypt photo — loads special graphics and displays the photo:

**Call flow**:
```
load_room_graphics_and_palette_dynamic()
outport_byte() × multiple       // VGA register writes
wait_or_process_input()
render_scene()
set_vga_palette()
```

---

### 0x2454C — Final Location Sequence (650+100)
**Size**: 35 bytes, 12 instructions | **Tags**: (minimal)

**Behavior**: Uses item 100 at the final location (hotspot 650). Short handler — likely end-game trigger.

---

### 0x2462B — Self-use Item 101 (101+101)
**Size**: 35 bytes, 12 instructions | **Tags**: DIALOG, SIMPLE

**Behavior**: Short dialog handler for examining item 101.

---

### 0x2464E — Mini-game Screen Item 108 (108+108)
**Size**: 869 bytes, 211 instructions | **Tags**: REMOVE_ITEM, ADD_ITEM, ANIMATION, AUDIO, LOAD_GRAPHICS, COMPLEX

**Behavior**: Launches a mini-game or special screen for item 108. Loads graphics, plays audio, animation loop:

**Call flow** (key calls):
```
load_room_graphics_and_palette_dynamic()
draw_cursor_to_screen()
render_menu_screen()
blit_image_to_screen() × multiple
file_seek() → file_read() → decompress_rle_block()
wait_or_process_input()
render_scene()
play_ambient_sound()
remove_inventory_item()
process_inventory_action(item)
set_vga_palette()
```

---

### 0x246BA — Mini-game Screen Item 109 (109+109)
**Size**: 761 bytes, 187 instructions | **Tags**: ANIMATION, AUDIO, LOAD_GRAPHICS, COMPLEX

**Behavior**: Similar to item 108 — launches a special screen/mini-game:

**Call flow**:
```
load_room_graphics_and_palette_dynamic()
draw_cursor_to_screen()
render_menu_screen()
blit_image_to_screen()
file_seek() → file_read() → decompress_rle_block()
wait_or_process_input()
render_scene()
play_ambient_sound()
set_vga_palette()
```

---

### 0x246F4 — CD Player / Soundtrack Screen (95+95) ⭐⭐
**Size**: 703 bytes, 173 instructions | **Tags**: ANIMATION, AUDIO, LOAD_GRAPHICS, COMPLEX

**Behavior**: Opens the CD audio player interface. Loads room 14 as background, displays CD controls from ALFRED.7:

**Call flow**:
```
load_room_graphics_and_palette_dynamic(14)
draw_cursor_to_screen()
render_menu_screen()
file_seek(ALFRED.7, 0x21CB68) → file_read(12658) → decompress_rle_block()  // CD controls
file_seek(ALFRED.7, 0x2207E8) → file_read(18) → decompress_rle_block()     // additional graphic
blit_image_to_screen()
room_number_to_ascii()            // track number display
memcpy_wrapper()
init_graphics_or_mode()
render_character_to_screen()
LOOP:
    wait_or_process_input()       // input loop
    render_scene()
    play_cd_audio_track() / fade_cd_audio()
END LOOP
init_or_stop_sound()
set_vga_mode() → set_vga_palette()
```

**See also**: `ITEMS_95_96_INVESTIGATION.md` for detailed byte-level analysis.

---

### 0x24ED7 — Background Art Gallery (96+96) ⭐⭐
**Size**: 576 bytes, 151 instructions | **Tags**: ROOM_CHANGE, ANIMATION, LOAD_GRAPHICS, COMPLEX

**Behavior**: Opens the background art gallery viewer. Loads backgrounds from ALFRED.7:

**Call flow**:
```
file_seek(ALFRED.7, 0x22DF86) → file_read() → decompress_rle_block()
file_seek(ALFRED.7, 0x30A6E0) → file_read()
load_room_graphics_and_palette_dynamic()
draw_cursor_to_screen()
render_menu_screen()
blit_image_to_screen() × 2
render_character_to_screen()
LOOP:
    wait_or_process_input()
    render_scene() / load_room_and_init_alfred()
END LOOP
```

**See also**: `ITEMS_95_96_INVESTIGATION.md`.

---

### 0x25471 — Store Item Self-Use (items 11-47)
**Size**: ~180 bytes | **Tags**: DESCRIPTION

**Behavior**: Shared handler for all store-bought items (guitar, fish, teddy bear, discs, monkey brain, books, palette, candy, conch, hat, cord, amulet, etc.). Calls `display_text_description` and `trigger_dialog_or_action` to show item description text.

**Used by**: Items 11-16, 18-23, 25-33, 35-47 (34 entries).

---

### 0x25525 — Give Store Item to Egypt Merchant (items 11-47 + 358)
**Size**: ~40 bytes | **Tags**: REMOVE_ITEM, SIMPLE

**Behavior**: Shared handler for giving any store-bought item to the Egypt merchant (hotspot 358). Removes the item from inventory and decrements a counter at `[0x495BE]`.

**Used by**: Items 11-16, 18-23, 25-33, 35-47 paired with hotspot 358 (34 entries).

---

## Summary Statistics

### Entry Type Breakdown
| Type | Count |
|------|-------|
| SELF-USE | 52 |
| ITEM+HOTSPOT | 44 |
| HOTSPOT+ITEM | 17 |

### Handler Size Distribution (Top 10)
| Handler | Size | Instructions | Primary Use |
|---------|------|-------------|-------------|
| 0x23310 | 1375 bytes | 334 | Library computer system |
| 0x239DD | 1175 bytes | 282 | Egypt market haggling |
| 0x2464E | 869 bytes | 211 | Mini-game item 108 |
| 0x246BA | 761 bytes | 187 | Mini-game item 109 |
| 0x246F4 | 703 bytes | 173 | CD player screen |
| 0x2284B | 684 bytes | 136 | Brick + window |
| 0x24ED7 | 576 bytes | 151 | Art gallery viewer |
| 0x24245 | 551 bytes | 125 | Orange trade w/merchant |
| 0x23F83 | 443 bytes | 97 | Bazaar fruit trade |
| 0x2448A | 403 bytes | 97 | View Egypt photo |

### Most Called Functions from Handlers
| Function | Call Count |
|----------|-----------|
| render_scene | 29 |
| file_seek | 26 |
| file_write | 25 |
| remove_inventory_item | 18 |
| setup_alfred_frame_from_state | 17 |
| wait_or_process_input | 17 |
| display_text_with_voice | 13 |
| file_read | 13 |
| blit_image_to_screen | 13 |
| update_conversation_state | 12 |
| decompress_rle_block | 12 |

### ScummVM Implementation Status
| Handler | Item+Hotspot | ScummVM Function | Status |
|---------|-------------|------------------|--------|
| 0x227B2 | 2+281 (card+ATM) | `useCardWithATM` | ✅ Implemented |
| 0x2284B | 4+294 (brick+window) | `useBrickWithWindow` | ✅ Implemented |
| 0x22AF7 | 4+295 (brick+storefront) | `useBrickWithShopWindow` | ✅ Implemented |
| 0x22B0B | 6+315 (cord+plug) | `useCordWithPlug` | ✅ Implemented |
| 0x22BF9 | 1+309 (ID+guard) | `giveIdToGuard` | ✅ Implemented |
| 0x22C58 | 5+309 (money+guard) | `giveMoneyToGuard` | ✅ Implemented |
| 0x22CC1 | 7+353 (amulet+statue) | `useAmuletWithStatue` | ✅ Implemented |
| 0x22E10 | 8+347 (code+librarian) | `giveSecretCodeToLibrarian` | ✅ Implemented |
| 0x22EC0 | 62+373 (spicy+counter) | `useSpicySauceWithBurger` | ✅ Implemented |
| 0x22E3D | 9+9 (letter self-use) | — | ❌ Not implemented |
| 0x22E51 | 8+358 (code+merchant) | — | ❌ Not implemented |
| 0x22EA1 | 4+358 (brick+merchant) | — | ❌ Not implemented |
| 0x22EB5 | 60/61+373 (drinks) | — | ❌ Not implemented |
| 0x22F07 | 0+0 (null) | — | ❌ Not implemented |
| 0x22F22 | 24+24 (ketchup) | — | ❌ Not implemented |
| 0x22F7B | 34+34 | — | ❌ Not implemented |
| 0x22F96 | 59+59 (recipe) | — | ❌ Not implemented |
| 0x22FD5 | 17+17 | — | ❌ Not implemented |
| 0x22FF7 | 63+63 (cooking) | — | ❌ Not implemented |
| 0x23088 | 64+64 (hamburger) | — | ❌ Not implemented |
| 0x23108 | 83+461 (newspaper) | — | ❌ Not implemented |
| 0x231C9 | 76+469 (travel agency) | — | ❌ Not implemented |
| 0x23310 | 88+88 (computer) | — | ❌ Not implemented |
| 0x2387E | 87+87 (museum pass) | — | ❌ Not implemented |
| 0x23892 | 84+503 (photo spot) | — | ❌ Not implemented |
| 0x2395D | 85/86/90/81+506 (temple) | — | ❌ Not implemented |
| 0x239DD | 91/92+601 (slave_1, room 41) | — | ✅ Implemented — `giveStoneToSlaves`: removes item 91 or 92, plays 7-frame animation, counter FLAG_ESCLAVO_CONTADOR_PIEDRAS (0→3): at 2: setCurrentRoot(41,2,0) (slave sings). At 3: addSticker(116,PERM) + FLAG_PIEDRAS_COGIDAS. TODO: slave reply text [0xBB10], sprite frame-6 wait, 5 walkboxes at count==3. |
| 0x23F03 | 97+97 (fight) | — | ❌ Not implemented |
| 0x23F83 | 86+614 (bazaar) | — | ❌ Not implemented |
| 0x2413E | 76+617 (pyramid) | — | ❌ Not implemented |
| 0x241E8 | 98+98 | — | ❌ Not implemented |
| 0x24245 | 86+500 (trade oranges) | — | ❌ Not implemented |
| 0x2446C | 99+506 (temple) | — | ❌ Not implemented |
| 0x2448A | 84+84 (view photo) | — | ❌ Not implemented |
| 0x2454C | 100+650 (final) | — | ❌ Not implemented |
| 0x2462B | 101+101 | — | ❌ Not implemented |
| 0x2464E | 108+108 (mini-game) | — | ❌ Not implemented |
| 0x246BA | 109+109 (mini-game) | — | ❌ Not implemented |
| 0x246F4 | 95+95 (CD player) | — | ❌ Not implemented |
| 0x24ED7 | 96+96 (art gallery) | — | ❌ Not implemented |
| 0x25471 | items 11-47 self-use | — | ❌ Not implemented |
| 0x25525 | items 11-47+358 | — | ❌ Not implemented |

**Status**: 9/42 handlers implemented (21%)

---

## Unidentified Functions

These call targets in the handler region have no Ghidra function definitions:

| Address | Called From | Likely Purpose |
|---------|-----------|----------------|
| 0x1846A | 0x2284B (brick+window) × 2 | Display NPC text at screen position |
| 0x1BB21 | 9 handlers | Unknown check/dialog function |
| 0x1BC3A | 6 handlers | Display animation or dialog sequence |
| 0x1BD53 | 0x22CC1 (amulet+statue) | Play dialog sound effect |
| 0x23E74 | 0x2395D (temple offerings) | Unknown state handler (in handler region) |
| 0x2662D | 3 handlers | Unknown (in handler region) |
| 0x26FAB | 0x231C9 (travel agency) | Unknown |

---

## Reproduction Guide

### Finding the Combination Table
```python
import struct
exe = open("files/JUEGO.EXE", "rb").read()
# Search for known entry: item1=294, item2=4, ptr=0x1284B (brick+window)
pattern = struct.pack('<HHI', 294, 4, 0x1284B)
pos = exe.find(pattern)  # Returns 0x4B320 (2nd entry)
# Table starts 8 bytes before at 0x4B318
```

### Reading All Entries
```python
off = 0x4B318
while True:
    id1 = struct.unpack_from('<H', exe, off)[0]
    if id1 == 0xFFFF: break
    id2 = struct.unpack_from('<H', exe, off+2)[0]
    ptr = struct.unpack_from('<I', exe, off+4)[0]
    ghidra_addr = ptr + 0x10000
    print(f"{id1}+{id2} -> 0x{ghidra_addr:05X}")
    off += 8
```

### Verifying Handler Validity
All valid handlers start with Watcom C prologue: `68 xx 00 00 00 E8` (PUSH stack_size; CALL __STK).
```python
foff = ghidra_addr - 0x10000 + 0x14200
assert exe[foff] == 0x68 and exe[foff+5] == 0xE8
```

### Raw Analysis Script
See `analyze_combo_handlers_v2.py` for the complete Capstone-based disassembly tool that produces `combo_handler_analysis_v2.txt` (4397 lines of annotated disassembly for all 42 handlers).
