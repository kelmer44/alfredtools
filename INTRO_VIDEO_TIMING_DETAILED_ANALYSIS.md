# Intro Video Timing: Detailed Analysis (VISOR.EXE vs ScummVM)

## Overview

A frame-by-frame comparison of the original VISOR.EXE (via Ghidra decompilation) with the ScummVM reimplementation reveals several critical bugs causing the video to play differently. The primary issues are:

1. **Off-by-one frame counter** — audio triggers fire 1 visual frame early
2. **Type 6 chunks cause duplicate audio triggers** — the last speech file plays twice
3. **Type 6 timing is inflated** — non-visual chunks consume ~110ms instead of 20ms
4. **Single audio channel** — voices overlap incorrectly compared to original's rotating channels
5. **Frame timing model is fundamentally different** — ChronoManager-based vs centisecond timing

---

## SSN File Structure (ESCENAX.SSN)

The SSN file contains **736 total chunks**:

| Type | Count | Purpose |
|------|-------|---------|
| 1 (RLE) | 285 | RLE-compressed delta frames |
| 2 (BlockCopy) | 402 | Block-copy delta frames |
| 3 (End) | 1 | End-of-video marker |
| 4 (Palette) | 1 | Palette load (first chunk only) |
| 6 (Timing Pad) | 47 | Timing delay padding (0xFF fill) |

**687 visual frames** (types 1+2), **47 non-visual type 6 padding chunks**.

### Type 6 Chunks: Timing Pads

All 47 type 6 chunks have identical structure:
- `block_count=1` (one 0x5000-byte block)
- `data_offset=0x635` (1589)
- Content: mostly 0xFF bytes with a small header

They are **NOT audio data**. They serve as **timing delay pads** — consuming a slot in the circular buffer (and thus one 20ms timing interval) without producing visual output or triggering audio.

Key clusters of type 6 chunks:
| Location | Count | Between visual frames | Purpose (likely) |
|----------|-------|----------------------|-------------------|
| chunks 13,17 | 2 | 11→12, 14→15 | Early scene pacing |
| chunks 72-73 | 2 | 68→69 | Scene transition pause |
| chunks 161-165 | 5 | 153→154 | Door opening scene pause |
| chunks 200-214 | **15** | 187→188 | Major scene transition (300ms) |
| chunks 408-411 | 4 | 374→375 | Scene pause |
| chunk 717 | 1 | 669→670 | **THE BUG TRIGGER** |

---

## SCR Command Mapping

The ESCENAX.SCR script file maps frame numbers to actions:

| Command | Purpose | Original Channel | Count |
|---------|---------|-----------------|-------|
| `/t` | Subtitle text | N/A | 65 |
| `/f` | SFX (fire, footsteps, door) | Rotating 0-3 (or 7 for frame 0) | 8 |
| `/x` | Voice/speech PCM | Channel 6 (with busy-wait) | 65 |
| `/c` | CD audio track | Channel 5 | 3 |

### ScummVM mapping (video.cpp `initMetadata`):
```
/x → _voiceEffect (voice speech) → channel 0  ← CORRECT
/f → _sfxEffect (sound effects)  → channel 1  ← CORRECT
/c → _musicEffect (CD audio)     → music       ← CORRECT
```

---

## Bug 1: Off-by-One Frame Counter (Audio Fires 1 Frame Early)

### Original (VISOR.EXE process_frame + copy_to_vga + render_subtitles)

```c
void process_frame(void) {
    int idx = get_current_chunk_index();
    if (chunk_types[idx] == 1) {
        decode_rle_frame(...);
        if (frame_counter == 0) memcpy(...);
        else apply_xor_delta(...);
        copy_to_vga();           // ← audio triggers HERE, using frame_counter
    } else if (chunk_types[idx] == 2) {
        decode_block_copy_frame(...);
        if (frame_counter == 0) memcpy(...);
        else apply_xor_delta(...);
        copy_to_vga();           // ← audio triggers HERE, using frame_counter
    } else {
        return;                  // ← type 6: returns early, NO audio check
    }
    frame_counter++;             // ← increment AFTER audio check
}
```

**Sequence**: decode → XOR → copy_to_vga(which calls render_subtitles(frame_counter)) → frame_counter++

Audio is checked **BEFORE** frame_counter is incremented. So when frame N is displayed, audio for frame N fires.

### ScummVM (video.cpp playIntro)

```cpp
processFrame(chunk, frameCounter++);          // frameCounter increments HERE
// ...
if (_voiceEffect.contains(frameCounter)) {    // checks frameCounter AFTER increment
```

**Sequence**: processFrame (using old frameCounter) → frameCounter++ → check voice at NEW frameCounter

Audio is checked **AFTER** frameCounter is incremented. So when frame N is displayed, audio for frame N+1 fires.

### Impact

Every audio trigger in ScummVM fires **one visual frame too early**. At the original's 20ms frame interval this would be barely noticeable, but at the ScummVM's ~110ms+ intervals, it's audible.

**Fix**: Move the audio check BEFORE `frameCounter++`, or check `frameCounter - 1`.

---

## Bug 2: Type 6 Chunks Cause Duplicate Audio Triggers

### The Problem

When a type 6 chunk is read, `frameCounter` is NOT incremented (only types 1/2 increment it). But the audio check still runs with the same `frameCounter` value.

### Trace of the Last Speech Bug

```
SCR entries:
  /x  670 VOC16_0Z.PCM  → _voiceEffect[670]
  /f  671 ETHERZZZ.SMP  → _sfxEffect[671]

SSN chunks near the end:
  chunk[716]  type=1  visual_frame=669
  chunk[717]  type=6  (timing pad)
  chunk[718]  type=1  visual_frame=670
```

ScummVM execution trace:

1. **chunk[716]** (visual frame 669):
   - `processFrame(chunk, 669)` → frameCounter becomes **670**
   - Check `_voiceEffect[670]` → **MATCH** → plays VOC16_0Z.PCM ✓

2. **chunk[717]** (type 6 - timing pad):
   - Falls into `default:` case → no increment → frameCounter stays **670**
   - Check `_voiceEffect[670]` → **MATCH AGAIN** → plays VOC16_0Z.PCM **a SECOND time!** ✗

3. **chunk[718]** (visual frame 670):
   - `processFrame(chunk, 670)` → frameCounter becomes **671**
   - Check `_sfxEffect[671]` → MATCH → plays ETHERZZZ.SMP ✓

**This is exactly the "last speech file played at two different points" bug.** The type 6 chunk between visual frames 669 and 670 causes the voice for frame 670 to fire twice.

### Why It Doesn't Happen in the Original

In the original, `process_frame()` returns immediately for type 6 chunks WITHOUT calling `copy_to_vga()` or `render_subtitles()`. Audio triggers are inside `render_subtitles`, so they are NEVER checked for type 6 chunks.

**Fix**: Skip audio/subtitle checks when chunk type is not 1 or 2.

---

## Bug 3: Type 6 Timing is Too Slow

### Original

Type 6 chunks go into the 20-slot circular buffer. When played from the buffer, they consume one timing interval:

```c
// main_video_player:
if (next_frame_time < current_time && playback_enabled && chunks > 0) {
    current_playback_frame++;
    process_frame();                    // returns immediately for type 6
    chunks_in_buffer--;
    next_frame_time = get_timer_ticks() + 2;  // 20ms interval
}
```

Each type 6 chunk adds **20ms** of delay.

47 type 6 chunks × 20ms = **940ms** total padding.

### ScummVM

```cpp
if (_chrono->_gameTick && _chrono->getFrameCount() % frameSkip == 0) {
    readChunk(videoFile, chunk);        // reads type 6
    switch (chunk.chunkType) {
    default:
        debug("Unknown chunk type");   // does nothing
        break;
    }
    // still goes through audio/subtitle checks and presentFrame
}
```

Each type 6 chunk consumes one chrono tick cycle. With frameSkip=2 at 55ms ticks:
- Each type 6 costs **~110ms** (or 220ms if subtitle active)

47 type 6 chunks × 110ms = **5,170ms** (5.2 seconds) extra delay.

**The type 6 chunks add 4.2 seconds MORE delay in ScummVM than the original.**

---

## Bug 4: Audio Channel System Mismatch

### Original Audio Channels (from render_subtitles decompilation)

**`/f` command (SFX):**
```c
// Frame 0: special channel 7
if (frame_counter == 0) {
    load_audio_for_subtitle(filename, 7);
    play_audio_sample();
} else {
    // Rotating channels 0-3
    stop_current_audio();
    cleanup_audio_channel();
    load_audio_for_subtitle(filename, audio_channel_index);
    play_audio_sample();
    audio_channel_index = (audio_channel_index + 1) & 3;  // cycle 0→1→2→3→0
}
```

**`/x` command (voice/speech):**
```c
// Busy-wait for channel 6 to be free
while (!check_audio_channel_ready(sound_driver_handle, 6)) {
    dos_yield();
}
// Stop previous, load, play on channel 6
if (sfx_channel_active != 0) {
    cleanup_audio_channel();
    free_buffer(0);
    sfx_channel_active = 0;
}
load_audio_for_subtitle(filename, 6);
play_audio_sample();
```

**`/c` command (CD music):**
```c
if (cd_audio_active != 0) {
    stop_current_audio();
    cleanup_audio_channel();
    free_buffer(0);
    cd_audio_active = 0;
}
int track = atoi_string(track_str);
load_audio_for_subtitle(cd_audio_track_table[track], 5);
play_audio_sample();
```

### ScummVM Audio

```cpp
// /x → voice on channel 0, with wait
while (_sound->isPlaying(0)) { delay; }
_sound->playSound(voiceBuffer, length, 0);

// /f → SFX on channel 1, no wait
_sound->playSound(sfxBuffer, length, 1);
```

### Key Differences

1. **Original uses channel 6 with busy-wait for voice**; ScummVM uses channel 0
2. **Original rotates channels 0-3 for SFX** allowing overlap; ScummVM uses single channel 1
3. **Original `/f` frame 0 uses channel 7** as a special case
4. The busy-wait behavior is similar (both block until audio finishes), but the channel architecture differs

---

## Bug 5: Frame Blackout Range Missing

### Original (copy_to_vga)

```c
void copy_to_vga(void) {
    memcpy_internal();  // copy frame data
    if ((frame_counter < 0x23b) || (0x29d < frame_counter)) {
        render_subtitles(frame_counter);
    }
    write_to_vga_memory();
    // subtitle delay...
}
```

Subtitles (and ALL audio triggers) are **skipped entirely** for frames 571-669 (0x23B-0x29D). No subtitles, no voice triggers, no SFX during this range.

### ScummVM

No such blackout range exists. Subtitles and audio are checked for all frames.

### Impact

Any SCR commands targeting frames 571-669 would fire in ScummVM but not in the original. Looking at the SCR data, there don't appear to be `/x` or `/f` commands in this range (the gap between `/x 559` and `/x 670`), so the main impact is that the `/c 570 32` CD music command would fire differently (frame 570 is just outside the range).

---

## Subtitle Extra Delay

### Original

After `write_to_vga_memory()`, if a subtitle was displayed:

```c
if (subtitle_displayed_flag != 0) {
    byte extra_delay = get_current_chunk_index(1);  // returns 1
    subtitle_end_time = current_timer_value + extra_delay;
    do {
        dos_yield();
    } while (current_timer_value <= subtitle_end_time);
}
```

`current_timer_value` is incremented by the INT 1Ch handler at **18.2 Hz** (~55ms per tick).
So the extra delay is **1 tick = ~55ms** per subtitle frame.

### ScummVM

Uses `frameSkip = 4` (vs 2 for non-subtitle frames), which doubles the inter-frame time.
With 55ms chrono ticks: 55ms × 4 = 220ms vs 55ms × 2 = 110ms.
Extra delay per subtitle: **110ms** (the difference between skip 4 and skip 2).

### Comparison

| | Original | ScummVM |
|--|----------|---------|
| Normal frame interval | 20ms | ~110ms |
| Subtitle extra delay | 55ms | 110ms |
| Effective subtitle frame time | 75ms | ~220ms |

---

## Frame Counting: How the Game Does It vs ScummVM

### Original Game (VISOR.EXE)

```
Chunk from buffer → process_frame():
  if type 1/2:
    decode → XOR → copy_to_vga() → render_subtitles(frame_counter) → VGA write
    frame_counter++
  else (type 6):
    return immediately (NO frame_counter increment, NO audio/subtitle check)
```

- `frame_counter` counts ONLY visual frames (types 1 and 2)
- Audio/subtitle triggers are INSIDE `copy_to_vga()` → `render_subtitles()`
- render_subtitles scans the ENTIRE SCR script from the beginning every frame
- Commands fire when `frame_number_in_SCR == frame_counter` (exact match)
- frame_counter is checked BEFORE incrementing

### ScummVM

```
readChunk() → switch type:
  case 1/2: processFrame(chunk, frameCounter++)  // post-increment
  case 4: loadPalette
  default: debug log
// Then ALWAYS check audio (regardless of chunk type):
if (_voiceEffect.contains(frameCounter)) { ... }
if (_sfxEffect.contains(frameCounter)) { ... }
presentFrame()
```

- `frameCounter` counts only visual frames (same as original) ← CORRECT
- Audio checks are OUTSIDE processFrame ← WRONG: fires for non-visual chunks too
- Audio checks use POST-INCREMENTED frameCounter ← WRONG: off by one
- Subtitle tracking uses `_currentSubtitleIndex` sequential scan ← matches original behavior mostly

---

## Original Speech Cutoff Issue

The original game has an issue where speech audio gets cut off towards the end. The root cause:

The `/x` command does `while (!check_audio_channel_ready(6)) { dos_yield(); }` — a busy-wait. If voice N starts playing on channel 6, and voice N+1's trigger frame arrives while voice N is still playing, the busy-wait blocks the entire frame processing pipeline. The frame timing counter (`next_frame_time`) continues advancing, but frames can't be processed until the wait completes.

This creates a cascade effect near the end of the video where many voices arrive in quick succession (frames 670, 675, 680 with VOC16_0Z, VOC16_1Z, VOC16_2Z), potentially causing the last voices to be cut short as the video reaches the type 3 end marker.

---

## Summary of Fixes Needed

| Bug | Fix |
|-----|-----|
| Off-by-one audio | Check audio BEFORE `frameCounter++`, or check at `frameCounter-1` |
| Type 6 duplicate triggers | Only check audio/subtitle when `chunk.chunkType == 1 || chunk.chunkType == 2` |
| Type 6 timing too slow | Process type 6 instantly (no timing gate), or reduce delay to 20ms |
| Missing frame blackout | Skip subtitle/audio for frames 571-669 |
| Audio channels | Use channel 6 for voice with proper busy-wait, rotate 0-3 for SFX |

---

## Ghidra Renames (VISOR.EXE)

### Functions Renamed

| Address | Old Name | New Name | Purpose |
|---------|----------|----------|---------|
| 0x00010028 | main_video_player | main_video_player | Main playback loop (already named) |
| 0x000107f3 | read_chunk_from_ssn | read_chunk_from_ssn | Sequential SSN chunk reader |
| 0x0001090a | set_vga_palette_from_chunk | set_vga_palette_from_chunk | Type 4 palette load |
| 0x00010961 | decode_block_copy_frame | decode_block_copy_frame | Type 2 decoder |
| 0x000109cc | decode_rle_frame | decode_rle_frame | Type 1 RLE decoder |
| 0x00010a3c | apply_xor_delta | apply_xor_delta | XOR current with previous |
| 0x00010a63 | process_frame | process_frame | Main frame dispatch |
| 0x00010b6e | copy_to_vga | copy_to_vga | Frame + subtitle → VGA |
| 0x00010be7 | write_to_vga_memory | write_to_vga_memory | Final VGA blit |
| 0x00010c17 | render_text_to_vga | render_text_to_vga | Bitmap font renderer |
| 0x00010ed4 | render_subtitles | render_subtitles | SCR command dispatcher |
| 0x0001175f | load_introsnd_dat | load_introsnd_dat | Load audio archive |
| 0x000119f1 | load_audio_for_subtitle | load_audio_for_subtitle | Load audio sample |
| 0x00011a83 | FUN_00011a83 | **setup_timer_interrupt_hook** | Install INT 1Ch handler |
| 0x00011abb | FUN_00011abb | **restore_timer_interrupt** | Restore INT 1Ch |
| 0x00011afe | allocate_frame_buffer | allocate_frame_buffer | Memory allocation |
| 0x00011b10 | FUN_00011b10 | **set_display_mode** | VGA mode setup |
| 0x00011b5f | FUN_00011b5f | **init_sound_driver** | Initialize audio |
| 0x000118cd | FUN_000118cd | **shutdown_sound_system** | Audio cleanup |
| 0x000127ae | cleanup_audio_channel | cleanup_audio_channel | Audio channel cleanup |
| 0x00012863 | play_audio_sample | play_audio_sample | Start audio playback |
| 0x000129e2 | stop_current_audio | stop_current_audio | Stop playing audio |
| 0x00012f85 | check_audio_channel_ready | check_audio_channel_ready | Poll channel status |
| 0x00013d72 | FUN_00013d72 | **verify_cdrom_driver** | CD-ROM driver check |
| 0x00013f22 | FUN_00013f22 | **verify_original_cd** | Anti-piracy CD check |
| 0x00014a8c | get_current_chunk_index | get_current_chunk_index | Get playback index |
| 0x00014c63 | FUN_00014c63 | **open_file** | DOS file open |
| 0x00014d3b | FUN_00014d3b | **file_seek_to_start** | Seek to beginning |
| 0x00014e37 | FUN_00014e37 | **file_read_bytes** | Read bytes from file |
| 0x00015002 | FUN_00015002 | **exit_program** | Exit to DOS |
| 0x00015050 | init_frame_buffer | init_frame_buffer | Buffer init/memset |
| 0x00015068 | get_timer_ticks | get_timer_ticks | Read centisecond timer |
| 0x0001506d | dos_yield | dos_yield | CPU yield (INT 28h) |
| 0x000150a6 | memcpy_video | memcpy_video | Memory copy |
| 0x000150cb | free_buffer | free_buffer | Free allocated memory |
| 0x00015129 | FUN_00015129 | **close_file** | DOS file close |
| 0x0001508f | FUN_0001508f | **check_user_key_press** | Keyboard input check |
| 0x000152cd | atoi_string | atoi_string | String to int |
| 0x00015281 | memcpy_internal | memcpy_internal | Internal memcpy |
| 0x00015421 | FUN_00015421 | **get_interrupt_vector** | DOS get vector |
| 0x00015455 | FUN_00015455 | **set_interrupt_vector** | DOS set vector |
| 0x0001c833 | get_bios_time_centiseconds | get_bios_time_centiseconds | DOS INT 21h AH=2Ch |
| 0x0001e6cf | call_dos_int21h | call_dos_int21h | Generic DOS INT 21h |
| 0x0001eab6 | FUN_0001eab6 | **set_display_font_mode** | Set font/display mode |
| 0x0001f016 | FUN_0001f016 | **set_text_cursor_position** | Position cursor |
| 0x0001f207 | FUN_0001f207 | **display_error_message** | Print error string |
| 0x00014a38 | FUN_00014a38 | **set_vga_resolution** | VGA resolution setup |

### Data Labels Renamed

| Address | New Name | Purpose |
|---------|----------|---------|
| 0x00033898 | next_frame_time | Target centisecond for next frame |
| 0x00033c9d | user_interrupt_flag | Set when ESC pressed |
| 0x000338d8 | audio_enabled | CD-ROM/audio system flag |
| 0x00033c6c | original_int1c_handler_offset | Saved INT 1Ch vector offset |
| 0x00033c70 | original_int1c_handler_segment | Saved INT 1Ch vector segment |
| 0x00033a80 | text_render_buffer_2 | Secondary text buffer |
| 0x000338a8 | font_file_handle | Handle for letras.bin |
| 0x000338ac | path_file_handle | Handle for path.dat |
| 0x00033d0c | chunk_header_buffer | Temp buffer for chunk headers |
| 0x000338c0 | chunk_data_offset | Current chunk's data_offset field |
| 0x0003040c | cd_audio_track_table | Track index → filename mapping |
| 0x00033c7c | is_first_audio_played | Flag for first frame audio |
| 0x00033c90 | chunk_secondary_size | Size of secondary chunk data |
| 0x00033c98 | chunk_primary_size | Size of primary chunk data |

(Previously renamed labels from earlier analysis sessions are also present: frame_counter, video_exit_flag, audio_channel_index, subtitle_displayed_flag, subtitle_end_time, current_timer_value, script_cursor, sound_driver_handle, sfx_channel_active, cd_audio_active, voice_channel_handles, voice_audio_buffers, current_frame_buffer, previous_frame_buffer, vga_display_buffer, text_render_buffer, font_data_buffer, script_data_buffer, palette_buffer, chunk_data_buffer, current_block_index, blocks_remaining, ssn_file_handle, scr_file_handle, chunks_in_buffer, playback_enabled, total_chunks_loaded, current_playback_frame, write_chunk_index, chunk_types, frame_buffer_ptrs, frame_buffer_sizes, delta_buffer_ptrs, delta_buffer_sizes)
