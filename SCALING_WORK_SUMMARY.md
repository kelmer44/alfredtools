# Sprite Scaling Analysis - Summary

## What Was Done

### 1. Documentation Verification ✓
- Verified `SPRITE_SCALING.md` against Ghidra decompilation
- Confirmed scaling algorithm at address 0x00015340 matches documentation
- Validated formula: `scale_delta = (y_threshold - player_y) / scale_divisor`
- Confirmed: `scale_down = scale_delta`, `scale_up = scale_delta / 2`

### 2. Ghidra Project Updates ✓

**Functions Identified:**
- `init_character_scaling_tables` @ 0x00011e28
- `render_character_sprite_scaled` @ 0x00016ff8
- `load_room_data` @ 0x00015340

**Variables Renamed:**
- `DAT_0004967e` → `scale_up`
- `DAT_0004967f` → `scale_down`
- `DAT_00053290` → `width_scaling_lookup_table`
- `DAT_00053cbc` → `height_scaling_lookup_table`

**Comments Added:**
- Detailed comments at lookup table addresses explaining their purpose
- Comment at load_room_data explaining scaling calculation
- Documentation of scaling parameter offsets (0x214-0x217)

### 3. Scripts Created ✓

**verify_and_demo_scaling.py**
- Extracts background from ALFRED.1
- Extracts character sprite from ALFRED.3 (first sprite, 51×102 pixels)
- Applies proper image scaling using PIL (not just cropping!)
- Renders character at three different heights:
  - Top (Y=100) - scaled smaller
  - Middle (Y=200) - medium scaling
  - Bottom (Y=370) - normal size
- Generates annotated image showing scaling in action

**extract_scaling_lookup_tables.py**
- Extracts lookup tables from game binary
- Analyzes table structure and content
- Saves tables to C header files for reference
- Documents the lookup table algorithm

### 4. Documentation Created ✓

**GHIDRA_SCALING_ANALYSIS.md**
- Complete reference of all functions and variables
- Memory addresses and sizes
- Detailed algorithm explanations
- Example calculations for Room 6
- Comments added to Ghidra project

## Key Findings

### Scaling Algorithm
The game uses a two-stage scaling approach:

1. **Calculate scale factors** (in load_room_data):
   ```c
   if (player_y < y_threshold) {
       scale_delta = (y_threshold - player_y) / scale_divisor;
       scale_down = scale_delta;      // scanlines to skip
       scale_up = scale_delta / 2;    // scanlines to duplicate
   }
   ```

2. **Apply via lookup tables** (in render_character_sprite_scaled):
   - Width table (51×51) determines which horizontal pixels to draw
   - Height table (102×102) determines which scanlines to draw/duplicate
   - Final height = 102 - scale_down + scale_up

### Lookup Tables
- **Width table** @ 0x00053290 (2,601 bytes)
- **Height table** @ 0x00053cbc (10,404 bytes)
- Both initialized at game startup by `init_character_scaling_tables`
- Tables create smooth scaling by selectively drawing/duplicating pixels

### Data Format (ALFRED.1)
Scaling parameters stored in each room's Pair 10 at offset 0x214:
```
+0x214: y_threshold (uint16 LE)  - where scaling starts
+0x216: scale_divisor (uint8)    - scaling rate
+0x217: scale_mode (int8)        - 0x00=normal, 0xFF=max, 0xFE=none
```

## Files Modified/Created

- [X] `verify_and_demo_scaling.py` - Created with proper scaling
- [X] `extract_scaling_lookup_tables.py` - New script for table extraction
- [X] `GHIDRA_SCALING_ANALYSIS.md` - Complete Ghidra reference
- [X] Ghidra project - Variables renamed, comments added

## Next Steps (Optional)

If you want to explore further:

1. **Run the extraction script** on the game binary to get actual lookup table data
2. **Generate demo images** for multiple rooms to see different scaling behaviors
3. **Extract all room scaling parameters** to see which rooms use which modes
4. **Analyze the lookup table patterns** to understand the exact pixel selection algorithm

## Usage

```bash
# Generate scaling demo for room 6
python3 verify_and_demo_scaling.py files/ALFRED.1 files/ALFRED.3 6

# Extract lookup tables (requires game binary)
python3 extract_scaling_lookup_tables.py ALFRED.EXE lookup_tables/

# Extract all room scaling parameters
python3 src/extract_scaling.py files/ALFRED.1 output/
```
