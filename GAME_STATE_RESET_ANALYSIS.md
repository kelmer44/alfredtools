# Game State Reset Mechanism - Complete Analysis

## Executive Summary

After extensive analysis of the Alfred Pelrock game's code and data files, here is the definitive understanding of how game state reset works:

### Key Finding: FA OVERWRITES 0x08, NOT FB!

When a conversation choice is disabled:
- FA is written at **FB+2** (where the 0x08 text color command is)
- The FB marker itself remains unchanged
- ALFRED.B restores the 0x08 bytes that FA overwrote

| File | Records | Purpose |
|------|---------|--------|
| ALFRED.8 | 82 | Room metadata (exits, hotspots, walkboxes) |
| ALFRED.B | 1180 | **Restores 0x08 bytes overwritten by FA** |

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

### Category 3: Conversation Text State (FB/F1/FA markers in ALFRED.1)

Two types of choice markers:
- **FB** = One-time choice (1180 total) - gets disabled after selection
- **F1** = Repeatable choice (192 total) - never disabled
- **FA** = Disabled marker - written at FB+2 to disable a choice

Structure: `FB [idx] 08 0D [text...]` → `FB [idx] FA 0D [text...]` when disabled

## How Conversation State Actually Works

### During Gameplay (handle_conversation_tree at 0x00018690):
1. Player selects a conversation choice
2. Code checks at 0x18c3d: Is marker at position-2 == 0xF1? If yes, skip (repeatable)
3. For FB markers: FA is written at position+2 (the 0x08 byte) in ALFRED.1
4. A journal record is written to ALFRED.A: `[room:2][offset:2][1][0xFA]`
5. The offset in journal points to the FA position (FB+2), not the FB itself

### The Journal (ALFRED.A) Purpose:
- **Write-only during gameplay** - stores FA write locations
- **Deleted on normal exit** - `thunk_FUN_00031f2d("alfred.a")` called at end
- **NOT read for revert purposes** - No code reads journal to restore values

### The ALFRED.B Purpose (CORRECTED):
All 1180 records restore `0x08` at the exact positions where FA gets written:
```
Before disable: FB [idx] 08 0D [text...]
After disable:  FB [idx] FA 0D [text...]  <- FA overwrites 0x08
ALFRED.B:       Restores 08 at this position on startup!
```
**ALFRED.B DOES reset conversation state by restoring the 0x08 bytes!**

## How Conversation Reset Works

The game's design:

1. **On startup**: `apply_alfred8_room_defaults` applies ALFRED.B patches
2. **ALFRED.B restores 0x08**: Overwrites any FA markers back to 0x08
3. **Result**: All FB choices become enabled again (0x08 at +2, not FA)

4. **F1 markers are never touched**: They don't get FA written, don't need restoration

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
