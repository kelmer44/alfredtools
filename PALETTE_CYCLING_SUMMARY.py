#!/usr/bin/env python3
"""
PALETTE CYCLING DISCOVERY - SUMMARY
====================================

This script documents the complete palette cycling system discovered through:
1. Ghidra decompilation of JUEGO.EXE
2. Analysis of user-provided video frames
3. Binary search of JUEGO.EXE

FINDINGS:
- Room 2 (McDowells restaurant) uses palette cycling
- Animation is MODE 1 (single color fade, not rotation)
- Animates palette index 250 (green color in McDowells sign)
- Config stored at file offset 0x0004B860 in JUEGO.EXE
"""

import struct

def read_config(data, offset):
    """Read and parse 12-byte cycling config."""
    if offset + 12 > len(data):
        return None

    cfg = data[offset:offset+12]
    return {
        'offset': offset,
        'raw': cfg,
        'start_index': cfg[0],
        'mode': cfg[1],
        'current_rgb': (cfg[2], cfg[3], cfg[4]),
        'min_rgb': (cfg[5], cfg[6], cfg[7]),
        'max_rgb': (cfg[8], cfg[9], cfg[10]),
        'flags': cfg[11]
    }

def print_config(config):
    """Pretty-print a cycling config."""
    print(f"  File offset: 0x{config['offset']:08X}")
    print(f"  Raw bytes: {' '.join(f'{b:02x}' for b in config['raw'])}")
    print(f"  Palette index: {config['start_index']} (0x{config['start_index']:02X})")
    mode_str = 'fade' if config['mode'] == 1 else f"rotate (count={config['mode']})"
    print(f"  Mode: {config['mode']} ({mode_str})")
    print(f"  Current RGB (6-bit): {config['current_rgb']} = ({config['current_rgb'][0]*4}, {config['current_rgb'][1]*4}, {config['current_rgb'][2]*4}) in 8-bit")
    print(f"  Min RGB (6-bit): {config['min_rgb']} = ({config['min_rgb'][0]*4}, {config['min_rgb'][1]*4}, {config['min_rgb'][2]*4}) in 8-bit")
    print(f"  Max RGB (6-bit): {config['max_rgb']} = ({config['max_rgb'][0]*4}, {config['max_rgb'][1]*4}, {config['max_rgb'][2]*4}) in 8-bit")
    print(f"  Flags: 0x{config['flags']:02X} (binary: {config['flags']:08b})")
    if config['mode'] == 1:
        print(f"    Bit 6 (direction): {'1=down' if config['flags'] & 0x40 else '0=up'}")
        print(f"    Lower bits (speed): {config['flags'] & 0x3F}")

# Load JUEGO.EXE
with open('files/JUEGO.EXE', 'rb') as f:
    exe_data = f.read()

print("="*80)
print("ALFRED PELROCK - PALETTE CYCLING SYSTEM")
print("="*80)
print()

print("DISCOVERED THROUGH:")
print("  1. Ghidra MCP decompilation of update_palette_cycling @ 0x00016804")
print("  2. User-provided video frames showing McDowells sign animation")
print("  3. Binary pattern search for min/max RGB values in JUEGO.EXE")
print()

print("="*80)
print("ROOM 2 - McDowells Restaurant Sign Animation")
print("="*80)
print()

# Read room 2 config
room2_config = read_config(exe_data, 0x0004B860)
if room2_config:
    print("CONFIGURATION:")
    print_config(room2_config)
    print()
    print("VISUAL DESCRIPTION:")
    print("  - Location: McDowells sign/logo in background")
    print("  - Sign area: approximately (350, 53, 588, 160)")
    print("  - Only ONE color animates: the green text/logo")
    print("  - Animation: Fades from dark green to bright green and back")
    print("  - Darkest: RGB(48, 81, 32)")
    print("  - Lightest: RGB(146, 178, 32)")
    print()
    print("HOW IT WORKS:")
    print("  - Game calls update_palette_cycling() every frame in render loop")
    print("  - Reads config pointer from DAT_0004f8ec (set by load_room_data)")
    print("  - Gradually increments/decrements RGB values toward min or max")
    print("  - Writes to VGA palette ports 0x3C8 (index) and 0x3C9 (RGB data)")
    print("  - Creates smooth color fade effect")

print()
print("="*80)
print("OTHER CYCLING CONFIGS FOUND NEARBY")
print("="*80)
print()

# Scan for other configs near room 2's config
print("Scanning 0x4B800 to 0x4BA00 for additional configs...")
configs_found = []

for offset in range(0x4B800, 0x4BA00, 12):
    if offset + 12 > len(exe_data):
        break

    cfg_data = exe_data[offset:offset+12]

    # Validate: mode 1-10, RGB values 0-63
    if 1 <= cfg_data[1] <= 10:
        if all(0 <= cfg_data[i] <= 63 for i in range(5, 11)):
            configs_found.append(read_config(exe_data, offset))

print(f"Found {len(configs_found)} potential cycling configs:")
print()

for i, cfg in enumerate(configs_found, 1):
    print(f"CONFIG #{i}:")
    print_config(cfg)

    if cfg['offset'] == 0x0004B860:
        print("  *** THIS IS THE ROOM 2 CONFIG (McDowells sign) ***")

    print()

print("="*80)
print("CYCLING TABLE STRUCTURE")
print("="*80)
print()
print("Based on Ghidra decompilation of load_room_data @ 0x000152f5:")
print()
print("  Table location: &DAT_000486a4 (memory address)")
print("  Entry format: [room_number:2 bytes][config_pointer:4 bytes]")
print("  Terminator: 0xFFFF")
print()
print("  The game scans this table at room load:")
print("    - Loops through entries checking room_number")
print("    - When match found, sets DAT_0004f8ea = 1 (cycling enabled)")
print("    - Sets DAT_0004f8ec = config_pointer")
print("    - Config pointer points to 12-byte config in executable")
print()
print("  NOTE: File offset mapping for table not yet determined.")
print("        Room 2's config definitely at file 0x4B860.")
print()

print("="*80)
print("FILES GENERATED")
print("="*80)
print()
print("  room_02_mcdowells_fade.gif")
print("    - Animated GIF showing palette index 250 fading")
print("    - Fades between dark and bright green")
print("    - Matches actual game animation")
print()
print("  search_cycling_config.py")
print("    - Searches JUEGO.EXE for cycling configs by RGB values")
print("    - Found room 2 config at 0x4B860")
print()
print("  create_mcdowells_fade.py")
print("    - Extracts room 2 background with correct RLE decompression")
print("    - Creates fade animation using config values")
print()

print("="*80)
print("RELATED DOCUMENTATION")
print("="*80)
print()
print("  CONVERSATION_SYSTEM_DOCUMENTATION.md")
print("    - Complete documentation of the conversation tree system")
print("    - Control bytes, text formatting, and branching logic")
print("    - Located in resource pair 12")
print()
print("="*80)
print("NEXT STEPS")
print("="*80)
print()
print("  1. Map cycling table at 0x486a4 to file offset")
print("  2. Extract all room cycling configs from table")
print("  3. Create animations for other rooms with cycling")
print("  4. Document complete palette cycling system")
print()
print("="*80)
