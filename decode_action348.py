#!/usr/bin/env python3
"""Decode action 348 (0x015C) - the crash handler from piracy dialog."""
import struct

def code_to_file(addr):
    return addr - 0x10000 + 0x14200

with open("files/JUEGO.EXE", "rb") as f:
    exe_data = f.read()

addr = 0x21F3D
file_off = code_to_file(addr)
block = exe_data[file_off:file_off + 200]

print("="*70)
print(f"ACTION 348 (0x015C) HANDLER at 0x{addr:05X}")
print("="*70)

# Hex dump
for i in range(0, 200, 16):
    a = addr + i
    hexbytes = ' '.join(f'{b:02x}' for b in block[i:i+16])
    print(f"  0x{a:05X}: {hexbytes}")

# Trace instructions
print(f"\n  Instruction trace:")
i = 0
while i < 200:
    a = addr + i
    b = block[i]

    if b == 0x68 and i + 4 < len(block):  # PUSH imm32
        imm = struct.unpack_from('<I', block, i+1)[0]
        print(f"    0x{a:05X}: PUSH 0x{imm:X} ({imm})")
        i += 5
    elif b == 0xe8 and i + 4 < len(block):  # CALL rel32
        disp = struct.unpack_from('<i', block, i+1)[0]
        target = a + 5 + disp
        print(f"    0x{a:05X}: CALL 0x{target:05X}")
        i += 5
    elif b == 0xe9 and i + 4 < len(block):  # JMP rel32
        disp = struct.unpack_from('<i', block, i+1)[0]
        target = a + 5 + disp
        print(f"    0x{a:05X}: JMP  0x{target:05X}")
        i += 5
    elif b == 0xb8 and i + 4 < len(block):  # MOV EAX, imm32
        imm = struct.unpack_from('<I', block, i+1)[0]
        print(f"    0x{a:05X}: MOV  EAX, 0x{imm:X} ({imm})")
        i += 5
    elif b == 0xbb and i + 4 < len(block):  # MOV EBX, imm32
        imm = struct.unpack_from('<I', block, i+1)[0]
        print(f"    0x{a:05X}: MOV  EBX, 0x{imm:X} ({imm})")
        i += 5
    elif b == 0xba and i + 4 < len(block):  # MOV EDX, imm32
        imm = struct.unpack_from('<I', block, i+1)[0]
        print(f"    0x{a:05X}: MOV  EDX, 0x{imm:X} ({imm})")
        i += 5
    elif b == 0x53:
        print(f"    0x{a:05X}: PUSH EBX"); i += 1
    elif b == 0x52:
        print(f"    0x{a:05X}: PUSH EDX"); i += 1
    elif b == 0x5a:
        print(f"    0x{a:05X}: POP  EDX"); i += 1
    elif b == 0x5b:
        print(f"    0x{a:05X}: POP  EBX"); i += 1
    elif b == 0xc3:
        print(f"    0x{a:05X}: RET"); i += 1
        break
    elif b == 0x31 and i+1 < len(block):
        r1 = (block[i+1] >> 3) & 7
        r2 = block[i+1] & 7
        regs = ['EAX','ECX','EDX','EBX','ESP','EBP','ESI','EDI']
        print(f"    0x{a:05X}: XOR  {regs[r2]}, {regs[r1]}")
        i += 2
    elif b == 0x89 and i+1 < len(block):
        modrm = block[i+1]
        r1 = (modrm >> 3) & 7
        r2 = modrm & 7
        regs = ['EAX','ECX','EDX','EBX','ESP','EBP','ESI','EDI']
        print(f"    0x{a:05X}: MOV  {regs[r2]}, {regs[r1]}")
        i += 2
    elif b == 0x80 and i+6 < len(block) and block[i+1] == 0x35:
        addr_val = struct.unpack_from('<I', block, i+2)[0]
        imm = block[i+6]
        print(f"    0x{a:05X}: XOR  byte [0x{addr_val:05X}], 0x{imm:X}")
        i += 7
    elif b == 0xa0 and i+4 < len(block):
        addr_val = struct.unpack_from('<I', block, i+1)[0]
        print(f"    0x{a:05X}: MOV  AL, [0x{addr_val:05X}]")
        i += 5
    elif b == 0x83 and i+2 < len(block):
        modrm = block[i+1]
        imm = block[i+2]
        ops = ['ADD','OR','ADC','SBB','AND','SUB','XOR','CMP']
        reg = modrm & 7
        op = (modrm >> 3) & 7
        regs = ['EAX','ECX','EDX','EBX','ESP','EBP','ESI','EDI']
        print(f"    0x{a:05X}: {ops[op]}  {regs[reg]}, 0x{imm:X}")
        i += 3
    elif b == 0x0f and i+5 < len(block):
        cc = block[i+1]
        disp = struct.unpack_from('<i', block, i+2)[0]
        target = a + 6 + disp
        cc_names = {0x84:'JE', 0x85:'JNE', 0x8E:'JLE', 0x8F:'JG', 0x8C:'JL', 0x8D:'JGE'}
        name = cc_names.get(cc, f'J?? (0x{cc:02X})')
        print(f"    0x{a:05X}: {name}  0x{target:05X}")
        i += 6
    elif b == 0x75 and i+1 < len(block):
        disp = struct.unpack_from('<b', block, i+1)[0]
        target = a + 2 + disp
        print(f"    0x{a:05X}: JNE  0x{target:05X}")
        i += 2
    elif b == 0x74 and i+1 < len(block):
        disp = struct.unpack_from('<b', block, i+1)[0]
        target = a + 2 + disp
        print(f"    0x{a:05X}: JE   0x{target:05X}")
        i += 2
    elif b == 0xeb and i+1 < len(block):
        disp = struct.unpack_from('<b', block, i+1)[0]
        target = a + 2 + disp
        print(f"    0x{a:05X}: JMP  0x{target:05X}")
        i += 2
    elif b == 0xcd and i+1 < len(block):
        intno = block[i+1]
        print(f"    0x{a:05X}: INT  0x{intno:02X}")
        i += 2
    elif b == 0xcf:
        print(f"    0x{a:05X}: IRET"); i += 1
    elif b == 0xf4:
        print(f"    0x{a:05X}: HLT  *** HALTS CPU ***"); i += 1
    elif b == 0xfa:
        print(f"    0x{a:05X}: CLI  *** DISABLE INTERRUPTS ***"); i += 1
    elif b == 0xfb:
        print(f"    0x{a:05X}: STI  *** ENABLE INTERRUPTS ***"); i += 1
    elif b == 0xcc:
        print(f"    0x{a:05X}: INT3 *** BREAKPOINT / CRASH ***"); i += 1
    else:
        print(f"    0x{a:05X}: DB   0x{b:02X}")
        i += 1

# Also check the known functions
known = {
    0x2A218: "stack_check/get_current_room_number",
    0x1B666: "update_conversation_state",
    0x24157: "process_inventory_action",
    0x28FD5: "set_vga_mode",
    0x244E8: "set_vga_palette",
}
print(f"\n  Known function addresses:")
for a, n in sorted(known.items()):
    print(f"    0x{a:05X}: {n}")
