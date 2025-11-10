# Room Metadata Extraction

The `extract_room_metadata.py` tool is a unified extractor that combines all Pair 10 data extraction into a single tool.

## What It Extracts

From each room's Pair 10 data block, it extracts:

1. **Hotspots** (0x47A) - Interactive objects/clickable areas
   - Position, size, type, and action ID

2. **Exits** (0x1BE) - Room connections/doorways
   - Trigger zones, destination room, destination coordinates, facing direction

3. **Walkboxes** (0x213) - Walkable areas
   - Position, size, and flags

4. **Hover Areas** (heuristic scan) - Cursor change regions
   - Detected areas where mouse cursor changes appearance
   - Categorized by screen region (left/center/right)

## Usage

### Extract all rooms:
```bash
python3 src/extract_room_metadata.py files/ALFRED.1
```

### Extract a single room:
```bash
python3 src/extract_room_metadata.py files/ALFRED.1 --room 1
```

### Choose output formats:
```bash
python3 src/extract_room_metadata.py files/ALFRED.1 --formats json py txt
```

### Skip hover areas (faster):
```bash
python3 src/extract_room_metadata.py files/ALFRED.1 --no-hover
```

### Custom output directory:
```bash
python3 src/extract_room_metadata.py files/ALFRED.1 --output my_output/
```

## Output Formats

- **JSON** - Complete structured data, easy to parse programmatically
- **Python** - Dictionary format for importing into Python scripts
- **Text** - Human-readable format for quick inspection

## Example Output Structure

```json
{
  "room": 1,
  "pair10_offset": 453988,
  "pair10_size": 1328,
  "hotspots": [
    {
      "index": 0,
      "type": 0,
      "x": 21,
      "y": 216,
      "width": 89,
      "height": 124,
      "extra": 276
    }
  ],
  "exits": [
    {
      "index": 0,
      "destination_room": 0,
      "trigger": {"x": 28, "y": 340, "width": 28, "height": 2},
      "destination": {"x": 235, "y": 282, "direction": 2, "direction_name": "down"},
      "flags": 1
    }
  ],
  "walkboxes": [
    {
      "index": 0,
      "x": 4,
      "y": 364,
      "width": 584,
      "height": 8,
      "flags": 0
    }
  ],
  "hover_areas": [
    {
      "offset": 1149,
      "x": 21,
      "y": 216,
      "width": 89,
      "height": 124,
      "region": "left"
    }
  ]
}
```

## Related Tools

- **paint_hover_areas.py** - Visualize hover areas over room backgrounds
- **check_hotspot_types.py** - Analyze cursor behavior at specific coordinates

## Technical Details

All data comes from the room's **Pair 10** data block:
- Each room has 13 pairs (0-12) of offset+size pointers
- Pair 10 contains the bulk of room metadata
- Screen resolution: 640x400 pixels
- Direction encoding: 0=right, 1=left, 2=down, 3=up
