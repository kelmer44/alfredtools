# Room Initialization Dispatch Table Documentation

## Overview

When loading a room in Alfred Pelrock, the game uses a dispatch table to execute room-specific initialization code. This table is located at address `0x484e4` in JUEGO.EXE.

## Table Format

```
struct RoomInitEntry {
    uint16_t room_number;    // Room ID (0-55), or 0xFFFF for terminator
    uint32_t handler_addr;   // Address of handler code
};
// Each entry is 6 bytes
```

The dispatch lookup happens in `load_room_and_init_alfred` at address `0x15aca`:

```c
// Pseudo-code for dispatch lookup
for (int i = 0; room_init_dispatch_table[i].room_number != 0xFFFF; i++) {
    if (room_init_dispatch_table[i].room_number == current_room_number) {
        room_init_dispatch_table[i].handler();
        break;
    }
}
```

## Important Architecture Note

**The handlers are NOT separate functions.** They are entry points within the monolithic `load_room_and_init_alfred` function (0x152f5-0x15c90). When a handler is called, execution enters mid-function and continues through the remaining code until returning.

This means:
- Handlers "skip" earlier parts of the initialization
- Some rooms share handlers (e.g., Room 0 and Room 4)
- Rooms without handlers (like Room 1) run the full default initialization

## Rooms 0-5 Handler Summary

| Room | Handler Address | Has Handler | Description |
|------|-----------------|-------------|-------------|
| 0    | 0x1561F         | ✅ YES      | Generic init after Room 3 text handling |
| 1    | N/A             | ❌ NO       | Uses full default initialization |
| 2    | 0x15C22         | ✅ YES      | Special VGA/palette setup |
| 3    | 0x15889         | ✅ YES      | Skip scaling calculation |
| 4    | 0x1561F         | ✅ YES      | Same as Room 0 |
| 5    | 0x15A3D         | ✅ YES      | Player sprite render setup |

## Detailed Handler Analysis

### Room 0 & Room 4: Generic Handler (0x1561F)

These rooms use a shared handler that enters after the Room 3 specific text manipulation code.

**What it does:**
- Skips Room 3 text swap logic
- Continues with standard sprite position data loading
- Sets up conversation pointers normally

**Code context:**
```asm
; Room 3 specific code above (0x15601-0x15635)
; Handler entry point:
0001561F: MOV ESI,dword ptr [0x0004fab0]  ; sprite_position_data_ptr
```

**ScummVM Implementation:** No special handling needed. These rooms use standard initialization.

---

### Room 1: No Handler (Default Initialization)

Room 1 has NO dispatch table entry and runs the complete `load_room_and_init_alfred` function.

**ScummVM Implementation:** Standard room loading, no special cases.

---

### Room 2: VGA Register Setup (0x15C22)

This handler enters during the `room_load_mode == 1` section, specifically at the VGA register configuration.

**What it does:**
- Sets up VGA video registers for palette animation
- Configures display mode 0x12
- Initializes palette base address

**Code:**
```asm
00015C22: MOV EBX,0x4fb54                 ; VGA state buffer address
00015C26: MOV EAX,0x10                    ; INT 10h video services
00015C2B: CALL set_video_registers
00015C30: MOV byte ptr [0x0004fb3c],0x36  ; Palette register value
00015C37: MOV byte ptr [0x0004fb38],0x1   ; Video mode flag
00015C3E: MOV byte ptr [0x0004fb39],0x12  ; Mode 0x12 (640x480 16-color VGA)
```

**Purpose:** Room 2 (McDowells restaurant scene) has animated elements like neon signs that require palette cycling. This handler sets up the correct VGA mode for those effects.

**ScummVM Implementation:** 
```cpp
if (roomNumber == 2) {
    // Enable palette cycling for neon sign animation
    _paletteCyclingEnabled = true;
    // Room 2 specific VGA setup (if needed)
}
```

---

### Room 3: Skip Scaling Calculation (0x15889)

This handler jumps over the dynamic scaling calculation code.

**What it does:**
- Executes `JMP 0x15909` to bypass scaling computation
- Sets `alfred_scale_x = 0` and `alfred_scale_y = 0` implicitly (not executed)

**Code:**
```asm
00015889: JMP 0x00015909  ; Jump directly to sprite initialization
```

The skipped code (0x1588e-0x15908) calculates Alfred's scale based on Y position:
```c
// SKIPPED CODE for Room 3:
if (alfred_y_position > room_scale_reference_y) {
    alfred_scale_x = 0;
    alfred_scale_y = 0;
} else {
    uint scale = (room_scale_reference_y - alfred_y_position) / scale_divisor;
    alfred_scale_y = scale;
    alfred_scale_x = scale >> 1;
}
```

**Purpose:** Room 3 doesn't use dynamic perspective scaling. Alfred's sprite size remains constant regardless of Y position.

**ScummVM Implementation:**
```cpp
if (roomNumber == 3) {
    // Skip dynamic scaling calculation
    // Use fixed scale or no scaling
    _alfredScaleX = 0;  // Or a fixed value
    _alfredScaleY = 0;
}
```

---

### Room 5: Sprite Render Configuration (0x15A3D)

This handler configures Alfred's rendering state after the scaling calculation.

**What it does:**
- Sets `alfred_scale_factor` based on Y position formula
- Enables `alfred_render_enabled = 1`
- Clears `palette_cycling_flag = 0`

**Code:**
```asm
00015A3D: MOV byte ptr [EAX*0x2 + 0x4f930],DL  ; alfred_scale_factor
00015A44: MOV byte ptr [EAX*0x2 + 0x4f931],0x1 ; alfred_render_enabled
00015A4C: XOR AL,AL
00015A4E: MOV [0x0004f8ea],AL                   ; Clear palette_cycling_enabled
```

**Scale factor formula:**
```c
alfred_scale_factor = ((399 - alfred_y_position) & 0xFFFE) >> 1) + 10;
```

**Purpose:** Room 5 has specific sprite rendering requirements and explicitly disables any palette cycling from previous rooms.

**ScummVM Implementation:**
```cpp
if (roomNumber == 5) {
    _alfredRenderEnabled = true;
    _paletteCyclingEnabled = false;
    _alfredScaleFactor = ((399 - _alfredYPosition) & 0xFFFE) / 2 + 10;
}
```

---

## Complete Dispatch Table (Known Entries)

Based on the decompilation, here are additional rooms with handlers:

| Room | Handler | Notes |
|------|---------|-------|
| 0    | 0x1561F | Generic |
| 2    | 0x15C22 | VGA setup |
| 3    | 0x15889 | Skip scaling |
| 4    | 0x1561F | Same as Room 0 |
| 5    | 0x15A3D | Sprite setup |
| 7    | 0x1587A | Unknown |
| 9    | 0x158BD | Unknown |
| 12   | 0x15C49 | Unknown |
| 13   | 0x15C68 | Unknown |
| ...  | ...     | Additional entries |
| 0xFFFF | N/A   | Table terminator |

## Other Dispatch Tables

The game uses three other dispatch tables for room-specific behavior:

1. **palette_cycling_dispatch_table** (0x486a4) - Per-frame palette animation
2. **render_scene_dispatch_table** (0x48630) - Background animation rendering  
3. **main_loop_dispatch_table** (0x485bc) - Main game loop callbacks

## Related Variables

| Address | Name | Type | Description |
|---------|------|------|-------------|
| 0x4967e | alfred_scale_x | byte | X-axis scaling factor |
| 0x4967f | alfred_scale_y | byte | Y-axis scaling factor |
| 0x4fb94 | current_room_number | word | Currently loaded room |
| 0x4f8ea | palette_cycling_enabled | byte | 1 if palette cycling active |
| 0x4f930 | alfred_scale_factor | byte | Depth-based scale factor |
| 0x4f931 | alfred_render_enabled | byte | 1 if Alfred should render |

## ScummVM Implementation Strategy

For ScummVM, implement room handlers as a switch statement:

```cpp
void PelrockEngine::executeRoomInitHandler(int roomNumber) {
    switch (roomNumber) {
    case 0:
    case 4:
        // Generic initialization - no special handling
        break;
    
    case 2:
        // McDowells - enable palette cycling for neon signs
        _paletteCyclingEnabled = true;
        break;
    
    case 3:
        // Skip dynamic scaling
        _alfredScaleX = 0;
        _alfredScaleY = 0;
        break;
    
    case 5:
        // Sprite render setup
        _alfredRenderEnabled = true;
        _paletteCyclingEnabled = false;
        calculateAlfredScaleFactor();
        break;
    
    // Room 1 and others: default initialization
    default:
        // Standard scaling calculation
        calculateDynamicScaling();
        break;
    }
}
```
