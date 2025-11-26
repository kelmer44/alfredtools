#!/usr/bin/env python3
"""
Alfred Pelrock - Sound Extractor (Raw PCM - Final)

Based on analysis: The .SMP files ARE 8-bit PCM, but stored as RAW SIGNED PCM.
Miles Sound System format 0x05 = 8-bit signed PCM.

The issue with previous attempts: We were converting unsigned to signed, but the
data is ALREADY signed (-128 to 127, not 0-255).
"""

import struct
import sys
from pathlib import Path
import wave

def parse_smp_header(data):
    """Parse SMP file header if present"""
    if len(data) < 128 or data[0] != 0x01 or data[1] != 0x2e:
        return False, 11025, len(data), 0

    sample_rate = struct.unpack('<I', data[0x1c:0x20])[0]

    # Sanity check
    if sample_rate < 4000 or sample_rate > 50000:
        sample_rate = 11025

    # Header is 80 bytes for format 0x05 files
    return True, sample_rate, 0, 80

def save_as_wav(pcm_data, output_file, sample_rate):
    """Save 8-bit SIGNED PCM as WAV file (no conversion needed!)"""
    with wave.open(str(output_file), 'wb') as wav:
        wav.setnchannels(1)
        wav.setsampwidth(1)  # 8-bit
        wav.setframerate(sample_rate)
        # Write data AS-IS - it's already signed 8-bit PCM
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

    print("Alfred Pelrock - Sound Extractor (Raw Signed PCM)")
    print("=" * 80)
    print(f"Archive: {sonidos_path}")
    print(f"Files: {file_count}")
    print()
    print("Format: 8-bit SIGNED PCM (Miles Sound System format 0x05)")
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

    # Extract files
    success_count = 0

    for i, file_info in enumerate(files):
        name = file_info['name']
        file_offset = file_info['offset']
        size = file_info['size']

        # Skip very small files
        if size < 200:
            print(f"{i+1:3d}. {name:20s} SKIPPED (only {size} bytes)")
            continue

        # Extract raw data
        sound_data = data[file_offset:file_offset+size]

        # Parse header
        has_header, sample_rate, _, data_offset = parse_smp_header(sound_data)
        audio_data = sound_data[data_offset:]

        # Save as WAV with NO CONVERSION - data is already signed PCM
        wav_file = output_path / (Path(name).stem + '.wav')
        save_as_wav(audio_data, wav_file, sample_rate)

        header_str = f"{data_offset:3d}B hdr" if has_header else "raw      "
        print(f"{i+1:3d}. {name:20s} -> {wav_file.name:25s} {sample_rate:5d} Hz ({header_str})")
        success_count += 1

    print("-" * 80)
    print(f"Successfully extracted {success_count}/{len(files)} files")
    print(f"Output directory: {output_path.absolute()}")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print()
        print("Usage: python extract_sounds_final.py <SONIDOS.DAT> [output_dir]")
        sys.exit(1)

    sonidos_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "sounds_final"

    if not Path(sonidos_path).exists():
        print(f"Error: File not found: {sonidos_path}")
        sys.exit(1)

    extract_sounds(sonidos_path, output_dir)

if __name__ == "__main__":
    main()
