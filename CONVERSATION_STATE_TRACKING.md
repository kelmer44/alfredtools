# Conversation State Tracking - Complete Analysis

## Overview

The Alfred Pelrock game tracks conversation progress using **two separate mechanisms**:

1. **Branch/Choice Level Disabling** - Individual dialog choices get disabled via `0xFA` marker
2. **Root Level Disabling** - Entire conversation trees can be disabled via state array

---

## 1. Branch/Choice Level Disabling (0xFA Marker)

### Location in Code
- `handle_conversation_tree` at **0x00018690**
- Choice disabling logic at **0x00018c38-0x00018c48**
- Repeatable check at **0x00018c3d**: `CMP [ESI-2], 0xF1`

### How It Works

When a player selects a conversation choice:

1. **The FA marker is written at position+2** (where 0x08 text color command is), NOT replacing FB!
2. This change is written **directly to ALFRED.1 file** at runtime
3. A 6-byte journal record is written to ALFRED.A (file handle 0x0004f914)
4. **F1 markers are NEVER disabled** - code at 0x18c3d checks if marker-2 == 0xF1 and skips

### Two Types of Choice Markers

| Marker | Count | Behavior | Purpose |
|--------|-------|----------|--------|
| **0xFB** | 1180 | ONE-TIME: Gets disabled after selection | Story-critical choices |
| **0xF1** | 192 | REPEATABLE: Never disabled | Info/repeat questions |

### Text Data Structure (CORRECTED)

```
Before selection:  FD FB <choice#> 08 0D <voice_id_lo> <voice_id_hi> "Text..."
After selection:   FD FB <choice#> FA 0D <voice_id_lo> <voice_id_hi> "Text..."
                                   ^^ FA written HERE (at +2), replacing 0x08

Repeatable choice: FD F1 <choice#> 08 0D <voice_id_lo> <voice_id_hi> "Text..."
                      ^^ F1 marker - selecting this does NOT write FA
```

### Journal Record Format (6 bytes at 0x0004fb70)

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 2 | room_number | Current room (little-endian) |
| +0x02 | 2 | text_offset | Offset within room's text data |
| +0x04 | 1 | length | Always 1 (single byte) |
| +0x05 | 1 | value | Always 0xFA (disabled marker) |

### Code Flow (Ghidra Analysis)

```asm
; At 0x00018c38 - Check if this is a repeatable F1 marker
00018c38: MOV AL,byte ptr [ESI + -0x2]   ; Get marker 2 bytes before current pos
00018c3d: CMP EAX,0xf1                   ; Is it F1 (repeatable)?
00018c42: JZ 0x00018d0e                  ; Skip disabling if F1!

; At 0x00018c48 - Write FA to disable (only for FB markers)
00018c48: MOV byte ptr [ESI],0xfa        ; Write FA at position+2 (where 0x08 was)
```

```c
// Equivalent C code:
if (current_text_ptr[-2] == 0xF1) {
    // F1 marker = repeatable choice, skip disabling
    goto skip_disable;
}
*current_text_ptr = 0xFA;  // Write FA at position+2 (the 0x08 byte)
offset = current_text_ptr - room_text_data_ptr;

// Write to ALFRED.1 file
file_seek(file_handle_alfred1, room_text_base + offset);
write_data_to_alfred1(current_text_ptr, 1, file_handle_alfred1);

// Write journal record
_DAT_0004fb70 = current_room_number;
_DAT_0004fb72 = offset;  // Points to the FA position (+2 from FB)
DAT_0004fb74 = 1;        // length
DAT_0004fb75 = 0xFA;     // value
write_data_to_alfred1(&DAT_0004fb70, 6, DAT_0004f914);  // journal file
```

### Effect on Choice Display

When parsing choices (around 0x000189a1-0x000189a6):
```asm
000189a1: CMP EAX,0xfa    ; Check if byte at +2 is FA (disabled)
000189a6: JNZ 0x000189aa  ; If not FA, don't decrement counter
000189a8: DEC DH          ; FA found - decrement visible choice count
```

- Code reads byte at marker+2 to check for FA
- Choice counter decrements for each `0xFA` encountered
- If all choices in a branch have `0xFA` at +2, conversation auto-proceeds

---

## 2. Root Level Disabling (conversation_branch_state_array)

### Memory Location
- **Address**: `0x0004fba4`
- **Size**: 4 bytes per room × 56 rooms = 224 bytes
- **Access Pattern**: `array[room_number * 4 + slot_index]`

### How It Works

1. Script actions (via F8 control codes) call `update_conversation_state` at **0x0001b666**
2. The function writes to `conversation_branch_state_array[room * 4 + slot]`
3. When loading a room, the code checks this array
4. If `array[room * 4 + slot] != 0`, the entire conversation root is skipped

### Code in update_conversation_state (0x0001b666)

```c
void update_conversation_state(void) {
    room = get_current_room_number();
    // Write state to array
    conversation_branch_state_array[room * 4 + slot] = value;

    if (room == current_room_number) {
        // Update text pointer table to skip past disabled root
        // Scans for FE markers and F7 branch ends
        // Updates room_sprite_data_ptr + 0x3DA pointer table
    }
}
```

### Text Structure for Roots

```
FE <root_index> FC <room#> <speaker> <voice_file_id> "NPC greeting..."
   └─ Root marker        └─ Speaker ID (08 = Alfred)
```

---

## 3. NPC-to-Root Assignment (Multi-NPC Rooms)

### The Problem
In rooms with multiple NPCs (like Room 22 - McDowell's Diner), how does the game know which conversation root belongs to which NPC?

### The Mechanism

The game uses a **position-based** system using `queued_sprite_talk_count`:

```c
// In handle_conversation_tree (0x00018690):
conversation_index = sprite_count - 2 + hotspot_count + queued_sprite_talk_count;
text_ptr = room_data[0x3DA + conversation_index * 4] + 2;
```

### How queued_sprite_talk_count Works

1. In `check_sprite_hover_and_trigger_conversation` (0x00018e47):
   - Game iterates through sprites starting at index 2 (skipping Alfred at 0, 1)
   - For each sprite with `action_flags & 0x10` (TALK flag): `sprite_talk_count++`
   - When NPC is clicked, `queued_sprite_talk_count = sprite_talk_count`

2. The clicked NPC's position in the "talkable sprite" list determines which root is used

### Example: Room with 3 NPCs

| Sprite Index | Has TALK Flag | sprite_talk_count | Uses Root |
|--------------|---------------|-------------------|-----------|
| 2 | Yes | 0 | Root #1 |
| 3 | No | - | - |
| 4 | Yes | 1 | Root #2 |
| 5 | Yes | 2 | Root #3 |

### Text Pointer Table

- Located at `room_data + 0x3DA`
- Contains 4-byte absolute pointers to conversation start positions
- Index = `sprite_count - 2 + hotspot_count + talk_index`

---

## 4. State Reset for New Game

### Key Question
How does the game restore conversation state when starting a new game?

### Investigation Results

**ALFRED.8** and **ALFRED.B** are loaded at game initialization via `load_alfred8_and_alfred9()` at **0x00014977**.

#### ALFRED.8 Format (Pair 10 - Room Data)
- Restores sprite positions, object states
- Does NOT contain FB markers
- Uses offset 0x50 (Pair 10) in room directory

#### ALFRED.B Format (Pair 12 - Text Data)
- Contains 1180 entries across 28 rooms
- Each entry: `[room:2][offset:2][length:1][value:1]`
- **All entries write 0x08** (text color command byte)
- Uses offset 0x60 (Pair 12) in room directory

### Critical Finding - ALFRED.B Purpose (VERIFIED)

**ALFRED.B restores the 0x08 byte that FA overwrites!**

- Structure: `FB [idx] 08 0D [text...]`
- When disabled: `FB [idx] FA 0D [text...]` (0x08 → FA)
- ALFRED.B targets exactly these positions to restore 0x08
- This re-enables the conversation choices on game startup

### Why This Works

1. FA is written at FB+2 (where 0x08 was)
2. ALFRED.B stores 0x08 values for all 1180 FB marker positions
3. On startup, ALFRED.B patches restore 0x08, "undoing" all FA markers
4. Result: All FB choices become enabled again

### Actual New Game Mechanism

The game most likely uses one of these approaches:
1. **CD-based reset**: Copies clean ALFRED.1 from CD-ROM
2. **Backup file**: Uses a backup copy of ALFRED.1
3. **File verification**: The game has CD authentication checks

The `verify_cd_authenticity()` call in `game_initialization()` suggests the original CD is required, possibly to restore pristine data files.

---

## 5. Summary Tables

### Choice Marker Types (VERIFIED)

| Marker | Count | Position+2 | Behavior |
|--------|-------|------------|----------|
| **0xFB** | 1180 | 0x08 → FA when disabled | ONE-TIME: Disabled after selection |
| **0xF1** | 192 | 0x08 (never changes) | REPEATABLE: Can select multiple times |

### Binary Structure (VERIFIED)

```
Enabled:   FB [idx] 08 0D [voice_lo] [voice_hi] [text...]
                    ^^ text color command

Disabled:  FB [idx] FA 0D [voice_lo] [voice_hi] [text...]
                    ^^ FA overwrites 0x08

Repeatable: F1 [idx] 08 0D [voice_lo] [voice_hi] [text...]
            ^^ F1 marker - code at 0x18c3d skips FA write
```

### State Tracking Mechanisms

| Level | Marker | Storage | Persistence |
|-------|--------|---------|-------------|
| Choice/Branch | `0xFB+2` → `0xFA` | Direct in ALFRED.1 text | Written to file |
| Root | `0xFE` | `conversation_branch_state_array[room*4+slot]` | Save journal |

### Control Code Markers

| Byte | Meaning | Notes |
|------|---------|-------|
| `0xFE` | Conversation root marker | Starts a conversation tree |
| `0xFB` | One-time dialog choice | Gets disabled (FA at +2) after selection |
| `0xF1` | Repeatable dialog choice | Never disabled, can select multiple times |
| `0xFA` | Disabled marker | Written at FB+2 to disable choice |
| `0x08` | Text color command | At FB+2, overwritten by FA when disabled |
| `0x0D` | Text color value | Always follows 0x08, not overwritten |
| `0xF7` | Branch/root end marker | |
| `0xFD` | Text line terminator | |
| `0xFC` | Speaker/room identifier | |

### File Roles

| File | Purpose | State Reset Role |
|------|---------|------------------|
| ALFRED.1 | Main game data | Modified at runtime (FA written at FB+2) |
| ALFRED.8 | Room defaults | Restores exits, hotspots, walkboxes (82 records) |
| ALFRED.B | Conversation resets | Restores 0x08 at FA positions (1180 records) |
| ALFRED.A | Change journal | Tracks FA writes, deleted on clean exit |

---

## 6. Ghidra Annotations Applied

### Data Labels

| Address | Name |
|---------|------|
| 0x0004fb70 | conversation_state_change_record |
| 0x0004fb72 | conv_state_text_offset |
| 0x0004fb74 | conv_state_length |
| 0x0004fb75 | conv_state_new_marker |
| 0x0004fba4 | conversation_branch_state_array |
| 0x0004f914 | file_handle_save_journal |

### Code Comments

| Address | Comment |
|---------|---------|
| 0x00018c38 | CHECK F1 REPEATABLE: If marker at [ESI-2] is 0xF1, skip disabling |
| 0x00018c48 | WRITE FA AT FB+2: Disables by writing 0xFA where 0x08 was |
| 0x00018c6a | PERSIST TO ALFRED.1: Seeks to text data offset |
| 0x00018c7e | WRITE 0xFA MARKER to ALFRED.1 file |
| 0x00018cbb | JOURNAL ENTRY: Writes 6-byte record to save journal |
| 0x000189a1 | CHECK DISABLED: If byte at marker+2 is 0xFA, skip choice |
| 0x000157ce | ROOT SKIP CHECK: conversation_branch_state_array[room*4 + slot] |
| 0x0001b688 | STORE ROOT STATE: marks entire conversation roots as disabled |
| 0x0001b717 | UPDATE TEXT POINTER: updates pointer table to skip disabled root |

---

## 7. Key Insights

1. **FA Placement (CRITICAL)**: FA is written at FB+2 (the 0x08 byte), NOT replacing FB!

2. **Two Marker Types**:
   - **0xFB** (1180): One-time choices, disabled after selection
   - **0xF1** (192): Repeatable choices, never disabled

3. **ALFRED.B Purpose**: Restores 0x08 bytes that FA overwrote, effectively re-enabling conversations

4. **No Topic IDs**: The game uses physical byte offsets, not named topic identifiers

5. **Positional Tracking**:
   - Individual choices: FA written at FB+2 in ALFRED.1
   - Root trees: Index-based array (`room * 4 + slot`)

6. **NPC Mapping**: Sprite order in room data determines conversation root assignment

4. **File Modification**: ALFRED.1 is modified at runtime - not just memory!

5. **State Reset Limitation**: Neither ALFRED.8 nor ALFRED.B can fully restore conversation state; a clean ALFRED.1 copy is likely needed for true "new game"
