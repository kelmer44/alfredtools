# Alfred Pelrock - Text Display Algorithm Documentation

## Summary

I analyzed the decompiled game executable using the Ghidra MCP server and found the text display and word wrapping algorithm used in Alfred Pelrock.

## Function Location

**Function:** `display_dialog_text` at address `0x0001a298`

This function handles all text display for:
- Hotspot descriptions (when examining objects)
- NPC dialogue
- Character speech

## Algorithm Overview

### Constants
- **MAX_CHARS_PER_LINE:** 47 characters (`0x2F`)
- **MAX_LINES:** 4 lines per page
- **Text Color:** Pink (palette index 13) for hotspot descriptions

### Word Wrapping Strategy

The algorithm processes text **word by word** with the following logic:

1. **Initialize state:**
   - `chars_remaining_on_line = 0x2F` (47 characters)
   - `current_line_number = 0`

2. **For each word:**
   - Calculate word length (includes the trailing space)
   - **Key decision:** `if (chars_remaining_on_line < word_length)`
     - If true: wrap to next line, reset chars_remaining to 47
     - If false: add word to current line
   - Decrement `chars_remaining_on_line` by `word_length`

3. **Line management:**
   - After 4 lines, create a new page
   - Insert control character `0xF9` for page breaks

4. **Text centering:**
   - For lines shorter than 46 characters
   - Center by adding spaces on the left
   - Formula: `padding = (47 - line_length) / 2`

### Control Characters

The text uses special control characters (stored as signed chars):

| Hex  | Dec   | Purpose            |
|------|-------|--------------------|
| 0xFD | -3    | End of text marker |
| 0xF4 | -12   | Alt end marker     |
| 0xF8 | -8    | End marker (adds 3 to word length) |
| 0xF0 | -16   | Alt end marker     |
| 0xF6 | -10   | Newline marker     |
| 0xF9 | -7    | Page break marker  |
| 0x20 | 32    | Space (word boundary) |

### Example

**Input text (hex):**
```
AD 20 41 68 68 20 21 20 4E 6F 63 68 65 73 20 64 65 20
6C 61 20 67 72 61 6E 20 63 69 75 64 61 64 2E 2E 2E 20
43 6F 6D 6F 20 64 69 6A 6F 20 65 6C 20 70 6F 65 74 61 FD
```

**Decoded:**
```
¡ Ahh ! Noches de la gran ciudad... Como dijo el poeta
```

**Output (wrapped):**
```
Line 1: ¡ Ahh ! Noches de la gran ciudad... Como dijo
Line 2: el poeta.
```

**Explanation:**
1. Process word by word: "¡ ", "Ahh ", "! ", "Noches ", "de ", "la ", "gran ", "ciudad... ", "Como ", "dijo "
2. After "dijo ", chars_remaining = 0 (exactly)
3. Next word "el " has length 3
4. Since `0 < 3`, wrap to line 2
5. Line 2 gets "el poeta"

## Edge Cases

### Screen Clamping
- Text is clamped against screen edges (640x400 resolution)
- When text would extend past right edge, it wraps
- When text would extend past bottom edge, new page is created

### Special Characters
The game uses custom encoding for Spanish characters:
- `0xAD` → `¡` (inverted exclamation)
- `0x80` → `ñ`
- `0x82` → `¡`
- `0x7B` → `á`
- `0x7C` → `é`
- `0x7D` → `í`
- `0x7E` → `ó`
- `0x7F` → `ú`

(See `main7.cpp::getExtraCharacters()` for full mapping)

## Ghidra Annotations Added

I added the following annotations to the Ghidra project:

1. **Variable renames in `display_dialog_text`:**
   - `local_28` → `word_length`
   - `local_38` → `text_buffer`

2. **Data renames:**
   - `DAT_0005856a` → `chars_remaining_on_line`
   - `DAT_0005856b` → `current_line_number`

3. **Comments:**
   - At 0x0001a2e7: "DAT_0005856a appears to be remaining characters on current line (starts at 0x2f = 47)"
   - At 0x0001a2ea: "DAT_0005856b appears to be current line number (max 4 lines)"
   - At 0x0001a35e: "Key decision: if chars_remaining < word_length, wrap to next line"
   - At 0x0001a57b: "Centering algorithm: for lines shorter than 46 chars, center them by adding spaces on the left"

## Related Functions

- `trigger_dialog_or_action` (0x0001a683): Renders the formatted text with font
- `handle_conversation_tree` (0x00018690): Manages NPC dialogue trees
- `FUN_000140cd` (0x000140cd): Called after text display (currently empty stub)

## Files

- `text_display_algorithm.py`: Python implementation of the algorithm
- This document: Summary of findings
