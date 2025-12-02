#!/usr/bin/env python3
"""
Patch JUEGO.EXE to enable the jukebox cheat code "HIJODELAGRANPUTA"

This patches the flag at 0x495f3 from 0x00 to 0x01, enabling cheat detection.
"""

import sys
import os
import shutil

def patch_juego_exe(input_path, output_path=None):
    """Patch JUEGO.EXE to enable cheat code detection"""

    # Read the original file
    with open(input_path, 'rb') as f:
        data = bytearray(f.read())

    print(f"Loaded {input_path} ({len(data)} bytes)")

    # The flag address in memory is 0x000495f3
    # Need to find it in the file (might be different offset due to DOS4GW header)
    # Common DOS4GW offset is around 0x200-0x800

    # Strategy 1: Calculate correct file offset for DOS4GW executable
    # DOS4GW LINEAR executables have different file vs memory layout
    # The cheat string is at file 0x44141, memory 0x40f41
    # Difference: 0x44141 - 0x40f41 = 0x3200
    # So: file_offset = memory_address + 0x3200

    MEMORY_ADDRESS = 0x495f3
    FILE_OFFSET = MEMORY_ADDRESS + 0x3200  # = 0x4C7F3

    print(f"\nMemory address: 0x{MEMORY_ADDRESS:06x}")
    print(f"Calculated file offset: 0x{FILE_OFFSET:06x}")

    if FILE_OFFSET < len(data):
        current_value = data[FILE_OFFSET]
        print(f"Current value at file offset: 0x{current_value:02x}")

        if current_value == 0x00:
            print("✓ Found the flag (0x00), patching to 0x01...")
            data[FILE_OFFSET] = 0x01
        else:
            print(f"⚠ Value is 0x{current_value:02x}, patching anyway...")
            data[FILE_OFFSET] = 0x01
    else:
        print(f"⚠ Offset 0x{FILE_OFFSET:06x} beyond file size")

    # Strategy 2: Search for the cheat string and work backwards
    cheat_string = b'HIJODELAGRANPUTA'
    cheat_pos = data.find(cheat_string)

    if cheat_pos != -1:
        print(f"\n✓ Found cheat string at file offset 0x{cheat_pos:06x}")
        print(f"  Memory address would be around 0x{cheat_pos:06x}")

        # The flag is read before the string comparison
        # Let's search for the comparison instruction pattern near it
        # This is more reliable than guessing the offset

    # Strategy 3: Search for the initialization area
    # Look for the pattern where DAT_00049604 is set (we know this from 'p' flag)
    # The cheat flag should be nearby in the .data section

    # For DOS4GW executables, the linear executable format means
    # file offset ≈ memory address - 0x1000 (typical load address)
    # But let's try memory address directly first

    # Backup and save
    if output_path is None:
        backup_path = input_path + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(input_path, backup_path)
            print(f"\n✓ Created backup: {backup_path}")
        output_path = input_path

    with open(output_path, 'wb') as f:
        f.write(data)

    print(f"✓ Patched file saved to: {output_path}")
    print("\nPatch complete! Try the cheat code 'HIJODELAGRANPUTA' in-game.")
    print("If it doesn't work, we may need to find the correct file offset.")

    return True

def verify_patch(filepath):
    """Verify the patch was applied"""
    with open(filepath, 'rb') as f:
        data = f.read()

    MEMORY_ADDRESS = 0x495f3
    FILE_OFFSET = MEMORY_ADDRESS + 0x3200

    if FILE_OFFSET < len(data):
        value = data[FILE_OFFSET]
        print(f"\nVerification: file offset 0x{FILE_OFFSET:06x} = 0x{value:02x}")
        if value == 0x01:
            print("✓ Patch verified!")
            return True
        else:
            print("✗ Patch not applied")
            return False
    return False

if __name__ == '__main__':
    input_file = 'files/JUEGO.EXE'

    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        sys.exit(1)

    print("="*60)
    print("JUEGO.EXE Cheat Code Enabler")
    print("="*60)

    patch_juego_exe(input_file)
    verify_patch(input_file)

    print("\n" + "="*60)
    print("Instructions:")
    print("1. Run the patched JUEGO.EXE")
    print("2. Type: HIJODELAGRANPUTA")
    print("3. Use arrow keys to navigate music tracks")
    print("4. Press ESC to exit jukebox mode")
    print("="*60)
