# Brick + Window Combination Analysis

## Summary

When using the brick (inventory item 4) on the window (hotspot extra 294) in room 3:

### Observed Behavior
1. Alfred plays a "throwing" special animation
2. Sprite 6 (brick projectile) animates moving vertically toward the window
3. Sticker 11 (broken window graphic) is placed on screen
4. NPC dialog sequence plays:
   - "¡¡ QUE HA SIDO ESO !!" (What was that!)
   - "¡¡ QUIEN ANDA AHI !!" (Who's there!)
   - "Yo me voy" (I'm leaving)
5. NPC character walks to right edge of screen and exits

## Original Code Analysis

### Memory Mapping (verified)
- Code segment: memory 0x10000+ → file offset 0x14200+ (formula: file = mem + 0x4200)
- Data segment: memory 0x40000+ → file offset 0x43200+ (formula: file = mem + 0x3200)

### Dispatch Table Entry
- Located at: memory 0x48118 (file 0x4B318)  
- Entry format: 8 bytes (item1:2, item2:2, func_ptr:4)
- Entry 1: item1=0x0126 (294=window), item2=0x0004 (4=brick), func_ptr=0x0001284B

### Dispatcher Function
The item combination table is processed by `execute_complex_item_script_table` at 0x191E9:
```c
// At 0x192FB: CALL dword ptr [EAX*0x8 + 0x4811c]
// This calls the function pointer from the table
```

### CRITICAL ISSUE: Function Pointer Points to Mid-Instruction
The function pointer 0x1284B does NOT point to a valid function entry point:
- Address 0x12849 contains: `MOV BX,word ptr [0x0004fb9e]` (6 bytes)
- Address 0x1284B is 2 bytes INTO this instruction
- Ghidra shows 0x124AD as the start of the containing function (misnamed `brick_window_handler`)
- This function at 0x124AD is actually the ACTION MENU POPUP HANDLER (shows verb icons)

**Analysis**: The function pointers in this table appear invalid. All entries in the 0x48118 table
have func_ptrs that point to interior addresses of the action menu handler function (0x124AD-0x12917).
This may indicate:
1. The table is dynamically patched at runtime
2. The table structure is misunderstood  
3. There's a relocation/fixup mechanism not accounted for
4. The original data is corrupted in our copy

### Calling Context
From `main_game_loop` at 0x106C2:
```c
if ((mouse_hover_state != '\0') && (3 < frameCount) && 
    (current_room != 0x15) && (current_room != 0x37)) {
    action_menu_handler();  // <- This was misnamed brick_window_handler
}
```

### Dialog Text Locations (file offsets in ALFRED.1)
- 0x443A0: "¡¡ QUE HA SIDO ESO !!" (prefix: FD 00 08 07)
- 0x443BF: "¡¡ QUIEN ANDA AHI !!" (prefix: FD 00 08 07)
- 0x443DD: "Yo me voy" (prefix: FD 00 08 0D)
- Text indices: WHATWASTHAT=13, WHOS_THERE=14, IMOFF=15

### Sticker 11
- Located in ALFRED.6 at offset pegatina_offsets[11] = 0x008529
- Room 3 palette (tablapaletas[11] = 3)
- This is the "broken window" graphic that replaces the intact window

### Sprite 6 (Room 3)
- The brick projectile animation
- Moves from Alfred's throwing position upward to the window

## ScummVM Implementation

### Implementation Status: COMPLETE (basic functionality)
Location: `/Users/gabriel/Desktop/source/scummvm/engines/pelrock/actions.cpp`

```cpp
void PelrockEngine::useBrickWithWindow(int inventoryObject, HotSpot *hotspot) {
    // Check if window is already broken
    if (_room->hasSticker(11)) {
        _alfredState.direction = ALFRED_UP;
        _dialog->say(_res->_ingameTexts[YA_ABIERTO_M]);
        return;
    }
    
    // TODO: Play Alfred's throwing animation
    // TODO: Animate sprite 6 (brick projectile)
    
    _room->addSticker(11);                              // Broken window graphic
    _state->removeInventoyItem(4);                      // Remove brick
    _dialog->say(_res->_ingameTexts[WHATWASTHAT]);     // "What was that!"
    _dialog->say(_res->_ingameTexts[WHOS_THERE]);      // "Who's there!"  
    _dialog->say(_res->_ingameTexts[IMOFF]);           // "I'm leaving"
    
    // TODO: Make NPC walk off screen to the right
}
```

### Dispatch Table Entry
```cpp
// In combinationTable[]:
{4, 294, &PelrockEngine::useBrickWithWindow},  // Brick + Window
```

### Related Files
- `engines/pelrock/actions.cpp` - Implementation
- `engines/pelrock/pelrock.h` - Declaration (line 259)
- `engines/pelrock/actions.h` - CombinationEntry struct
- `engines/pelrock/offsets.h` - Text indices

## TODO Items
1. [ ] Find/add throwing animation for Alfred
2. [ ] Implement sprite 6 projectile animation
3. [ ] Implement NPC walk-off animation after dialog
4. [ ] Investigate why original func_ptr points to invalid address
