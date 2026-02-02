# Statue Palette Fade Animation System

## Overview

When the player uses the **amulet (item 7)** on the **statue (hotspot 353)** in room 7, a palette fade animation transforms the statue's colors from grayish tones to reddish/warm tones.

## Key Addresses

| Description | Memory Address | File Offset |
|------------|----------------|-------------|
| Palette table | 0x49500 | 0x4C700 |
| Fade frame counter | 0x95F4 | - (BSS) |
| Step value array | 0xFC94 | - (BSS) |
| Step counter | 0xFBA2 | - (BSS) |
| F8 handler (action 353) | 0x1215E | 0x1435E |
| Fade handler (renamed in Ghidra) | 0x120E2 | 0x152E2 |
| Palette fade snippets | 0x227B1-0x228B0 | 0x259B1-0x25AB0 |
| Step storage function | 0x25157 | 0x28357 |

## Ghidra Function Names

| Address | Original Name | Renamed To |
|---------|---------------|------------|
| 0x120E2 | init_mouse_and_inventory | **trigger_statue_palette_fade** |

## Palette Table Structure (at file 0x4C700)

```
Offset  Size  Description
------  ----  -----------
0x00    2     X position (368)
0x02    2     Y position (148)
0x04    2     Type (2)
0x06    2     Padding
0x08    16    Palette indices to modify
0x18    48    Source RGB values (16 colors × 3 bytes, 6-bit VGA)
0x48    48    Target RGB values (16 colors × 3 bytes, 6-bit VGA)
```

**Total size: 120 bytes (0x78)**

## Modified Palette Indices

The animation modifies these 16 palette entries:
```
[30, 37, 39, 41, 44, 62, 74, 79, 83, 89, 105, 120, 152, 179, 217, 238]
```

## Color Transformation

| Index | Source (R,G,B) 6-bit | Target (R,G,B) 6-bit | Effect |
|-------|----------------------|----------------------|--------|
| 30 | (44,44,40) | (53,34,23) | Gray → Orange-brown |
| 37 | (36,36,36) | (62,39,3) | Gray → Bright orange |
| 39 | (16,16,16) | (46,5,1) | Dark gray → Dark red |
| 41 | (20,20,20) | (9,3,0) | Gray → Near black |
| 44 | (36,36,32) | (48,22,15) | Gray → Brown |
| 62 | (28,32,28) | (30,16,25) | Gray-green → Purple-brown |
| 74 | (32,32,32) | (63,43,16) | Gray → Golden |
| 79 | (16,16,12) | (60,25,0) | Dark gray → Orange |
| 83 | (16,20,20) | (16,20,20) | No change |
| 89 | (52,52,44) | (63,38,20) | Light gray → Gold |
| 105 | (12,12,12) | (0,0,0) | Dark → Black |
| 120 | (36,40,40) | (36,40,40) | No change |
| 152 | (45,44,40) | (27,6,20) | Gray → Dark magenta |
| 179 | (48,52,44) | (48,52,44) | No change |
| 217 | (24,24,24) | (29,5,0) | Gray → Dark orange |
| 238 | (24,28,28) | (50,13,7) | Gray → Red-orange |

*RGB values are 6-bit VGA (0-63). Multiply by 4 for 8-bit equivalents.*

## Animation Mechanism

### 1. Trigger
When item 7 (amulet) is used on hotspot 353 (statue):
- The F8 handler table entry for action_id 353 calls `trigger_statue_palette_fade` (0x120E2)
- This function initializes Alfred's position and sets various state variables
- Sets a counter at `0x495C4` to **13** (0x0D)

### 2. Per-Frame Processing
The code at `0x227B1-0x228B0` contains 4 code snippets that form the animation loop:

Each snippet:
1. Delays for 12 ticks (PUSH 0xC; CALL delay)
2. Calls step storage function (0x25157) with step value in EAX
3. Optionally calls with a second step value
4. Increments the frame counter at `0x95F4`
5. Compares counter to 4 (CMP EAX, 4)
6. If counter == 4, triggers conversation

### 3. Step Values
The animation uses these palette step indices:

| Snippet | Address | Step 1 | Step 2 |
|---------|---------|--------|--------|
| 1 | 0x227B1 | 0x4D (77) | 0x6B (107) |
| 2 | 0x227FA | 0x4E (78) | - |
| 3 | 0x22839 | 0x4F (79) | 0x6C (108) |
| 4 | 0x22882 | 0x50 (80) | 0x6D (109) |

These step values are stored in an array at `0xFC94` indexed by a counter at `0xFBA2`.

### 4. Step Storage Function (0x25157)
This function:
1. Delays for 12 ticks
2. Reads the step counter from `0xFBA2`
3. Stores the step value (from EAX) at `[step_counter*2 + 0xFC94]`
4. Increments the step counter
5. Handles overflow (resets when counter reaches 0xFFFF)
6. Checks various flags and triggers additional logic

### 5. Completion
When the frame counter reaches 4:
- A function is called with parameters (EBX=2, EDX=1, EAX=0x1B)
- This triggers conversation root 1 with the statue

## Code Flow

```
User: Use amulet (item 7) on statue (hotspot 353)
  │
  ▼
Item combination table lookup (353 + 7)
  │
  ▼
F8 handler table lookup (action_id 353)
  │
  ▼
trigger_statue_palette_fade (0x120E2)
  │
  ├── Set Alfred position (x=235, y=279)
  ├── Set facing direction = 2
  ├── Reset state variables
  └── Set statue_palette_fade_counter = 13
  │
  ▼
Per-frame animation loop (4 iterations)
  │
  ├── Snippet 1: Delay, store steps 77,107
  ├── Snippet 2: Delay, store step 78
  ├── Snippet 3: Delay, store steps 79,108
  └── Snippet 4: Delay, store steps 80,109
  │
  ▼ (when counter == 4)
Trigger conversation root 1 with statue
```

## Step Value System

The animation uses a queue-based step system where step values index into pre-computed animation frames:

### Step Value Transformation
When a step value is processed, it's transformed:
```
if (step >= 59):
    adjusted = step - 44
elif (step >= 11):
    adjusted = step - 11
else:
    adjusted = step

offset = adjusted * 224  # (7 * 32)
```

### Step Values Used
| Set | Steps | Adjusted | Offsets |
|-----|-------|----------|---------|
| 1 | 77, 78, 79, 80 | 33, 34, 35, 36 | 0x1CE0, 0x1DC0, 0x1EA0, 0x1F80 |
| 2 | 107, 108, 109 | 63, 64, 65 | 0x3720, 0x3800, 0x38E0 |

These offsets likely point to pre-computed palette animation frame data.

## Implementation Notes for ScummVM

### 1. Palette Interpolation
The original game uses pre-computed step values. For ScummVM, a cleaner approach:
- Read the palette table structure at room load
- Implement linear interpolation between source and target colors
- Apply changes to only the 16 specified palette indices
- Formula: `color[i] = source[i] + ((target[i] - source[i]) * frame) / total_frames`

### 2. Timing
- Each frame waits for 12 timer ticks (~200ms at 60Hz)
- 4 main iterations with 1-2 palette steps per iteration
- 7 total step updates across the animation
- Total animation duration: ~48+ timer ticks (~800ms)

### 3. Conversation Trigger
After 4 iterations (counter at 0x95F4 reaches 4):
- A function is called with EAX=0x1B (27) to trigger conversation
- This enables conversation root 1 with the statue

### 4. UI Blocking
During the animation:
- Mouse cursor is hidden
- Player input is blocked
- Normal game processing continues (ambient sounds, etc.)

### 5. Palette Table Location
The palette data is embedded in JUEGO.EXE at file offset 0x4C700 (memory 0x49500).
This data can be extracted and used directly for the ScummVM implementation.

### 6. Simplified ScummVM Implementation
```cpp
// Palette indices to modify
static const byte kStatuePaletteIndices[] = {
    30, 37, 39, 41, 44, 62, 74, 79, 83, 89, 105, 120, 152, 179, 217, 238
};

// Source colors (6-bit VGA)
static const byte kStatuePaletteSource[][3] = {
    {44,44,40}, {36,36,36}, {16,16,16}, {20,20,20}, {36,36,32},
    {28,32,28}, {32,32,32}, {16,16,12}, {16,20,20}, {52,52,44},
    {12,12,12}, {36,40,40}, {45,44,40}, {48,52,44}, {24,24,24}, {24,28,28}
};

// Target colors (6-bit VGA)
static const byte kStatuePaletteTarget[][3] = {
    {53,34,23}, {62,39,3}, {46,5,1}, {9,3,0}, {48,22,15},
    {30,16,25}, {63,43,16}, {60,25,0}, {16,20,20}, {63,38,20},
    {0,0,0}, {36,40,40}, {27,6,20}, {48,52,44}, {29,5,0}, {50,13,7}
};

void animateStatuePaletteFade(int numFrames) {
    for (int frame = 0; frame <= numFrames; frame++) {
        for (int i = 0; i < 16; i++) {
            byte r = kStatuePaletteSource[i][0] +
                     (kStatuePaletteTarget[i][0] - kStatuePaletteSource[i][0]) * frame / numFrames;
            byte g = kStatuePaletteSource[i][1] +
                     (kStatuePaletteTarget[i][1] - kStatuePaletteSource[i][1]) * frame / numFrames;
            byte b = kStatuePaletteSource[i][2] +
                     (kStatuePaletteTarget[i][2] - kStatuePaletteSource[i][2]) * frame / numFrames;

            setPaletteEntry(kStatuePaletteIndices[i], r, g, b);
        }
        delayTicks(12);  // ~200ms per frame
    }
}
```

## Related Files

- `JUEGO.EXE`: Contains the code and palette table
- `ALFRED.1`: Room 7 data (statue hotspot defined here)

## Test Cases

1. Enter room 7 with amulet in inventory
2. Use amulet on statue
3. Verify:
   - Screen fades to warm colors over ~4 iterations
   - Conversation with statue triggers after fade completes
   - Specific palette indices change while others remain stable
