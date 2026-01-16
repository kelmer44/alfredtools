# Room Handler Analysis - Detailed

## Summary

After careful analysis, the room initialization handlers in Alfred Pelrock serve purposes that are **mostly already data-driven** in ScummVM through the room metadata. Here's the breakdown:

### Rooms 0-15 Handler Analysis

#### Room Initialization Handlers (Table 1 - load_room_data)

| Room | Handler | What It Does | ScummVM Status |
|------|---------|--------------|----------------|
| 0 | 0x1561F | Entry point after Room 3 text swap | ✅ No action needed |
| 1 | None | Default initialization | ✅ Already works |
| 2 | 0x15C22 | VGA register setup for palette cycling | ⚠️ Already handled by palette anim system |
| 3 | 0x15889 | Jump past scaling code | ✅ Handled by scaleMode data |
| 4 | 0x1561F | Same as Room 0 | ✅ No action needed |
| 5 | 0x15A3D | Sets render enable and scale factor | ✅ Already standard behavior |
| 6 | None | Default initialization | ✅ Already works |
| 7 | 0x1587A | Disable scaling (scale_min=0, scale_max=0) | ✅ Use scaleMode=0 in room data |
| 8 | None | Default initialization | ✅ Already works |
| 9 | 0x158BD | Scaling calculation setup | ✅ Handled by scaleMode data |
| 10 | None | Default initialization | ✅ Already works |
| 11 | None | Default initialization | ✅ Already works |
| 12 | 0x15C49 | Near-end-of-function init | ✅ Standard behavior |
| 13 | 0x15BEC | Shared handler | ✅ No special logic needed |
| 14 | None | Default initialization | ✅ Already works |
| 15 | None | Default initialization | ✅ Already works |

#### Per-Frame Handlers (Tables 3 & 4)

| Room | Table | Handler | What It Does | ScummVM Implementation |
|------|-------|---------|--------------|----------------------|
| 1 | 4 | 0x118AD | Ambient event every ~7.5 min | ⚠️ **NEEDS IMPL** |
| 2 | 4 | 0x118AD | Ambient event every ~7.5 min | ⚠️ **NEEDS IMPL** |
| 3 | 4 | 0x118AD | Ambient event every ~7.5 min | ⚠️ **NEEDS IMPL** |
| 8 | 4 | 0x118AD | Ambient event every ~7.5 min | ⚠️ **NEEDS IMPL** |
| 9 | 3 | 0x1167A | Mouse animation L→R | ⚠️ **NEEDS IMPL** |
| 12 | 4 | 0x118AD | Ambient event every ~7.5 min | ⚠️ **NEEDS IMPL** |
| 14 | 4 | 0x118AD | Ambient event every ~7.5 min | ⚠️ **NEEDS IMPL** |
| 15 | 4 | 0x11DE5 | One-shot cutscene trigger | ⚠️ **NEEDS IMPL** |

---

## Detailed Per-Frame Handler Analysis

### Room 9: Mouse Passing Animation (0x1167A)

**Purpose**: A mouse runs across the floor from left to right every ~56 seconds.

**Disassembly Analysis**:
```
Frame counter trigger: (game_frame_counter & 0x3FF) == 0x3FF
Latch variable: 0x95EB (prevents re-trigger while mouse visible)
State variable: 0x964E (mouse animation state)

Logic:
1. Check if frame_counter & 0x3FF == 0x3FF (~56 sec)
2. If latch 0x95EB is clear, set it and start animation
3. Set sprite[0].animation_id = 0xD2 (mouse running)
4. As mouse moves, check X position against waypoints:
   - X > 200: Set direction flag 0x95EC, change direction
   - X > 330: Set flag 0x95ED, change scale
   - X > 135: Set flag 0x95EE, final waypoint
5. When animation ends (sprite[0].enabled == 0), clear latch
```

**ScummVM Implementation**:
```cpp
// In room.cpp or a new passingSprites.cpp

struct PassingSpriteState {
    bool latch;           // 0x95EB - prevents re-trigger
    bool waypoint1;       // 0x95EC
    bool waypoint2;       // 0x95ED
    bool waypoint3;       // 0x95EE
    uint8 animState;      // 0x964E
};

void AlfredEngine::updateRoom9PassingSprite() {
    // Check frame trigger every ~56 seconds
    if ((_frameCounter & 0x3FF) == 0x3FF && !_room9State.latch) {
        _room9State.latch = true;
        // Start mouse animation - sprite slot 0, animation 0xD2
        startSpriteAnimation(0, 0xD2);  // Mouse running right
    }

    // Check if mouse animation complete
    if (_room9State.latch) {
        Sprite *mouse = &_sprites[0];

        // Waypoint checks - change direction/scale at certain X positions
        if (mouse->x > 200 && !_room9State.waypoint1) {
            _room9State.waypoint1 = true;
            mouse->direction = 3;  // Change facing
            mouse->z_order = 0x3E0;
        }
        if (mouse->x > 330 && !_room9State.waypoint2) {
            _room9State.waypoint2 = true;
            mouse->direction = 2;
            mouse->z_order = 0x1F;
        }
        // ... more waypoints

        // Clear latch when animation ends
        if (!mouse->enabled) {
            _room9State.latch = false;
            _room9State.waypoint1 = false;
            _room9State.waypoint2 = false;
            _room9State.waypoint3 = false;
        }
    }
}
```

---

### Rooms 1, 2, 3, 8, 12, 14: Shared Ambient Handler (0x118AD)

**Purpose**: Periodic ambient event that triggers every ~7.5 minutes across multiple rooms.

**Disassembly Analysis**:
```
Frame counter trigger: (game_frame_counter & 0x1FFF) == 0x1FFF
  = Every 8192 frames = ~7.5 minutes at 18.2 Hz

Logic:
1. Check frame_counter & 0x1FFF == 0x1FFF (~7.5 min)
2. Get current room number from [0xFB94]
3. Look up room-specific sprite index from table at 0x4B854
4. Get sprite data at [sprite_data_ptr + index * 0x2C]
5. Check if sprite[index].field_0x21 == 0xFF (disabled state)
6. If so, set sprite[index].field_0x21 = 3 (enable animation)
```

**Room-to-Sprite Index Table** (extracted from 0x4B854):
| Room | Sprite Index | Description |
|------|--------------|-------------|
| 1 | 7 | Ambient sprite slot 7 |
| 2 | 5 | Ambient sprite slot 5 |
| 3 | 8 | Ambient sprite slot 8 |
| 8 | 9 | Ambient sprite slot 9 |
| 12 | (not in table) | Uses default? |
| 14 | (not in table) | Uses default? |

**ScummVM Implementation**:
```cpp
// Room-to-sprite mapping table (from address 0x4B854)
static const uint8 kAmbientSpriteIndex[] = {
    0,  // Room 0
    7,  // Room 1
    5,  // Room 2
    8,  // Room 3
    0,  // Room 4
    0,  // Room 5
    0,  // Room 6
    0,  // Room 7
    9,  // Room 8
    0,  // Room 9
    0,  // Room 10
    4,  // Room 11
    0,  // Room 12 - not in table, may not trigger
    0,  // Room 13
    0,  // Room 14 - not in table, may not trigger
    // ... etc
};

void AlfredEngine::updateAmbientSprites() {
    // Trigger every ~7.5 minutes
    if ((_frameCounter & 0x1FFF) != 0x1FFF)
        return;

    // Get sprite index for this room
    uint8 spriteIndex = kAmbientSpriteIndex[_currentRoom];
    if (spriteIndex == 0)
        return;  // No ambient sprite for this room

    Sprite *sprite = &_sprites[spriteIndex];

    // Sprite struct is 0x2C (44) bytes
    // field_0x21 is the animation state byte
    if (sprite->animState == 0xFF) {
        sprite->animState = 3;  // Enable animation
    }
}
```

---

### Room 15: One-Shot Cutscene Trigger (0x11DE5)

**Purpose**: Triggers a cutscene/dialog once when entering room 15.

**Disassembly Analysis**:
```
One-shot flag: 0x9653 (prevents re-trigger after first execution)

Logic:
1. Check if flag [0x9653] == 0 (not yet triggered)
2. If flag is clear:
   a. Set flag [0x9653] = 1 (prevent future triggers)
   b. Call play_get_naked_easter_egg (0x1B1A2) with param from [0xBC80]
   c. Call display_text_with_voice (0x25487) with param from [0xBC84]
   d. Call play_get_naked_easter_egg (0x1B1A2) with param from [0xBC88]
3. Exit
```

The functions called are:
- `0x1B1A2` = `play_get_naked_easter_egg` - Displays text with character animation
- `0x25487` = `display_text_with_voice` - Shows text with voice playback

**Note**: The function name `play_get_naked_easter_egg` is misleading - it's a general dialog display function.

**ScummVM Implementation**:
```cpp
// In room loading or per-frame update

void AlfredEngine::updateRoom15() {
    if (_room15TriggeredFlag)
        return;

    _room15TriggeredFlag = true;

    // Trigger the room 15 entrance dialog sequence
    // Values from addresses 0xBC80, 0xBC84, 0xBC88 are dialog IDs
    uint32 dialogParam1 = getDataWord(0xBC80);
    uint32 soundParam = getDataWord(0xBC84);
    uint32 dialogParam2 = getDataWord(0xBC88);

    // Display dialog with character animation
    playDialogWithAnimation(dialogParam1);
    displayTextWithVoice(soundParam);
    playDialogWithAnimation(dialogParam2);
}

// Reset flag when appropriate (check original game behavior)
// This flag should be saved in save game state
```

---

## Key Finding

The dispatch table handlers are **OPTIMIZATION CODE**, not special logic. They skip portions of the initialization that don't apply to certain rooms:

1. **Room 3 Handler (0x15889)**: Enters right at a JMP instruction that skips the remaining scaling calculation. This is because Room 3's `scaleMode` byte in the room data already indicates no dynamic scaling is needed.

2. **Room 0/4 Handler (0x1561F)**: These enter after the Room 3 text swap code because they don't need that text manipulation.

3. **Room 2 Handler (0x15C22)**: Enters late in the function during VGA setup. This is already handled by ScummVM's palette animation system.

4. **Room 5 Handler (0x15A3D)**: Enters at sprite render setup. Standard behavior, no special handling.

5. **Room 7 Handler (0x1587A)**: Sets scale_min=0, scale_max=0. ScummVM handles this via scaleMode in room data.

### Room 3 Text Swap

There IS one piece of special logic - Room 3 has text data that gets reordered:

```c
// Original DOS code for Room 3:
if (room_number == 3) {
    // Find '-' character in text data
    while (*text_scanner != '-') text_scanner++;
    // Swap text blocks
    memcpy(text_scanner + 0x4e22, text_scanner + 2, 0x474);
    memcpy(text_scanner + 10, text_scanner + 0x4e22, 0x474);
}
```

This swaps conversation text for Room 3. **This is NOT handled by dispatch table but is hardcoded logic in the main function.**

---

## ScummVM Implementation Summary

### Already Working (No Changes Needed)
- Room initialization handlers (Table 1) - all are optimization jumps
- Room 7 scaling disable - use scaleMode data
- Room 2 palette cycling - already in PaletteAnim system

### Needs Implementation

#### 1. Room 9 Passing Mouse
```cpp
// Add to AlfredEngine class:
struct {
    bool latch;
    bool waypoints[3];
} _room9PassingState;

// Call from main loop when in room 9:
if (_currentRoom == 9) {
    updateRoom9PassingSprite();
}
```

#### 2. Ambient Sprite Handler (Rooms 1,2,3,8,12,14)
```cpp
// Add to AlfredEngine class:
// Call from main loop for these rooms:
if (isAmbientRoom(_currentRoom)) {
    updateAmbientSprites();
}
```

#### 3. Room 15 One-Shot
```cpp
// Add flag to save game state:
bool _room15TriggeredFlag;

// Check on room entry or per-frame:
if (_currentRoom == 15 && !_room15TriggeredFlag) {
    triggerRoom15Cutscene();
}
```

#### 4. Room 3 Text Swap (if needed)
```cpp
// In Room::loadTextData() when room == 3:
if (roomNumber == 3) {
    swapTextBlocks();
}
```

---

## Related Documentation

- **DISPATCH_TABLES_COMPLETE_ANALYSIS.md** - Full dispatch table reference
- **CONVERSATION_SYSTEM_DOCUMENTATION.md** - Dialog system for Room 15 cutscene
- **SPRITE_SCALING.md** - Sprite scaling for Room 9 mouse waypoints
