#!/usr/bin/env python3
"""
Alfred Pelrock - Room SFX (Ambient Sound Effects) Extractor

Extracts the mapping of ambient sound effects for each room from ALFRED.1.

Based on Ghidra reverse engineering of load_room_music_and_ambient_sounds():

Structure in ALFRED.1:
- Room directory at offset 0, size 0x189C (6300 bytes)
- Each room entry is 104 bytes (13 pairs of offset+size, 8 bytes each)
- Pair 9 (offset 0x48 from room entry) contains the sound/music data pointer

Sound data structure (10 bytes):
- Byte 0: Music track ID (CD audio track number, 0 = silence)
- Bytes 1-9: Sound file indices into sound_filename_array (0 = NO_SOUND.SMP)

The game loads 9 ambient sounds per room from SONIDOS.DAT based on these indices.
"""

import struct
import sys
from pathlib import Path

# Sound filename array extracted from JUEGO.EXE at 0x48dd8
# Index 0 = NO_SOUND.SMP means slot is disabled
SOUND_FILENAMES = [
    "NO_SOUND.SMP",    # 0 - Silence/disabled
    "BUHO_ZZZ.SMP",    # 1 - Owl
    "BIRD_1_1.SMP",    # 2 - Bird variant 1
    "BIRD_1_2.SMP",    # 3 - Bird variant 2
    "BIRD_1_3.SMP",    # 4 - Bird variant 3
    "DESPERZZ.SMP",    # 5 - Yawn/stretch
    "HORN_5ZZ.SMP",    # 6 - Car horn 5
    "HORN_6ZZ.SMP",    # 7 - Car horn 6
    "HORN_8ZZ.SMP",    # 8 - Car horn 8
    "SUZIPASS.SMP",    # 9 - Suzi passing
    "CAT_1ZZZ.SMP",    # 10 - Cat
    "DOG_01ZZ.SMP",    # 11 - Dog bark 1
    "DOG_02ZZ.SMP",    # 12 - Dog bark 2
    "DOG_04ZZ.SMP",    # 13 - Dog bark 4
    "DOG_05ZZ.SMP",    # 14 - Dog bark 5
    "DOG_06ZZ.SMP",    # 15 - Dog bark 6
    "DOG_07ZZ.SMP",    # 16 - Dog bark 7
    "DOG_09ZZ.SMP",    # 17 - Dog bark 9
    "ALARMZZZ.SMP",    # 18 - Alarm
    "AMBULAN1.SMP",    # 19 - Ambulance
    "FOUNTAIN.SMP",    # 20 - Fountain
    "GRILLOSZ.SMP",    # 21 - Crickets
    "HOJASZZZ.SMP",    # 22 - Leaves rustling
    "FLASHZZZ.SMP",    # 23 - Flash/camera
    "CUCHI1ZZ.SMP",    # 24 - Knife 1
    "KNRRRRRZ.SMP",    # 25 - Snoring
    "PHONE_02.SMP",    # 26 - Phone ring 2
    "PHONE_03.SMP",    # 27 - Phone ring 3
    "SSSHTZZZ.SMP",    # 28 - Shush/quiet
    "BURGUER1.SMP",    # 29 - Burger sizzle
    "FLIES_2Z.SMP",    # 30 - Flies buzzing
    "PARRILLA.SMP",    # 31 - Grill
    "WATER_2Z.SMP",    # 32 - Water
    "XIQUETZZ.SMP",    # 33 - Whistle
    "RONQUIZZ.SMP",    # 34 - Snoring
    "MOCO1ZZZ.SMP",    # 35 - Snot/mucus 1
    "MOCO2ZZZ.SMP",    # 36 - Snot/mucus 2
    "SPRINGZZ.SMP",    # 37 - Spring bounce
    "MARUJASZ.SMP",    # 38 - Gossip/chatter
    "ELECTROZ.SMP",    # 39 - Electric shock
    "GLASS1ZZ.SMP",    # 40 - Glass clink
    "OPDOORZZ.SMP",    # 41 - Door open
    "CLDOORZZ.SMP",    # 42 - Door close
    "FXH2ZZZZ.SMP",    # 43 - Effect 2
    "BOTEZZZZ.SMP",    # 44 - Bottle
    "ELEC3ZZZ.SMP",    # 45 - Electric 3
    "AJARLZZZ.SMP",    # 46 - Ajar/creak
    "BELCHZZZ.SMP",    # 47 - Belch/burp
    "64ZZZZZZ.SMP",    # 48 - Sound effect 64
    "BIRDOWL2.SMP",    # 49 - Bird/owl 2
    "BUBBLE2Z.SMP",    # 50 - Bubbles
    "BURGUER1.SMP",    # 51 - Burger (duplicate)
    "CACKLEZZ.SMP",    # 52 - Cackle/laugh
    "CERAMIC1.SMP",    # 53 - Ceramic break
    "CLANG5ZZ.SMP",    # 54 - Metal clang
    "CUCHI2ZZ.SMP",    # 55 - Knife 2
    "CUCHI3ZZ.SMP",    # 56 - Knife 3
    "ELEC3ZZZ.SMP",    # 57 - Electric 3 (duplicate)
    "HOJASZZZ.SMP",    # 58 - Leaves (duplicate)
    "LIMA1ZZZ.SMP",    # 59 - File/rasp
    "MOROSZZZ.SMP",    # 60 - Moors/crowd
    "MOROZZZZ.SMP",    # 61 - Moor/crowd
    "MUD1ZZZZ.SMP",    # 62 - Mud squelch
    "PICOZZZZ.SMP",    # 63 - Pickaxe
    "PICO1XZZ.SMP",    # 64 - Pickaxe 1
    "PICO2XZZ.SMP",    # 65 - Pickaxe 2
    "PICO3XZZ.SMP",    # 66 - Pickaxe 3
    "RIMSHOTZ.SMP",    # 67 - Rimshot drum
    "RONCOZZZ.SMP",    # 68 - Snoring
    "SORBOZZZ.SMP",    # 69 - Slurp/sip
    "VIENTO1Z.SMP",    # 70 - Wind
    "2ZZZZZZZ.SMP",    # 71 - Sound 2
    "20ZZZZZZ.SMP",    # 72 - Sound 20
    "21ZZZZZZ.SMP",    # 73 - Sound 21
    "23ZZZZZZ.SMP",    # 74 - Sound 23
    "107ZZZZZ.SMP",    # 75 - Sound 107
    "39ZZZZZZ.SMP",    # 76 - Sound 39
    "81ZZZZZZ.SMP",    # 77 - Sound 81
    "88ZZZZZZ.SMP",    # 78 - Sound 88
    "92ZZZZZZ.SMP",    # 79 - Sound 92
    "SAW_2ZZZ.SMP",    # 80 - Saw
    "QUAKE2ZZ.SMP",    # 81 - Earthquake
    "ROCKSZZZ.SMP",    # 82 - Rocks falling
    "IN_FIREZ.SMP",    # 83 - Fire
    "BEAMZZZZ.SMP",    # 84 - Beam/ray
    "GLISSDWN.SMP",    # 85 - Glissando down
    "REMATERL.SMP",    # 86 - Rematerialize
    "FXH1ZZZZ.SMP",    # 87 - Effect 1
    "FXH3ZZZZ.SMP",    # 88 - Effect 3
    "FXH4ZZZZ.SMP",    # 89 - Effect 4
    "MATCHZZZ.SMP",    # 90 - Match strike
    "SURF_01Z.SMP",    # 91 - Surf wave 1
    "SURF_02Z.SMP",    # 92 - Surf wave 2
    "SURF_04Z.SMP",    # 93 - Surf wave 4
    "TWANGZZZ.SMP",    # 94 - Twang
    "LANDCRAS.SMP",    # 95 - Crash landing
    # Extended entries (indices 96+)
]

# CD Audio track names (from executable strings)
CD_TRACK_NAMES = {
    0: "(Silence)",
    1: "Alfred, Sax Machine",
    2: "Alfred's Paradise",
    3: "Alfred Quest",
    4: "Alfred Quest II",
    5: "Alfred goes to Egypt",
    6: "Alfred, Sawed Sax",
    7: "Alfred: Intro 1",
    8: "Alfred: Intro 2",
    9: "Alfred: Intro 3",
}

NUM_ROOMS = 56
ROOM_ENTRY_SIZE = 104  # 13 pairs × 8 bytes
PAIR_9_OFFSET = 9 * 8  # Pair 9 contains sound data offset/size (0x48)


def get_sound_filename(index):
    """Get sound filename for given index, handling out-of-range indices"""
    if index < len(SOUND_FILENAMES):
        return SOUND_FILENAMES[index]
    return f"UNKNOWN_{index}.SMP"


def extract_room_sfx(alfred1_path, room_number=None, output_dir=None):
    """
    Extract SFX mapping for rooms from ALFRED.1

    Args:
        alfred1_path: Path to ALFRED.1 file
        room_number: Specific room to extract (None = all rooms)
        output_dir: Directory for output files (None = print only)

    Returns:
        List of room sound data dictionaries
    """
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    print("=" * 80)
    print("Alfred Pelrock - Room SFX Extractor")
    print("=" * 80)
    print()

    all_rooms = []

    # Determine which rooms to process
    if room_number is not None:
        rooms_to_process = [room_number]
    else:
        rooms_to_process = range(NUM_ROOMS)

    for room_num in rooms_to_process:
        if room_num >= NUM_ROOMS:
            print(f"Error: Room {room_num} out of range (0-{NUM_ROOMS-1})")
            continue

        # Calculate position in room directory
        room_dir_offset = room_num * ROOM_ENTRY_SIZE

        # Get Pair 9 offset and size (sound/music data)
        pair9_ptr = room_dir_offset + PAIR_9_OFFSET
        sound_data_offset = struct.unpack('<I', data[pair9_ptr:pair9_ptr+4])[0]
        sound_data_size = struct.unpack('<I', data[pair9_ptr+4:pair9_ptr+8])[0]

        if sound_data_offset == 0 or sound_data_size < 10:
            print(f"Room {room_num:2d}: No sound data (offset=0x{sound_data_offset:08X}, size={sound_data_size})")
            continue

        # Read sound data (10 bytes: 1 music ID + 9 sound indices)
        music_track_id = data[sound_data_offset]
        sound_indices = list(data[sound_data_offset + 1:sound_data_offset + 10])

        # Map indices to filenames
        sounds = [get_sound_filename(idx) for idx in sound_indices]

        # Count active sounds (non-zero index)
        active_sounds = [(i, idx, sounds[i]) for i, idx in enumerate(sound_indices) if idx != 0]

        room_data = {
            'room': room_num,
            'music_track_id': music_track_id,
            'music_track_name': CD_TRACK_NAMES.get(music_track_id, f"Track {music_track_id}"),
            'sound_data_offset': sound_data_offset,
            'sound_indices': sound_indices,
            'sounds': sounds,
            'active_count': len(active_sounds),
        }
        all_rooms.append(room_data)

        # Print room info
        track_name = CD_TRACK_NAMES.get(music_track_id, f"Track {music_track_id}")
        print(f"Room {room_num:2d}: Music={music_track_id} ({track_name})")
        print(f"         Data at 0x{sound_data_offset:08X}, {len(active_sounds)} active sound(s)")

        if active_sounds:
            for slot, idx, filename in active_sounds:
                print(f"         Slot {slot}: [{idx:3d}] {filename}")
        print()

    # Save output if requested
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save as detailed text report
        txt_file = output_path / "room_sfx_report.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("Alfred Pelrock - Room Sound Effects Report\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated from: {alfred1_path}\n")
            f.write(f"Total rooms: {len(all_rooms)}\n")
            f.write("=" * 80 + "\n\n")

            for room in all_rooms:
                f.write(f"Room {room['room']:2d}\n")
                f.write(f"  Music Track: {room['music_track_id']} - {room['music_track_name']}\n")
                f.write(f"  Data Offset: 0x{room['sound_data_offset']:08X}\n")
                f.write(f"  Active Sounds: {room['active_count']}/9\n")
                f.write("  Sound Slots:\n")
                for i, (idx, filename) in enumerate(zip(room['sound_indices'], room['sounds'])):
                    status = "ACTIVE" if idx != 0 else "off"
                    f.write(f"    [{i}] Index {idx:3d}: {filename:16s} ({status})\n")
                f.write("\n")

        print(f"Saved report to: {txt_file}")

        # Save as Python module
        py_file = output_path / "room_sfx_data.py"
        with open(py_file, 'w', encoding='utf-8') as f:
            f.write('"""Alfred Pelrock - Room Sound Effects Data"""\n\n')
            f.write("# Sound filename lookup table\n")
            f.write("SOUND_FILENAMES = [\n")
            for i, name in enumerate(SOUND_FILENAMES):
                f.write(f'    "{name}",  # {i}\n')
            f.write("]\n\n")

            f.write("# CD Audio track names\n")
            f.write("CD_TRACK_NAMES = {\n")
            for tid, name in sorted(CD_TRACK_NAMES.items()):
                f.write(f'    {tid}: "{name}",\n')
            f.write("}\n\n")

            f.write("# Room sound effect configuration\n")
            f.write("# Keys: room number\n")
            f.write("# Values: dict with music_track_id and sound_indices (9 slots)\n")
            f.write("ROOM_SFX = {\n")
            for room in all_rooms:
                f.write(f"    {room['room']}: {{\n")
                f.write(f"        'music_track_id': {room['music_track_id']},\n")
                f.write(f"        'sound_indices': {room['sound_indices']},\n")
                f.write(f"    }},\n")
            f.write("}\n")

        print(f"Saved Python data to: {py_file}")

        # Save as JSON
        import json
        json_file = output_path / "room_sfx_data.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'sound_filenames': SOUND_FILENAMES,
                'cd_track_names': CD_TRACK_NAMES,
                'rooms': {room['room']: {
                    'music_track_id': room['music_track_id'],
                    'music_track_name': room['music_track_name'],
                    'sound_indices': room['sound_indices'],
                    'sounds': room['sounds'],
                } for room in all_rooms}
            }, f, indent=2)

        print(f"Saved JSON data to: {json_file}")

    print()
    print("=" * 80)
    print(f"Processed {len(all_rooms)} rooms")

    return all_rooms


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract room SFX (ambient sound effects) from Alfred Pelrock's ALFRED.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python extract_room_sfx.py files/ALFRED.1
  python extract_room_sfx.py files/ALFRED.1 --room 5
  python extract_room_sfx.py files/ALFRED.1 --output sfx_data/
  python extract_room_sfx.py files/ALFRED.1 --room 2 --output sfx_data/
        """
    )
    parser.add_argument('alfred1', help='Path to ALFRED.1 file')
    parser.add_argument('--room', '-r', type=int, help='Extract specific room only (0-55)')
    parser.add_argument('--output', '-o', help='Output directory for reports')

    args = parser.parse_args()

    if not Path(args.alfred1).exists():
        print(f"Error: File not found: {args.alfred1}")
        sys.exit(1)

    extract_room_sfx(args.alfred1, room_number=args.room, output_dir=args.output)


if __name__ == "__main__":
    main()
