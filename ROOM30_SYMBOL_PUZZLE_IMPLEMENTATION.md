# Room 30 Symbol Puzzle — Complete Implementation Guide

## Overview

Room 30 contains an Egyptian symbol puzzle where the player must press 4 specific symbols in any order to open a secret door. The puzzle requires the player to have first examined the markings in Room 29 (Extra 327), which sets a prerequisite flag.

---

## Puzzle Architecture

### Prerequisites

**Room 29 — Egyptian Museum**
- **Extra 327** (F8 dialog handler): Triggered when player LOOKs at Room 29 hotspot whose dialog text contains F8 control code 327
- **Action**: Sets flag `[0x495E5] = 1` (memory address 0x95E5 in data segment)
- **Purpose**: Enables the symbol puzzle in Room 30. Without this flag, clicking symbols does nothing.

### Room 30 — Symbol Puzzle

**10 Hotspots total**, all type 0x20 (LOOK enabled):

| Hotspot | Position | Extra | Symbol | Sets Bit |
|---------|----------|-------|--------|----------|
| 0 | (431, 244) 8×30 | 435 | Symbol 1 | 0x1 (bit 0) |
| 1 | (430, 178) 15×26 | 436 | Symbol 2 | 0x2 (bit 1) |
| 2 | (456, 192) 10×23 | 437 | Symbol 3 | 0x4 (bit 2) |
| 3 | (428, 207) 14×13 | 438 | Symbol 4 | 0x8 (bit 3) |
| 4 | (429, 224) 13×18 | **439** | decoy/repeat | *(shares handler with extras 435-438)* |
| 5 | (447, 218) 20×10 | **440** | decoy/repeat | *(shares handler with extras 435-438)* |
| 6 | (446, 229) 9×23 | **441** | decoy/repeat | *(shares handler with extras 435-438)* |
| 7 | (440, 253) 32×4 | 439 | decoy/repeat | *(duplicate extra)* |
| 8 | (450, 260) 22×35 | 440 | decoy/repeat | *(duplicate extra)* |
| 9 | (429, 275) 19×15 | 441 | decoy/repeat | *(duplicate extra)* |

**Note**: Extras 435-438 are the 4 unique symbols. Extras 439-441 appear to be decoys or duplicates that reuse the same handler logic.

---

## Handler Logic

### Symbol Click Handlers (Extras 435-438)

**Source**: LOOK verb dispatch table at 0x47BF0
- Extra 435 → `0x1C065` (Ghidra `0x2C065`)
- Extra 436 → `0x1C098` (Ghidra `0x2C098`) - Extra 437 → `0x1C0CB` (Ghidra `0x2C0CB`)
- Extra 438 → `0x1C0FE` (Ghidra `0x2C0FE`)

**Each handler follows the same pattern:**

```c
void symbol_handler(int bit_mask) {
    // Check prerequisite: Room 29 flag must be set
    if (game_flags[0x495E5] == 0) {
        return;  // Puzzle not enabled yet
    }
    
    // Set this symbol's bit using OR (accumulates clicks)
    game_flags[0x495C8] |= bit_mask;  // bit_mask = 0x1, 0x2, 0x4, or 0x8
    
    // Check if all 4 symbols have been clicked
    if (game_flags[0x495C8] == 0x0F) {  // 0x0F = binary 1111 (all 4 bits set)
        trigger_statue_secret();
    }
}
```

**Key Points:**
1. Uses **bitwise OR** to accumulate clicks (clicking same symbol twice doesn't break puzzle)
2. Order doesn't matter — any sequence works as long as all 4 are clicked
3. Flag at `[0x495C8]` accumulates: `0x1 | 0x2 | 0x4 | 0x8 = 0x0F`
4. When `0x0F` reached, triggers the secret door sequence

---

## Secret Door Trigger Sequence

**Function**: `trigger_statue_secret` at 0x1C131 (Ghidra 0x2C131)

### Pseudocode

```c
void trigger_statue_secret() {
    RoomData *room = room_data_ptr;  // [0xFAC8]
    
    // Prevent retriggering
    if (room->data[0x1C1] != 0) {
        return;  // Already triggered
    }
    
    // === ANIMATION PHASE ===
    // Play secret door animation (parameters suggest sprite/sticker animations)
    uint8_t param1 = memory[0x13002];
    uint32_t param2 = memory[0x13234];
    uint32_t param3 = memory[0x13204];
    
    play_animation(
        sprite_id: param3,
        x_offset: -1 (0xFFFF),
        y_offset1: 0x100,
        y_offset2: 0x100,
        flags: 0x40,
        param2: param2,
        param1: param1
    );  // Function at 0x37CE1
    
    // === PERSISTENCE PHASE ===
    // Mark puzzle as solved permanently
    room->data[0x1C1] = 1;
    write_room_data_to_alfred1(room_id, offset=0x1C1, data=1, size=1);
    
    // Set animation control bytes
    room->data[0x129] = 0xFC;  // Animation trigger
    room->data[0x124] = 2;     // Animation state
    
    // === WAIT FOR ANIMATION COMPLETION ===
    while (true) {
        wait_or_process_input(0x15D);  // Wait with event processing
        render_frame();  // Function at 0x247C9
        update_scene(0);  // Function at 0x25E4C
        
        // Check if animation finished
        if (room->data[0x129] == 0xFF) {
            break;  // Animation complete
        }
    }
    
    // === REVEAL SECRET DOOR ===
    // Set global flag (probably enables exit or new hotspot)
    game_flags[0xA6E8] = 1;
    
    // Display sticker showing secret door open
    display_sticker_from_alfred6(
        offset: 0x6C84D,
        size: 0x4110
    );  // Function at 0x2BA45
}
```

### Memory Addresses Reference

| Address | Type | Purpose |
|---------|------|---------|
| `0x495E5` | byte | Prerequisite flag (set by Room 29 Extra 327) |
| `0x495C8` | byte | Symbol accumulator (bits: 0x1, 0x2, 0x4, 0x8) |
| `room_data[0x1C1]` | byte | Puzzle solved flag (persistent in ALFRED.1) |
| `room_data[0x124]` | byte | Animation state byte |
| `room_data[0x129]` | byte | Animation control byte (0xFC → 0xFF when done) |
| `0xA6E8` | byte | Secret door revealed flag |

---

## ScummVM Implementation Steps

### Step 1: Room 29 Setup (Prerequisite)

```cpp
// In room29.cpp or equivalent

void Room29::handleF8Code(uint16 extra) {
    if (extra == 327) {
        // Player examined markings
        _vm->setGameFlag(0x95E5, 1);
        
        // Optional: Show feedback message
        // "The ancient symbols seem important..."
    }
}
```

### Step 2: Room 30 State Variables

```cpp
// Add to PelrockEngine or Room30 class

class Room30 {
private:
    uint8 _symbolBits;        // Accumulator for clicked symbols (stored at 0x495C8)
    bool _puzzleSolved;       // Stored in room_data[0x1C1], persisted to ALFRED.1
    bool _prerequisiteMet;    // Reads from flag 0x495E5
    
public:
    Room30() : _symbolBits(0), _puzzleSolved(false), _prerequisiteMet(false) {}
    
    void init() {
        // Load state from save game
        _prerequisiteMet = _vm->getGameFlag(0x95E5);
        _puzzleSolved = _vm->getRoomData(30, 0x1C1);
        _symbolBits = _vm->getGameFlag(0x495C8);
    }
};
```

### Step 3: Hotspot Click Handlers

```cpp
void Room30::onLookAtHotspot(uint16 hotspotIndex) {
    uint16 extra = _hotspots[hotspotIndex].extra;
    
    // Handle symbol clicks (extras 435-438)
    if (extra >= 435 && extra <= 438) {
        handleSymbolClick(extra);
        return;
    }
    
    // ... handle other hotspots
}

void Room30::handleSymbolClick(uint16 extra) {
    // Check prerequisite
    if (!_prerequisiteMet) {
        // No feedback — player hasn't seen Room 29 markings yet
        return;
    }
    
    // Check if already solved
    if (_puzzleSolved) {
        return;  // Door already open
    }
    
    // Determine which bit to set
    uint8 bit = 0;
    switch (extra) {
        case 435: bit = 0x01; break;  // Symbol 1
        case 436: bit = 0x02; break;  // Symbol 2
        case 437: bit = 0x04; break;  // Symbol 3
        case 438: bit = 0x08; break;  // Symbol 4
        default: return;
    }
    
    // Set bit (OR operation allows clicking same symbol multiple times safely)
    _symbolBits |= bit;
    _vm->setGameFlag(0x495C8, _symbolBits);
    
    // Optional: Play symbol activation sound/effect
    // _vm->playSound(SYMBOL_CLICK_SFX);
    
    // Check if puzzle solved
    if (_symbolBits == 0x0F) {  // All 4 bits set: 0x1 | 0x2 | 0x4 | 0x8
        triggerSecretDoor();
    }
}
```

### Step 4: Secret Door Trigger

```cpp
void Room30::triggerSecretDoor() {
    // Mark as solved (prevents retriggering)
    _puzzleSolved = true;
    _vm->setRoomData(30, 0x1C1, 1);
    _vm->persistRoomDataToALFRED1(30, 0x1C1, 1);  // Save to disk
    
    // === ANIMATION SEQUENCE ===
    
    // Set animation control bytes
    _vm->setRoomData(30, 0x129, 0xFC);  // Start animation
    _vm->setRoomData(30, 0x124, 2);     // Animation state
    
    // Play door opening animation
    // Parameters from original: sprite from memory[0x13204], offsets 0x100, 0x100
    uint32 spriteId = _vm->readMemory(0x13204);
    playSecretDoorAnimation(spriteId);
    
    // Wait for animation to complete
    // The original checks room_data[0x129] == 0xFF
    while (_vm->getRoomData(30, 0x129) != 0xFF) {
        _vm->processEvents();  // Keep game responsive
        _vm->updateFrame();
        _vm->delay(16);  // ~60fps
    }
    
    // === REVEAL SECRET DOOR ===
    
    // Set global flag (may enable new exit or hotspot)
    _vm->setGameFlag(0xA6E8, 1);
    
    // Display sticker: secret door revealed
    // Original: sticker at ALFRED.6 offset 0x6C84D, size 0x4110 (16656 bytes)
    _vm->displaySticker(0x6C84D, 0x4110);
    
    // Optional: Play door opening sound
    // _vm->playSound(SECRET_DOOR_OPEN_SFX);
    
    // Optional: Show congratulatory message
    // _vm->displayText("A secret passage opens in the wall!");
}

void Room30::playSecretDoorAnimation(uint32 spriteId) {
    // Original calls function at 0x37CE1 with params:
    // - sprite_id (from memory[0x13204])
    // - x_offset: -1 (0xFFFF) — likely means "center" or "default position"
    // - y_offset1: 0x100 (256)
    // - y_offset2: 0x100 (256)
    // - flags: 0x40 (64)
    // - param2: memory[0x13234]
    // - param1: memory[0x13002]
    
    uint32 param2 = _vm->readMemory(0x13234);
    uint8 param1 = _vm->readMemory(0x13002);
    
    _vm->playSpriteAnimation(spriteId, -1, 0x100, 0x100, 0x40, param2, param1);
    
    // NOTE: You'll need to reverse-engineer function at 0x37CE1 to understand
    // exactly what these parameters do. It may involve:
    // - Loading animation frames from ALFRED.3 or ALFRED.7
    // - Setting up sprite rendering structures
    // - Playing a sequence of frames
}
```

### Step 5: Save/Load Integration

```cpp
void Room30::saveState(SaveGame *save) {
    save->writeByte(_symbolBits);
    save->writeByte(_puzzleSolved ? 1 : 0);
}

void Room30::loadState(SaveGame *save) {
    _symbolBits = save->readByte();
    _puzzleSolved = (save->readByte() != 0);
    _prerequisiteMet = _vm->getGameFlag(0x95E5);  // Always read from game state
}
```

---

## Testing Checklist

### Basic Functionality
- [ ] Room 30 loads without crashing
- [ ] All 10 hotspots are clickable
- [ ] LOOKing at non-puzzle hotspots works normally

### Puzzle Prerequisite
- [ ] Clicking symbols in Room 30 **before** visiting Room 29 does nothing
- [ ] Looking at markings in Room 29 (Extra 327 F8 code) sets flag 0x495E5
- [ ] After Room 29, clicking symbols in Room 30 now works

### Puzzle Mechanics
- [ ] Clicking any of the 4 unique symbols (435-438) accumulates bits
- [ ] Order doesn't matter (try different sequences)
- [ ] Clicking same symbol twice doesn't break puzzle
- [ ] Clicking all 4 symbols triggers secret door

### Secret Door Sequence
- [ ] Animation plays when puzzle solved
- [ ] Animation doesn't skip or freeze
- [ ] Sticker displays showing door open
- [ ] Flag 0xA6E8 is set after door opens
- [ ] Puzzle doesn't retrigger if clicked again

### Persistence
- [ ] Save game after solving puzzle
- [ ] Load save — door should still be open
- [ ] Flag 0x495C8 should retain value 0x0F- [ ] Room data[0x1C1] should be 1

---

## Common Implementation Pitfalls

1. **Forgetting Prerequisite Check**
   - Symbols must do nothing if flag 0x495E5 is not set
   - Don't show error messages — silently return

2. **Using Assignment Instead of OR**
   - MUST use `|=` not `=` for _symbolBits
   - Using `=` breaks if player clicks same symbol twice

3. **Not Persisting Puzzle State**
   - Room data[0x1C1] must be saved to ALFRED.1
   - Otherwise puzzle resets on room re-entry

4. **Animation Parameters**
   - The animation function at 0x37CE1 needs careful reverse-engineering
   - Parameters come from specific memory addresses
   - May need to extract exact animation data from ALFRED.3/ALFRED.7

5. **Sticker Offset/Size**
   - Sticker at 0x6C84D in ALFRED.6
   - Size is 0x4110 (16656 bytes)
   - Verify this matches actual ALFRED.6 data

---

## Ghidra Analysis Commands

If you need to investigate further in Ghidra:

```
# Decompile symbol handlers
Function: 0x2C065 (Extra 435, Symbol 1, sets bit 0x1)
Function: 0x2C098 (Extra 436, Symbol 2, sets bit 0x2)
Function: 0x2C0CB (Extra 437, Symbol 3, sets bit 0x4)
Function: 0x2C0FE (Extra 438, Symbol 4, sets bit 0x8)

# Decompile secret door trigger
Function: 0x2C131 (trigger_statue_secret)

# Decompile animation function
Function: 0x37CE1 (play animation — called by trigger_statue_secret)

# Decompile sticker display
Function: 0x2BA45 (display_sticker_from_alfred6)

# Find references to puzzle flags
Search for: 0x495E5 (prerequisite flag)
Search for: 0x495C8 (symbol accumulator)
Search for: 0xA6E8 (secret door flag)
```

---

## Related Documentation

- [VERB_DISPATCH_ARCHITECTURE.md](VERB_DISPATCH_ARCHITECTURE.md) — LOOK verb dispatch to 0x47BF0 table
- [F8_ACTION_CODE_COMPLETE_REFERENCE.md](F8_ACTION_CODE_COMPLETE_REFERENCE.md) — Room 29 Extra 327
- [VERB_ACTIONS_COMPLETE.md](VERB_ACTIONS_COMPLETE.md) — Extras 435-438 handlers (lines 5231-5400)
- ALFRED.1 format — Room hotspot data structure
- ALFRED.6 format — Sticker data at offset 0x6C84D

---

## Summary

The Room 30 puzzle is a well-designed mechanic that:
- **Requires exploration** (must visit Room 29 first)
- **Forgiving** (order doesn't matter, can click symbols multiple times)
- **Persistent** (saves state to disk, door stays open)
- **Visual feedback** (animation + sticker display)
- **Integrates with game state** (sets flag 0xA6E8 which likely enables new areas)

Implementation should focus on:
1. Proper prerequisite checking (flag 0x495E### Summary

The Room 30 puzzle is a well-designed mechanic that:
- **Requires exploration** (must visit Room 29 first)
- **Forgiving** (order doesn't matter, can click symbols multiple times)
- **Persistent** (saves state to disk, door stays open)
- **Visual feedback** (animation + sticker display)
- **Integrates with game state** (sets flag 0xA6E8 which likely enables new areas)

Implementation priorities:
1. Prerequisite checking (flag 0x495E5)
2. Bitwise OR accumulation (not assignment)
3. State persistence (room_data[0x1C1] to ALFRED.1)
4. Animation reverse-engineering (function 0x37CE1)
5. Sticker extraction from ALFRED.6 offset 0x6C84D
