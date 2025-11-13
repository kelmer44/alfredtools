# Conversation Entry Points - Complete Analysis

## Overview

Conversations in Alfred Pelrock have **multiple entry points** based on the **sprite_talk_count** variable, which tracks how many times the player has initiated conversation with an NPC.

## Entry Point Mechanism

### Code Reference (from `handle_conversation_tree` @ 0x00018690)

```c
// Calculate which conversation entry point to use
pcVar12 = (char *)(*(int *)(room_data_ptr + 0x3da +
          (uint)(byte)(*(char *)(room_data_ptr + 5) + -2 +
                      *(char *)(room_data_ptr + 0x47a) + sprite_talk_count) * 4) + 2);
```

**Formula**: `entry_index = room_data[5] - 2 + room_data[0x47a] + sprite_talk_count`

### Room 2 Example

For Room 2 (prostitute conversation):
- `room_data[5]` = 7
- `room_data[0x47a]` = 1
- Formula: `entry_index = 7 - 2 + 1 + sprite_talk_count = 6 + sprite_talk_count`

**Entry Points**:
- `sprite_talk_count = 0` → Index 6 → **Initial greeting** (index 0x0A)
- `sprite_talk_count = 1` → Index 7 → **Return greeting** (index 0x2B)
- `sprite_talk_count = 2` → Index 8 → (future conversations)

## Line Separator Types

### 1. FD FE Pattern - Initial Greeting

**Structure**: `FD FE [unknown_byte] [control] [speaker_id] 08 [separator] [index] 00 [text]`

**Example** (Room 2, Index 0x0A @ 0xB21DD):
```
FD FE 01 FC 41 08 20 0A 00 83 20 54 65 20 61 70 65 63 65 74 65...
```

**Decoded**:
- `FD` = Line separator
- `FE` = Special marker (initial greeting flag)
- `01` = Unknown byte (always 0x01?)
- `FC` = Speaker change control
- `41` = Speaker ID (NPC)
- `08` = Marker byte
- `20` = NPC separator (0x0D = ALFRED, 0x20 = NPC)
- `0A` = Line index
- `00` = Terminator
- Text: "¿Te apecete pasar un buen rato, guapo?"

**Text Offset**: After the `00` terminator (+9 bytes from FD)

### 2. F7 Pattern - Return Greeting

**Structure**: `F7 [control] [speaker_id] 08 [separator] [index] 00 [text]`

**Example** (Room 2, Index 0x2B @ 0xB2EBC):
```
F7 FC 41 08 20 2B 00 83 20 48 61 73 20 63 6F 6E 73 65 67 75 69 64 6F...
```

**Decoded**:
- `F7` = Alternate entry point marker
- `FC` = Speaker change control
- `41` = Speaker ID (NPC)
- `08` = Marker byte
- `20` = NPC separator
- `2B` = Line index
- `00` = Terminator
- Text: "¿Has conseguido los condones?"

**Text Offset**: After the `00` terminator (+7 bytes from F7)

**Usage**: F7 is used for conversation re-entry points after the first conversation has been completed (when `sprite_talk_count > 0`).

### 3. FD Pattern - Normal Conversation Flow

**Structure**: `FD [control] [speaker_id] 08 [separator] [index] 00 [text]`

**Example** (Room 2, Index 0x0B @ 0xB220E):
```
FD FB 01 08 0D 0B 00 4E 6F 20 73 65 2C 20 83 20 43 75 61 6E 74 6F...
```

**Decoded**:
- `FD` = Line separator
- `FB` = Continue speaker control
- `01` = Speaker ID
- `08` = Marker byte
- `0D` = ALFRED separator
- `0B` = Line index
- `00` = Terminator
- Text: "No se, ¿Cuanto cobras?"

**Text Offset**: After the `00` terminator (+7 bytes from FD)

**Usage**: Standard conversation tree flow, player choice responses, NPC replies.

### 4. F4 FB Pattern - Alternative Player Choice

**Structure**: `F4 FB [choice_group_id] 08 [separator] [index] 00 [text]`

**Example** (Room 2, Index 0x29 @ 0xB2E62):
```
F4 FB 01 08 0D 29 00 4E 6F 20 70 75 65 64 6F 2E 20 45 73 74 6F 79...
```

**Decoded**:
- `F4` = Alternative choice marker
- `FB` = Continue speaker control
- `01` = **choice_group_id** (links to other choices)
- `08` = Marker byte
- `0D` = ALFRED separator
- `29` = Line index
- `00` = Terminator
- Text: "No puedo. Estoy buscando a una princesa"

**Text Offset**: After the `00` terminator (+7 bytes from F4)

**Usage**: Alternative player response at the same decision point. Lines with the same `choice_group_id` are presented as alternatives to the player. The game displays one choice (FD pattern) by default, but other choices (F4 FB patterns) with matching choice_group_id are also available.

**Key Insight**: The third byte in both FD and F4 FB patterns is the `choice_group_id`, NOT a speaker ID. Lines sharing the same choice_group_id represent alternative responses at the same point in the conversation tree, even if they appear far apart in the file.

### 5. F8 Pattern - Embedded Dialogue

**Structure within text**: `[main_text] F8 [XX] [XX] [control] [speaker_id] 08 [sep] [idx] 00 [embedded_text]`

**Example** (Index 0x18 contains embedded index 0x19):
- Main: "No vuelvas sin ellos"
- Embedded (0x19): "Los con qué?"

**Usage**: Inline interruptions or follow-up questions that branch from the middle of a line.

## Control Codes Summary

| Code | Name | Meaning |
|------|------|---------|
| `FD` | Line separator | Standard conversation line |
| `FE` | Initial greeting marker | First-time conversation flag (follows FD) |
| `F7` | Return entry | Subsequent conversation entry point |
| `F8` | Embedding marker | Inline dialogue branch |
| `FB` | Continue speaker | Same speaker continues |
| `FC` | Speaker change | Different speaker |
| `F1` | New speaker | New speaker introduction |
| `F4` | Alternative choice | Marks alternative player response (followed by FB) |

## Choice Group ID System

The third byte in both `FD` and `F4 FB` patterns is the **choice_group_id**, not a speaker ID:

```
FD [control] [choice_group_id] 08 [sep] [index] 00 [text]
F4 FB [choice_group_id] 08 [sep] [index] 00 [text]
```

Lines with the **same choice_group_id** represent **alternative player responses** at the same decision point:

**Example from Room 2:**
- After NPC says "Bueno ... Si prescindimos..." (index 0x0E)
- Player has multiple responses, all with choice_group_id = **0x03**:
  - Index 0x0F (FD): "Todav}a es muy caro para mi"
  - Index 0x27 (F4 FB): "Yo no uso ese tipo de ropa"

These appear far apart in the file but are linked by their matching choice_group_id.

## Conversation Flow

### First Conversation (`sprite_talk_count = 0`)
1. Game uses entry index 6 → points to FD FE line (0x0A)
2. NPC: "¿Te apecete pasar un buen rato, guapo?" ← **INITIAL GREETING**
3. Player responds with index 0x0B
4. Conversation tree continues...
5. When conversation ends, `sprite_talk_count` increments to 1

### Return Conversation (`sprite_talk_count = 1`)
1. Game uses entry index 7 → points to F7 line (0x2B)
2. NPC: "¿Has conseguido los condones?" ← **RETURN GREETING**
3. Conversation continues from this point

## Room 2 Complete Line List

| Index | Speaker | Type | Text |
|-------|---------|------|------|
| 0x0A | NPC | INITIAL | ¿Te apecete pasar un buen rato, guapo? |
| 0x0B | ALFRED | Normal | No se, ¿Cuanto cobras? |
| 0x0C | NPC | Normal | Completo, 25000 |
| 0x0D | ALFRED | Normal | ¿No me puedes hacer una tarifa especial? |
| ... | ... | ... | ... |
| 0x2B | NPC | RETURN | ¿Has conseguido los condones? |
| 0x2C | ALFRED | Normal | Estoy en ello |
| ... | ... | ... | ... |

**Total**: 37 lines (including 2 embedded, 4 alternative choices)

**Choice Groups**: Lines are organized into choice groups by choice_group_id:
- Group 0x01: 2 alternatives (indices 0x0B, 0x29)
- Group 0x03: 2 alternatives (indices 0x0F, 0x27)
- Group 0x04: 2 alternatives (indices 0x11, 0x25)
- Group 0x05: 2 alternatives (indices 0x13, 0x23)

## Implementation Notes

### Extraction Strategy

To extract ALL conversation lines including entry points:

1. **Start scanning BEFORE the main conversation block** to catch FD FE patterns
2. **Handle four separator types**:
   - `FD FE` (+9 bytes to text) - Initial greeting
   - `F7` (+7 bytes to text) - Return greeting
   - `FD` (+7 bytes to text) - Normal flow
   - `F4 FB` (+7 bytes to text) - Alternative player choice
3. **Track choice_group_id** (3rd byte) to link alternative responses
4. **Group lines by choice_group_id** to reconstruct the decision tree
   - `FD` (+7 bytes to text)
3. **Track entry point type** (initial/return/normal) for documentation
4. **Process F8 embedded patterns** inline

### Text Pointer Table

The text pointer table at `room_data + 0x3DA` contains **runtime memory addresses** (DOS segment:offset format), not file offsets. These pointers are valid only when the data is loaded into memory by the game engine.

For static analysis, follow the entry point index calculation and scan for the appropriate separator pattern (FD FE for initial, F7 for return).

## Functions Referenced

- `handle_conversation_tree` @ 0x00018690 - Main conversation handler
- `handle_hotspot_action` @ 0x00017aaa - Sets `sprite_talk_count` before conversation
- `display_dialog_text` @ 0x0001a298 - Renders text
- `trigger_dialog_or_action` @ 0x0001a683 - Processes control codes

## Variables

- `sprite_talk_count` @ 0x0005175f - Conversation counter per NPC
- `room_data_ptr` - Pointer to current room's data structure
- `room_text_data_ptr` - Pointer to Pair 12 text data
