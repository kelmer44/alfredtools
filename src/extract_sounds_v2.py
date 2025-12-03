#!/usr/bin/env python3
"""
Alfred Pelrock - Sound Extractor v2

Extracts all sound files from SONIDOS.DAT and converts them to playable WAV format.

Supported formats in SONIDOS.DAT:
1. RIFF WAV (magic: 52 49 "RI") - already standard WAV, just extract
2. AIL/Miles Sound System (magic: 01 2e) - 80 byte header, sample rate at 0x1c
3. Other AIL variants (magic: 01 XX) - 80 byte header
4. Raw 8-bit signed PCM (magic: 7x/8x) - no header, default 11025 Hz
5. Silence placeholders (size <= 100) - skip or generate silence

Usage:
    python extract_sounds_v2.py <SONIDOS.DAT> [output_dir]
"""

import struct
import sys
import wave
from pathlib import Path


def detect_format(data):
    """
    Detect the audio format from the file header.

    Returns: (format_type, sample_rate, header_size)
    """
    if len(data) < 16:
        return ('too_small', 11025, 0)

    byte0, byte1 = data[0], data[1]
    magic_2 = data[0:2]
    magic_4 = data[0:4]

    # RIFF WAV format
    if magic_4 == b'RIFF':
        # Standard WAV - sample rate at offset 24 (0x18) in WAV structure
        # But in our case it seems to be at 0x1c based on analysis
        if len(data) >= 0x20:
            sample_rate = struct.unpack('<I', data[0x18:0x1c])[0]
            if not (4000 <= sample_rate <= 48000):
                sample_rate = 11025
        else:
            sample_rate = 11025
        return ('riff_wav', sample_rate, 0)  # Keep full RIFF, no header skip

    # AIL/Miles Sound System format (01 2e)
    if byte0 == 0x01 and byte1 == 0x2e:
        sample_rate = 11025
        if len(data) >= 0x20:
            rate = struct.unpack('<I', data[0x1c:0x20])[0]
            if 4000 <= rate <= 48000:
                sample_rate = rate
        return ('ail_miles', sample_rate, 80)  # 80 byte header

    # Other AIL variants (01 XX where XX is ASCII letter)
    if byte0 == 0x01 and 0x40 <= byte1 <= 0x7f:
        # These have varying header sizes, try to find sample rate
        sample_rate = 11025
        if len(data) >= 0x14:
            # Try offset 0x10 which seems common for these
            rate = struct.unpack('<I', data[0x10:0x14])[0]
            if 4000 <= rate <= 48000:
                sample_rate = rate
        return ('ail_other', sample_rate, 80)  # Assume 80 byte header

    # ScreamTracker module
    if magic_2 == b'ST':
        return ('st3_module', 0, 0)  # Don't convert, just copy

    # Silence/placeholder (all zeros or very small)
    if len(data) <= 100:
        return ('silence', 11025, 0)

    # Raw 8-bit signed PCM (first bytes are audio samples, typically around 0x7f-0x81)
    if 0x70 <= byte0 <= 0x90 or byte0 == 0x00:
        return ('raw_pcm', 11025, 0)

    # Unknown format - treat as raw PCM
    return ('unknown', 11025, 0)


def save_as_wav(pcm_data, output_file, sample_rate):
    """
    Save 8-bit PCM data as WAV file.

    Note: The SMP files store data that works correctly when written as-is.
    Do NOT convert signed<->unsigned - the original extractor confirmed this.
    """
    with wave.open(str(output_file), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)  # 8-bit
        wav.setframerate(sample_rate)
        wav.writeframes(pcm_data)


def extract_sounds(sonidos_path, output_dir):
    """Extract all sound files from SONIDOS.DAT"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(sonidos_path, 'rb') as f:
        data = f.read()

    # Parse PACK header
    magic = data[0:4]
    if magic != b'PACK':
        print(f"Error: Invalid magic bytes: {magic}")
        return

    file_count = struct.unpack('<I', data[4:8])[0]

    print("Alfred Pelrock - Sound Extractor v2")
    print("=" * 80)
    print(f"Archive: {sonidos_path}")
    print(f"Files: {file_count}")
    print()
    print("-" * 80)
    print(f"{'#':>3} {'Filename':<20} {'Size':>8} {'Format':<12} {'Rate':>6} {'Output':<25}")
    print("-" * 80)

    # Parse directory
    offset = 8
    files = []

    for i in range(file_count):
        name_end = data.find(b'\x00', offset)
        if name_end == -1:
            break

        filename = data[offset:name_end].decode('ascii', errors='ignore')
        offset = name_end + 1

        file_offset = struct.unpack('<I', data[offset:offset+4])[0]
        file_size = struct.unpack('<I', data[offset+4:offset+8])[0]
        offset += 8

        files.append({
            'name': filename,
            'offset': file_offset,
            'size': file_size
        })

    # Extract and convert files
    success_count = 0
    skip_count = 0

    for i, file_info in enumerate(files):
        name = file_info['name']
        file_offset = file_info['offset']
        size = file_info['size']

        # Extract raw data
        sound_data = data[file_offset:file_offset+size]

        # Detect format
        fmt, sample_rate, header_size = detect_format(sound_data)

        # Determine output filename
        stem = Path(name).stem

        if fmt == 'silence' or size <= 100:
            print(f"{i+1:3d} {name:<20} {size:>8} {'SKIP':<12} {'-':>6} {'(silence/placeholder)':<25}")
            skip_count += 1
            continue

        if fmt == 'st3_module':
            # Copy ST3 file as-is
            out_file = output_path / name
            with open(out_file, 'wb') as f:
                f.write(sound_data)
            print(f"{i+1:3d} {name:<20} {size:>8} {'ST3':<12} {'-':>6} {out_file.name:<25}")
            success_count += 1
            continue

        if fmt == 'riff_wav':
            # Already a WAV file - just save it
            out_file = output_path / (stem + '.wav')
            with open(out_file, 'wb') as f:
                f.write(sound_data)
            print(f"{i+1:3d} {name:<20} {size:>8} {'RIFF/WAV':<12} {sample_rate:>6} {out_file.name:<25}")
            success_count += 1
            continue

        # For AIL and raw formats, extract audio data and convert to WAV
        if fmt in ('ail_miles', 'ail_other'):
            audio_data = sound_data[header_size:]
            fmt_str = 'AIL/Miles' if fmt == 'ail_miles' else 'AIL/other'
        else:
            audio_data = sound_data
            fmt_str = 'Raw PCM'

        if len(audio_data) < 10:
            print(f"{i+1:3d} {name:<20} {size:>8} {'SKIP':<12} {'-':>6} {'(no audio data)':<25}")
            skip_count += 1
            continue

        # Save as WAV
        out_file = output_path / (stem + '.wav')
        save_as_wav(audio_data, out_file, sample_rate)

        print(f"{i+1:3d} {name:<20} {size:>8} {fmt_str:<12} {sample_rate:>6} {out_file.name:<25}")
        success_count += 1

    print("-" * 80)
    print(f"Extracted: {success_count} files")
    print(f"Skipped: {skip_count} files (silence/placeholder)")
    print(f"Output directory: {output_path.absolute()}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    sonidos_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "sounds_extracted"

    if not Path(sonidos_path).exists():
        print(f"Error: File not found: {sonidos_path}")
        sys.exit(1)

    extract_sounds(sonidos_path, output_dir)


if __name__ == "__main__":
    main()
