#!/usr/bin/env python3
"""
Systematically extract BUDA ranges to find 640x400 screens
"""

import sys
from pathlib import Path
from PIL import Image

def decompress_rle(data, offset, end_offset):
    size = end_offset - offset
    if size == 0x8000 or size == 0x6800:
        # Uncompressed block - read directly
        return data[offset:offset+size]
    result = bytearray()
    pos = offset
    while pos + 2 <= min(end_offset, len(data)):
        if pos + 4 <= len(data) and data[pos:pos+4] == b'BUDA':
            pos+=4
            continue
        count = data[pos]
        value = data[pos + 1]
        result.extend([value] * count)
        pos += 2
    return bytes(result)


def main():
    alfred7 = sys.argv[1] if len(sys.argv) > 1 else "ALFRED.7"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "buda_scan"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with open(alfred7, 'rb') as f:
        data = f.read()


    raw = decompress_rle(data, 0, len(data))
    output_file = f'decompressed_alfred7.bin'
    with open(output_file, 'wb') as f:
        f.write(raw)

if __name__ == "__main__":
    main()
