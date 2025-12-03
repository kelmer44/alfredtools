# Alfred Pelrock - Ambient Sound System Documentation

## Overview

The ambient sound system in Alfred Pelrock provides atmospheric background sounds that play randomly during gameplay. The system is **frame-based with random probability** - NOT a fixed timer as initially thought.

## Timing System (CORRECTED v2)

### Game Tick Rate

Based on empirical observation (screensaver triggers at ~60 seconds with threshold 1090):

**Game Tick Rate = 1090 / 60 ≈ 18.17 Hz** (NOT 70 Hz!)

This is likely the main game loop iteration rate, not the DOS timer interrupt.

### Trigger Mechanism (in render_scene @ 0x00015eeb)

The ambient sound trigger is checked **every game tick** during rendering:

```c
// Called every game tick (~18 Hz)
void render_scene() {
    // ... rendering code ...

    // Ambient sound check
    if (random() > 0x4000) {                    // ~50% chance per tick
        if ((frame_counter & 0x1F) == 0x1F) {   // Every 32 ticks aligned
            frame_counter++;
            int slot = (random() & 0x3) + 12;   // Slots 12-15 only!
            if (sound_loaded[slot] && sound_handle[slot]) {
                play_ambient_sound(slot);
            }
        }
    }
}
```

### Key Constants

| Constant | Value | Description |
|----------|-------|-------------|
| Game Tick Rate | ~18.17 Hz | Main game loop frequency |
| Random Threshold | 0x4000 (16384) | ~50% probability |
| Counter Mask | 0x1F (31) | Check every 32 ticks |
| Slot Range | 12-15 | Only 4 slots used for ambient |

### Timing Calculation

- Tick interval: 32 ticks / 18.17 Hz = **~1.76 seconds**
- With 50% probability: **~3.5 seconds average** between attempts
- First sound: Counter starts at 0, reaches 31 after ~1.7s, then 50% chance = **~3-5 seconds** ✓
- In practice: **4-6 seconds** observed between sounds (matches!)

### Important: Mouse Does NOT Affect Timing

Unlike idle animations, the ambient sound system is **NOT reset by mouse movement**. The frame counter continues regardless of player input.

## Sound Slot Architecture

The game uses 17 sound slots (0-16) organized into two groups:

### Global Sound Slots (0-7)

Loaded once at game startup in `game_initialization`:

| Slot | Filename | Purpose |
|------|----------|---------|
| 0 | 11ZZZZZZ.SMP | UI/system sound |
| 1 | 41ZZZZZZ.SMP | UI/system sound |
| 2 | 56ZZZZZZ.SMP | UI/system sound |
| 3 | GATITOZZ.SMP | Kitten meow |
| 4-7 | (unused) | Reserved |

These persist across room changes.

### Room-Specific Sound Slots (8-16)

Loaded from room data when entering each room:

| Slot | Room Data Index | Used for Ambient |
|------|-----------------|------------------|
| 8 | 0 | No - room event sounds |
| 9 | 1 | No - room event sounds |
| 10 | 2 | No - room event sounds |
| 11 | 3 | No - room event sounds |
| **12** | **4** | **Yes - ambient** |
| **13** | **5** | **Yes - ambient** |
| **14** | **6** | **Yes - ambient** |
| **15** | **7** | **Yes - ambient** |
| 16 | 8 | No - room event sounds |

**CRITICAL**: Only slots **12-15** (room data indices 4-7) are used for ambient playback!

## Room Sound Data

### Storage Format

Each room has 10 bytes of sound data stored in ALFRED.1 (Pair 9):

```
Byte 0:    Music track ID (for room music)
Bytes 1-9: Sound indices for slots 8-16
```

### Sound Loading

The 9 room sound indices are loaded into **slots 8-16** (not 0-8!):

```c
for (i = 0; i < 9; i++) {
    load_sound_file(SOUND_FILENAMES[room_data[i+1]], slot: i + 8);
}
```

## Sound Index Mapping

Index 0 = "NO_SOUND.SMP" (disabled/empty slot)

| Index | Filename | Description |
|-------|----------|-------------|
| 0 | NO_SOUND.SMP | Silence (empty slot) |
| 1 | BUHO_ZZZ.SMP | Owl hoot |
| 2-4 | BIRD_1_[1-3].SMP | Bird chirps |
| 5 | DESPERZZ.SMP | Yawn/stretch |
| 6-8 | HORN_[5,6,8]ZZ.SMP | Car horns |
| 9 | SUZIPASS.SMP | Suzi passing |
| 10 | CAT_1ZZZ.SMP | Cat meow |
| 11-17 | DOG_0[1-9]ZZ.SMP | Dog barks |
| 18 | ALARMZZZ.SMP | Alarm |
| 19 | AMBULAN1.SMP | Ambulance siren |
| 20 | FOUNTAIN.SMP | Water fountain |
| 21 | GRILLOSZ.SMP | Crickets |
| 22 | HOJASZZZ.SMP | Leaves rustling |
| 25 | KNRRRRRZ.SMP | Snoring |
| 26-27 | PHONE_0[2-3].SMP | Phone ringing |
| 29 | BURGUER1.SMP | Burger sizzle |
| 30 | FLIES_2Z.SMP | Flies buzzing |

## ScummVM Implementation Guide

### Algorithm

```cpp
// Constants
const int AMBIENT_RANDOM_THRESHOLD = 0x4000;  // 16384

// State
uint32 _ambientFrameCounter = 0;
uint8 _roomAmbientSlots[9];  // Loaded from room data

// Called every frame (~70Hz)
void updateAmbientSounds() {
    // 50% random chance per frame
    if (_rnd.getRandomNumber(0x7FFF) > AMBIENT_RANDOM_THRESHOLD) {
        // Check if counter is aligned to 32 frames
        if ((_ambientFrameCounter & 0x1F) == 0x1F) {
            _ambientFrameCounter++;

            // Pick random slot from 12-15 (indices 4-7 in room data)
            int slotOffset = _rnd.getRandomNumber(3);  // 0-3
            int roomDataIndex = slotOffset + 4;        // 4-7

            int soundIndex = _roomAmbientSlots[roomDataIndex];
            if (soundIndex != 0) {  // 0 = no sound
                playSound(SOUND_FILENAMES[soundIndex]);
            }
        }
    }

    // Counter always increments (via timer interrupt)
    _ambientFrameCounter++;
}
```

### Alternative: Simpler Time-Based Approximation

If exact emulation isn't needed:

```cpp
const int AMBIENT_MIN_MS = 3000;   // 3 seconds minimum
const int AMBIENT_MAX_MS = 8000;   // 8 seconds maximum

void updateAmbientSounds() {
    uint32 now = g_system->getMillis();

    if (now - _lastAmbientTime > _nextAmbientDelay) {
        // Pick random ambient slot (indices 4-7)
        int slotOffset = _rnd.getRandomNumber(3);
        int soundIndex = _roomAmbientSlots[4 + slotOffset];

        if (soundIndex != 0) {
            playSound(SOUND_FILENAMES[soundIndex]);
        }

        // Schedule next sound
        _lastAmbientTime = now;
        _nextAmbientDelay = _rnd.getRandomNumber(AMBIENT_MAX_MS - AMBIENT_MIN_MS) + AMBIENT_MIN_MS;
    }
}
```

## Room Examples (Corrected)

### Room 0 (Street/Exterior)
```
Music: Track 0
Full slot data: [41, 42, 4, 0, 7, 2, 3, 10, 0]
                 │   │   │  │  │  │  │  │   └── Slot 16 (unused)
                 │   │   │  │  │  │  │  └────── Slot 15: CAT_1ZZZ (ambient)
                 │   │   │  │  │  │  └───────── Slot 14: BIRD_1_2 (ambient)
                 │   │   │  │  │  └──────────── Slot 13: BIRD_1_1 (ambient)
                 │   │   │  │  └─────────────── Slot 12: HORN_6ZZ (ambient)
                 │   │   │  └────────────────── Slot 11: empty (unused)
                 │   │   └───────────────────── Slot 10: BIRD_1_3 (unused)
                 │   └───────────────────────── Slot 9: CLDOORZZ (unused)
                 └───────────────────────────── Slot 8: OPDOORZZ (unused)

AMBIENT SOUNDS: Horn, Bird, Bird, Cat
```

### Room 1
```
Music: Track 1
Full slot data: [0, 0, 0, 0, 7, 8, 9, 13, 0]

AMBIENT SOUNDS (slots 12-15): HORN_6ZZ, HORN_8ZZ, SUZIPASS, DOG_04ZZ
```

## Sound Ordering and RNG Behavior

### Random Number Generator

The game uses the **standard ANSI C / glibc LCG** (Linear Congruential Generator):

```c
// Function: random_number_generator @ 0x0002b12f
// State pointer: get_rng_state_ptr @ 0x0002b129
// State variable: rng_state @ 0x0004c3f0

uint32 rng_state;  // Seeded at startup with non-zero value

uint16 random() {
    // Standard glibc rand() constants
    rng_state = rng_state * 0x41C64E6D + 0x3039;
    //                      ^ 1103515245  ^ 12345
    return (rng_state >> 16) & 0x7FFF;  // Returns 0-32767
}
```

### RNG Constants

| Constant | Value | Notes |
|----------|-------|-------|
| Multiplier | 0x41C64E6D | 1103515245 (glibc standard) |
| Increment | 0x3039 | 12345 (glibc standard) |
| Modulus | 2^32 | Implicit via 32-bit overflow |
| State Address | 0x0004c3f0 | In BSS section (uninitialized data) |

### Sound Sequence is DETERMINISTIC but RNG Seed Unknown

**Key Discovery**: The ambient sound sequence is **completely deterministic** - it's the same
every time the game is launched in DOSBox. However, simulating with seed=0 does NOT produce
the observed sequence.

**Observed vs Predicted (seed=0):**

| Seed | First 6 Sounds |
|------|----------------|
| 0 (expected BSS default) | BIRD→CAT→CAT→BIRD→BIRD→HORN |
| 3515 (matches observed) | BIRD→BIRD→CAT→HORN→CAT→BIRD at ~5.2, 8.6, 10.3, 13.8, 19.0, 22.5s |
| **User Observed** | BIRD→BIRD→CAT→HORN→CAT→BIRD at ~5, 9, 10, 15, 19, 24s |

**Timing Model:**
- Timer ISR runs at 18.2 Hz, incrementing `ambient_sound_frame_counter`
- `render_scene` calls RNG every frame and checks `(counter & 0x1F) == 0x1F`
- Multiple RNG calls per potential trigger opportunity (gate + slot selection)

**Why Seed != 0:**
The RNG state is in the BSS section at 0x0004c3f0. In DOS, BSS memory is NOT necessarily
zeroed - it contains whatever was in memory previously. The determinism comes from DOSBox
always loading the executable into the same memory state.

**For ScummVM Implementation:**
- Option 1: Use seed=0 for clean/predictable behavior
- Option 2: Use `g_system->getMillis()` for varied sequences each playthrough
- Option 3: Use seed=3515 to approximate original DOSBox behavior

### First Sounds in Room 0 (with seed ~2765)

With Room 0 slots [HORN_6ZZ, BIRD_1_1, BIRD_1_2, CAT_1ZZZ]:

| # | Time | Sound | Notes |
|---|------|-------|-------|
| 1 | ~5s | BIRD_1_1 or BIRD_1_2 | First ambient sound |
| 2 | ~7-9s | BIRD (other variant) | May overlap with previous |
| 3 | ~10-12s | CAT_1ZZZ | |
| 4 | ~15s | HORN_6ZZ (car horn) | |
| 5 | ~17-19s | CAT_1ZZZ | |
| 6 | ~19-24s | BIRD | |

Run `python ambient_sound_simulator.py --analyze 0` to see sequences with different seeds!

### Overlapping Sounds

The game does NOT prevent sounds from overlapping. If:
- Counter is at 31 (0x1F) or 63 (0x3F), etc.
- AND random > 0x4000 passes twice in succession

Two sounds can trigger in very close succession (~55ms apart = 1 tick at 18.17 Hz).

**For ScummVM**: You may want to add a minimum delay between ambient sounds to prevent overlap, OR allow overlapping for authenticity.

## Idle Animation System (Separate from Ambient Sounds)

The idle animation system is completely separate from ambient sounds. It tracks player inactivity and triggers special animations.

### Idle Timers (Reset on Mouse Movement)

| Timer | Address | Threshold | Time | Trigger |
|-------|---------|-----------|------|---------|
| Hair Combing | 0x0005168c | 300 | ~16.5s | Alfred combs hair |
| Screensaver | 0x00051690 | 1090 | ~60s | Sliding puzzle |

**Key Difference**: Idle timers reset when mouse moves. Ambient sounds do NOT.

### Hair Combing Animation Details

**Function**: `play_hair_combing_idle_animation`
**Address**: Part of main_game_loop handler
**Trigger**: 300 ticks of inactivity (~16.5 seconds)

```c
void play_hair_combing_idle_animation() {
    char room = get_current_room_number();

    // ONLY plays in rooms 0 and 1!
    if (room != 0 && room != 1) return;

    // Allocate 64KB buffer for animation frames
    byte* buffer = allocate_memory(0x10000);

    // HARDCODED offsets in ALFRED.7:
    uint32 offset;
    if (room == 0) {
        offset = 0x108C2;  // Right-facing Alfred
    } else {
        offset = 0x15958;  // Left-facing Alfred
    }

    // Read and decompress RLE animation data (0x5596 bytes)
    file_seek(ALFRED7_HANDLE, offset);
    file_read(ALFRED7_HANDLE, compressed_buffer, 0x5596);
    decompress_rle_block(compressed_buffer, buffer);

    // Play 10 frames forward (frame size = 0x1452 = 5202 bytes each)
    for (int i = 0; i < 10; i++) {
        process_game_state(1);
        update_animations();
        display_frame(buffer + i * 0x1452);
        render_scene();
    }

    // Swap frames 0-2 with frames 7-9 for reverse sequence
    swap_frame_pairs(buffer);

    // Play 6 frames (reversed portion)
    for (int i = 0; i < 6; i++) {
        process_game_state(1);
        update_animations();
        display_frame(buffer + i * 0x1452);
        render_scene();
    }

    free(buffer);
}
```

**Animation Data in ALFRED.7**:
- Room 0 offset: 0x108C2 (right-facing)
- Room 1 offset: 0x15958 (left-facing)
- Compressed size: 0x5596 bytes (RLE)
- Frame size: 0x1452 bytes (5202 bytes per frame)
- Total frames: 10 forward + 6 reversed = 16 frame sequence
- Likely resolution: ~51x102 pixels per frame

### Sliding Puzzle Screensaver Details

**Function**: `screensaver_sliding_puzzle` @ 0x00026879
**Trigger**: 1090 ticks of inactivity (~60 seconds)

```c
void screensaver_sliding_puzzle() {
    // Initialize puzzle tiles in order
    for (int i = 0; i < puzzle_width * puzzle_height; i++) {
        tile_positions[i] = i;
    }

    // Clear screen and draw initial grid
    set_video_mode(0);
    render_menu_screen();
    present_frame();
    puzzle_draw_grid();

    // Scramble phase: randomly swap tiles
    do {
        wait_for_input();

        // Generate two random tile positions
        uint pos1 = random() & mask;
        uint pos2 = random() & mask;

        // Ensure valid positions
        while (pos1 >= tile_count || pos2 >= tile_count) {
            pos1 = random() & mask;
            pos2 = random() & mask;
        }

        puzzle_swap_tiles(pos1, pos2);
        present_frame();
        play_ambient_sound();  // Ambient sounds still play!

    } while (!check_keyboard_input());

    // Wait for key release
    do {
        wait_for_input();
    } while (check_keyboard_input());

    // Interactive puzzle solving phase
    while (true) {
        wait_for_input();
        render_scene(0xFF);

        if (mouse_button_held) {
            // Wait for release
            while (mouse_button_held) {
                render_scene(0xFF);
            }

            puzzle_handle_mouse_click(mouse_x, mouse_y);

            // Check if puzzle is solved
            bool solved = true;
            for (int i = 0; i < tile_count - 1; i++) {
                if (tile_positions[i] != i) {
                    solved = false;
                    break;
                }
            }

            if (solved) {
                // Victory! Play "CHIQUITO.SMP" sound
                load_sound_file("CHIQUITO.SMP", 6);
                play_ambient_sound();

                // Wait for sound to finish
                do {
                    wait_for_input();
                    render_scene(0xFF);
                } while (!sound_finished(miles_driver, 3));

                sound_cleanup();
            }
        }

        // Exit on any key press
        if (check_keyboard_input()) {
            break;
        }
    }
}
```

**Puzzle Features**:
- Classic sliding tile puzzle
- Random scrambling animation before player interaction
- Ambient sounds continue playing during puzzle
- "CHIQUITO.SMP" plays on successful completion
- Exit on any key press

**For ScummVM**: This is a mini-game that should be implemented as a separate game state.

## Idle Timer Check Location

Both idle timers are checked in `main_game_loop` @ 0x00010442:

```c
// In main_game_loop
if (idle_timer_hair_combing > 300) {
    play_hair_combing_idle_animation();
    idle_timer_hair_combing = 0;
}

if (idle_timer_screensaver > 0x442) {  // 1090
    play_ambient_sound();
    screensaver_sliding_puzzle();
    idle_timer_screensaver = 0;
}

// Always increment timers (reset elsewhere on mouse movement)
idle_timer_hair_combing++;
idle_timer_screensaver++;
```

## Related Memory Addresses (JUEGO.EXE)

| Address | Name | Purpose |
|---------|------|---------|
| 0x0004c3f0 | rng_state | LCG random number generator state |
| 0x00051738 | ambient_sound_frame_counter | Counter for ambient sound timing |
| 0x0004fa38 | sound_slot_loaded_flags | Array of sound slot flags |
| 0x00053214 | sound_slot_handles | Array of sound handle pointers (slot * 4) |
| 0x00048dd8 | sound_filename_table | Array of .SMP filename strings |
| 0x0004fa40 | room_sound_indices | 9 bytes of ambient indices |
| 0x00053002 | sound_enabled_flag | Global sound enable flag |
| 0x00053204 | miles_sound_driver_ptr | Miles Sound System driver |
| 0x0005168c | idle_timer_hair_combing | Timer for hair combing animation (threshold 300) |
| 0x00051690 | idle_timer_screensaver | Timer for sliding puzzle screensaver (threshold 1090) |
| 0x0004fb94 | current_room_number | Current room ID |
| 0x0004fa55 | current_music_track_id | Current CD audio track |

## Detailed Investigation Notes

### RNG Seed Mystery (December 2024)

During reverse engineering, we discovered a discrepancy between simulated and observed behavior:

**Observed Behavior (DOSBox recording):**
- Sequence: BIRD→BIRD→CAT→HORN→CAT→BIRD
- Times: ~5s, ~9s, ~10s, ~15s, ~19s, ~24s
- **Deterministic**: Same sequence every time game is launched

**Simulated Behavior (seed=0):**
- Sequence: BIRD→CAT→CAT→BIRD→BIRD→HORN
- Times: ~5.2s, ~13.9s, ~22.6s, ~26.1s, ~27.8s, ~29.5s
- **Does NOT match observed!**

**Investigation findings:**
1. **RNG algorithm verified**: Disassembly at 0x0002b12f confirms ANSI C LCG with standard constants
2. **State in BSS**: RNG state at 0x0004c3f0 is in uninitialized data section
3. **No explicit seeding**: Only one xref to state address (get_rng_state_ptr)
4. **Counter increment locations**:
   - Timer ISR at 0x00015250 (continuous)
   - render_scene at 0x00015f04 (after trigger)

**Exhaustive seed search found:**
- Seeds 799, 1122, 2986, 3363, 3376, 3515, 3561, 3939, 4420, 4632 produce matching sequence
- Seed 3515 has closest timing match (error ~3.6s total)

**Conclusion:**
The RNG state is NOT zero at game start. In DOS/DOSBox, BSS memory contains residual data
from previous memory contents. The determinism comes from DOSBox consistently loading the
executable into the same memory layout.

### Counter Increment Mechanics

The `ambient_sound_frame_counter` is incremented in TWO places:

1. **Timer ISR (0x00015250)**: Increments continuously at ~18.2 Hz (DOS INT 0x1C)
2. **render_scene (0x00015f04)**: Increments after successful sound trigger

The trigger condition `(counter & 0x1F) == 0x1F` means sounds can trigger when counter
equals 31, 63, 95, 127, etc. After triggering, counter is incremented to move past the
trigger point (becomes 32, 64, 96, 128, etc.).

## Related Functions

| Address | Name | Purpose |
|---------|------|---------|
| 0x00015e4c | render_scene | Contains ambient sound trigger |
| 0x00027ce1 | play_ambient_sound | Plays sound from slot |
| 0x00015c95 | load_room_music_and_ambient_sounds | Loads room sound config |
| 0x0002b129 | get_rng_state_ptr | Returns pointer to rng_state (0x4c3f0) |
| 0x0002b12f | random_number_generator | LCG random (returns 0-0x7FFF) |
| 0x00010442 | main_game_loop | Main game loop with timer checks |
| 0x0001bfba | process_game_state | Game state processing |
| 0x000267dd | load_sound_file | Loads .SMP file into slot |
| 0x0002a218 | get_current_room_number | Returns current room ID |
| 0x0002a258 | wait_or_process_input | Waits for input/timer |
| 0x00026879 | screensaver_sliding_puzzle | Sliding puzzle screensaver minigame |
| 0x000104XX | play_hair_combing_idle_animation | Alfred's hair combing idle animation |
| 0x00026f58 | puzzle_handle_mouse_click | Handle clicks in puzzle minigame |

## Audio Format

All sounds in SONIDOS.DAT are:
- **Sample Rate**: 11025 Hz (some at 22050 Hz)
- **Bit Depth**: 8-bit signed PCM
- **Channels**: Mono
- **Format**: Mix of RIFF WAV, AIL/Miles headers, and raw PCM

For ScummVM, extract all sounds to standard WAV format using `extract_sounds_v2.py`.
