#!/usr/bin/env python3
"""
Alfred Pelrock - Ambient Sound System Simulator

This script demonstrates how the original game plays ambient sounds.
Use this as reference for ScummVM implementation.

CORRECTED TIMING v2 (based on empirical observation):
- Screensaver triggers at ~60 seconds with threshold 1090
- Therefore: Game tick rate = 1090 / 60 ≈ 18.17 Hz (NOT 70 Hz!)
- Every tick: 50% random chance AND counter check
- Counter check: (counter & 0x1F) == 0x1F (every 32 ticks)
- Only slots 12-15 are used (room data indices 4-7)
- Mouse movement does NOT affect timing

TIMING MATH:
- 32 ticks / 18.17 Hz = ~1.76 seconds between counter alignments
- With 50% probability = ~3.5 seconds average between attempts
- First sound at ~5 seconds (counter reaches 31 + random delay)

RNG DETAILS:
- Standard ANSI C LCG (same as glibc rand())
- Multiplier: 0x41C64E6D (1103515245)
- Increment: 0x3039 (12345)
- Seed: NOT 0! Game initializes RNG with non-zero seed at startup.
        Likely seeded from DOS timer or system time.
        Empirical testing found seed ~2765 matches observed behavior.
- Formula: state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
- Returns: (state >> 16) & 0x7FFF (15-bit value 0-32767)

NOTE: With seed=0, the sequence is: BIRD→CAT→HORN→CAT→HORN→HORN...
      But observed game behavior was: BIRD→BIRD→CAT→HORN→CAT→BIRD
      This confirms the seed is non-zero. For ScummVM, recommend using
      system time as seed to match original non-deterministic behavior.

SOUND SELECTION:
- Random slot from 12-15: (random() & 3) + 12
- Only 4 of the 9 room sounds are actually ambient sounds!
- Volume: 256 (0x100) for both left and right channels

Usage:
    python ambient_sound_simulator.py --info        # Show all room configs
    python ambient_sound_simulator.py --simulate 0  # Simulate room 0
    python ambient_sound_simulator.py --export      # Export for ScummVM
"""

import struct
import sys
from pathlib import Path


# =============================================================================
# RNG Implementation (exact match of game's ANSI C LCG)
# =============================================================================

class GameRNG:
    """
    Exact implementation of Alfred Pelrock's random number generator.

    This is the standard ANSI C LCG used by glibc rand():
    - Multiplier: 0x41C64E6D (1103515245)
    - Increment: 0x3039 (12345)
    - Modulus: 2^32 (implicit via 32-bit overflow)

    The game stores the state at address 0x0004c3f0 (rng_state).
    Since this is in BSS, it's initialized to 0 on program start.
    """

    # LCG constants (from JUEGO.EXE @ 0x0002b12f)
    MULTIPLIER = 0x41C64E6D  # 1103515245
    INCREMENT = 0x3039       # 12345

    def __init__(self, seed=None):
        """Initialize RNG with seed (default None = use system time like original game)"""
        if seed is None:
            import time
            seed = int(time.time() * 1000) & 0xFFFF  # Low 16 bits of milliseconds
        self.state = seed & 0xFFFFFFFF

    def random(self):
        """
        Generate next random number (0-32767).

        Assembly from 0x0002b12f:
            IMUL EDX, [EAX], 0x41c64e6d
            ADD EDX, 0x3039
            MOV [EAX], EDX
            MOV EAX, EDX
            SHR EAX, 0x10
            AND EAX, 0x7fff
        """
        self.state = (self.state * self.MULTIPLIER + self.INCREMENT) & 0xFFFFFFFF
        return (self.state >> 16) & 0x7FFF

    def get_state(self):
        """Get current RNG state"""
        return self.state

    def set_state(self, state):
        """Set RNG state (for save/load)"""
        self.state = state & 0xFFFFFFFF


# =============================================================================
# Game Constants
# =============================================================================

# Timing (CORRECTED based on empirical observation)
GAME_TICK_HZ = 18.17  # Main game loop frequency (NOT 70 Hz DOS timer!)
RANDOM_THRESHOLD = 0x4000  # 16384 - ~50% probability
COUNTER_MASK = 0x1F  # 31 - check every 32 ticks
AMBIENT_SLOT_OFFSET = 12  # Slots 12-15 used for ambient
AMBIENT_SLOT_COUNT = 4  # Only 4 slots

# RNG seed (NOT 0 - game seeds with system time or similar)
# Empirical testing shows seed ~2765 matches observed behavior
DEFAULT_RNG_SEED = None  # Use system time for ScummVM compatibility

# Sound filename array from JUEGO.EXE at 0x48dd8 (indices 0-95)
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
]

NUM_ROOMS = 56
ROOM_ENTRY_SIZE = 104
PAIR_9_OFFSET = 9 * 8


def get_sound_filename(index):
    """Get sound filename for given index"""
    if index < len(SOUND_FILENAMES):
        return SOUND_FILENAMES[index]
    return f"SOUND_{index}.SMP"


def load_room_sounds(alfred1_path):
    """Load sound mappings for all rooms from ALFRED.1"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    rooms = {}

    for room_num in range(NUM_ROOMS):
        room_dir_offset = room_num * ROOM_ENTRY_SIZE
        pair9_ptr = room_dir_offset + PAIR_9_OFFSET

        sound_data_offset = struct.unpack('<I', data[pair9_ptr:pair9_ptr+4])[0]
        sound_data_size = struct.unpack('<I', data[pair9_ptr+4:pair9_ptr+8])[0]

        if sound_data_offset == 0 or sound_data_size < 10:
            rooms[room_num] = {
                'music_track': 0,
                'sounds': [0] * 9
            }
            continue

        music_track_id = data[sound_data_offset]
        sound_indices = list(data[sound_data_offset + 1:sound_data_offset + 10])

        rooms[room_num] = {
            'music_track': music_track_id,
            'sounds': sound_indices
        }

    return rooms


class AmbientSoundSystem:
    """
    Simulates the original game's ambient sound system with EXACT RNG behavior.

    CORRECTED algorithm based on render_scene disassembly:
    - Every frame: check if random() > 0x4000 (~50%)
    - If yes AND (counter & 0x1F) == 0x1F: play sound
    - Only slots 12-15 (room indices 4-7) are used
    - Mouse movement does NOT reset timer

    RNG: Standard ANSI C LCG with seed=0 (deterministic sequence!)
    """

    def __init__(self, room_sounds, rng_seed=DEFAULT_RNG_SEED):
        self.room_sounds = room_sounds
        self.current_room = 0
        self.frame_counter = 0
        self.rng = GameRNG(rng_seed)  # Use exact game RNG

    def get_ambient_sounds(self, room_num):
        """Get list of ambient sounds for a room (only indices 4-7)"""
        if room_num not in self.room_sounds:
            return []

        sounds = self.room_sounds[room_num]['sounds']
        ambient = []
        # Only indices 4-7 are used for ambient (slots 12-15)
        for i in range(4, 8):
            sound_idx = sounds[i]
            if sound_idx != 0:
                ambient.append({
                    'room_index': i,
                    'slot': i + 8,  # Actual slot number
                    'sound_index': sound_idx,
                    'filename': get_sound_filename(sound_idx)
                })
        return ambient

    def tick(self):
        """
        Called every game tick (~18.17Hz, not 70Hz!).
        Returns sound to play, or None.

        Algorithm from render_scene @ 0x00015eeb:
        1. random() > 0x4000 (50% chance)
        2. (counter & 0x1F) == 0x1F (every 32 ticks)
        3. Pick slot = (random() & 3) + 12

        Uses exact game RNG for deterministic reproduction!
        """
        self.frame_counter += 1

        # 50% random chance (first RNG call)
        rand1 = self.rng.random()
        if rand1 <= RANDOM_THRESHOLD:
            return None

        # Counter alignment check
        if (self.frame_counter & COUNTER_MASK) != COUNTER_MASK:
            return None

        # Pick random slot 12-15 (second RNG call)
        rand2 = self.rng.random()
        slot_offset = rand2 & 3
        room_data_index = slot_offset + 4

        sounds = self.room_sounds.get(self.current_room, {}).get('sounds', [0] * 9)
        sound_idx = sounds[room_data_index] if room_data_index < len(sounds) else 0

        if sound_idx == 0:
            return None

        return {
            'room_index': room_data_index,
            'slot': room_data_index + 8,
            'sound_index': sound_idx,
            'filename': get_sound_filename(sound_idx)
        }

    def change_room(self, room_num):
        """Called when entering a new room"""
        self.current_room = room_num
        # Note: Frame counter is NOT reset on room change


def print_room_sound_config(rooms):
    """Print sound configuration for all rooms"""
    print("=" * 80)
    print("ALFRED PELROCK - ROOM AMBIENT SOUND CONFIGURATION (CORRECTED)")
    print("=" * 80)
    print()
    print("TIMING SYSTEM (from render_scene @ 0x00015eeb):")
    print(f"  - Game tick rate: {GAME_TICK_HZ} Hz (NOT 70 Hz!)")
    print(f"  - Random threshold: 0x{RANDOM_THRESHOLD:04X} (~50% chance per tick)")
    print(f"  - Counter mask: 0x{COUNTER_MASK:02X} (check every 32 ticks)")
    print(f"  - Result: ~3.5 second average intervals")
    print(f"  - Mouse movement does NOT affect timing")
    print()
    print("RNG SYSTEM (from random_number_generator @ 0x0002b12f):")
    print(f"  - Algorithm: ANSI C LCG (glibc rand())")
    print(f"  - Multiplier: 0x{GameRNG.MULTIPLIER:08X}")
    print(f"  - Increment: 0x{GameRNG.INCREMENT:04X}")
    print(f"  - Seed: {DEFAULT_RNG_SEED} (BSS initialized to zero)")
    print(f"  - State address: 0x0004c3f0 (rng_state)")
    print(f"  - DETERMINISTIC: Same sounds play in same order every game!")
    print()
    print("IMPORTANT: Only room data indices 4-7 (slots 12-15) are ambient sounds!")
    print()
    print("=" * 80)
    print()

    for room_num in range(NUM_ROOMS):
        room = rooms[room_num]
        sounds = room['sounds']

        print(f"Room {room_num:2d}: Music Track {room['music_track']}")
        print(f"  All 9 slots: {sounds}")

        # Show ambient slots specifically
        ambient = []
        for i in range(4, 8):
            idx = sounds[i]
            if idx != 0:
                ambient.append(f"[{i}]={get_sound_filename(idx)}")

        if ambient:
            print(f"  AMBIENT (slots 12-15): {', '.join(ambient)}")
        else:
            print(f"  AMBIENT: (none)")
        print()


def simulate_ambient_sounds(rooms, room_num, duration_seconds=60):
    """
    Simulate ambient sound playback for a room.
    Shows when sounds would play with the corrected algorithm.
    """
    print(f"\n{'='*60}")
    print(f"SIMULATING ROOM {room_num} - {duration_seconds}s")
    print(f"{'='*60}")

    system = AmbientSoundSystem(rooms)
    system.change_room(room_num)

    ambient = system.get_ambient_sounds(room_num)
    print(f"\nAmbient sounds in room (indices 4-7 only):")
    for s in ambient:
        print(f"  Index {s['room_index']} (Slot {s['slot']}): {s['filename']}")

    if not ambient:
        print("\nNo ambient sounds in this room.")
        return

    print(f"\nSound events (simulated {duration_seconds}s):")
    print("-" * 40)

    total_ticks = int(duration_seconds * GAME_TICK_HZ)
    sound_events = []
    last_sound_time = 0

    for tick in range(total_ticks):
        sound = system.tick()
        if sound:
            time_sec = tick / GAME_TICK_HZ
            interval = time_sec - last_sound_time
            sound_events.append((time_sec, sound, interval))
            print(f"  {time_sec:6.2f}s (+{interval:4.2f}s): {sound['filename']}")
            last_sound_time = time_sec

    print("-" * 40)
    print(f"Total sounds in {duration_seconds}s: {len(sound_events)}")

    if sound_events:
        intervals = [e[2] for e in sound_events[1:]]  # Skip first (no interval)
        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            print(f"Average interval: {avg_interval:.2f}s")


def export_scummvm_config(rooms, output_file):
    """Export room sound config in a format suitable for ScummVM"""

    lines = [
        "// Alfred Pelrock - Room Ambient Sound Configuration",
        "// Auto-generated for ScummVM implementation",
        "//",
        "// CORRECTED TIMING v2 (from render_scene disassembly + empirical observation):",
        "// - Every tick (~18.17Hz, NOT 70Hz!): 50% random chance",
        "// - If random passes AND (counter & 0x1F) == 0x1F: play sound",
        "// - Only slots 12-15 (room indices 4-7) are ambient sounds",
        "// - Mouse movement does NOT affect timing",
        "// - Screensaver triggers at 1090 ticks = ~60 seconds",
        "//",
        "// RNG: Standard ANSI C LCG (glibc rand())",
        "// - Multiplier: 0x41C64E6D (1103515245)",
        "// - Increment: 0x3039 (12345)",
        "// - Seed: 0 (BSS initialized - DETERMINISTIC SEQUENCE!)",
        "// - Formula: state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF",
        "// - Returns: (state >> 16) & 0x7FFF",
        "//",
        f"// #define GAME_TICK_HZ              {GAME_TICK_HZ}",
        f"// #define AMBIENT_RANDOM_THRESHOLD  0x{RANDOM_THRESHOLD:04X}",
        f"// #define AMBIENT_COUNTER_MASK     0x{COUNTER_MASK:02X}",
        f"// #define RNG_MULTIPLIER           0x{GameRNG.MULTIPLIER:08X}",
        f"// #define RNG_INCREMENT            0x{GameRNG.INCREMENT:04X}",
        f"// #define RNG_INITIAL_SEED         {DEFAULT_RNG_SEED}",
        "//",
        "// Average interval: ~3.5 seconds (32 ticks / 18.17 Hz * 2 for 50% probability)",
        "",
        "struct RoomAmbientSound {",
        "    uint8 musicTrack;",
        "    uint8 allSlots[9];      // All 9 sound indices",
        "    // Note: Only indices 4-7 are ambient sounds (slots 12-15)",
        "};",
        "",
        "static const RoomAmbientSound ROOM_SOUNDS[] = {",
    ]

    for room_num in range(NUM_ROOMS):
        room = rooms[room_num]
        slots_str = ", ".join(f"{s:2d}" for s in room['sounds'])
        lines.append(f"    /* Room {room_num:2d} */ {{ {room['music_track']:2d}, {{ {slots_str} }} }},")

    lines.append("};")
    lines.append("")
    lines.append("// Ambient slots are indices 4-7 (slots 12-15)")
    lines.append("// Access: ROOM_SOUNDS[room].allSlots[4..7]")
    lines.append("")
    lines.append("// Sound filename lookup table")
    lines.append("static const char* SOUND_FILENAMES[] = {")

    for i, fname in enumerate(SOUND_FILENAMES):
        stem = Path(fname).stem
        lines.append(f'    /* {i:2d} */ "{stem}.wav",')

    lines.append("};")

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Exported ScummVM config to: {output_file}")


def analyze_rng_sequence(rooms, room_num=0, num_sounds=10):
    """
    Analyze the deterministic RNG sequence for a room.

    Shows exactly which sounds will play and when, given the
    fixed RNG seed of 0. This explains why the game always
    starts with the same sound sequence!
    """
    print(f"\n{'='*70}")
    print(f"RNG SEQUENCE ANALYSIS - Room {room_num}")
    print(f"{'='*70}")
    print()
    print("RNG Implementation: ANSI C LCG (glibc rand())")
    print(f"  Multiplier: 0x41C64E6D (1103515245)")
    print(f"  Increment:  0x3039 (12345)")
    print(f"  Seed:       0 (BSS initialized)")
    print()

    room_sounds = rooms.get(room_num, {}).get('sounds', [0] * 9)
    ambient_sounds = room_sounds[4:8]  # Indices 4-7

    print(f"Room {room_num} ambient sounds (indices 4-7):")
    slot_names = []
    for i, idx in enumerate(ambient_sounds):
        name = get_sound_filename(idx) if idx != 0 else "(empty)"
        slot_names.append(name)
        print(f"  Slot {i}: index {idx} = {name}")
    print()

    # Simulate with exact RNG
    rng = GameRNG(0)
    frame_counter = 0
    triggers = []

    print(f"First {num_sounds} sound triggers (deterministic!):")
    print("-" * 70)
    print(f"{'Tick':>6} {'Time':>8} {'RNG1':>7} {'RNG2':>7} {'Slot':>5} {'Sound':<20}")
    print("-" * 70)

    while len(triggers) < num_sounds:
        frame_counter += 1

        # First RNG call for 50% gate
        rand1 = rng.random()

        if rand1 > RANDOM_THRESHOLD:
            if (frame_counter & COUNTER_MASK) == COUNTER_MASK:
                # Second RNG call for slot selection
                rand2 = rng.random()
                slot = rand2 & 3
                sound_idx = ambient_sounds[slot]
                sound_name = slot_names[slot]
                time_sec = frame_counter / GAME_TICK_HZ

                triggers.append({
                    'tick': frame_counter,
                    'time': time_sec,
                    'rand1': rand1,
                    'rand2': rand2,
                    'slot': slot,
                    'sound': sound_name
                })

                print(f"{frame_counter:6d} {time_sec:7.2f}s {rand1:7d} {rand2:7d} {slot:5d} {sound_name:<20}")

    print("-" * 70)
    print()
    print("CONCLUSION:")
    print("The sound sequence is DETERMINISTIC because the RNG seed is always 0!")
    print("The same sounds will play in the same order every time the game starts.")
    print()

    # Show the pattern
    pattern = [t['sound'] for t in triggers[:5]]
    print(f"First 5 sounds: {' -> '.join(pattern)}")


def main():
    alfred1_path = "files/ALFRED.1"

    if not Path(alfred1_path).exists():
        print(f"Error: {alfred1_path} not found")
        sys.exit(1)

    rooms = load_room_sounds(alfred1_path)

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExamples:")
        print("  python ambient_sound_simulator.py --info        # Show all room configs")
        print("  python ambient_sound_simulator.py --simulate 0  # Simulate room 0")
        print("  python ambient_sound_simulator.py --analyze 0   # Analyze RNG sequence")
        print("  python ambient_sound_simulator.py --export      # Export for ScummVM")
        sys.exit(0)

    if sys.argv[1] == '--info':
        print_room_sound_config(rooms)

    elif sys.argv[1] == '--simulate':
        room_num = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        simulate_ambient_sounds(rooms, room_num, duration)

    elif sys.argv[1] == '--analyze':
        room_num = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        num_sounds = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        analyze_rng_sequence(rooms, room_num, num_sounds)

    elif sys.argv[1] == '--export':
        output = sys.argv[2] if len(sys.argv) > 2 else "scummvm_ambient_sounds.h"
        export_scummvm_config(rooms, output)

    else:
        try:
            room_num = int(sys.argv[1])
            simulate_ambient_sounds(rooms, room_num)
        except ValueError:
            print(f"Unknown option: {sys.argv[1]}")
            sys.exit(1)


if __name__ == "__main__":
    main()
