# Room Handler Analysis - Detailed

## Summary

After careful analysis, the room initialization handlers in Alfred Pelrock serve purposes that are **mostly already data-driven** in ScummVM through the room metadata. Here's the breakdown:

### Rooms 0-5 Handler Analysis

| Room | Handler | What It Does | ScummVM Status |
|------|---------|--------------|----------------|
| 0 | 0x1561F | Entry point after Room 3 text swap | ✅ No action needed |
| 1 | None | Default initialization | ✅ Already works |
| 2 | 0x15C22 | VGA register setup for palette cycling | ⚠️ Already handled by palette anim system |
| 3 | 0x15889 | Jump past scaling code | ✅ Handled by scaleMode data |
| 4 | 0x1561F | Same as Room 0 | ✅ No action needed |
| 5 | 0x15A3D | Sets render enable and scale factor | ✅ Already standard behavior |

### Key Finding

The dispatch table handlers are **OPTIMIZATION CODE**, not special logic. They skip portions of the initialization that don't apply to certain rooms:

1. **Room 3 Handler (0x15889)**: Enters right at a JMP instruction that skips the remaining scaling calculation. This is because Room 3's `scaleMode` byte in the room data already indicates no dynamic scaling is needed.

2. **Room 0/4 Handler (0x1561F)**: These enter after the Room 3 text swap code because they don't need that text manipulation.

3. **Room 2 Handler (0x15C22)**: Enters late in the function during VGA setup. This is already handled by ScummVM's palette animation system.

4. **Room 5 Handler (0x15A3D)**: Enters at sprite render setup. Standard behavior, no special handling.

### Room 3 Text Swap

There IS one piece of special logic - Room 3 has text data that gets reordered:

```c
// Original DOS code for Room 3:
if (room_number == 3) {
    // Find '-' character in text data
    while (*text_scanner != '-') text_scanner++;
    // Swap text blocks
    memcpy(text_scanner + 0x4e22, text_scanner + 2, 0x474);
    memcpy(text_scanner + 10, text_scanner + 0x4e22, 0x474);
}
```

This swaps conversation text for Room 3. **This is NOT handled by dispatch table but is hardcoded logic in the main function.**

### ScummVM Implementation Needed

Only Room 3's text swap needs implementation:

```cpp
// In room.cpp when loading room 3 text data:
if (roomNumber == 3) {
    // Find '-' delimiter in text data
    byte *scanner = pair12;
    while (*scanner != '-' && (scanner - pair12) < pair12size) {
        scanner++;
    }
    if (*scanner == '-') {
        // Swap text blocks (0x474 = 1140 bytes each)
        byte *tempBuffer = new byte[0x474];
        memcpy(tempBuffer, scanner + 2, 0x474);
        memcpy(scanner + 10, scanner + 0x4e22, 0x474); 
        memcpy(scanner + 0x4e22, tempBuffer, 0x474);
        delete[] tempBuffer;
    }
}
```

However, I recommend checking if this swap is actually necessary in practice - it might be a developer artifact for testing conversation branches.

### Palette Cycling Rooms

These rooms have palette cycling enabled via the palette_cycling_dispatch_table (0x486a4):
- Room 2 (McDowells restaurant - neon signs)
- Other rooms with animated elements

This is already handled by ScummVM's `getPaletteAnimForRoom()` function.

## Conclusion

**No code changes needed** for rooms 0-5 handlers. The original game's dispatch table exists for performance optimization (skipping irrelevant code), not for implementing different behavior. ScummVM's data-driven approach already handles all the necessary room-specific behavior through:

1. `scaleMode` parameter for scaling behavior
2. `PaletteAnim` system for palette cycling
3. Standard room loading for everything else

The only potential missing piece is Room 3's text swap, but this may not be gameplay-critical.
