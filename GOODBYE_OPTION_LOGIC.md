# Goodbye Option Logic Analysis

## Overview

The conversation system has an optional "Adios. Estoy cansado de hablar contigo" (Goodbye. I'm tired of talking to you) line that can be added as an extra dialogue choice to end conversations. This line is located at **JUEGO.EXE offset 0x492EE**.

## Control Flag

**Global Flag Address:** `0x00049613` (in JUEGO.EXE memory space)

The logic for adding the goodbye option is controlled by a single byte flag at this address.

## Logic Flow

### In `handle_conversation_tree` function (0x00018690)

After collecting all dialogue choices for a conversation menu, the code checks whether to add the goodbye option:

**Check 1 - At 0x00018a6b:**
```assembly
00018a69: XOR EAX,EAX
00018a6b: MOV AL,[0x00049613]      ; Load goodbye flag
00018a70: TEST EAX,EAX             ; Test if zero
00018a72: JNZ 0x00018afd           ; If NOT zero, skip to "don't add goodbye"
```

**If flag == 0, continue to 0x00018a78 which evaluates choices:**
```assembly
00018a78: MOV BL,0x1               ; Assume we can add goodbye
00018a7a: XOR DL,DL
00018a7c: JMP 0x00018aba
...
; Loop through all choices checking if any end with 0xF8 or 0xF4
00018aa4: XOR EAX,EAX
00018aa6: MOV AL,byte ptr [ESI]
00018aa8: CMP EAX,0xf8             ; Check for 0xF8 (action trigger)
00018aad: JZ 0x00018ab6
00018aaf: CMP EAX,0xf4             ; Check for 0xF4 (end conversation)
00018ab4: JNZ 0x00018ab8
00018ab6: XOR BL,BL                ; If found F8 or F4, BL=0 (don't add goodbye)
...
00018ad6: TEST BL,BL               ; Check if BL still 1
00018ad8: JZ 0x00018afd            ; If BL=0, skip adding goodbye
```

**If BL still == 1, add goodbye option at 0x00018ada:**
```assembly
00018ada: XOR BH,BH
00018adc: MOV byte ptr [0x0005177f],BH   ; Clear flag
00018ae2: XOR EAX,EAX
00018ae4: MOV AL,DH                       ; DH = current choice count
00018ae6: MOV EBX,dword ptr [0x0004c084] ; Load goodbye text pointer
00018aec: MOV dword ptr [EAX*0x4 + 0x4f8a4],EBX  ; Add to choice array
00018af3: MOV byte ptr [0x00051694],DH   ; Store as "exit choice" index
00018af9: INC DH                          ; Increment choice count
00018afb: JMP 0x00018b04
```

**Second check - At 0x00018ba3:**
```assembly
00018ba1: XOR EAX,EDX
00018ba3: MOV AL,[0x00049613]      ; Load flag again
00018ba8: CMP EAX,0x1              ; Check if equals 1
00018bab: JNZ 0x00018d0e           ; If NOT 1, allow selected goodbye choice
```

## Decision Logic

The goodbye option is added **IF AND ONLY IF** all these conditions are met:

1. **`[0x49613] == 0`** - Global goodbye flag must be zero
2. **No choices end with 0xF8 or 0xF4** - None of the existing dialogue choices contain action triggers (0xF8) or conversation terminators (0xF4)

### Why the second condition?

The code checks each choice's ending marker:
- **0xF8 (Action Trigger):** Indicates the choice will trigger a game action and likely end the conversation naturally
- **0xF4 (End Conversation):** Explicitly ends the conversation tree

If any choice already provides a way to exit the conversation, the goodbye option is redundant and not added.

## Example Analysis

**Room 4, Second Conversation Root:**
- Flag `[0x49613]` = 0
- All choices end with 0xFD (simple text end) or 0xF7 (branch end), not 0xF8 or 0xF4
- **Result:** Goodbye option IS added

**Room with action-triggering choices:**
- Flag `[0x49613]` = 0
- One or more choices end with 0xF8 (e.g., "Pick up item")
- **Result:** Goodbye option NOT added (conversation will end after action)

## Flag Purpose

The flag at `0x49613` appears to be a **global disable switch** for the goodbye option:
- **Value 0:** Goodbye option enabled (but still subject to the 0xF8/0xF4 check)
- **Value 1+:** Goodbye option globally disabled for all conversations

Based on the analysis, the current value appears to be `0x20` (32 in decimal), which means the goodbye option is currently **globally disabled**.

## Related Data

- **Goodbye text:** "Adios. Estoy cansado de hablar contigo." at 0x492EE in JUEGO.EXE
- **Goodbye text pointer:** Stored at 0x0004c084 (memory address, referenced in code)
- **Choice array:** 0x0004f8a4 (array of pointers to dialogue choice text)
- **Exit choice index:** 0x00051694 (stores which choice is the "goodbye" exit)
- **Current choice count:** DH register during execution

## Control Byte Reference

| Byte | Name | Purpose |
|------|------|---------|
| 0xF4 | END_CONVERSATION | Terminates conversation completely |
| 0xF7 | END_BRANCH | Returns to previous menu level |
| 0xF8 | ACTION_TRIGGER | Executes game action (followed by 2 parameter bytes) |
| 0xFD | END_TEXT | Marks end of a dialogue line |

## Implementation Notes

For ScummVM reimplementation:
1. Store global goodbye flag (default: 0 to enable)
2. When building choice menu, check flag first
3. Scan all choices for ending bytes (0xF8 or 0xF4)
4. If flag==0 AND no action/end markers found, append goodbye option
5. Store goodbye choice index separately for special handling
6. When goodbye selected, exit conversation immediately
