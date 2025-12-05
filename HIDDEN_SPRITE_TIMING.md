# Hidden Sprite Timing Mechanism

## Overview
Hidden "passing by" sprites (camel in room 21, mouse in room 9) are controlled by
the render_scene dispatch table at virtual address 0x48630.

## Frame Counter Trigger
Both use the same basic trigger formula:
```
if ((frame_counter & 0x3FF) == 0x3FF) { trigger }
```
- Checks every 1024 frames ≈ 56.2 seconds (at 18.2 Hz)
- Frame counter at 0x11738 is NOT reset per room - only at game start
- Entry timing depends on when you entered the room relative to counter

## Camel (Room 21) - Handler at 0x107c2

**NO LATCH FLAG** - simpler mechanism:
1. Frame counter check triggers every ~56 seconds
2. When triggered: sets sprite X position to 639 (right edge)
3. State variable 0x11755 tracks animation progress (0→1→2→3)
4. NO blocking mechanism - will re-trigger every 56 seconds

```c
void room21_camel() {
    if (state == 2) { /* animation step 2 */ }
    if (state == 3) { /* animation step 3 with shadow */ }

    // Always check frame counter
    if ((frame_counter & 0x3FF) == 0x3FF) {
        sprite[0xFD] = 100;    // enable
        sprite[0xE6] = 639;    // X position = right edge
    }
}
```

## Mouse (Room 9) - Handler at 0x1167a

**HAS LATCH FLAG at 0x95EB** - prevents re-trigger:
1. Frame counter check triggers every ~56 seconds
2. Before triggering, checks if latch 0x95EB == 0
3. When triggered: sets latch to 1, enables mouse sprite
4. Latch only resets when mouse X position > 355 (off screen)

```c
void room9_mouse() {
    // Frame counter trigger
    if ((frame_counter & 0x3FF) == 0x3FF) {
        if (latch == 0) {
            latch = 1;          // prevent re-trigger
            sprite[0xD1] = 210; // start animation
        }
    }

    // Latch reset when mouse exits right
    if (sprite[0xBC] > 355) {
        latch = 0;  // allow next trigger
    }
}
```

## Why Variable Delays?

1. **Entry Timing**: Frame counter runs continuously from game start.
   Entering a room at random times means 0-56 second wait until next trigger.

2. **Latch (Mouse only)**: If you enter room 9 while mouse animation is still
   in progress (X ≤ 355), the latch is set. Must wait for:
   - Mouse to finish (reach X > 355)
   - THEN wait for next 56-second cycle

3. **Animation Duration**: Camel/mouse cross the screen, taking several seconds.
   If you leave and re-enter before animation finishes, the timing feels different.

## Dispatch Tables

render_scene dispatch table at 0x48630:
- Room 21 → 0x107c2 (camel)
- Room 9 → 0x1167a (mouse)
- Room 29 → 0x11919
- Room 46 → 0x11a29
- Room 47 → 0x11b41
- Room 50 → 0x11c4e
- Room 31 → 0x11d66

All "passing by" animations share similar frame counter logic.

## Key Memory Addresses

| Address | Description |
|---------|-------------|
| 0x11738 | Frame counter (18.2 Hz, only reset at game start) |
| 0x11755 | Camel animation state (0→1→2→3) |
| 0x95EB  | Mouse trigger latch flag |
| 0xFAC8  | Pointer to sprite array |
| 0x48630 | render_scene dispatch table |

## Explaining 2+ Minute Delays

Your observation of 2+ minute delays is explained by the combination of:

1. **Random entry point**: You enter room at some random frame count
2. **Just missed trigger**: If you entered just after (counter & 0x3FF) == 0x3FF,
   you must wait almost the full 56 seconds
3. **Latch blocking (mouse)**: If the mouse animation started before you entered,
   the latch prevents new triggers until mouse finishes AND next 56-sec cycle hits

Maximum possible wait = ~112 seconds (2 full cycles) if:
- You enter just after a trigger fired
- Latch was set from previous animation
- Must wait for latch clear + next trigger
