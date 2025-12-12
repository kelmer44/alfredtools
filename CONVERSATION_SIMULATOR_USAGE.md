# Conversation Simulator - Usage Examples

## Basic Usage

The conversation simulator lets you interactively experience conversations as they appear in the game. It now automatically extracts conversation data from ALFRED.1 files.

### From ALFRED.1 File (Recommended)

```bash
# Simulate a conversation from a specific room
python simulate_conversation.py ALFRED.1 2

# Where:
#   ALFRED.1 = resource file
#   2 = room number
```

The simulator will:
1. Read the ALFRED.1 file
2. Extract resource pair 12 (conversations) for the specified room
3. Calculate sprite and hotspot counts from pair 10
4. Skip past sprite/hotspot descriptions
5. Start the conversation simulation

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

The simulator now automatically handles this! Just provide the ALFRED.1 file and room number.

### How Conversations Are Located

Conversations are stored in **resource pair 12** of each room. The structure is:

```
Pair 12 Structure:
├─ Sprite/Hotspot Descriptions (variable count)
│  ├─ Each: 0xFF + 4 bytes + text + 0xFD
│  └─ Count = sprite_count + hotspot_count (from pair 10)
│
└─ Conversation Data (starts after descriptions)
   ├─ Speaker markers (0x08)
   ├─ Dialogue markers (0xFB/0xF1)
   ├─ Text content
   └─ Control bytes
```

### Extraction Process

The simulator:
1. Reads pair 12 from ALFRED.1 for the specified room
2. Reads pair 10 to get sprite_count (offset 0x05 - 2)
3. Reads pair 10 to get hotspot_count (offset 0x47A)
4. Skips `sprite_count + hotspot_count` descriptions
5. Conversation data starts immediately after

### Manual Extraction (Optional)

If you want to extract conversation data manually:

```python
# Example: Extract Room 2 conversation data
import struct

def read_room_pair(data, room_num, pair_num):
    room_offset = room_num * 104
    pair_offset_pos = room_offset + (pair_num * 8)
    offset = struct.unpack('<I', data[pair_offset_pos:pair_offset_pos+4])[0]
    size = struct.unpack('<I', data[pair_offset_pos+4:pair_offset_pos+8])[0]
    return data[offset:offset+size]

with open('ALFRED.1', 'rb') as f:
    alfred1_data = f.read()

pair12 = read_room_pair(alfred1_data, 2, 12)  # Room 2, pair 12
pair10 = read_room_pair(alfred1_data, 2, 10)  # For counts

sprite_count = pair10[5] - 2
hotspot_count = pair10[0x47A]
description_count = sprite_count + hotspot_count

# Skip descriptions to find conversation start
# (See simulator source code for full implementation)
```

## Example Session```
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
