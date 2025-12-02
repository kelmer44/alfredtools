#!/usr/bin/env python3
"""
Alternative patch: NOP out the flag check entirely

Instead of setting the flag, we'll patch the conditional jump so it never skips the cheat code.

Assembly at 0x00010500 (file offset 0x13700):
00010500: CMP byte ptr [0x000495f3],0x0    ; 80 3D F3 95 04 00 00
00010507: JZ 0x00010621                     ; 0F 84 14 01 00 00

We'll NOP out the JZ instruction (6 bytes) so it never jumps.
"""

import sys
import os
import shutil

def patch_juego_nop(input_path, output_path=None):
    """Patch JUEGO.EXE by NOPing the flag check"""

    with open(input_path, 'rb') as f:
        data = bytearray(f.read())

    print(f"Loaded {input_path} ({len(data)} bytes)")

    # Calculate file offset for the JZ instruction at memory 0x00010507
    # Using same offset calculation: memory + 0x3200
    # But this is in code segment (.object1), not data segment
    # Code segment starts at memory 0x00010000
    # Need to find actual file offset by searching for the instruction pattern

    # The pattern around the check:
    # 80 3D F3 95 04 00 00   CMP byte ptr [0x000495f3],0x0
    # 0F 84 14 01 00 00      JZ 0x00010621 (relative jump)

    pattern = bytes([0x80, 0x3D, 0xF3, 0x95, 0x04, 0x00, 0x00, 0x0F, 0x84])

    pos = data.find(pattern)
    if pos == -1:
        print("✗ Could not find the flag check pattern")
        print("Searching for alternative patterns...")

        # Try just the JZ part with some context
        alt_pattern = bytes([0x3D, 0xF3, 0x95, 0x04, 0x00, 0x00, 0x0F, 0x84])
        pos = data.find(alt_pattern)
        if pos != -1:
            pos -= 1  # Back up to include the 0x80

    if pos != -1:
        jz_offset = pos + 7  # Position of the JZ instruction (0x0F 0x84)
        print(f"\n✓ Found flag check at file offset: 0x{pos:06x}")
        print(f"  JZ instruction at: 0x{jz_offset:06x}")

        # Show current bytes
        current = data[pos:pos+13]
        print(f"  Current bytes: {' '.join(f'{b:02x}' for b in current)}")

        # NOP out the JZ instruction (6 bytes: 0F 84 14 01 00 00)
        # NOP = 0x90
        for i in range(6):
            data[jz_offset + i] = 0x90

        patched = data[pos:pos+13]
        print(f"  Patched bytes: {' '.join(f'{b:02x}' for b in patched)}")
        print("\n✓ NOP'd out the conditional jump - cheat check will always pass")
    else:
        print("✗ Could not find instruction pattern")
        print("Trying direct offset calculation...")

        # Fallback: calculate offset directly
        # Code segment memory 0x10000 -> file offset needs verification
        # Let's search for a known function start
        mem_addr = 0x00010507

        # Try different base offsets
        for base in [0x200, 0x400, 0x600, 0x800, 0x1000, 0x2000, 0x3000, 0x3200]:
            file_offset = mem_addr - 0x10000 + base
            if file_offset < len(data) - 10:
                chunk = data[file_offset:file_offset+10]
                if chunk[0:2] == bytes([0x0F, 0x84]):
                    print(f"Found JZ at offset 0x{file_offset:06x} (base=0x{base:04x})")
                    for i in range(6):
                        data[file_offset + i] = 0x90
                    break

    # Backup and save
    if output_path is None:
        backup_path = input_path + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(input_path, backup_path)
            print(f"\n✓ Created backup: {backup_path}")
        else:
            print(f"\n✓ Using existing backup: {backup_path}")
        output_path = input_path

    with open(output_path, 'wb') as f:
        f.write(data)

    print(f"✓ Patched file saved to: {output_path}")
    return True

if __name__ == '__main__':
    input_file = 'files/JUEGO.EXE'

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        sys.exit(1)

    # Restore from backup first
    backup_file = input_file + '.backup'
    if os.path.exists(backup_file):
        print(f"Restoring from backup: {backup_file}")
        shutil.copy2(backup_file, input_file)

    print("="*60)
    print("JUEGO.EXE Cheat Code Patcher (NOP method)")
    print("="*60)

    patch_juego_nop(input_file)

    print("\n" + "="*60)
    print("Patch complete!")
    print("Type 'HIJODELAGRANPUTA' during gameplay to activate jukebox")
    print("="*60)
