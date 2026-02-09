#!/usr/bin/env python3
"""
Decode the F8 handlers for room 22 actions 349-351 at their real addresses 
(+0x10000 fixup applied). These are the handlers that give the CD to the player.
"""
import struct

def code_to_file(addr):
    return addr - 0x10000 + 0x14200

with open("files/JUEGO.EXE", "rb") as f:
    exe_data = f.read()

# Real addresses after fixup
handlers = [
    (349, 0x21fc8, "action_349_disable_conv_root"),
    (350, 0x21ffb, "action_350_unknown"),
    (351, 0x2202f, "action_351_trigger_conversation"),
]

for action_id, real_addr, desc in handlers:
    print(f"{'='*70}")
    print(f"F8 ACTION {action_id} HANDLER at 0x{real_addr:05x} ({desc})")
    print(f"{'='*70}")
    
    file_off = code_to_file(real_addr)
    block = exe_data[file_off:file_off + 128]
    
    # Hex dump
    for i in range(0, 128, 16):
        addr = real_addr + i
        hexbytes = ' '.join(f'{b:02x}' for b in block[i:i+16])
        print(f"  0x{addr:05x}: {hexbytes}")
    
    # Trace CALL/JMP targets
    print(f"\n  CALL/JMP targets:")
    for i in range(min(len(block) - 5, 200)):
        b = block[i]
        addr_cur = real_addr + i
        if b == 0xe8:  # CALL rel32
            disp = struct.unpack_from('<i', block, i + 1)[0]
            target = addr_cur + 5 + disp
            print(f"    0x{addr_cur:05x}: CALL 0x{target:05x}")
        elif b == 0xe9:  # JMP rel32
            disp = struct.unpack_from('<i', block, i + 1)[0]
            target = addr_cur + 5 + disp
            print(f"    0x{addr_cur:05x}: JMP  0x{target:05x}")
    print()

# Also check: where does item 95 get added to inventory?
# The grant code at 0x21b80 (found earlier): MOV EAX, 95; JMP process_inventory_action
# With fixup: the real address would be 0x21b80 + 0x10000 = 0x31b80??? 
# Wait, no - 0x21b80 was found by searching WITHIN the code section, not from a table.
# The bytes at 0x21b80 are at file offset 0x21b80 - 0x10000 + 0x14200 = 0x25d80.
# Let me verify.

print(f"{'='*70}")
print("ITEM 95 GRANT CODE AT 0x21b80")
print(f"{'='*70}")

addr = 0x21b80
file_off = code_to_file(addr)
block = exe_data[file_off:file_off + 32]
hexstr = ' '.join(f'{b:02x}' for b in block)
print(f"  0x{addr:05x}: {hexstr}")

# This should be: b8 5f000000 e9 xxxx = MOV EAX, 95; JMP process_inventory_action
# process_inventory_action is at 0x24157 (or does IT also need fixup?)
# Wait - 0x24157 was a Ghidra address. If it's in the analyzed region, it should be correct.
# But the JMP displacement is computed from the raw bytes...

# Let me decode:
if block[0] == 0xb8:
    imm = struct.unpack_from('<I', block, 1)[0]
    print(f"  MOV EAX, {imm} (item ID)")
    if block[5] == 0xe9:
        disp = struct.unpack_from('<i', block, 6)[0]
        target = addr + 10 + disp
        print(f"  JMP 0x{target:05x} (process_inventory_action?)")

print()
print(f"{'='*70}")
print("ITEM 96 GRANT CODE AT 0x21b94")
print(f"{'='*70}")

addr = 0x21b94
file_off = code_to_file(addr)
block = exe_data[file_off:file_off + 32]
hexstr = ' '.join(f'{b:02x}' for b in block)
print(f"  0x{addr:05x}: {hexstr}")

if block[0] == 0xb8:
    imm = struct.unpack_from('<I', block, 1)[0]
    print(f"  MOV EAX, {imm} (item ID)")
    if block[5] == 0xe9:
        disp = struct.unpack_from('<i', block, 6)[0]
        target = addr + 10 + disp
        print(f"  JMP 0x{target:05x} (process_inventory_action?)")

# Now check what calls 0x21b80 - trace who references this address
print()
print(f"{'='*70}")
print("SEARCHING FOR CALL/JMP TO 0x21b80 and 0x21b94")
print(f"{'='*70}")

code_start = 0x14200
code_end = 0x43200

for target_addr in [0x21b80, 0x21b94]:
    for opcode_byte, name in [(0xe8, "CALL"), (0xe9, "JMP")]:
        for pos in range(code_start, code_end - 5):
            if exe_data[pos] == opcode_byte:
                disp = struct.unpack_from('<i', exe_data, pos + 1)[0]
                ghidra_pos = pos - 0x14200 + 0x10000
                call_target = ghidra_pos + 5 + disp
                if call_target == target_addr:
                    print(f"  {name} to 0x{target_addr:05x} from 0x{ghidra_pos:05x}")
