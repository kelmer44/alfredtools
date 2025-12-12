# Conversation Simulator - Usage Examples

## Basic Usage

The conversation simulator lets you interactively experience conversations as they appear in the game.

### From Resource File

```bash
# Simulate a conversation from a resource file
python simulate_conversation.py ALFRED1 12345

# Where:
#   ALFRED1 = resource file name
#   12345 = byte offset to conversation data
```

### From Hex Data

```bash
# Provide conversation data directly in hex format
python simulate_conversation.py --hex "08 0D 48 6F 6C 61 FD FB 01 08 0D 53 69 FD FB 01 08 0D 4E 6F FD F4"
```

## How It Works

1. **Display Text**: Each dialogue line is shown with the speaker name
   - Press Enter to advance to the next line

2. **Choices**: When choices appear, you'll see a menu:
   ```
   ============================================================
   CHOICES:
   ============================================================
     [1] First choice option
     [2] Second choice option
     [3] Third choice option

   Select choice (1-3):
   ```

3. **Auto-dialogue**: If a "choice" only appears once in the data, ALFRED automatically speaks it:
   ```
   ALFRED: (automatically)
     This line is spoken without player input
   ```

4. **Disabled Choices**: Previously selected choices are marked:
   ```
     [1] [DISABLED] Already selected this
     [2] Available choice
   ```

## Finding Conversation Data

To use the simulator, you need to extract conversation data from the game's resource files.

### Method 1: Extract from Resource Pair 12

Conversations are stored in resource pair 12 (e.g., `ALFRED1` file).

```python
# Example: Extract Room 2 conversation data
import struct

with open('ALFRED1', 'rb') as f:
    # Resource pair 12 structure varies by room
    # You'll need to find the correct offset for your target conversation
    f.seek(offset_to_conversation)
    conversation_data = f.read(4096)

with open('conversation_room2.bin', 'wb') as out:
    out.write(conversation_data)
```

Then run:
```bash
python simulate_conversation.py conversation_room2.bin
```

### Method 2: Use Existing Tools

If you have extraction tools:

```bash
# Extract conversation from Room 2
./extract_conversations.py ALFRED1 --room 2 > room2_conv.bin

# Simulate it
python simulate_conversation.py room2_conv.bin
```

## Example Session

```
============================================================
CONVERSATION START
============================================================

NPC_05:
  Te apetece pasar un buen rato, guapo ?

[Press Enter to continue...]

============================================================
CHOICES:
============================================================
  [1] No se, ¿ Cuanto cobras ?
  [2] No puedo. Estoy buscando a una princesa

Select choice (1-2): 1

ALFRED:
  No se, ¿ Cuanto cobras ?

[Press Enter to continue...]

NPC_05:
  Completo, 25000

[Press Enter to continue...]

ALFRED: (automatically)
  No me puedes hacer una tarifa especial ?. Estoy muy desesperado

[Press Enter to continue...]

============================================================
CONVERSATION ENDED
============================================================
```

## Testing Your Own Conversations

You can create test conversation data in hex format to understand the system:

```bash
# Simple conversation: NPC says "Hello", Alfred responds with 2 choices
python simulate_conversation.py --hex "
  08 05 48 65 6C 6C 6F FD
  FB 01 08 0D 48 69 FD
  FB 01 08 0D 42 79 65 FD
  F4
"

# Breakdown:
# 08 05       = Speaker ID (NPC 05)
# 48 65 ... = "Hello" in ASCII
# FD          = End text
# FB 01       = Choice marker, index 01
# 08 0D       = Speaker ID (ALFRED = 0x0D)
# 48 69       = "Hi"
# FD          = End text
# FB 01       = Choice marker, index 01 (same index = same choice group)
# 08 0D       = Speaker ID (ALFRED)
# 42 79 65    = "Bye"
# FD          = End text
# F4          = End conversation
```

## Control Bytes Reference

| Hex  | Meaning |
|------|---------|
| 0x08 | Speaker ID (followed by character ID byte) |
| 0xFB | Dialogue/choice marker (followed by choice index) |
| 0xF1 | Alternative dialogue marker (same as 0xFB) |
| 0xFD | End of text line |
| 0xF4 | End conversation completely |
| 0xFA | Disabled choice (already selected) |
| 0xF9 | Page break |
| 0xF8 | Action trigger (2 param bytes follow) |
| 0xF7 | End branch |
| 0xF6 | Line continuation |

## Spanish Characters

The simulator handles the game's custom character encoding:

| Hex  | Character |
|------|-----------|
| 0x80 | ñ |
| 0x81 | í |
| 0x82 | ¡ |
| 0x83 | ¿ |
| 0x84 | ú |
| 0x7B | á |
| 0x7C | é |
| 0x7D | í |
| 0x7E | ó |
| 0x7F | ú |

## Troubleshooting

**Problem**: "No more dialogue - conversation ended" immediately

**Solution**: The conversation data might not start at the correct offset. Try different starting positions or verify the data structure.

**Problem**: Garbled text

**Solution**: Check that you're using the correct character encoding. The game uses a custom Spanish character set above 0x7A.

**Problem**: Choices don't appear

**Solution**: Verify that your conversation data has proper 0xFB/0xF1 markers with choice indices that appear multiple times (real choices) vs. once (auto-dialogue).
