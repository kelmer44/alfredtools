# Brick Throw Animation Analysis

## Summary

The brick throw animation that plays when using object 4 (brick) with hotspot 294 (window) in room 3 has been identified and added to ScummVM.

## Animation Details

| Property | Value |
|----------|-------|
| Offset in ALFRED.7 | 0x1AF3EA (1766378) |
| Width | 72 pixels |
| Height | 33 pixels per frame |
| Frames | 9 |
| Compression | RLE (has BUDA marker) |
| Compressed size | ~3818 bytes |
| Decompressed size | 21384 bytes (72 × 33 × 9) |

## Code Location in Original

The brick throw animation is loaded at memory address 0x255CE in JUEGO.EXE:

```asm
0x255B1: PUSH 0x00        ; param8
0x255B3: PUSH 0x00        ; param7  
0x255B5: PUSH 0x01        ; param6 - compressed flag (1 = RLE)
0x255B7: PUSH 0x02        ; param5
0x255B9: PUSH 0x09        ; param4 - frames (9)
0x255BB: PUSH 0x48 (72)   ; param3 - width
0x255BD: PUSH 0x21 (33)   ; param2 - height per frame
0x255BF: MOV ECX, 0x38    ; (56)
0x255C4: MOV EBX, 0x134   ; (308)
0x255C9: MOV EDX, 0x0EEA  ; (3818) - compressed size
0x255CE: MOV EAX, 0x1AF3EA ; animation offset in ALFRED.7
0x255D3: JMP 0x2559B      ; jump to common CALL play_fight_animation
```

## Combo Table Entry

The combo table at memory 0x48118 has entry:
- item1 = 294 (window hotspot)
- item2 = 4 (brick inventory item)
- handler = 0x1284B (points mid-function, likely uses action dispatcher mechanism)

## ScummVM Implementation

### offsets.h
Added to `alfredSpecialAnims` array:
```cpp
{9, 72, 33, 1, 0x1AF3EA, 1},  // 4: BRICK THROW (RLE compressed)
```

### actions.cpp
Updated `useBrickWithWindow()`:
```cpp
// Play Alfred's throwing animation (index 4 in alfredSpecialAnims)
_res->loadAlfredSpecialAnim(4);
_alfredState.animState = ALFRED_SPECIAL_ANIM;
waitForSpecialAnimation();
```

## Extracted Frames

The animation shows Alfred in a throwing motion over 9 frames of 72x33 pixels each:
- Frames 0-4: Alfred's arm motion with brick
- Frames 5-7: Brick leaving frame, arm follow-through
- Frame 8: Empty (fully transparent)

Files extracted to: `output_brick_throw_9frames/`
