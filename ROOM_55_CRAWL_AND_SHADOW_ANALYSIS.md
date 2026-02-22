# Room 55 Crawl System & Shadow Analysis

## Overview

Room 55 is a narrow passage where Alfred crawls instead of walking normally. This document covers two key differences from standard rooms:
1. **Walking animation**: Uses crawl sprites (130×55) instead of normal walking sprites (51×102), with only LEFT/RIGHT directions available
2. **Shadow system**: Room 55 has no shadow map in ALFRED.5 — it's the only room with a sentinel entry

---

## 1. Walking Direction Handling (Crawl Animation)

### The Problem

The standard walking system can set `alfred_facing_direction` to any of 4 values:
| Value | Direction |
|-------|-----------|
| 0 | RIGHT |
| 1 | LEFT |
| 2 | DOWN |
| 3 | UP |

The pathfinding system generates movement steps with vertical components (UP/DOWN flags), and the walking loop at `0x17D46` sets the direction accordingly. Room 55's crawl animation only has RIGHT and LEFT sprites — there are no DOWN or UP crawl animations.

### How the Original Game Solves It

**The game does NOT restrict the walking directions.** Instead, it remaps the animation pointer table so that DOWN and UP look up the same sprite data as RIGHT and LEFT.

In `load_room_and_init_alfred` at `0x15968`, the animation state table for room 55 is initialized as:

```c
// Room 55 (0x37) crawl animation setup
anim_state_table_dir0_ptr = alfred3_anim_data_base_ptr + 0x4C339;  // RIGHT crawl
anim_state_table_dir1_ptr = alfred3_anim_data_base_ptr + 0x5BE97;  // LEFT crawl
anim_state_table_dir2_ptr = anim_state_table_dir0_ptr;             // DOWN → RIGHT crawl
anim_state_table_dir3_ptr = anim_state_table_dir1_ptr;             // UP → LEFT crawl
anim_state_sprite_width   = 0x82;   // 130 pixels
anim_state_sprite_height  = 0x37;   // 55 pixels
anim_state_frame_size     = 0x1BEE; // 7150 bytes (130 × 55)
```

Compare with normal rooms:
```c
anim_state_table_dir0_ptr = alfred3_anim_data_base_ptr + 0x00000;  // RIGHT walk
anim_state_table_dir1_ptr = alfred3_anim_data_base_ptr + 0x0B6E2;  // LEFT walk
anim_state_table_dir2_ptr = alfred3_anim_data_base_ptr + 0x16DC4;  // DOWN walk
anim_state_table_dir3_ptr = alfred3_anim_data_base_ptr + 0x1D35E;  // UP walk
anim_state_sprite_width   = 0x33;   // 51 pixels
anim_state_sprite_height  = 0x66;   // 102 pixels
anim_state_frame_size     = 0x1452; // 5202 bytes (51 × 102)
```

### Animation State Table Structure

The table at `0x4F7B4` has a stride of 0x14 (20 bytes) per animation state:

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 4 | dir0_ptr | Pointer to frame data for direction 0 (RIGHT) |
| +0x04 | 4 | dir1_ptr | Pointer to frame data for direction 1 (LEFT) |
| +0x08 | 4 | dir2_ptr | Pointer to frame data for direction 2 (DOWN) |
| +0x0C | 4 | dir3_ptr | Pointer to frame data for direction 3 (UP) |
| +0x10 | 1 | width | Sprite width in pixels |
| +0x11 | 1 | height | Sprite height in pixels |
| +0x12 | 2 | frame_size | Single frame size in bytes (width × height) |

Multiple animation states (idle/walk=0, talk=1, interact=2, etc.) are stored consecutively at `0x14` byte intervals.

### Walking Frame Selection Formula

From `walk_to_target_and_execute_queued_action` at `0x17D26`:

```c
// Frame mask determines number of walking frames
if (alfred_facing_direction < 2) {
    mask = 7;   // RIGHT/LEFT: 8 walking frames (0-7)
} else {
    mask = 3;   // DOWN/UP: 4 walking frames (0-3)
}

// Frame data pointer calculation:
frame_ptr = base_ptr + frame_size + ((counter & mask) * frame_size);
```

**Frame layout in sprite data:**
- Frame 0: Idle/standing frame (used by `setup_alfred_frame_from_state`)
- Frames 1-8: Walking cycle for LEFT/RIGHT (accessed with mask=7 → indices 1 through 8)
- Frames 1-4: Walking cycle for DOWN/UP (accessed with mask=3 → indices 1 through 4)

For room 55 with direction remapping:
- Walking RIGHT or DOWN: Uses RIGHT crawl data, frames 1-8 or 1-4
- Walking LEFT or UP: Uses LEFT crawl data, frames 1-8 or 1-4

### Critical ScummVM Bugs

**Bug 1: Array out-of-bounds crash**

```cpp
// CURRENT (crashes when direction is DOWN=2 or UP=3):
drawSpriteToBuffer(..., _res->alfredCrawlFrames[_alfredState.direction][...], ...);

// alfredCrawlFrames only has 2 entries: [0]=RIGHT, [1]=LEFT
// Accessing [2] or [3] is undefined behavior → crash
```

**Fix**: Map direction for room 55 — DOWN→RIGHT (0), UP→LEFT (1):
```cpp
int crawlDir = _alfredState.direction;
if (crawlDir == ALFRED_DOWN) crawlDir = ALFRED_RIGHT;
if (crawlDir == ALFRED_UP) crawlDir = ALFRED_LEFT;
drawSpriteToBuffer(..., _res->alfredCrawlFrames[crawlDir][...], ...);
```

**Bug 2: Wrong frame count**

```cpp
// CURRENT (wraps at 9, includes idle frame):
if (_alfredState.curFrame >= 9) {
    _alfredState.curFrame = 0;
}
```

The original game uses frame mask 7 (8 walking frames) for LEFT/RIGHT and mask 3 (4 walking frames) for UP/DOWN. Frame 0 is the idle frame and is NOT used during walking. The walking formula adds `frame_size` before the frame offset, effectively starting at frame 1.

**Fix**: Use 8 walking frames for left/right, wrapping properly:
```cpp
int crawlDir = _alfredState.direction;
if (crawlDir == ALFRED_DOWN) crawlDir = ALFRED_RIGHT;
if (crawlDir == ALFRED_UP) crawlDir = ALFRED_LEFT;

int maxFrames = (crawlDir < 2) ? 8 : 4; // Same as original mask+1
if (_alfredState.curFrame >= maxFrames) {
    _alfredState.curFrame = 0;
}
// Note: Frame index 0 in alfredCrawlFrames should map to walking frame 1
// (skip the idle frame at the beginning of the animation data)
```

---

## 2. Shadow System in Room 55

### ALFRED.5 Shadow Map

Room 55 is the **only room** (out of 56) that has no shadow map. Its directory entry in ALFRED.5 contains the sentinel value `0xFFFFFFFF`:

| Room | Offset (hex) | Raw bytes | Status |
|------|-------------|-----------|--------|
| 0 | 0x000258 | `58 02 00 00 92 0B` | Normal shadow map |
| 54 | 0x01DB14 | `14 DB 01 00 5A 09` | Normal shadow map |
| **55** | **0xFFFFFFFF** | `FF FF FF FF FF FF` | **Sentinel — no shadow map** |

### ALFRED.5 Directory Entry Format

Each entry is 6 bytes:

| Offset | Size | Field |
|--------|------|-------|
| 0 | 4 | 32-bit LE offset into ALFRED.5 (0xFFFFFFFF = no shadow) |
| 4 | 2 | 16-bit LE compressed data size |

### What Happens in the Original Game

1. `file_seek(alfred5, 0xFFFFFFFF)` — seeks past the 126KB file (DOS silently handles this)
2. `file_read(temp_buf, 0xFFFF, alfred5)` — reads 0 bytes (past EOF)
3. `decompress_rle_block(temp_buf, shadow_map_buffer)` — processes stale buffer data
4. The shadow map buffer (`0x4FB24`) retains whatever data was left from the previous room

The rendering function `render_alfred_sprite_with_scaling_and_shadow` at `0x16FF8` still scans the shadow buffer, but:
- Shadow detection uses a **hardcoded** `+0x66` (102) Y offset for foot sampling
- Room 55's crawl sprite is only 55 pixels tall
- The sampling point is 47 pixels below the actual sprite feet
- The stale shadow data may or may not have shadow values at the sampled position
- In practice, the visual effect is minimal/undefined since room 55 is a narrow tunnel

### Shadow Detection Algorithm (from `render_alfred_sprite_with_scaling_and_shadow`)

```c
// Scan shadow map at character foot line
shadow_scan_col = 0;
do {
    if (sprite_width_minus_scale <= shadow_scan_col) {
        // No shadow found → render without shadow
        break;
    }
    shadow_pixel = shadow_map_buffer[(sprite_top_y + 0x66) * 640 + sprite_x + shadow_scan_col];
    if (shadow_pixel != 0xFF) {
        shadow_detected = true;
        shadow_level = shadow_pixel;  // 0-3 indexes into remap tables
        break;
    }
    shadow_scan_col++;
} while (true);

// During rendering, if shadow detected:
if (shadow_detected) {
    output_pixel = shadow_palette_remap_tables[pixel_color + shadow_level * 256];
}
```

### ALFRED.9 Shadow Palette Remap Tables

**Important bug in ScummVM**: The game reads ALFRED.9 at offset `room_number * 1024` (confirmed in assembly at `0x15419`: `SHL EDX,0xa`). The ScummVM code incorrectly uses `0x200 + (roomNumber * 1024)`.

Room 55 has valid remap data in ALFRED.9 (at offset 56320), but it's never actually used because no shadow map exists to trigger the remap.

### ScummVM Shadow Loading

The current `loadShadowMap()` in the ScummVM code reads the sentinel offset `0xFFFFFF` (24-bit portion), then `readUntilBuda` returns 0 compressed bytes, `rleDecompress` produces 0 bytes, and `_pixelsShadows` is set to `nullptr`. The null check in `drawAlfred()` correctly skips shadow application. Room 55 crawl rendering also bypasses `drawAlfred()` entirely (uses `drawSpriteToBuffer` directly), so shadow is never applied regardless.

**The shadow system works correctly for room 55 in the ScummVM implementation** (no shadow applied), matching the intended behavior.

---

## 3. Additional Bug: ALFRED.9 Remap Table Offset

### Original Game (correct)
```asm
00015417: MOV EDX,EDI          ; room_number
00015419: SHL EDX,0xa          ; * 1024
0001541c: MOV EAX,[0x0004f910] ; file_handle_alfred9
00015421: XOR EBX,EBX
00015423: CALL file_seek        ; seek to room * 1024
```

### ScummVM Implementation (incorrect)
```cpp
// room.cpp line 1298
uint32 remapOffset = 0x200 + (roomNumber * 1024);  // WRONG: should be just roomNumber * 1024
```

This means ALL rooms read shadow remap data from an offset shifted by 512 bytes. Room 0's remap starts at byte 512 instead of byte 0. This causes every room to use incorrect shadow darkening palettes.

---

## 4. Ghidra Renames Applied

### Functions
| Address | Old Name | New Name |
|---------|----------|----------|
| 0x16FF8 | `render_alfred_sprite_scaled` | `render_alfred_sprite_with_scaling_and_shadow` |

### Data Labels
| Address | New Name | Purpose |
|---------|----------|---------|
| 0x4F7B4 | `anim_state_table_dir0_ptr` | Animation state table: direction 0 (RIGHT) frame data pointer |
| 0x4F7B8 | `anim_state_table_dir1_ptr` | Direction 1 (LEFT) frame data pointer |
| 0x4F7BC | `anim_state_table_dir2_ptr` | Direction 2 (DOWN) frame data pointer |
| 0x4F7C0 | `anim_state_table_dir3_ptr` | Direction 3 (UP) frame data pointer |
| 0x4F7C4 | `anim_state_sprite_width` | Sprite width for current animation state |
| 0x4F7C5 | `anim_state_sprite_height` | Sprite height for current animation state |
| 0x4F7C6 | `anim_state_frame_size` | Frame size (width × height) for current animation state |
| 0x4FA94 | `alfred3_anim_data_base_ptr` | Base pointer to decompressed ALFRED.3 animation data |
| 0x4FB24 | `shadow_map_buffer` | Decompressed shadow map from ALFRED.5 (256,000 bytes) |
| 0x52BFC | `shadow_palette_remap_tables` | Shadow palette remap tables from ALFRED.9 (4 × 256 bytes) |
| 0x4FAB4 | `shadow_dir_entry_buffer` | 6-byte directory entry buffer for ALFRED.5 |
| 0x4F900 | `file_handle_alfred5` | File handle for ALFRED.5 |
| 0x4F910 | `file_handle_alfred9` | File handle for ALFRED.9 |

### Variables (in functions)
| Function | Old Name | New Name |
|----------|----------|----------|
| `walk_to_target_and_execute_queued_action` | `pcVar5` | `walk_step_ptr` |
| `render_alfred_sprite_with_scaling_and_shadow` | `bVar2` | `shadow_detected` |
| `render_alfred_sprite_with_scaling_and_shadow` | `local_18` | `shadow_level` |

### Decompiler Comments Added
| Address | Description |
|---------|-------------|
| 0x159A0 | Room 55 crawl animation setup: direction remapping explanation |
| 0x159DE | DOWN→RIGHT and UP→LEFT pointer mapping for crawl |
| 0x153A0 | ALFRED.5 shadow loading with sentinel explanation |
| 0x17D26 | Walking animation frame mask system (8 frames horiz, 4 frames vert) |
| 0x17D46 | Walking direction update from movement step flags |
| 0x17002 | Shadow detection loop with hardcoded +0x66 offset |
| 0x17089 | Shadow palette remap application |

### Assembly Comments Added
| Address | Description |
|---------|-------------|
| 0x15968 | Room 55 crawl animation init header |
| 0x15983 | DIR2/DIR3 remapping to prevent direction crash |
| 0x15419 | ALFRED.9 offset calculation (no 0x200 header) |
| 0x153A0 | ALFRED.5 sentinel handling for room 55 |

---

## 5. Summary of Required ScummVM Fixes

1. **Crawl direction mapping** — Map DOWN→RIGHT and UP→LEFT before indexing `alfredCrawlFrames`. Apply to both IDLE and WALKING states.
2. **Crawl frame count** — Use 8 walking frames for LEFT/RIGHT (mask=7), 4 for DOWN/UP (mask=3). Don't include the idle frame (frame 0) in the walking cycle.
3. **ALFRED.9 remap offset** — Remove the `0x200` addition in `loadRemaps()`. The original game reads at `roomNumber * 1024` directly.
