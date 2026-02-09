# Items 95 and 96 Investigation - Complete Analysis

## Overview

This document analyzes inventory items 95 (CD Player/Soundtrack) and 96 (Background Book) in Alfred Pelrock, including how they are added to inventory and what happens when used on Alfred.

## Item Descriptions

| Item ID | Spanish Name | English Translation |
|---------|--------------|---------------------|
| 95 | Banda sonora de Alfred Pelrock | Soundtrack of Alfred Pelrock |
| 96 | Un album con las pantallas de Alfred Pelrock | An album with the screens of Alfred Pelrock |

These are **bonus/extras** items that let players view the game's soundtrack and background art.

## Item Combination Table Entry

The item combination table at `0x48118` contains self-use handlers for these items:

| Entry | Item1 | Item2 | Handler | Purpose |
|-------|-------|-------|---------|---------|
| 43 | 95 | 95 | 0x146f4 | Use CD Player on Alfred |
| 44 | 96 | 96 | 0x14ed7 | Use Background Book on Alfred |

### Handler Analysis

#### Handler 0x146f4 (Item 95 - CD Player)

**Problem**: This address points INSIDE `setup_action_menu_icons` (0x14622-0x14750), not at a valid function entry point.

```
Location: Inside setup_action_menu_icons
Bytes at 0x146f4: 05 83 e8 2c eb 1e
Interpretation: ADD EAX, 0x2ce88305 (garbage)
```

This is **broken/placeholder code** - the handler was never properly implemented.

#### Handler 0x14ed7 (Item 96 - Background Book)

**Problem**: This address points to the VERY END of `init_memory_buffers` (0x14bd0-0x14ee3).

```
Location: End of init_memory_buffers
Bytes at 0x14ed7: 00 00 b0 01 5a 5b c3
Interpretation: MOV AL, 1; POP EDX; POP EBX; RET
```

This handler simply **returns 1 (success)** without doing anything visible.

## Item Grant Mechanism

### Where Items Are Added to Inventory

Code at `0x21b80` and `0x21b94` grants these items:

```asm
; Item 95 grant at 0x21b80
0x21b80: B8 5F 00 00 00    MOV EAX, 95
0x21b85: E9 CD 25 00 00    JMP process_inventory_action (0x24157)

; Item 96 grant at 0x21b94  
0x21b94: B8 60 00 00 00    MOV EAX, 96
0x21b99: E9 B9 25 00 00    JMP process_inventory_action (0x24157)
```

### Unanalyzed Code Region

The item grant code is part of a large unanalyzed region:
- **Address Range**: 0x1ec00 - 0x24157 (~22KB)
- **Contains**: 34 direct calls + 8 jumps to `process_inventory_action`
- **Pattern**: `PUSH 4; CALL get_current_room_number; MOV EAX, item_id; JMP process_inventory_action`

### Items Granted in This Region

| Address | Item ID | Item Name |
|---------|---------|-----------|
| 0x21b58 | 93 | Licor de arena (Sand liquor) |
| 0x21b6c | 94 | Crema para el sol (Sunscreen) |
| **0x21b80** | **95** | **Banda sonora (Soundtrack)** |
| **0x21b94** | **96** | **Album de pantallas (Background Album)** |
| 0x21dad | 102 | Naranjas de Nules |
| 0x21e32 | 103 | Mogollón de naranjas |
| 0x22185 | 105 | Folletos del SIDA |
| 0x222f5 | 111 | Cinta del Rey Elvis |

## Dispatch Mechanism (Unknown)

**Problem**: No xrefs or jump tables reference the unanalyzed region.

Checked tables:
- F8 Action Dispatch Table (0x47e58) - No matches
- Hotspot Action Table (0x47bf0) - No matches
- Room-Specific Script Table (0x47d24) - No matches
- Item Combination Table (0x48118) - No matches
- Main Game Loop Table (0x485bc) - No matches

**Hypothesis**: The code may be reached through:
1. Fall-through from preceding code
2. Computed jumps with base address not in data tables
3. Legacy/dead code that was never properly integrated

## F8 Action Codes

The F8 action table has entries for these item numbers:

| F8 Action ID | Handler | Item Related |
|--------------|---------|--------------|
| 0x015F (351) | 0x1202f | Item 95 - inside `init_sprite_scaling_tables` |
| 0x0160 (352) | 0x1151d | Item 96 - unanalyzed region |

These F8 handlers also point to invalid locations.

## Conclusions

### Why the CD Player "Doesn't Work"

The self-use handler at 0x146f4 points to invalid code inside another function. When the player uses the CD Player on Alfred:
1. Game looks up handler in item combination table
2. Calls address 0x146f4
3. Executes garbage instructions from middle of `setup_action_menu_icons`
4. Behavior is undefined/crashes

### Why the Background Book "Works"

The self-use handler at 0x14ed7 is at the tail of `init_memory_buffers`:
1. Game looks up handler in item combination table
2. Calls address 0x14ed7
3. Executes `MOV AL, 1; POP; POP; RET`
4. Returns success without doing anything visible

The book might "work" because:
- The actual book viewer code is called elsewhere (before the self-use handler)
- Or the item triggers a different code path when first used

### Recommendations for ScummVM Implementation

1. **Item 95 (CD Player)**: Implement a proper soundtrack player
2. **Item 96 (Background Book)**: Implement a background art gallery viewer
3. **Grant Mechanism**: These items should be granted after game completion or through a specific puzzle/action
4. **Self-Use Handlers**: Replace broken handlers with functional implementations

## Debug Access

Items 95 and 96 can be added to inventory at game startup using command-line parameters:

```bash
JUEGO.EXE o 95    # Adds CD Player/Soundtrack
JUEGO.EXE o 96    # Adds Background Book  
JUEGO.EXE o 95 o 96  # Adds both items
```

This is implemented in `game_initialization` (0x10010):

```c
if (*(char *)*puVar5 == 'o') {
    uVar2 = FUN_0002a27a(puVar5[1]);  // Parse item number
    (&inventory_item_ids)[num_available_actions] = uVar2;
    num_available_actions++;
}
```

## Technical Reference

### Memory Addresses

| Purpose | Ghidra Address | File Offset |
|---------|----------------|-------------|
| Item Combination Table | 0x48118 | 0x4B318 |
| Item 95 Self-Use Handler | 0x146f4 | 0x188f4 |
| Item 96 Self-Use Handler | 0x14ed7 | 0x190d7 |
| Item 95 Grant Code | 0x21b80 | 0x25d80 |
| Item 96 Grant Code | 0x21b94 | 0x25d94 |
| process_inventory_action | 0x24157 | 0x28357 |

### Offset Formulas

```
Code: file_offset = ghidra_addr - 0x10000 + 0x14200
Data: file_offset = ghidra_addr - 0x40000 + 0x43200
```
