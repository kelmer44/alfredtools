# Alfred Pelrock Timing System Documentation

## ⚠️ CRITICAL CORRECTION (v2)

**Previous analysis was WRONG about walking speed.** Key insight discovered:

| Game State | Wait Call | Ticks Waited | Effective Rate |
|------------|-----------|--------------|----------------|
| **Idle/Menu** | `process_game_state(0)` | 1 tick | **18.2 FPS** (55ms/frame) |
| **Walking** | `process_game_state(1)` | 2 ticks | **9.1 FPS** (110ms/step) |

**The walking loop runs at HALF the main loop speed!**

- Alfred moves 6 px (X) or 5 px (Y) per **110ms** (not 55ms)
- Walk animation: 8 frames takes **0.88 seconds** (not 0.44s)
- Sprites animate at **18.2 Hz** (main loop rate), NOT walking rate

## Overview

The original Alfred Pelrock game uses the DOS timer interrupt (INT 1Ch) for timing, which fires at **18.2065 Hz** (exactly 1193182 / 65536 Hz). This is NOT CPU-dependent - the game runs at a fixed rate regardless of CPU speed.

## Key Findings

### 1. Master Clock: INT 1Ch at 18.2 Hz

The game initializes the timer interrupt in `game_initialization()`:

```
FUN_00026861("Inicializando timmer ...\n");
open_file_handle_28();
```

The function `open_file_handle_28()` hooks interrupt vector **0x1C** (decimal 28), which is the DOS timer tick interrupt. This interrupt is triggered by the BIOS interrupt handler for INT 08h after each 18.2 Hz tick.

**Exact frequency**: 1,193,182 Hz / 65,536 = **18.2065 Hz**
**Exact tick period**: **54.9254 milliseconds** (~55ms)

### 2. Frame Timing via `process_game_state()`

The critical timing function is `process_game_state(int num_ticks)`:

```c
void process_game_state(int num_ticks)
{
    // Calculate target frame to wait for
    target = frame_counter + num_ticks;

    // Handle overflow protection
    if (target < frame_counter) {
        frame_counter = 0;
        target = num_ticks;
    }

    mouse_button_during_wait = 0;

    // Wait until frame counter EXCEEDS target (not just equals)
    do {
        wait_or_process_input();
        if (mouse_button_held != 0) {
            mouse_button_during_wait = 1;
        }
    } while (frame_counter <= target);  // ⚠️ CRITICAL: Uses <= not <
}
```

**CRITICAL INSIGHT**: The condition is `<=` (less-than-or-equal), which means:
- `process_game_state(0)`: Waits for **1 tick** (loop exits when counter > original value)
- `process_game_state(1)`: Waits for **2 ticks** (loop exits when counter > original+1)

The `frame_counter` is incremented by the INT 1Ch ISR at 18.2 Hz (~55ms per tick).

### 3. Main Game Loop vs Walking Loop Timing

**This is the key insight!**

The **main idle loop** calls `process_game_state(0)`:
```c
void main_game_loop(void) {
    do {
        wait_or_process_input();
        check_keyboard_input();
        process_game_state(0);           // Waits 1 tick (~55ms)
        setup_alfred_frame_from_state();
        render_scene(0);
        // ... handle mouse clicks, hotspots, etc.
    } while (true);
}
```

The **walking loop** calls `process_game_state(1)`:
```c
// Inside walk_to_target_and_execute_queued_action()
do {
    if (*pathNode == -1) goto done;

    process_game_state(1);              // Waits 2 ticks (~110ms)
    // ... calculate scaling ...
    // ... select animation frame ...
    walking_frame_counter++;
    render_scene(0);

    // Move Alfred 6 px horizontally OR 5 px vertically
    if (direction & HORIZONTAL_MOVE) {
        if (direction & LEFT) {
            alfred_x_position -= 6;
        } else {
            alfred_x_position += 6;
        }
    }
    if (direction & VERTICAL_MOVE) {
        if (direction & UP) {
            alfred_y_position -= 5;
        } else {
            alfred_y_position += 5;
        }
    }

    pathNode += 3;
} while (true);
```

**Timing comparison:**
| Loop | Function Call | Wait Time | Effective Rate |
|------|--------------|-----------|----------------|
| Main idle | `process_game_state(0)` | 1 tick | **18.2 FPS** (55ms) |
| Walking | `process_game_state(1)` | 2 ticks | **9.1 FPS** (110ms) |

### 4. Walking Speed

From `walk_to_target_and_execute_queued_action()`:

| Direction | Pixels per Step |
|-----------|-----------------|
| Horizontal (X) | **6 pixels** |
| Vertical (Y) | **5 pixels** |

```c
if ((pcVar5[1] & 2U) != 0) {
    if ((pcVar5[1] & 1U) == 0) {
        alfred_facing_direction = 1;
        alfred_x_position = alfred_x_position - 6;  // LEFT
    } else {
        alfred_facing_direction = 0;
        alfred_x_position = alfred_x_position + 6;  // RIGHT
    }
}
if ((pcVar5[1] & 8U) != 0) {
    if ((pcVar5[1] & 4U) == 0) {
        alfred_facing_direction = 3;
        alfred_y_position = alfred_y_position - 5;  // UP
    } else {
        alfred_facing_direction = 2;
        alfred_y_position = alfred_y_position + 5;  // DOWN
    }
}
```

**Walking speed in real units** (at **9.1 steps/second** due to 110ms wait per step):
- Horizontal: 6 pixels × 9.1 = **~54.6 pixels/second**
- Vertical: 5 pixels × 9.1 = **~45.5 pixels/second**

⚠️ **NOTE**: Previous calculation of 109 px/s was WRONG! The `process_game_state(1)` call waits 2 ticks, effectively halving the rate.

### 5. Walking Animation Frames

Alfred's walking animation cycles through frames:

| Direction | Animation Frames |
|-----------|-----------------|
| Left/Right | **8 frames** (0-7), mask 0x07 |
| Up/Down | **4 frames** (0-3), mask 0x03 |

From the decompiled code:
```c
if (alfred_facing_direction < 2) {
    uVar6 = 7;   // Mask for left/right: 8 frames
} else {
    uVar6 = 3;   // Mask for up/down: 4 frames
}
// Frame index = (walking_frame_counter & mask)
```

**Animation speed**: The walking animation advances **once per walking step** (every 110ms):
- Left/Right: Full cycle = 8 frames × 110ms = **0.88 seconds**
- Up/Down: Full cycle = 4 frames × 110ms = **0.44 seconds**

⚠️ **Previous values were WRONG** - I incorrectly said 18.2 Hz when walking actually runs at 9.1 Hz due to the 2-tick wait.

### 6. Sprite Animation Timing

Sprite structures have timing data at specific offsets:

| Offset | Size | Description |
|--------|------|-------------|
| +0x1C | byte[] | Frame delay (per frame) - how many ticks to wait before advancing |
| +0x20 | byte | Current frame index in sequence |
| +0x2D | byte | Frame delay counter (counts up to delay value) |

Animation update logic from `update_npc_sprite_animations()`:
```c
// Increment delay counter
sprite[0x2D]++;

// Check if delay reached
if (sprite[0x2D] == sprite[0x1C + current_anim_sequence]) {
    sprite[0x20]++;      // Advance to next frame
    sprite[0x2D] = 0;    // Reset counter

    // Check if animation sequence complete
    if (sprite[0x14 + sequence] == sprite[0x20]) {
        // Handle loop or next sequence
    }
}
```

**Sprite animation speed** = `delay_value × 54.9ms`

For a sprite with `speed = 2`: Animation updates every **109.8ms** (2 × 54.9ms)

### 7. Talk/Speech Timing

Talk animations use a different timing mechanism based on text length:

From `display_text_with_voice()`:
```c
// Duration based on text length
if (frame_toggle_flag == 0) {
    duration = (text_length >> 1);  // Half the text length in ticks
}
```

Talk animation alternates between open/closed mouth at 8 ticks for left/right, 4 for up/down:
```c
if (alfred_facing_direction < 2) {
    uVar6 = 0x800;  // 8 frames for left/right talk
} else {
    uVar6 = 0x400;  // 4 frames for up/down talk
}
```

### 8. Idle Animation Timer

The idle hair-combing animation triggers after:
- **300 ticks** of idleness = **16.5 seconds** (300 / 18.2)

Screensaver (sliding puzzle) triggers after:
- **0x442 ticks** (1090 ticks) = **~60 seconds**

```c
if (300 < idle_timer_hair_combing) {
    play_hair_combing_idle_animation();
    idle_timer_hair_combing = 0;
}
if (0x442 < idle_timer_screensaver) {
    screensaver_sliding_puzzle();
    idle_timer_screensaver = 0;
}
```

### 9. Palette Cycling Timing

`update_palette_cycling()` is called once per frame (after `present_frame_to_screen()`). It has its own frame counter:

```c
void update_palette_cycling(void) {
    // Increment frame counter every call
    palette_frame_counter++;

    if (palette_animation_enabled) {
        if (palette_data[1] == 1) {
            // Type 1: Direct color fade (changes every frame)
            // Used for single-color fade effects
        }
        else if (palette_data[3] <= palette_frame_counter) {
            // Type 2: Palette rotation
            // Only triggers when counter exceeds threshold from palette_data[3]
            palette_frame_counter = 0;  // Reset counter
            // ... rotate palette colors ...
        }
    }
}
```

**Key insight**: `palette_data[3]` is the **delay threshold** for palette rotation.
- If `palette_data[3] = 0`: Rotate EVERY frame (~55ms)
- If `palette_data[3] = 5`: Rotate every ~6 frames (~330ms)

**Room 2 (McDowell's)**: If the palette animation appears too fast, check what delay threshold is being loaded from the room's palette cycling data. Each room has its own palette cycling configuration loaded at room entry.

The palette cycling data is room-specific and loaded from a table at `DAT_000486a4`:
```c
// During load_room_and_init_alfred():
if (DAT_000486a4[room_index] == current_room_number) {
    palette_animation_enabled = 1;
    palette_data = DAT_000486a6[room_index];  // Points to palette cycling params
}
```

## ScummVM Implementation Recommendations

### CORRECTED Understanding

The key insight is that **different game states run at different speeds**:

| Game State | Wait Function | Ticks Wait | Frame Rate | Period |
|------------|--------------|------------|------------|--------|
| Idle/Menu | `process_game_state(0)` | 1 tick | 18.2 FPS | 55ms |
| Walking | `process_game_state(1)` | 2 ticks | 9.1 FPS | 110ms |
| Sprites | Per-sprite counter | Variable | Variable | Variable |

### Previous Incorrect Recommendations (IGNORE THESE)

My previous advice was wrong:
- ❌ "Walking animation advances every 18.2 Hz" - **WRONG**, it's every 9.1 Hz (110ms)
- ❌ "Don't divide by 2 for Alfred animations" - **WRONG**, walking SHOULD be twice as slow
- ❌ "Movement at 109 pixels/second" - **WRONG**, it's ~55 pixels/second

### Correct Implementation

1. **Walking Loop Timing**:
   ```cpp
   // Walking should run at HALF the normal frame rate (~110ms per step)
   const int kWalkingTickMs = 110;  // 2x the normal tick

   // OR keep 55ms tick but only advance walking every 2 ticks:
   if (_chrono->getFrameCount() % 2 == 0) {  // Every other tick
       // Move and animate Alfred
   }
   ```

2. **Walking Animation + Movement are COUPLED**:
   ```cpp
   // In the walking loop, these happen together, once per 110ms:
   _alfredState.curFrame++;  // Advance animation frame
   moveAlfredOneStep();       // Move 6px (X) or 5px (Y)
   renderScene();
   ```

3. **Main Idle Loop Timing**:
   ```cpp
   // Idle/menu runs at full 18.2 Hz (55ms)
   const int kIdleTickMs = 55;
   ```

4. **Sprite Animation**:
   Sprites use their OWN timing based on the main loop (18.2 Hz), so:
   ```cpp
   // Each sprite has its own delay counter
   animData.elapsedFrames++;  // Incremented every 55ms
   if (animData.elapsedFrames >= animData.speed) {
       animData.elapsedFrames = 0;
       animData.curFrame++;
   }
   ```

5. **Palette Cycling**:
   ```cpp
   // update_palette_cycling() runs every frame at 18.2 Hz
   // It has its own frame counter and delay threshold per room
   _paletteFrameCounter++;
   if (_paletteFrameCounter > _paletteDelayThreshold) {
       _paletteFrameCounter = 0;
       rotatePalette();
   }
   ```

5. **Movement speed is per-tick, not per-frame of animation**:
   - Move Alfred 6px/5px EVERY game tick
   - Advance animation frame EVERY game tick

### Timing Comparison Table (CORRECTED)

| Feature | Original Value | Notes |
|---------|---------------|-------|
| Tick period | 54.9ms | Base rate from INT 1Ch |
| Idle loop rate | 18.2 FPS | 1 tick wait |
| Walking loop rate | 9.1 FPS | 2 tick wait |
| Alfred walk speed | 6px × 9.1 = ~55 px/s (X), 5px × 9.1 = ~45 px/s (Y) | Per step at 9.1 Hz |
| Walk anim cycle | 0.88s (8 frames L/R), 0.44s (4 frames U/D) | At 9.1 Hz |
| Sprite animation | Per-sprite delay counter × 55ms | Based on 18.2 Hz |
| Palette cycling | Room-specific delay threshold | Based on 18.2 Hz |

### CPU Independence

The original game is **NOT CPU-dependent**. It uses the hardware timer interrupt which fires at a fixed 18.2 Hz regardless of CPU speed. Your ScummVM implementation using `g_system->getMillis()` is correct for achieving CPU independence.

## Movement Flags (Sprites)

Sprite movement is controlled by a 16-bit flags field at offset +0x22 (per frame):

```
Bits 0-2:   Movement amount X (0-7 pixels per frame)
Bit 3:      Enable X movement (0x8)
Bit 4:      X direction (0x10): 0=left, 1=right
Bits 5-7:   Movement amount Y (0xE0, shifted by 5)
Bit 8:      Y direction (0x100): 0=up, 1=down
Bit 9:      Enable Y movement (0x200)
Bits 10-12: Z movement amount (0x1C00, shifted by 10)
Bit 13:     Z direction (0x2000): 0=back, 1=forward
Bit 14:     Enable Z movement (0x4000)
```

## Your Current Implementation Issues

### Issue 1: Same Movement Speed for X and Y
In [types.h](../scummvm/engines/pelrock/types.h#L129):
```cpp
uint16 movementSpeed = 6; // pixels per frame  <- WRONG for Y movement
```

**Fix**: Use different speeds for X (6) and Y (5):
```cpp
uint16 movementSpeedX = 6; // 6 pixels per tick horizontal
uint16 movementSpeedY = 5; // 5 pixels per tick vertical
```

### Issue 2: Sprite Animation Using Global Frame Count Modulo
In [pelrock.cpp](../scummvm/engines/pelrock/pelrock.cpp#L847):
```cpp
if (_chrono->getFrameCount() % animData.speed == 0) {
```

This means animations skip unless frame count is exactly divisible by speed. The original uses per-sprite delay counters.

**Fix**: Use elapsed frames counter:
```cpp
animData.elapsedFrames++;
if (animData.elapsedFrames >= animData.speed) {
    animData.elapsedFrames = 0;
    // advance frame
}
```

### Issue 3: Alfred Walking Speed Divider (CORRECTED)

**Previous analysis was WRONG.** Looking at the actual code:

```cpp
// If you have kAlfredAnimationSpeed = 2 and are checking:
if (_chrono->getFrameCount() % kAlfredAnimationSpeed == 0) {
    // advance animation and movement
}
```

This **IS CORRECT** if your base tick is 55ms! The walking loop runs at half speed (2 ticks = 110ms), so using `% 2` achieves the same effect.

**The issue is NOT the modulo check** - it's that you need to ensure:
1. Both animation AND movement happen in the same modulo check
2. The base tick rate is 55ms (not faster)

### Issue 4: Palette Cycling Speed

If palette cycling on Room 2 is too fast, check:
1. Are you incrementing the palette frame counter every 55ms?
2. Are you respecting the delay threshold from the room's palette data?
3. The threshold is at `palette_data[3]` - if you're ignoring this, rotation happens every frame

## Corrected Timing Values Summary

| Parameter | Original Value | Correct Implementation |
|-----------|---------------|------------------------|
| Base tick | 54.93ms | 55ms ✓ |
| Idle loop | 1 tick (55ms) | Run at 18.2 FPS |
| Walking loop | 2 ticks (110ms) | Run at 9.1 FPS (or 18.2 with % 2) |
| X movement | 6 px/step at 9.1 Hz | 6 px every 110ms |
| Y movement | 5 px/step at 9.1 Hz | 5 px every 110ms |
| Walk anim | 1 frame/step at 9.1 Hz | Advance with movement |
| Sprite anim | Per-sprite counter at 18.2 Hz | Use elapsed frames, not modulo |
| Palette cycle | Room-specific threshold at 18.2 Hz | Respect delay threshold |

## Conclusion

**The key insight is that WALKING runs at HALF the normal frame rate!**

The main game loop calls `process_game_state(0)` → waits 1 tick → **18.2 FPS**
The walking loop calls `process_game_state(1)` → waits 2 ticks → **9.1 FPS**

If Alfred is animating/walking too fast, you're probably running the walking loop at 18.2 FPS instead of 9.1 FPS.

If sprites are too slow, you might be timing them against the walking rate instead of the main loop rate.

If palette cycling is too fast, you're probably ignoring the per-room delay threshold.

### Quick Fix Checklist

1. ☐ Ensure walking loop runs at **110ms** (not 55ms)
2. ☐ Change Y movement speed from 6 to **5** pixels
3. ☐ Sprites run at main loop rate (55ms), not walking rate (110ms)
4. ☐ Use per-sprite elapsed frame counters (not global frame modulo)
5. ☐ Palette cycling: read and use room's delay threshold from palette_data[3]
