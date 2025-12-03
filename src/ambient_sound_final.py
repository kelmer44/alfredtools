#!/usr/bin/env python3
"""
Alfred Pelrock - Ambient Sound System Simulator (Final Version)

This script accurately simulates the original game's ambient sound system.
Use this as reference for ScummVM implementation.

ALGORITHM (from render_scene @ 0x00015eeb):
1. Timer ISR increments counter at ~18.2 Hz
2. Every frame: call random() and check if > 0x4000 (~50%)
3. If pass AND (counter & 0x1F) == 0x1F: trigger sound
4. Pick slot: (random() & 3) + 12 -> slots 12-15

RNG: Standard ANSI C LCG (glibc rand())
- Multiplier: 0x41C64E6D (1103515245)
- Increment: 0x3039 (12345)
- State: 0x0004c3f0 (BSS section)

SEED OPTIONS:
- seed=0: Clean predictable behavior (different from DOSBox)
- seed=3515: Approximates original DOSBox behavior
- seed=None: Random seed for varied sequences

Usage:
    python ambient_sound_final.py                     # Show help
    python ambient_sound_final.py --simulate 0        # Simulate room 0 (random seed)
    python ambient_sound_final.py --simulate 0 --seed 0      # Seed 0
    python ambient_sound_final.py --simulate 0 --seed 3515   # DOSBox-like
    python ambient_sound_final.py --compare           # Compare seed behaviors
    python ambient_sound_final.py --export            # Export for ScummVM
"""

import struct
import sys
import argparse
from pathlib import Path


# =============================================================================
# Constants
# =============================================================================

# RNG constants (from JUEGO.EXE @ 0x0002b12f)
RNG_MULTIPLIER = 0x41C64E6D  # 1103515245
RNG_INCREMENT = 0x3039       # 12345

# Timing constants
TICK_RATE = 18.2             # DOS timer ISR rate (Hz)
RNG_THRESHOLD = 0x4000       # 16384 (~50% pass rate)
COUNTER_MASK = 0x1F          # Check every 32 ticks

# Slot mapping (room data indices 4-7 -> slots 12-15)
AMBIENT_SLOT_OFFSET = 12

# Known good seeds
SEED_CLEAN = 0               # Clean slate, different from DOSBox
SEED_DOSBOX = 3515           # Approximates original DOSBox behavior

# Sound filename table
SOUND_FILENAMES = [
    "NO_SOUND.SMP", "BUHO_ZZZ.SMP", "BIRD_1_1.SMP", "BIRD_1_2.SMP",
    "BIRD_1_3.SMP", "DESPERZZ.SMP", "HORN_5ZZ.SMP", "HORN_6ZZ.SMP",
    "HORN_8ZZ.SMP", "SUZIPASS.SMP", "CAT_1ZZZ.SMP", "DOG_01ZZ.SMP",
    "DOG_02ZZ.SMP", "DOG_04ZZ.SMP", "DOG_05ZZ.SMP", "DOG_06ZZ.SMP",
    "DOG_07ZZ.SMP", "DOG_09ZZ.SMP", "ALARMZZZ.SMP", "AMBULAN1.SMP",
    "FOUNTAIN.SMP", "GRILLOSZ.SMP", "HOJASZZZ.SMP", "FLASHZZZ.SMP",
    "CUCHI1ZZ.SMP", "KNRRRRRZ.SMP", "PHONE_02.SMP", "PHONE_03.SMP",
    "SSSHTZZZ.SMP", "BURGUER1.SMP", "FLIES_2Z.SMP", "PARRILLA.SMP",
    "WATER_2Z.SMP", "XIQUETZZ.SMP", "RONQUIZZ.SMP", "MOCO1ZZZ.SMP",
    "MOCO2ZZZ.SMP", "SPRINGZZ.SMP", "MARUJASZ.SMP", "ELECTROZ.SMP",
    "GLASS1ZZ.SMP", "OPDOORZZ.SMP", "CLDOORZZ.SMP", "FXH2ZZZZ.SMP",
    "BOTEZZZZ.SMP", "ELEC3ZZZ.SMP",
]

# Human-readable names for common sounds
SOUND_NAMES = {
    0: "NONE", 2: "BIRD", 3: "BIRD", 4: "BIRD",
    7: "HORN", 8: "HORN", 10: "CAT", 11: "DOG",
}


# =============================================================================
# RNG Implementation
# =============================================================================

class GameRNG:
    """Exact implementation of Alfred Pelrock's ANSI C LCG random number generator."""

    def __init__(self, seed=0):
        self.state = seed & 0xFFFFFFFF

    def random(self):
        """Generate next random number (0-32767)."""
        self.state = (self.state * RNG_MULTIPLIER + RNG_INCREMENT) & 0xFFFFFFFF
        return (self.state >> 16) & 0x7FFF

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state & 0xFFFFFFFF


# =============================================================================
# Room Data
# =============================================================================

def load_room_sounds(alfred1_path):
    """Load sound mappings for all rooms from ALFRED.1"""
    with open(alfred1_path, 'rb') as f:
        data = f.read()

    rooms = {}
    for room_num in range(56):
        room_dir_offset = room_num * 104
        pair9_ptr = room_dir_offset + 9 * 8

        sound_data_offset = struct.unpack('<I', data[pair9_ptr:pair9_ptr+4])[0]
        sound_data_size = struct.unpack('<I', data[pair9_ptr+4:pair9_ptr+8])[0]

        if sound_data_offset == 0 or sound_data_size < 10:
            rooms[room_num] = {'music_track': 0, 'sounds': [0] * 9}
            continue

        music_track_id = data[sound_data_offset]
        sound_indices = list(data[sound_data_offset + 1:sound_data_offset + 10])
        rooms[room_num] = {'music_track': music_track_id, 'sounds': sound_indices}

    return rooms


def get_sound_name(idx):
    """Get human-readable sound name."""
    if idx in SOUND_NAMES:
        return SOUND_NAMES[idx]
    if idx < len(SOUND_FILENAMES):
        return SOUND_FILENAMES[idx].replace('.SMP', '').replace('_', '')[:8]
    return f"SND{idx}"


def get_sound_filename(idx):
    """Get sound filename."""
    if idx < len(SOUND_FILENAMES):
        return SOUND_FILENAMES[idx]
    return f"SOUND_{idx}.SMP"


# =============================================================================
# Simulator
# =============================================================================

class AmbientSoundSimulator:
    """
    Simulates the ambient sound system with exact RNG behavior.

    The algorithm:
    1. Timer ISR increments counter at ~18.2 Hz
    2. Each frame: RNG called, check if > 0x4000
    3. If pass AND (counter & 0x1F) == 0x1F: play sound
    4. Slot = (random() & 3) + 12
    """

    def __init__(self, room_sounds, seed=0):
        self.room_sounds = room_sounds
        self.rng = GameRNG(seed)
        self.counter = 0
        self.tick = 0
        self.current_room = 0

    def get_ambient_sounds(self, room_num):
        """Get ambient sounds for room (indices 4-7 only)."""
        if room_num not in self.room_sounds:
            return [0, 0, 0, 0]
        return self.room_sounds[room_num]['sounds'][4:8]

    def simulate_until_sounds(self, max_time=30.0, max_sounds=10):
        """Simulate and return list of sound triggers."""
        sounds = []
        ambient = self.get_ambient_sounds(self.current_room)

        while len(sounds) < max_sounds and self.tick / TICK_RATE < max_time:
            # Timer ISR increments counter
            self.counter = (self.counter + 1) & 0xFFFFFFFF
            current_time = self.tick / TICK_RATE

            # RNG gate check (every frame)
            rng_val = self.rng.random()
            if rng_val > RNG_THRESHOLD:
                # Counter alignment check
                if (self.counter & COUNTER_MASK) == COUNTER_MASK:
                    # Trigger! Increment counter and select slot
                    self.counter = (self.counter + 1) & 0xFFFFFFFF
                    slot_rng = self.rng.random()
                    slot_offset = slot_rng & 3
                    sound_idx = ambient[slot_offset]

                    if sound_idx != 0:
                        sounds.append({
                            'time': current_time,
                            'tick': self.tick,
                            'slot': slot_offset + 12,
                            'sound_idx': sound_idx,
                            'sound_name': get_sound_name(sound_idx),
                            'filename': get_sound_filename(sound_idx),
                        })

            self.tick += 1

        return sounds

    def change_room(self, room_num):
        """Change current room (counter is NOT reset)."""
        self.current_room = room_num


# =============================================================================
# Commands
# =============================================================================

def cmd_simulate(rooms, room_num, seed, duration, count):
    """Simulate ambient sounds for a room."""
    print(f"\n{'='*60}")
    print(f"SIMULATING ROOM {room_num}")
    print(f"Seed: {seed}, Duration: {duration}s, Max sounds: {count}")
    print(f"{'='*60}")

    ambient = rooms.get(room_num, {}).get('sounds', [0]*9)[4:8]
    print(f"\nAmbient slots (indices 4-7):")
    for i, idx in enumerate(ambient):
        name = get_sound_name(idx) if idx != 0 else "(empty)"
        print(f"  Slot {i+12}: index {idx:2d} = {name}")

    if all(idx == 0 for idx in ambient):
        print("\nNo ambient sounds in this room.")
        return

    sim = AmbientSoundSimulator(rooms, seed=seed)
    sim.change_room(room_num)
    sounds = sim.simulate_until_sounds(max_time=duration, max_sounds=count)

    print(f"\nSound triggers:")
    print("-" * 50)
    prev_time = 0
    for s in sounds:
        gap = s['time'] - prev_time
        print(f"  {s['time']:6.1f}s (+{gap:4.1f}s): {s['sound_name']:6s} (slot {s['slot']}, idx {s['sound_idx']})")
        prev_time = s['time']

    print("-" * 50)
    print(f"Total: {len(sounds)} sounds")

    # Show sequence
    seq = [s['sound_name'] for s in sounds]
    print(f"\nSequence: {' → '.join(seq)}")


def cmd_compare(rooms, room_num=0):
    """Compare different seed behaviors."""
    print(f"\n{'='*60}")
    print(f"SEED COMPARISON - Room {room_num}")
    print(f"{'='*60}")

    # User's observed sequence
    print("\nTarget (observed from DOSBox):")
    print("  Sequence: BIRD → BIRD → CAT → HORN → CAT → BIRD")
    print("  Times:    ~5s, ~9s, ~10s, ~15s, ~19s, ~24s")

    seeds_to_test = [
        (0, "Clean slate (BSS=0)"),
        (3515, "DOSBox approximation"),
    ]

    for seed, description in seeds_to_test:
        print(f"\nSeed {seed} ({description}):")
        sim = AmbientSoundSimulator(rooms, seed=seed)
        sim.change_room(room_num)
        sounds = sim.simulate_until_sounds(max_time=30.0, max_sounds=6)

        seq = [s['sound_name'] for s in sounds]
        times = [f"{s['time']:.1f}" for s in sounds]
        print(f"  Sequence: {' → '.join(seq)}")
        print(f"  Times:    {', '.join(times)}s")


def cmd_export(rooms, output_file):
    """Export ScummVM configuration header."""
    lines = [
        "// Alfred Pelrock - Ambient Sound System Configuration",
        "// Auto-generated for ScummVM implementation",
        "//",
        "// Algorithm (render_scene @ 0x00015eeb):",
        "// 1. Timer ISR increments counter at ~18.2 Hz",
        "// 2. Each frame: RNG called, check if > 0x4000 (~50%)",
        "// 3. If pass AND (counter & 0x1F) == 0x1F: trigger",
        "// 4. Slot = (random() & 3) + 12 -> slots 12-15",
        "//",
        "// RNG: ANSI C LCG (glibc rand())",
        f"// #define RNG_MULTIPLIER           0x{RNG_MULTIPLIER:08X}",
        f"// #define RNG_INCREMENT            0x{RNG_INCREMENT:04X}",
        f"// #define TICK_RATE                {TICK_RATE}",
        f"// #define RNG_THRESHOLD            0x{RNG_THRESHOLD:04X}",
        f"// #define COUNTER_MASK             0x{COUNTER_MASK:02X}",
        "//",
        "// Seed options:",
        f"// #define SEED_CLEAN               {SEED_CLEAN}     // Predictable",
        f"// #define SEED_DOSBOX              {SEED_DOSBOX}  // DOSBox-like",
        "",
        "struct RoomSoundConfig {",
        "    uint8_t musicTrack;",
        "    uint8_t slots[9];  // indices 4-7 are ambient (slots 12-15)",
        "};",
        "",
        "static const RoomSoundConfig ROOM_SOUNDS[] = {",
    ]

    for room_num in range(56):
        room = rooms.get(room_num, {'music_track': 0, 'sounds': [0]*9})
        slots_str = ", ".join(f"{s:2d}" for s in room['sounds'])
        lines.append(f"    /* Room {room_num:2d} */ {{ {room['music_track']:2d}, {{ {slots_str} }} }},")

    lines.append("};")
    lines.append("")
    lines.append("static const char* SOUND_FILES[] = {")
    for i, fname in enumerate(SOUND_FILENAMES):
        lines.append(f'    /* {i:2d} */ "{fname}",')
    lines.append("};")

    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))

    print(f"Exported to: {output_file}")


def cmd_info(rooms):
    """Show room information."""
    print("\n" + "="*70)
    print("ROOM AMBIENT SOUND CONFIGURATION")
    print("="*70)

    for room_num in range(56):
        room = rooms.get(room_num, {'music_track': 0, 'sounds': [0]*9})
        ambient = room['sounds'][4:8]

        if any(idx != 0 for idx in ambient):
            ambient_names = [get_sound_name(idx) if idx != 0 else "-" for idx in ambient]
            print(f"Room {room_num:2d}: Music {room['music_track']:2d}, Ambient: {', '.join(ambient_names)}")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Alfred Pelrock Ambient Sound Simulator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --simulate 0                    Simulate room 0 with seed=0
  %(prog)s --simulate 0 --seed 3515        Use DOSBox-like seed
  %(prog)s --compare                       Compare seed behaviors
  %(prog)s --export                        Export ScummVM config
  %(prog)s --info                          Show all room configs

Seed options:
  0      Clean predictable behavior
  3515   Approximates original DOSBox behavior
        """
    )

    parser.add_argument('--simulate', type=int, metavar='ROOM',
                       help='Simulate ambient sounds for room')
    parser.add_argument('--seed', type=int, default=0,
                       help='RNG seed (default: 0)')
    parser.add_argument('--duration', type=int, default=30,
                       help='Simulation duration in seconds (default: 30)')
    parser.add_argument('--count', type=int, default=10,
                       help='Max sounds to simulate (default: 10)')
    parser.add_argument('--compare', action='store_true',
                       help='Compare different seed behaviors')
    parser.add_argument('--export', type=str, nargs='?', const='scummvm_ambient_config.h',
                       help='Export ScummVM configuration')
    parser.add_argument('--info', action='store_true',
                       help='Show room configurations')
    parser.add_argument('--alfred1', type=str, default='files/ALFRED.1',
                       help='Path to ALFRED.1 file')

    args = parser.parse_args()

    if not Path(args.alfred1).exists():
        print(f"Error: {args.alfred1} not found")
        sys.exit(1)

    rooms = load_room_sounds(args.alfred1)

    if args.simulate is not None:
        cmd_simulate(rooms, args.simulate, args.seed, args.duration, args.count)
    elif args.compare:
        cmd_compare(rooms)
    elif args.export:
        cmd_export(rooms, args.export)
    elif args.info:
        cmd_info(rooms)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
