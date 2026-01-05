# Game State Reset Mechanism - Complete Analysis

## Executive Summary

After extensive analysis of the Alfred Pelrock game's code and data files, here is the definitive understanding of how game state reset works:

### Key Finding: NO DYNAMIC FB RESTORATION EXISTS

Neither ALFRED.8 nor ALFRED.B contains records to restore FB conversation markers. The game **does NOT reset conversation state (FB markers) on startup**.

| File | Records | Restores FB? | Purpose |
|------|---------|--------------|---------|
| ALFRED.8 | 82 | **0** | Room metadata (exits, hotspots, walkboxes) |
| ALFRED.B | 1180 | **0** | Text color bytes (0x08) |

## The Three Categories of Game State

### Category 1: Persistent State (Saved to SALVAJOC.XXX)
- Player position (X, Y)
- Current room
- Inventory items
- Conversation branch states (memory array at 0x0004fba4)
- Various game flags

When loading a save: The game reads these from the save file and restores them to memory.

### Category 2: Room Data State (Modified in ALFRED.1, Reset by ALFRED.8)
- Hotspot positions (can be moved offscreen to disable)
- Exit enable/disable flags
- Walkbox configurations

On startup: `apply_alfred8_room_defaults` reads ALFRED.8 and patches these values into ALFRED.1, restoring the default room configurations.

### Category 3: Conversation Text State (FB/FA markers in ALFRED.1)
- FB = Available conversation choice
- FA = Used/exhausted conversation choice  

**CRITICAL: These are NEVER reset by any startup code!**

## How Conversation State Actually Works

### During Gameplay (handle_conversation_tree at 0x00018690):
1. Player selects a conversation choice marked with FB
2. FB is changed to FA in ALFRED.1 (via write_data_to_alfred1)
3. A journal record is written to ALFRED.A: `[room:2][offset:2][1][0xFA]`
4. Memory array at conversation_branch_state_array is updated

### The Journal (ALFRED.A) Purpose:
- **Write-only during gameplay** - stores FA conversions
- **Deleted on normal exit** - `thunk_FUN_00031f2d("alfred.a")` called at end of `game_initialization`
- **NOT read for revert purposes** - No code reads journal to restore FB markers

### The ALFRED.B Purpose:
All 1180 records restore `0x08` (text color command) at offsets 2 bytes after FB markers:
```
Text structure: FB [choice_idx] 08 0D [text...]
                              ^^ ALFRED.B targets this byte
```
This restores text formatting, NOT the FB marker itself.

## Why FB Markers Don't Need Resetting

The game's design assumes:

1. **Fresh Install = Fresh State**: ALFRED.1 is extracted from PACKET.001 during installation with all FB markers intact.

2. **No "New Game" Feature**: The game has no way to start over except reinstalling.

3. **Save Games Store Memory State**: The conversation_branch_state_array (224 bytes at 0x0004fba4) tracks which conversations are exhausted. This is saved/loaded separately from ALFRED.1.

4. **ALFRED.1 Modifications Accumulate**: As you play, FA markers accumulate in ALFRED.1 across sessions. This is intentional - the file reflects your total game progress.

## The Real Reset Flow

```
INSTALL:
  PACKET.001 → extract → ALFRED.1 (pristine, all FB)
  
STARTUP (every time):
  open_all_resource_files()     → Opens ALFRED.A (creates if needed)
  load_alfred8_and_alfred9()    → Patches room data defaults to ALFRED.1
  [game runs]
  thunk_FUN_00031f2d("alfred.a") → Deletes journal on clean exit

LOAD SAVE:
  conversation_branch_state_array ← loaded from SALVAJOC.XXX
  (ALFRED.1's FA markers are NOT modified - they persist)
```

## Implications for ScummVM Implementation

### What Must Be Saved:
1. conversation_branch_state_array (224 bytes) - which conversations are exhausted
2. Inventory items
3. Room flags/states
4. Player position

### What Should NOT Be Modified in ALFRED.1:
- FB/FA markers should probably be kept in memory only
- Or stored in save game, not the resource file

### ALFRED.8/B Application:
- Apply ALFRED.8 room defaults on startup (exits, hotspots, walkboxes)
- ALFRED.B text color restoration may be unnecessary if text is parsed correctly

## File Summary

| File | Format | Purpose | When Applied |
|------|--------|---------|--------------|
| ALFRED.1 | Resource file | All room data, text, sprites | Read at runtime |
| ALFRED.8 | Patch records | Room metadata defaults | Startup |
| ALFRED.B | Patch records | Text color bytes | Startup (may be redundant) |
| ALFRED.A | Journal | Tracks FB→FA changes | Write-only, deleted on exit |
| SALVAJOC.XXX | Save game | Memory state snapshot | Load game |

## Save Game Conversation State Location

Analysis of save files confirms conversation state is stored at offset **0x34** in the save file:

```
SALVAJOC.024 (JUSTSTARTED): [(14, 13), (154, 12), (155, 10), (156, 12)]
SALVAJOC.025 (ROOM0OPEN):   [(0, 4), (14, 13), (154, 12), (155, 10), (156, 12)]
                             ^^^^^^ New entry! room 0, slot 0, value 4
```

This confirms:
- Conversation branch states are stored in save files at offset 0x34
- The array is 224 bytes (56 rooms × 4 slots)
- **ALFRED.1's FB/FA markers are NOT used for state tracking**
- The memory array `conversation_branch_state_array` is what drives conversation display

## How Conversations Actually Work

1. **ALFRED.1 FB/FA markers**: These are modified during gameplay but serve as a **permanent record**, not the active state

2. **Memory array (0x0004fba4)**: This is loaded from save game at offset 0x34 and determines which text branches to show

3. **Text display logic**: Checks the memory array, NOT the ALFRED.1 FA markers, when deciding what to display

This means:
- FB→FA changes in ALFRED.1 are cosmetic/logging
- The actual game state is in memory, saved to SALVAJOC.XXX

## Open Questions

1. **Why journal if not for revert?** Possibly for debugging, crash recovery detection, or abandoned feature.

2. **Why modify ALFRED.1 if state is in memory?** Likely a belt-and-suspenders approach, or ALFRED.1 serves as a persistent backup.

3. **Why restore 0x08 bytes?** All targets already have 0x08. Possibly defensive coding or the original ALFRED.1 had different values during development.

4. **Can the game be played without modifying ALFRED.1?** Probably yes - the memory array is the real state. ScummVM could skip ALFRED.1 modifications entirely.
