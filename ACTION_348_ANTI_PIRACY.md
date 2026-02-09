# Action 348 (0x015C) — Anti-Piracy Crash Handler

## Context
In Room 22's conversation tree with the first NPC, the player encounters a dialog branch about pirating the game. Selecting "Sí de acuerdo" (Yes, I agree [to pirate]) triggers **ACTION 015C** (decimal 348). This is an intentional anti-piracy punishment that corrupts the screen, makes noise, and crashes the game.

## Handler Location
- **Dispatch table entry**: Action ID `0x015C`, stored pointer `0x00011F3D`
- **Handler address**: `0x11F3D + 0x10000 = 0x21F3D` (Ghidra)
- **File offset**: `0x21F3D - 0x10000 + 0x14200 = 0x2613D` (in JUEGO.EXE)

**Note**: Ghidra does not recognize this as a function boundary — there is no named function here.

## Full Execution Flow

### Phase 1: Setup
```asm
0x21F3D: PUSH 0x14              ; param = 20
0x21F42: CALL 0x2A218           ; stack_check / get_current_room_number
0x21F47: PUSH EBX               ; save EBX
0x21F48: PUSH EDX               ; save EDX
0x21F49: MOV EAX, [0x4FAC8]     ; load pointer (room buffer base)
0x21F4E: MOV byte [EAX+5], 0x02 ; set flag byte to 2
0x21F52: XOR EBX, EBX           ; EBX = 0 (used as iterator later)
0x21F54: CALL 0x29037           ; init_or_stop_sound(0) — stops all sound
```

### Phase 2: Corruption Loop
```asm
LOOP_START:
0x21F59: PUSH 0x163             ; 355 — parameter for wait function
0x21F5E: CALL 0x2A258           ; wait_or_process_input(355)
0x21F63: ADD ESP, 4             ; clean stack

0x21F66: CALL 0x152B6           ; check_keyboard_input()
0x21F6B: TEST AL, AL            ; any key pressed?
0x21F6D: JNE CRASH_SECTION      ; if yes → crash immediately

; --- Visual corruption ---
0x21F6F: CALL 0x2B12F           ; random_number_generator() → EAX
0x21F74: MOV EDX, EAX           ; EDX = random value
0x21F76: AND EDX, 0xF           ; mask to 0-15
0x21F79: CALL 0x2B12F           ; random_number_generator() → EAX
0x21F7E: IMUL EAX, EDX          ; EAX = random1 * (random2 & 0xF)
0x21F81: MOV [0x4FADC], EAX     ; ★ CORRUPT background buffer pointer!

0x21F86: CALL 0x15DD4           ; copy_background_to_front_buffer()
                                 ;   → copies FROM corrupted address TO screen
0x21F8B: CALL 0x1625D           ; present_frame_to_screen()
                                 ;   → shows garbage on monitor

; --- Audio corruption ---
0x21F90: XOR EDX, EDX           ; DL = 0
0x21F92: MOV DL, [EBX]          ; DL = byte from sequential memory (addr 0,1,2...)
0x21F94: MOV EAX, 0x61          ; port 0x61 = PC speaker / PPI Port B
0x21F99: CALL 0x2B11B           ; outport_byte(0x61, garbage_byte)
                                 ;   → makes noise through PC speaker
0x21F9E: INC EBX                ; next memory byte
0x21F9F: JMP LOOP_START         ; repeat corruption loop
```

### Phase 3: Intentional Crash
```asm
CRASH_SECTION:
0x21FA1: XOR AH, AH            ; AH = 0
0x21FA3: MOV [0x1179E], AH      ; clear a game flag
0x21FA9: XOR EBX, EBX           ; EBX = 0 (divisor!)
0x21FAB: MOV EAX, 1             ; EAX = 1 (dividend)
0x21FB0: MOV EDX, EAX           ; EDX = 1
0x21FB2: SAR EDX, 31            ; EDX = 0 (sign extension for IDIV)
0x21FB5: IDIV EBX               ; ★ DIVIDE BY ZERO! → CPU exception → crash!

; --- Dead code (never reached) ---
0x21FB7: PUSH EAX
0x21FB8: PUSH 0x164             ; 356
0x21FBD: CALL 0x2A258           ; wait_or_process_input(356)
0x21FC2: ADD ESP, 8
0x21FC5: POP EDX
0x21FC6: POP EBX
0x21FC7: RET
```

## Mechanism Summary

| Phase | Effect | Technical Detail |
|-------|--------|-----------------|
| 1. Stop sound | Silence | `init_or_stop_sound(0)` |
| 2. Corrupt pointer | Screen garbage | Writes `random() * (random() & 0xF)` to `DAT_0004fadc` (background buffer pointer at 0x4FADC). Then `copy_background_to_front_buffer` reads from this garbage address → screen shows random memory contents |
| 3. Speaker noise | Buzzing/clicking | Writes sequential bytes from memory address 0+ to I/O port `0x61` (PC speaker), producing garbage noise |
| 4. Wait for keypress | Loop continues | Each frame: re-corrupts pointer, refreshes screen with new garbage, advances speaker noise |
| 5. Crash | Divide by zero | `IDIV EBX` with `EBX=0` → INT 0 (divide error) → DOS terminates the program |

## Key Addresses
- `0x4FADC` — Background buffer pointer (also used by `render_scene`, `calculate_screen_buffer_offset`). Corrupted to cause visual garbage.
- `0x4FAC8` — Room buffer base pointer. Byte at `[base+5]` set to 2 (possibly disables normal rendering).
- `0x1179E` — Game flag cleared just before crash.
- Port `0x61` — PC Programmable Peripheral Interface Port B (controls PC speaker).

## Dead Code
After the `IDIV EBX` crash, there are instructions that would call `wait_or_process_input(356)`. These never execute because the divide-by-zero terminates the program first. They may be:
- Leftover from development/testing (where the crash was disabled)
- Intentional misdirection for reverse engineers
- Compiler artifact from a removed code path

## Behavior in DOSBox
In DOSBox, the divide-by-zero exception causes the emulated DOS to terminate the program immediately, just as it would on real hardware. The screen corruption loop runs until any key is pressed, then the game crashes to the DOS prompt.

## ScummVM Implications
This action should **not** crash ScummVM. Instead, implement it as:
1. Stop sound
2. Show a brief visual glitch or message (optional, for authenticity)
3. Return to the main menu or display an error message
4. Alternatively, just skip the action entirely — the player can reload a save
