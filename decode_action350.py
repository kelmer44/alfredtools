#!/usr/bin/env python3
"""
Decode action 350 (0x015E) handler at 0x21FFB from JUEGO.EXE.
Also decode the JMP targets at 0x222E3 and 0x222E8 and 0x1D66A.
"""
import struct

def code_to_file(addr):
    return addr - 0x10000 + 0x14200

def decode_block(exe_data, addr, length, label=""):
    print(f"\n{'='*70}")
    print(f"{label} at 0x{addr:05X}")
    print(f"{'='*70}")

    file_off = code_to_file(addr)
    block = exe_data[file_off:file_off + length]

    # Hex dump
    for i in range(0, length, 16):
        a = addr + i
        hexbytes = ' '.join(f'{b:02x}' for b in block[i:i+16])
        print(f"  0x{a:05X}: {hexbytes}")

    # Simple instruction decode
    print(f"\n  Decoded instructions:")
    i = 0
    while i < length:
        a = addr + i
        b = block[i]

        if b == 0x68 and i + 4 < length:  # PUSH imm32
            imm = struct.unpack_from('<I', block, i+1)[0]
            print(f"    0x{a:05X}: PUSH 0x{imm:X}")
            i += 5
        elif b == 0xe8 and i + 4 < length:  # CALL rel32
            disp = struct.unpack_from('<i', block, i+1)[0]
            target = a + 5 + disp
            print(f"    0x{a:05X}: CALL 0x{target:05X}")
            i += 5
        elif b == 0xe9 and i + 4 < length:  # JMP rel32
            disp = struct.unpack_from('<i', block, i+1)[0]
            target = a + 5 + disp
            print(f"    0x{a:05X}: JMP  0x{target:05X}")
            i += 5
        elif b == 0x53:
            print(f"    0x{a:05X}: PUSH EBX")
            i += 1
        elif b == 0x52:
            print(f"    0x{a:05X}: PUSH EDX")
            i += 1
        elif b == 0x5a:
            print(f"    0x{a:05X}: POP  EDX")
            i += 1
        elif b == 0x5b:
            print(f"    0x{a:05X}: POP  EBX")
            i += 1
        elif b == 0xc3:
            print(f"    0x{a:05X}: RET")
            i += 1
        elif b == 0x31 and i+1 < length and block[i+1] == 0xc0:
            print(f"    0x{a:05X}: XOR  EAX, EAX")
            i += 2
        elif b == 0x89 and i+1 < length and block[i+1] == 0xda:
            print(f"    0x{a:05X}: MOV  EDX, EBX")
            i += 2
        elif b == 0xa0 and i+4 < length:  # MOV AL, [imm32]
            addr_val = struct.unpack_from('<I', block, i+1)[0]
            print(f"    0x{a:05X}: MOV  AL, [0x{addr_val:05X}]")
            i += 5
        elif b == 0xb8 and i+4 < length:  # MOV EAX, imm32
            imm = struct.unpack_from('<I', block, i+1)[0]
            print(f"    0x{a:05X}: MOV  EAX, 0x{imm:X} ({imm})")
            i += 5
        elif b == 0xbb and i+4 < length:  # MOV EBX, imm32
            imm = struct.unpack_from('<I', block, i+1)[0]
            print(f"    0x{a:05X}: MOV  EBX, 0x{imm:X} ({imm})")
            i += 5
        elif b == 0x83 and i+2 < length:  # CMP/ADD/SUB EAX, imm8
            modrm = block[i+1]
            imm = block[i+2]
            if modrm == 0xf8:
                print(f"    0x{a:05X}: CMP  EAX, 0x{imm:X} ({imm})")
            elif modrm == 0xc0:
                print(f"    0x{a:05X}: ADD  EAX, 0x{imm:X}")
            else:
                print(f"    0x{a:05X}: OP83 /{(modrm>>3)&7} 0x{imm:X}")
            i += 3
        elif b == 0x80 and i+6 < length and block[i+1] == 0x35:  # XOR byte [addr], imm8
            addr_val = struct.unpack_from('<I', block, i+2)[0]
            imm = block[i+6]
            print(f"    0x{a:05X}: XOR  byte [0x{addr_val:05X}], 0x{imm:X}")
            i += 7
        elif b == 0x0f and i+5 < length and block[i+1] == 0x85:  # JNE rel32
            disp = struct.unpack_from('<i', block, i+2)[0]
            target = a + 6 + disp
            print(f"    0x{a:05X}: JNE  0x{target:05X}")
            i += 6
        elif b == 0x0f and i+5 < length and block[i+1] == 0x84:  # JE rel32
            disp = struct.unpack_from('<i', block, i+2)[0]
            target = a + 6 + disp
            print(f"    0x{a:05X}: JE   0x{target:05X}")
            i += 6
        elif b == 0x8b and i+1 < length:  # MOV r32, r/m32
            modrm = block[i+1]
            if modrm == 0x15 and i+5 < length:  # MOV EDX, [imm32]
                addr_val = struct.unpack_from('<I', block, i+2)[0]
                print(f"    0x{a:05X}: MOV  EDX, [0x{addr_val:05X}]")
                i += 6
            elif modrm == 0x0d and i+5 < length:
                addr_val = struct.unpack_from('<I', block, i+2)[0]
                print(f"    0x{a:05X}: MOV  ECX, [0x{addr_val:05X}]")
                i += 6
            else:
                print(f"    0x{a:05X}: MOV  (modrm=0x{modrm:02X}) ...")
                i += 2
        elif b == 0xa2 and i+4 < length:  # MOV [imm32], AL
            addr_val = struct.unpack_from('<I', block, i+1)[0]
            print(f"    0x{a:05X}: MOV  [0x{addr_val:05X}], AL")
            i += 5
        elif b == 0x3c and i+1 < length:  # CMP AL, imm8
            print(f"    0x{a:05X}: CMP  AL, 0x{block[i+1]:X}")
            i += 2
        elif b == 0x74 and i+1 < length:  # JE rel8
            disp = struct.unpack_from('<b', block, i+1)[0]
            target = a + 2 + disp
            print(f"    0x{a:05X}: JE   0x{target:05X}")
            i += 2
        elif b == 0x75 and i+1 < length:  # JNE rel8
            disp = struct.unpack_from('<b', block, i+1)[0]
            target = a + 2 + disp
            print(f"    0x{a:05X}: JNE  0x{target:05X}")
            i += 2
        elif b == 0xeb and i+1 < length:  # JMP rel8
            disp = struct.unpack_from('<b', block, i+1)[0]
            target = a + 2 + disp
            print(f"    0x{a:05X}: JMP  0x{target:05X}")
            i += 2
        elif b == 0xc6 and i+1 < length and block[i+1] == 0x05 and i+6 < length:  # MOV byte [addr], imm8
            addr_val = struct.unpack_from('<I', block, i+2)[0]
            imm = block[i+6]
            print(f"    0x{a:05X}: MOV  byte [0x{addr_val:05X}], 0x{imm:X}")
            i += 7
        elif b == 0x90:
            print(f"    0x{a:05X}: NOP")
            i += 1
        else:
            print(f"    0x{a:05X}: DB   0x{b:02X}")
            i += 1

with open("files/JUEGO.EXE", "rb") as f:
    exe_data = f.read()

# Action 350 handler: core logic (0x21FFB - 0x2202E)
decode_block(exe_data, 0x21FFB, 52, "ACTION 350 CORE (0x015E)")

# JMP target when flag == 3 → 0x222E3
decode_block(exe_data, 0x222E3, 32, "JMP TARGET: flag==3 path (0x222E3)")

# JNE target when flag != 3 → 0x222E8
decode_block(exe_data, 0x222E8, 16, "JNE TARGET: flag!=3 path (0x222E8)")

# Action 351 full body for comparison (0x2202F onwards - 300 bytes)
decode_block(exe_data, 0x2202F, 320, "ACTION 351 FULL (0x015F)")

# JMP target 0x1D66A
decode_block(exe_data, 0x1D66A, 64, "JMP TARGET 0x1D66A")

# Also check if 0x222E3 falls within a known larger block
print(f"\n{'='*70}")
print("FUNCTION ANALYSIS: What's at 0x222E3?")
print(f"{'='*70}")
print(f"  Action 349 starts at 0x21FC8, ends around 0x21FFA")
print(f"  Action 350 starts at 0x21FFB")
print(f"  Action 351 starts at 0x2202F")
print(f"  JMP target 0x222E3 is 0x2B4 bytes after action 351 start")
print(f"  JNE target 0x222E8 is 5 bytes after 0x222E3")

# Cross-reference: known function addresses
known_funcs = {
    0x1B666: "update_conversation_state",
    0x1B1A2: "play_get_naked_easter_egg (NPC talking anim)",
    0x2A218: "get_current_room_number (stack check)",
    0x24157: "process_inventory_action",
    0x15E4C: "render_scene",
    0x1D66A: "unknown_target",
    0x26F6C: "FUN_00026f6c",
}
print(f"\n  Known function cross-reference:")
for addr, name in sorted(known_funcs.items()):
    print(f"    0x{addr:05X}: {name}")
