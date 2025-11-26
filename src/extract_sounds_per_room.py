#!/usr/bin/env python3
"""
Alfred Pelrock - Room Sound Effects Extractor

Extracts the mapping of ambient sound effects for each room from ALFRED.1.

Structure:
- Each room has a 104-byte structure
- Pair 12 at offset (room * 104) + (12 * 8) contains sound data
- First byte: palette ID
- Next 9 bytes: indices into the sound filename array (0-102)
"""

import struct
import sys
from pathlib import Path

# Sound filename array (from game executable at 0x48dd8)
SOUND_FILENAMES = [
    "NO_SOUND.SMP",    # 0
    "BUHO_ZZZ.SMP",    # 1
    "BIRD_1_1.SMP",    # 2
    "BIRD_1_2.SMP",    # 3
    "BIRD_1_3.SMP",    # 4
    "DESPERZZ.SMP",    # 5
    "HORN_5ZZ.SMP",    # 6
    "HORN_6ZZ.SMP",    # 7
    "HORN_8ZZ.SMP",    # 8
    "SUZIPASS.SMP",    # 9
    "CAT_1ZZZ.SMP",    # 10
    "DOG_01ZZ.SMP",    # 11
    "DOG_02ZZ.SMP",    # 12
    "DOG_04ZZ.SMP",    # 13
    "DOG_05ZZ.SMP",    # 14
    "DOG_06ZZ.SMP",    # 15
    "DOG_07ZZ.SMP",    # 16
    "DOG_09ZZ.SMP",    # 17
    "ALARMZZZ.SMP",    # 18
    "AMBULAN1.SMP",    # 19
    "FOUNTAIN.SMP",    # 20
    "GRILLOSZ.SMP",    # 21
    "HOJASZZZ.SMP",    # 22
    "FLASHZZZ.SMP",    # 23
    "CUCHI1ZZ.SMP",    # 24
    "KNRRRRRZ.SMP",    # 25
    "PHONE_02.SMP",    # 26
    "PHONE_03.SMP",    # 27
    "SSSHTZZZ.SMP",    # 28
    "BURGUER1.SMP",    # 29
    "FLIES_2Z.SMP",    # 30
    "PARRILLA.SMP",    # 31
    "WATER_2Z.SMP",    # 32
    "XIQUETZZ.SMP",    # 33
    "RONQUIZZ.SMP",    # 34
    "MOCO1ZZZ.SMP",    # 35
    "MOCO2ZZZ.SMP",    # 36
    "SPRINGZZ.SMP",    # 37
    "MARUJASZ.SMP",    # 38
    "ELECTROZ.SMP",    # 39
    "GLASS1ZZ.SMP",    # 40
    "OPDOORZZ.SMP",    # 41
    "CLDOORZZ.SMP",    # 42
    "FXH2ZZZZ.SMP",    # 43
    "BOTEZZZZ.SMP",    # 44
    "ELEC3ZZZ.SMP",    # 45
    "AJARLZZZ.SMP",    # 46
    "BELCHZZZ.SMP",    # 47
    "64ZZZZZZ.SMP",    # 48
    "BIRDOWL2.SMP",    # 49
    "BUBBLE2Z.SMP",    # 50
    "BURGUER1.SMP",    # 51  # Duplicate
    "CACKLEZZ.SMP",    # 52
    "CERAMIC1.SMP",    # 53
    "CLANG5ZZ.SMP",    # 54
    "CUCHI2ZZ.SMP",    # 55
    "CUCHI3ZZ.SMP",    # 56
    "ELEC3ZZZ.SMP",    # 57  # Duplicate
    "HOJASZZZ.SMP",    # 58  # Duplicate
    "LIMA1ZZZ.SMP",    # 59
    "MOROSZZZ.SMP",    # 60
    "MOROZZZZ.SMP",    # 61
    "MUD1ZZZZ.SMP",    # 62
    "PICOZZZZ.SMP",    # 63
    "PICO1XZZ.SMP",    # 64
    "PICO2XZZ.SMP",    # 65
    "PICO3XZZ.SMP",    # 66
    "RIMSHOTZ.SMP",    # 67
    "RONCOZZZ.SMP",    # 68
    "SORBOZZZ.SMP",    # 69
    "VIENTO1Z.SMP",    # 70
    "2ZZZZZZZ.SMP",    # 71
    "20ZZZZZZ.SMP",    # 72
    "21ZZZZZZ.SMP",    # 73
    "23ZZZZZZ.SMP",    # 74
    "107ZZZZZ.SMP",    # 75
    "39ZZZZZZ.SMP",    # 76
    "81ZZZZZZ.SMP",    # 77
    "88ZZZZZZ.SMP",    # 78
    "92ZZZZZZ.SMP",    # 79
    "SAW_2ZZZ.SMP",    # 80
    "QUAKE2ZZ.SMP",    # 81
    "ROCKSZZZ.SMP",    # 82
    "IN_FIREZ.SMP",    # 83
    "BEAMZZZZ.SMP",    # 84
    "GLISSDWN.SMP",    # 85
    "REMATERL.SMP",    # 86
    "FXH1ZZZZ.SMP",    # 87
    "FXH3ZZZZ.SMP",    # 88
    "FXH4ZZZZ.SMP",    # 89
    "MATCHZZZ.SMP",    # 90
    "SURF_01Z.SMP",    # 91
    "SURF_02Z.SMP",    # 92
    "SURF_04Z.SMP",    # 93
    "11ZZZZZZ.SMP",    # 94
    "41ZZZZZZ.SMP",    # 95
    "56ZZZZZZ.SMP",    # 96
    "GATITOZZ.SMP",    # 97
    "9ZZZZZZZ.SMP",    # 98
    "CHIQUITO.SMP",    # 99
]

def extract_room_sounds(alfred1_path, output_dir=None):
    """Extract sound effect mappings for all rooms"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("Alfred Pelrock - Room Sound Effects Extractor")
    print("=" * 80)
    print()

    NUM_ROOMS = 56
    ROOM_STRUCT_SIZE = 104

    all_rooms = []

    for room_num in range(NUM_ROOMS):
        room_offset = room_num * ROOM_STRUCT_SIZE

        # Pair 12 contains sound data (offset + size at room_offset + 12*8)
        pair12_offset_pos = room_offset + (12 * 8)
        pair12_data_offset = struct.unpack('<I', data[pair12_offset_pos:pair12_offset_pos+4])[0]
        pair12_size = struct.unpack('<I', data[pair12_offset_pos+4:pair12_offset_pos+8])[0]

        if pair12_data_offset == 0 or pair12_size == 0:
            print(f"Room {room_num:2d}: No sound data")
            continue

        # First byte is palette ID
        palette_id = data[pair12_data_offset]

        # Next 9 bytes are sound indices
        sound_indices = []
        sounds = []
        for i in range(9):
            idx = data[pair12_data_offset + 1 + i]
            sound_indices.append(idx)
            if idx < len(SOUND_FILENAMES):
                sounds.append(SOUND_FILENAMES[idx])
            else:
                sounds.append(f"UNKNOWN_{idx}")

        # Filter out NO_SOUND entries for cleaner display
        active_sounds = [s for s in sounds if s != "NO_SOUND.SMP"]

        all_rooms.append({
            'room': room_num,
            'palette_id': palette_id,
            'sound_indices': sound_indices,
            'sounds': sounds
        })

        if active_sounds:
            print(f"Room {room_num:2d}: Palette {palette_id:2d} | {len(active_sounds)} sound(s)")
            for i, sound in enumerate(sounds):
                if sound != "NO_SOUND.SMP":
                    print(f"  Slot {i}: {sound} (index {sound_indices[i]})")
        else:
            print(f"Room {room_num:2d}: Palette {palette_id:2d} | No ambient sounds")

    # Save outputs if requested
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save as text
        txt_file = output_path / "room_sounds.txt"
        with open(txt_file, 'w') as f:
            f.write("Alfred Pelrock - Room Sound Effects\n")
            f.write("=" * 80 + "\n\n")

            for room_data in all_rooms:
                f.write(f"Room {room_data['room']:2d}:\n")
                f.write(f"  Palette ID: {room_data['palette_id']}\n")
                f.write(f"  Ambient Sounds:\n")
                for i, (idx, sound) in enumerate(zip(room_data['sound_indices'], room_data['sounds'])):
                    if sound != "NO_SOUND.SMP":
                        f.write(f"    Slot {i}: {sound} (index {idx})\n")
                f.write("\n")

        print(f"\nSaved to: {txt_file}")

        # Save as Python
        py_file = output_path / "room_sounds.py"
        with open(py_file, 'w') as f:
            f.write("# Alfred Pelrock - Room Sound Effects\n\n")
            f.write("ROOM_SOUNDS = {\n")
            for room_data in all_rooms:
                f.write(f"    {room_data['room']}: {{\n")
                f.write(f"        'palette_id': {room_data['palette_id']},\n")
                f.write(f"        'sound_indices': {room_data['sound_indices']},\n")
                f.write(f"        'sounds': {room_data['sounds']},\n")
                f.write("    },\n")
            f.write("}\n")

        print(f"Saved to: {py_file}")

    print("\n" + "=" * 80)
    print(f"Extracted sound data for {len(all_rooms)} rooms")

    return all_rooms

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nUsage: python extract_room_sounds.py <alfred.1> [output_dir]")
        print("\nExample:")
        print("  python extract_room_sounds.py ALFRED.1 room_sounds/")
        sys.exit(1)

    alfred1_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "room_sounds"

    if not Path(alfred1_path).exists():
        print(f"Error: File not found: {alfred1_path}")
        sys.exit(1)

    extract_room_sounds(alfred1_path, output_dir)

if __name__ == "__main__":
    main()
