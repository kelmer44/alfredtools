#!/usr/bin/env python3
"""
Alfred Pelrock - Room Sound Extractor

Extracts and converts the actual ambient sound files for a specific room.
Combines room SFX mapping with SONIDOS.DAT extraction.

Usage:
    python extract_room_sounds.py <room_number> [output_dir]
    python extract_room_sounds.py --all [output_dir]
    python extract_room_sounds.py --list  (list all rooms and their sounds)
"""

import struct
import sys
import wave
import shutil
from pathlib import Path


# Sound filename array from JUEGO.EXE at 0x48dd8
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
]

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
ROOM_ENTRY_SIZE = 104
PAIR_9_OFFSET = 9 * 8


def get_sound_filename(index):
    """Get sound filename for given index"""
    if index < len(SOUND_FILENAMES):
        return SOUND_FILENAMES[index]
    return f"UNKNOWN_{index}.SMP"


def detect_format(data):
    """Detect audio format from file header"""
    if len(data) < 16:
        return ('too_small', 11025, 0)

    byte0, byte1 = data[0], data[1]
    magic_4 = data[0:4]

    if magic_4 == b'RIFF':
        sample_rate = struct.unpack('<I', data[0x18:0x1c])[0] if len(data) >= 0x20 else 11025
        if not (4000 <= sample_rate <= 48000):
            sample_rate = 11025
        return ('riff_wav', sample_rate, 0)

    if byte0 == 0x01 and byte1 == 0x2e:
        sample_rate = 11025
        if len(data) >= 0x20:
            rate = struct.unpack('<I', data[0x1c:0x20])[0]
            if 4000 <= rate <= 48000:
                sample_rate = rate
        return ('ail_miles', sample_rate, 80)

    if byte0 == 0x01 and 0x40 <= byte1 <= 0x7f:
        sample_rate = 11025
        if len(data) >= 0x14:
            rate = struct.unpack('<I', data[0x10:0x14])[0]
            if 4000 <= rate <= 48000:
                sample_rate = rate
        return ('ail_other', sample_rate, 80)

    if len(data) <= 100:
        return ('silence', 11025, 0)

    return ('raw_pcm', 11025, 0)


def save_as_wav(pcm_data, output_file, sample_rate):
    """
    Save 8-bit PCM data as WAV file.
    Write data as-is - do NOT convert signed<->unsigned.
    """
    with wave.open(str(output_file), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm_data)


def load_sonidos_index(sonidos_path):
    """Load file index from SONIDOS.DAT"""
    with open(sonidos_path, 'rb') as f:
        data = f.read()

    if data[0:4] != b'PACK':
        raise ValueError(f"Invalid SONIDOS.DAT magic: {data[0:4]}")

    file_count = struct.unpack('<I', data[4:8])[0]

    offset = 8
    files = {}

    for _ in range(file_count):
        name_end = data.find(b'\x00', offset)
        filename = data[offset:name_end].decode('ascii', errors='ignore')
        offset = name_end + 1

        file_offset = struct.unpack('<I', data[offset:offset+4])[0]
        file_size = struct.unpack('<I', data[offset+4:offset+8])[0]
        offset += 8

        files[filename.upper()] = {
            'offset': file_offset,
            'size': file_size,
            'data': data[file_offset:file_offset+file_size]
        }

    return files


def extract_sound_to_wav(sound_name, sonidos_index, output_path):
    """Extract a single sound file and convert to WAV"""
    sound_name_upper = sound_name.upper()

    if sound_name_upper not in sonidos_index:
        return None, f"Not found in SONIDOS.DAT"

    sound_data = sonidos_index[sound_name_upper]['data']

    if len(sound_data) <= 100:
        return None, "Silence/placeholder"

    fmt, sample_rate, header_size = detect_format(sound_data)

    if fmt == 'riff_wav':
        # Already WAV, just copy
        with open(output_path, 'wb') as f:
            f.write(sound_data)
        return output_path, f"RIFF/WAV {sample_rate}Hz"

    if fmt in ('ail_miles', 'ail_other'):
        audio_data = sound_data[header_size:]
    else:
        audio_data = sound_data

    save_as_wav(audio_data, output_path, sample_rate)
    return output_path, f"{fmt} {sample_rate}Hz"


def get_room_sounds(alfred1_data, room_num):
    """Get sound mapping for a room"""
    room_dir_offset = room_num * ROOM_ENTRY_SIZE
    pair9_ptr = room_dir_offset + PAIR_9_OFFSET

    sound_data_offset = struct.unpack('<I', alfred1_data[pair9_ptr:pair9_ptr+4])[0]
    sound_data_size = struct.unpack('<I', alfred1_data[pair9_ptr+4:pair9_ptr+8])[0]

    if sound_data_offset == 0 or sound_data_size < 10:
        return None

    music_track_id = alfred1_data[sound_data_offset]
    sound_indices = list(alfred1_data[sound_data_offset + 1:sound_data_offset + 10])

    return {
        'room_num': room_num,
        'music_track': music_track_id,
        'music_name': CD_TRACK_NAMES.get(music_track_id, f"Track {music_track_id}"),
        'sounds': [(i, idx, get_sound_filename(idx)) for i, idx in enumerate(sound_indices)]
    }


def extract_room_sounds(room_num, output_dir, alfred1_path, sonidos_path):
    """Extract all sounds for a specific room"""
    with open(alfred1_path, 'rb') as f:
        alfred1_data = f.read()

    room_info = get_room_sounds(alfred1_data, room_num)
    if room_info is None:
        print(f"Room {room_num}: No sound data")
        return

    output_path = Path(output_dir) / f"room_{room_num:02d}"
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Room {room_num}")
    print(f"Music: Track {room_info['music_track']} - {room_info['music_name']}")
    print(f"{'='*60}")

    # Load SONIDOS.DAT index
    sonidos_index = load_sonidos_index(sonidos_path)

    # Extract each sound
    extracted = []
    for slot, idx, smp_name in room_info['sounds']:
        if idx == 0 or smp_name == "NO_SOUND.SMP":
            print(f"  Slot {slot}: (empty)")
            continue

        wav_name = Path(smp_name).stem + '.wav'
        out_file = output_path / wav_name

        result, info = extract_sound_to_wav(smp_name, sonidos_index, out_file)

        if result:
            print(f"  Slot {slot}: {smp_name} -> {wav_name} ({info})")
            extracted.append(wav_name)
        else:
            print(f"  Slot {slot}: {smp_name} - SKIP ({info})")

    # Write info file
    info_file = output_path / "room_info.txt"
    with open(info_file, 'w') as f:
        f.write(f"Room {room_num} Ambient Sounds\n")
        f.write(f"{'='*40}\n\n")
        f.write(f"Music Track: {room_info['music_track']} - {room_info['music_name']}\n\n")
        f.write("Ambient Sound Slots:\n")
        for slot, idx, smp_name in room_info['sounds']:
            if idx == 0:
                f.write(f"  Slot {slot}: (empty)\n")
            else:
                f.write(f"  Slot {slot}: {smp_name}\n")
        f.write(f"\nExtracted files: {len(extracted)}\n")

    print(f"\nExtracted {len(extracted)} sound files to: {output_path}")
    return extracted


def list_all_rooms(alfred1_path):
    """List sounds for all rooms"""
    with open(alfred1_path, 'rb') as f:
        alfred1_data = f.read()

    print("="*80)
    print("Alfred Pelrock - Room Sound Mapping")
    print("="*80)

    for room_num in range(NUM_ROOMS):
        room_info = get_room_sounds(alfred1_data, room_num)
        if room_info is None:
            print(f"\nRoom {room_num:2d}: No sound data")
            continue

        active_sounds = [s for s in room_info['sounds'] if s[1] != 0]
        print(f"\nRoom {room_num:2d}: Music={room_info['music_track']} ({room_info['music_name']})")

        if active_sounds:
            for slot, idx, name in active_sounds:
                print(f"    Slot {slot}: [{idx:2d}] {name}")
        else:
            print(f"    (no ambient sounds)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    alfred1_path = "files/ALFRED.1"
    sonidos_path = "files/SONIDOS.DAT"

    if sys.argv[1] == '--list':
        list_all_rooms(alfred1_path)
        return

    if sys.argv[1] == '--all':
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "room_sounds"
        for room_num in range(NUM_ROOMS):
            extract_room_sounds(room_num, output_dir, alfred1_path, sonidos_path)
        return

    try:
        room_num = int(sys.argv[1])
    except ValueError:
        print(f"Error: Invalid room number: {sys.argv[1]}")
        sys.exit(1)

    if room_num < 0 or room_num >= NUM_ROOMS:
        print(f"Error: Room number must be 0-{NUM_ROOMS-1}")
        sys.exit(1)

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "room_sounds"
    extract_room_sounds(room_num, output_dir, alfred1_path, sonidos_path)


if __name__ == "__main__":
    main()
