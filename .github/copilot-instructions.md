# Copilot Instructions for alfredtools

## Project Overview
Reverse engineering toolkit for **Alfred Pelrock** (1997 DOS point-and-click adventure game). Primary goal: complete ScummVM reimplementation.

## CRITICAL: Inviolable Rules

These rules have the highest priority and must never be violated.

1. **File Editing**: NEVER use `cat <<EOF`or heredocs, especially python. They break the terminal.

2. **Output to file**: IF you find you cant read the terminal output, THEN output to a file and read that file, don't keep trying to read the terminal output.


## Architecture

### Game Data Files (in `files/`)
| File | Purpose | Size |
|------|---------|------|
| ALFRED.1 | Room data (backgrounds, sprites, text, hotspots, walkboxes, exits) | 12.9MB |
| ALFRED.2 | Character talking animations (RLE compressed) | 2.1MB |
| ALFRED.3 | Character movement animations | 311KB |
| ALFRED.4 | UI graphics (popups, speech balloons) | 43KB |
| ALFRED.5 | Shadow layers per room | 1.7MB |
| ALFRED.6 | Overlay graphics ("pegatinas"/stickers) | 700KB |
| ALFRED.7 | Sprites and cursors | 3.6MB |
| ALFRED.8 | Room default state values (clean state) | 649B |
| ALFRED.9 | Fonts, color remap tables | 146KB |
| ALFRED.B | Conversation state reset flags | 7KB |
| JUEGO.EXE | Main executable with game logic | 338KB |
| VISOR.EXE | Player for intro video (custom format) | 132KB |

### Key Data Structures
- **ALFRED.1**: 56 rooms × 13 data pairs (offset+size). Room directory at 0x0000.
- **Room offsets**: Pair 10 = hotspots/walkboxes/exits, Pair 11 = palette (768B), Pair 12 = text
- **Walkbox**: 9 bytes each at room_data+0x218, count at +0x213
- **Hotspot**: 9 bytes each at room_data+0x47C, count at +0x47A
- **Exit**: 14 bytes each at room_data+0x1BF, count at +0x1BE

## Build & Run

```bash
make          # Builds bin/alfredcli
make clean    # Removes bin/
make run      # Builds and runs
```

## Code Conventions

### C Code (`src/*.c`)
- Little-endian structs with `#pragma pack(push, 1)`
- File paths hardcoded as `files/ALFRED.*`
- Use `lodepng` for PNG output
- Switch which extraction runs in `main.c` by commenting/uncommenting

### Python Scripts (`src/*.py`, root `*.py`)
- Standalone extraction/analysis scripts
- Use `struct.unpack('<I', ...)` for little-endian
- Output to `output_*/` directories
- Run directly: `python3 src/extract_backgrounds.py`

### ImHex Patterns (`*.hexpat`)
- Binary format definitions for game files
- Use with ImHex to visualize structures

## Key Documentation
- [SAVE_GAME_SYSTEM_ANALYSIS.md](SAVE_GAME_SYSTEM_ANALYSIS.md) - Memory addresses, state structures
- [RESOURCE_FILE_FORMAT_DOCUMENTATION.md](RESOURCE_FILE_FORMAT_DOCUMENTATION.md) - Complete ALFRED.* formats
- [CONVERSATION_SYSTEM_DOCUMENTATION.md](CONVERSATION_SYSTEM_DOCUMENTATION.md) - Dialog/text control codes
- [SHADOW_SYSTEM_DOCUMENTATION.md](SHADOW_SYSTEM_DOCUMENTATION.md) - Character shadows per room

## Workflow Tips
1. Ghidra is the ultimate source of truth for reverse engineering. Files in the project might and will be flawed or incomplete.
2. You can check existing `.md` docs - most systems are already documented - but take care to verify against Ghidra.
3. All offsets are little-endian unless noted otherwise
