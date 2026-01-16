# Complete Dispatch Table Analysis - Alfred Pelrock Game Engine

## Overview

The Alfred Pelrock game engine uses **four main dispatch tables** to handle room-specific behaviors. Each table serves a distinct purpose in the game's architecture and is called at different points in the game loop.

---

## Summary of Dispatch Tables

| Table Name | Virtual Address | File Offset | Purpose | Called From | Timing |
|------------|----------------|-------------|---------|-------------|---------|
| **Room Init** | `0x484e4` | `0x4b6e4` | Room initialization logic | `load_room_data()` | Once per room load |
| **Palette Cycling** | `0x486a4` | `0x4b8a4` | Animated palette effects | `load_room_data()` | Setup once, runs per frame |
| **Passing Sprites** | `0x48630` | `0x4b830` | Background animations | `render_scene()` | Every frame when active |
| **Main Loop Events** | `0x485bc` | `0x4b7bc` | Room-specific per-frame logic | `main_game_loop()` | Every frame |

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
| 2 | `0x15C22` | **TBD** - Handler address to be analyzed |
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

#### Room 2 Handler - To Be Analyzed
**Handler**: `0x15C22` (within `load_room_data`)

**Note**: The actual room 2 handler needs further analysis.

However, there IS interesting code at `0x15BB0-0x15C8D` that runs for ALL rooms when game mode (`0x52ffd`) equals 1. This code checks if the previous room was 0x1C (28) and if so, loads a special **palette** (768 bytes = 256 colors × 3 bytes RGB):

```asm
00015BC0: XOR    EAX, EAX
00015BC2: MOV    AL, [0x0005178c]        ; Previous room number
00015BC7: CMP    EAX, 0x1C               ; Was it room 28?
00015BCA: JNZ    0x00015BFA              ; Skip if not

; Load alternative palette from ALFRED.7 (at runtime memory 0x1610ce)
00015BD9: MOV    EDX, 0x1610ce           ; Palette data location
00015BEE: MOV    EDX, 0x300              ; 768 bytes (VGA palette)
```

**Purpose**: When leaving room 28 (likely after picking up an object or triggering an event), the game loads an **alternative palette** for the next room, creating a visual state change. This is a narrative/game-state technique - the world looks different after certain events in room 28.

**Technical**: 768 bytes = 256 VGA palette entries × 3 bytes (RGB), loaded from ALFRED.7 into runtime memory at `0x1610ce`.

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
| 9 | Config TBD | Office palette animation | shiny stuff
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

| Room | Handler Address | Raw Offset | Animation | Trigger Type | Counter/Latch |
|------|----------------|------------|-----------|--------------|---------------|
| 21 | `0x000107c2` | `0x07c2` | **Camel** R→L | frame_counter & 0x3FF | None (simple) |
| 9 | `0x0001167a` | `0x167a` | **Mouse** L→R | frame_counter & 0x3FF | `0x95EB`, `0x964E` |
| 29 | `0x00011919` | `0x1919` | **Background sprite** bidirectional | counter > 150 | `0x95F5-0x95F9` |
| 31 | `0x00011d66` | `0x1d66` | **Background sprite** X:63→268 | counter > 200 | `0x9624-0x9625` |
| 46 | `0x00011a29` | `0x1a29` | **Background sprite** bidirectional | counter > 250 | `0x95FA-0x95FE` |
| 47 | `0x00011b41` | `0x1b41` | **Background sprite** bidirectional | counter > 200 | `0x95FF-0x9603` |
| 50 | `0x00011c4e` | `0x1c4e` | **Background sprite** bidirectional | counter > 200 | `0x961E-0x9622` |

### Sprite Offset Fields (at sprite_data_ptr + offset)

| Offset | Field | Description |
|--------|-------|-------------|
| +0xBA | X position (slot 0) | 16-bit X coordinate |
| +0xD0 | Animation state (slot 0) | Current animation frame |
| +0xD1 | Animation ID (slot 0) | Animation sequence to play |
| +0xE6 | X position (slot 1) | 16-bit X coordinate |
| +0xFD | Animation ID (slot 1) | Animation sequence to play |
| +0x112 | X position (slot 2) | 16-bit X coordinate |
| +0x129 | Animation ID (slot 2) | Animation sequence to play |

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

## Table 4: Main Game Loop Dispatch (0x485bc)

### Purpose
This table handles **room-specific per-frame logic** called from `main_game_loop()`. Unlike the passing sprite table, this handles various room-specific behaviors: cutscene triggers, one-shot events, periodic ambient events, and complex state machines.

### Technical Details
- **Virtual Address**: `0x485bc`
- **File Offset**: `0x4b7bc`
- **Entry Format**: 6 bytes - `[u16 room_number][u32 handler_offset]`
- **Terminator**: `0xFFFF`
- **Called From**: `main_game_loop()` at address `0x103dd` every frame
- **Handler Relocation**: Raw offset values need `+0x10000` (code segment base)

### Table Location in Code
```asm
; main_game_loop at 0x10337
; Dispatch call at 0x103dd:
mov  eax, dword ptr [passing_sprite_dispatch_table + 0x14]  ; Note: +0x14 offset from 0x48630
                                                              ; = 0x48630 + 0x14 = actual 0x485bc
```

### Room Entries (18 entries)

| Room | Handler | Raw Offset | Purpose |
|------|---------|------------|---------|
| 1 | `0x000118ad` | `0x18ad` | Shared handler - ambient events |
| 2 | `0x000118ad` | `0x18ad` | Shared handler - ambient events |
| 3 | `0x000118ad` | `0x18ad` | Shared handler - ambient events |
| 8 | `0x000118ad` | `0x18ad` | Shared handler - ambient events |
| 12 | `0x000118ad` | `0x18ad` | Shared handler - ambient events |
| 14 | `0x000118ad` | `0x18ad` | Shared handler - ambient events |
| 17 | `0x000118ad` | `0x18ad` | Shared handler - ambient events |
| 15 | `0x00011de5` | `0x1de5` | One-shot flag event |
| 19 | `0x000115ef` | `0x15ef` | TBD |
| 24 | `0x00025cd7` | `0x15cd7` | TBD (note: different segment) |
| 26 | `0x0001087c` | `0x087c` | Periodic ambient event |
| 30 | `0x0001094b` | `0x094b` | Inventory item check |
| 36 | `0x0001098f` | `0x098f` | Complex cutscene trigger |
| 48 | `0x00010d4c` | `0x0d4c` | Dialog/cutscene sequence |
| 51 | `0x000113dc` | `0x13dc` | Shared handler |
| 52 | `0x000113dc` | `0x13dc` | Shared handler |
| 53 | `0x000113dc` | `0x13dc` | Shared handler |
| 54 | `0x000113dc` | `0x13dc` | Shared handler |

### Shared Handler Pattern (Rooms 1,2,3,8,12,14,17)

The shared handler at `0x118ad` fires every ~7.5 minutes using a different frame counter mask:

```c
// Trigger condition for shared handler
// Fires every 8192 frames (~7.5 minutes at 18.2 Hz)
bool is_ambient_trigger() {
    return (game_frame_counter & 0x1FFF) == 0x1FFF;
}
```

These rooms likely share common ambient sound/animation events (e.g., periodic bird sounds, clock chimes).

### Key Handler Behaviors

#### Room 15: One-Shot Event
- **Handler**: `0x11de5`
- **Latch**: `0x9653`
- **Behavior**: Fires once when entering room, sets flag to prevent re-trigger

#### Room 30: Inventory Check
- **Handler**: `0x1094b`
- **Check**: `inventory_array + 0x63`
- **Behavior**: Triggers event when player has specific inventory item

#### Room 36: Complex Cutscene
- **Handler**: `0x1098f`
- **Behavior**: Multi-stage state machine for cutscene triggering

#### Rooms 51-54: Shared Handler
- **Handler**: `0x113dc`
- **Behavior**: Shared logic for related rooms (possibly same location)

---

## Rooms 0-15 Per-Frame Handler Coverage

This section summarizes which rooms in the 0-15 range have per-frame handlers in Tables 3 and 4.

| Room | Table 3 (Passing Sprites) | Table 4 (Main Loop) | Notes |
|------|--------------------------|---------------------|-------|
| 0 | ❌ None | ❌ None | City lights via palette cycling only |
| 1 | ❌ None | ✅ `0x118ad` (shared) | Ambient events every ~7.5 min |
| 2 | ❌ None | ✅ `0x118ad` (shared) | Ambient events every ~7.5 min |
| 3 | ❌ None | ✅ `0x118ad` (shared) | Ambient events every ~7.5 min |
| 4 | ❌ None | ❌ None | - |
| 5 | ❌ None | ❌ None | - |
| 6 | ❌ None | ❌ None | - |
| 7 | ❌ None | ❌ None | - |
| 8 | ❌ None | ✅ `0x118ad` (shared) | Ambient events every ~7.5 min |
| 9 | ✅ `0x1167a` (mouse) | ❌ None | Mouse runs L→R every ~56 sec |
| 10 | ❌ None | ❌ None | - |
| 11 | ❌ None | ❌ None | - |
| 12 | ❌ None | ✅ `0x118ad` (shared) | Ambient events every ~7.5 min |
| 13 | ❌ None | ❌ None | - |
| 14 | ❌ None | ✅ `0x118ad` (shared) | Ambient events every ~7.5 min |
| 15 | ❌ None | ✅ `0x11de5` (one-shot) | Event fires once per room entry |

**Summary for Rooms 0-15:**
- **Table 3**: Only Room 9 has a passing sprite handler (mouse animation)
- **Table 4**: Rooms 1, 2, 3, 8, 12, 14 share ambient handler; Room 15 has one-shot event
- **Neither**: Rooms 0, 4, 5, 6, 7, 10, 11, 13 have no per-frame handlers

---

## Key Variables Reference

| Address | Name | Type | Purpose |
|---------|------|------|---------|
| `0x11738` | game_frame_counter | u32 | Global frame counter (never reset) |
| `0x4fb94` | current_room_number | u16 | Current room ID |
| `0x4967e` | scale_min | u8 | Minimum sprite scaling factor |
| `0x4967f` | scale_max | u8 | Maximum sprite scaling factor |
| `0xFAC8` | sprite_data_ptr | u32 | Base pointer to sprite data array |
| `0x4f7b4-0x4f7c0` | sprite_ptr_array | u32[4] | 4 pointers to sprite graphics |
| `0x4fa94` | graphics_base | u32 | Base pointer to loaded graphics |
| `0x4f8ea` | palette_cycling_enabled | u8 | 1 = cycling active |
| `0x4f8ec` | palette_cycling_config | u32 | Pointer to 12-byte config |
| `0x95EB` | room9_mouse_latch | bool | Prevents room 9 mouse re-trigger |
| `0x964E` | room9_mouse_state | u8 | Room 9 mouse animation state |
| `0x95F5-0x95F9` | room29_passing_state | struct | Room 29 passing animation state |
| `0x95FA-0x95FE` | room46_passing_state | struct | Room 46 passing animation state |
| `0x95FF-0x9603` | room47_passing_state | struct | Room 47 passing animation state |
| `0x961E-0x9622` | room50_passing_state | struct | Room 50 passing animation state |
| `0x9624-0x9625` | room31_passing_state | struct | Room 31 passing animation state |
| `0x9653` | room15_oneshot_flag | bool | Room 15 one-shot event flag |

---

## Function Reference

| Function | Address | Purpose |
|----------|---------|---------|
| `main_game_loop()` | `0x10337` | Main game loop, dispatches Table 4 handlers |
| `load_room_data()` | `0x152f5` | Loads room, dispatches init and palette setup |
| `render_scene()` | `0x161fc` | Renders room, dispatches Table 3 passing sprite handlers |
| `update_palette_cycling()` | `0x16804` | Updates VGA palette every frame |

### Handler Code Region

All Table 3 and Table 4 handlers are located in an **undefined code region** between:
- **Start**: `0x107c2` (first handler - room 21 camel)
- **End**: `0x11e25` (last handler ends before `init_sprite_scaling_tables`)

This region contains 22+ handlers that are NOT defined as functions in Ghidra.

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

### 2. Per-Frame Main Loop Sequence
```
1. main_game_loop() at 0x10337 is called
2. Increment global frame counter at 0x11738 (NEVER reset!)
3. Check Table 4 (0x485bc) for current room → call handler if found
   → Handles cutscenes, inventory checks, ambient events
   → Some handlers use (frame_counter & 0x1FFF) == 0x1FFF (~7.5 min trigger)
4. Process input, update game state
5. Call render_scene() at 0x161fc
```

### 3. Per-Frame Rendering Sequence
```
1. render_scene() is called from main loop
2. If palette cycling enabled (0x4f8ea == 1):
   → update_palette_cycling() reads config at 0x4f8ec
   → Modifies VGA palette registers
3. Check Table 3 (0x48630) for current room → call handler if found
4. Handler checks (frame_counter & 0x3FF) == 0x3FF (~56 sec trigger)
5. If trigger fires and latch clear → enable sprite, set position
6. Render all enabled sprites with proper z-order
```

### 4. Testing Checklist

**Table 2 - Palette Cycling:**
- [ ] Verify Room 2 McDowells sign fades green correctly
- [ ] Verify Room 0 city lights rotate (6 colors, ~5 sec delay)

**Table 3 - Passing Sprites:**
- [ ] Verify Room 21 camel appears every ~56 seconds, walks R→L
- [ ] Verify Room 9 mouse appears every ~56 seconds, runs L→R
- [ ] Verify Room 29 background animation triggers at counter > 150
- [ ] Verify Room 31 sprite moves X:63→268
- [ ] Verify Room 46 animation triggers at counter > 250
- [ ] Verify Room 47 animation triggers at counter > 200
- [ ] Verify Room 50 animation triggers at counter > 200
- [ ] Verify latch flags prevent overlapping triggers

**Table 4 - Main Loop Events:**
- [ ] Verify Rooms 1,2,3,8,12,14,17 shared handler fires every ~7.5 min
- [ ] Verify Room 15 one-shot event only fires once
- [ ] Verify Room 30 inventory item check works correctly
- [ ] Verify Room 36 cutscene trigger state machine

**General:**
- [ ] Verify frame counter at 0x11738 is never reset (global state)
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
