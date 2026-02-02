# ALFRED.7 Complete Extraction Summary

## Overview
Successfully mapped and extracted the entirety of ALFRED.7 (3,571,728 bytes).

## Extraction Results

### Extracted Content
- **78 BUDA compressed images/animations** → PNG files
- **15 Direct bitmap regions** → 41 PNG files (including multi-frame animations)
- **12 Palette entries** → .bin (raw) + .png (color swatches)
- **22 Raw binary regions** → .bin files

### Coverage Statistics
- **Total mapped: 3,254,082 bytes (91.11%)**
- **Previously unmapped: 317,646 bytes (8.89%)** - now all extracted as raw binaries

## File Structure

### Output Directory: `output_alfred7_complete/`
```
output_alfred7_complete/
├── buda0_CUADROCAMA/ ... buda195_CREDITOS/  (78 BUDA directories)
├── direct/                                    (15 direct bitmap regions)
│   ├── entry_0/ through entry_14/
│   └── Contains 41 PNG files total (multi-frame animations)
├── palettes/                                  (12 palette extractions)
│   ├── entry_8_558009/ through entry_29_2971796/
│   └── Each contains: .bin (raw palette) + .png (color swatch visualization)
└── raw/                                       (22 raw binary regions)
    ├── entry_0_0/ through entry_33_3271450/
    └── All unmapped byte sequences as .bin files
```

## Key Mapped Regions

### Named Content
- **File header** (0x000000, 260 bytes) - File format header
- **Library books** (0x309E0, 13,606 bytes) - Spanish library database
- **English books** (1361215, 13,593 bytes) - English library database
- **Code snippets** (1038909, 672 bytes) - Cursor handler code

### Palettes
All 768-byte palette regions properly identified and extracted:
- BUDA 48 palette (558009)
- BUDA 49 palette (558913)
- BUDA 68 palette (909325)
- BUDA 86 palette (1147077)
- BUDA 94 palette (1267951)
- BUDA 106 palette (1425348)
- BUDA 107 palette (1446090)
- BUDA 143 palette (2284674)
- BUDA 153 palette (2321060)
- BUDA 173 palette (2833272)
- BUDA 181 palette (2971796)
- Plus one unidentified palette (1040445)

### Large Regions
- **Large unknown gap** (0x30A8B4, 33,330 bytes) - Purpose unknown
- **Very large gap** (0x31EB1A, 256,004 bytes) - ~250KB, likely image or code

## BUDA Compression Format

RLE compression terminates at "BUDA" marker (0x42554441). Each BUDA entry:
- Start offset from file beginning
- Optional offset adjustment (e.g., +768 for palette skip)
- Compressed until next BUDA or EOF
- Multi-frame animations use `isContinued` flag to chain multiple BUDAs

## Script Updates

### extract_alfred7_bruteforce.py
Updated to:
1. ✅ Map all 34 previously unmapped byte sequences
2. ✅ Identify palettes (768-byte regions) automatically
3. ✅ Extract palettes as both .bin and .png (color swatch)
4. ✅ Extract all raw regions as .bin files
5. ✅ Maintain existing BUDA and direct bitmap extraction

### Usage
```bash
python3 src/extract_alfred7_bruteforce.py files/ALFRED.7 output_alfred7_complete
```

## Complete Coverage Achieved
Every byte of ALFRED.7 is now accounted for and extracted in an appropriate format:
- Compressed images → PNG
- Direct bitmaps → PNG
- Palettes → .bin + .png
- Unknown data → .bin

No gaps remain unmapped.
