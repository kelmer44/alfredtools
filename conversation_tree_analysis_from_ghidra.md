# Conversation Tree Structure - Analysis from Ghidra

## Overview
Based on reverse-engineering the game's code in Ghidra, here's how the conversation system works:

## 1. Text Data Loading (from `load_room_data()` @ 0x000152f5)

### Pair 12 Loading
```c
// Load Pair 12 (text data) into room_text_data_ptr
text_scanner = room_text_data_ptr;
uVar3 = *(undefined4 *)(local_24 + 100);  // Pair 12 size
file_seek(DAT_0004f8f0, *(undefined4 *)(local_24 + 0x60));  // Pair 12 offset
file_read(text_scanner, uVar3, DAT_0004f8f0);
```

### Text Pointer Table Construction

The game builds a **text pointer table** at offset `+0x3DA` in the room data structure by scanning through Pair 12 and looking for marker bytes:

```c
cVar6 = '\0';
uVar8 = 0;
uVar11 = 0;
text_scanner = room_text_data_ptr;

while (cVar9 = (char)uVar11, cVar6 != -0xb) {  // -0xb = 0xF5 (end marker)
  cVar6 = *text_scanner;

  // TEXT INDEXING SYSTEM:
  // 0xFF marker = new text entry for selectable sprites/hotspots
  if (cVar6 == -1) {  // -1 = 0xFF
    text_scanner = text_scanner + 2;
    *(char **)(room_data_ptr + uVar8 * 4 + 0x3da) = text_scanner;
    uVar8 = (uint)(byte)((char)uVar8 + 1);
  }

  // 0xFE marker = conditional text entry
  if (cVar6 == -2) {  // -2 = 0xFE
    text_scanner = text_scanner + 2;

    // Check if condition flag is set for this room
    if ((&DAT_0004fba4)[(uint)room_number * 4 + uVar11] != '\0') {
      // Skip past conditional text section
      do {
        wait_or_process_input();
        cVar6 = *text_scanner;
        if (cVar6 == -9) {  // -9 = 0xF7
          // Handle nested structure
        }
        text_scanner = text_scanner + 1;
      } while (/* condition */);
    }

    *(char **)(room_data_ptr + uVar8 * 4 + 0x3da) = text_scanner;
    uVar8 = (uint)(byte)((char)uVar8 + 1);
    uVar11 = (uint)(byte)(cVar9 + 1);
  }

  text_scanner = text_scanner + 1;
}
```

**Key Finding:** The text pointer table is indexed by the **order of appearance** of 0xFF and 0xFE markers, NOT by the index bytes within the conversation data!

## 2. Conversation Entry Structure

Based on our extraction analysis and the Ghidra code, each conversation entry has this structure:

```
FD [CONTROL] [SPEAKER] 08 [SEP] [INDEX] 00 [TEXT...]
```

Where:
- `FD` = Entry separator (marks start of new dialogue line)
- `CONTROL` = FB (continue), FC (change), F1 (new speaker)
- `SPEAKER` = Speaker ID (byte)
- `08` = Fixed marker
- `SEP` = Speaker separator (0x0D = ALFRED, 0x20 = NPC)
- `INDEX` = Position in conversation tree (byte)
- `00` = Null terminator
- `TEXT` = ASCII text with possible embedded control codes

## 3. Embedded Dialogue Lines

### Discovery
Line 0x18 in Room 2 contains TWO dialogue lines:
1. NPC: "No vuelvas sin ellos" (Don't come back without them)
2. ALFRED: "¿Los con qué?" (With what?) - **This is a CHOICE**

### Pattern
```
[MAIN_LINE_HEADER] [TEXT1] F8 [XX] [XX] FB/FC/F1 [SPEAKER] 08 [SEP] [EMBEDDED_INDEX] 00 [TEXT2]
```

The `F8` byte acts as an **embedding marker**, followed by two bytes, then a complete control structure for the embedded line (but **WITHOUT the FD prefix**).

### Example from Room 2 (offset 0x0274):
```
FD FC 41 08 20 18 00                              // Line 0x18 header (NPC)
4E 6F 20 76 75 65 6C 76 61 73 20 73 69 6E 20     // "No vuelvas sin "
65 6C 6C 6F 73                                    // "ellos"
F8 48 01                                          // Embedding marker + 2 bytes
FB 07 08 0D 19 00                                 // Embedded line 0x19 header (ALFRED) - NO FD!
83 20 4C 6F 73 20 63 6F 6E 20 71 75 7C 20 3F     // "¿Los con qu|?"
```

**Key observation:** The embedded line (0x19) is a **player choice** that appears after the NPC's line.

## 4. How Choices Work

### Hypothesis Based on Evidence

1. **No explicit "choice" marker byte exists** - we've confirmed this through extensive analysis

2. **Choices are indicated by CONTEXT**:
   - When multiple ALFRED lines appear with sequential or near-sequential indices
   - When an ALFRED line is embedded within an NPC line using the F8 pattern
   - The game tracks conversation state using the index bytes

3. **Index-based tree navigation**:
   - Each line has an index byte (0x00, 0x01, 0x02, ... 0x18, 0x19, etc.)
   - Index gaps indicate branching points
   - The engine follows indices to navigate the conversation tree
   - Multiple responses with different indices = choice branches

### Room 2 Example
```
Line 0x00 (idx 00): NPC  - "¿Oye, quieres trabajar en la construcción?"
Line 0x01 (idx 01): ALFRED - "No se, cuanto cobras?"  [CHOICE A]
Line 0x02 (idx 02): ALFRED - "Como construcción?"     [CHOICE B]
...
Line 0x18 (idx 18): NPC  - "No vuelvas sin ellos"
Line 0x19 (idx 19): ALFRED - "¿Los con qu|?" [EMBEDDED CHOICE - triggered by line 0x18]
```

When the NPC says line 0x18, the embedded line 0x19 becomes available as a response choice.

## 5. Display Function (`display_dialog_text()` @ 0x0001a298)

This function handles text rendering with word wrapping and pagination:

```c
void display_dialog_text(void) {
  // ... initialization ...

  do {
    wait_or_process_input();
    local_28 = '\0';

    // Scan for word boundaries or control codes
    for (pcVar12 = pcVar11;
        (((cVar2 = *pcVar12, cVar2 != ' ' && (cVar2 != -3)) && (cVar2 != -0xc)) &&
        ((cVar2 != -8 && (cVar2 != -0x10))));
        pcVar12 = pcVar12 + 1) {
      local_28 = local_28 + '\x01';
      _DAT_00051794 = _DAT_00051794 + 1;
    }

    cVar2 = *pcVar12;
    // Check for line-ending control codes
    if (((cVar2 == -3) || (cVar2 == -0xc)) ||   // FD or F4
        ((cVar2 == -8 || (cVar2 == -0x10)))) {  // F8 or F0
      bVar3 = true;
    }

    // Handle F8 code (adds extra spacing/formatting)
    bVar9 = local_28 + 1;
    if (*pcVar12 == -8) {  // F8
      bVar9 = local_28 + 3;
    }

    // Word wrapping logic...
    // Pagination when screen fills...

  } while (!bVar3);
}
```

**Key findings:**
- F8 is treated specially - adds 3 characters worth of spacing
- This supports our finding that F8 marks embedded dialogue
- The function handles display but doesn't parse the tree structure

## 6. Trigger Function (`trigger_dialog_or_action()` @ 0x0001a683)

This function processes the text byte-by-byte and handles control codes for display:

```c
// Scans through text checking for:
// -3 (0xFD) = line separator
// -12 (0xF4) = paragraph break
// -8 (0xF8) = embedding marker (special formatting)
// -7 (0xF9) = unknown
// -16 (0xF0) = unknown
// -21 (0xEB) = unknown
```

This function is more about **display execution** than tree parsing.

## 7. Tree Structure Summary

### Data Storage
- All dialogue lines stored **sequentially** in Pair 12
- Separated by `FD` bytes
- Each line has an index byte
- Some lines embedded within others using `F8` pattern

### Runtime Parsing
1. Game loads Pair 12 into memory
2. **Scans for 0xFF markers** to build text pointer table for descriptions/hotspots
3. Conversation data (after 0xFF sections) contains dialogue with FD separators
4. Engine maintains **current conversation index**
5. When displaying NPC line, checks for **embedded ALFRED responses** (F8 pattern)
6. If multiple ALFRED lines available (sequential indices or embedded), presents as **choices**
7. Player selects choice → engine jumps to that index → continues from there

### Choice Detection Algorithm (Inferred)
```python
def get_available_choices(current_index):
    choices = []

    # 1. Check if current line (NPC) contains embedded ALFRED line
    if has_embedded_line(current_index):
        embedded_idx = extract_embedded_index(current_index)
        choices.append(embedded_idx)

    # 2. Check for sequential ALFRED lines after current
    next_idx = current_index + 1
    while line_exists(next_idx) and is_alfred_line(next_idx):
        choices.append(next_idx)
        next_idx += 1

    # 3. If only one choice, it's a required response (not really a choice)
    # 4. If multiple choices, present selection menu to player

    return choices
```

## 8. Remaining Questions

1. **How does the engine determine conversation entry points?**
   - Likely triggered by hotspot/object actions
   - May use the text pointer table indices

2. **How are conversation state/flags managed?**
   - Reference to `DAT_0004fba4` array suggests per-room flags
   - May track which conversations have been seen

3. **What determines conversation end?**
   - Probably when no ALFRED responses available
   - Or when reaching a terminal NPC line with no embedded choices

4. **F8 two-byte payload meaning?**
   - The two bytes after F8 (e.g., `48 01` in line 0x18) - what do they mean?
   - Possibly: timing, display delay, or formatting flags

## 9. Updated Control Code Table

| Hex | Dec | Symbol | Meaning | Context |
|-----|-----|--------|---------|---------|
| FD | -3 | ␍ | Line separator | Marks start of new dialogue entry |
| FC | -4 | ␌ | Speaker change | In control structure |
| FB | -5 | ␛ | Continue speaker | In control structure |
| F8 | -8 | ␘ | Embedding marker | Precedes embedded dialogue, adds spacing |
| F7 | -9 | ␗ | Unknown | Seen in conditional sections |
| F4 | -12 | ␔ | Paragraph break | Forces new screen |
| F1 | -15 | ␑ | New speaker | In control structure |
| F0 | -16 | ␐ | Unknown | Checked in display function |
| EB | -21 | ␛ | Unknown | Checked in display function |
| FF | -1 | ␡ | Text section marker | Marks description/hotspot text start |
| FE | -2 | ␞ | Conditional marker | Conditional text based on game state |
| F5 | -11 | ␕ | End marker | Terminates text data section |

## Conclusion

The conversation system is a **flat sequential format** that the engine interprets as a tree:
- Data is stored linearly with FD separators
- Index bytes provide tree navigation
- Choices indicated by: multiple sequential ALFRED lines OR embedded F8 patterns
- No explicit "choice marker" byte exists
- Tree structure emerges from the pattern of NPC/ALFRED line alternation and index gaps
- Embedded dialogue (F8 pattern) allows NPC lines to contain immediate player response options

This is an elegant compression technique - stores tree as flat data, uses indices for navigation!
