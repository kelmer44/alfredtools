# ScummVM Implementation: "Passing By" Sprite Animations

## Overview

This document describes how to implement the hidden "passing by" sprite animations
(camel in room 21, mouse in room 9, etc.) for ScummVM. These are background sprites
that appear periodically to add atmosphere.

## Summary of Mechanism

The original game uses:
1. **Frame counter trigger**: `(frame_counter & 0x3FF) == 0x3FF` fires every 1024 frames (~56 seconds)
2. **render_scene dispatch table**: Room-specific handlers at virtual address 0x48630
3. **Per-room latch flags**: Some rooms prevent re-triggering until animation completes

---

## Core Algorithm

### Frame Counter System

```cpp
// Global frame counter - increments every frame (~18.2 Hz / 55ms per frame)
// NEVER RESET - runs continuously from game start
// Overflow is harmless because trigger uses bitmask (see below)
uint32 _gameFrameCounter = 0;

// Called every game frame
void updateFrameCounter() {
    _gameFrameCounter++;  // Let it overflow naturally - doesn't matter
}

// Check if trigger condition is met
bool isPassingSpriteTrigger() {
    return (_gameFrameCounter & 0x3FF) == 0x3FF;
}
```

**Key points:**
- Counter runs at 18.2 Hz (DOS timer interrupt rate)
- Trigger fires when lower 10 bits are all 1s
- This happens every 1024 frames = **56.2 seconds**
- Counter is GLOBAL - not reset per room
- **Overflow safe**: The `& 0x3FF` mask uses only bottom 10 bits, so the trigger
  works correctly regardless of total counter value (even after overflow)
- A `uint32` would overflow after ~2.7 days of continuous play, but the mask
  makes this irrelevant - no reset needed

---

## Room-Specific Implementations

### Room 21: Desert Camel

**Behavior**: Camel walks across the background from right to left every ~56 seconds.

**NO LATCH** - Simple implementation:

```cpp
// Room 21 state
struct Room21State {
    uint8 camelAnimState;  // 0=idle, 1=triggered, 2=animating, 3=with_shadow
};

void room21_updateCamelAnimation() {
    // Always check frame counter (every frame while in room 21)
    if (isPassingSpriteTrigger()) {
        // Start camel animation
        Sprite *camel = getSprite(ROOM21_CAMEL_SPRITE_ID);  // Usually sprite index 3
        camel->x = 639;           // Start at right edge
        camel->enabled = true;
        camel->scale = 100;       // Full size (or use sprite[0xFD])
        _room21State.camelAnimState = 1;
    }

    // Handle animation states
    switch (_room21State.camelAnimState) {
        case 1:  // Just triggered
            _room21State.camelAnimState = 2;
            break;

        case 2:  // Animating - camel walking
            // Movement handled by sprite animation system
            // Animation movement flags move camel leftward
            break;

        case 3:  // With shadow rendering
            // Shadow system draws camel shadow
            break;
    }

    // Check if camel exited left
    Sprite *camel = getSprite(ROOM21_CAMEL_SPRITE_ID);
    if (camel->enabled && camel->x < 0) {
        camel->enabled = false;
        _room21State.camelAnimState = 0;
    }
}
```

### Room 9: Office Mouse

**Behavior**: Mouse runs across floor from left to right every ~56 seconds.

**HAS LATCH** - Prevents re-triggering while visible:

```cpp
// Room 9 state
struct Room9State {
    bool mouseLatch;      // True = mouse visible, don't trigger again
};

void room9_updateMouseAnimation() {
    // Frame counter trigger
    if (isPassingSpriteTrigger()) {
        // Only trigger if latch is clear
        if (!_room9State.mouseLatch) {
            _room9State.mouseLatch = true;  // Set latch

            Sprite *mouse = getSprite(ROOM9_MOUSE_SPRITE_ID);  // Usually sprite index 2
            mouse->x = 0;              // Start at left edge
            mouse->y = 210;            // Near bottom of screen
            mouse->enabled = true;
            startSpriteAnimation(mouse, MOUSE_RUN_SEQUENCE);
        }
    }

    // Check if mouse exited right - clear latch
    Sprite *mouse = getSprite(ROOM9_MOUSE_SPRITE_ID);
    if (mouse->enabled && mouse->x > 355) {
        _room9State.mouseLatch = false;  // Clear latch, allow next trigger

        // Also reset related animation state
        mouse->enabled = false;
    }
}
```

---

## Complete Room Handler Table

Rooms with "passing by" animations (from render_scene dispatch table at 0x48630):

| Room | Description | Handler | Has Latch | Trigger Reset Condition |
|------|-------------|---------|-----------|------------------------|
| 9    | Office      | 0x1167a | YES (0x95EB) | Mouse X > 355 |
| 21   | Desert      | 0x107c2 | NO | N/A |
| 29   | Unknown     | 0x11919 | Check | Check |
| 31   | Unknown     | 0x11d66 | Check | Check |
| 46   | Newspaper   | 0x11a29 | YES (0x95FA/FB) | Sprite reaches edge |
| 47   | Unknown     | 0x11b41 | Check | Check |
| 50   | Unknown     | 0x11c4e | Check | Check |

### Rooms 46, 47, 50 Pattern

These rooms share similar latch variables (0x95FA counter, 0x95FB latch):

```cpp
// Shared latch for rooms 26/46/47/50
struct PassingAnimLatch {
    uint8 counter;   // Increments each frame, triggers at >100
    bool latch;      // Prevents re-trigger until sprite exits
};

void room46_updatePassingAnimation() {
    if (_passingLatch.counter > 100 && !_passingLatch.latch) {
        // Trigger animation
        _passingLatch.latch = true;
        _passingLatch.counter = 0;
        // Start sprite...
    }

    // Always increment counter
    _passingLatch.counter++;

    // Clear latch when sprite exits
    if (sprite->x <= 40 || sprite->x >= 60000) {
        _passingLatch.latch = false;
        _passingLatch.counter = 0;
    }
}
```

---

## Sprite Animation Movement

The sprites move across screen using the animation movement flag system:

### Movement Flags (16-bit per animation sequence)

```cpp
struct MovementFlags {
    // Bits 0-2: X movement amount (0-7 pixels/frame)
    // Bit 3: X movement enabled
    // Bit 4: X direction (0=left, 1=right)
    // Bits 5-7: Y movement amount
    // Bit 8: Y direction (0=up, 1=down)
    // Bit 9: Y movement enabled
    // Bits 10-12: Z movement amount
    // Bit 13: Z direction (0=back, 1=forward)
    // Bit 14: Z movement enabled
    uint16 flags;
};

void applySpriteMovement(Sprite *sprite, uint16 movementFlags) {
    // X movement
    if (movementFlags & 0x0008) {  // X enabled
        int amount = movementFlags & 0x0007;
        if (movementFlags & 0x0010) {  // Direction
            sprite->x += amount;  // Move right
        } else {
            sprite->x -= amount;  // Move left
        }
    }

    // Y movement
    if (movementFlags & 0x0200) {  // Y enabled
        int amount = (movementFlags >> 5) & 0x07;
        if (movementFlags & 0x0100) {
            sprite->y += amount;  // Move down
        } else {
            sprite->y -= amount;  // Move up
        }
    }

    // Z-depth movement (for sorting)
    if (movementFlags & 0x4000) {  // Z enabled
        int amount = (movementFlags >> 10) & 0x07;
        if (movementFlags & 0x2000) {
            sprite->zDepth += amount;  // Move forward
        } else {
            sprite->zDepth -= amount;  // Move backward
        }
    }

    // Disable sprite if off-screen
    if (sprite->x >= 640 || sprite->x < -sprite->width ||
        sprite->y >= 400 || sprite->y < -sprite->height) {
        sprite->enabled = false;
        sprite->zDepth = 0xFF;  // Mark as disabled
    }
}
```

---

## Integration with Main Loop

```cpp
// In your main game loop
void updateRoom() {
    // Update global frame counter
    updateFrameCounter();

    // Call room-specific passing sprite handler
    switch (_currentRoom) {
        case 9:
            room9_updateMouseAnimation();
            break;
        case 21:
            room21_updateCamelAnimation();
            break;
        case 29:
            room29_updatePassingAnimation();
            break;
        case 31:
            room31_updatePassingAnimation();
            break;
        case 46:
            room46_updatePassingAnimation();
            break;
        case 47:
            room47_updatePassingAnimation();
            break;
        case 50:
            room50_updatePassingAnimation();
            break;
    }

    // Regular sprite animation updates...
    updateSpriteAnimations();

    // Render scene...
    renderScene();
}
```

---

## Why Timing Appears Random

Players observe variable delays (23 seconds to 2+ minutes) because:

1. **Entry timing**: Frame counter runs from game start, not room entry.
   Entering a room at a random point in the ~56 second cycle means waiting 0-56 seconds.

2. **Latch blocking** (rooms with latches): If you enter while animation is in progress,
   you wait for it to finish PLUS the next 56-second cycle.

3. **Maximum wait**: Up to ~112 seconds if you just miss a trigger AND latch is set.

### Timing Diagram

```
Frame counter: 0...........................1023  0...........................1023
               |                           |     |                           |
               ^--- Trigger fires here ----^     ^--- Next trigger -----------^

Entry A: Enter at frame 100 → Wait ~51 seconds until trigger
Entry B: Enter at frame 1020 → Wait ~0.2 seconds until trigger
Entry C: Enter while latch set → Wait for latch clear + next cycle
```

---

## Data Extraction

### Sprite Data Location

For room 21 (camel):
```
Room data file: ALFRED.1 (or room-specific file)
Sprite structure offset: 0x3B6181 + (sprite_id * 0x2C)
Sprite size: 44 bytes (0x2C)
```

### Key Offsets in Sprite Structure

| Offset | Size | Description |
|--------|------|-------------|
| 0x0A | 2 | X coordinate |
| 0x0C | 2 | Y coordinate |
| 0x0E | 1 | Width |
| 0x0F | 1 | Height |
| 0x12 | 1 | Number of sequences |
| 0x13 | 1 | Current sequence |
| 0x14 | 4 | Frames per sequence (array) |
| 0x18 | 4 | Loop counts (array, 0xFF=infinite) |
| 0x20 | 1 | Current frame |
| 0x21 | 1 | Z-depth (0xFF=disabled) |
| 0x22+ | 2*n | Movement flags per sequence |

---

## Simplified Implementation

If exact emulation isn't critical, use time-based approximation:

```cpp
const int PASSING_SPRITE_INTERVAL_MS = 56000;  // 56 seconds
const int PASSING_SPRITE_VARIANCE_MS = 10000;  // ±10 seconds

uint32 _lastPassingSpriteTime = 0;
uint32 _nextPassingSpriteDelay = 0;

void updatePassingSpriteSimple(int roomId) {
    uint32 now = g_system->getMillis();

    if (now - _lastPassingSpriteTime > _nextPassingSpriteDelay) {
        // Trigger appropriate room animation
        triggerRoomPassingSprite(roomId);

        // Schedule next trigger
        _lastPassingSpriteTime = now;
        _nextPassingSpriteDelay = PASSING_SPRITE_INTERVAL_MS +
            _rnd.getRandomNumber(PASSING_SPRITE_VARIANCE_MS * 2) - PASSING_SPRITE_VARIANCE_MS;
    }
}
```

---

## Testing

To verify implementation:

1. **Camel (Room 21)**: Enter desert, wait up to 56 seconds. Camel should walk across.
2. **Mouse (Room 9)**: Enter office, wait. Mouse runs across floor. Leave and re-enter
   immediately - should NOT trigger again until mouse finishes AND 56 seconds pass.
3. **Frame counter**: Save game, note time to next animation. Load, should be similar
   timing (counter preserved in save).

---

## Summary

| Component | Original Game | ScummVM Implementation |
|-----------|---------------|----------------------|
| Frame counter | 18.2 Hz global timer | `_gameFrameCounter++` every frame |
| Trigger check | `(fc & 0x3FF) == 0x3FF` | Same formula |
| Trigger interval | ~56.2 seconds | Same |
| Room handlers | Dispatch table at 0x48630 | Switch statement by room |
| Latches | Memory flags (0x95EB, etc.) | Bool/struct per room |
| Movement | Animation movement flags | `applySpriteMovement()` |

## Related Files

- `ANIMATION_MOVEMENT_DOCUMENTATION.md` - Movement flag system details
- `Z_ORDER_SYSTEM_DOCUMENTATION.md` - Sprite depth sorting
- `HIDDEN_SPRITE_TIMING.md` - Original analysis notes
