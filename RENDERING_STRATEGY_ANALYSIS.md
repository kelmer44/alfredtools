# Rendering Strategy Analysis: Full Frame vs Dirty Rectangles

## Question: Does the game use dirty rectangle optimization?

**Answer: NO - The game uses full-frame rendering**

## Evidence from Decompiled Code

### 1. Background Copying

Every frame, the entire background is copied to the front buffer:

```c
void copy_background_to_front_buffer(void) {
    get_current_room_number();

    // Copies ENTIRE background buffer to front buffer
    memcpy_wrapper(
        DAT_0004fa9c,    // Destination: front buffer
        DAT_0004fadc,    // Source: background buffer
        // Size parameter in EBX (entire screen: 640x400 = 256,000 bytes)
    );
}
```

**Key Point**: This is a full `memcpy` of the entire background, not selective region copying.

### 2. `memcpy_wrapper` Implementation

The memory copy function copies the full buffer size:

```c
void memcpy_wrapper(void* dest, void* src, size_t size) {
    // Copies 'size' bytes (EBX register contains full buffer size)

    // Optimized copy: 4 bytes at a time
    for (count = size >> 2; count != 0; count--) {
        *dest_ptr++ = *src_ptr++;
    }

    // Remaining bytes (size & 3)
    for (count = size & 3; count != 0; count--) {
        *dest_byte++ = *src_byte++;
    }
}
```

**Analysis**: No conditional logic, no rectangle bounds - just straight memory copy.

### 3. Sprite Rendering

Sprites are rendered on top of the already-copied background:

```c
// From render_scene()
copy_background_to_front_buffer();    // Copy entire background
update_npc_sprite_animations();       // Update sprite states
// ... sprites are rendered to render queue ...

// Then all sprites rendered via:
for (i = 0; i < sprite_count; i++) {
    render_sprite(sprite_data);  // Blit sprite over background
}
```

Each sprite is blitted individually, but the background is **always** copied in full first.

### 4. Present to Screen

The final blit to VGA also copies the entire frame buffer:

```c
void present_frame_to_screen(void) {
    get_current_room_number();

    blit_buffer_to_vga(
        DAT_0004fa9c,      // Source: front buffer
        DAT_000586ac,      // VGA memory (0xA0000)
        DAT_000586b4 >> 3, // Full screen size
        // ... other params ...
    );
}

void blit_buffer_to_vga(buffer, vga_mem, size, ...) {
    // Copy entire buffer to VGA in 64KB chunks
    while (size > 0) {
        set_vga_display_start(page);
        memcpy_wrapper(0xA0000, buffer);  // Copy 64KB chunk
        buffer += 0x10000;
        page++;
        size -= 0x10000;
    }
}
```

**Key Point**: Entire frame buffer (256KB for 640x400) is copied to VGA memory.

## Rendering Pipeline

```
Every Frame:
    ↓
1. copy_background_to_front_buffer()
    ├─ memcpy(front_buffer, background, 256000 bytes)
    └─ ENTIRE background copied
    ↓
2. update_npc_sprite_animations()
    ├─ Update sprite frame counters
    ├─ Advance animation sequences
    └─ Process movement
    ↓
3. Render sprites to front buffer
    ├─ For each sprite in render queue:
    │   └─ Blit sprite pixels over background
    └─ Sprites drawn with transparency
    ↓
4. Draw cursor
    └─ Blit cursor sprite at mouse position
    ↓
5. present_frame_to_screen()
    └─ memcpy(VGA_memory, front_buffer, 256000 bytes)
        └─ ENTIRE front buffer copied to VGA
```

## Performance Implications

### Memory Bandwidth Used Per Frame

At 18.2 frames per second (DOS timer interrupt rate):

1. **Background copy**: 256,000 bytes/frame
2. **VGA blit**: 256,000 bytes/frame
3. **Total per frame**: 512,000 bytes
4. **Total per second**: ~9.3 MB/s

### Why Full-Frame Rendering?

**Advantages:**
1. ✅ **Simple implementation** - No complex dirty rectangle tracking
2. ✅ **No visual artifacts** - Every pixel updated every frame
3. ✅ **Predictable performance** - Constant frame time
4. ✅ **No state tracking** - Don't need to remember what changed
5. ✅ **Easy debugging** - Clear, linear flow

**Disadvantages:**
1. ❌ **Wastes bandwidth** - Copies unchanged pixels
2. ❌ **CPU intensive** - 512KB memcpy per frame
3. ❌ **Can't optimize static areas** - Background always recopied

### Why This Works in DOS

1. **Fast memory access**: DOS had direct memory access, no OS overhead
2. **Simple graphics**: 640x400x8bpp = 256KB (manageable for 1992 hardware)
3. **Limited animations**: Only a few sprites moving at once
4. **Timer-based**: Fixed 18.2 FPS (not trying for 60 FPS)

## Comparison: Dirty Rectangle Algorithm

If the game **did** use dirty rectangles, we'd see:

```c
// HYPOTHETICAL dirty rectangle approach (NOT in this game)
struct DirtyRect {
    int x, y, width, height;
};

void render_with_dirty_rects() {
    DirtyRect dirty_regions[MAX_DIRTY];
    int dirty_count = 0;

    // Mark regions that changed
    for (each sprite that moved) {
        dirty_regions[dirty_count++] = sprite.old_bounds;
        dirty_regions[dirty_count++] = sprite.new_bounds;
    }

    // Only copy dirty regions
    for (int i = 0; i < dirty_count; i++) {
        copy_rect_from_background(dirty_regions[i]);
        render_sprites_in_rect(dirty_regions[i]);
        blit_rect_to_vga(dirty_regions[i]);
    }
}
```

**But this code is NOT present** in the decompiled game.

## Evidence Summary

| Feature | Dirty Rectangles | Full Frame | Game Uses |
|---------|------------------|------------|-----------|
| Background copy | Only changed areas | Entire buffer | **Entire buffer** |
| Sprite rendering | Track sprite bounds | Draw all sprites | **Draw all sprites** |
| VGA blit | Only dirty regions | Entire screen | **Entire screen** |
| State tracking | Must track changes | None needed | **None present** |
| Code complexity | High | Low | **Low** |

## Conclusion

The game uses a **straightforward full-frame rendering approach**:

1. Every frame, copy the entire background (256KB)
2. Render all sprites on top
3. Copy the entire result to VGA (256KB)

**No dirty rectangle optimization** is present. This is typical for early 90s DOS games where:
- Memory bandwidth was sufficient for 640x400x8bpp
- Implementation simplicity was valued
- Fixed frame rates (18.2 FPS) were acceptable
- Direct hardware access made full copies fast enough

The architecture prioritizes **code simplicity and correctness** over **optimal performance**, which was a reasonable trade-off for 1992 hardware running at fixed 18.2 FPS.
