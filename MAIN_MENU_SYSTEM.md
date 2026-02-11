# Alfred Pelrock - Main Menu System Documentation

## Overview

The main menu is accessed by **right-clicking** during gameplay. It displays:
- Alfred's character portrait
- Up to **4 inventory item icons** (scrollable with arrows)
- Menu buttons: Save Game, Load Game, Sounds, Exit to DOS
- A question mark button (credits)

## Entry Point

- **Function**: `main_menu_handler` at `0x12918`
- **Called from**: `main_game_loop` at `0x1075e` when `is_in_menu` flag (`[0x4FB8D]`) is non-zero
- **Triggered by**: Right mouse button click during gameplay

## Menu Graphics Loading

The menu graphics are loaded **on demand** each time the menu opens:

```
1. Allocate 0x70CA bytes of memory
2. Seek to offset 0x30BA20 in ALFRED.1
3. Read 0x70CA bytes of menu graphics data
```

This contains all button graphics (normal + pressed states), the Alfred portrait icon, and the inventory item icon areas. Graphics offsets within this block are stored in tables at `0x48770`–`0x487B5`.

## Menu Structure

### Button Hit-Test Table (`0x486F8`)

The menu uses a table-driven hit-test system. Each entry is 10 bytes:

| Offset | Size | Field |
|--------|------|-------|
| +0 | 2 | X min (hitbox left) |
| +2 | 2 | Y min (hitbox top) |
| +4 | 1 | Width |
| +5 | 1 | Height |
| +6 | 4 | Handler function pointer |

**Entries 0–3 are inventory item icons (60×60). Entries 4–7 are menu action buttons (narrow text buttons). Entry 8 is a small icon button.** The table is terminated by `0xFFFF` sentinel.

### Button Indices

| Index | Element | Position | Size |
|-------|---------|----------|------|
| **0** | **Inventory item 1** (leftmost) | x=140, y=115 | 60×60 |
| **1** | **Inventory item 2** | x=222, y=107 | 60×60 |
| **2** | **Inventory item 3** | x=304, y=99 | 60×60 |
| **3** | **Inventory item 4** (rightmost) | x=386, y=91 | 60×60 |
| 4 | Menu button (e.g. Save) | x=132, y=188 | 75×23 |
| 5 | Menu button (e.g. Load) | x=134, y=222 | 72×25 |
| 6 | Menu button (e.g. Sounds) | x=134, y=259 | 72×25 |
| 7 | Menu button (e.g. Exit) | x=134, y=294 | 70×25 |
| 8 | Small icon button | x=217, y=293 | 32×32 |

The inventory icons (0–3) are arranged in a diagonal line going right-and-up. Menu action buttons (4–7) are stacked vertically on the left.

### Inventory Item Graphics Table (`0x48770`)

Each inventory item slot has a 14-byte (0x0E) entry:

| Offset | Size | Field |
|--------|------|-------|
| +0x00 | 4 | Normal-state graphic offset (in ALFRED.1 relative to 0x30BA20) |
| +0x04 | 4 | Pressed-state graphic offset |
| +0x08 | 2 | Icon width |
| +0x0C | 1 | X position |
| +0x0D | 1 | Y position |

## Click Flow

### Menu Action Buttons (index >= 4)

When the player clicks a **menu button** (Save, Load, Sounds, Exit):

```
1. render_menu_screen()     — redraw base menu
2. Blit PRESSED graphic for the clicked button
3. present_frame_to_screen()
4. play_ambient_sound(...)  — play generic click SFX from slot 0 (11ZZZZZZ.SMP)
5. process_game_state(2)    — wait ~2 frames (visual feedback delay)
6. Blit NORMAL graphic back (un-press the button)
7. draw_cursor_to_screen()
8. present_frame_to_screen()
9. Call handler function from menu_button_handler_table[button_index]
```

The click SFX slot is computed from the button index at `0x12B93`:

```asm
AND AL, 0xFC             ; Round down to group of 4
SUB EDX, 0x4             ; Subtract 4
SAR EAX, 0x1             ; Divide by 2
; For buttons 4-7: ((4 & 0xFC) - 4) / 2 = 0 → slot 0 (11ZZZZZZ.SMP)
; For button 8:    ((8 & 0xFC) - 4) / 2 = 2 → slot 2 (56ZZZZZZ.SMP)
```

### Inventory Item Icons (index < 4)

When the player clicks an **inventory item icon** (index 0–3):

```
1. render_menu_screen()     — redraw base menu (NO highlight, NO generic click SFX)
2. Call handler function from menu_button_handler_table[button_index]
```

The handler function (at `0x12DA7` for slot 0) performs the actual per-item logic:

```asm
; Inventory item handler at 0x12DA7:
0x12DCA: MOV AL, [inventory_slot_index]     ; which slot was clicked (0-3)
0x12DCF: CMP AL, [max_inventory_items]      ; bounds check
0x12DD5: JAE exit                           ; no item in slot → skip

0x12DDB: MOVZX ESI, AL
0x12DDE: MOV SI, [ESI*2 + inventory_array]  ; SI = actual item ID from inventory
0x12DE8: MOV BX, SI                         ; BX = item ID

; --- Load per-item sound ---
0x12DEB: MOV EAX, [EBX*4 + 0x490F8]        ; EAX = item_sound_filename_ptr_table[item_id]
0x12DF2: MOV EDX, 7                         ; sound slot 7 (on-demand item sounds)
0x12DF7: CALL load_sound_file               ; load from SONIDOS.DAT into slot 7

; --- Play per-item sound ---
0x12E20: CALL play_ambient_sound            ; play the item-specific sound from slot 7
```

**Each inventory item has its own sound effect**, loaded on-demand from `SONIDOS.DAT` into **slot 7**. The sound filename is looked up from a data-driven table indexed by item ID.

---

## Sound Effect System

### Sound Slot Architecture

| Slot Range | Loaded When | Freed When | Purpose |
|------------|-------------|------------|---------|
| **0–3** | Game startup | Never (until exit) | Global UI/system sounds |
| 4–6 | (unused) | — | Reserved |
| **7** | **On demand (item click)** | **Overwritten each click** | **Per-item inventory sound** |
| 8–16 | Room change | Room change | Room-specific event & ambient sounds |

### Global Startup Sounds (Slots 0–3)

Pre-loaded during `game_initialization` (at `0x10381`–`0x103B5`):

| Slot | Filename | Purpose |
|------|----------|---------|
| 0 | `11ZZZZZZ.SMP` | Menu button click SFX (for buttons 4–7 only) |
| 1 | `41ZZZZZZ.SMP` | UI/system sound |
| 2 | `56ZZZZZZ.SMP` | Button 8 click SFX / UI sound |
| 3 | `GATITOZZ.SMP` | Kitten meow |

These are loaded once and **never freed or replaced**.

### Per-Item Inventory Sounds (Slot 7)

**Different inventory items play different sounds.** Each of the 113 item IDs maps to a specific SMP filename via a data-driven lookup table.

#### Data Structures

- **`item_sound_filenames_inline`** at `0x407CB`: 113 entries, 13 bytes each (8-char filename + ".SMP\0")
- **`item_sound_filename_ptr_table`** at `0x490F8`: 113 entries, 4 bytes each (data-relative pointers to the inline strings above; add `0x40000` for Ghidra addresses)

#### Code Path (at `0x12DEB`)

```asm
MOV EAX, [EBX*4 + item_sound_filename_ptr_table]  ; get SMP filename for item
MOV EDX, 7                                          ; slot 7
CALL load_sound_file                                ; load from SONIDOS.DAT
; ... (setup Miles Sound System parameters) ...
CALL play_ambient_sound                             ; play the loaded sound
```

#### Item Sound Table (non-default entries only)

Items with `HOJASZZZ.SMP` use the default leaf-rustle sound; items with `11ZZZZZZ.SMP` use the generic click. The notable per-item sounds are:

| Item ID | Sound Filename | Description |
|---------|---------------|-------------|
| 0 | HOJASZZZ.SMP | Default (leaf rustle) |
| 1–3, 5, 9 | 11ZZZZZZ.SMP | Generic click |
| **4** | **GLASS1ZZ.SMP** | **Glass clink (brick)** |
| 6 | ELEC3ZZZ.SMP | Electric zap |
| 7 | REMATERL.SMP | Rematerialize |
| 8 | 81ZZZZZZ.SMP | (numbered SFX) |
| 10 | SSSHTZZZ.SMP | Shushing |
| **60–62** | **BOTEZZZZ.SMP** | **Bottle sound** |
| 63 | BELCHZZZ.SMP | Belch |
| 64 | BEAMZZZZ.SMP | Beam/ray |
| **65** | **ELVIS1ZZ.SMP** | **Elvis impression** |
| 66 | CAT_1ZZZ.SMP | Cat sound |
| 67 | BOOOOOIZ.SMP | Boing |
| 68 | DISCOSZZ.SMP | Disco music |
| 69 | MONORLZZ.SMP | Monorail |
| **73** | **CARACOLA.SMP** | **Seashell** |
| 76 | WATER_2Z.SMP | Water splash |
| 79 | EEEEKZZZ.SMP | Shriek |
| 80 | REMATERL.SMP | Rematerialize |
| 83 | ELVIS1ZZ.SMP | Elvis impression |
| 84 | RIMSHOTZ.SMP | Rimshot |
| 86 | WATER_2Z.SMP | Water splash |
| 87 | MOTOSZZZ.SMP | Motorcycle |
| 89 | TWANGZZZ.SMP | Twang |
| 91 | QUAKE2ZZ.SMP | Earthquake |
| 93 | SORBOZZZ.SMP | Slurp |
| 94 | BOTEZZZZ.SMP | Bottle sound |
| 95 | ELVIS1ZZ.SMP | Elvis impression |
| **100** | **LLAVESZZ.SMP** | **Keys jingling** |
| **104** | **EVLLAUGH.SMP** | **Evil laugh** |
| 106 | BURROLZZ.SMP | Donkey bray |
| 108, 110 | TWANGZZZ.SMP | Twang |
| 111 | ELVIS1ZZ.SMP | Elvis impression |
| **112** | **SEX3ZZZZ.SMP** | **Suggestive sound** |

27 unique sounds across 113 item IDs. Items 11–59 and 88, 96–98, 101 all use the default `HOJASZZZ.SMP`.

### Loading Mechanism (`load_sound_file` at `0x267DD`)

```c
void load_sound_file(char *filename, int slot) {
    if (!sound_enabled_flag) return;
    
    // 1. Find file in SONIDOS.DAT archive
    int archive_offset = find_sound_in_archive(filename);
    int file_size = get_sound_file_size(filename);
    
    // 2. Allocate Miles Sound System buffer and load data
    if (file_size != 0) {
        sound_slot_buffer_table[slot] = allocate_miles_sound_buffer(
            miles_driver_handle,       // Miles Sound System driver
            &sound_config,             // Sound configuration
            sound_driver_type          // Driver type flag
        );
    } else {
        sound_slot_buffer_table[slot] = 0;
    }
}
```

Sounds are stored in `SONIDOS.DAT`, a PACK archive. The file is opened once at startup (`open_sonidos_dat` at `0x2616B`), and individual sounds are extracted by filename lookup.

## Key Addresses

| Address | Name | Description |
|---------|------|-------------|
| `0x12918` | `main_menu_handler` | Entry point for menu |
| `0x12DA7` | *(inline, not a Ghidra function)* | Inventory slot 0 handler (loads & plays per-item sound) |
| `0x12FBB` | `exit_menu_and_restore_game` | Clean exit from menu |
| `0x267DD` | `load_sound_file` | Load SMP from SONIDOS.DAT into slot |
| `0x27CE1` | `play_ambient_sound` | Play sound from buffer (7 params, stdcall) |
| `0x407CB` | `item_sound_filenames_inline` | 113 inline SMP filename strings (13 bytes each) |
| `0x486F8` | `menu_button_hitbox_table` | Hit-test rectangles for buttons (9 entries) |
| `0x486FE` | `menu_button_handler_table` | Function pointers for button actions |
| `0x48770` | `menu_inv_normal_gfx_offsets` | Normal-state icon offsets |
| `0x48774` | `menu_inv_pressed_gfx_offsets` | Pressed-state icon offsets |
| `0x48778` | `menu_inv_icon_width` | Icon widths |
| `0x4877C` | `menu_inv_icon_x_pos` | Icon X positions |
| `0x4877D` | `menu_inv_icon_y_pos` | Icon Y positions |
| `0x487A8` | `menu_alfred_icon_gfx_offset` | Alfred portrait offset |
| `0x490F8` | `item_sound_filename_ptr_table` | 113-entry ptr table → SMP filenames (indexed by item ID) |
| `0x51751` | `menu_exit_requested` | Flag: menu should close |
| `0x51752` | `menu_exit_return_value` | Return value on menu exit |
| `0x53002` | `sound_driver_type` | Sound system enabled flag / driver type |
| `0x53204` | `miles_driver_handle` | Miles Sound System driver handle |
| `0x53214` | `sound_slot_buffer_table` | Array of 17 sound buffer handles |

## Ghidra Renames Applied

### Functions
| Address | Old Name | New Name |
|---------|----------|----------|
| `0x2616B` | `FUN_0002616b` | `open_sonidos_dat` |
| `0x2636B` | `FUN_0002636b` | `find_sound_in_archive` |
| `0x2631A` | `FUN_0002631a` | `get_sound_file_size` |
| `0x27B5A` | `FUN_00027b5a` | `allocate_miles_sound_buffer` |

### Data Labels
| Address | New Name |
|---------|----------|
| `0x407CB` | `item_sound_filenames_inline` |
| `0x486F8` | `menu_button_hitbox_table` |
| `0x486FE` | `menu_button_handler_table` |
| `0x48770` | `menu_inv_normal_gfx_offsets` |
| `0x48774` | `menu_inv_pressed_gfx_offsets` |
| `0x48778` | `menu_inv_icon_width` |
| `0x4877C` | `menu_inv_icon_x_pos` |
| `0x4877D` | `menu_inv_icon_y_pos` |
| `0x487A8` | `menu_alfred_icon_gfx_offset` |
| `0x487B0` | `menu_alfred_icon_height` |
| `0x487B2` | `menu_alfred_icon_width` |
| `0x487B4` | `menu_alfred_icon_x` |
| `0x487B5` | `menu_alfred_icon_y` |
| `0x48DD8` | `room_sound_filename_ptrs` |
| `0x490F8` | `item_sound_filename_ptr_table` |
| `0x51751` | `menu_exit_requested` |
| `0x51752` | `menu_exit_return_value` |
| `0x53002` | `sound_driver_type` |
| `0x53204` | `miles_driver_handle` |
| `0x53214` | `sound_slot_buffer_table` |
| `0x53274` | `sound_load_offset` |
| `0x53278` | `sound_load_reserved` |
| `0x5327C` | `sound_load_archive_offset` |
| `0x53284` | `sound_load_flags` |
| `0x53288` | `sound_load_file_size` |

### Variables (in `main_menu_handler`)
| Old Name | New Name |
|----------|----------|
| `iVar3` | `menu_gfx_buffer` |
| `local_18` | `button_index` |
| `iVar1` | `hitbox_table_offset` |
