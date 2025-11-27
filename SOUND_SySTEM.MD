#!/usr/bin/env python3
"""
Alfred Pelrock - Complete Sound System Documentation
Based on Ghidra reverse engineering analysis

AMBIENT SOUND PLAYBACK SYSTEM:
===============================

1. TRIGGER TIMING:
   - Main game loop counter increments every frame (~18-20 FPS)
   - When counter > 0x442 (1090 decimal), ambient sound check occurs
   - Counter resets to 0
   - Approximately every 54-60 seconds at 20 FPS

2. CALL PARAMETERS (at 0x0001073e):

   play_ambient_sound(
       sound_system_ptr,     // Pointer to sound system structure
       slot_index,           // -1 = auto-select, 0-8 = specific slot
       min_delay,            // 0x100 (256 decimal)
       max_delay,            // 0x100 (256 decimal)
       unknown_param,        // 0x20 (32 decimal)
       sound_data_ptr,       // Pointer to loaded sound data
       enabled_flag          // Sound enabled boolean
   )

3. INTERVAL CALCULATION (at 0x00027dd7):

   Formula:
   -------
   interval_ticks = 0xd9300000 / (interval_param * sample_rate)

   Where:
   - 0xd9300000 = 3,643,801,600 (magic timer constant)
   - interval_param = 32 (0x20 from stack parameter)
   - sample_rate = from sound file header (e.g., 11025 Hz)

   Example calculations:
   - At 11025 Hz: 3,643,801,600 / (32 * 11025) = 10,328 ticks
   - At 22050 Hz: 3,643,801,600 / (32 * 22050) = 5,164 ticks

   These ticks are converted to actual playback timing by Miles Sound System.

4. DELAY PARAMETERS:

   Min/Max delay = 256 (0x100)

   Since min == max, sounds play at FIXED intervals, not random.
   The 256 value is likely in game ticks or another time unit.

   At 20 FPS, 256 ticks = 12.8 seconds between sound triggers.

5. SOUND SLOT SELECTION:

   When slot_index = -1 (auto-select):

   a) Searches for first inactive slot (active flag at offset 0x1c == 0)
   b) If all slots active, finds slot with oldest timestamp
   c) Assigns sound to selected slot

   Each slot structure (0x1d bytes = 29 bytes):
   - 0x00: Timestamp (4 bytes)
   - 0x04: Calculated interval timer (4 bytes)
   - 0x08: Min delay (4 bytes) = 0x100
   - 0x0c: Max delay (4 bytes) = 0x100
   - 0x10: Sound buffer pointer (4 bytes)
   - 0x14: Sound control structure pointer (4 bytes)
   - 0x1c: Active flag (1 byte)

6. LOOP BEHAVIOR:

   Sounds DO NOT loop within the file. Instead:
   - Sound plays once
   - After calculated interval, sound is retriggered
   - Process repeats indefinitely while in room
   - Creates "looping" effect through repeated one-shot playback

   No explicit loop count parameter exists.

7. ROOM CONFIGURATION:

   From ALFRED.1 Pair 12:
   - Byte 0: Palette ID
   - Bytes 1-9: Sound file indices (0-162)
     - Index 0 = NO_SOUND.SMP (disabled)
   - 9 simultaneous sound slots per room

   Sound files loaded from SONIDOS.DAT when room loads.

8. SOUND PRIORITIES:

   No explicit priority system found. Selection based on:
   - Availability (inactive slots preferred)
   - Age (oldest timestamp selected if all active)
   - Room configuration (sound index order)

PLAYBACK TIMING EXAMPLES:
==========================

With interval_param = 32 and delay = 256 ticks (12.8s at 20 FPS):

Sound file at 11025 Hz:
- Interval: 10,328 Miles Sound ticks
- Plus delay: 256 game ticks (12.8s)
- Total: Retriggered every ~13-15 seconds

Sound file at 22050 Hz:
- Interval: 5,164 Miles Sound ticks
- Plus delay: 256 game ticks (12.8s)
- Total: Retriggered every ~13-15 seconds

The interval calculation ensures sounds retrigger at consistent rates
regardless of sample rate.

SOUND SYSTEM CHECK:
===================

Every 1090 game ticks (~54-60 seconds):
1. Iterate through 9 room sound slots
2. Check if sound index != 0 (not disabled)
3. Check timing: has interval + delay elapsed?
4. If yes, select slot and trigger playback
5. Update slot timestamp and status

Multiple sounds can trigger on same check, creating layered ambience.

CONFIGURATION SUMMARY:
======================

HARDCODED IN EXECUTABLE:
- Timer check interval: 1090 ticks (~54-60s)
- Interval parameter: 32 (0x20)
- Min delay: 256 ticks (~12.8s at 20 FPS)
- Max delay: 256 ticks (same = fixed)
- Magic timer constant: 0xd9300000

STORED IN ALFRED.1:
- Which 9 sounds each room uses (by index)
- Sound indices 0-162 reference SONIDOS.DAT

STORED IN SONIDOS.DAT:
- Actual sound data (8-bit signed PCM)
- Sample rates (in 80-byte headers when present)

CONCLUSION:
===========

Ambient sounds in Alfred Pelrock:
1. Load when entering a room (9 sounds max)
2. Check for playback every ~54-60 seconds
3. Each sound plays once when triggered
4. Retriggered every ~13-15 seconds based on calculated interval
5. Creates continuous ambient soundscape through overlapping one-shots
6. No true file looping or random intervals (min=max=256)
7. All timing parameters hardcoded in executable

The system creates a pseudo-random ambient soundscape by having multiple
sounds at different sample rates triggering at slightly offset times.
"""

def main():
    print(__doc__)

if __name__ == "__main__":
    main()
