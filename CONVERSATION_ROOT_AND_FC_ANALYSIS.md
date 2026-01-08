# Conversation Roots and FC Byte Analysis

## Executive Summary

This document explains how to identify conversation roots and the meaning of the FC byte in Alfred Pelrock's conversation system.

## 1. Identifying Conversation Roots

There are **two ways** conversation roots are marked in the data:

### Primary Root: FE [index]

```
FE [root_idx] FC [speaker] 08 [voice_high] [voice_lo] [voice_hi] [text...] FD
```

- `FE` = Primary conversation root marker
- `root_idx` = Root index (1, 2, etc.) used for state tracking
- `FC` = Speaker change marker
- The rest follows the standard speaker line format

**Example (Room 2):**
```
FE 01 FC 41 08 20 0A 00 83 20 54 65 ...
                           "¿ Te apecete pasar un buen rato, guapo ?"
```

### Secondary Root: F7 FC

```
F7 FC [speaker] 08 [voice_high] [voice_lo] [voice_hi] [text...] FD
```

- `F7` = End of branch marker
- `FC` = Speaker change marker (immediately after F7 signals new root)
- When F7 is immediately followed by FC, it marks an **alternative conversation root**

**Example (Room 2):**
```
F7 FC 41 08 20 2B 00 83 20 48 61 73 ...
                        "¿ Has conseguido los condones ?"
```

### Root Discovery Algorithm

```cpp
// Scan for conversation roots
while (pos < dataSize) {
    byte b = data[pos];
    
    // Primary root: FE [index]
    if (b == 0xFE) {
        int rootIndex = data[pos + 1];
        // This is root #rootIndex
        // State for this root stored at conversation_branch_state_array[room * 4 + slot]
        pos += 2;
        continue;
    }
    
    // Secondary root: F7 FC
    if (b == 0xF7 && pos + 1 < dataSize && data[pos + 1] == 0xFC) {
        // This is an alternative root (F7 ends previous branch, FC starts new root)
        pos += 1; // Move past F7, next iteration will process FC
        continue;
    }
    
    pos++;
}
```

## 2. The FC Byte Explained

The FC byte marks a **speaker change** to an NPC. It does NOT mean "Alfred speaking".

### FC Structure

```
FC [speaker_id] 08 [voice_high] [voice_lo] [voice_hi] [text...]
```

| Byte | Meaning |
|------|---------|
| FC | Speaker change marker |
| speaker_id | NPC identifier (usually 0x41 = 'A' for first NPC) |
| 08 | Speaker marker (constant) |
| voice_high | High byte of voice file ID |
| voice_lo | Low byte of voice file ID |
| voice_hi | (second part of voice ID) |

### FC 41 Meaning

`FC 41` means "NPC speaker 0x41" - the first NPC in the room. In Room 2, this is the prostitute.

The 0x41 is ASCII 'A' - simply the first speaker identifier. In rooms with multiple NPCs, you might see:
- `FC 41` = First NPC
- Different separators for different NPCs (see Room 22 with 0xC7 and 0xD7)

### The Separator Byte (After 08)

The byte after `08` is NOT a speaker indicator - it's the **high byte of the voice file ID**.

| Room | FC Pattern | Voice File High Byte |
|------|-----------|---------------------|
| Room 2 | FC 41 08 **20** | 0x20xx |
| Room 4 | FC 41 08 **05** | 0x05xx |
| Room 14 | FC 41 08 **19** | 0x19xx |
| Room 22 (NPC1) | FC 41 08 **D7** | 0xD7xx |
| Room 22 (NPC2) | FC 41 08 **C7** | 0xC7xx |

This explains why Room 22 has two different separator values - it has two different NPCs with different voice file ranges!

## 3. Speaker Identification (Alfred vs NPC)

The speaker is determined by the marker that precedes the line, NOT the FC byte:

### NPC Speaking (FC marker)

```
FC [speaker_id] 08 [voice_high] [voice_lo] [voice_hi] [text...] FD
```

### Alfred Speaking (FB/F1 marker)

```
FB [choice_idx] 08 0D [voice_lo] [voice_hi] [text...] FD
F1 [choice_idx] 08 0D [voice_lo] [voice_hi] [text...] FD
```

Key differences:
- **FC** = NPC speaking, followed by speaker_id
- **FB** = Alfred's one-time choice, followed by choice_idx
- **F1** = Alfred's repeatable choice, followed by choice_idx

For Alfred, the voice high byte is always **0x0D** (indicating Alfred's voice files).

## 4. State Tracking for Roots

Each FE-marked root has a corresponding slot in `conversation_branch_state_array`:

```cpp
// Address: 0x0004fba4
// Size: 224 bytes (56 rooms × 4 slots per room)
byte conversation_branch_state_array[224];

// Access pattern
int slot = room_number * 4 + root_slot;
if (conversation_branch_state_array[slot] != 0) {
    // This root is disabled, skip to next
}
```

### What Needs Saving

For save games, you need to track:
1. `conversation_branch_state_array[224]` - which roots are disabled
2. The FA markers written to FB positions (at FB+2, overwriting 0x08)

## 5. Text Positioning in Original Game

From Ghidra analysis of `display_talk_animation_and_wait`:

```cpp
// Text positioning for dialogue
if (alfred_facing_direction < 2) {
    uVar3 = 0x800;  // Frame count for animation
} else {
    uVar3 = 0x400;
}

// X position calculation (centered on Alfred)
render_queue_x = alfred_x_position - (mouse_cursor_width / 2);
// Clamp to screen bounds: 0 to 0x27f (639) - width

// Y position calculation (above Alfred's head)
render_queue_y = alfred_y_position - ((0x66 - alfred_scale_y) + mouse_cursor_height);
// 0x66 (102) is Alfred's base height before scaling
// If too high (< 60), clamp to y=1
```

### Text Display Constants

- Maximum line width: **47 characters** (0x2F)
- Maximum lines per screen: **4-5 lines**
- Text centering: Lines shorter than 46 chars are centered by adding leading spaces

## 6. ScummVM Implementation Notes

### Root Detection

```cpp
struct ConversationRoot {
    int index;           // FE root index (or -1 for F7 FC roots)
    uint32 dataOffset;   // Position in conversation data
    bool isDisabled;     // From state array
};

Common::Array<ConversationRoot> findRoots(const byte *data, uint32 size) {
    Common::Array<ConversationRoot> roots;
    
    for (uint32 pos = 0; pos < size - 1; pos++) {
        if (data[pos] == 0xFE) {
            ConversationRoot root;
            root.index = data[pos + 1];
            root.dataOffset = pos;
            root.isDisabled = false; // Check state array
            roots.push_back(root);
        }
        else if (data[pos] == 0xF7 && data[pos + 1] == 0xFC) {
            ConversationRoot root;
            root.index = -1; // F7 FC roots don't have numbered indices
            root.dataOffset = pos + 1; // Point to FC
            root.isDisabled = false;
            roots.push_back(root);
        }
    }
    
    return roots;
}
```

### Speaker Detection

```cpp
bool isAlfredSpeaking(byte marker) {
    return (marker == 0xFB || marker == 0xF1);
}

bool isNPCSpeaking(byte marker) {
    return (marker == 0xFC);
}
```

### Text Positioning

```cpp
void positionDialogue(int speakerId, int &xPos, int &yPos, int textWidth, int textHeight) {
    if (speakerId == ALFRED_SPEAKER_ID) {
        // Position above Alfred
        xPos = alfredState.x - textWidth / 2;
        yPos = alfredState.y - kAlfredFrameHeight - textHeight;
    } else {
        // Position above NPC sprite
        xPos = curSprite->x + curSprite->w / 2 - textWidth / 2;
        yPos = curSprite->y - textHeight;
    }
    
    // Clamp to screen bounds
    xPos = CLIP(xPos, 0, 640 - textWidth);
    yPos = CLIP(yPos, 0, 400 - textHeight);
}
```

## Summary

| Pattern | Meaning |
|---------|---------|
| `FE [idx]` | Primary conversation root #idx |
| `F7 FC` | Secondary/alternative conversation root |
| `FC [id] 08 [vh] [vl] [vh2]` | NPC speaking |
| `FB [idx] 08 0D [vl] [vh]` | Alfred one-time choice |
| `F1 [idx] 08 0D [vl] [vh]` | Alfred repeatable choice |
| `F7` alone | End of current branch (return to parent) |
| `F4` | End of entire conversation |

The FC byte is NOT a speaker indicator - it's a marker for NPC lines. The byte that appears after FC (like 0x41) is the NPC identifier, and the bytes after 08 form the voice file ID.
