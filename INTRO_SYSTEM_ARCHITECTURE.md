# Alfred Pelrock Intro System Architecture

## Overview

The intro video system in Alfred Pelrock is a sophisticated multi-layered system that coordinates video playback, audio, and subtitles. The system is centered around the `main_video_player` function at address `0x00010028`.

## File Components

### 1. ESCENAX.SSN - Video Data
- **Size**: 37.64 MB (39,464,960 bytes)
- **Format**: Custom chunked video format with multiple sequences
- **Content**: 687 video chunks throughout the file
- **Structure**: Each chunk is aligned to 0x1000 byte boundaries (4096 bytes)

### 2. ESCENAX.SCR - Script/Subtitle Data
- **Purpose**: Controls subtitle timing, text rendering, and audio synchronization
- **Format**: Text-based script with markers
- **Loaded at startup**: Read into `script_data_buffer` (10,000 bytes allocated)

### 3. INTROSND.DAT - Audio Data
- **Purpose**: Contains audio samples for voices, sound effects, and music
- **Format**: Custom audio format
- **Loaded conditionally**: Only loaded if CD-ROM is present (`DAT_000338d8 != 0`)

### 4. path.dat - Path Configuration
- **Purpose**: Likely configures file paths for different data files
- **Usage**: Loaded at startup to populate path strings

## System Architecture

### Main Video Player Loop (`main_video_player` @ 0x00010028)

The main video player implements a **producer-consumer buffering system**:

#### Initialization Phase:
1. Load `path.dat` to configure file paths
2. Allocate frame buffers:
   - `current_frame_buffer`: 0x3e800 bytes (256,000 bytes = 640×400)
   - `previous_frame_buffer`: 0x3e800 bytes
   - `vga_display_buffer`: 0x3e800 bytes
   - `text_render_buffer`: 100,000 bytes
   - `font_data_buffer`: 0x12c0 bytes (4,800 bytes for font glyphs)
   - `script_data_buffer`: 10,000 bytes
   - `palette_buffer`: 0x300 bytes (768 bytes = 256 colors × 3 RGB)
3. Load `letras.bin` (font data)
4. Open SSN and SCR files
5. Load INTROSND.DAT if CD-ROM is present

#### Main Playback Loop:
```
while (!video_exit_flag) {
    // Check for user interrupt (ESC key)
    if (user_pressed_key()) {
        video_exit_flag = true;
    }

    // Buffer management
    if (chunks_in_buffer == 0x13) {  // Max 19 chunks buffered
        playback_enabled = false;     // Stop playback if buffer full
    } else if (total_chunks_loaded > 10) {
        playback_enabled = true;      // Start playback after buffering 10 chunks
    }

    // Frame playback (timing-based)
    if (time_elapsed() && playback_enabled && chunks_in_buffer > 0) {
        current_playback_frame++;
        process_frame();              // Decode and display frame
        if (current_playback_frame == 0x14) {  // Circular buffer of 20 slots
            current_playback_frame = 0;
        }
        chunks_in_buffer--;
    }

    // Chunk loading (async buffering)
    if (chunks_in_buffer < 0xf) {     // Keep buffer reasonably full
        read_chunk_from_ssn();
        if (chunk_loaded) {
            process_chunk_header();
            store_in_circular_buffer();
            chunks_in_buffer++;
            total_chunks_loaded++;
        }
    }
}
```

### Chunk Types and Processing

The system handles 6 different chunk types:

#### Type 1: RLE Compressed Frame
- **Purpose**: Full or delta frame with Run-Length Encoding compression
- **Processing**:
  - `decode_rle_frame()` decompresses data
  - If first frame (`frame_counter == 0`): copy to `previous_frame_buffer`
  - If delta frame: `apply_xor_delta()` with previous frame
  - `copy_to_vga()` to display buffer

#### Type 2: Block Copy Frame
- **Purpose**: Uncompressed or lightly compressed frame data
- **Processing**: Similar to Type 1 but uses `decode_block_copy_frame()`

#### Type 3: End Marker
- **Purpose**: Signals end of video sequence
- **Processing**: Sets `video_exit_flag = 1` to exit loop

#### Type 4: Palette Update
- **Purpose**: Changes the color palette (768 bytes = 256 colors × 3 RGB)
- **Processing**: `process_chunk_type_4()` waits for VBlank and updates VGA palette registers
- **Hardware Access**: Writes to ports 0x3C8 and 0x3C9

#### Type 6: Special/Unknown
- **Purpose**: Not fully documented, appears to be data-only chunks
- **Processing**: Stored in delta buffer array

### Circular Buffer System

The system uses **two parallel circular buffers**:

1. **Frame Buffer Array**: 20 slots for decoded frame data
   - `frame_buffer_ptrs[20]`: Pointers to allocated buffers
   - `frame_buffer_sizes[20]`: Size of each buffer

2. **Delta Buffer Array**: 20 slots for XOR delta data
   - `delta_buffer_ptrs[20]`: Pointers to allocated buffers
   - `delta_buffer_sizes[20]`: Size of each buffer

3. **Chunk Type Array**: Tracks what type each chunk is
   - `chunk_types[20]`: Type identifier (1, 2, 4, 6, etc.)

**Indices**:
- `write_chunk_index`: Where to write next loaded chunk (0-19)
- `current_playback_frame`: Which frame is currently being played (0-19)
- `chunks_in_buffer`: How many chunks are ready to play

### Frame Decoding Pipeline (`process_frame` @ 0x00010a63)

```
1. Get chunk type from circular buffer
2. If Type 1 (RLE):
   - decode_rle_frame(compressed_data, current_frame_buffer)
3. If Type 2 (Block Copy):
   - decode_block_copy_frame(compressed_data, current_frame_buffer)
4. Apply frame to screen:
   - If frame_counter == 0 (first frame):
       memcpy(previous_frame_buffer, current_frame_buffer)
   - Else (delta frame):
       apply_xor_delta(previous_frame_buffer, current_frame_buffer)
5. copy_to_vga(vga_display_buffer, previous_frame_buffer)
6. frame_counter++
```

**Important**: No smoothing filter exists between XOR delta application and VGA copy.

## Subtitle System (`render_subtitles` @ 0x00010ed4)

The script file (ESCENAX.SCR) contains command markers that synchronize subtitles and audio with video frames.

### Script Command Format

The script parser searches for commands starting with `/`:

#### `/t` - Text/Subtitle Command
```
Format: /t[start][end][x][y][text]
- start: 4 bytes - starting frame number
- end: 4 bytes - ending frame number
- x: 4 bytes - X coordinate for text
- y: 4 bytes - Y coordinate for text
- text: Variable length string until next command or '*'
```

**Processing**:
- Check if current frame is between `start` and `end`
- If yes: call `render_text_to_vga(text, 0, x, y)`
- Sets `DAT_00033c84 = 1` to indicate subtitle is active

#### `/f` - Voice/Audio File Command
```
Format: /f[frame][filename]
- frame: 4 bytes - frame number to trigger
- filename: 12 bytes - audio filename to play
```

**Processing**:
- If current frame matches trigger frame:
  - First frame (frame == 0): Just load and play
  - Other frames: Stop previous audio, load new audio
- Calls `load_audio_for_subtitle(filename, channel)`
- Calls `play_audio_sample()` to start playback
- Uses cycling buffer of 4 audio channels

#### `/c` - Sound Effect Command
```
Format: /c[frame][sound_id]
- frame: 4 bytes - frame number to trigger
- sound_id: 4 bytes - index into sound effect table
```

**Processing**:
- If current frame matches trigger frame:
  - Stop previous sound effect (if playing)
  - Load sound from `sound_table[sound_id]`
  - Play on channel 5

#### `/x` - Special Audio Command
```
Format: /x[frame][filename]
- frame: 4 bytes - frame number to trigger
- filename: 12 bytes - audio filename
```

**Processing**:
- Similar to `/f` but uses channel 6
- Includes a blocking wait: `while (!audio_ready(channel_6)) { wait(); }`
- May be used for critical audio that must complete

### Text Rendering (`render_text_to_vga` @ 0x00010c17)

Complex bitmap font rendering system:

1. **Clear text buffer**: Fill with 0xFF (transparent)
2. **Parse text**:
   - Handle special control codes:
     - `0x08`: Set color (next byte is color index)
     - `0xFA`: Unknown (2-byte command)
     - `0xF6`: Newline
     - `0x0D`: End of text / render command
   - Calculate text dimensions
3. **Render glyphs**:
   - Each glyph is 12×24 pixels (0x30 bytes in font data)
   - Font data uses 2 bytes per row (12 bits used)
   - Render with 3-pixel shadow/outline
4. **Composite to VGA buffer**:
   - Only pixels not marked 0xFF are rendered
   - Respects transparency for subtitle overlays

## Audio System

### Audio Channels

The system supports **multiple concurrent audio channels**:

- **Channels 0-3**: Voice/dialog files (cycled via `DAT_00033c73`)
- **Channel 5**: Sound effects
- **Channel 6**: Special/blocking audio
- **Channel 7**: Music/ambient (inferred from `/f` command usage)

### Audio Loading (`load_audio_for_subtitle` @ 0x000119f1)

1. Load audio file from INTROSND.DAT
2. Get audio buffer information
3. If repeating audio: set `repeat_count = 0`
4. Store audio handle in channel buffer array

### Audio Playback (`play_audio_sample` @ 0x00012863)

1. Find free audio slot (or oldest slot if all busy)
2. Calculate sample rate conversion
3. Set up audio registers:
   - Volume
   - Panning
   - Sample rate
   - Buffer pointers
4. Start playback
5. Increment global audio counter

## Sequence Management

### How Multiple Sequences Form Complete Intro

The intro video is **NOT** a single continuous video. Instead:

1. **Single SSN File**: ESCENAX.SSN contains all sequences in one file
2. **Sequential Reading**: `read_chunk_from_ssn()` reads chunks sequentially from start to end
3. **Type 3 Marker**: End of each sequence is marked with a Type 3 chunk
4. **Automatic Continuation**: After Type 3, the outer loop resets and continues:
   ```c
   if (chunk_type == 3) {
       video_exit_flag = 1;  // Exit inner loop
   }
   // Outer loop may restart for next sequence
   ```

5. **Script Synchronization**: ESCENAX.SCR contains commands for ALL sequences
   - Frame numbers are **sequential across all sequences**
   - Parser searches entire script for commands matching current frame

### Multi-Sequence Playback Flow

```
Main Loop (can repeat):
    Initialize buffers
    frame_counter = 0

    Inner Loop:
        Load chunks from SSN file
        Process frames
        Render subtitles based on frame_counter

        If chunk type == 3:
            Break inner loop

    Cleanup buffers

    If user_interrupt:
        Break main loop
    Else:
        Continue to next sequence (inner loop repeats)
```

**Key Insight**: The system reads the SSN file **linearly** from beginning to end. Multiple "sequences" are just different sections of the same file, separated by Type 3 markers. The script file coordinates everything using global frame numbers.

## Timing System

The video player uses a **frame-rate limiter**:

1. `DAT_00033898 = current_time() + 2`
2. Before playing next frame: `if (current_time() >= DAT_00033898)`
3. After playing frame: `DAT_00033898 = current_time() + 2`

This creates approximately **30-36 fps** playback (DOS timer ticks at ~18.2 Hz, +2 ticks ≈ 0.11 seconds per frame).

## Memory Management

### Buffer Allocation:
- All buffers allocated via `allocate_frame_buffer(size)`
- Buffers freed with `free_buffer(ptr)`
- Circular buffer slots reused: old buffer freed before allocating new

### Frame Persistence:
- **Current frame**: Temporary decode buffer
- **Previous frame**: Kept for XOR delta calculations
- **VGA buffer**: Final composited output with subtitles

## CD-ROM Detection

The system has optional CD-ROM support:

```c
if (DAT_000338d8 != 0) {  // CD-ROM enabled flag
    // Check for CD-ROM driver
    // Verify original CD is inserted
    // Load INTROSND.DAT from CD
}
```

If CD-ROM is not present, intro likely runs **silently** (no audio).

## Error Handling

The system includes Spanish error messages:
- "No encuentro el driver del CD-ROM" (Can't find CD-ROM driver)
- "Por favor, inserte el CD ORIGINAL del juego" (Please insert the original game CD)

On error, the system:
1. Displays error via `FUN_0001f207()`
2. Loads and displays `err.int` (error intro)
3. Exits with `FUN_00015002(0)`

## Summary: Complete Intro Extraction Requirements

To extract the **entire intro**, you need to:

1. **Parse ESCENAX.SSN sequentially** from beginning to end
2. **Handle all chunk types** (1, 2, 3, 4, 6)
3. **Track frame counter globally** across Type 3 boundaries
4. **Parse ESCENAX.SCR** for subtitle/audio synchronization data
5. **Extract Type 4 palette changes** and apply them
6. **Decode both Type 1 (RLE) and Type 2 (Block Copy)** frames
7. **Continue reading past Type 3 markers** until end of file

The current script only extracts the **first frame of the first sequence**. A complete extractor would need to:
- Loop through all chunks until EOF
- Reset state (but not frame counter) on Type 3
- Save each decoded frame as PNG
- Track palette changes and apply to subsequent frames
- Optionally render subtitles from SCR file onto frames
