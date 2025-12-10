# Palette Cycling System - Offset Documentation

## Overview
The Alfred Pelrock game uses a palette cycling/animation system to create animated visual effects without changing the background pixels. This is achieved by modifying VGA palette entries in real-time.

## Room 2 - McDowells Restaurant Sign Animation

### Configuration Location
- **File**: `JUEGO.EXE`
- **Offset**: `0x0004B860`
- **Size**: 12 bytes

### Raw Data
```
fa 01 24 2c 08 0c 14 08 24 2c 08 05
```

### Structure for Mode 1 (FADE) - 12 bytes

| Offset | Size | Field | Value | Description |
|--------|------|-------|-------|-------------|
| +0 | 1 | Palette Index | 0xFA (250) | The palette index to animate |
| +1 | 1 | Mode | 0x01 | Animation mode: 1 = fade |
| +2 | 1 | Current R | 0x24 (36) | Current red value (6-bit) |
| +3 | 1 | Current G | 0x2C (44) | Current green value (6-bit) |
| +4 | 1 | Current B | 0x08 (8) | Current blue value (6-bit) |
| +5 | 1 | Min R | 0x0C (12) | Minimum red value (6-bit) |
| +6 | 1 | Min G | 0x14 (20) | Minimum green value (6-bit) |
| +7 | 1 | Min B | 0x08 (8) | Minimum blue value (6-bit) |
| +8 | 1 | Max R | 0x24 (36) | Maximum red value (6-bit) |
| +9 | 1 | Max G | 0x2C (44) | Maximum green value (6-bit) |
| +10 | 1 | Max B | 0x08 (8) | Maximum blue value (6-bit) |
| +11 | 1 | Flags | 0x05 | Control flags (speed, direction) |

### RGB Value Conversion
The color values are stored in 6-bit format (0-63) and need to be multiplied by 4 to convert to standard 8-bit RGB (0-255):

- **Minimum RGB (6-bit)**: (12, 20, 8)
- **Minimum RGB (8-bit)**: (48, 80, 32) - Dark green
- **Maximum RGB (6-bit)**: (36, 44, 8)
- **Maximum RGB (8-bit)**: (144, 176, 32) - Bright green

### Animation Details
- **Visual Effect**: McDowells restaurant sign/logo fades between dark and bright green
- **Sign Location**: Approximately coordinates (350, 53, 588, 160) in the background
- **Mode 1 (Fade)**: Single palette entry smoothly transitions between min and max RGB values
- **Flags**: 0x05
  - Lower 5 bits (0x05): Speed/step value
  - Bit 6: Direction (0 = fading up toward max)

## Room 0 - City Lights Window Animation

### Configuration Location
- **File**: `JUEGO.EXE`
- **Offset**: `0x0004B88C`
- **Size**: 12 bytes

### Raw Data
```
c8 06 00 5a e0 04 00 04 67 07 00 01
```

### Structure for Mode 6 (ROTATE) - 12 bytes

| Offset | Size | Field | Value | Description |
|--------|------|-------|-------|-------------|
| +0 | 1 | Palette Start | 0xC8 (200) | Starting palette index for rotation |
| +1 | 1 | Mode/Count | 0x06 (6) | Mode 6: Rotate 6 consecutive palette entries |
| +2 | 1 | Unknown | 0x00 | Possibly unused or counter state |
| +3 | 1 | Delay | 0x5A (90) | Delay in frames between rotations (~5 sec @ 18 FPS) |
| +4-10 | 7 | Unknown | Various | Purpose TBD - may store rotation state |
| +11 | 1 | Flags | 0x01 | Control flags |

### Animation Details
- **Visual Effect**: City building windows turn on/off by rotating colors
- **Palette Range**: Indices 200-205 (6 colors total)
- **Mode 6 (Rotate)**: Cyclically shifts color values through consecutive palette entries
- **Delay**: 90 frames (~5 seconds at 18 FPS) between rotation steps
- **Window Location**: Visible through bedroom window at night

## Code References

### Game Engine Functions

#### `update_palette_cycling()`
- **Memory Address**: `0x00016804`
- **Called**: Every frame during room rendering
- **Reads from**: `DAT_0004f8ec` (pointer to current room's cycling config)
- **Writes to**: VGA palette ports (0x3C8 for index, 0x3C9 for RGB data)

#### `load_room_data()`
- **Memory Address**: `0x000152f5`
- **Reads**: Cycling table at `&DAT_000486a4`
- **Sets**: `DAT_0004f8ea = 1` (cycling enabled flag)
- **Sets**: `DAT_0004f8ec = config_pointer` (pointer to 12-byte config)

### Cycling Table Structure
- **Memory Location**: `&DAT_000486a4` (memory address - file mapping TBD)
- **Candidate File Location**: Around `0x0004B780` (contains Room 2 reference)
- **Entry Format**: 6 bytes per entry
  - Bytes 0-1: Room number (little-endian word)
  - Bytes 2-5: Pointer to 12-byte config structure (little-endian dword)
- **Terminator**: `0xFFFF` marks end of table

**Note**: The exact file-to-memory address mapping is complex due to DOS EXE segment relocation.
Multiple dispatch tables exist in the 0x4B780-0x4B850 region, but precise mapping to the
palette cycling configs requires further analysis of the segment base address used at runtime.

## Related Files

### Scripts That Use This Data
1. **`create_mcdowells_fade.py`**
   - Extracts room 2 background
   - Creates animated GIF showing palette fade effect
   - Uses config values from offset 0x4B860

2. **`PALETTE_CYCLING_SUMMARY.py`**
   - Documents the complete palette cycling discovery process
   - Parses and displays cycling configs from JUEGO.EXE
   - Scans for additional cycling configs

### Generated Output
- **`room_02_mcdowells_fade.gif`**: Animated visualization of the McDowells sign fade effect

## Discovery Process

This information was discovered through:
1. **Ghidra MCP decompilation** of JUEGO.EXE functions
2. **User-provided video frames** showing the actual animation
3. **Binary pattern search** for RGB min/max values in JUEGO.EXE
4. **Manual analysis** of the 12-byte config structure

## Summary of Discoveries

### Known Palette Cycling Configurations

| Room | File Offset | Mode | Description | Palette Range | Script |
|------|-------------|------|-------------|---------------|--------|
| 2 | 0x4B860 | 1 (Fade) | McDowells sign | Index 250 | `create_mcdowells_fade.py` |
| 0 | 0x4B88C | 6 (Rotate) | City lights | Indices 200-205 | `create_room0_city_lights.py` |

### Configuration Structure Differences

**Mode 1 (FADE)**:
- Byte 0: Single palette index
- Bytes 2-4: Current RGB (6-bit)
- Bytes 5-7: Min RGB (6-bit)
- Bytes 8-10: Max RGB (6-bit)
- Byte 11: Speed/direction flags

**Mode 6 (ROTATE)**:
- Byte 0: Starting palette index
- Byte 1: Number of palette entries to rotate
- Byte 3: Delay in frames between rotations
- Remaining bytes: State/configuration (purpose TBD)

### Other Rooms

Scanning JUEGO.EXE found approximately 260 potential palette cycling configs in the 0x40000-0x50000 range.
However, many are false positives (data that coincidentally matches the validation criteria).

The actual palette cycling table that maps room numbers to configs is located in the 0x4B700-0x4B900 region,
but exact identification requires:
1. Determining the DOS EXE segment base address used at runtime
2. Mapping memory addresses to file offsets
3. Correlating with Ghidra's decompiled references to `DAT_000486a4`

## Technical Notes

### VGA Palette
- Standard VGA palette has 256 color entries (indices 0-255)
- Each entry stores RGB values in 6-bit format (0-63)
- Hardware registers: 0x3C8 (write index), 0x3C9 (RGB data)

### Animation Modes
- **Mode 1 (Fade)**: Single color smoothly transitions between min and max
- **Mode 2+ (Rotate)**: Multiple consecutive palette entries cycle through color values
  - Mode value indicates number of palette entries to rotate

### Performance
- Updates happen every frame (approximately 18-20 FPS in original game)
- Only changes palette, not pixel data - very efficient
- Creates illusion of animation on static backgrounds
