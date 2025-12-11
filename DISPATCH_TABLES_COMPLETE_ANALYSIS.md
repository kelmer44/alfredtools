# Complete Dispatch Table Analysis - Alfred Pelrock Game Engine

## Overview

The Alfred Pelrock game engine uses **three main dispatch tables** to handle room-specific behaviors. Each table serves a distinct purpose in the game's architecture and is called at different points in the game loop.

---

## Summary of Dispatch Tables

| Table Name | Virtual Address | File Offset | Purpose | Called From | Timing |
|------------|----------------|-------------|---------|-------------|---------|
| **Room Init** | `0x484e4` | `0x4b6e4` | Room initialization logic | `load_room_data()` | Once per room load |
| **Palette Cycling** | `0x486a4` | `0x4b8a4` | Animated palette effects | `load_room_data()` | Setup once, runs per frame |
| **Passing Sprites** | `0x48630` | `0x4b830` | Background animations | `render_scene()` | Every frame when active |

---

## Table 1: Room Initialization Dispatch (0x484e4)

### Purpose
This table handles **room-specific initialization** when a room is first loaded. It customizes sprite setup, scaling parameters, graphics pointers, and other room-specific configurations.

### Technical Details
- **Virtual Address**: `0x484e4`
- **File Offset**: `0x4b6e4`
- **Entry Format**: 6 bytes - `[u16 room_number][u32 function_pointer]`
- **Terminator**: `0xFFFF`
- **Called From**: `load_room_data()` at offset `0x15aac-0x15aeb`

### How It Works
1. When a room loads, `load_room_data()` iterates through this table
2. Compares each `room_number` with `current_room_number` at `[0x4fb94]`
3. When match found, calls the handler via `CALL dword ptr [EDX + 0x484e6]`
4. After handler returns, exits the dispatch loop

### Important Note
**All handlers are EMBEDDED within `load_room_data()`** - they are not separate functions but mid-function entry points. Handlers execute specific setup code and then RET back to the dispatch loop.

### Rooms with Custom Initialization (35 rooms)

| Room(s) | Handler Address | Purpose/Notes |
|---------|----------------|---------------|
| 0, 4 | `0x1561F` | General initialization - falls through to standard setup |
| 2 | `0x15C22` | Special mode for room transitions |
| 3 | `0x15889` | Skip scaling calculation, jump directly to sprite setup |
| 5 | `0x15A3D` | Player sprite setup |
| 7 | `0x1587A` | Disable scaling (sets scale_min=0, scale_max=0) |
| 9 (first) | `0x158BD` | Scaling calculation setup |
| 9 (second) | `0x15A7F` | Secondary dispatch comparison |
| 12 | `0x15C49` | Near-end-of-function initialization |
| 13, 17, 19 | `0x15BEC` | Shared handler for these three rooms |
| 13 (also) | `0x15C68` | Alternative handler for room 13 |
| 19 (also) | `0x15A68` | Alternative handler near dispatch loop |
| 22 | Handler TBD | Custom initialization |
| 24 | `0x15A96` | Post-dispatch setup |
| 26 | `0x15BB7` | Late initialization |
| 27 | `0x15B5B` | Palette/render call |
| 28 | `0x158E1` | Scaling setup |
| 30 | `0x15959` | Standard sprite pointer setup (4 pointers with offsets) |
| 32 | `0x15B07` | Render setup |
| 34 | Handler TBD | Custom initialization |
| 36 | `0x1592B` | Pre-sprite setup |
| 37 | Handler TBD | Custom initialization |
| 38 | `0x15AAD` | Pre-render setup |
| 39, 40 | `0x15BA5` | Shared handler |
| 41 | `0x15AF0` | Post-dispatch setup |
| 48 | `0x15994` | Room 55 special sprite offsets |
| 49 | Handler TBD | Custom initialization |
| 50 | Handler TBD | Custom initialization |
| 51-54 | `0x159E9` | Shared handler for all four rooms - sprite position setup |

### Key Handler Examples

#### Room 7 Handler - Disable Scaling
```asm
0x1587a: XOR    DH, DH
0x1587d: MOV    byte ptr [0x0004967e], DH  ; scale_min = 0
0x15883: MOV    byte ptr [0x0004967f], DH  ; scale_max = 0
0x15889: JMP    0x00015909                 ; Continue to sprite setup
```
Sets both scaling variables to 0 (no sprite scaling in room 7).

#### Room 30 Handler - Standard Sprite Setup
```asm
0x15959: MOV    EAX, [0x0004fa94]           ; Get base graphics pointer
0x1595d: MOV    [0x0004f7b4], EAX           ; sprite_ptr_1 = base
0x15962: LEA    EDX, [EAX + 0xb6e2]         ; sprite_ptr_2 = base + 0xb6e2
```
Sets up 4 sprite pointers with fixed offsets from base graphics memory.

#### Rooms 51-54 Handler - Shared Position Setup
```asm
0x159e9: MOV    DX, word ptr [0x0004fb96]
0x159ef: MOV    word ptr [EAX*0x2 + 0x4f928], DX
```
Sets up sprite position data, shared by all 4 rooms (51, 52, 53, 54).

### Rooms WITHOUT Custom Handlers
These rooms use only the default initialization path:
1, 6, 8, 10, 11, 14, 15, 16, 18, 20, 21, 23, 25, 29, 31, 33, 35, 42-47, 55+

---

## Table 2: Palette Cycling Dispatch (0x486a4)

### Purpose
This table configures **animated palette effects** for rooms that have color-cycling animations (like neon signs, flickering lights, rotating colors).

### Technical Details
- **Virtual Address**: `0x486a4`
- **File Offset**: `0x4b8a4`
- **Entry Format**: 6 bytes - `[u16 room_number][u32 config_pointer]`
- **Terminator**: `0xFFFF`
- **Called From**: `load_room_data()` at offset `0x15a55-0x15a9e`

### How It Works
1. When room loads, `load_room_data()` scans this table for matching room number
2. If match found:
   - Sets `DAT_0004f8ea = 1` (enables palette cycling)
   - Sets `DAT_0004f8ec = config_pointer` (pointer to 12-byte config)
3. Every frame, `update_palette_cycling()` reads the config and updates VGA palette

### Palette Cycling Configuration Format (12 bytes)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0 | 1 | Palette Index/Start | For mode 1: single index; mode 2+: start of range |
| +1 | 1 | Mode/Count | Mode 1 = fade, 2+ = rotate N entries |
| +2 | 1 | Current/State R | Current red value or state |
| +3 | 1 | Delay/State G | Delay between steps or state |
| +4 | 1 | State B | Blue state value |
| +5 | 1 | Min/Param R | Minimum red (fade) or parameter |
| +6 | 1 | Min/Param G | Minimum green or parameter |
| +7 | 1 | Min/Param B | Minimum blue or parameter |
| +8 | 1 | Max/Param R | Maximum red or parameter |
| +9 | 1 | Max/Param G | Maximum green or parameter |
| +10 | 1 | Max/Param B | Maximum blue or parameter |
| +11 | 1 | Flags | Speed, direction, control flags |

### Rooms with Palette Cycling (13 rooms)

| Room | Config Address | Animation Description |
|------|---------------|----------------------|
| 0 | `0x0004b88c` | **City lights** - 6-color rotation for window lights |
| 2 | `0x0004b860` | **McDowells sign** - Green fade effect on restaurant logo |
| 9 | Config TBD | Office palette animation |
| 17 | Config TBD | Palette effect |
| 18 | Config TBD | Palette effect |
| 19 | Config TBD | Palette effect |
| 21 | Config TBD | Desert palette effect |
| 25 | Config TBD | Palette effect |
| 32 | Config TBD | Palette effect |
| 33 | Config TBD | Palette effect |
| 38 | Config TBD | Palette effect |
| 39 | Config TBD | Palette effect |
| 46 | Config TBD | Palette effect |

### Detailed Examples

#### Room 2: McDowells Sign (Fade Mode)
**Config Location**: `0x4b860`
**Raw Data**: `fa 01 24 2c 08 0c 14 08 24 2c 08 05`

| Field | Value | Description |
|-------|-------|-------------|
| Palette Index | 250 (0xFA) | Color entry to animate |
| Mode | 1 | Fade mode |
| Min RGB (6-bit) | (12, 20, 8) | Dark green: (48, 80, 32) in 8-bit |
| Max RGB (6-bit) | (36, 44, 8) | Bright green: (144, 176, 32) in 8-bit |
| Flags | 0x05 | Speed=5, fading up |

**Visual Effect**: Restaurant sign smoothly pulses between dark and bright green.

#### Room 0: City Lights (Rotate Mode)
**Config Location**: `0x4b88c`
**Raw Data**: `c8 06 00 5a e0 04 00 04 67 07 00 01`

| Field | Value | Description |
|-------|-------|-------------|
| Palette Start | 200 (0xC8) | First color in range |
| Mode | 6 | Rotate 6 consecutive entries (200-205) |
| Delay | 90 (0x5A) | ~5 seconds @ 18 FPS |
| Flags | 0x01 | Control flags |

**Visual Effect**: Building windows visible through bedroom window turn on/off by rotating through the 6-color palette range.

### Animation Modes

- **Mode 1 (Fade)**: Single palette entry smoothly transitions between min and max RGB values
- **Mode 2-255 (Rotate)**: Mode value = number of consecutive palette entries to cycle
  - Colors shift through palette indices creating rotation effect
  - Example: Mode 6 rotates 6 consecutive colors

---

## Table 3: Passing Sprite Dispatch (0x48630)

### Purpose
This table handles **"passing by" background animations** - NPCs or objects that periodically move across the screen to add atmosphere (mouse, camel, cars, etc.).

### Technical Details
- **Virtual Address**: `0x48630`
- **File Offset**: `0x4b830`
- **Entry Format**: 6 bytes - `[u16 room_number][u32 handler_offset]`
- **Terminator**: `0xFFFF`
- **Called From**: `render_scene()` every frame
- **Handler Relocation**: Raw offset values need `+0x10000` (code segment base) to get actual address

### How It Works
1. Every frame during `render_scene()`, the dispatch loop checks this table
2. If current room matches an entry, calls the room-specific handler
3. Handler checks **frame counter trigger**: `(frame_counter & 0x3FF) == 0x3FF`
   - Fires every 1024 frames (~56 seconds at 18.2 Hz)
4. When trigger fires, handler enables sprite and starts animation
5. Some rooms use **latch flags** to prevent re-triggering until animation completes

### Frame Counter System
```c
// Global frame counter - increments every frame (~18.2 Hz)
// NEVER RESET - runs continuously from game start
uint32 game_frame_counter = 0;

// Trigger condition - fires every 1024 frames (~56 seconds)
bool is_passing_sprite_trigger() {
    return (game_frame_counter & 0x3FF) == 0x3FF;
}
```

**Key Points**:
- Counter runs at DOS timer rate: 18.2 Hz (55ms per frame)
- Trigger fires when lower 10 bits are all 1s
- Counter is GLOBAL across all rooms
- Overflow safe - the `& 0x3FF` mask uses only bottom 10 bits

### Rooms with Passing Animations (7 rooms)

| Room | Handler Address | Raw Offset | Animation | Has Latch | Latch Variable |
|------|----------------|------------|-----------|-----------|----------------|
| 9 | `0x0001167a` | `0x167a` | **Mouse** running L→R | YES | `0x95EB` |
| 21 | `0x000107c2` | `0x07c2` | **Camel** walking R→L | NO | N/A |
| 29 | `0x00011919` | `0x1919` | Unknown animation | TBD | TBD |
| 31 | `0x00011d66` | `0x1d66` | Unknown animation | TBD | TBD |
| 46 | `0x00011a29` | `0x1a29` | Newspaper/animation | YES | `0x95FA/FB` |
| 47 | `0x00011b41` | `0x1b41` | Unknown animation | TBD | TBD |
| 50 | `0x00011c4e` | `0x1c4e` | Unknown animation | TBD | TBD |

### Detailed Handler Examples

#### Room 21: Desert Camel (Simple - No Latch)

**Handler**: `0x000107c2`
**Behavior**: Camel walks across background from right to left every ~56 seconds

```c
void room21_update_camel() {
    // Check frame counter every frame
    if (is_passing_sprite_trigger()) {
        Sprite *camel = get_sprite(CAMEL_SPRITE_ID);  // Usually sprite 3
        camel->x = 639;           // Start at right edge
        camel->enabled = true;
        camel->scale = 100;       // Full size
        camel->animation_state = WALKING;
    }

    // Check if camel exited left
    Sprite *camel = get_sprite(CAMEL_SPRITE_ID);
    if (camel->enabled && camel->x < 0) {
        camel->enabled = false;
    }
}
```

**No latch needed** - camel takes <56 seconds to cross screen, so new camel won't trigger until current one is gone.

#### Room 9: Office Mouse (Complex - With Latch)

**Handler**: `0x0001167a`
**Latch Variable**: `0x95EB`
**Behavior**: Mouse runs across floor from left to right every ~56 seconds

```c
struct {
    bool mouse_latch;  // At 0x95EB - prevents re-trigger while visible
} room9_state;

void room9_update_mouse() {
    // Frame counter trigger
    if (is_passing_sprite_trigger()) {
        // Only trigger if latch is clear
        if (!room9_state.mouse_latch) {
            room9_state.mouse_latch = true;  // Set latch

            Sprite *mouse = get_sprite(MOUSE_SPRITE_ID);  // Usually sprite 2
            mouse->x = 0;              // Start at left edge
            mouse->y = 210;            // Near bottom of screen
            mouse->enabled = true;
            start_sprite_animation(mouse, MOUSE_RUN_SEQUENCE);
        }
    }

    // Check if mouse exited right - clear latch
    Sprite *mouse = get_sprite(MOUSE_SPRITE_ID);
    if (mouse->enabled && mouse->x > 355) {
        room9_state.mouse_latch = false;  // Clear latch
        mouse->enabled = false;
    }
}
```

**Latch required** - prevents multiple triggers before mouse completes journey.

#### Rooms 46, 47, 50: Shared Latch Pattern

**Latch Variables**:
- `0x95FA` - Counter (increments each frame)
- `0x95FB` - Latch flag (prevents re-trigger)

```c
struct {
    uint8 counter;   // Increments each frame, triggers at >100
    bool latch;      // Prevents re-trigger until sprite exits
} passing_anim_latch;

void room46_update_passing() {
    if (passing_anim_latch.counter > 100 && !passing_anim_latch.latch) {
        // Trigger animation
        passing_anim_latch.latch = true;
        passing_anim_latch.counter = 0;
        // Start sprite...
    }

    // Always increment counter
    passing_anim_latch.counter++;

    // Clear latch when sprite exits
    Sprite *sprite = get_sprite(SPRITE_ID);
    if (sprite->x <= 40 || sprite->x >= 60000) {
        passing_anim_latch.latch = false;
        passing_anim_latch.counter = 0;
    }
}
```

### Sprite Movement System

Sprites move using **animation movement flags** (16-bit value per animation sequence):

| Bits | Field | Description |
|------|-------|-------------|
| 0-2 | X Amount | Pixels to move per frame (0-7) |
| 3 | X Enable | Enable X movement |
| 4 | X Direction | 0=left, 1=right |
| 5-7 | Y Amount | Pixels to move per frame (0-7) |
| 8 | Y Direction | 0=up, 1=down |
| 9 | Y Enable | Enable Y movement |

**Example**: Mouse running right would have X_Enable=1, X_Direction=1 (right), X_Amount=3-4 pixels/frame

---

## Key Variables Reference

| Address | Name | Type | Purpose |
|---------|------|------|---------|
| `0x4fb94` | current_room_number | u16 | Current room ID |
| `0x4967e` | scale_min | u8 | Minimum sprite scaling factor |
| `0x4967f` | scale_max | u8 | Maximum sprite scaling factor |
| `0x4f7b4-0x4f7c0` | sprite_ptr_array | u32[4] | 4 pointers to sprite graphics |
| `0x4fa94` | graphics_base | u32 | Base pointer to loaded graphics |
| `0x4f8ea` | palette_cycling_enabled | u8 | 1 = cycling active |
| `0x4f8ec` | palette_cycling_config | u32 | Pointer to 12-byte config |
| `0x95EB` | room9_mouse_latch | bool | Prevents mouse re-trigger |
| `0x95FA` | passing_anim_counter | u8 | Frame counter for rooms 46/47/50 |
| `0x95FB` | passing_anim_latch | bool | Latch for rooms 46/47/50 |

---

## Function Reference

| Function | Address | Purpose |
|----------|---------|---------|
| `load_room_data()` | `0x152f5` | Loads room, dispatches init and palette setup |
| `render_scene()` | Address TBD | Renders room, dispatches passing sprite handlers |
| `update_palette_cycling()` | `0x16804` | Updates VGA palette every frame |
| `main_game_loop()` | Address TBD | Increments frame counter, main game loop |

---

## Implementation Notes for Emulation/Reverse Engineering

### 1. Room Loading Sequence
```
1. load_room_data() is called with room number
2. Load room graphics, backgrounds, sprites
3. Check Table 1 (0x484e4) for custom init handler → execute if found
4. Check Table 2 (0x486a4) for palette config → setup if found
5. Initialize sprite arrays and z-order
6. Continue to render loop
```

### 2. Per-Frame Rendering Sequence
```
1. Increment global frame counter (never reset!)
2. If palette cycling enabled (0x4f8ea == 1):
   → update_palette_cycling() reads config at 0x4f8ec
   → Modifies VGA palette registers
3. render_scene() is called
4. Check Table 3 (0x48630) for current room → call handler if found
5. Handler checks (frame_counter & 0x3FF) == 0x3FF
6. If trigger fires and latch clear → enable sprite, set position
7. Render all enabled sprites with proper z-order
```

### 3. Testing Checklist
- [ ] Verify Room 2 McDowells sign fades green correctly
- [ ] Verify Room 0 city lights rotate (6 colors, ~5 sec delay)
- [ ] Verify Room 21 camel appears every ~56 seconds, walks R→L
- [ ] Verify Room 9 mouse appears every ~56 seconds, runs L→R
- [ ] Verify mouse latch prevents overlapping triggers
- [ ] Verify frame counter is never reset (global state)
- [ ] Verify rooms without handlers use default initialization

---

## Related Documentation

- **`ROOM_DISPATCH_TABLE_ANALYSIS.md`** - Earlier analysis of Table 1 (room init)
- **`PALETTE_CYCLING_OFFSETS.md`** - Detailed palette cycling documentation
- **`SCUMMVM_PASSING_SPRITES_IMPLEMENTATION.md`** - ScummVM implementation guide
- **`Z_ORDER_SYSTEM_DOCUMENTATION.md`** - Sprite rendering and z-order
- **`SPRITE_SCALING.md`** - Sprite scaling system

---

## Discovery Process

This analysis was compiled from:
1. **Ghidra decompilation** of JUEGO.EXE functions
2. **Binary analysis** of dispatch table structures
3. **Runtime observation** of game behavior
4. **Chat history** documenting investigation process
5. **Cross-referencing** multiple documentation files

Last Updated: December 11, 2025
