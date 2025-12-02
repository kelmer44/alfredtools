# room_script_dispatch_table Analysis

## Table Location
- **Virtual Address**: `0x484e4` (referenced by `0x15aca`)
- **File Offset**: `0x4B6E4`
- **Entry Format**: 6 bytes each - `[u16 room_number][u32 function_ptr]`
- **End Marker**: `0xFFFF`

## How It Works
The dispatch loop at `0x15aac-0x15aeb` in `load_room_data`:

1. Iterates through the table at `0x484e4`
2. Compares each `room_number` with `current_room_number` at `[0x4fb94]`
3. When match found, calls the function pointer via `CALL dword ptr [EDX + 0x484e6]`
4. After call returns, exits the loop

## Important: All Handlers are EMBEDDED

All function pointers point to addresses within `load_room_data` (0x152f5-0x15c90).
These are NOT separate functions - they're mid-function entry points.

The handlers are meant to be called and then RET back to the dispatch loop at `0x15ae7`.

## Room Handler Table

| Room | Handler Addr | Offset in func | Shared With | Purpose |
|------|--------------|----------------|-------------|---------|
| 0 | 0x1561F | +0x032A | Room 4 | Unknown - falls through to general init |
| 3 | 0x15889 | +0x0594 | - | JMP 0x15909 (skip scaling setup) |
| 4 | 0x1561F | +0x032A | Room 0 | Same as room 0 |
| 7 | 0x1587A | +0x0585 | - | Skip scaling, set scaling flags to 0 |
| 9 | 0x158BD | +0x05C8 | (duplicate entry) | Scaling calculation |
| 12 | 0x15C49 | +0x0954 | - | Near end of function |
| 13 | 0x15C68 | +0x0973 | (also has 0x15BEC) | Near end of function |
| 28 | 0x158E1 | +0x05EC | - | Scaling setup |
| 30 | 0x15959 | +0x0664 | - | Standard sprite pointer setup |
| 36 | 0x1592B | +0x0636 | - | Before sprite setup |
| 48 | 0x15994 | +0x069F | - | Room 55/0x37 special sprite offsets |
| 51-54 | 0x159E9 | +0x06F4 | All share | Same handler for rooms 51,52,53,54 |
| 5 | 0x15A3D | +0x0748 | - | Player sprite setup |
| 19 | 0x15A68 | +0x0773 | (also has 0x15BEC) | Near dispatch loop |
| 9 | 0x15A7F | +0x078A | (second entry!) | Compare current_room with dispatch |
| 24 | 0x15A96 | +0x07A1 | - | After secondary dispatch |
| 38 | 0x15AAD | +0x07B8 | - | Pre-render setup |
| 41 | 0x15AF0 | +0x07FB | - | Post-dispatch |
| 32 | 0x15B07 | +0x0812 | - | Render setup |
| 27 | 0x15B5B | +0x0866 | - | Palette/render call |
| 39,40 | 0x15BA5 | +0x08B0 | Shared | Same handler |
| 26 | 0x15BB7 | +0x08C2 | - | Late init |
| 2 | 0x15C22 | +0x092D | - | Special mode for room 0x1C |
| 17 | 0x15BEC | +0x08F7 | Rooms 13,19 | Shared handler |
| 13 | 0x15BEC | +0x08F7 | Rooms 17,19 | (duplicate) |
| 19 | 0x15BEC | +0x08F7 | Rooms 13,17 | (duplicate) |

## Handler Code Analysis

### Room 0/4 Handler (0x1561F)
At this address, code falls through from room 3 special case handling. This is after the text/conversation script parsing section.

### Room 3 Handler (0x15889)
```asm
00015889: JMP 0x00015909  ; Skip scaling calculation, jump to sprite setup
```
Simply skips the scaling calculation and goes directly to sprite initialization.

### Room 7 Handler (0x1587A)
```asm
0001587a: XOR DH,DH
0001587d: MOV byte ptr [0x0004967e],DH  ; scale_min = 0
00015883: MOV byte ptr [0x0004967f],DH  ; scale_max = 0
00015889: JMP 0x00015909                 ; Continue to sprite setup
```
Sets both scaling variables to 0 (no scaling in this room).

### Room 30 Handler (0x15959) - Standard Sprite Setup
```asm
00015959: MOV EAX,[0x0004fa94]           ; Get base graphics pointer
0001595d: MOV [0x0004f7b4],EAX           ; sprite_ptr_1 = base
00015962: LEA EDX,[EAX + 0xb6e2]         ; sprite_ptr_2 = base + 0xb6e2
...
```
Sets up 4 sprite pointers with fixed offsets from base graphics memory.

### Rooms 51-54 Handler (0x159E9)
```asm
000159e9: MOV DX,word ptr [0x0004fb96]
000159ef: MOV word ptr [EAX*0x2 + 0x4f928],DX
...
```
Sets up sprite position data, shared by all 4 rooms.

### Room 48/55 Handler (0x15994)
This is the special case for room 55 (0x37) which uses DIFFERENT sprite offsets:
- Uses offset `0x4c339` instead of `0x0`
- Uses offset `0x5be97` instead of `0xb6e2`
Different walking animation set for this room.

## Secondary Dispatch Table

There's ANOTHER table at `0x486a4` with similar structure, checked at `0x15a55-0x15a9e`.
This stores a function pointer into `[0x4f8ec]` when room matches - used for room-specific callbacks that persist.

## Rooms WITHOUT Custom Handlers

These rooms use only the default initialization path:
- 1, 6, 8, 10, 11, 14, 15, 16, 18, 20, 21, 22, 23, 25, 29, 31, 33, 34, 35, 37, 42-47, 49, 50, 55+

## Key Variables

| Address | Name | Purpose |
|---------|------|---------|
| 0x4fb94 | current_room_number | Current room ID (u16) |
| 0x4967e | scale_min | Minimum sprite scaling factor |
| 0x4967f | scale_max | Maximum sprite scaling factor |
| 0x4f7b4-0x4f7c0 | sprite_ptr_array | 4 pointers to sprite graphics |
| 0x4fa94 | graphics_base | Base pointer to loaded graphics |
| 0x4f8ea | has_room_callback | Boolean flag |
| 0x4f8ec | room_callback_ptr | Function pointer for room-specific callback |
