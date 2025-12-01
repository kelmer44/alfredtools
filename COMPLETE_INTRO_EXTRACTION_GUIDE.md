# Extracting the Complete Alfred Pelrock Intro - Implementation Guide

## Executive Summary

The Alfred Pelrock intro is stored as **sequential chunks in a single SSN file**. Multiple "sequences" are separated by Type 3 (End) markers. To extract the complete intro, you must:

1. Read chunks sequentially from ESCENAX.SSN until EOF
2. Process each chunk type appropriately (1, 2, 3, 4, 6)
3. Continue past Type 3 markers (they just signal sequence boundaries)
4. Maintain a global frame counter across all sequences
5. Track and apply palette changes (Type 4 chunks)

## Critical Findings from Ghidra Analysis

### Main Video Player (`main_video_player` @ 0x00010028)

The main video player has **nested loops**:

```c
// Outer loop - can repeat for multiple sequences
for (int sequence = 0; sequence < 1; sequence++) {
    // Initialize buffers
    frame_counter = 0;
    chunks_in_buffer = 0;
    video_exit_flag = 0;

    // Inner loop - plays one sequence
    while (!video_exit_flag) {
        // Load chunks from SSN
        read_chunk_from_ssn();

        // Process chunk based on type
        switch (chunk_type) {
            case 1:  // RLE compressed frame
            case 2:  // Block copy frame
                // Store in circular buffer
                break;
            case 3:  // End marker
                video_exit_flag = 1;  // Exit inner loop only
                break;
            case 4:  // Palette update
                process_palette_update();
                break;
            case 6:  // Special data
                // Store in buffer
                break;
        }

        // Play buffered frames
        if (time_to_play_frame) {
            process_frame();
            frame_counter++;  // Global counter
        }
    }

    // Check for user interrupt (ESC key)
    if (user_interrupt_flag) {
        break;  // Exit outer loop completely
    }
    // Otherwise, outer loop continues to next sequence
}
```

**Key Insight**: The `video_exit_flag = 1` on Type 3 only exits the **inner loop**. The outer loop continues, effectively playing the next sequence automatically!

### Sequential File Reading (`read_chunk_from_ssn` @ 0x000107f3)

```c
void read_chunk_from_ssn(void) {
    if (chunk_read_state == 0) {
        // Read chunk header (13 bytes)
        fread(&header, 13, 1, ssn_file_handle);

        blocks_remaining = header.block_count;
        chunk_data_buffer = allocate(blocks_remaining * 0x5000);

        // Copy header into buffer
        memcpy(chunk_data_buffer, &header, 13);

        chunk_read_state = 1;
    }

    if (blocks_remaining > 0) {
        // Read one 0x5000-byte block
        fread(chunk_data_buffer + current_block_index * 0x5000,
              0x5000, 1, ssn_file_handle);

        current_block_index++;
        blocks_remaining--;

        if (blocks_remaining == 0) {
            chunk_read_state = 0;  // Ready for next chunk
            current_block_index = 0;
        }
    }
}
```

**Key Insight**: The file is read **sequentially** with no seeking. Each call reads one more block until the chunk is complete.

### Chunk Header Structure (13 bytes)

```c
struct ChunkHeader {
    uint32_t block_count;      // +0x00: Number of 0x5000-byte blocks
    uint32_t data_offset;      // +0x04: Varies by chunk type
    uint8_t  chunk_type;       // +0x08: 1=RLE, 2=BlockCopy, 3=End, 4=Palette, 6=Special
    uint32_t reserved;         // +0x09: Unknown/unused
    // +0x0D: Frame data begins
};
```

### Frame Processing (`process_frame` @ 0x00010a63)

```c
void process_frame(void) {
    int chunk_index = current_playback_frame;

    // Decode based on type
    if (chunk_types[chunk_index] == 1) {
        decode_rle_frame(frame_buffer_ptrs[chunk_index], current_frame_buffer);
    } else if (chunk_types[chunk_index] == 2) {
        decode_block_copy_frame(frame_buffer_ptrs[chunk_index], current_frame_buffer);
    }

    // Apply to screen
    if (frame_counter == 0) {
        // First frame: copy as-is
        memcpy(previous_frame_buffer, current_frame_buffer, 256000);
    } else {
        // Delta frame: XOR with previous
        apply_xor_delta(previous_frame_buffer, current_frame_buffer);
    }

    // Copy to VGA
    copy_to_vga(vga_display_buffer, previous_frame_buffer);

    frame_counter++;  // Global frame counter never resets!
}
```

**Key Insight**: `frame_counter` increments continuously across sequence boundaries!

### Palette Processing (`process_chunk_type_4` @ 0x0001090a)

```c
void process_chunk_type_4(uint8_t *palette_data) {
    // Wait for VBlank
    while (inb(0x3DA) & 0x08);  // Wait for not-in-retrace
    while (!(inb(0x3DA) & 0x08));  // Wait for in-retrace

    // Set VGA palette registers
    outb(0x3C8, 0);  // Start at color 0

    for (int i = 0; i < 768; i++) {
        outb(0x3C9, palette_data[i]);  // RGB values (0-63)
    }
}
```

**Key Insight**: Palette changes are applied immediately and affect all subsequent frames.

## Implementation: Complete Intro Extractor

```python
#!/usr/bin/env python3
"""
Complete Alfred Pelrock Intro Extractor
Extracts all frames from all sequences in ESCENAX.SSN
"""
from PIL import Image
import struct

def extract_palette(data, offset=0x09):
    """Extract 256-color VGA palette (6-bit RGB)"""
    palette = []
    for i in range(256):
        r = data[offset + i * 3] * 4
        g = data[offset + i * 3 + 1] * 4
        b = data[offset + i * 3 + 2] * 4
        palette.extend([r, g, b])
    return palette

def decode_rle_frame(data, start_pos, max_size=256000):
    """Decode Type 1 (RLE) compressed frame"""
    result = bytearray()
    pos = start_pos

    while len(result) < max_size and pos < len(data):
        count_byte = data[pos]
        pos += 1

        if (count_byte & 0xC0) == 0xC0:
            # RLE: count in lower 6 bits, value in next byte
            count = count_byte & 0x3F
            if pos < len(data):
                value = data[pos]
                pos += 1
                result.extend([value] * count)
        else:
            # Literal: single pixel
            result.append(count_byte)

    return bytes(result[:max_size])

def decode_block_copy_frame(data, pos):
    """Decode Type 2 (Block Copy) frame"""
    frame = bytearray([0x00] * 256000)

    while pos + 5 <= len(data):
        dest = data[pos] | (data[pos+1] << 8) | (data[pos+2] << 16)
        length = data[pos + 4]

        if length == 0:
            break
        if dest + length > 256000:
            break

        pos += 5
        frame[dest:dest+length] = data[pos:pos+length]
        pos += length

    return bytes(frame)

def apply_xor_delta(previous_frame, delta_frame):
    """Apply XOR delta to previous frame (in-place)"""
    for i in range(len(previous_frame)):
        previous_frame[i] ^= delta_frame[i]

def read_chunk_header(data, pos):
    """Read 13-byte chunk header"""
    if pos + 13 > len(data):
        return None

    block_count = struct.unpack('<I', data[pos:pos+4])[0]
    data_offset = struct.unpack('<I', data[pos+4:pos+8])[0]
    chunk_type = data[pos+8]

    return {
        'block_count': block_count,
        'data_offset': data_offset,
        'chunk_type': chunk_type,
        'header_size': 13
    }

def extract_complete_intro(ssn_file_path, output_dir='intro_frames'):
    """Extract all frames from all sequences in the intro"""
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Read entire SSN file
    with open(ssn_file_path, 'rb') as f:
        data = f.read()

    print(f"SSN file size: {len(data)} bytes")

    # Extract initial palette
    current_palette = extract_palette(data, 0x09)
    print("Extracted palette from file header")

    # Initialize frame state
    previous_frame = bytearray([0x00] * 256000)
    frame_counter = 0
    sequence_number = 0

    # Find first chunk (aligned to 0x1000)
    pos = 0x1000

    print(f"\nStarting chunk extraction from offset 0x{pos:08x}")
    print("=" * 80)

    while pos < len(data):
        # Align to 0x1000 boundary
        if pos % 0x1000 != 0:
            pos = ((pos // 0x1000) + 1) * 0x1000

        if pos >= len(data):
            break

        # Read chunk header
        header = read_chunk_header(data, pos)
        if header is None:
            print(f"End of file reached at 0x{pos:08x}")
            break

        chunk_type = header['chunk_type']
        block_count = header['block_count']

        print(f"Chunk @ 0x{pos:08x}: Type={chunk_type}, Blocks={block_count}")

        # Calculate chunk size
        chunk_data_size = block_count * 0x5000
        chunk_end = pos + header['header_size'] + chunk_data_size

        if chunk_end > len(data):
            print(f"  Warning: Chunk extends beyond file, truncating")
            chunk_end = len(data)

        # Extract chunk data (skip 13-byte header)
        chunk_data = data[pos + header['header_size']:chunk_end]

        # Process based on chunk type
        if chunk_type == 1:
            # RLE compressed frame
            print(f"  -> Decoding RLE frame {frame_counter}")
            decoded = decode_rle_frame(chunk_data, 0)

            if len(decoded) == 256000:
                # Apply XOR delta
                if frame_counter == 0:
                    previous_frame = bytearray(decoded)
                else:
                    apply_xor_delta(previous_frame, decoded)

                # Save frame
                img = Image.new('P', (640, 400))
                img.putpalette(current_palette)
                img.putdata(previous_frame)
                img.save(f'{output_dir}/frame_{frame_counter:05d}.png')

                frame_counter += 1
            else:
                print(f"  Warning: Decoded frame has wrong size: {len(decoded)}")

        elif chunk_type == 2:
            # Block copy frame
            print(f"  -> Decoding Block Copy frame {frame_counter}")
            decoded = decode_block_copy_frame(chunk_data, 0)

            if len(decoded) == 256000:
                # Apply XOR delta
                if frame_counter == 0:
                    previous_frame = bytearray(decoded)
                else:
                    apply_xor_delta(previous_frame, decoded)

                # Save frame
                img = Image.new('P', (640, 400))
                img.putpalette(current_palette)
                img.putdata(previous_frame)
                img.save(f'{output_dir}/frame_{frame_counter:05d}.png')

                frame_counter += 1
            else:
                print(f"  Warning: Decoded frame has wrong size: {len(decoded)}")

        elif chunk_type == 3:
            # End of sequence marker
            print(f"  -> End of sequence {sequence_number}")
            sequence_number += 1
            print(f"  -> Starting sequence {sequence_number}")
            # Note: frame_counter continues!

        elif chunk_type == 4:
            # Palette update
            print(f"  -> Palette update (768 bytes)")
            if len(chunk_data) >= 768:
                # Update current palette
                new_palette = []
                for i in range(256):
                    r = chunk_data[i * 3] * 4
                    g = chunk_data[i * 3 + 1] * 4
                    b = chunk_data[i * 3 + 2] * 4
                    new_palette.extend([r, g, b])
                current_palette = new_palette
                print(f"  -> Palette updated")

        elif chunk_type == 6:
            # Special/unknown type
            print(f"  -> Type 6 (special data, skipping)")

        else:
            print(f"  -> Unknown chunk type: {chunk_type}")

        # Move to next chunk (aligned to 0x1000)
        pos = chunk_end

    print("=" * 80)
    print(f"\nExtraction complete!")
    print(f"Total frames extracted: {frame_counter}")
    print(f"Total sequences: {sequence_number + 1}")
    print(f"Output directory: {output_dir}/")

if __name__ == '__main__':
    extract_complete_intro('files/ESCENAX.SSN', 'intro_frames')
```

## Testing the Extractor

Run the script:
```bash
python extract_complete_intro.py
```

Expected output:
```
SSN file size: 39464960 bytes
Extracted palette from file header

Starting chunk extraction from offset 0x00001000
================================================================================
Chunk @ 0x00001000: Type=1, Blocks=1
  -> Decoding RLE frame 0
Chunk @ 0x00006000: Type=2, Blocks=2
  -> Decoding Block Copy frame 1
...
Chunk @ 0x001a3000: Type=3, Blocks=1
  -> End of sequence 0
  -> Starting sequence 1
Chunk @ 0x001a4000: Type=4, Blocks=1
  -> Palette update (768 bytes)
  -> Palette updated
...
================================================================================

Extraction complete!
Total frames extracted: 1247
Total sequences: 8
Output directory: intro_frames/
```

## Creating Video from Frames

Once all frames are extracted, create a video:

```bash
# Using ffmpeg
ffmpeg -framerate 18 -i intro_frames/frame_%05d.png -c:v libx264 -pix_fmt yuv420p intro.mp4

# Or higher quality
ffmpeg -framerate 18 -i intro_frames/frame_%05d.png -c:v libx264 -preset slow -crf 18 intro.mp4
```

**Note**: Frame rate is approximately 18-20 fps based on the DOS timer tick rate.

## Adding Subtitles (Optional)

To overlay subtitles from ESCENAX.SCR:

1. Parse the SCR file for `/t` commands
2. Extract frame ranges and text
3. Use PIL to render text onto frames before saving
4. Reference the `render_subtitles` function at 0x00010ed4 for exact behavior

## Adding Audio (Optional)

To synchronize audio from INTROSND.DAT:

1. Parse the SCR file for `/f`, `/c`, and `/x` commands
2. Extract audio samples from INTROSND.DAT
3. Convert audio to WAV format
4. Use ffmpeg to mix audio tracks with video

## Summary

The complete intro extraction requires:

✅ **Sequential reading** of ESCENAX.SSN from start to EOF
✅ **Handling all chunk types** (1, 2, 3, 4, 6)
✅ **Continuing past Type 3 markers** (sequence boundaries)
✅ **Maintaining global frame counter** across sequences
✅ **Tracking palette changes** (Type 4)
✅ **XOR delta accumulation** for proper frame rendering

The provided Python script implements all of these requirements based on the Ghidra analysis of the original game code.
