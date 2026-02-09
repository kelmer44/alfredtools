# F8 Action Code Tracing Guide

## Purpose
This document explains how to reverse-engineer what a specific "F8 action code" does in Alfred Pelrock's `JUEGO.EXE`. These action codes appear in conversation trees and room handler scripts as numeric IDs (e.g., ACTION 0x015E = 350 decimal) and trigger game logic via a dispatch table.

**Audience**: AI agents and humans reverse-engineering the game.

---

## Overview of the F8 Dispatch System

The game uses a centralized dispatch mechanism for "special actions" triggered during gameplay. These are called **F8 actions** because they go through the `process_f8_dispatch` function. Each action has a 16-bit ID (e.g., 0x015C = 348) and a corresponding handler function in the executable.

### Where Action Codes Appear

1. **Conversation trees** (in room text data, ALFRED.1 Pair 12): Encoded as `ACTION XXXX` where XXXX is a hex value. The conversation system calls `process_f8_dispatch(action_id)` when a dialog option with an action code is selected.
2. **Room handler scripts**: Room-specific logic tables that fire actions on events.
3. **Item use handlers**: When using inventory items on hotspots.

---

## The Dispatch Table

### Location
- **Ghidra address**: `0x47E58`
- **File offset in JUEGO.EXE**: `0x47E58 - 0x10000 + 0x14200 = 0x4C058`

### Format
The table consists of **116 entries**, each **6 bytes**:

| Offset | Size | Description |
|--------|------|-------------|
| +0 | 2 bytes | Action ID (uint16 LE) |
| +2 | 4 bytes | Handler pointer (uint32 LE, needs +0x10000 fixup) |

The table is terminated when the dispatcher doesn't find a matching action ID.

### Entry Example
```
Bytes: 5C 01 F3 1F 01 00
       ^^^^              Action ID = 0x015C (348 decimal)
             ^^^^^^^^^^  Stored pointer = 0x00011FF3
```

### Address Fixup Formula
The stored pointer needs a fixup to get the actual runtime/Ghidra address:
```
ghidra_address = stored_pointer + 0x10000
```
Example: `0x00011FF3 + 0x10000 = 0x00021FF3` → handler is at Ghidra address `0x21FF3`

### Converting Ghidra Address to File Offset
To find the handler bytes in the raw `JUEGO.EXE` file:
```
file_offset = ghidra_address - 0x10000 + 0x14200
```
Example: `0x21FF3 - 0x10000 + 0x14200 = 0x261F3`

---

## Step-by-Step Tracing Process

### Step 1: Identify the Action Code
Find the action code in context. For conversation trees, look for lines like:
```
ACTION 015E    → action ID = 0x015E (350 decimal)
```

### Step 2: Find the Dispatch Table Entry
**Method A: Read from the EXE file**
```python
import struct

TABLE_OFFSET = 0x4C058   # File offset of dispatch table in JUEGO.EXE
ENTRY_SIZE = 6
NUM_ENTRIES = 116

with open("files/JUEGO.EXE", "rb") as f:
    for i in range(NUM_ENTRIES):
        f.seek(TABLE_OFFSET + i * ENTRY_SIZE)
        data = f.read(ENTRY_SIZE)
        action_id = struct.unpack_from('<H', data, 0)[0]
        stored_ptr = struct.unpack_from('<I', data, 2)[0]
        if action_id == 0x015E:  # target action
            ghidra_addr = stored_ptr + 0x10000
            print(f"Action 0x{action_id:04X}: handler at Ghidra 0x{ghidra_addr:05X}")
            break
```

**Method B: Use Ghidra MCP**
1. Read memory at `0x47E58` and scan entries
2. Or decompile `process_f8_dispatch` and look at the table it references

### Step 3: Decompile the Handler
Use Ghidra to decompile the handler function at the address found in Step 2:
```
mcp_ghidra_decompile_function_by_address(address="0x21FFB")
```

If the handler is not recognized as a function (no function boundary), also try:
```
mcp_ghidra_disassemble_function(address="0x21FFB")
```

### Step 4: Identify Called Functions
Handlers typically call well-known engine functions. Common ones:

| Function | Ghidra Address | Purpose |
|----------|---------------|---------|
| `wait_or_process_input` | 0x2A258 | Yield/process events; sometimes takes an action ID parameter to chain to another F8 action |
| `update_conversation_state` | 0x2BA42 | Advances conversation tree state (params: room, npc_id, branch) |
| `init_or_stop_sound` | 0x29037 | Start/stop sound playback |
| `check_keyboard_input` | 0x152B6 | Poll keyboard state |
| `random_number_generator` | 0x2B12F | Returns random value |
| `outport_byte` | 0x2B11B | Write to hardware I/O port |
| `copy_background_to_front_buffer` | 0x15DD4 | Copy background layer to visible buffer |
| `present_frame_to_screen` | 0x1625D | Push frame buffer to display |
| `render_scene` | (varies) | Full scene re-render |
| `set_game_flag` / `clear_game_flag` | (varies) | Manipulate game state flags |

### Step 5: Understand the Handler Logic
Most handlers follow common patterns:

#### Pattern: Conversation Gate Flag
```c
// XOR a bit in a flag byte, used to track if player has seen required dialog branches
flag_byte ^= bit_value;  // e.g., XOR with 0x01 or 0x02
if (flag_byte == target_value) {
    update_conversation_state(room, npc, branch);
}
```
Example: Actions 349 and 350 both XOR bits of `[0x495F0]`. When both are triggered (flag = 3), the conversation advances.

#### Pattern: Chain to Another Action
```c
wait_or_process_input(next_action_id);
```
The handler does some work, then chains to another action ID via `wait_or_process_input`.

#### Pattern: Set Flag and Return
```c
game_state[offset] = value;
```
Simple flag set/clear to track game progress.

#### Pattern: Visual Effect + Chain
```c
// Loop with visual effects
do {
    modify_screen_or_palette();
    present_frame_to_screen();
} while (condition);
wait_or_process_input(next_action);
```

---

## Dispatch Function Internals

The `process_f8_dispatch` function works as follows:

1. Receives an action ID (16-bit) as parameter
2. Scans the dispatch table at `0x47E58` linearly
3. For each entry, compares the 2-byte action ID
4. On match: adds `0x10000` to the stored 4-byte pointer to get the handler address
5. Jumps to (calls) the handler
6. If no match found: returns without action

### Key Insight: Pointer Fixup
The game's executable is loaded at segment offset `0x10000` in memory. All pointers stored in the dispatch table are relative to the start of the executable image, so `+0x10000` converts them to runtime addresses. In Ghidra (which uses the runtime address space), the handler addresses directly match after this fixup.

---

## Quick Reference

### Address Conversion Cheat Sheet
| From | To | Formula |
|------|----|---------|
| Dispatch table stored ptr | Ghidra/runtime address | `+ 0x10000` |
| Ghidra/runtime address | EXE file offset | `- 0x10000 + 0x14200` |
| EXE file offset | Ghidra/runtime address | `- 0x14200 + 0x10000` |

### Dispatch Table Quick Stats
- **Start**: Ghidra `0x47E58` / File `0x4C058`
- **Entries**: 116
- **Entry size**: 6 bytes (2 ID + 4 pointer)
- **Total size**: 696 bytes (0x2B8)
- **End**: Ghidra `0x48110` / File `0x4C310`

### Common Action ID Ranges
- 0x0100–0x01FF: Conversation-related actions
- Actions are NOT sequential — gaps exist
- Each action ID appears exactly once in the table

---

## Example Walkthrough: Tracing Action 350 (0x015E)

1. **Source**: Found in Room 22 conversation tree: `ACTION 015E`
2. **Table lookup**: Entry at dispatch table has stored ptr `0x00011FFB`
3. **Fixup**: `0x11FFB + 0x10000 = 0x21FFB`
4. **Decompile** `0x21FFB` in Ghidra → handler code
5. **Analysis**: Handler XORs bit 1 (value 2) of flag byte at `[0x495F0]`, then checks if flag == 3. If so, calls `update_conversation_state(room=22, npc=1, branch=1)` to advance dialog.
6. **Context**: Action 349 (0x015D) XORs bit 0 (value 1) of the same flag. Player must trigger BOTH to advance the conversation tree.

---

## Tips for AI Agents

1. **Always use Ghidra as source of truth** — project documentation may be outdated or incomplete.
2. **Check function boundaries**: If `decompile_function_by_address` returns garbled results, the address may be mid-function. Try `get_function_by_address` first to find the function start.
3. **Resolve called functions**: Use `get_function_by_address` on any CALL target to identify known engine functions.
4. **Watch for register-based parameters**: The game uses Watcom calling convention — parameters in EAX, EDX, EBX, ECX, then stack. Ghidra may not always recognize these correctly.
5. **Chain actions**: If a handler calls `wait_or_process_input(action_id)`, trace that action too — it's part of the same logical sequence.
6. **Flag bytes**: Game state flags are stored in the data segment (addresses like `0x495xx`). Multiple actions may read/write the same flag byte — search for xrefs.
