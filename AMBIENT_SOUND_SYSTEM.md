# Alfred Pelrock - Ambient Sound System Documentation

## Overview

The ambient sound system in Alfred Pelrock provides atmospheric background sounds that play randomly when the player is idle. The system is **identical for all rooms** - only the loaded sound files change.

## Timing System

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| Game Tick Rate | 70 Hz | DOS timer interrupt frequency |
| Timer Threshold | 1090 ticks (0x442) | Ticks before ambient sound plays |
| Real-World Interval | ~15.57 seconds | Time between sounds when idle |

### Timer Behavior

```
idle_timer_2 (address 0x00051690)
├── Increments every game tick (~14.3ms)
├── Resets to 0 on ANY mouse movement
├── When > 1090:
│   ├── Call play_ambient_sound(-1, ...) // -1 = random slot
│   └── Reset timer to 0
```

**Key insight**: Mouse movement completely resets the timer. In practice, a player actively playing will rarely hear ambient sounds. They're primarily for when the player steps away or is reading/thinking.

## Room Sound Data

### Storage Format

Each room has 10 bytes of sound data stored in ALFRED.1 (Pair 9):

```
Byte 0:    Music track ID (for room music)
Bytes 1-9: Ambient sound slot indices (9 slots)
```

### Sound Index Mapping

Index 0 = "NO_SOUND.SMP" (disabled/empty slot)

Active sounds are loaded from SONIDOS.DAT based on the index:

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
| 32 | WATER_2Z.SMP | Water sounds |

## Sound Playback Details

### Function: play_ambient_sound (0x00027ce1)

```c
void play_ambient_sound(
    void* sound_driver,    // Miles Sound System driver
    int slot,              // -1 for random, or 0-8 for specific
    uint16_t volume_left,  // 0x100 (256) = full volume
    uint16_t volume_right, // 0x100 (256) = full volume  
    uint16_t param_5,      // 0x20 (32) - unknown/unused
    void* sound_handles,   // Array at 0x53234
    bool sound_enabled     // Global sound enable flag
);
```

### Volume

- Both left and right channels use value 256 (0x100)
- This represents center-panned mono playback at full volume

### Slot Selection

- When slot = -1, function picks a random active slot
- Empty slots (index 0) are skipped
- Selection is uniformly random among non-empty slots

## ScummVM Implementation Guide

### Required Components

1. **Timer Variable** (`_ambientTimer`)
   - uint16 or larger
   - Increments each game tick

2. **Room Sound Array** (`_roomSounds[9]`)
   - Loaded when entering room
   - Each entry is index into sound filename table

3. **Mouse Movement Handler**
   - Reset `_ambientTimer = 0` on any movement

### Pseudocode

```cpp
// Constants
const int AMBIENT_TICK_RATE = 70;  // Hz
const int AMBIENT_THRESHOLD = 1090;

// In game loop (called ~70 times per second)
void updateAmbientSounds() {
    _ambientTimer++;
    
    if (_ambientTimer > AMBIENT_THRESHOLD) {
        playRandomAmbientSound();
        _ambientTimer = 0;
    }
}

void onMouseMove(int x, int y) {
    _ambientTimer = 0;  // Reset on any movement
    // ... rest of mouse handling
}

void playRandomAmbientSound() {
    // Collect active slots
    Common::Array<int> activeSlots;
    for (int i = 0; i < 9; i++) {
        if (_roomSounds[i] != 0) {
            activeSlots.push_back(i);
        }
    }
    
    if (activeSlots.empty())
        return;
    
    // Pick random slot
    int slot = activeSlots[_rnd.getRandomNumber(activeSlots.size() - 1)];
    int soundIndex = _roomSounds[slot];
    
    // Play sound
    playSound(SOUND_FILENAMES[soundIndex]);
}
```

### Alternative: Real-Time Based

If you prefer real-time instead of tick-based:

```cpp
const int AMBIENT_INTERVAL_MS = 15571;  // ~15.57 seconds

void updateAmbientSounds() {
    uint32 currentTime = g_system->getMillis();
    
    if (currentTime - _lastAmbientTime > AMBIENT_INTERVAL_MS) {
        if (!_mouseMovedRecently) {
            playRandomAmbientSound();
        }
        _lastAmbientTime = currentTime;
    }
}
```

## Room Examples

### Room 0 (Street/Exterior)
```
Music: Track 1
Sounds: [2, 3, 4, 6, 7, 8, 9, 0, 0]
        Birds, Birds, Birds, Horn, Horn, Horn, Suzi, -, -
```

### Room 5 (Interior)  
```
Music: Track 3
Sounds: [21, 22, 0, 0, 0, 0, 0, 0, 0]
        Crickets, Leaves, -, -, -, -, -, -, -
```

## Audio Format

All sounds in SONIDOS.DAT are:
- **Sample Rate**: 11025 Hz (some at 22050 Hz)
- **Bit Depth**: 8-bit signed PCM
- **Channels**: Mono
- **Format**: Mix of RIFF WAV, AIL/Miles headers, and raw PCM

For ScummVM, extract all sounds to standard WAV format using `extract_sounds_v2.py`.

## Related Memory Addresses (JUEGO.EXE)

| Address | Name | Purpose |
|---------|------|---------|
| 0x00051690 | idle_timer_2 | Ambient sound timer |
| 0x0005168c | idle_timer_1 | Idle animation timer (threshold 300) |
| 0x00053234 | sound_handles | Array of sound handle pointers |
| 0x00048dd8 | sound_filenames | Array of .SMP filename strings |
| 0x0004fa40 | room_sound_data | 9 bytes of ambient indices after load |
| 0x00053002 | sound_enabled | Global sound enable flag |
| 0x00053204 | sound_driver_ptr | Miles Sound System driver |

## Related Functions

| Address | Name | Purpose |
|---------|------|---------|
| 0x00010442 | main_game_loop | Contains timer check and sound trigger |
| 0x00027ce1 | play_ambient_sound | Plays sound from slot |
| 0x00015c95 | load_room_music_and_ambient_sounds | Loads room sound config |
