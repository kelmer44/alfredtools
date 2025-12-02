#!/usr/bin/env python3
"""
Alfred Pelrock - Ambient Sound System Simulator

This script demonstrates how the original game plays ambient sounds.
Use this as reference for ScummVM implementation.

TIMING CONSTANTS (from reverse engineering):
- Game runs at ~70 Hz (DOS timer)  
- Ambient sound timer threshold: 0x442 (1090 ticks)
- 1090 ticks / 70 Hz = ~15.57 seconds between ambient sounds when idle
- Timer resets on ANY mouse movement

SOUND SELECTION:
- Each room has 9 ambient sound slots (indices 0-8)
- Slot 0 means "no sound" (NO_SOUND.SMP)
- When timer triggers, a random available slot is selected
- Volume: 256 (0x100) for both left and right channels (stereo center)

Usage:
    python ambient_sound_simulator.py [room_number]
    python ambient_sound_simulator.py --extract-all
"""

import struct
import random
import time
import sys
from pathlib import Path


# Constants from reverse engineering
GAME_TIMER_HZ = 70  # DOS timer interrupt rate
AMBIENT_TIMER_THRESHOLD = 0x442  # 1090 decimal
IDLE_ANIM_THRESHOLD = 0x12C  # 300 decimal

# Calculate real-world timing
AMBIENT_INTERVAL_SECONDS = AMBIENT_TIMER_THRESHOLD / GAME_TIMER_HZ  # ~15.57 seconds

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
    "FLASHZZZ.SMP",    # 23 - Flash/camera (placeholder - 100 bytes)
    "CUCHI1ZZ.SMP",    # 24 - Knife 1
    "KNRRRRRZ.SMP",    # 25 - Snoring
    "PHONE_02.SMP",    # 26 - Phone ring 2
    "PHONE_03.SMP",    # 27 - Phone ring 3
    "SSSHTZZZ.SMP",    # 28 - Shush/quiet
    "BURGUER1.SMP",    # 29 - Burger sizzle
    "FLIES_2Z.SMP",    # 30 - Flies buzzing
    "PARRILLA.SMP",    # 31 - Grill (placeholder - 100 bytes)
    "WATER_2Z.SMP",    # 32 - Water
    "XIQUETZZ.SMP",    # 33 - Whistle (placeholder - 100 bytes)
    "RONQUIZZ.SMP",    # 34 - Snoring (not in SONIDOS.DAT)
    "MOCO1ZZZ.SMP",    # 35 - Snot/mucus 1
    "MOCO2ZZZ.SMP",    # 36 - Snot/mucus 2
    "SPRINGZZ.SMP",    # 37 - Spring bounce
    "MARUJASZ.SMP",    # 38 - Gossip/chatter (placeholder - 100 bytes)
    "ELECTROZ.SMP",    # 39 - Electric shock (not in SONIDOS.DAT)
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
                'sounds': [0] * 9  # All empty
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
    Simulates the original game's ambient sound system.
    
    For ScummVM implementation, you need:
    1. A timer that increments each game tick (~70Hz)
    2. Reset timer to 0 on any mouse movement
    3. When timer > 1090, play random sound and reset timer
    """
    
    def __init__(self, room_sounds):
        self.room_sounds = room_sounds
        self.current_room = 0
        self.ambient_timer = 0
        self.idle_timer = 0
        self.last_mouse_pos = (0, 0)
        
    def get_active_sounds(self, room_num):
        """Get list of non-empty sound slots for a room"""
        if room_num not in self.room_sounds:
            return []
        
        sounds = self.room_sounds[room_num]['sounds']
        active = []
        for slot, sound_idx in enumerate(sounds):
            if sound_idx != 0:  # 0 = NO_SOUND
                active.append({
                    'slot': slot,
                    'index': sound_idx,
                    'filename': get_sound_filename(sound_idx)
                })
        return active
    
    def on_mouse_move(self, new_pos):
        """Called when mouse moves - resets both timers"""
        if new_pos != self.last_mouse_pos:
            self.ambient_timer = 0
            self.idle_timer = 0
            self.last_mouse_pos = new_pos
    
    def tick(self):
        """
        Called every game tick (~70Hz).
        Returns sound to play, or None.
        """
        self.ambient_timer += 1
        self.idle_timer += 1
        
        # Check ambient sound timer
        if self.ambient_timer > AMBIENT_TIMER_THRESHOLD:
            self.ambient_timer = 0
            return self.select_random_sound()
        
        return None
    
    def select_random_sound(self):
        """Select a random sound from active slots"""
        active = self.get_active_sounds(self.current_room)
        if not active:
            return None
        
        # Original game uses simple random selection
        selected = random.choice(active)
        return selected
    
    def change_room(self, room_num):
        """Called when entering a new room"""
        self.current_room = room_num
        # Note: Original game does NOT reset timers on room change
        # But new room sounds are loaded


def print_room_sound_config(rooms):
    """Print sound configuration for all rooms"""
    print("=" * 80)
    print("ALFRED PELROCK - ROOM AMBIENT SOUND CONFIGURATION")
    print("=" * 80)
    print()
    print("TIMING SYSTEM:")
    print(f"  - Game tick rate: {GAME_TIMER_HZ} Hz")
    print(f"  - Ambient timer threshold: {AMBIENT_TIMER_THRESHOLD} ticks")
    print(f"  - Real-world interval: {AMBIENT_INTERVAL_SECONDS:.2f} seconds (when idle)")
    print(f"  - Timer resets on mouse movement")
    print()
    print("=" * 80)
    print()
    
    for room_num in range(NUM_ROOMS):
        room = rooms[room_num]
        active = [(i, idx) for i, idx in enumerate(room['sounds']) if idx != 0]
        
        print(f"Room {room_num:2d}: Music Track {room['music_track']}")
        
        if active:
            for slot, idx in active:
                fname = get_sound_filename(idx)
                print(f"    Slot {slot}: [{idx:2d}] {fname}")
        else:
            print(f"    (no ambient sounds)")
        print()


def simulate_ambient_sounds(rooms, room_num, duration_seconds=60):
    """
    Simulate ambient sound playback for a room.
    Shows when sounds would play if player is completely idle.
    """
    print(f"\n{'='*60}")
    print(f"SIMULATING ROOM {room_num} - {duration_seconds}s of idle time")
    print(f"{'='*60}")
    
    system = AmbientSoundSystem(rooms)
    system.change_room(room_num)
    
    active = system.get_active_sounds(room_num)
    print(f"\nActive sounds in room: {len(active)}")
    for s in active:
        print(f"  Slot {s['slot']}: {s['filename']}")
    
    if not active:
        print("\nNo ambient sounds in this room.")
        return
    
    print(f"\nSound events (assuming no mouse movement):")
    print("-" * 40)
    
    total_ticks = int(duration_seconds * GAME_TIMER_HZ)
    sound_events = []
    
    for tick in range(total_ticks):
        sound = system.tick()
        if sound:
            time_sec = tick / GAME_TIMER_HZ
            sound_events.append((time_sec, sound))
            print(f"  {time_sec:6.2f}s: Play {sound['filename']} (slot {sound['slot']})")
    
    print("-" * 40)
    print(f"Total sounds in {duration_seconds}s: {len(sound_events)}")
    expected = duration_seconds / AMBIENT_INTERVAL_SECONDS
    print(f"Expected (theoretical): {expected:.1f}")


def export_scummvm_config(rooms, output_file):
    """Export room sound config in a format suitable for ScummVM"""
    
    lines = [
        "// Alfred Pelrock - Room Ambient Sound Configuration",
        "// Auto-generated for ScummVM implementation",
        "//",
        "// TIMING CONSTANTS:",
        f"// #define AMBIENT_TIMER_HZ       {GAME_TIMER_HZ}",
        f"// #define AMBIENT_TIMER_TICKS    {AMBIENT_TIMER_THRESHOLD}",
        f"// #define AMBIENT_INTERVAL_MS    {int(AMBIENT_INTERVAL_SECONDS * 1000)}",
        "//",
        "// BEHAVIOR:",
        "// - Increment timer each game tick (70Hz / ~14ms)",
        "// - Reset timer to 0 on any mouse movement", 
        "// - When timer > 1090, pick random sound from room's active slots",
        "// - Play sound at volume 256 (center stereo)",
        "// - Reset timer after playing",
        "",
        "struct RoomAmbientSound {",
        "    uint8 musicTrack;",
        "    uint8 soundSlots[9];  // Index into SOUND_FILENAMES, 0 = none",
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
    lines.append("// Sound filename lookup table")
    lines.append("static const char* SOUND_FILENAMES[] = {")
    
    for i, fname in enumerate(SOUND_FILENAMES):
        stem = Path(fname).stem
        lines.append(f'    /* {i:2d} */ "{stem}.wav",')
    
    lines.append("};")
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"Exported ScummVM config to: {output_file}")


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
        print("  python ambient_sound_simulator.py --export      # Export for ScummVM")
        sys.exit(0)
    
    if sys.argv[1] == '--info':
        print_room_sound_config(rooms)
    
    elif sys.argv[1] == '--simulate':
        room_num = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        duration = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        simulate_ambient_sounds(rooms, room_num, duration)
    
    elif sys.argv[1] == '--export':
        output = sys.argv[2] if len(sys.argv) > 2 else "scummvm_ambient_sounds.h"
        export_scummvm_config(rooms, output)
    
    else:
        # Assume it's a room number
        try:
            room_num = int(sys.argv[1])
            simulate_ambient_sounds(rooms, room_num)
        except ValueError:
            print(f"Unknown option: {sys.argv[1]}")
            sys.exit(1)


if __name__ == "__main__":
    main()
