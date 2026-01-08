# Conversation Root Identification and Disable Mechanism

**Verified against Ghidra decompilation of JUEGO.EXE**

## Summary

The conversation root disable mechanism works as follows:

1. **Roots are identified by their sequential position** in the text data (0th FE, 1st FE, etc.), NOT by the index byte after FE
2. **State is stored** in `conversation_branch_state_array[room * 4 + slot]` where `slot` is 0-3
3. **F8 0x0148** is the action that marks the current conversation root as disabled
4. **On room load**, disabled roots are skipped to their alternate branch

---

## Key Data Structures

### Conversation Branch State Array

```
Address: 0x0004fba4
Size: 224 bytes (56 rooms × 4 slots)
Layout: state_array[room_id * 4 + slot_index]

Values:
  0 = original state (show primary branch)
  N = skip to Nth F7 marker (show alternate branch)
```

### Text Pointer Table

```
Address: room_sprite_data_ptr + 0x3DA
Layout: Array of 4-byte pointers
Index calculation: (sprite_count - 2) + hotspot_count + queued_sprite_talk_count
```

---

## How F8 0x0148 Handler Works

### Simplified Call Chain

```
1. handle_conversation_tree() or handle_dialog_interaction()
   - Parses text data
   - Encounters F8 marker
   
2. Dispatches via F8_ACTION_TABLE at 0x00047e58
   - Looks up action ID 0x0148
   - Calls associated function pointer
   
3. F8 0x0148 handler (at addresses 0x22825, 0x22caf area)
   - Gets current conversation root slot from engine context
   - Calls update_conversation_state(slot, 1)

4. update_conversation_state()
   - Writes to state_array[room * 4 + slot]
   - If in current room, updates text pointer table
```

### Register Passing

Based on Ghidra's decompilation of `update_conversation_state`:
- `DL` register = slot index (0-3)
- `BL` register = state value to store (typically 1 = "disabled")

---

## How Root Index Is Determined

### Key Insight: Two Different Indices

There are **TWO DIFFERENT indices** in the conversation system:

1. **Text Pointer Index** (used to START a conversation):
   - Calculated as: `(sprite_count - 2) + hotspot_count + queued_sprite_talk_count`
   - Determines which entry in the text pointer table to use
   - This maps NPC sprites to their conversation data

2. **FE Slot Index** (used for STATE tracking):
   - Sequential counter of FE markers in the text data
   - Room 2 has one FE marker → slot 0
   - Room 22 might have FE 01, FE 02, FE 03 → slots 0, 1, 2
   - The `FE [index_byte]` is metadata, NOT the slot!

### How the F8 0x0148 Handler Knows Which Slot

The F8 handler doesn't receive the slot as a parameter. Instead:

1. The conversation engine maintains global state tracking which FE root is "active"
2. When F8 0x0148 is triggered, it uses the **currently active FE slot**
3. The FE slot counter starts at 0 and increments for each FE marker encountered

Looking at `update_conversation_state` decompilation:
- `DL` register = FE slot index (0-3)
- `BL` register = state value (typically 1)

The F8 handler at ~0x22825 must set these registers from global conversation state.

### At Room Load

In `load_room_and_init_alfred`:
```c
slot_counter = 0;
while (text_scanner < end) {
    if (*text_scanner == 0xFE) {
        text_scanner += 2;  // Skip FE and index byte
        
        if (state_array[room * 4 + slot_counter] != 0) {
            // Skip forward counting F7 markers
            branch_count = 0;
            while (branch_count != state_value) {
                if (*text_scanner == 0xF7) branch_count++;
                text_scanner++;
            }
        }
        
        // Store pointer for this text index
        text_pointer_table[ptr_index++] = text_scanner;
        slot_counter++;
    }
    ...
}
```

---

## ScummVM Implementation Guidelines

### 1. State Storage

Create a state array:
```cpp
uint8 _conversationState[56][4];  // 56 rooms, 4 slots each

// Access:
uint8 getConversationState(uint8 room, uint8 slot) {
    return _conversationState[room][slot];
}

void setConversationState(uint8 room, uint8 slot, uint8 value) {
    _conversationState[room][slot] = value;
}
```

### 2. During Conversation Parsing

Track the current slot:
```cpp
void PelrockEngine::parseConversation(uint8 *textData) {
    uint8 currentSlot = 0;
    
    while (*textData != 0xF5) {  // End of conversation
        switch (*textData) {
            case 0xFE:  // Root marker
                textData += 2;  // Skip FE and index
                _currentConversationSlot = currentSlot;
                currentSlot++;
                break;
                
            case 0xF8:  // Action trigger
                uint16 actionId = READ_LE_UINT16(textData + 1);
                if (actionId == 0x0148) {
                    // Disable current root
                    setConversationState(_currentRoom, _currentConversationSlot, 1);
                    updateTextPointers();  // If still in same room
                }
                textData += 3;
                break;
                
            // ... other cases
        }
    }
}
```

### 3. At Room Load

Apply state when building text pointer table:
```cpp
void PelrockEngine::buildTextPointerTable(uint8 *textData) {
    uint8 slotCounter = 0;
    uint8 ptrIndex = 0;
    
    while (*textData != 0xF5) {
        if (*textData == 0xFE) {
            textData += 2;  // Skip FE and index byte
            
            uint8 stateValue = getConversationState(_currentRoom, slotCounter);
            if (stateValue != 0) {
                // Skip forward to Nth F7 marker
                int branchCount = 0;
                while (branchCount < stateValue) {
                    if (*textData == 0xF7) branchCount++;
                    textData++;
                }
            }
            
            _textPointerTable[ptrIndex++] = textData;
            slotCounter++;
        }
        else if (*textData == 0xFF) {
            textData += 2;  // Skip FF and index
            _textPointerTable[ptrIndex++] = textData;
        }
        // ...
    }
}
```

### 4. Save/Load

Include in save game:
```cpp
void PelrockEngine::saveState(Common::WriteStream *stream) {
    for (int room = 0; room < 56; room++) {
        for (int slot = 0; slot < 4; slot++) {
            stream->writeByte(_conversationState[room][slot]);
        }
    }
}

void PelrockEngine::loadState(Common::ReadStream *stream) {
    for (int room = 0; room < 56; room++) {
        for (int slot = 0; slot < 4; slot++) {
            _conversationState[room][slot] = stream->readByte();
        }
    }
    // Rebuild text pointer table for current room
    buildTextPointerTable(getCurrentRoomTextData());
}
```

---

## F7 FC Secondary Roots

Some conversations have secondary entry points marked by `F7 FC`:
- F7 = end of branch marker
- FC = NPC speaker marker

The sequence `F7 FC` creates an alternate entry point that the state mechanism can skip to.

When `state_array[room * 4 + slot] = 1`:
- Parser skips past 1 F7 marker
- Lands at the F7 FC secondary root
- This becomes the new conversation starting point

---

## Example: Room 2 Conversation

```
FE 01 ...primary root text (prostitute negotiation)...
    ...nested FB choices...
        ...F8 48 01 (disable root when reaching conclusion)...
F7 FC 41 ...secondary root text (Have you got condoms?)...
    ...F1 repeatable choices...
F5 (end)
```

After F8 0x0148 triggers:
- `state_array[2 * 4 + 0] = 1` (room 2, slot 0)
- Next time room loads, text pointer skips to F7 FC secondary root
- Player only sees "Have you got condoms?" conversation
