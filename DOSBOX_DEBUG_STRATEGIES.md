# DOSBox-X Debugging Strategies for Alfred Pelrock Animation Analysis

## Quick Reference: Finding the Brick Throwing Animation

### Goal
Locate the 3-frame animation (~71 pixels wide) used when Alfred throws the brick at the window in room 3.

### Method 1: Break on File Read During Brick Action

```bash
# Start DOSBox-X with debugger
dosbox-x -debug

# Inside DOSBox, run the game and go to room 3
# Save your game state before the brick action

# Enable debugger (Alt+Pause)
# Set breakpoint on DOS file read (INT 21h, AH=3Fh)
BPINT 21 3F

# Return to game (F5) and use brick on window
# When breakpoint hits, check DS:DX for buffer address
# and CX for read size
```

### Method 2: Memory Snapshot Comparison

```bash
# In debugger before brick action:
MEMDUMPBIN 0 FFFFF before.bin

# Perform the brick animation

# After animation:
MEMDUMPBIN 0 FFFFF after.bin

# Then compare externally:
xxd before.bin > before.hex
xxd after.bin > after.hex
diff before.hex after.hex | head -100
```

### Method 3: Trace play_fight_animation Calls

The `play_fight_animation` function is at real-mode address `seg:26420`.

```bash
# In DOSBox-X debugger:
# First find the game's code segment
# Then set breakpoint at play_fight_animation
BP seg:26420

# When it breaks, examine stack for parameters:
# - Frame count
# - Width
# - Height
# - Animation data pointer
```

### Method 4: Break on Animation Display (VGA BLIT)

Animation frames are eventually copied to VGA memory at A000:0000.

```bash
# Set memory write breakpoint on VGA segment
# This is more advanced - look for writes to A000:0000-A000:FFFF
# during the brick animation
```

## Key Addresses to Monitor

| Address | Description |
|---------|-------------|
| 0x26420 | play_fight_animation function |
| 0x191E9 | execute_complex_item_script_table |
| 0x47120 | Item combo table (brick+window entry) |
| 0x48118 | ALFRED.7 book table |

## ALFRED.1 Room 3 Structure

Room 3 data pairs:
- **Pair 0**: Background image (26896 bytes compressed)
- **Pair 1**: Sprites/chars (24806 bytes → 31670 decompressed, 4.3% transparent)
- **Pair 8**: Unknown data (64162 bytes → 235876 decompressed, 71% transparent)
- **Pair 11**: Palette (768 bytes - 256 RGB triplets)

## Animation Data Sources

1. **ALFRED.2**: Character talking animations (RLE compressed)
2. **ALFRED.3**: Character movement animations
3. **ALFRED.7**: Misc sprites and cursors (has BUDA markers)
4. **Room data (ALFRED.1)**: Room-specific sprites in pairs 0, 1, 8

## Search Strategy

The brick animation might be:
1. In ALFRED.7 (general sprites file) - Already searched, found candidate at 0x1AF3EA
2. Embedded in room 3's data pairs - Currently analyzing
3. Loaded dynamically based on item combo handler

## DOSBox-X Debugger Commands Reference

```bash
# Breakpoints
BP seg:offset       # Code breakpoint
BPM addr            # Memory read/write breakpoint
BPINT num func      # Interrupt breakpoint

# Memory
MEMDUMPBIN addr len file  # Dump memory to file
D seg:offset              # Display memory
C seg:off seg:off len     # Compare memory

# Execution
G                   # Go (continue)
F5                  # Continue
T                   # Trace (step)
P                   # Procedure step (step over calls)

# Information
R                   # Show registers
SR                  # Show segment registers
LOG C               # Log all CALL instructions
```

## Alternative: Static Analysis Approach

If DOSBox-X tracing is complex, try:

1. Search JUEGO.EXE for references to the brick+window combo entry
2. Find the handler that loads/plays the animation
3. Trace which file and offset it reads from

Key code to find: The corrupted handler at 0x1284B might have nearby valid handlers that show the pattern.
