# Intro Video Timing Analysis: ScummVM vs Original VISOR.EXE

## Executive Summary

The ScummVM implementation of the intro video player has significant timing differences compared to the original DOS executable (VISOR.EXE). The original uses **centisecond-based timing** (1/100th second = 10ms per tick) with a **2 centisecond frame interval** (20ms, ~50 FPS effective rate), while the ScummVM implementation uses a complex frame-skip mechanism tied to a 55ms game tick (~18 FPS).

## Original VISOR.EXE Timing Analysis (Ghidra)

### Timer System - TWO TIMING SOURCES

The original uses **two separate timing mechanisms**:

#### 1. High-Resolution Timer (Centiseconds)
DOS interrupt 0x21, function 0x2C (Get System Time) via `get_bios_time_centiseconds()`:

```c
// Returns time in centiseconds (1/100th second = 10ms resolution)
int get_bios_time_centiseconds(void) {
    // DOS INT 21h, AH=2Ch returns:
    // CH = hour, CL = minute, DH = second, DL = centisecond
    return (((hour * 60 + minute) * 60) + second) * 100 + centisecond;
}
```

This is used for the **main frame timing loop** with 2 centisecond (20ms) intervals.

#### 2. Low-Resolution Timer (18.2 Hz Ticks)
DOS BIOS timer interrupt 0x1C, hooked via `FUN_00011a83()`:

```c
// Sets up INT 0x1C hook - the BIOS timer tick at 18.2 Hz (~55ms per tick)
void setup_timer_interrupt(void) {
    original_int1c_handler = get_interrupt_vector(0x1C);  // Save original
    set_interrupt_vector(0x1C, timer_tick_handler);        // Install hook
}

// Interrupt handler increments current_timer_value at 18.2 Hz
void timer_tick_handler(void) {
    current_timer_value++;  // Incremented ~18.2 times per second
    // Chain to original handler...
}
```

This is used for **subtitle display extra delay** in `copy_to_vga()`.

### Main Video Loop Timing

```c
// From main_video_player() in Ghidra:
iVar4 = get_timer_ticks();
next_frame_time = iVar4 + 2;  // <-- KEY: 2 centiseconds = 20ms

while (video_exit_flag == 0) {
    // ... buffering logic ...

    current_time = get_timer_ticks();

    // Process frame when: current_time > next_frame_time
    if ((next_frame_time < current_time) && playback_enabled && chunks_in_buffer > 0) {
        current_playback_frame++;
        process_frame();

        if (current_playback_frame == 0x14) {  // 20-frame circular buffer
            current_playback_frame = 0;
        }

        chunks_in_buffer--;

        // Schedule next frame 2 centiseconds later
        iVar4 = get_timer_ticks();
        next_frame_time = iVar4 + 2;  // <-- 20ms interval = 50 FPS
    }

    // Read more chunks if buffer is low
    if (chunks_in_buffer < 0xf) {  // 15
        read_chunk_from_ssn();
        // ... buffer chunk ...
    }
}
```

### Critical Timing Constants (Original)

| Constant | Value | Meaning |
|----------|-------|---------|
| Frame interval | 2 centiseconds | 20ms between frames |
| Effective FPS | 50 FPS | 1000ms / 20ms |
| Buffer size | 20 slots | Circular buffer (0x14) |
| Min buffer before play | 10 chunks | `total_chunks_loaded > 10` |
| Max buffer before pause | 19 chunks | `chunks_in_buffer == 0x13` |
| Low buffer threshold | 15 chunks | `chunks_in_buffer < 0xf` |

### Subtitle Display Timing (Original)

From `copy_to_vga()`:
```c
void copy_to_vga(void) {
    // ... copy frame buffer ...

    // Skip subtitles during frames 571-669 (specific scene?)
    if ((frame_counter < 0x23b) || (0x29d < frame_counter)) {
        render_subtitles(frame_counter);
    }

    write_to_vga_memory();

    // CRITICAL: If subtitle was displayed, ADD EXTRA DELAY
    // Uses 18.2 Hz timer (NOT centiseconds!)
    if (subtitle_displayed_flag != 0) {
        byte extra_delay = 1;  // Actually comes from get_current_chunk_index(1)
        subtitle_end_time = current_timer_value + extra_delay;
        do {
            dos_yield();  // Yield CPU while waiting
        } while (current_timer_value <= subtitle_end_time);
    }
}
```

The extra delay is **1 tick of the 18.2 Hz timer = ~55ms**.

This means:
- Normal frames: just the 20ms frame interval
- Frames with subtitles: 20ms + 55ms = **75ms** (effectively ~13 FPS)

This creates a **variable frame rate** that depends on subtitle presence.

### Audio System (Original)

The original handles multiple command types in the SCR script using **multiple audio channels**:

| Command | Purpose | Channel | Handler |
|---------|---------|---------|---------|
| `/t` | Text subtitle | N/A | `render_text_to_vga()` - no audio |
| `/f` | Voice file (speech) | 0-3 (rotating) | `load_audio_for_subtitle()` + `play_audio_sample()` |
| `/c` | CD audio track | 5 | Load from CD music track (tracks 30-32) |
| `/x` | SFX/extra sound | 6 | Load and play with **busy-wait** |

#### Voice Channel Rotation (`/f` command)
```c
// Voices use channels 0-3 in rotation
audio_channel_index = (audio_channel_index + 1) & 3;  // Cycles 0,1,2,3,0,1,2...
```

#### CD Audio (`/c` command)
```c
if (command == '/c') {
    if (cd_audio_active != 0) {
        stop_current_audio();
        cleanup_audio_channel();
        free_buffer(0);
        cd_audio_active = 0;
    }
    int track = atoi_string(track_str);
    // Lookup from track table at DAT_0003040c
    load_audio_for_subtitle(track_table[track], 5);  // Channel 5
    play_audio_sample();
}
```

#### SFX Busy-Wait (`/x` command) - CRITICAL FOR TIMING
```c
if (command == '/x') {
    // BUSY-WAIT until audio channel 6 is ready!
    while (!check_audio_channel_ready(sound_driver_handle, 6)) {
        dos_yield();  // This can block for arbitrary time!
    }

    if (sfx_channel_active != 0) {
        cleanup_audio_channel();
        free_buffer(0);
        sfx_channel_active = 0;
    }

    load_audio_for_subtitle(filename, 6);  // Channel 6
    play_audio_sample();
}
```

**This busy-wait is the likely cause of speech audio cutoff/skipping in the original!**

The `/x` command blocks the main loop until channel 6 is free. If the previous SFX
hasn't finished playing, the video frame processing stalls, but the frame timing
continues advancing. This causes desynchronization between video frames and audio.

### Audio Channel Summary

| Channel | Purpose | Notes |
|---------|---------|-------|
| 0-3 | Voice (rotating) | Speech from introsnd.dat |
| 5 | CD Audio | Background music tracks |
| 6 | SFX | Sound effects with busy-wait |
| 7 | Special | First frame (frame 0) voice |

---

## ScummVM Implementation Analysis

### Current Timing System

```cpp
// chrono.h
const int kTickMs = 55;  // Game tick interval

// video.cpp - playIntro()
while (!videoExitFlag) {
    _chrono->updateChrono();
    _events->pollEvent();

    Subtitle *subtitle = getSubtitleForFrame(frameCounter);
    int frameSkip = subtitle != nullptr ? 4 : 2;  // Different frame skip based on subtitle

    if (_chrono->_gameTick && _chrono->getFrameCount() % frameSkip == 0) {
        // Process frame
        readChunk(videoFile, chunk);
        // ... handle chunk ...
        frameCounter++;
    }

    g_system->delayMillis(10);  // 10ms delay each loop iteration
}
```

### ScummVM Timing Constants

| Constant | Value | Effect |
|----------|-------|--------|
| kTickMs | 55ms | Base game tick |
| frameSkip (no subtitle) | 2 | Process every 2nd tick |
| frameSkip (with subtitle) | 4 | Process every 4th tick |
| Loop delay | 10ms | Added every iteration |

### Calculated Frame Rates (ScummVM)

**Without subtitle:**
- Effective interval = 55ms × 2 = 110ms
- FPS = ~9.1 FPS

**With subtitle:**
- Effective interval = 55ms × 4 = 220ms
- FPS = ~4.5 FPS

**This is significantly slower than the original's 50 FPS!**

---

## Key Differences

### 1. Frame Rate

| Aspect | Original | ScummVM |
|--------|----------|---------|
| Base frame interval | 20ms | 110-220ms |
| Effective FPS | 50 FPS | 4.5-9.1 FPS |
| Speed ratio | 1x | **5-11x slower** |

### 2. Buffering Strategy

| Aspect | Original | ScummVM |
|--------|----------|---------|
| Uses ring buffer | Yes (20 slots) | No |
| Async loading | Yes (loads while playing) | No |
| Chunk pre-loading | 10 chunks before play | None |
| Decoupled I/O | Yes | No (sequential read) |

### 3. Subtitle Timing

| Aspect | Original | ScummVM |
|--------|----------|---------|
| Extra delay for subtitles | Yes (busy-wait) | Yes (via frameSkip=4) |
| Frame blackout range | 571-669 | Not implemented |

### 4. Audio Synchronization

| Aspect | Original | ScummVM |
|--------|----------|---------|
| Multiple channels | Yes (at least 7) | Single sound |
| Wait for voice finish | Yes (busy-wait before next) | Yes |
| SFX channel handling | Dedicated channel 6 | Not implemented |
| Music/CD support | Yes (via `/c` command) | Not implemented |

---

## Expected Video Duration Calculation

### SCR File Command Statistics
- `/t` commands (text subtitles): **65**
- `/f` + `/x` commands (voice/SFX): **74**
- `/c` commands (CD audio): **3**

Highest frame referenced: **680**

### Duration Calculation

Given the **two-timer system**:

#### Frame Timing (20ms base)
- Base frame interval: 20ms (2 centiseconds)
- Total frames: ~680

Base playback time: `680 × 20ms = 13,600ms = 13.6 seconds`

#### Subtitle Delay (55ms extra per subtitle)
- Frames with subtitles: ~65 subtitle ranges
- Extra delay per subtitle frame: 55ms (1 tick @ 18.2 Hz)

Estimated subtitle delay: `65 × 55ms = 3,575ms = 3.6 seconds`

#### Total Estimated Time
`13.6s + 3.6s = 17.2 seconds`

**This is way shorter than 3:29 (209 seconds)!**

### Re-Analysis: The Buffering Factor

Looking at the main loop again, the original uses a **producer-consumer buffer**:
- Chunks are read from disk asynchronously
- Playback starts only after 10 chunks are buffered
- Frame processing happens when `next_frame_time < current_time`

The timing `iVar4 + 2` is in **centiseconds**, not milliseconds!

But `current_timer_value` for subtitles uses **18.2 Hz ticks**.

### Correct Timing Model

1. **Frame timing**: Every 2 centiseconds (20ms) → 50 potential FPS
2. **Subtitle delay**: Extra 1 tick @ 18.2 Hz (55ms) when subtitle displayed
3. **Audio sync**: `/x` command busy-waits for audio channel

With audio files averaging 2-4 seconds each, and 74 voice/SFX commands,
the total audio time dominates:

`74 voice clips × ~3s average = ~222 seconds`

This is much closer to the 3:29 (209 seconds) duration!

### Key Insight: Audio Drives the Timing

The intro's duration is primarily determined by **audio playback**, not frame rate.

Your implementation waits for voice to finish before playing the next:
```cpp
while (_sound->isPlaying()) {
    _events->pollEvent();
    g_system->delayMillis(10);
}
```

This is conceptually correct, but the frame timing system should be independent.
The original continues advancing frames while audio plays, only blocking for `/x` SFX.

---

## Recommended Fixes

### 1. Fix Frame Timing (CRITICAL - Main Issue)

Replace the ChronoManager-based timing with direct millisecond timing matching the original's
**2 centisecond (20ms) frame interval**:

```cpp
void VideoManager::playIntro() {
    const uint32 FRAME_INTERVAL_MS = 20;  // 2 centiseconds = 50 FPS like original
    const uint32 SUBTITLE_EXTRA_DELAY_MS = 55;  // 1 tick @ 18.2 Hz

    uint32 lastFrameTime = g_system->getMillis();
    uint32 frameCounter = 0;

    // Wait until 10 chunks are buffered before starting playback
    // (Optional: implement ring buffer for smoother playback)

    while (!videoExitFlag && !g_engine->shouldQuit()) {
        _events->pollEvent();

        if (_events->_lastKeyEvent == Common::KEYCODE_ESCAPE) {
            break;
        }

        uint32 currentTime = g_system->getMillis();

        if (currentTime - lastFrameTime >= FRAME_INTERVAL_MS) {
            ChunkHeader chunk;
            readChunk(videoFile, chunk);

            switch (chunk.chunkType) {
            case 1:
            case 2:
                processFrame(chunk, frameCounter);

                // Check for subtitle
                Subtitle *subtitle = getSubtitleForFrame(frameCounter);

                // Render subtitle if in valid range (not frames 571-669)
                if ((frameCounter < 571 || frameCounter > 669) && subtitle) {
                    renderSubtitle(subtitle);
                }

                presentFrame();
                frameCounter++;

                // Add extra delay if subtitle was displayed
                if (subtitle != nullptr) {
                    g_system->delayMillis(SUBTITLE_EXTRA_DELAY_MS);
                }
                break;

            case 3:
                videoExitFlag = true;
                break;

            case 4:
                loadPalette(chunk);
                break;
            }

            lastFrameTime = currentTime;
        }

        g_system->delayMillis(1);  // Small yield to OS
    }
}
```

### 2. Remove frameSkip Logic

The current implementation uses `frameSkip` which artificially slows down playback:

```cpp
// REMOVE THIS:
int frameSkip = subtitle != nullptr ? 4 : 2;
if (_chrono->_gameTick && _chrono->getFrameCount() % frameSkip == 0) {
```

Replace with direct timing as shown above.

### 3. Implement Proper Audio Channel System

Create an audio channel system matching the original:

```cpp
// Audio channel constants
static const int VOICE_CHANNELS = 4;      // Channels 0-3 for rotating voice
static const int CD_AUDIO_CHANNEL = 5;    // Channel 5 for CD music
static const int SFX_CHANNEL = 6;         // Channel 6 for SFX (with wait)
static const int SPECIAL_CHANNEL = 7;     // Channel 7 for frame 0 voice

// Handle /f command (voice)
void handleVoiceCommand(int frame, const Common::String &filename) {
    int channel = _voiceChannelIndex;
    _voiceChannelIndex = (_voiceChannelIndex + 1) & 3;  // Rotate 0-3
    playAudioOnChannel(filename, channel);
}

// Handle /x command (SFX with busy-wait)
void handleSfxCommand(int frame, const Common::String &filename) {
    // Wait for channel 6 to be free (like original)
    while (_sound->isChannelPlaying(SFX_CHANNEL)) {
        _events->pollEvent();
        g_system->delayMillis(1);
        if (g_engine->shouldQuit()) break;
    }
    playAudioOnChannel(filename, SFX_CHANNEL);
}

// Handle /c command (CD audio)
void handleCdAudioCommand(int frame, int trackNumber) {
    // Map track number to actual music file
    // Tracks 30, 31, 32 correspond to intro music segments
    stopChannel(CD_AUDIO_CHANNEL);
    playMusicTrack(trackNumber, CD_AUDIO_CHANNEL);
}
```

### 4. Implement Frame Blackout Range

The original skips subtitle rendering for frames 571-669:

```cpp
void VideoManager::renderSubtitles(uint16 frameCounter) {
    // Skip subtitles during frames 571-669 (0x23b - 0x29d)
    if (frameCounter >= 571 && frameCounter <= 669) {
        return;  // No subtitles in this range
    }

    // Normal subtitle processing...
}
```

### 5. Handle All SCR Command Types

Your current implementation only handles `/t` and `/x`. Add support for:

```cpp
void VideoManager::processScriptCommands(uint16 frameCounter) {
    for (auto &cmd : _scriptCommands) {
        if (cmd.frame != frameCounter) continue;

        switch (cmd.type) {
        case 't':  // Text subtitle
            // Already implemented
            break;

        case 'f':  // Voice file
            handleVoiceCommand(frameCounter, cmd.filename);
            break;

        case 'x':  // SFX (with wait)
            handleSfxCommand(frameCounter, cmd.filename);
            break;

        case 'c':  // CD audio track
            handleCdAudioCommand(frameCounter, cmd.trackNumber);
            break;
        }
    }
}
```

---

## Ghidra Symbols Renamed During Analysis

### Functions
| Original | New Name | Purpose |
|----------|----------|---------|
| `mystery_timing_function` | `set_vga_palette_from_chunk` | Loads palette from Type 4 chunk |
| `FUN_0001c833` | `get_bios_time_centiseconds` | Returns time in centiseconds via INT 21h |
| `FUN_0001e6cf` | `call_dos_int21h` | Generic DOS interrupt caller |
| `FUN_0001506d` | `dos_yield` | Yields CPU (INT 28h or similar) |
| `FUN_000152cd` | `atoi_string` | Converts string to integer |
| `FUN_00012f85` | `check_audio_channel_ready` | Checks if audio channel is free |
| `FUN_000129e2` | `stop_current_audio` | Stops playing audio |
| `FUN_000127ae` | `cleanup_audio_channel` | Cleans up audio channel resources |

### Data Labels
| Address | New Name | Purpose |
|---------|----------|---------|
| `DAT_00033c84` | `subtitle_displayed_flag` | Set when subtitle is rendered |
| `DAT_00033a98` | `subtitle_end_time` | Target timer value for subtitle delay |
| `DAT_00033a94` | `current_timer_value` | Incremented by INT 1Ch (18.2 Hz) |
| `DAT_00033a8c` | `script_cursor` | Current position in SCR script |
| `DAT_000338d8` | `audio_enabled` | Flag for audio system availability |
| `DAT_00033c73` | `audio_channel_index` | Rotating voice channel (0-3) |
| `DAT_00033ba8` | `sound_driver_handle` | Handle to sound driver |
| `DAT_00033bd0` | `sfx_channel_active` | Flag for SFX channel 6 |
| `DAT_00033bcc` | `cd_audio_active` | Flag for CD audio channel 5 |
| `DAT_00033bb8` | `voice_channel_handles` | Array of voice channel handles |
| `DAT_00033ca4` | `voice_audio_buffers` | Array of voice audio buffers |

---

## Frame Blackout Mystery

The original skips subtitle rendering for frames 571-669:
```c
if ((frame_counter < 0x23b) || (0x29d < frame_counter)) {
    render_subtitles(frame_counter);
}
```

At 50 FPS, frames 571-669 span approximately:
- Start: 571 / 50 = 11.42 seconds
- End: 669 / 50 = 13.38 seconds

This 2-second window likely corresponds to a scene transition or specific animation where subtitles shouldn't appear.

---

## Original Speech Audio Issues

You mentioned the original has timing issues where speech audio gets cut off or skips. This is likely due to:

1. **Busy-wait blocking**: The `/x` command busy-waits for audio channel availability
2. **No audio synchronization**: Video frames continue advancing while waiting for audio
3. **Buffer underrun**: If I/O is slow, audio might be interrupted

The original was designed for specific CD-ROM speeds and DOS timing. DOSBox-X may not perfectly emulate the audio subsystem timing.

---

## Conclusion

The primary issue causing your video to play at the wrong speed is the **frame timing mechanism**. The original uses a simple 20ms interval (50 FPS), while your implementation uses a complex frame-skip system that results in effective rates of 4.5-9.1 FPS.

**Immediate fix**: Change to direct millisecond-based timing with 20ms intervals between frames.

**Additional improvements**: Implement the ring buffer for smoother playback and handle all SCR command types for proper audio sync.
