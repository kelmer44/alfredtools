# JUKEBOX CHEAT CODE - COMPLETE ANALYSIS

## The Cheat Code
**HIJODELAGRANPUTA** (Spanish profanity meaning "son of the great whore")

## How It Works

### Code Flow (in main_game_loop at 0x1044a):

1. **0x104f3**: `CALL check_keyboard_input` - Scans keyboard buffer for any pressed key
2. **0x104f8**: `TEST AL,AL` - Check if any key was pressed
3. **0x104fa**: `JZ 0x10621` - Skip if no key pressed
4. **0x10500**: `CMP byte ptr [0x495f3], 0` - Check the "cheat enabled" flag
5. **0x10507**: `JZ 0x10621` - Skip if flag is 0 (**NOW NOP'd**)
6. **0x1050d**: `CALL 0x15258` - Get the ASCII character from scan code table
7. **0x10520**: Compare character with `cheat_string[counter]`
8. **0x10527**: Increment counter if match, else reset to 0
9. **0x1053d**: If counter equals 16 (cheat length), activate jukebox!

### Data Locations (Memory → File):
| Purpose | Memory Address | File Offset | Value |
|---------|---------------|-------------|-------|
| Cheat flag | 0x495f3 | 0x4c7f3 | 0x00 → **0x01** (patched) |
| Cheat string | 0x40f41 | 0x44141 | "HIJODELAGRANPUTA\0" |
| Cheat pointer | 0x4b79c | 0x4e99c | 0x00000f41 (relocates to 0x40f41) |
| Cheat length | 0x4b7a0 | 0x4e9a0 | 0x10 (16 characters) |
| Cheat counter | 0x5178d | (runtime) | Increments with each matching char |
| JZ instruction | 0x10507 | 0x14707 | 0F 84 14 01 00 00 → **90 90 90 90 90 90** (NOP'd) |

### Address Conversion Formulas:
- **Code segment**: `file_offset = memory_address - 0x10000 + 0x14200`
- **Data segment**: `file_offset = memory_address - 0x40000 + 0x43200`

## Patches Applied

### Patch 1: Enable Flag (0x4c7f3)
```
Original: 00
Patched:  01
```

### Patch 2: NOP the JZ (0x14707)
```
Original: 0F 84 14 01 00 00  (JZ +0x114)
Patched:  90 90 90 90 90 90  (NOP NOP NOP NOP NOP NOP)
```

## Why It Might Not Be Working

The patches ARE correctly applied to the file. Possible runtime issues:

1. **DOSBox configuration**: The keyboard interrupt (INT 9h) must work correctly
2. **Game state**: Must be in normal gameplay (walking around), not in:
   - Main menu
   - Pause menu
   - Dialog/conversation
   - Cutscene
3. **Typing speed**: The game loops and checks keyboard each frame. If you type too fast, keys might be missed
4. **Keyboard layout**: Must use US keyboard layout (QWERTY)

## How to Test

1. Launch the game: `dosbox-x JUEGO.EXE` or through ALFRED.COM
2. Wait until you're controlling the character and can walk around
3. Type **HIJODELAGRANPUTA** (uppercase, no shift needed - scan codes are the same)
4. If it works, the jukebox (music player) should appear

## What Happens When Cheat Activates

1. Plays sound file `9ZZZZZZZ.SMP`
2. Sets `DAT_0005178f = 1` (jukebox mode active)
3. Enters a loop that:
   - Displays a music selection interface
   - Responds to left/right arrows to change track
   - Lets you listen to the game's music
4. ESC or another key exits jukebox mode

## Alternative: Force Jukebox Mode Directly

Instead of relying on the cheat input, we could patch to ALWAYS enter jukebox mode by:
1. NOP the first JZ at 0x104fa (keyboard check) - **NOT RECOMMENDED** (would break game)
2. Or patch `0x5178f` to 0x01 in data segment - Would require finding the right trigger point
