# How the Game Retrieves Sprite N from ALFRED.6

## Quick Answer

**The game uses a hardcoded offset table** stored in the executable to directly access any sprite by index in O(1) time.

To retrieve sprite 12:
```c
offset = pegatina_offsets[12];  // 0x0092C4
fseek(alfred6_file, offset, SEEK_SET);
fread(&header, 6, 1, fp);  // x=190, y=251, w=48, h=90
fread(pixels, 48*90, 1, fp);  // 4,320 pixel bytes
palette = getRoomPalette(tablapaletas[12]);  // Room 4 palette
```

## The Offset Table

The game executable contains a pre-built array of 137 offsets:

```c
unsigned int pegatina_offsets[137] = {
    0x000000,  // Sprite 0
    0x00005B,  // Sprite 1
    0x0000B6,  // Sprite 2
    // ...
    0x0092C4,  // Sprite 12 ← HERE
    0x00A3AA,  // Sprite 13
    // ...
    0x0816B1   // Sprite 136
};
```

## Complete Loading Process

### 1. Index Validation
```c
int load_sprite(int sprite_index) {
    if (sprite_index < 0 || sprite_index >= 137) {
        return ERROR_INVALID_INDEX;
    }
```

### 2. Offset Lookup
```c
    unsigned int file_offset = pegatina_offsets[sprite_index];
```

### 3. Seek to Position
```c
    FILE *fp = fopen("ALFRED.6", "rb");
    fseek(fp, file_offset, SEEK_SET);
```

### 4. Read Header (6 bytes)
```c
    unsigned short x = read_word_le(fp);  // Screen X position
    unsigned short y = read_word_le(fp);  // Screen Y position
    unsigned char w = read_byte(fp);      // Width in pixels
    unsigned char h = read_byte(fp);      // Height in pixels
```

### 5. Allocate Buffer
```c
    unsigned int pixel_count = w * h;
    unsigned char *pixels = malloc(pixel_count);
```

### 6. Read Pixel Data
```c
    fread(pixels, pixel_count, 1, fp);
```

### 7. Get Room Palette
```c
    int room_num = tablapaletas[sprite_index];
    unsigned char *palette = getRoomPalette(room_num);
```

### 8. Create Sprite Object
```c
    Sprite *sprite = create_sprite(x, y, w, h, pixels, palette);
    return sprite;
}
```

## Key Data Structures

### Offset Table Location (in Executable)
- **Type:** Array of 32-bit unsigned integers
- **Size:** 137 entries × 4 bytes = 548 bytes
- **Likely section:** `.data` or `.rdata` (initialized read-only data)
- **Search pattern:** `00 00 00 00 5B 00 00 00 B6 00 00 00 98 02 00 00...`

### Palette Mapping Table
```c
int tablapaletas[140] = {
    0,0,0,0,0,0,0,    // Sprites 0-6: Room 0
    2,2,              // Sprites 7-8: Room 2
    3,3,3,3,3,3,3,3,  // Sprites 9-16: Room 3
    4,4,4,4,4,        // Sprites 17-21: Room 4 ← Sprite 12 uses this
    // ... etc
};
```

## Why This Design?

### Advantages
1. **O(1) access time** - instant lookup, no scanning needed
2. **No file parsing** - skip directly to sprite data
3. **Simple implementation** - just array indexing
4. **Efficient** - one seek, one read for header, one read for pixels

### Why Not Sequential?
The file IS sequentially laid out, but:
- Some sprites have padding (0xBF bytes)
- Four sprites have gaps (37, 67, 68, 88)
- Scanning would require reading every header to find sprite N
- Pre-computed table eliminates this overhead

## Example: Sprite 12 in Detail

```
Sprite Index:     12
File Offset:      0x0092C4 (37,572 decimal)
Position:         (190, 251) pixels from top-left
Dimensions:       48×90 pixels
Pixel Data Size:  4,320 bytes
Room Palette:     4 (tablapaletas[12])
Total Size:       4,326 bytes (6 header + 4,320 pixels)
Next Sprite:      13 at 0x00A3AA
```

### Memory Layout
```
Offset      Bytes        Meaning
─────────────────────────────────────────
0x0092C4    BE 00        X position = 190
0x0092C6    FB 00        Y position = 251
0x0092C8    30           Width = 48
0x0092C9    5A           Height = 90
0x0092CA    [4320 bytes] Pixel data (48×90)
0x00A3AA    [Sprite 13]  Next sprite begins
```

## Finding This in Ghidra

### Step 1: Search for Known Offsets
Search for these hex patterns (little-endian):
- `C4 92 00 00` (sprite 12: 0x0092C4)
- `C4 B8 01 00` (sprite 37: 0x01B8C4)
- `13 F8 03 00` (sprite 67: 0x03F813)

### Step 2: Locate the Array
Find where these appear consecutively in memory. Should see:
```
pegatina_offsets:
  00 00 00 00   ; Sprite 0
  5B 00 00 00   ; Sprite 1
  B6 00 00 00   ; Sprite 2
  98 02 00 00   ; Sprite 3
  ...
  C4 92 00 00   ; Sprite 12  ← Look for this
  AA A3 00 00   ; Sprite 13
  ...
```

### Step 3: Find References
Use Ghidra's "Find References" on the array address.
Look for code like:
```c
offset = *(uint32_t *)(pegatina_offsets + sprite_index * 4);
```

### Step 4: Rename Everything
Once found:
- Array → `pegatina_offsets` or `alfred6_sprite_offsets`
- Function → `load_pegatina()` or `get_sprite_from_alfred6()`
- File handle → `alfred6_file_handle`
- Variables → `sprite_x`, `sprite_y`, `sprite_width`, `sprite_height`

### Step 5: Document the Function
Add comments explaining:
- What sprite indices are valid (0-136)
- Which room palette each sprite uses
- How the x,y positioning works
- The file format structure

## Performance Characteristics

| Operation | Time Complexity | Notes |
|-----------|----------------|-------|
| Find sprite offset | O(1) | Array lookup |
| Seek to sprite | O(1) | Direct file seek |
| Read header | O(1) | Fixed 6 bytes |
| Read pixels | O(n) | n = width × height |
| Total | O(n) | Linear in sprite size |

## File Format vs. Access Method

```
FILE STRUCTURE (ALFRED.6):
  Sprite 0 → Sprite 1 → Sprite 2 → ... → Sprite 136
  (Sequential, but with variable padding)

ACCESS METHOD (Game Executable):
  pegatina_offsets[N] → Direct seek → Read sprite
  (Random access via offset table)
```

This is a classic **trade-off**:
- **Space cost:** 548 bytes for offset table in executable
- **Time savings:** Instant access to any sprite without scanning

## Related Files

- **ALFRED.6** - The sprite data file (519 KB)
- **Game executable** - Contains `pegatina_offsets[]` array
- **ALFRED.1** - Contains room palettes (via `getRoomPalette()`)
- **Palette table** - Maps sprite index → room number (`tablapaletas[]`)

## Implementation Reference

See these files for complete implementation:
- `alfred6.c` - Sequential extraction (rebuilds offset table)
- `analyze_alfred6_structure.py` - Generates offset table
- `alfred6_offset_table.json` - Complete offset data
- `ALFRED6_FILE_FORMAT.md` - Full file format documentation
