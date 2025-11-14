# Conversation System Documentation

## Overview

The conversation system in this game uses a tree-based structure where conversations branch based on player choices. The system is handled primarily by the function `handle_conversation_tree` at address `0x00018690`.

## Quick Reference

### Critical Discovery: Choice Detection

**The 0xFB and 0xF1 control bytes do NOT always indicate player choice menus!**

- These bytes mark dialogue segments with a **choice index**
- **If the index appears multiple times**: It's a real player choice menu
- **If the index appears only once**: It's automatic dialogue (ALFRED auto-speaks)

Example from Room 2:
- Index `[07]` appears 2 times → Player menu with 2 options
- Index `[09]` appears 1 time → ALFRED automatically says the line

### Key Control Bytes Summary

| Hex  | Purpose | Notes |
|------|---------|-------|
| 0x08 | Speaker ID | Followed by character ID (0x0D = ALFRED) |
| 0xFB | Dialogue marker | Followed by choice index - may be choice OR auto-dialogue |
| 0xF1 | Dialogue marker (alt) | Same as 0xFB |
| 0xFD | End of text | Terminates a dialogue line |
| 0xF4 | End conversation | Completely terminates conversation tree |
| 0xF7 | End branch | Returns to previous conversation level |
| 0xF8 | Action trigger | Followed by 2 parameter bytes |
| 0xFA | Disabled choice | Choice already selected/unavailable |

### Parsing Algorithm

```python
from collections import Counter

# 1. Parse all dialogue markers and collect choice indices
choice_indices = []
for marker in [0xFB, 0xF1]:
    choice_index = next_byte_after_marker
    choice_indices.append(choice_index)

# 2. Count occurrences
index_counts = Counter(choice_indices)

# 3. Determine type
for element in dialogue_elements:
    if index_counts[element.choice_index] > 1:
        element.type = "PLAYER_CHOICE"  # Real menu
    else:
        element.type = "AUTO_DIALOGUE"  # ALFRED auto-speaks
```

## Data Location

- **Storage**: Conversations are stored in resource pair 12
- **Structure**: Text starts after sprite/hotspot descriptions
- **Description Count**: `sprite_count + hotspot_count` (all sprites, not just selectable ones)
- **Example**: Room 2 has 4 sprites + 6 hotspots = 10 descriptions before conversations begin

## Conversation Activation

1. User long-clicks on a "selectable" sprite that allows the TALK action
2. Action popup menu appears
3. User clicks on the talk icon
4. `handle_conversation_tree()` is called

## Control Bytes

The conversation data uses various control bytes to structure the dialogue flow:

### Text Flow Control

| Byte | Hex  | Purpose | Description |
|------|------|---------|-------------|
| -3   | 0xFD | End of text/choice | Marks the end of a dialogue line or choice option |
| -4   | 0xFC | Text terminator | Used internally to mark end of text processing |
| -5   | 0xFB | Choice/Dialogue marker | **Critical**: Followed by choice index byte. Does NOT always mean "player choice menu" - see Choice Detection below |
| -6   | 0xFA | Skip/disabled choice | Marks a choice that has been selected or is disabled |
| -7   | 0xF9 | Page break | New text block/page, used when text spans multiple screens |
| -8   | 0xF8 | Action trigger | Triggers a conditional check or action (followed by 2 parameter bytes) |
| -10  | 0xF6 | Line continuation | Indicates text continues on next line |
| -12  | 0xF4 | End conversation | Completely ends the conversation and terminates tree |
| -15  | 0xF1 | Choice/Dialogue marker (alt) | Alternative to 0xFB, same behavior - see Choice Detection |
| -16  | 0xF0 | Go back | Return to previous menu/choice level |
| -21  | 0xEB | Alternate end marker | Alternative conversation end marker |
| -9   | 0xF7 | End branch | Ends current conversation branch, returns to previous level |
| -11  | 0xF5 | Unknown end marker | Another conversation termination variant |
| -2   | 0xFE | Unknown end marker | Another conversation termination variant |

## Choice Detection Algorithm (Critical Discovery)

**The 0xFB and 0xF1 bytes do NOT always indicate a player choice menu!** They mark dialogue segments, and the **choice index byte** determines whether it's a real choice or automatic dialogue.

### Choice Index Byte

Immediately after 0xFB or 0xF1, there is a **choice index** byte (e.g., 0x01, 0x02, 0x03, etc.).

### The Key Rule: Multiple Occurrences = Real Choice

**If a choice index appears multiple times in the conversation data, it represents an actual player choice menu.**
**If a choice index appears only once, it's automatic dialogue continuation (ALFRED auto-speaks).**

### Examples from Room 2

Choice indices in Room 2: `[01][02][03][04][05][06][07][08][09][0A]`

**Real Choices (appear 2+ times):**
- Index `[01]` appears 2 times → Player gets 2 options to choose from
- Index `[03]` appears 2 times → Player gets 2 options
- Index `[04]` appears 2 times → Player gets 2 options
- Index `[05]` appears 2 times → Player gets 2 options
- Index `[06]` appears 2 times → Player gets 2 options
- Index `[07]` appears 2 times → Player gets 2 options

**Auto-Dialogue (appear only once):**
- Index `[02]` appears 1 time → ALFRED automatically speaks this line (no menu)
- Index `[08]` appears 1 time → ALFRED automatically speaks
- Index `[09]` appears 1 time → ALFRED automatically speaks (e.g., "¿ Eso es lo de la bomba bacteriológica de Mururoa ?")
- Index `[0A]` appears 1 time → ALFRED automatically speaks

### Implementation

```python
from collections import Counter

# Count all choice indices in conversation
choice_indices = []  # Collect all indices after 0xFB/0xF1
index_counts = Counter(choice_indices)

# Determine if each index is a real choice
for index in choice_indices:
    is_real_choice = index_counts[index] > 1
    # if is_real_choice: render as "CHOICE X:"
    # else: render as "ALFRED:" (auto-dialogue)
```

### Why This Matters

- **Misinterpreting auto-dialogue as choices** creates incorrect conversation trees
- The game uses the same 0xFB marker for both player choices AND automatic dialogue
- Only the **count of each index** reveals the true structure
- This allows ALFRED to automatically continue conversations without player input

### Character/Display Control

| Byte | Hex  | Purpose | Description |
|------|------|---------|-------------|
| 8    | 0x08 | Character ID | Followed by a byte indicating which character is speaking (0x0D = ALFRED, others = NPCs) |
| 32   | 0x20 | Space | Standard space character |
| 13   | 0x0D | Carriage return | Line break in dialogue |

### Special Character Encoding (Extended ASCII for Spanish)

| Character | Decimal | Hex  | Notes |
|-----------|---------|------|-------|
| ñ         | 128     | 0x80 | Spanish n with tilde |
| í         | 129     | 0x81 | Accented i |
| ¡         | 130     | 0x82 | Inverted exclamation |
| ¿         | 131     | 0x83 | Inverted question mark |
| ú         | 132     | 0x84 | Accented u |
| á         | 123     | 0x7B | Accented a |
| é         | 124     | 0x7C | Accented e |
| í         | 125     | 0x7D | Accented i (alternate) |
| ó         | 126     | 0x7E | Accented o |
| ú         | 127     | 0x7F | Accented u (alternate) |

**Note**: The game uses a custom character encoding that differs from standard ASCII for characters above 0x7A.

## Conversation Tree Structure

### Basic Structure

```
[Character ID Byte: 0x08 + ID]
[Text content]
[Control byte: 0xFD] (end of line)

// Dialogue markers (may be choices OR auto-dialogue):
[Dialogue marker: 0xFB or 0xF1]
[Choice index byte: 0x01-0xFF]
[Speaker marker: 0x08]
[Speaker ID: 0x0D for ALFRED, other for NPC]
[Dialogue text]
[End marker: 0xFD]

[Dialogue marker: 0xFB or 0xF1]
[Choice index byte: same or different]
[Speaker marker: 0x08]
[Speaker ID]
[Dialogue text]
[End marker: 0xFD]

// Response to dialogue:
[Character ID: 0x08 + ID]
[Response text]
[End marker: 0xFD]

// Can lead to more dialogue or end with:
[End conversation: 0xF4 or 0xEB or 0xF5 or 0xF7 or 0xFE]
```

### Choice Index Structure

After 0xFB or 0xF1:
1. **Choice index byte** (e.g., 0x01, 0x02, 0x03...)
2. **Speaker marker** (0x08)
3. **Speaker ID** (0x0D = ALFRED, others = NPC)
4. **Text content**
5. **Terminator** (0xFD)

**Critical**: The choice index byte determines grouping:
- Same index = options in same menu
- Count > 1 = real player choice
- Count = 1 = automatic dialogue

### Room 2 Example (Verified)

**Initial Conversation:**

```
NPC: "Te apetece pasar un buen rato, guapo ?"
(20 54 65 20 61 70 65 63 65 74 65 20 70 61 73 61 72 20 75 6E 20 62 75 65 6E 20 72 61 74 6F 2C 20 67 75 61 70 6F 20 3F)

Choice 1: "No se, ¿ Cuanto cobras ?"
(4E 6F 20 73 65 2C 20 83 20 43 75 61 6E 74 6F 20 63 6F 62 72 61 73 20 3F)

Choice 2: "No puedo. Estoy buscando a una princesa"
(4E 6F 20 70 75 65 64 6F 2E 20 45 73 74 6F 79 20 62 75 73 63 61 6E 64 6F 20 61 20 75 6E 61 20 70 72 69 6E 63 65 73 61)
```

**After Choice 1:**

```
NPC: "Completo, 25000"
(43 6F 6D 70 6C 65 74 6F 2C 20 32 35 30 30 30)

Alfred: "No me puedes hacer una tarifa especial ?. Estoy muy desesperado"
(20 4E 6F 20 6D 65 20 70 75 65 64 65 73 20 68 61 63 65 72 20 75 6E 61 20 74 61 72 69 66 61 20 65 73 70 65 63 69 61 6C 20 3F 2E 20 45 73 74 6F 79 20 6D 75 79 20 64 65 73 65 73 70 65 72 61 64 6F)

NPC: "Bueno ... Si prescindimos de la lencería sexy, podría dejártelo en 20000"
(42 75 65 6E 6F 20 2E 2E 2E 20 53 69 20 70 72 65 73 63 69 6E 64 69 6D 6F 73 20 64 65 20 6C 61 20 6C 65 6E 63 65 72 7D 61 20 73 65 78 79 2C 20 70 6F 64 72 7D 61 20 64 65 6A 7B 72 74 65 6C 6F 20 65 6E 20 32 30 30 30 30)

Choice 1: "Todavía es muy caro para mi. ¿ Que más me puedes rebajar ?"
(54 6F 64 61 76 7D 61 20 65 73 20 6D 75 79 20 63 61 72 6F 20 70 61 72 61 20 6D 69 2E 20 83 20 51 75 65 20 6D 7B 73 20 6D 65 20 70 75 65 64 65 73 20 72 65 62 61 6A 61 72 20 3F)

Choice 2: "Yo no uso ese tipo de ropa, ¡ eh !"
(59 6F 20 6E 6F 20 75 73 6F 20 65 73 65 20 74 69 70 6F 20 64 65 20 72 6F 70 61 2C 20 82 20 65 68 20 21)
```

**Alternative Conversation Starter (after first conversation):**

```
NPC: "¿ Has conseguido los condones ?"
(83 20 48 61 73 20 63 6F 6E 73 65 67 75 69 64 6F 20 6C 6F 73 20 63 6F 6E 64 6F 6E 65 73 20 3F FD F1 01 08 0D 2C 00)

Choice 1: "Estoy en ello"
(45 73 74 6F 79 20 65 6E 20 65 6C 6C 6F FD FC 41 08 20 2D 00)

Choice 2: "No los hay de mi tamaño, nena"
(4E 6F 20 6C 6F 73 20 68 61 79 20 64 65 20 6D 69 20 74 61 6D 61 80 6F 2C 20 6E 65 6E 61 FD FC 41 08 20 2F 00)
```

### Room 14 Example (Verified) - Encyclopedia Salesman

**Initial Conversation:**

```
Salesman: "¡ Enhorabuena caballero ! ¡ Hoy es su dia de suerte !"
(82 20 45 6E 68 6F 72 61 62 75 65 6E 61 20 63 61 62 61 6C 6C 65 72 6F 20 21 20 82 20 48 6F 79 20 65 73 20 73 75 20 64 69 61 20 64 65 20 73 75 65 72 74 65 20 21)

Choice 1: "¡ No me diga !"
(00 82 20 4E 6F 20 6D 65 20 64 69 67 61 20 21)

Choice 2: "No digas tonterías y quítate de mi camino"
(4E 6F 20 64 69 67 61 73 20 74 6F 6E 74 65 72 7D 61 73 20 79 20 71 75 7D 74 61 74 65 20 64 65 20 6D 69 20 63 61 6D 69 6E 6F)

Choice 3: "Cuántas ha vendido ya ?"
(20 43 75 7B 6E 74 61 73 20 68 61 20 76 65 6E 64 69 64 6F 20 79 61 20 3F)
```

## Detailed Byte Sequence Examples

### Real Player Choice (Index appears 2+ times)

From Room 2, Choice Index [07]:

**First occurrence at offset 0x0246:**
```
FB 07 08 0D    [Choice marker][Index 07][Speaker][ALFRED ID]
45 73 74 6F 6F 6F 20 2E 2E 2E 20 41 68 6F 72 61 20 6D 69 73 6D 6F 20 6E 6F 20 74 65 6E 67 6F 2E 20 56 6F 79 20 61 20 62 75 73 63 61 72 6C 6F 73
["Estooo ... Ahora mismo no tengo. Voy a buscarlos"]
FD             [End of text]
```

**Second occurrence at offset 0x029A:**
```
FB 07 08 0D    [Choice marker][Index 07][Speaker][ALFRED ID]
83 20 4C 6F 73 20 63 6F 6E 20 71 75 7C 20 3F
["¿ Los con qué ?"]
FD             [End of text]
```

**Result**: Index [07] appears 2 times → Player sees menu with 2 choices

### Auto-Dialogue (Index appears only once)

From Room 2, Choice Index [09] at offset 0x073B:

```
FB 09 08 0D    [Choice marker][Index 09][Speaker][ALFRED ID]
83 20 45 73 6F 20 65 73 20 6C 6F 20 64 65 20 6C 61 20 62 6F 6D 62 61 20 62 61 63 74 65 72 69 6F 6C 7E 67 69 63 61 20 64 65 20 4D 75 72 75 72 6F 61 20 3F
["¿ Eso es lo de la bomba bacteriológica de Mururoa ?"]
FD             [End of text]
```

**Result**: Index [09] appears 1 time → ALFRED automatically speaks (no menu)

### Action Trigger Example

```
F8 XX XX       [Action marker][Parameter 1][Parameter 2]
```

The two parameter bytes determine which action/condition to check from the handler table at 0x47e58.

### Complete Conversation Segment with All Control Bytes

From Room 2, showing full structure:

```
08 20          [Speaker: NPC]
54 65 20 61 70 65 63 65 74 65 20 70 61 73 61 72 20 75 6E 20 62 75 65 6E 20 72 61 74 6F 2C 20 67 75 61 70 6F 20 3F
["Te apetece pasar un buen rato, guapo ?"]
FD             [End NPC text]

FB 01 08 0D    [Choice marker][Index 01][Speaker][ALFRED]
4E 6F 20 73 65 2C 20 83 20 43 75 61 6E 74 6F 20 63 6F 62 72 61 73 20 3F
["No se, ¿ Cuanto cobras ?"]
FD             [End choice 1]

FB 01 08 0D    [Choice marker][Index 01 AGAIN][Speaker][ALFRED]
4E 6F 20 70 75 65 64 6F 2E 20 45 73 74 6F 79 20 62 75 73 63 61 6E 64 6F 20 61 20 75 6E 61 20 70 72 69 6E 63 65 73 61
["No puedo. Estoy buscando a una princesa"]
FD             [End choice 2]

08 20          [Speaker: NPC]
43 6F 6D 70 6C 65 74 6F 2C 20 32 35 30 30 30
["Completo, 25000"]
FD             [End NPC response]

FB 02 08 0D    [Choice marker][Index 02 - ONLY ONCE][Speaker][ALFRED]
4E 6F 20 6D 65 20 70 75 65 64 65 73 20 68 61 63 65 72 20 75 6E 61 20 74 61 72 69 66 61 20 65 73 70 65 63 69 61 6C 20 3F
["No me puedes hacer una tarifa especial ?"]
FD             [End auto-dialogue]

08 20          [Speaker: NPC]
42 75 65 6E 6F 20 2E 2E 2E
["Bueno ..."]
FD             [End NPC response]

F4             [END_CONV - Terminate conversation]
```

**Analysis:**
- Index [01] appears 2 times → Real choice menu with 2 options
- Index [02] appears 1 time → Auto-dialogue (ALFRED speaks automatically)
- 0xF4 terminates the entire conversation tree

## Text Display Algorithm

### Line Breaking

The system automatically breaks text into multiple lines based on:

1. **Maximum line width**: 47 characters (0x2f)
2. **Maximum lines per screen**: 4-5 lines
3. **Word boundary detection**: Searches for space characters (0x20)

When text exceeds line width:
- System searches backward for last space
- Breaks line at space
- Inserts `0xF6` (line continuation marker)

### Multi-screen Text

For very long dialogue that doesn't fit on one screen:
- System uses `0xF9` (page break) marker
- Followed by `0x08` and character ID byte
- Text continues on new screen
- Player must click to continue

### Example: Long Text Broken into Two Screens

```
Line 1: "Los con qué? Pero tu no sabes que en 1981 se identificó a cinco personas enfermas con una patología hasta entonces desconocida que era de origen vírico según las tesis oficiales (aunque yo me reservo mi opinión: después si"

[0xF9 0x08 ID] (page break)

Line 2: "te interesa te la doy) y que se la denominó con el nombre de SIDA. ¿ Tus padres no te han hablado del SIDA y de preservativos ?. ¿ En la escuela tampoco ?"
```

## Display Timing

The system likely calculates display time based on:

1. **Text length**: Longer text displays longer
2. **Character count**: Each character adds to display time
3. **Manual progression**: Player can click to advance (in some cases)

Timing calculation appears to use:
- Base time per character
- Minimum display time
- Maximum display time cap

## Complete Parsing Workflow

### Step 1: Locate Conversation Data

1. Read room data from ALFRED.1
2. Access pair 12 (conversations)
3. Count sprites and hotspots for the room
4. Skip `(sprite_count + hotspot_count)` descriptions
5. Conversation data starts after descriptions

### Step 2: Parse All Elements

Scan through conversation data byte by byte:

```python
while pos < len(conv_data):
    if data[pos] == 0x08:  # SPEAKER
        speaker_id = data[pos + 1]
        pos += 2
        # Read text until control byte

    elif data[pos] in [0xFB, 0xF1]:  # DIALOGUE MARKER
        pos += 1
        choice_index = data[pos]  # CRITICAL: Store this!
        pos += 1
        # Skip speaker bytes (0x08 + ID)
        pos += 2
        # Read text until control byte

    elif data[pos] == 0xF8:  # ACTION
        pos += 3  # Skip action + 2 parameter bytes

    elif data[pos] == 0xF4:  # END_CONV
        # Mark conversation end
        pos += 1

    elif data[pos] == 0xF7:  # END_BRANCH
        # Mark branch end
        pos += 1
```

### Step 3: Count Choice Indices

```python
from collections import Counter

# After parsing, count all choice indices
choice_indices = [...]  # All indices collected in Step 2
index_counts = Counter(choice_indices)

# Example result:
# Counter({0x01: 2, 0x03: 2, 0x07: 2, 0x02: 1, 0x09: 1})
```

### Step 4: Mark Real Choices vs Auto-Dialogue

```python
for element in elements:
    if element.has_choice_index:
        count = index_counts[element.choice_index]
        element.is_real_choice = (count > 1)
```

### Step 5: Build Tree Structure

- Start with NPC root dialogue
- For each dialogue marker:
  - **If is_real_choice == True**: Create CHOICE node (player menu)
  - **If is_real_choice == False**: Create ALFRED auto-dialogue node
- Nest based on index values (higher index = deeper nesting)
- Terminate branches on 0xF4, 0xF7, etc.

## Choice Selection

### Display

- Choices are rendered at bottom of screen
- Position calculation: `400 - (choice_count * 16)` pixels from top
- Each choice occupies 16 pixels vertically
- Maximum of 10 choices supported (though rarely used)
- **Only real choices (count > 1) are displayed in menu**

### Selection

- Mouse Y position is checked against choice regions
- Formula: `(mouse_y - y_offset) >> 4 & 7`
- Clicking a choice:
  1. Alfred speaks the choice text
  2. NPC responds
  3. May lead to more choices or end conversation
- **Auto-dialogue (count = 1) plays automatically without player input**

### Special Choice: 0xFA (Disabled)

When a choice has been selected before or shouldn't be shown:
- Choice marker is written to file with `0xFA`
- Game seeks to file position and writes the byte
- This permanently marks the choice as "used" in save data

## Conditional Actions (0xF8)

The `0xF8` control byte triggers conditional logic:

1. Followed by 2 bytes (likely condition parameters)
2. System checks table at `0x47e58` for condition handlers
3. Each entry: `[condition_id: 2 bytes][function_pointer: 4 bytes]`
4. If condition ID matches, corresponding function is called
5. Function can:
   - Modify game state
   - Trigger animations
   - Give/take inventory items
   - Change conversation flow

## Back Navigation (0xF0)

The `0xF0` control byte allows returning to previous choice:

1. System searches backward through conversation data
2. Looks for previous `0xFB` or `0xF1` markers
3. Finds choice with lower ID number
4. Re-displays that choice set
5. Allows player to explore different conversation branches

## Important Memory Locations

| Address    | Purpose |
|------------|---------|
| 0x0004f8a4 | Array of choice text pointers (up to 10) |
| 0x0004f8d6 | Array of choice text lengths |
| 0x00051694 | Current selected choice index |
| 0x00051762 | Total number of choices |
| 0x0005177f | Single choice flag (1 = only one choice) |
| 0x00051785 | In conversation flag |
| 0x00051791 | Dialog display active flag |
| 0x0004fb94 | Current room number |
| 0x0004fb9a | Current character/NPC ID |
| 0x0004fac8 | Room data pointer |
| 0x0004facc | Room text data pointer |

## Conversation Data Format

Each conversation entry in pair 12:

```
[Header - possibly offsets/metadata]
[Sprite/Hotspot descriptions × (sprite_count + hotspot_count)]
[Conversation data starts here]
  [Character byte: 0x08 + character_id]
  [Text content]
  [Control byte: 0xFD]
  [Choices if any]
  [Responses]
  [More choices or end markers]
```

## Key Functions

| Function | Address | Purpose |
|----------|---------|---------|
| `handle_conversation_tree` | 0x00018690 | Main conversation loop |
| `display_dialog_text` | 0x0001a298 | Renders dialogue text to screen |
| `trigger_dialog_or_action` | 0x0001a683 | Processes control bytes and triggers actions |
| `handle_hotspot_action` | 0x00017aaa | Initiates conversation when hotspot clicked |

## Troubleshooting Common Parsing Issues

### Issue: Auto-dialogue marked as player choices

**Problem**: Lines like "¿ Eso es lo de la bomba bacteriológica de Mururoa ?" show up as CHOICE when they should be ALFRED auto-dialogue.

**Solution**: Count occurrences of each choice index. Only indices appearing 2+ times are real choices.

```python
# WRONG: Treating all 0xFB as choices
if byte == 0xFB:
    create_choice_node()

# CORRECT: Count indices first
index_counts = Counter(all_choice_indices)
if byte == 0xFB and index_counts[choice_index] > 1:
    create_choice_node()
else:
    create_auto_dialogue_node()
```

### Issue: Garbled text with control characters

**Problem**: Text appears with garbage like `"ANo me diga"` or `"#Bueno"`.

**Solution**: Clean leading control bytes that leak into text:

```python
def clean_text(text):
    # Remove [XX][00] patterns at start
    while '[' in text[:15]:
        # Remove bracket sequences

    # Remove single leading control characters
    if text[0] in 'AH#%\')!+,.-"*&$(/':
        text = text[1:].lstrip()

    return text.strip()
```

### Issue: Incorrect nesting/indentation

**Problem**: Conversation tree depth doesn't match actual game behavior.

**Solution**:
1. Use choice index values to determine depth (higher index = deeper)
2. Pop stack when encountering 0xF7 (END_BRANCH)
3. Clear stack on 0xF4 (END_CONV)
4. Compare same indices to group choices at same level

### Issue: Missing conversations or descriptions

**Problem**: Parser finds no conversations for a room that should have them.

**Solution**: Ensure you skip the correct number of descriptions:
- Count ALL sprites (not just selectable ones)
- Count ALL hotspots (even non-interactive ones)
- Each description ends with 0xFD
- Conversation data starts after last description

## Verification Checklist

When exporting conversation trees, verify:

- [ ] Choice indices appearing 2+ times are marked as CHOICE
- [ ] Choice indices appearing once are marked as ALFRED: (auto-dialogue)
- [ ] No control byte artifacts in displayed text
- [ ] Proper indentation showing conversation depth
- [ ] TERMINATES markers at conversation ends (0xF4)
- [ ] Branch ends properly handled (0xF7)
- [ ] Spanish special characters render correctly (ñ, á, é, í, ó, ú, ¿, ¡)
- [ ] All 51 rooms with conversations export successfully

## Tools

### export_trees_correct.py

The final, verified conversation tree exporter implementing all discoveries:

**Features:**
- Counts choice index occurrences using `collections.Counter`
- Distinguishes real choices from auto-dialogue
- Cleans control byte artifacts from text
- Builds proper tree structure with correct nesting
- Exports all 51 rooms or individual room

**Usage:**
```bash
# Export single room
python3 export_trees_correct.py 2

# Export all rooms
python3 export_trees_correct.py --all
```

**Output:**
- Directory: `conversation_trees_final/`
- Format: `roomXX_tree.txt` (e.g., `room02_tree.txt`)
- Structure: Human-readable indented tree

## Notes

- The system supports cyclic conversations (returning to earlier states)
- Conversations can be nested multiple levels deep
- The tree structure allows for complex branching narratives
- Some conversations change based on game state (items, flags, etc.)
- Character ID determines portrait/avatar shown during dialogue
- The 0x08 byte is a "set speaker" command followed by speaker ID
- **Critical discovery**: 0xFB/0xF1 do NOT always mean "choice menu" - use index counting instead
- Room 2 verified against manual analysis: 6 real choices, 4 auto-dialogues
- Room 14 verified: Encyclopedia salesman with deep nested choices
- Total rooms with conversations: 51 out of 55 rooms
