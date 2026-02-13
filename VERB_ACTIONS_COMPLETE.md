# Complete Verb Action Handler Documentation

Auto-generated analysis of all verb action handlers from JUEGO.EXE.
Each handler is disassembled and pattern-matched for hotspot moves, flag sets,
sticker displays, palette changes, and conversation state updates.

## Architecture Reference

### Address Mapping

- Code: Ghidra addr = raw_func_ptr + 0x10000; file offset = Ghidra addr + 0x4200
- Data: fixed addr = raw_addr + 0x40000
- Hotspot structure: type(1) X(2) Y(2) W(1) H(1) extra(2) = 9 bytes each
- Hotspot array starts at room_data + 0x47C, count at room_data + 0x47A
- Hidden hotspot convention: X=640, Y=400 (off-screen)

### Known Functions

| Address | Name |
|---------|------|
| 0x1B1A2 | `display_text_with_character_animation` |
| 0x1B666 | `update_conversation_state` |
| 0x1BA45 | `load_and_render_sticker_from_alfred6` |
| 0x1BD53 | `fade_palette_to_target` |
| 0x1C131 | `trigger_statue_secret` |
| 0x25487 | `default_verb_response` |
| 0x25E90 | `allocate_memory` |
| 0x26F6C | `end_dialog` |
| 0x27CE1 | `play_ambient_sound` |
| 0x2A342 | `file_seek` |
| 0x2A43E | `file_read` |
| 0x2A60D | `free_memory` |
| 0x2A66B | `memcpy_wrapper` |
| 0x2A6B7 | `write_data_to_alfred1` |

## Summary

| Verb | Entries | Unique Handlers |
|------|---------|----------------|
| LOOK | 4 | 4 |
| OPEN | 26 | 26 |
| PULL | 16 | 16 |
| PICKUP | 48 | 44 |

## Room Index

| Room | Verb | Extras |
|------|------|--------|
| -1 | OPEN | 288, 9 |
| -1 | PICKUP | 0, 273, 700 |
| 0 | OPEN | 261, 268, 263 |
| 0 | PICKUP | 1, 2, 3 |
| 0 | PULL | 261, 268 |
| 1 | OPEN | 277 |
| 1 | PICKUP | 4 |
| 2 | OPEN | 282 |
| 2 | PICKUP | 283, 284 |
| 2 | PULL | 282 |
| 3 | OPEN | 290 |
| 3 | PICKUP | 308 |
| 3 | PULL | 290 |
| 4 | OPEN | 315, 312 |
| 4 | PICKUP | 316, 310, 311 |
| 4 | PULL | 312 |
| 8 | OPEN | 355 |
| 8 | PICKUP | 357 |
| 8 | PULL | 355 |
| 9 | OPEN | 363 |
| 9 | PICKUP | 360, 361, 362 |
| 9 | PULL | 363 |
| 12 | OPEN | 370 |
| 12 | PICKUP | 60, 62, 61 |
| 12 | PULL | 370 |
| 13 | OPEN | 374, 375 |
| 13 | PULL | 374 |
| 15 | PICKUP | 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 6, 7 |
| 16 | OPEN | 388 |
| 16 | PULL | 388 |
| 17 | OPEN | 393 |
| 17 | PULL | 393 |
| 19 | OPEN | 400 |
| 19 | PULL | 400 |
| 25 | PICKUP | 609 |
| 28 | PICKUP | 472, 87, 88, 89, 112 |
| 29 | OPEN | 434 |
| 29 | PULL | 434 |
| 30 | LOOK | 435, 436, 437, 438 |
| 31 | OPEN | 462 |
| 31 | PICKUP | 101 |
| 32 | OPEN | 473 |
| 32 | PICKUP | 100 |
| 33 | OPEN | 465, 651 |
| 33 | PULL | 465 |
| 37 | PICKUP | 90 |
| 38 | PICKUP | 81, 99 |
| 42 | PICKUP | 605, 606, 607, 608 |
| 46 | OPEN | 621 |
| 46 | PULL | 621 |
| 47 | OPEN | 800 |
| 47 | PICKUP | 628 |
| 47 | PULL | 800 |
| 55 | OPEN | 613 |

---

## Unknown Room

### OPEN Extra 9

**Handler:** Ghidra `0x1C9D5` | File `0x20BD5` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1C9D5: push     4
  1C9DA: call     0x2a218  ; __STK
  1C9DF: mov      eax, dword ptr [0xb9c4]
  1C9E4: jmp      0x25487
```

</details>

### OPEN Extra 288

**Handler:** Ghidra `0x1C632` | File `0x20832` | Size: 214 bytes | 43 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49840] == 0
   2. Set flag [0x49840] = 1
   3. Display sticker from ALFRED.6 offset=0xB490, size=0x216
   4. SHOW hotspot[18] @0x51F → (519, 363)

<details>
<summary>Raw disassembly (43 instructions)</summary>

```asm
  1C632: push     0x10
  1C637: call     0x2a218  ; __STK
  1C63C: push     ebx
  1C63D: push     ecx
  1C63E: push     edx
  1C63F: cmp      byte ptr [0x9840], 0
  1C646: jne      0x1c708
  1C64C: call     0x1c716
  1C651: mov      byte ptr [0x9840], 1
  1C658: mov      edx, 0x216
  1C65D: mov      eax, 0xb490
  1C662: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1C667: mov      eax, dword ptr [0xfac8]
  1C66C: mov      word ptr [eax + 0x51f], 0x207
  1C675: mov      eax, dword ptr [0xfac8]
  1C67A: mov      word ptr [eax + 0x521], 0x16b
  1C683: mov      ax, word ptr [0xfb94]
  1C689: mov      word ptr [0xfb78], ax
  1C68F: mov      word ptr [0xfb7a], 0x51f
  1C698: mov      byte ptr [0xfb7c], 4
  1C69F: mov      word ptr [0xfb7d], 0x207
  1C6A8: mov      word ptr [0xfb7f], 0x16b
  1C6B1: mov      ecx, dword ptr [0xf914]
  1C6B7: mov      ebx, 1
  1C6BC: mov      edx, 9
  1C6C1: mov      eax, 0xfb78
  1C6C6: call     0x2a6b7  ; write_data_to_alfred1
  1C6CB: mov      eax, dword ptr [0xfaac]
  1C6D0: mov      edx, dword ptr [eax + 0x50]
  1C6D3: add      edx, 0x51f
  1C6D9: mov      eax, dword ptr [0xf8f0]
  1C6DE: xor      ebx, ebx
  1C6E0: call     0x2a342  ; file_seek
  1C6E5: mov      ecx, dword ptr [0xf8f0]
  1C6EB: mov      eax, dword ptr [0xfac8]
  1C6F0: add      eax, 0x51f
  1C6F5: mov      ebx, 1
  1C6FA: mov      edx, 4
  1C6FF: call     0x2a6b7  ; write_data_to_alfred1
  1C704: pop      edx
  1C705: pop      ecx
  1C706: pop      ebx
  1C707: ret      
```

</details>

### PICKUP Extra 0

**Handler:** Ghidra `0x1E444` | File `0x22644` | Size: 787 bytes | 144 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x49687] = 1
   2. Display sticker from ALFRED.6 offset=0x60C87, size=0x92
   3. HIDE hotspot[4] @0x4A1 → (640, 400)
   4. HIDE hotspot[8] @0x4C5 → (640, 400)
   5. HIDE hotspot[9] @0x4CE → (640, 400)
   6. HIDE hotspot[10] @0x4D7 → (640, 400)
   7. SHOW hotspot[0] @0x47D → (191, 243)
   8. JMP → 0x1D2F5

<details>
<summary>Raw disassembly (144 instructions)</summary>

```asm
  1E444: push     0x10
  1E449: call     0x2a218  ; __STK
  1E44E: push     ebx
  1E44F: push     ecx
  1E450: push     edx
  1E451: mov      byte ptr [0x9687], 1
  1E458: mov      edx, 0x92
  1E45D: mov      eax, 0x60c87
  1E462: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1E467: mov      eax, dword ptr [0xfac8]
  1E46C: mov      word ptr [eax + 0x4a1], 0x280
  1E475: mov      eax, dword ptr [0xfac8]
  1E47A: mov      word ptr [eax + 0x4a3], 0x190
  1E483: mov      ax, word ptr [0xfb94]
  1E489: mov      word ptr [0xfb78], ax
  1E48F: mov      word ptr [0xfb7a], 0x4a1
  1E498: mov      byte ptr [0xfb7c], 4
  1E49F: mov      word ptr [0xfb7d], 0x280
  1E4A8: mov      word ptr [0xfb7f], 0x190
  1E4B1: mov      ecx, dword ptr [0xf914]
  1E4B7: mov      ebx, 1
  1E4BC: mov      edx, 9
  1E4C1: mov      eax, 0xfb78
  1E4C6: call     0x2a6b7  ; write_data_to_alfred1
  1E4CB: mov      eax, dword ptr [0xfaac]
  1E4D0: mov      edx, dword ptr [eax + 0x50]
  1E4D3: add      edx, 0x4a1
  1E4D9: mov      eax, dword ptr [0xf8f0]
  1E4DE: xor      ebx, ebx
  1E4E0: call     0x2a342  ; file_seek
  1E4E5: mov      ecx, dword ptr [0xf8f0]
  1E4EB: mov      eax, dword ptr [0xfac8]
  1E4F0: add      eax, 0x4a1
  1E4F5: jmp      0x1e808
  1E4FA: push     0x10
  1E4FF: call     0x2a218  ; __STK
  1E504: push     ebx
  1E505: push     ecx
  1E506: push     edx
  1E507: mov      eax, dword ptr [0xfac8]
  1E50C: mov      word ptr [eax + 0x4c5], 0x280
  1E515: mov      eax, dword ptr [0xfac8]
  1E51A: mov      word ptr [eax + 0x4c7], 0x190
  1E523: mov      ax, word ptr [0xfb94]
  1E529: mov      word ptr [0xfb78], ax
  1E52F: mov      word ptr [0xfb7a], 0x4c5
  1E538: mov      byte ptr [0xfb7c], 4
  1E53F: mov      word ptr [0xfb7d], 0x280
  1E548: mov      word ptr [0xfb7f], 0x190
  1E551: mov      ecx, dword ptr [0xf914]
  1E557: mov      ebx, 1
  1E55C: mov      edx, 9
  1E561: mov      eax, 0xfb78
  1E566: call     0x2a6b7  ; write_data_to_alfred1
  1E56B: mov      eax, dword ptr [0xfaac]
  1E570: mov      edx, dword ptr [eax + 0x50]
  1E573: add      edx, 0x4c5
  1E579: mov      eax, dword ptr [0xf8f0]
  1E57E: xor      ebx, ebx
  1E580: call     0x2a342  ; file_seek
  1E585: mov      ecx, dword ptr [0xf8f0]
  1E58B: mov      eax, dword ptr [0xfac8]
  1E590: add      eax, 0x4c5
  1E595: jmp      0x1e808
  1E59A: push     0x10
  1E59F: call     0x2a218  ; __STK
  1E5A4: push     ebx
  1E5A5: push     ecx
  1E5A6: push     edx
  1E5A7: mov      eax, dword ptr [0xfac8]
  1E5AC: mov      word ptr [eax + 0x4ce], 0x280
  1E5B5: mov      eax, dword ptr [0xfac8]
  1E5BA: mov      word ptr [eax + 0x4d0], 0x190
  1E5C3: mov      ax, word ptr [0xfb94]
  1E5C9: mov      word ptr [0xfb78], ax
  1E5CF: mov      word ptr [0xfb7a], 0x4ce
  1E5D8: mov      byte ptr [0xfb7c], 4
  1E5DF: mov      word ptr [0xfb7d], 0x280
  1E5E8: mov      word ptr [0xfb7f], 0x190
  1E5F1: mov      ecx, dword ptr [0xf914]
  1E5F7: mov      ebx, 1
  1E5FC: mov      edx, 9
  1E601: mov      eax, 0xfb78
  1E606: call     0x2a6b7  ; write_data_to_alfred1
  1E60B: mov      eax, dword ptr [0xfaac]
  1E610: mov      edx, dword ptr [eax + 0x50]
  1E613: add      edx, 0x4ce
  1E619: mov      eax, dword ptr [0xf8f0]
  1E61E: xor      ebx, ebx
  1E620: call     0x2a342  ; file_seek
  1E625: mov      ecx, dword ptr [0xf8f0]
  1E62B: mov      eax, dword ptr [0xfac8]
  1E630: add      eax, 0x4ce
  1E635: jmp      0x1e808
  1E63A: push     0x10
  1E63F: call     0x2a218  ; __STK
  1E644: push     ebx
  1E645: push     ecx
  1E646: push     edx
  1E647: mov      eax, dword ptr [0xfac8]
  1E64C: mov      word ptr [eax + 0x4d7], 0x280
  1E655: mov      eax, dword ptr [0xfac8]
  1E65A: mov      word ptr [eax + 0x4d9], 0x190
  1E663: mov      ax, word ptr [0xfb94]
  1E669: mov      word ptr [0xfb78], ax
  1E66F: mov      word ptr [0xfb7a], 0x4d7
  1E678: mov      byte ptr [0xfb7c], 4
  1E67F: mov      word ptr [0xfb7d], 0x280
  1E688: mov      word ptr [0xfb7f], 0x190
  1E691: mov      ecx, dword ptr [0xf914]
  1E697: mov      ebx, 1
  1E69C: mov      edx, 9
  1E6A1: mov      eax, 0xfb78
  1E6A6: call     0x2a6b7  ; write_data_to_alfred1
  1E6AB: mov      edx, dword ptr [0xfaac]
  1E6B1: mov      edx, dword ptr [edx + 0x50]
  1E6B4: add      edx, 0x4d7
  1E6BA: mov      eax, dword ptr [0xf8f0]
  1E6BF: xor      ebx, ebx
  1E6C1: call     0x2a342  ; file_seek
  1E6C6: mov      ecx, dword ptr [0xf8f0]
  1E6CC: mov      eax, dword ptr [0xfac8]
  1E6D1: add      eax, 0x4d7
  1E6D6: mov      ebx, 1
  1E6DB: mov      edx, 4
  1E6E0: call     0x2a6b7  ; write_data_to_alfred1
  1E6E5: mov      eax, dword ptr [0xfac8]
  1E6EA: mov      word ptr [eax + 0x47d], 0xbf
  1E6F3: mov      eax, dword ptr [0xfac8]
  1E6F8: mov      word ptr [eax + 0x47f], 0xf3
  1E701: mov      ax, word ptr [0xfb94]
  1E707: mov      word ptr [0xfb78], ax
  1E70D: mov      word ptr [0xfb7a], 0x47d
  1E716: mov      byte ptr [0xfb7c], 4
  1E71D: mov      word ptr [0xfb7d], 0xde
  1E726: mov      word ptr [0xfb7f], 0x104
  1E72F: mov      ecx, dword ptr [0xf914]
  1E735: mov      ebx, 1
  1E73A: mov      edx, 9
  1E73F: mov      eax, 0xfb78
  1E744: call     0x2a6b7  ; write_data_to_alfred1
  1E749: mov      edx, dword ptr [0xfaac]
  1E74F: mov      edx, dword ptr [edx + 0x50]
  1E752: jmp      0x1d2f5
```

</details>

### PICKUP Extra 273

**Handler:** Ghidra `0x1E81B` | File `0x22A1B` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1E81B: push     4
  1E820: call     0x2a218  ; __STK
  1E825: mov      eax, dword ptr [0xb9d0]
  1E82A: jmp      0x25487
```

</details>

### PICKUP Extra 700

**Handler:** Ghidra `0x20781` | File `0x24981` | Size: 1174 bytes | 222 instructions | Ends: `jmp`

**Operations:**

   1. Load palette from ALFRED.7 offset=0x1613CE
   2. Set room_data[0xEA] = 93
   3. Set room_data[0xEB] = 88
   4. Set room_data[0xEC] = 8184
   5. Set room_data[0xEE] = 1
   6. Set room_data[0xEF] = 0
   7. Set room_data[0xF0] = 9
   8. Set room_data[0xF8] = 1
   9. Set room_data[0xFC] = 0
   10. Set room_data[0x109] = 0
   11. Set room_data[0x10A] = 0
   12. Set room_data[0x10D] = 1
   13. Set room_data[0xFE] = 767
   14. Set room_data[0x116] = 68
   15. Set room_data[0x117] = 31
   16. Set room_data[0x118] = 2108
   17. Set room_data[0x11A] = 1
   18. Set room_data[0x11B] = 0
   19. Set room_data[0x11C] = 7
   20. Set room_data[0x124] = 1
   21. Set room_data[0x128] = 0
   22. Set room_data[0x135] = 0
   23. Set room_data[0x136] = 0
   24. Set room_data[0x139] = 1
   25. Set room_data[0x142] = 79
   26. Set room_data[0x143] = 95
   27. Set room_data[0x144] = 7505
   28. Set room_data[0x146] = 1
   29. Set room_data[0x147] = 0
   30. Set room_data[0x148] = 9
   31. Set room_data[0x150] = 1
   32. Set room_data[0x154] = 0
   33. Set room_data[0x161] = 0
   34. Set room_data[0x162] = 0
   35. Set room_data[0x165] = 1
   36. Set room_data[0x16E] = 54
   37. Set room_data[0x16F] = 42
   38. Set room_data[0x170] = 2268
   39. Set room_data[0x172] = 1
   40. Set room_data[0x173] = 0
   41. Set room_data[0x174] = 8
   42. Set room_data[0x17C] = 1
   43. Set room_data[0x180] = 0
   44. Set room_data[0x18D] = 0
   45. Set room_data[0x18E] = 0
   46. Set room_data[0x191] = 1
   47. Set room_data[0x6C] = 1
   48. Set room_data[0x78] = 0
   49. Set flag [0x4FB9A] = 3
   50. Set flag [0x4FB9A] = 3
   51. JMP → 0x13A66

<details>
<summary>Raw disassembly (222 instructions)</summary>

```asm
  20781: push     0x1c
  20786: call     0x2a218  ; __STK
  2078B: push     ebx
  2078C: push     ecx
  2078D: push     edx
  2078E: push     esi
  2078F: push     edi
  20790: call     0x29037
  20795: xor      eax, eax
  20797: mov      al, byte ptr [0xc240]
  2079C: add      eax, 0x1b
  207A1: cwde     
  207A2: call     0x28d32
  207A7: mov      edx, 0x1309c
  207AC: mov      eax, 0x13098
  207B1: call     0x2942d
  207B6: mov      edx, dword ptr [0x1309c]
  207BC: mov      eax, dword ptr [0x13098]
  207C1: call     0x28fd5
  207C6: mov      esi, dword ptr [0xfa60]
  207CC: mov      edi, dword ptr [0xfabc]
  207D2: mov      eax, dword ptr [0xf908]
  207D7: xor      ebx, ebx
  207D9: mov      edx, 0x1613ce
  207DE: call     0x2a342  ; file_seek
  207E3: mov      ecx, dword ptr [0xf908]
  207E9: mov      ebx, 1
  207EE: mov      edx, 0x66da
  207F3: mov      eax, esi
  207F5: call     0x2a43e  ; file_read
  207FA: lea      edx, [edi + 0x18f4e]
  20800: mov      eax, esi
  20802: call     0x14b6a
  20807: mov      eax, dword ptr [0xfac8]
  2080C: mov      edx, dword ptr [eax + 0xe2]
  20812: add      edx, 0x11fb8
  20818: mov      dword ptr [eax + 0x10e], edx
  2081E: mov      eax, dword ptr [0xfac8]
  20823: mov      edx, dword ptr [eax + 0x10e]
  20829: add      edx, 0x39a4
  2082F: mov      dword ptr [eax + 0x13a], edx
  20835: mov      eax, dword ptr [0xfac8]
  2083A: mov      edx, dword ptr [eax + 0x13a]
  20840: add      edx, 0x107d9
  20846: mov      dword ptr [eax + 0x166], edx
  2084C: mov      eax, dword ptr [0xfac8]
  20851: add      word ptr [eax + 0xe6], 3
  20859: mov      eax, dword ptr [0xfac8]
  2085E: sub      word ptr [eax + 0xe8], 0x11
  20866: mov      eax, dword ptr [0xfac8]
  2086B: mov      byte ptr [eax + 0xea], 0x5d
  20872: mov      eax, dword ptr [0xfac8]
  20877: mov      byte ptr [eax + 0xeb], 0x58
  2087E: mov      eax, dword ptr [0xfac8]
  20883: mov      word ptr [eax + 0xec], 0x1ff8
  2088C: mov      eax, dword ptr [0xfac8]
  20891: mov      byte ptr [eax + 0xee], 1
  20898: mov      eax, dword ptr [0xfac8]
  2089D: mov      byte ptr [eax + 0xef], 0
  208A4: mov      eax, dword ptr [0xfac8]
  208A9: mov      byte ptr [eax + 0xf0], 9
  208B0: mov      eax, dword ptr [0xfac8]
  208B5: mov      byte ptr [eax + 0xf8], 1
  208BC: mov      eax, dword ptr [0xfac8]
  208C1: mov      byte ptr [eax + 0xfc], 0
  208C8: mov      eax, dword ptr [0xfac8]
  208CD: mov      byte ptr [eax + 0x109], 0
  208D4: mov      eax, dword ptr [0xfac8]
  208D9: mov      byte ptr [eax + 0x10a], 0
  208E0: mov      eax, dword ptr [0xfac8]
  208E5: mov      byte ptr [eax + 0x10d], 1
  208EC: mov      eax, dword ptr [0xfac8]
  208F1: mov      word ptr [eax + 0xfe], 0x2ff
  208FA: mov      eax, dword ptr [0xfac8]
  208FF: inc      word ptr [eax + 0x112]
  20906: mov      eax, dword ptr [0xfac8]
  2090B: mov      byte ptr [eax + 0x116], 0x44
  20912: mov      eax, dword ptr [0xfac8]
  20917: mov      byte ptr [eax + 0x117], 0x1f
  2091E: mov      eax, dword ptr [0xfac8]
  20923: mov      word ptr [eax + 0x118], 0x83c
  2092C: mov      eax, dword ptr [0xfac8]
  20931: mov      byte ptr [eax + 0x11a], 1
  20938: mov      eax, dword ptr [0xfac8]
  2093D: mov      byte ptr [eax + 0x11b], 0
  20944: mov      eax, dword ptr [0xfac8]
  20949: mov      byte ptr [eax + 0x11c], 7
  20950: mov      eax, dword ptr [0xfac8]
  20955: mov      byte ptr [eax + 0x124], 1
  2095C: mov      eax, dword ptr [0xfac8]
  20961: mov      byte ptr [eax + 0x128], 0
  20968: mov      eax, dword ptr [0xfac8]
  2096D: mov      byte ptr [eax + 0x135], 0
  20974: mov      eax, dword ptr [0xfac8]
  20979: mov      byte ptr [eax + 0x136], 0
  20980: mov      eax, dword ptr [0xfac8]
  20985: mov      byte ptr [eax + 0x139], 1
  2098C: mov      eax, dword ptr [0xfac8]
  20991: sub      word ptr [eax + 0x13e], 0xe
  20999: mov      eax, dword ptr [0xfac8]
  2099E: sub      word ptr [eax + 0x140], 0x12
  209A6: mov      eax, dword ptr [0xfac8]
  209AB: mov      byte ptr [eax + 0x142], 0x4f
  209B2: mov      eax, dword ptr [0xfac8]
  209B7: mov      byte ptr [eax + 0x143], 0x5f
  209BE: mov      eax, dword ptr [0xfac8]
  209C3: mov      word ptr [eax + 0x144], 0x1d51
  209CC: mov      eax, dword ptr [0xfac8]
  209D1: mov      byte ptr [eax + 0x146], 1
  209D8: mov      eax, dword ptr [0xfac8]
  209DD: mov      byte ptr [eax + 0x147], 0
  209E4: mov      eax, dword ptr [0xfac8]
  209E9: mov      byte ptr [eax + 0x148], 9
  209F0: mov      eax, dword ptr [0xfac8]
  209F5: mov      byte ptr [eax + 0x150], 1
  209FC: mov      eax, dword ptr [0xfac8]
  20A01: mov      byte ptr [eax + 0x154], 0
  20A08: mov      eax, dword ptr [0xfac8]
  20A0D: mov      byte ptr [eax + 0x161], 0
  20A14: mov      eax, dword ptr [0xfac8]
  20A19: mov      byte ptr [eax + 0x162], 0
  20A20: mov      eax, dword ptr [0xfac8]
  20A25: mov      byte ptr [eax + 0x165], 1
  20A2C: mov      eax, dword ptr [0xfac8]
  20A31: dec      word ptr [eax + 0x16a]
  20A38: mov      eax, dword ptr [0xfac8]
  20A3D: sub      word ptr [eax + 0x16c], 8
  20A45: mov      eax, dword ptr [0xfac8]
  20A4A: mov      byte ptr [eax + 0x16e], 0x36
  20A51: mov      eax, dword ptr [0xfac8]
  20A56: mov      byte ptr [eax + 0x16f], 0x2a
  20A5D: mov      eax, dword ptr [0xfac8]
  20A62: mov      word ptr [eax + 0x170], 0x8dc
  20A6B: mov      eax, dword ptr [0xfac8]
  20A70: mov      byte ptr [eax + 0x172], 1
  20A77: mov      eax, dword ptr [0xfac8]
  20A7C: mov      byte ptr [eax + 0x173], 0
  20A83: mov      eax, dword ptr [0xfac8]
  20A88: mov      byte ptr [eax + 0x174], 8
  20A8F: mov      eax, dword ptr [0xfac8]
  20A94: mov      byte ptr [eax + 0x17c], 1
  20A9B: mov      eax, dword ptr [0xfac8]
  20AA0: mov      byte ptr [eax + 0x180], 0
  20AA7: mov      eax, dword ptr [0xfac8]
  20AAC: mov      byte ptr [eax + 0x18d], 0
  20AB3: mov      eax, dword ptr [0xfac8]
  20AB8: mov      byte ptr [eax + 0x18e], 0
  20ABF: mov      eax, dword ptr [0xfac8]
  20AC4: mov      byte ptr [eax + 0x191], 1
  20ACB: push     0x15f
  20AD0: call     0x2a258
  20AD5: add      esp, 4
  20AD8: call     0x147c9
  20ADD: xor      eax, eax
  20ADF: call     0x15e4c
  20AE4: xor      eax, eax
  20AE6: call     0x1bfba
  20AEB: mov      eax, dword ptr [0xfac8]
  20AF0: xor      edx, edx
  20AF2: mov      dl, byte ptr [eax + 0xfd]
  20AF8: cmp      edx, 0xff
  20AFE: jne      0x20acb
  20B00: xor      edx, edx
  20B02: mov      dl, byte ptr [eax + 0x129]
  20B08: cmp      edx, 0xff
  20B0E: jne      0x20acb
  20B10: xor      edx, edx
  20B12: mov      dl, byte ptr [eax + 0x155]
  20B18: cmp      edx, 0xff
  20B1E: jne      0x20acb
  20B20: xor      edx, edx
  20B22: mov      dl, byte ptr [eax + 0x181]
  20B28: cmp      edx, 0xff
  20B2E: jne      0x20acb
  20B30: mov      dx, word ptr [0xfb96]
  20B37: add      edx, 0x46
  20B3A: mov      word ptr [eax + 0x7a], 0x14
  20B40: push     0x160
  20B45: call     0x2a258
  20B4A: add      esp, 4
  20B4D: mov      eax, dword ptr [0xfac8]
  20B52: cmp      dx, word ptr [eax + 0x62]
  20B56: ja       0x20b6d
  20B58: call     0x147c9
  20B5D: xor      eax, eax
  20B5F: call     0x15e4c
  20B64: xor      eax, eax
  20B66: call     0x1bfba
  20B6B: jmp      0x20b40
  20B6D: mov      word ptr [eax + 0x7a], 0
  20B73: mov      edx, dword ptr [0xfad0]
  20B79: mov      eax, dword ptr [0xfabc]
  20B7E: mov      ebx, 0x13a7
  20B83: call     0x2a66b  ; memcpy_wrapper
  20B88: mov      eax, dword ptr [0xfac8]
  20B8D: mov      byte ptr [eax + 0x6c], 1
  20B91: mov      eax, dword ptr [0xfac8]
  20B96: mov      byte ptr [eax + 0x78], 0
  20B9A: xor      edx, edx
  20B9C: mov      eax, 2
  20BA1: call     0x18dce
  20BA6: call     0x1b8b3
  20BAB: mov      word ptr [0xfb96], 0x10f
  20BB4: mov      word ptr [0xfb98], 0x181
  20BBD: mov      byte ptr [0xfb9a], 3
  20BC4: xor      edx, edx
  20BC6: mov      eax, 0x28
  20BCB: call     0x152f5
  20BD0: xor      edx, edx
  20BD2: mov      eax, 2
  20BD7: call     0x18dce
  20BDC: call     0x1b8b3
  20BE1: mov      word ptr [0xfb96], 0xd0
  20BEA: mov      word ptr [0xfb98], 0x185
  20BF3: mov      byte ptr [0xfb9a], 3
  20BFA: xor      edx, edx
  20BFC: mov      eax, 0x29
  20C01: call     0x152f5
  20C06: xor      edx, edx
  20C08: mov      eax, 2
  20C0D: call     0x18dce
  20C12: jmp      0x13a66
```

</details>

---

## Room 0

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 191 | 243 | 32 | 11 | 261 | Visible |
| 1 | 0x485 | 0x00 | 123 | 146 | 100 | 49 | 262 | Visible |
| 2 | 0x48E | 0x01 | 191 | 258 | 32 | 11 | 263 | Visible |
| 3 | 0x497 | 0x00 | 303 | 138 | 121 | 22 | 264 | Visible |
| 4 | 0x4A0 | 0x08 | 174 | 206 | 31 | 15 | 0 | Visible |
| 5 | 0x4A9 | 0x00 | 303 | 164 | 90 | 28 | 260 | Visible |
| 6 | 0x4B2 | 0x00 | 299 | 233 | 190 | 49 | 267 | Visible |
| 7 | 0x4BB | 0x03 | 231 | 138 | 65 | 136 | 268 | Visible |
| 8 | 0x4C4 | 0x08 | 191 | 243 | 32 | 11 | 1 | Visible |
| 9 | 0x4CD | 0x08 | 191 | 243 | 32 | 11 | 2 | Visible |
| 10 | 0x4D6 | 0x08 | 191 | 243 | 32 | 11 | 3 | Visible |
| 11 | 0x4DF | 0x00 | 58 | 176 | 41 | 54 | 3 | Visible |

### OPEN Extra 261

**Handler:** Ghidra `0x1C25A` | File `0x2045A` | Size: 209 bytes | 42 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4968E] == 0
   2. Set flag [0x4968E] = 1
   3. Display sticker from ALFRED.6 offset=0x5C561, size=0x1CD
   4. HIDE hotspot[0] @0x47D → (640, 400)

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x47D | 0 | 261 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (42 instructions)</summary>

```asm
  1C25A: push     0x10
  1C25F: call     0x2a218  ; __STK
  1C264: push     ebx
  1C265: push     ecx
  1C266: push     edx
  1C267: cmp      byte ptr [0x968e], 0
  1C26E: jne      0x1c32b
  1C274: mov      byte ptr [0x968e], 1
  1C27B: mov      edx, 0x1cd
  1C280: mov      eax, 0x5c561
  1C285: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1C28A: mov      eax, dword ptr [0xfac8]
  1C28F: mov      word ptr [eax + 0x47d], 0x280
  1C298: mov      eax, dword ptr [0xfac8]
  1C29D: mov      word ptr [eax + 0x47f], 0x190
  1C2A6: mov      ax, word ptr [0xfb94]
  1C2AC: mov      word ptr [0xfb78], ax
  1C2B2: mov      word ptr [0xfb7a], 0x47d
  1C2BB: mov      byte ptr [0xfb7c], 4
  1C2C2: mov      word ptr [0xfb7d], 0x280
  1C2CB: mov      word ptr [0xfb7f], 0x190
  1C2D4: mov      ecx, dword ptr [0xf914]
  1C2DA: mov      ebx, 1
  1C2DF: mov      edx, 9
  1C2E4: mov      eax, 0xfb78
  1C2E9: call     0x2a6b7  ; write_data_to_alfred1
  1C2EE: mov      eax, dword ptr [0xfaac]
  1C2F3: mov      edx, dword ptr [eax + 0x50]
  1C2F6: add      edx, 0x47d
  1C2FC: mov      eax, dword ptr [0xf8f0]
  1C301: xor      ebx, ebx
  1C303: call     0x2a342  ; file_seek
  1C308: mov      ecx, dword ptr [0xf8f0]
  1C30E: mov      eax, dword ptr [0xfac8]
  1C313: add      eax, 0x47d
  1C318: mov      ebx, 1
  1C31D: mov      edx, 4
  1C322: call     0x2a6b7  ; write_data_to_alfred1
  1C327: pop      edx
  1C328: pop      ecx
  1C329: pop      ebx
  1C32A: ret      
```

</details>

### OPEN Extra 263

**Handler:** Ghidra `0x1C423` | File `0x20623` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1C423: push     4
  1C428: call     0x2a218  ; __STK
  1C42D: mov      eax, dword ptr [0xb9b4]
  1C432: jmp      0x25487
```

</details>

### OPEN Extra 268

**Handler:** Ghidra `0x1C339` | File `0x20539` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49680] == 0
   2. Play ambient sound
   3. Set flag [0x49680] = 1
   4. Display sticker from ALFRED.6 offset=0x5C8FB, size=0x21C6
   5. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1C339: push     0x2c
  1C33E: call     0x2a218  ; __STK
  1C343: push     ebx
  1C344: push     ecx
  1C345: push     edx
  1C346: cmp      byte ptr [0x9680], 0
  1C34D: jne      0x1c415
  1C353: xor      eax, eax
  1C355: mov      al, byte ptr [0x13002]
  1C35A: push     eax
  1C35B: mov      edx, dword ptr [0x13234]
  1C361: push     edx
  1C362: push     0x20
  1C364: push     0x100
  1C369: push     0x100
  1C36E: push     -1
  1C370: mov      ebx, dword ptr [0x13204]
  1C376: push     ebx
  1C377: call     0x27ce1  ; play_ambient_sound
  1C37C: mov      byte ptr [0x9680], 1
  1C383: mov      edx, 0x21c6
  1C388: mov      eax, 0x5c8fb
  1C38D: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1C392: mov      eax, dword ptr [0xfac8]
  1C397: mov      byte ptr [eax + 0x1c1], 1
  1C39E: mov      ax, word ptr [0xfb94]
  1C3A4: mov      word ptr [0xfb70], ax
  1C3AA: mov      word ptr [0xfb72], 0x1c1
  1C3B3: mov      dh, 1
  1C3B5: mov      byte ptr [0xfb74], dh
  1C3BB: mov      byte ptr [0xfb75], dh
  1C3C1: mov      ecx, dword ptr [0xf914]
  1C3C7: mov      ebx, 1
  1C3CC: mov      edx, 6
  1C3D1: mov      eax, 0xfb70
  1C3D6: call     0x2a6b7  ; write_data_to_alfred1
  1C3DB: mov      eax, dword ptr [0xfaac]
  1C3E0: mov      edx, dword ptr [eax + 0x50]
  1C3E3: add      edx, 0x1c1
  1C3E9: mov      eax, dword ptr [0xf8f0]
  1C3EE: xor      ebx, ebx
  1C3F0: call     0x2a342  ; file_seek
  1C3F5: mov      ecx, dword ptr [0xf8f0]
  1C3FB: mov      eax, dword ptr [0xfac8]
  1C400: add      eax, 0x1c1
  1C405: mov      ebx, 1
  1C40A: mov      edx, ebx
  1C40C: call     0x2a6b7  ; write_data_to_alfred1
  1C411: pop      edx
  1C412: pop      ecx
  1C413: pop      ebx
  1C414: ret      
```

</details>

### PULL Extra 261

**Handler:** Ghidra `0x1D638` | File `0x21838` | Size: 45 bytes | 12 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4968E] == 0
   2. Set flag [0x4968E] = 13
   3. Display sticker from ALFRED.6 offset=0x5C72E, size=0x1CD

<details>
<summary>Raw disassembly (12 instructions)</summary>

```asm
  1D638: push     8
  1D63D: call     0x2a218  ; __STK
  1D642: push     edx
  1D643: cmp      byte ptr [0x968e], 0
  1D64A: je       0x1d665
  1D64C: xor      dl, dl
  1D64E: mov      byte ptr [0x968e], dl
  1D654: mov      edx, 0x1cd
  1D659: mov      eax, 0x5c72e
  1D65E: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D663: pop      edx
  1D664: ret      
```

</details>

### PULL Extra 268

**Handler:** Ghidra `0x1D671` | File `0x21871` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49680] == 0
   2. Play ambient sound
   3. Set flag [0x49680] = 13
   4. Display sticker from ALFRED.6 offset=0x5EAC1, size=0x21C6
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1D671: push     0x2c
  1D676: call     0x2a218  ; __STK
  1D67B: push     ebx
  1D67C: push     ecx
  1D67D: push     edx
  1D67E: cmp      byte ptr [0x9680], 0
  1D685: je       0x1d74f
  1D68B: xor      eax, eax
  1D68D: mov      al, byte ptr [0x13002]
  1D692: push     eax
  1D693: mov      edx, dword ptr [0x13238]
  1D699: push     edx
  1D69A: push     0x20
  1D69C: push     0x100
  1D6A1: push     0x100
  1D6A6: push     -1
  1D6A8: mov      ebx, dword ptr [0x13204]
  1D6AE: push     ebx
  1D6AF: call     0x27ce1  ; play_ambient_sound
  1D6B4: xor      dl, dl
  1D6B6: mov      byte ptr [0x9680], dl
  1D6BC: mov      edx, 0x21c6
  1D6C1: mov      eax, 0x5eac1
  1D6C6: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D6CB: mov      eax, dword ptr [0xfac8]
  1D6D0: mov      byte ptr [eax + 0x1c1], 0
  1D6D7: mov      ax, word ptr [0xfb94]
  1D6DD: mov      word ptr [0xfb70], ax
  1D6E3: mov      word ptr [0xfb72], 0x1c1
  1D6EC: mov      byte ptr [0xfb74], 1
  1D6F3: xor      bl, bl
  1D6F5: mov      byte ptr [0xfb75], bl
  1D6FB: mov      ecx, dword ptr [0xf914]
  1D701: mov      ebx, 1
  1D706: mov      edx, 6
  1D70B: mov      eax, 0xfb70
  1D710: call     0x2a6b7  ; write_data_to_alfred1
  1D715: mov      eax, dword ptr [0xfaac]
  1D71A: mov      edx, dword ptr [eax + 0x50]
  1D71D: add      edx, 0x1c1
  1D723: mov      eax, dword ptr [0xf8f0]
  1D728: xor      ebx, ebx
  1D72A: call     0x2a342  ; file_seek
  1D72F: mov      ecx, dword ptr [0xf8f0]
  1D735: mov      eax, dword ptr [0xfac8]
  1D73A: add      eax, 0x1c1
  1D73F: mov      ebx, 1
  1D744: mov      edx, ebx
  1D746: call     0x2a6b7  ; write_data_to_alfred1
  1D74B: pop      edx
  1D74C: pop      ecx
  1D74D: pop      ebx
  1D74E: ret      
```

</details>

### PICKUP Extra 1

**Handler:** Ghidra `0x1E4FA` | File `0x226FA` | Size: 605 bytes | 110 instructions | Ends: `jmp`

**Operations:**

   1. HIDE hotspot[8] @0x4C5 → (640, 400)
   2. HIDE hotspot[9] @0x4CE → (640, 400)
   3. HIDE hotspot[10] @0x4D7 → (640, 400)
   4. SHOW hotspot[0] @0x47D → (191, 243)
   5. JMP → 0x1D2F5

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x4C5 | 8 | 1 | 640 | 400 | HIDE |
| 0x4CE | 9 | 2 | 640 | 400 | HIDE |
| 0x4D7 | 10 | 3 | 640 | 400 | HIDE |
| 0x47D | 0 | 261 | 191 | 243 | SHOW |

<details>
<summary>Raw disassembly (110 instructions)</summary>

```asm
  1E4FA: push     0x10
  1E4FF: call     0x2a218  ; __STK
  1E504: push     ebx
  1E505: push     ecx
  1E506: push     edx
  1E507: mov      eax, dword ptr [0xfac8]
  1E50C: mov      word ptr [eax + 0x4c5], 0x280
  1E515: mov      eax, dword ptr [0xfac8]
  1E51A: mov      word ptr [eax + 0x4c7], 0x190
  1E523: mov      ax, word ptr [0xfb94]
  1E529: mov      word ptr [0xfb78], ax
  1E52F: mov      word ptr [0xfb7a], 0x4c5
  1E538: mov      byte ptr [0xfb7c], 4
  1E53F: mov      word ptr [0xfb7d], 0x280
  1E548: mov      word ptr [0xfb7f], 0x190
  1E551: mov      ecx, dword ptr [0xf914]
  1E557: mov      ebx, 1
  1E55C: mov      edx, 9
  1E561: mov      eax, 0xfb78
  1E566: call     0x2a6b7  ; write_data_to_alfred1
  1E56B: mov      eax, dword ptr [0xfaac]
  1E570: mov      edx, dword ptr [eax + 0x50]
  1E573: add      edx, 0x4c5
  1E579: mov      eax, dword ptr [0xf8f0]
  1E57E: xor      ebx, ebx
  1E580: call     0x2a342  ; file_seek
  1E585: mov      ecx, dword ptr [0xf8f0]
  1E58B: mov      eax, dword ptr [0xfac8]
  1E590: add      eax, 0x4c5
  1E595: jmp      0x1e808
  1E59A: push     0x10
  1E59F: call     0x2a218  ; __STK
  1E5A4: push     ebx
  1E5A5: push     ecx
  1E5A6: push     edx
  1E5A7: mov      eax, dword ptr [0xfac8]
  1E5AC: mov      word ptr [eax + 0x4ce], 0x280
  1E5B5: mov      eax, dword ptr [0xfac8]
  1E5BA: mov      word ptr [eax + 0x4d0], 0x190
  1E5C3: mov      ax, word ptr [0xfb94]
  1E5C9: mov      word ptr [0xfb78], ax
  1E5CF: mov      word ptr [0xfb7a], 0x4ce
  1E5D8: mov      byte ptr [0xfb7c], 4
  1E5DF: mov      word ptr [0xfb7d], 0x280
  1E5E8: mov      word ptr [0xfb7f], 0x190
  1E5F1: mov      ecx, dword ptr [0xf914]
  1E5F7: mov      ebx, 1
  1E5FC: mov      edx, 9
  1E601: mov      eax, 0xfb78
  1E606: call     0x2a6b7  ; write_data_to_alfred1
  1E60B: mov      eax, dword ptr [0xfaac]
  1E610: mov      edx, dword ptr [eax + 0x50]
  1E613: add      edx, 0x4ce
  1E619: mov      eax, dword ptr [0xf8f0]
  1E61E: xor      ebx, ebx
  1E620: call     0x2a342  ; file_seek
  1E625: mov      ecx, dword ptr [0xf8f0]
  1E62B: mov      eax, dword ptr [0xfac8]
  1E630: add      eax, 0x4ce
  1E635: jmp      0x1e808
  1E63A: push     0x10
  1E63F: call     0x2a218  ; __STK
  1E644: push     ebx
  1E645: push     ecx
  1E646: push     edx
  1E647: mov      eax, dword ptr [0xfac8]
  1E64C: mov      word ptr [eax + 0x4d7], 0x280
  1E655: mov      eax, dword ptr [0xfac8]
  1E65A: mov      word ptr [eax + 0x4d9], 0x190
  1E663: mov      ax, word ptr [0xfb94]
  1E669: mov      word ptr [0xfb78], ax
  1E66F: mov      word ptr [0xfb7a], 0x4d7
  1E678: mov      byte ptr [0xfb7c], 4
  1E67F: mov      word ptr [0xfb7d], 0x280
  1E688: mov      word ptr [0xfb7f], 0x190
  1E691: mov      ecx, dword ptr [0xf914]
  1E697: mov      ebx, 1
  1E69C: mov      edx, 9
  1E6A1: mov      eax, 0xfb78
  1E6A6: call     0x2a6b7  ; write_data_to_alfred1
  1E6AB: mov      edx, dword ptr [0xfaac]
  1E6B1: mov      edx, dword ptr [edx + 0x50]
  1E6B4: add      edx, 0x4d7
  1E6BA: mov      eax, dword ptr [0xf8f0]
  1E6BF: xor      ebx, ebx
  1E6C1: call     0x2a342  ; file_seek
  1E6C6: mov      ecx, dword ptr [0xf8f0]
  1E6CC: mov      eax, dword ptr [0xfac8]
  1E6D1: add      eax, 0x4d7
  1E6D6: mov      ebx, 1
  1E6DB: mov      edx, 4
  1E6E0: call     0x2a6b7  ; write_data_to_alfred1
  1E6E5: mov      eax, dword ptr [0xfac8]
  1E6EA: mov      word ptr [eax + 0x47d], 0xbf
  1E6F3: mov      eax, dword ptr [0xfac8]
  1E6F8: mov      word ptr [eax + 0x47f], 0xf3
  1E701: mov      ax, word ptr [0xfb94]
  1E707: mov      word ptr [0xfb78], ax
  1E70D: mov      word ptr [0xfb7a], 0x47d
  1E716: mov      byte ptr [0xfb7c], 4
  1E71D: mov      word ptr [0xfb7d], 0xde
  1E726: mov      word ptr [0xfb7f], 0x104
  1E72F: mov      ecx, dword ptr [0xf914]
  1E735: mov      ebx, 1
  1E73A: mov      edx, 9
  1E73F: mov      eax, 0xfb78
  1E744: call     0x2a6b7  ; write_data_to_alfred1
  1E749: mov      edx, dword ptr [0xfaac]
  1E74F: mov      edx, dword ptr [edx + 0x50]
  1E752: jmp      0x1d2f5
```

</details>

### PICKUP Extra 2

**Handler:** Ghidra `0x1E59A` | File `0x2279A` | Size: 445 bytes | 80 instructions | Ends: `jmp`

**Operations:**

   1. HIDE hotspot[9] @0x4CE → (640, 400)
   2. HIDE hotspot[10] @0x4D7 → (640, 400)
   3. SHOW hotspot[0] @0x47D → (191, 243)
   4. JMP → 0x1D2F5

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x4CE | 9 | 2 | 640 | 400 | HIDE |
| 0x4D7 | 10 | 3 | 640 | 400 | HIDE |
| 0x47D | 0 | 261 | 191 | 243 | SHOW |

<details>
<summary>Raw disassembly (80 instructions)</summary>

```asm
  1E59A: push     0x10
  1E59F: call     0x2a218  ; __STK
  1E5A4: push     ebx
  1E5A5: push     ecx
  1E5A6: push     edx
  1E5A7: mov      eax, dword ptr [0xfac8]
  1E5AC: mov      word ptr [eax + 0x4ce], 0x280
  1E5B5: mov      eax, dword ptr [0xfac8]
  1E5BA: mov      word ptr [eax + 0x4d0], 0x190
  1E5C3: mov      ax, word ptr [0xfb94]
  1E5C9: mov      word ptr [0xfb78], ax
  1E5CF: mov      word ptr [0xfb7a], 0x4ce
  1E5D8: mov      byte ptr [0xfb7c], 4
  1E5DF: mov      word ptr [0xfb7d], 0x280
  1E5E8: mov      word ptr [0xfb7f], 0x190
  1E5F1: mov      ecx, dword ptr [0xf914]
  1E5F7: mov      ebx, 1
  1E5FC: mov      edx, 9
  1E601: mov      eax, 0xfb78
  1E606: call     0x2a6b7  ; write_data_to_alfred1
  1E60B: mov      eax, dword ptr [0xfaac]
  1E610: mov      edx, dword ptr [eax + 0x50]
  1E613: add      edx, 0x4ce
  1E619: mov      eax, dword ptr [0xf8f0]
  1E61E: xor      ebx, ebx
  1E620: call     0x2a342  ; file_seek
  1E625: mov      ecx, dword ptr [0xf8f0]
  1E62B: mov      eax, dword ptr [0xfac8]
  1E630: add      eax, 0x4ce
  1E635: jmp      0x1e808
  1E63A: push     0x10
  1E63F: call     0x2a218  ; __STK
  1E644: push     ebx
  1E645: push     ecx
  1E646: push     edx
  1E647: mov      eax, dword ptr [0xfac8]
  1E64C: mov      word ptr [eax + 0x4d7], 0x280
  1E655: mov      eax, dword ptr [0xfac8]
  1E65A: mov      word ptr [eax + 0x4d9], 0x190
  1E663: mov      ax, word ptr [0xfb94]
  1E669: mov      word ptr [0xfb78], ax
  1E66F: mov      word ptr [0xfb7a], 0x4d7
  1E678: mov      byte ptr [0xfb7c], 4
  1E67F: mov      word ptr [0xfb7d], 0x280
  1E688: mov      word ptr [0xfb7f], 0x190
  1E691: mov      ecx, dword ptr [0xf914]
  1E697: mov      ebx, 1
  1E69C: mov      edx, 9
  1E6A1: mov      eax, 0xfb78
  1E6A6: call     0x2a6b7  ; write_data_to_alfred1
  1E6AB: mov      edx, dword ptr [0xfaac]
  1E6B1: mov      edx, dword ptr [edx + 0x50]
  1E6B4: add      edx, 0x4d7
  1E6BA: mov      eax, dword ptr [0xf8f0]
  1E6BF: xor      ebx, ebx
  1E6C1: call     0x2a342  ; file_seek
  1E6C6: mov      ecx, dword ptr [0xf8f0]
  1E6CC: mov      eax, dword ptr [0xfac8]
  1E6D1: add      eax, 0x4d7
  1E6D6: mov      ebx, 1
  1E6DB: mov      edx, 4
  1E6E0: call     0x2a6b7  ; write_data_to_alfred1
  1E6E5: mov      eax, dword ptr [0xfac8]
  1E6EA: mov      word ptr [eax + 0x47d], 0xbf
  1E6F3: mov      eax, dword ptr [0xfac8]
  1E6F8: mov      word ptr [eax + 0x47f], 0xf3
  1E701: mov      ax, word ptr [0xfb94]
  1E707: mov      word ptr [0xfb78], ax
  1E70D: mov      word ptr [0xfb7a], 0x47d
  1E716: mov      byte ptr [0xfb7c], 4
  1E71D: mov      word ptr [0xfb7d], 0xde
  1E726: mov      word ptr [0xfb7f], 0x104
  1E72F: mov      ecx, dword ptr [0xf914]
  1E735: mov      ebx, 1
  1E73A: mov      edx, 9
  1E73F: mov      eax, 0xfb78
  1E744: call     0x2a6b7  ; write_data_to_alfred1
  1E749: mov      edx, dword ptr [0xfaac]
  1E74F: mov      edx, dword ptr [edx + 0x50]
  1E752: jmp      0x1d2f5
```

</details>

### PICKUP Extra 3

**Handler:** Ghidra `0x1E63A` | File `0x2283A` | Size: 285 bytes | 50 instructions | Ends: `jmp`

**Operations:**

   1. HIDE hotspot[10] @0x4D7 → (640, 400)
   2. SHOW hotspot[0] @0x47D → (191, 243)
   3. JMP → 0x1D2F5

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x4D7 | 10 | 3 | 640 | 400 | HIDE |
| 0x47D | 0 | 261 | 191 | 243 | SHOW |

<details>
<summary>Raw disassembly (50 instructions)</summary>

```asm
  1E63A: push     0x10
  1E63F: call     0x2a218  ; __STK
  1E644: push     ebx
  1E645: push     ecx
  1E646: push     edx
  1E647: mov      eax, dword ptr [0xfac8]
  1E64C: mov      word ptr [eax + 0x4d7], 0x280
  1E655: mov      eax, dword ptr [0xfac8]
  1E65A: mov      word ptr [eax + 0x4d9], 0x190
  1E663: mov      ax, word ptr [0xfb94]
  1E669: mov      word ptr [0xfb78], ax
  1E66F: mov      word ptr [0xfb7a], 0x4d7
  1E678: mov      byte ptr [0xfb7c], 4
  1E67F: mov      word ptr [0xfb7d], 0x280
  1E688: mov      word ptr [0xfb7f], 0x190
  1E691: mov      ecx, dword ptr [0xf914]
  1E697: mov      ebx, 1
  1E69C: mov      edx, 9
  1E6A1: mov      eax, 0xfb78
  1E6A6: call     0x2a6b7  ; write_data_to_alfred1
  1E6AB: mov      edx, dword ptr [0xfaac]
  1E6B1: mov      edx, dword ptr [edx + 0x50]
  1E6B4: add      edx, 0x4d7
  1E6BA: mov      eax, dword ptr [0xf8f0]
  1E6BF: xor      ebx, ebx
  1E6C1: call     0x2a342  ; file_seek
  1E6C6: mov      ecx, dword ptr [0xf8f0]
  1E6CC: mov      eax, dword ptr [0xfac8]
  1E6D1: add      eax, 0x4d7
  1E6D6: mov      ebx, 1
  1E6DB: mov      edx, 4
  1E6E0: call     0x2a6b7  ; write_data_to_alfred1
  1E6E5: mov      eax, dword ptr [0xfac8]
  1E6EA: mov      word ptr [eax + 0x47d], 0xbf
  1E6F3: mov      eax, dword ptr [0xfac8]
  1E6F8: mov      word ptr [eax + 0x47f], 0xf3
  1E701: mov      ax, word ptr [0xfb94]
  1E707: mov      word ptr [0xfb78], ax
  1E70D: mov      word ptr [0xfb7a], 0x47d
  1E716: mov      byte ptr [0xfb7c], 4
  1E71D: mov      word ptr [0xfb7d], 0xde
  1E726: mov      word ptr [0xfb7f], 0x104
  1E72F: mov      ecx, dword ptr [0xf914]
  1E735: mov      ebx, 1
  1E73A: mov      edx, 9
  1E73F: mov      eax, 0xfb78
  1E744: call     0x2a6b7  ; write_data_to_alfred1
  1E749: mov      edx, dword ptr [0xfaac]
  1E74F: mov      edx, dword ptr [edx + 0x50]
  1E752: jmp      0x1d2f5
```

</details>

---

## Room 1

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 21 | 216 | 89 | 124 | 276 | Visible |
| 1 | 0x485 | 0x01 | 247 | 266 | 45 | 76 | 277 | Visible |
| 2 | 0x48E | 0x00 | 184 | 101 | 63 | 86 | 278 | Visible |
| 3 | 0x497 | 0x08 | 355 | 344 | 41 | 23 | 4 | Visible |

### OPEN Extra 277

**Handler:** Ghidra `0x1C437` | File `0x20637` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1C437: push     4
  1C43C: call     0x2a218  ; __STK
  1C441: mov      eax, dword ptr [0xb9cc]
  1C446: jmp      0x25487
```

</details>

### PICKUP Extra 4

**Handler:** Ghidra `0x1E757` | File `0x22957` | Size: 196 bytes | 40 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x4970C] = 1
   2. Display sticker from ALFRED.6 offset=0x80B84, size=0x3B5
   3. HIDE hotspot[3] @0x498 → (640, 400)

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x498 | 3 | 4 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (40 instructions)</summary>

```asm
  1E757: push     0x10
  1E75C: call     0x2a218  ; __STK
  1E761: push     ebx
  1E762: push     ecx
  1E763: push     edx
  1E764: mov      byte ptr [0x970c], 1
  1E76B: mov      edx, 0x3b5
  1E770: mov      eax, 0x80b84
  1E775: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1E77A: mov      eax, dword ptr [0xfac8]
  1E77F: mov      word ptr [eax + 0x498], 0x280
  1E788: mov      eax, dword ptr [0xfac8]
  1E78D: mov      word ptr [eax + 0x49a], 0x190
  1E796: mov      ax, word ptr [0xfb94]
  1E79C: mov      word ptr [0xfb78], ax
  1E7A2: mov      word ptr [0xfb7a], 0x498
  1E7AB: mov      byte ptr [0xfb7c], 4
  1E7B2: mov      word ptr [0xfb7d], 0x280
  1E7BB: mov      word ptr [0xfb7f], 0x190
  1E7C4: mov      ecx, dword ptr [0xf914]
  1E7CA: mov      ebx, 1
  1E7CF: mov      edx, 9
  1E7D4: mov      eax, 0xfb78
  1E7D9: call     0x2a6b7  ; write_data_to_alfred1
  1E7DE: mov      eax, dword ptr [0xfaac]
  1E7E3: mov      edx, dword ptr [eax + 0x50]
  1E7E6: add      edx, 0x498
  1E7EC: mov      eax, dword ptr [0xf8f0]
  1E7F1: xor      ebx, ebx
  1E7F3: call     0x2a342  ; file_seek
  1E7F8: mov      ecx, dword ptr [0xf8f0]
  1E7FE: mov      eax, dword ptr [0xfac8]
  1E803: add      eax, 0x498
  1E808: mov      ebx, 1
  1E80D: mov      edx, 4
  1E812: call     0x2a6b7  ; write_data_to_alfred1
  1E817: pop      edx
  1E818: pop      ecx
  1E819: pop      ebx
  1E81A: ret      
```

</details>

---

## Room 2

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 214 | 293 | 32 | 15 | 281 | Visible |
| 1 | 0x485 | 0x03 | 354 | 262 | 68 | 85 | 282 | Visible |
| 2 | 0x48E | 0x08 | 294 | 265 | 57 | 57 | 283 | Visible |
| 3 | 0x497 | 0x08 | 558 | 273 | 54 | 54 | 284 | Visible |
| 4 | 0x4A0 | 0x20 | 640 | 400 | 10 | 5 | 285 | Hidden |
| 5 | 0x4A9 | 0x20 | 640 | 400 | 10 | 5 | 286 | Hidden |

### OPEN Extra 282

**Handler:** Ghidra `0x1C44B` | File `0x2064B` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49798] == 0
   2. Play ambient sound
   3. Set flag [0x49798] = 1
   4. Display sticker from ALFRED.6 offset=0x4376, size=0xDA3
   5. Set room_data[0x1DD] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1C44B: push     0x2c
  1C450: call     0x2a218  ; __STK
  1C455: push     ebx
  1C456: push     ecx
  1C457: push     edx
  1C458: cmp      byte ptr [0x9798], 0
  1C45F: jne      0x1c527
  1C465: xor      eax, eax
  1C467: mov      al, byte ptr [0x13002]
  1C46C: push     eax
  1C46D: mov      edx, dword ptr [0x13234]
  1C473: push     edx
  1C474: push     0x20
  1C476: push     0x100
  1C47B: push     0x100
  1C480: push     -1
  1C482: mov      ebx, dword ptr [0x13204]
  1C488: push     ebx
  1C489: call     0x27ce1  ; play_ambient_sound
  1C48E: mov      byte ptr [0x9798], 1
  1C495: mov      edx, 0xda3
  1C49A: mov      eax, 0x4376
  1C49F: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1C4A4: mov      eax, dword ptr [0xfac8]
  1C4A9: mov      byte ptr [eax + 0x1dd], 1
  1C4B0: mov      ax, word ptr [0xfb94]
  1C4B6: mov      word ptr [0xfb70], ax
  1C4BC: mov      word ptr [0xfb72], 0x1dd
  1C4C5: mov      dh, 1
  1C4C7: mov      byte ptr [0xfb74], dh
  1C4CD: mov      byte ptr [0xfb75], dh
  1C4D3: mov      ecx, dword ptr [0xf914]
  1C4D9: mov      ebx, 1
  1C4DE: mov      edx, 6
  1C4E3: mov      eax, 0xfb70
  1C4E8: call     0x2a6b7  ; write_data_to_alfred1
  1C4ED: mov      eax, dword ptr [0xfaac]
  1C4F2: mov      edx, dword ptr [eax + 0x50]
  1C4F5: add      edx, 0x1dd
  1C4FB: mov      eax, dword ptr [0xf8f0]
  1C500: xor      ebx, ebx
  1C502: call     0x2a342  ; file_seek
  1C507: mov      ecx, dword ptr [0xf8f0]
  1C50D: mov      eax, dword ptr [0xfac8]
  1C512: add      eax, 0x1dd
  1C517: mov      ebx, 1
  1C51C: mov      edx, ebx
  1C51E: call     0x2a6b7  ; write_data_to_alfred1
  1C523: pop      edx
  1C524: pop      ecx
  1C525: pop      ebx
  1C526: ret      
```

</details>

### PULL Extra 282

**Handler:** Ghidra `0x1D75D` | File `0x2195D` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49798] == 0
   2. Play ambient sound
   3. Set flag [0x49798] = 13
   4. Display sticker from ALFRED.6 offset=0x5119, size=0xDA3
   5. Set room_data[0x1DD] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1D75D: push     0x2c
  1D762: call     0x2a218  ; __STK
  1D767: push     ebx
  1D768: push     ecx
  1D769: push     edx
  1D76A: cmp      byte ptr [0x9798], 0
  1D771: je       0x1d83b
  1D777: xor      eax, eax
  1D779: mov      al, byte ptr [0x13002]
  1D77E: push     eax
  1D77F: mov      edx, dword ptr [0x13238]
  1D785: push     edx
  1D786: push     0x20
  1D788: push     0x100
  1D78D: push     0x100
  1D792: push     -1
  1D794: mov      ebx, dword ptr [0x13204]
  1D79A: push     ebx
  1D79B: call     0x27ce1  ; play_ambient_sound
  1D7A0: xor      dl, dl
  1D7A2: mov      byte ptr [0x9798], dl
  1D7A8: mov      edx, 0xda3
  1D7AD: mov      eax, 0x5119
  1D7B2: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D7B7: mov      eax, dword ptr [0xfac8]
  1D7BC: mov      byte ptr [eax + 0x1dd], 0
  1D7C3: mov      ax, word ptr [0xfb94]
  1D7C9: mov      word ptr [0xfb70], ax
  1D7CF: mov      word ptr [0xfb72], 0x1dd
  1D7D8: mov      byte ptr [0xfb74], 1
  1D7DF: xor      bl, bl
  1D7E1: mov      byte ptr [0xfb75], bl
  1D7E7: mov      ecx, dword ptr [0xf914]
  1D7ED: mov      ebx, 1
  1D7F2: mov      edx, 6
  1D7F7: mov      eax, 0xfb70
  1D7FC: call     0x2a6b7  ; write_data_to_alfred1
  1D801: mov      eax, dword ptr [0xfaac]
  1D806: mov      edx, dword ptr [eax + 0x50]
  1D809: add      edx, 0x1dd
  1D80F: mov      eax, dword ptr [0xf8f0]
  1D814: xor      ebx, ebx
  1D816: call     0x2a342  ; file_seek
  1D81B: mov      ecx, dword ptr [0xf8f0]
  1D821: mov      eax, dword ptr [0xfac8]
  1D826: add      eax, 0x1dd
  1D82B: mov      ebx, 1
  1D830: mov      edx, ebx
  1D832: call     0x2a6b7  ; write_data_to_alfred1
  1D837: pop      edx
  1D838: pop      ecx
  1D839: pop      ebx
  1D83A: ret      
```

</details>

### PICKUP Extra 283

**Handler:** Ghidra `0x1E82F` | File `0x22A2F` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Shares handler with:** PICKUP extra 284

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1E82F: push     4
  1E834: call     0x2a218  ; __STK
  1E839: mov      eax, dword ptr [0xb9e4]
  1E83E: jmp      0x25487
```

</details>

### PICKUP Extra 284

**Handler:** Ghidra `0x1E82F` | File `0x22A2F` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Shares handler with:** PICKUP extra 283

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1E82F: push     4
  1E834: call     0x2a218  ; __STK
  1E839: mov      eax, dword ptr [0xb9e4]
  1E83E: jmp      0x25487
```

</details>

---

## Room 3

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 189 | 255 | 50 | 87 | 290 | Visible |
| 1 | 0x485 | 0x00 | 126 | 258 | 40 | 55 | 291 | Visible |
| 2 | 0x48E | 0x00 | 144 | 59 | 36 | 33 | 292 | Visible |
| 3 | 0x497 | 0x00 | 210 | 59 | 47 | 33 | 293 | Visible |
| 4 | 0x4A0 | 0x00 | 392 | 28 | 58 | 66 | 294 | Visible |
| 5 | 0x4A9 | 0x00 | 260 | 257 | 175 | 57 | 295 | Visible |
| 6 | 0x4B2 | 0x00 | 261 | 281 | 37 | 24 | 296 | Visible |
| 7 | 0x4BB | 0x00 | 299 | 302 | 36 | 5 | 297 | Visible |
| 8 | 0x4C4 | 0x00 | 311 | 268 | 6 | 33 | 298 | Visible |
| 9 | 0x4CD | 0x00 | 318 | 270 | 9 | 30 | 299 | Visible |
| 10 | 0x4D6 | 0x00 | 328 | 276 | 17 | 24 | 300 | Visible |
| 11 | 0x4DF | 0x00 | 346 | 294 | 17 | 9 | 301 | Visible |
| 12 | 0x4E8 | 0x00 | 351 | 282 | 16 | 11 | 302 | Visible |
| 13 | 0x4F1 | 0x00 | 368 | 285 | 19 | 15 | 303 | Visible |
| 14 | 0x4FA | 0x00 | 373 | 260 | 24 | 23 | 304 | Visible |
| 15 | 0x503 | 0x00 | 398 | 262 | 18 | 21 | 305 | Visible |
| 16 | 0x50C | 0x00 | 390 | 284 | 40 | 19 | 306 | Visible |
| 17 | 0x515 | 0x00 | 417 | 269 | 15 | 14 | 307 | Visible |
| 18 | 0x51E | 0x88 | 640 | 400 | 3 | 16 | 308 | Hidden |

### OPEN Extra 290

**Handler:** Ghidra `0x1C535` | File `0x20735` | Size: 239 bytes | 56 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4982B] == 0
   2. Check flag [0x49839] == 0
   3. Play ambient sound
   4. Set flag [0x49839] = 1
   5. Display sticker from ALFRED.6 offset=0xA3AA, size=0x10E6
   6. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (56 instructions)</summary>

```asm
  1C535: push     0x2c
  1C53A: call     0x2a218  ; __STK
  1C53F: push     ebx
  1C540: push     ecx
  1C541: push     edx
  1C542: cmp      byte ptr [0x982b], 0
  1C549: jne      0x1c555
  1C54B: mov      eax, dword ptr [0xb9f4]
  1C550: jmp      0x1c629
  1C555: cmp      byte ptr [0x9839], 0
  1C55C: jne      0x1c624
  1C562: xor      eax, eax
  1C564: mov      al, byte ptr [0x13002]
  1C569: push     eax
  1C56A: mov      edx, dword ptr [0x13234]
  1C570: push     edx
  1C571: push     0x20
  1C573: push     0x100
  1C578: push     0x100
  1C57D: push     -1
  1C57F: mov      ebx, dword ptr [0x13204]
  1C585: push     ebx
  1C586: call     0x27ce1  ; play_ambient_sound
  1C58B: mov      byte ptr [0x9839], 1
  1C592: mov      edx, 0x10e6
  1C597: mov      eax, 0xa3aa
  1C59C: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1C5A1: mov      eax, dword ptr [0xfac8]
  1C5A6: mov      byte ptr [eax + 0x1c1], 1
  1C5AD: mov      ax, word ptr [0xfb94]
  1C5B3: mov      word ptr [0xfb70], ax
  1C5B9: mov      word ptr [0xfb72], 0x1c1
  1C5C2: mov      bl, 1
  1C5C4: mov      byte ptr [0xfb74], bl
  1C5CA: mov      byte ptr [0xfb75], bl
  1C5D0: mov      ecx, dword ptr [0xf914]
  1C5D6: mov      ebx, 1
  1C5DB: mov      edx, 6
  1C5E0: mov      eax, 0xfb70
  1C5E5: call     0x2a6b7  ; write_data_to_alfred1
  1C5EA: mov      eax, dword ptr [0xfaac]
  1C5EF: mov      edx, dword ptr [eax + 0x50]
  1C5F2: add      edx, 0x1c1
  1C5F8: mov      eax, dword ptr [0xf8f0]
  1C5FD: xor      ebx, ebx
  1C5FF: call     0x2a342  ; file_seek
  1C604: mov      ecx, dword ptr [0xf8f0]
  1C60A: mov      eax, dword ptr [0xfac8]
  1C60F: add      eax, 0x1c1
  1C614: mov      ebx, 1
  1C619: mov      edx, ebx
  1C61B: call     0x2a6b7  ; write_data_to_alfred1
  1C620: pop      edx
  1C621: pop      ecx
  1C622: pop      ebx
  1C623: ret      
```

</details>

### PULL Extra 290

**Handler:** Ghidra `0x1D849` | File `0x21A49` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49839] == 0
   2. Play ambient sound
   3. Set flag [0x49839] = 13
   4. Display sticker from ALFRED.6 offset=0x92C4, size=0x10E6
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1D849: push     0x2c
  1D84E: call     0x2a218  ; __STK
  1D853: push     ebx
  1D854: push     ecx
  1D855: push     edx
  1D856: cmp      byte ptr [0x9839], 0
  1D85D: je       0x1d927
  1D863: xor      eax, eax
  1D865: mov      al, byte ptr [0x13002]
  1D86A: push     eax
  1D86B: mov      edx, dword ptr [0x13238]
  1D871: push     edx
  1D872: push     0x20
  1D874: push     0x100
  1D879: push     0x100
  1D87E: push     -1
  1D880: mov      ebx, dword ptr [0x13204]
  1D886: push     ebx
  1D887: call     0x27ce1  ; play_ambient_sound
  1D88C: xor      dl, dl
  1D88E: mov      byte ptr [0x9839], dl
  1D894: mov      edx, 0x10e6
  1D899: mov      eax, 0x92c4
  1D89E: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D8A3: mov      eax, dword ptr [0xfac8]
  1D8A8: mov      byte ptr [eax + 0x1c1], 0
  1D8AF: mov      ax, word ptr [0xfb94]
  1D8B5: mov      word ptr [0xfb70], ax
  1D8BB: mov      word ptr [0xfb72], 0x1c1
  1D8C4: mov      byte ptr [0xfb74], 1
  1D8CB: xor      bl, bl
  1D8CD: mov      byte ptr [0xfb75], bl
  1D8D3: mov      ecx, dword ptr [0xf914]
  1D8D9: mov      ebx, 1
  1D8DE: mov      edx, 6
  1D8E3: mov      eax, 0xfb70
  1D8E8: call     0x2a6b7  ; write_data_to_alfred1
  1D8ED: mov      eax, dword ptr [0xfaac]
  1D8F2: mov      edx, dword ptr [eax + 0x50]
  1D8F5: add      edx, 0x1c1
  1D8FB: mov      eax, dword ptr [0xf8f0]
  1D900: xor      ebx, ebx
  1D902: call     0x2a342  ; file_seek
  1D907: mov      ecx, dword ptr [0xf8f0]
  1D90D: mov      eax, dword ptr [0xfac8]
  1D912: add      eax, 0x1c1
  1D917: mov      ebx, 1
  1D91C: mov      edx, ebx
  1D91E: call     0x2a6b7  ; write_data_to_alfred1
  1D923: pop      edx
  1D924: pop      ecx
  1D925: pop      ebx
  1D926: ret      
```

</details>

### PICKUP Extra 308

**Handler:** Ghidra `0x20C17` | File `0x24E17` | Size: 84 bytes | 19 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49847] = 10
   2. Set flag [0x4984E] = 10
   3. Set flag [0x49855] = 10
   4. Set flag [0x498BE] = 10
   5. Display sticker from ALFRED.6 offset=0xB6A6, size=0x9B4
   6. Display sticker from ALFRED.6 offset=0xC05A, size=0x9B4
   7. Display sticker from ALFRED.6 offset=0xCA0E, size=0x9C2

<details>
<summary>Raw disassembly (19 instructions)</summary>

```asm
  20C17: push     8
  20C1C: call     0x2a218  ; __STK
  20C21: push     edx
  20C22: mov      ah, 1
  20C24: mov      byte ptr [0x9847], ah
  20C2A: mov      byte ptr [0x984e], ah
  20C30: mov      byte ptr [0x9855], ah
  20C36: mov      byte ptr [0x98be], ah
  20C3C: mov      edx, 0x9b4
  20C41: mov      eax, 0xb6a6
  20C46: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  20C4B: mov      edx, 0x9b4
  20C50: mov      eax, 0xc05a
  20C55: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  20C5A: mov      edx, 0x9c2
  20C5F: mov      eax, 0xca0e
  20C64: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  20C69: pop      edx
  20C6A: ret      
```

</details>

---

## Room 4

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x08 | 0 | 159 | 98 | 184 | 310 | Visible |
| 1 | 0x485 | 0x08 | 525 | 150 | 108 | 185 | 311 | Visible |
| 2 | 0x48E | 0x03 | 275 | 95 | 74 | 102 | 312 | Visible |
| 3 | 0x497 | 0x00 | 296 | 46 | 29 | 29 | 313 | Visible |
| 4 | 0x4A0 | 0x00 | 640 | 400 | 29 | 29 | 314 | Hidden |
| 5 | 0x4A9 | 0x01 | 372 | 182 | 10 | 8 | 315 | Visible |
| 6 | 0x4B2 | 0x08 | 640 | 400 | 34 | 15 | 316 | Hidden |

### OPEN Extra 312

**Handler:** Ghidra `0x1C7B5` | File `0x209B5` | Size: 40 bytes | 15 instructions | Ends: `ret`

**Operations:**

   1. Display text (ref=[0x4BA20])

<details>
<summary>Raw disassembly (15 instructions)</summary>

```asm
  1C7B5: push     0x2c
  1C7BA: call     0x2a218  ; __STK
  1C7BF: push     ebx
  1C7C0: push     ecx
  1C7C1: push     edx
  1C7C2: mov      ah, byte ptr [0x95b8]
  1C7C8: test     ah, ah
  1C7CA: jne      0x1c7dd
  1C7CC: mov      edx, dword ptr [0xba20]
  1C7D2: xor      eax, eax
  1C7D4: call     0x1b1a2  ; display_text_with_character_animation
  1C7D9: pop      edx
  1C7DA: pop      ecx
  1C7DB: pop      ebx
  1C7DC: ret      
```

</details>

### OPEN Extra 315

**Handler:** Ghidra `0x1C789` | File `0x20989` | Size: 44 bytes | 11 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x498B0] == 0
   2. Display sticker from ALFRED.6 offset=0xD3D0, size=0x9E
   3. Set flag [0x498B0] = 1

<details>
<summary>Raw disassembly (11 instructions)</summary>

```asm
  1C789: push     8
  1C78E: call     0x2a218  ; __STK
  1C793: push     edx
  1C794: cmp      byte ptr [0x98b0], 0
  1C79B: jne      0x1c7b3
  1C79D: mov      edx, 0x9e
  1C7A2: mov      eax, 0xd3d0
  1C7A7: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1C7AC: mov      byte ptr [0x98b0], 1
  1C7B3: pop      edx
  1C7B4: ret      
```

</details>

### PULL Extra 312

**Handler:** Ghidra `0x1D935` | File `0x21B35` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x498CC] == 0
   2. Play ambient sound
   3. Set flag [0x498CC] = 13
   4. Display sticker from ALFRED.6 offset=0x119D7, size=0x1D82
   5. Set room_data[0x1CF] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1D935: push     0x2c
  1D93A: call     0x2a218  ; __STK
  1D93F: push     ebx
  1D940: push     ecx
  1D941: push     edx
  1D942: cmp      byte ptr [0x98cc], 0
  1D949: je       0x1da13
  1D94F: xor      eax, eax
  1D951: mov      al, byte ptr [0x13002]
  1D956: push     eax
  1D957: mov      edx, dword ptr [0x13238]
  1D95D: push     edx
  1D95E: push     0x20
  1D960: push     0x100
  1D965: push     0x100
  1D96A: push     -1
  1D96C: mov      ebx, dword ptr [0x13204]
  1D972: push     ebx
  1D973: call     0x27ce1  ; play_ambient_sound
  1D978: xor      dl, dl
  1D97A: mov      byte ptr [0x98cc], dl
  1D980: mov      edx, 0x1d82
  1D985: mov      eax, 0x119d7
  1D98A: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D98F: mov      eax, dword ptr [0xfac8]
  1D994: mov      byte ptr [eax + 0x1cf], 0
  1D99B: mov      ax, word ptr [0xfb94]
  1D9A1: mov      word ptr [0xfb70], ax
  1D9A7: mov      word ptr [0xfb72], 0x1cf
  1D9B0: mov      byte ptr [0xfb74], 1
  1D9B7: xor      bl, bl
  1D9B9: mov      byte ptr [0xfb75], bl
  1D9BF: mov      ecx, dword ptr [0xf914]
  1D9C5: mov      ebx, 1
  1D9CA: mov      edx, 6
  1D9CF: mov      eax, 0xfb70
  1D9D4: call     0x2a6b7  ; write_data_to_alfred1
  1D9D9: mov      eax, dword ptr [0xfaac]
  1D9DE: mov      edx, dword ptr [eax + 0x50]
  1D9E1: add      edx, 0x1cf
  1D9E7: mov      eax, dword ptr [0xf8f0]
  1D9EC: xor      ebx, ebx
  1D9EE: call     0x2a342  ; file_seek
  1D9F3: mov      ecx, dword ptr [0xf8f0]
  1D9F9: mov      eax, dword ptr [0xfac8]
  1D9FE: add      eax, 0x1cf
  1DA03: mov      ebx, 1
  1DA08: mov      edx, ebx
  1DA0A: call     0x2a6b7  ; write_data_to_alfred1
  1DA0F: pop      edx
  1DA10: pop      ecx
  1DA11: pop      ebx
  1DA12: ret      
```

</details>

### PICKUP Extra 310

**Handler:** Ghidra `0x1EB8A` | File `0x22D8A` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Shares handler with:** PICKUP extra 311

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1EB8A: push     4
  1EB8F: call     0x2a218  ; __STK
  1EB94: mov      eax, dword ptr [0xba48]
  1EB99: jmp      0x25487
```

</details>

### PICKUP Extra 311

**Handler:** Ghidra `0x1EB8A` | File `0x22D8A` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Shares handler with:** PICKUP extra 310

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1EB8A: push     4
  1EB8F: call     0x2a218  ; __STK
  1EB94: mov      eax, dword ptr [0xba48]
  1EB99: jmp      0x25487
```

</details>

### PICKUP Extra 316

**Handler:** Ghidra `0x1E843` | File `0x22A43` | Size: 824 bytes | 189 instructions | Ends: `jmp`

**Operations:**

   1. Check flag [0x498C5] == 0
   2. Set flag [0x498B7] = 1
   3. Play ambient sound
   4. Set flag [0x4F93F] = 13
   5. Check combined flags == 0x3
   6. Set flag [0x4F93F] = 10
   7. Set flag [0x4F93F] = 12
   8. Check combined flags == 0x3
   9. Set flag [0x498C5] = 1
   10. Display sticker from ALFRED.6 offset=0xFB8F, size=0xC6
   11. HIDE hotspot[3] @0x498 → (640, 400)
   12. SHOW hotspot[4] @0x4A1 → (296, 46)
   13. Update conversation state (room=4)
   14. Default verb response ("I can't do that")
   15. JMP → 0x13A65

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x498 | 3 | 313 | 640 | 400 | HIDE |
| 0x4A1 | 4 | 314 | 296 | 46 | SHOW |

<details>
<summary>Raw disassembly (189 instructions)</summary>

```asm
  1E843: push     0x38
  1E848: call     0x2a218  ; __STK
  1E84D: push     ebx
  1E84E: push     ecx
  1E84F: push     edx
  1E850: push     esi
  1E851: push     edi
  1E852: push     ebp
  1E853: cmp      byte ptr [0x98c5], 0
  1E85A: jne      0x1eb7b
  1E860: mov      byte ptr [0x98b7], 1
  1E867: mov      eax, 0x783a
  1E86C: call     0x25e90  ; allocate_memory
  1E871: mov      ebp, eax
  1E873: mov      edi, eax
  1E875: mov      esi, eax
  1E877: mov      eax, dword ptr [0xf908]
  1E87C: xor      ebx, ebx
  1E87E: mov      edx, 0x9088
  1E883: call     0x2a342  ; file_seek
  1E888: mov      ecx, dword ptr [0xf908]
  1E88E: mov      ebx, 1
  1E893: mov      edx, 0x783a
  1E898: mov      eax, ebp
  1E89A: call     0x2a43e  ; file_read
  1E89F: xor      eax, eax
  1E8A1: mov      al, byte ptr [0x13002]
  1E8A6: push     eax
  1E8A7: mov      edx, dword ptr [0x13238]
  1E8AD: push     edx
  1E8AE: push     0x20
  1E8B0: push     0x100
  1E8B5: push     0x100
  1E8BA: push     -1
  1E8BC: mov      ebx, dword ptr [0x13204]
  1E8C2: push     ebx
  1E8C3: call     0x27ce1  ; play_ambient_sound
  1E8C8: xor      dl, dl
  1E8CA: mov      ebx, 0x2d
  1E8CF: mov      ecx, 0x57
  1E8D4: jmp      0x1e915
  1E8D6: xor      eax, eax
  1E8D8: call     0x1bfba
  1E8DD: call     0x147c9
  1E8E2: mov      dword ptr [0xf932], esi
  1E8E8: xor      dh, dh
  1E8EA: mov      byte ptr [0xf93f], dh
  1E8F0: mov      word ptr [0xf93a], bx
  1E8F7: mov      word ptr [0xf93c], cx
  1E8FE: add      word ptr [0xf938], 0xf
  1E906: add      esi, 0xf4b
  1E90C: xor      eax, eax
  1E90E: call     0x15e4c
  1E913: inc      dl
  1E915: xor      eax, eax
  1E917: mov      al, dl
  1E919: cmp      eax, 3
  1E91C: jl       0x1e8d6
  1E91E: add      esi, 0x1109
  1E924: mov      ebx, esi
  1E926: xor      dh, dh
  1E928: xor      eax, eax
  1E92A: mov      al, dh
  1E92C: cmp      eax, 0x14
  1E92F: jge      0x1e98e
  1E931: xor      dl, dl
  1E933: jmp      0x1e97f
  1E935: xor      eax, eax
  1E937: call     0x1bfba
  1E93C: call     0x147c9
  1E941: mov      dword ptr [0xf932], esi
  1E947: xor      al, al
  1E949: mov      byte ptr [0xf93f], al
  1E94E: mov      word ptr [0xf93a], 0x52
  1E957: mov      word ptr [0xf93c], 0x3a
  1E960: add      word ptr [0xf938], 0x2c
  1E968: sub      word ptr [0xf936], 0x15
  1E970: add      esi, 0x1294
  1E976: xor      eax, eax
  1E978: call     0x15e4c
  1E97D: inc      dl
  1E97F: xor      eax, eax
  1E981: mov      al, dl
  1E983: cmp      eax, 2
  1E986: jl       0x1e935
  1E988: mov      esi, ebx
  1E98A: inc      dh
  1E98C: jmp      0x1e928
  1E98E: mov      esi, edi
  1E990: mov      edx, 0xf4b
  1E995: lea      ebx, [edi + 0x1e96]
  1E99B: test     dx, dx
  1E99E: je       0x1e9ad
  1E9A0: mov      ah, byte ptr [esi]
  1E9A2: mov      al, byte ptr [ebx]
  1E9A4: mov      byte ptr [esi], al
  1E9A6: mov      byte ptr [ebx], ah
  1E9A8: inc      esi
  1E9A9: inc      ebx
  1E9AA: dec      edx
  1E9AB: jmp      0x1e99b
  1E9AD: mov      esi, edi
  1E9AF: xor      dl, dl
  1E9B1: mov      ebx, 0x2d
  1E9B6: jmp      0x1e9f9
  1E9B8: xor      eax, eax
  1E9BA: call     0x1bfba
  1E9BF: call     0x147c9
  1E9C4: mov      dword ptr [0xf932], esi
  1E9CA: xor      ch, ch
  1E9CC: mov      byte ptr [0xf93f], ch
  1E9D2: mov      word ptr [0xf93a], bx
  1E9D9: mov      word ptr [0xf93c], 0x57
  1E9E2: add      word ptr [0xf938], 0xf
  1E9EA: add      esi, 0xf4b
  1E9F0: xor      eax, eax
  1E9F2: call     0x15e4c
  1E9F7: inc      dl
  1E9F9: xor      eax, eax
  1E9FB: mov      al, dl
  1E9FD: cmp      eax, 3
  1EA00: jl       0x1e9b8
  1EA02: mov      byte ptr [0x98c5], 1
  1EA09: mov      edx, 0xc6
  1EA0E: mov      eax, 0xfb8f
  1EA13: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1EA18: mov      eax, dword ptr [0xfac8]
  1EA1D: mov      word ptr [eax + 0x498], 0x280
  1EA26: mov      eax, dword ptr [0xfac8]
  1EA2B: mov      word ptr [eax + 0x49a], 0x190
  1EA34: mov      ax, word ptr [0xfb94]
  1EA3A: mov      word ptr [0xfb78], ax
  1EA40: mov      word ptr [0xfb7a], 0x498
  1EA49: mov      byte ptr [0xfb7c], 4
  1EA50: mov      word ptr [0xfb7d], 0x280
  1EA59: mov      word ptr [0xfb7f], 0x190
  1EA62: mov      ecx, dword ptr [0xf914]
  1EA68: mov      ebx, 1
  1EA6D: mov      edx, 9
  1EA72: mov      eax, 0xfb78
  1EA77: call     0x2a6b7  ; write_data_to_alfred1
  1EA7C: mov      edx, dword ptr [0xfaac]
  1EA82: mov      edx, dword ptr [edx + 0x50]
  1EA85: add      edx, 0x498
  1EA8B: mov      eax, dword ptr [0xf8f0]
  1EA90: xor      ebx, ebx
  1EA92: call     0x2a342  ; file_seek
  1EA97: mov      ecx, dword ptr [0xf8f0]
  1EA9D: mov      eax, dword ptr [0xfac8]
  1EAA2: add      eax, 0x498
  1EAA7: mov      ebx, 1
  1EAAC: mov      edx, 4
  1EAB1: call     0x2a6b7  ; write_data_to_alfred1
  1EAB6: mov      eax, dword ptr [0xfac8]
  1EABB: mov      word ptr [eax + 0x4a1], 0x128
  1EAC4: mov      eax, dword ptr [0xfac8]
  1EAC9: mov      word ptr [eax + 0x4a3], 0x2e
  1EAD2: mov      ax, word ptr [0xfb94]
  1EAD8: mov      word ptr [0xfb78], ax
  1EADE: mov      word ptr [0xfb7a], 0x4a1
  1EAE7: mov      byte ptr [0xfb7c], 4
  1EAEE: mov      word ptr [0xfb7d], 0x128
  1EAF7: mov      word ptr [0xfb7f], 0x2e
  1EB00: mov      ecx, dword ptr [0xf914]
  1EB06: mov      ebx, 1
  1EB0B: mov      edx, 9
  1EB10: mov      eax, 0xfb78
  1EB15: call     0x2a6b7  ; write_data_to_alfred1
  1EB1A: mov      edx, dword ptr [0xfaac]
  1EB20: mov      edx, dword ptr [edx + 0x50]
  1EB23: add      edx, 0x4a1
  1EB29: mov      eax, dword ptr [0xf8f0]
  1EB2E: xor      ebx, ebx
  1EB30: call     0x2a342  ; file_seek
  1EB35: mov      ecx, dword ptr [0xf8f0]
  1EB3B: mov      eax, dword ptr [0xfac8]
  1EB40: add      eax, 0x4a1
  1EB45: mov      ebx, 1
  1EB4A: mov      edx, 4
  1EB4F: call     0x2a6b7  ; write_data_to_alfred1
  1EB54: mov      ebx, 1
  1EB59: xor      edx, edx
  1EB5B: mov      eax, 4
  1EB60: call     0x1b666  ; update_conversation_state
  1EB65: mov      eax, dword ptr [0xba4c]
  1EB6A: call     0x25487  ; default_verb_response
  1EB6F: mov      eax, edi
  1EB71: call     0x2a60d  ; free_memory
  1EB76: jmp      0x13a65
```

</details>

---

## Room 8

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 276 | 213 | 62 | 90 | 355 | Visible |
| 1 | 0x485 | 0x00 | 300 | 36 | 31 | 31 | 356 | Visible |
| 2 | 0x48E | 0x08 | 227 | 286 | 36 | 64 | 357 | Visible |

### OPEN Extra 355

**Handler:** Ghidra `0x1C8E3` | File `0x20AE3` | Size: 228 bytes | 54 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49AE0] == 0
   2. Play ambient sound
   3. Set flag [0x49AE0] = 1
   4. Set flag [0x495BF] = 13
   5. Display sticker from ALFRED.6 offset=0x14A9D, size=0x117E
   6. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (54 instructions)</summary>

```asm
  1C8E3: push     0x2c
  1C8E8: call     0x2a218  ; __STK
  1C8ED: push     ebx
  1C8EE: push     ecx
  1C8EF: push     edx
  1C8F0: cmp      byte ptr [0x9ae0], 0
  1C8F7: jne      0x1c9c7
  1C8FD: xor      eax, eax
  1C8FF: mov      al, byte ptr [0x13002]
  1C904: push     eax
  1C905: mov      edx, dword ptr [0x13234]
  1C90B: push     edx
  1C90C: push     0x20
  1C90E: push     0x100
  1C913: push     0x100
  1C918: push     -1
  1C91A: mov      ebx, dword ptr [0x13204]
  1C920: push     ebx
  1C921: call     0x27ce1  ; play_ambient_sound
  1C926: mov      byte ptr [0x9ae0], 1
  1C92D: xor      dh, dh
  1C92F: mov      byte ptr [0x95bf], dh
  1C935: mov      edx, 0x117e
  1C93A: mov      eax, 0x14a9d
  1C93F: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1C944: mov      eax, dword ptr [0xfac8]
  1C949: mov      byte ptr [eax + 0x1c1], 1
  1C950: mov      ax, word ptr [0xfb94]
  1C956: mov      word ptr [0xfb70], ax
  1C95C: mov      word ptr [0xfb72], 0x1c1
  1C965: mov      bl, 1
  1C967: mov      byte ptr [0xfb74], bl
  1C96D: mov      byte ptr [0xfb75], bl
  1C973: mov      ecx, dword ptr [0xf914]
  1C979: mov      ebx, 1
  1C97E: mov      edx, 6
  1C983: mov      eax, 0xfb70
  1C988: call     0x2a6b7  ; write_data_to_alfred1
  1C98D: mov      eax, dword ptr [0xfaac]
  1C992: mov      edx, dword ptr [eax + 0x50]
  1C995: add      edx, 0x1c1
  1C99B: mov      eax, dword ptr [0xf8f0]
  1C9A0: xor      ebx, ebx
  1C9A2: call     0x2a342  ; file_seek
  1C9A7: mov      ecx, dword ptr [0xf8f0]
  1C9AD: mov      eax, dword ptr [0xfac8]
  1C9B2: add      eax, 0x1c1
  1C9B7: mov      ebx, 1
  1C9BC: mov      edx, ebx
  1C9BE: call     0x2a6b7  ; write_data_to_alfred1
  1C9C3: pop      edx
  1C9C4: pop      ecx
  1C9C5: pop      ebx
  1C9C6: ret      
```

</details>

### PULL Extra 355

**Handler:** Ghidra `0x1DA21` | File `0x21C21` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49AE0] == 0
   2. Play ambient sound
   3. Set flag [0x49AE0] = 13
   4. Display sticker from ALFRED.6 offset=0x1391F, size=0x117E
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1DA21: push     0x2c
  1DA26: call     0x2a218  ; __STK
  1DA2B: push     ebx
  1DA2C: push     ecx
  1DA2D: push     edx
  1DA2E: cmp      byte ptr [0x9ae0], 0
  1DA35: je       0x1daff
  1DA3B: xor      eax, eax
  1DA3D: mov      al, byte ptr [0x13002]
  1DA42: push     eax
  1DA43: mov      edx, dword ptr [0x13238]
  1DA49: push     edx
  1DA4A: push     0x20
  1DA4C: push     0x100
  1DA51: push     0x100
  1DA56: push     -1
  1DA58: mov      ebx, dword ptr [0x13204]
  1DA5E: push     ebx
  1DA5F: call     0x27ce1  ; play_ambient_sound
  1DA64: xor      dl, dl
  1DA66: mov      byte ptr [0x9ae0], dl
  1DA6C: mov      edx, 0x117e
  1DA71: mov      eax, 0x1391f
  1DA76: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1DA7B: mov      eax, dword ptr [0xfac8]
  1DA80: mov      byte ptr [eax + 0x1c1], 0
  1DA87: mov      ax, word ptr [0xfb94]
  1DA8D: mov      word ptr [0xfb70], ax
  1DA93: mov      word ptr [0xfb72], 0x1c1
  1DA9C: mov      byte ptr [0xfb74], 1
  1DAA3: xor      bl, bl
  1DAA5: mov      byte ptr [0xfb75], bl
  1DAAB: mov      ecx, dword ptr [0xf914]
  1DAB1: mov      ebx, 1
  1DAB6: mov      edx, 6
  1DABB: mov      eax, 0xfb70
  1DAC0: call     0x2a6b7  ; write_data_to_alfred1
  1DAC5: mov      eax, dword ptr [0xfaac]
  1DACA: mov      edx, dword ptr [eax + 0x50]
  1DACD: add      edx, 0x1c1
  1DAD3: mov      eax, dword ptr [0xf8f0]
  1DAD8: xor      ebx, ebx
  1DADA: call     0x2a342  ; file_seek
  1DADF: mov      ecx, dword ptr [0xf8f0]
  1DAE5: mov      eax, dword ptr [0xfac8]
  1DAEA: add      eax, 0x1c1
  1DAEF: mov      ebx, 1
  1DAF4: mov      edx, ebx
  1DAF6: call     0x2a6b7  ; write_data_to_alfred1
  1DAFB: pop      edx
  1DAFC: pop      ecx
  1DAFD: pop      ebx
  1DAFE: ret      
```

</details>

### PICKUP Extra 357

**Handler:** Ghidra `0x1EB9E` | File `0x22D9E` | Size: 146 bytes | 31 instructions | Ends: `jmp`

**Operations:**

   1. Set room_data[0x48E] = 0
   2. JMP → 0x1E812

<details>
<summary>Raw disassembly (31 instructions)</summary>

```asm
  1EB9E: push     0x10
  1EBA3: call     0x2a218  ; __STK
  1EBA8: push     ebx
  1EBA9: push     ecx
  1EBAA: push     edx
  1EBAB: mov      eax, 9
  1EBB0: call     0x24157
  1EBB5: mov      eax, dword ptr [0xfac8]
  1EBBA: mov      byte ptr [eax + 0x48e], 0
  1EBC1: mov      ax, word ptr [0xfb94]
  1EBC7: mov      word ptr [0xfb70], ax
  1EBCD: mov      word ptr [0xfb72], 0x48e
  1EBD6: mov      byte ptr [0xfb74], 1
  1EBDD: xor      dl, dl
  1EBDF: mov      byte ptr [0xfb75], dl
  1EBE5: mov      ecx, dword ptr [0xf914]
  1EBEB: mov      ebx, 1
  1EBF0: mov      edx, 6
  1EBF5: mov      eax, 0xfb70
  1EBFA: call     0x2a6b7  ; write_data_to_alfred1
  1EBFF: mov      eax, dword ptr [0xfaac]
  1EC04: mov      edx, dword ptr [eax + 0x50]
  1EC07: add      edx, 0x48e
  1EC0D: mov      eax, dword ptr [0xf8f0]
  1EC12: xor      ebx, ebx
  1EC14: call     0x2a342  ; file_seek
  1EC19: mov      ecx, dword ptr [0xf8f0]
  1EC1F: mov      ebx, 1
  1EC24: mov      edx, ebx
  1EC26: mov      eax, 0xfb75
  1EC2B: jmp      0x1e812
```

</details>

---

## Room 9

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x08 | 53 | 148 | 60 | 205 | 360 | Visible |
| 1 | 0x485 | 0x08 | 438 | 187 | 62 | 93 | 361 | Visible |
| 2 | 0x48E | 0x08 | 508 | 162 | 56 | 130 | 362 | Visible |
| 3 | 0x497 | 0x03 | 309 | 151 | 83 | 126 | 363 | Visible |
| 4 | 0x4A0 | 0x00 | 182 | 291 | 26 | 23 | 364 | Visible |
| 5 | 0x4A9 | 0x00 | 337 | 102 | 26 | 25 | 365 | Visible |
| 6 | 0x4B2 | 0x00 | 249 | 253 | 10 | 7 | 365 | Visible |
| 7 | 0x4BB | 0x00 | 232 | 263 | 27 | 23 | 365 | Visible |

### OPEN Extra 363

**Handler:** Ghidra `0x1C9E9` | File `0x20BE9` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495BF] == 0
   2. Play ambient sound
   3. Set flag [0x495BF] = 1
   4. Display sticker from ALFRED.6 offset=0x17601, size=0x19E6
   5. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1C9E9: push     0x2c
  1C9EE: call     0x2a218  ; __STK
  1C9F3: push     ebx
  1C9F4: push     ecx
  1C9F5: push     edx
  1C9F6: cmp      byte ptr [0x95bf], 0
  1C9FD: jne      0x1cac5
  1CA03: xor      eax, eax
  1CA05: mov      al, byte ptr [0x13002]
  1CA0A: push     eax
  1CA0B: mov      edx, dword ptr [0x13234]
  1CA11: push     edx
  1CA12: push     0x20
  1CA14: push     0x100
  1CA19: push     0x100
  1CA1E: push     -1
  1CA20: mov      ebx, dword ptr [0x13204]
  1CA26: push     ebx
  1CA27: call     0x27ce1  ; play_ambient_sound
  1CA2C: mov      byte ptr [0x95bf], 1
  1CA33: mov      edx, 0x19e6
  1CA38: mov      eax, 0x17601
  1CA3D: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1CA42: mov      eax, dword ptr [0xfac8]
  1CA47: mov      byte ptr [eax + 0x1c1], 1
  1CA4E: mov      ax, word ptr [0xfb94]
  1CA54: mov      word ptr [0xfb70], ax
  1CA5A: mov      word ptr [0xfb72], 0x1c1
  1CA63: mov      dh, 1
  1CA65: mov      byte ptr [0xfb74], dh
  1CA6B: mov      byte ptr [0xfb75], dh
  1CA71: mov      ecx, dword ptr [0xf914]
  1CA77: mov      ebx, 1
  1CA7C: mov      edx, 6
  1CA81: mov      eax, 0xfb70
  1CA86: call     0x2a6b7  ; write_data_to_alfred1
  1CA8B: mov      eax, dword ptr [0xfaac]
  1CA90: mov      edx, dword ptr [eax + 0x50]
  1CA93: add      edx, 0x1c1
  1CA99: mov      eax, dword ptr [0xf8f0]
  1CA9E: xor      ebx, ebx
  1CAA0: call     0x2a342  ; file_seek
  1CAA5: mov      ecx, dword ptr [0xf8f0]
  1CAAB: mov      eax, dword ptr [0xfac8]
  1CAB0: add      eax, 0x1c1
  1CAB5: mov      ebx, 1
  1CABA: mov      edx, ebx
  1CABC: call     0x2a6b7  ; write_data_to_alfred1
  1CAC1: pop      edx
  1CAC2: pop      ecx
  1CAC3: pop      ebx
  1CAC4: ret      
```

</details>

### PULL Extra 363

**Handler:** Ghidra `0x1DB0D` | File `0x21D0D` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495BF] == 0
   2. Play ambient sound
   3. Set flag [0x495BF] = 13
   4. Display sticker from ALFRED.6 offset=0x15C1B, size=0x19E6
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1DB0D: push     0x2c
  1DB12: call     0x2a218  ; __STK
  1DB17: push     ebx
  1DB18: push     ecx
  1DB19: push     edx
  1DB1A: cmp      byte ptr [0x95bf], 0
  1DB21: je       0x1dbeb
  1DB27: xor      eax, eax
  1DB29: mov      al, byte ptr [0x13002]
  1DB2E: push     eax
  1DB2F: mov      edx, dword ptr [0x13238]
  1DB35: push     edx
  1DB36: push     0x20
  1DB38: push     0x100
  1DB3D: push     0x100
  1DB42: push     -1
  1DB44: mov      ebx, dword ptr [0x13204]
  1DB4A: push     ebx
  1DB4B: call     0x27ce1  ; play_ambient_sound
  1DB50: xor      dl, dl
  1DB52: mov      byte ptr [0x95bf], dl
  1DB58: mov      edx, 0x19e6
  1DB5D: mov      eax, 0x15c1b
  1DB62: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1DB67: mov      eax, dword ptr [0xfac8]
  1DB6C: mov      byte ptr [eax + 0x1c1], 0
  1DB73: mov      ax, word ptr [0xfb94]
  1DB79: mov      word ptr [0xfb70], ax
  1DB7F: mov      word ptr [0xfb72], 0x1c1
  1DB88: mov      byte ptr [0xfb74], 1
  1DB8F: xor      bl, bl
  1DB91: mov      byte ptr [0xfb75], bl
  1DB97: mov      ecx, dword ptr [0xf914]
  1DB9D: mov      ebx, 1
  1DBA2: mov      edx, 6
  1DBA7: mov      eax, 0xfb70
  1DBAC: call     0x2a6b7  ; write_data_to_alfred1
  1DBB1: mov      eax, dword ptr [0xfaac]
  1DBB6: mov      edx, dword ptr [eax + 0x50]
  1DBB9: add      edx, 0x1c1
  1DBBF: mov      eax, dword ptr [0xf8f0]
  1DBC4: xor      ebx, ebx
  1DBC6: call     0x2a342  ; file_seek
  1DBCB: mov      ecx, dword ptr [0xf8f0]
  1DBD1: mov      eax, dword ptr [0xfac8]
  1DBD6: add      eax, 0x1c1
  1DBDB: mov      ebx, 1
  1DBE0: mov      edx, ebx
  1DBE2: call     0x2a6b7  ; write_data_to_alfred1
  1DBE7: pop      edx
  1DBE8: pop      ecx
  1DBE9: pop      ebx
  1DBEA: ret      
```

</details>

### PICKUP Extra 360

**Handler:** Ghidra `0x1EC30` | File `0x22E30` | Size: 219 bytes | 55 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x495BA] = 10
   2. Set flag [0x495BA] = 1
   3. Set flag [0x495BA] = 2
   4. Check flag [0x495BB] == 0
   5. Display text (ref=[0x4BA68])
   6. Update conversation state (room=9)
   7. Set flag [0x495BB] = 1
   8. Update conversation state (room=9)
   9. Update conversation state (room=9)

<details>
<summary>Raw disassembly (55 instructions)</summary>

```asm
  1EC30: push     4
  1EC35: call     0x2a218  ; __STK
  1EC3A: xor      ah, ah
  1EC3C: mov      byte ptr [0x95ba], ah
  1EC42: jmp      0x1ec68
  1EC44: push     4
  1EC49: call     0x2a218  ; __STK
  1EC4E: mov      byte ptr [0x95ba], 1
  1EC55: jmp      0x1ec68
  1EC57: push     4
  1EC5C: call     0x2a218  ; __STK
  1EC61: mov      byte ptr [0x95ba], 2
  1EC68: push     0x14
  1EC6D: call     0x2a218  ; __STK
  1EC72: push     ebx
  1EC73: push     ecx
  1EC74: push     edx
  1EC75: cmp      byte ptr [0x95bb], 0
  1EC7C: jne      0x1ed0f
  1EC82: mov      edx, dword ptr [0xba68]
  1EC88: xor      eax, eax
  1EC8A: call     0x1b1a2  ; display_text_with_character_animation
  1EC8F: mov      eax, 3
  1EC94: call     0x1badf
  1EC99: test     al, al
  1EC9B: je       0x1eccb
  1EC9D: mov      ebx, 2
  1ECA2: xor      edx, edx
  1ECA4: mov      eax, 9
  1ECA9: call     0x1b666  ; update_conversation_state
  1ECAE: mov      eax, 0xa
  1ECB3: call     0x24157
  1ECB8: mov      eax, 3
  1ECBD: call     0x1b83a
  1ECC2: mov      byte ptr [0x95bb], 1
  1ECC9: jmp      0x1ecdc
  1ECCB: mov      ebx, 1
  1ECD0: xor      edx, edx
  1ECD2: mov      eax, 9
  1ECD7: call     0x1b666  ; update_conversation_state
  1ECDC: xor      edx, edx
  1ECDE: mov      eax, 2
  1ECE3: call     0x18dce
  1ECE8: mov      eax, 0xa
  1ECED: call     0x1badf
  1ECF2: test     al, al
  1ECF4: je       0x1ed0b
  1ECF6: mov      ebx, 3
  1ECFB: xor      edx, edx
  1ECFD: mov      eax, 9
  1ED02: call     0x1b666  ; update_conversation_state
  1ED07: pop      edx
  1ED08: pop      ecx
  1ED09: pop      ebx
  1ED0A: ret      
```

</details>

### PICKUP Extra 361

**Handler:** Ghidra `0x1EC44` | File `0x22E44` | Size: 199 bytes | 50 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x495BA] = 1
   2. Set flag [0x495BA] = 2
   3. Check flag [0x495BB] == 0
   4. Display text (ref=[0x4BA68])
   5. Update conversation state (room=9)
   6. Set flag [0x495BB] = 1
   7. Update conversation state (room=9)
   8. Update conversation state (room=9)

<details>
<summary>Raw disassembly (50 instructions)</summary>

```asm
  1EC44: push     4
  1EC49: call     0x2a218  ; __STK
  1EC4E: mov      byte ptr [0x95ba], 1
  1EC55: jmp      0x1ec68
  1EC57: push     4
  1EC5C: call     0x2a218  ; __STK
  1EC61: mov      byte ptr [0x95ba], 2
  1EC68: push     0x14
  1EC6D: call     0x2a218  ; __STK
  1EC72: push     ebx
  1EC73: push     ecx
  1EC74: push     edx
  1EC75: cmp      byte ptr [0x95bb], 0
  1EC7C: jne      0x1ed0f
  1EC82: mov      edx, dword ptr [0xba68]
  1EC88: xor      eax, eax
  1EC8A: call     0x1b1a2  ; display_text_with_character_animation
  1EC8F: mov      eax, 3
  1EC94: call     0x1badf
  1EC99: test     al, al
  1EC9B: je       0x1eccb
  1EC9D: mov      ebx, 2
  1ECA2: xor      edx, edx
  1ECA4: mov      eax, 9
  1ECA9: call     0x1b666  ; update_conversation_state
  1ECAE: mov      eax, 0xa
  1ECB3: call     0x24157
  1ECB8: mov      eax, 3
  1ECBD: call     0x1b83a
  1ECC2: mov      byte ptr [0x95bb], 1
  1ECC9: jmp      0x1ecdc
  1ECCB: mov      ebx, 1
  1ECD0: xor      edx, edx
  1ECD2: mov      eax, 9
  1ECD7: call     0x1b666  ; update_conversation_state
  1ECDC: xor      edx, edx
  1ECDE: mov      eax, 2
  1ECE3: call     0x18dce
  1ECE8: mov      eax, 0xa
  1ECED: call     0x1badf
  1ECF2: test     al, al
  1ECF4: je       0x1ed0b
  1ECF6: mov      ebx, 3
  1ECFB: xor      edx, edx
  1ECFD: mov      eax, 9
  1ED02: call     0x1b666  ; update_conversation_state
  1ED07: pop      edx
  1ED08: pop      ecx
  1ED09: pop      ebx
  1ED0A: ret      
```

</details>

### PICKUP Extra 362

**Handler:** Ghidra `0x1EC57` | File `0x22E57` | Size: 180 bytes | 46 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x495BA] = 2
   2. Check flag [0x495BB] == 0
   3. Display text (ref=[0x4BA68])
   4. Update conversation state (room=9)
   5. Set flag [0x495BB] = 1
   6. Update conversation state (room=9)
   7. Update conversation state (room=9)

<details>
<summary>Raw disassembly (46 instructions)</summary>

```asm
  1EC57: push     4
  1EC5C: call     0x2a218  ; __STK
  1EC61: mov      byte ptr [0x95ba], 2
  1EC68: push     0x14
  1EC6D: call     0x2a218  ; __STK
  1EC72: push     ebx
  1EC73: push     ecx
  1EC74: push     edx
  1EC75: cmp      byte ptr [0x95bb], 0
  1EC7C: jne      0x1ed0f
  1EC82: mov      edx, dword ptr [0xba68]
  1EC88: xor      eax, eax
  1EC8A: call     0x1b1a2  ; display_text_with_character_animation
  1EC8F: mov      eax, 3
  1EC94: call     0x1badf
  1EC99: test     al, al
  1EC9B: je       0x1eccb
  1EC9D: mov      ebx, 2
  1ECA2: xor      edx, edx
  1ECA4: mov      eax, 9
  1ECA9: call     0x1b666  ; update_conversation_state
  1ECAE: mov      eax, 0xa
  1ECB3: call     0x24157
  1ECB8: mov      eax, 3
  1ECBD: call     0x1b83a
  1ECC2: mov      byte ptr [0x95bb], 1
  1ECC9: jmp      0x1ecdc
  1ECCB: mov      ebx, 1
  1ECD0: xor      edx, edx
  1ECD2: mov      eax, 9
  1ECD7: call     0x1b666  ; update_conversation_state
  1ECDC: xor      edx, edx
  1ECDE: mov      eax, 2
  1ECE3: call     0x18dce
  1ECE8: mov      eax, 0xa
  1ECED: call     0x1badf
  1ECF2: test     al, al
  1ECF4: je       0x1ed0b
  1ECF6: mov      ebx, 3
  1ECFB: xor      edx, edx
  1ECFD: mov      eax, 9
  1ED02: call     0x1b666  ; update_conversation_state
  1ED07: pop      edx
  1ED08: pop      ecx
  1ED09: pop      ebx
  1ED0A: ret      
```

</details>

---

## Room 12

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 69 | 152 | 61 | 64 | 370 | Visible |
| 1 | 0x485 | 0x00 | 363 | 235 | 29 | 41 | 371 | Visible |
| 2 | 0x48E | 0x08 | 259 | 168 | 11 | 16 | 60 | Visible |
| 3 | 0x497 | 0x08 | 287 | 168 | 11 | 16 | 61 | Visible |
| 4 | 0x4A0 | 0x08 | 273 | 168 | 11 | 16 | 62 | Visible |

### OPEN Extra 370

**Handler:** Ghidra `0x1CAD3` | File `0x20CD3` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495C0] == 0
   2. Play ambient sound
   3. Set flag [0x495C0] = 1
   4. Display sticker from ALFRED.6 offset=0x1910A, size=0x6EA
   5. Set room_data[0x1CF] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1CAD3: push     0x2c
  1CAD8: call     0x2a218  ; __STK
  1CADD: push     ebx
  1CADE: push     ecx
  1CADF: push     edx
  1CAE0: cmp      byte ptr [0x95c0], 0
  1CAE7: jne      0x1cbaf
  1CAED: xor      eax, eax
  1CAEF: mov      al, byte ptr [0x13002]
  1CAF4: push     eax
  1CAF5: mov      edx, dword ptr [0x13234]
  1CAFB: push     edx
  1CAFC: push     0x20
  1CAFE: push     0x100
  1CB03: push     0x100
  1CB08: push     -1
  1CB0A: mov      ebx, dword ptr [0x13204]
  1CB10: push     ebx
  1CB11: call     0x27ce1  ; play_ambient_sound
  1CB16: mov      byte ptr [0x95c0], 1
  1CB1D: mov      edx, 0x6ea
  1CB22: mov      eax, 0x1910a
  1CB27: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1CB2C: mov      eax, dword ptr [0xfac8]
  1CB31: mov      byte ptr [eax + 0x1cf], 1
  1CB38: mov      ax, word ptr [0xfb94]
  1CB3E: mov      word ptr [0xfb70], ax
  1CB44: mov      word ptr [0xfb72], 0x1cf
  1CB4D: mov      dh, 1
  1CB4F: mov      byte ptr [0xfb74], dh
  1CB55: mov      byte ptr [0xfb75], dh
  1CB5B: mov      ecx, dword ptr [0xf914]
  1CB61: mov      ebx, 1
  1CB66: mov      edx, 6
  1CB6B: mov      eax, 0xfb70
  1CB70: call     0x2a6b7  ; write_data_to_alfred1
  1CB75: mov      eax, dword ptr [0xfaac]
  1CB7A: mov      edx, dword ptr [eax + 0x50]
  1CB7D: add      edx, 0x1cf
  1CB83: mov      eax, dword ptr [0xf8f0]
  1CB88: xor      ebx, ebx
  1CB8A: call     0x2a342  ; file_seek
  1CB8F: mov      ecx, dword ptr [0xf8f0]
  1CB95: mov      eax, dword ptr [0xfac8]
  1CB9A: add      eax, 0x1cf
  1CB9F: mov      ebx, 1
  1CBA4: mov      edx, ebx
  1CBA6: call     0x2a6b7  ; write_data_to_alfred1
  1CBAB: pop      edx
  1CBAC: pop      ecx
  1CBAD: pop      ebx
  1CBAE: ret      
```

</details>

### PULL Extra 370

**Handler:** Ghidra `0x1DBF9` | File `0x21DF9` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495C0] == 0
   2. Play ambient sound
   3. Set flag [0x495C0] = 13
   4. Display sticker from ALFRED.6 offset=0x197F4, size=0x6EA
   5. Set room_data[0x1CF] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1DBF9: push     0x2c
  1DBFE: call     0x2a218  ; __STK
  1DC03: push     ebx
  1DC04: push     ecx
  1DC05: push     edx
  1DC06: cmp      byte ptr [0x95c0], 0
  1DC0D: je       0x1dcd7
  1DC13: xor      eax, eax
  1DC15: mov      al, byte ptr [0x13002]
  1DC1A: push     eax
  1DC1B: mov      edx, dword ptr [0x13238]
  1DC21: push     edx
  1DC22: push     0x20
  1DC24: push     0x100
  1DC29: push     0x100
  1DC2E: push     -1
  1DC30: mov      ebx, dword ptr [0x13204]
  1DC36: push     ebx
  1DC37: call     0x27ce1  ; play_ambient_sound
  1DC3C: xor      dl, dl
  1DC3E: mov      byte ptr [0x95c0], dl
  1DC44: mov      edx, 0x6ea
  1DC49: mov      eax, 0x197f4
  1DC4E: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1DC53: mov      eax, dword ptr [0xfac8]
  1DC58: mov      byte ptr [eax + 0x1cf], 0
  1DC5F: mov      ax, word ptr [0xfb94]
  1DC65: mov      word ptr [0xfb70], ax
  1DC6B: mov      word ptr [0xfb72], 0x1cf
  1DC74: mov      byte ptr [0xfb74], 1
  1DC7B: xor      bl, bl
  1DC7D: mov      byte ptr [0xfb75], bl
  1DC83: mov      ecx, dword ptr [0xf914]
  1DC89: mov      ebx, 1
  1DC8E: mov      edx, 6
  1DC93: mov      eax, 0xfb70
  1DC98: call     0x2a6b7  ; write_data_to_alfred1
  1DC9D: mov      eax, dword ptr [0xfaac]
  1DCA2: mov      edx, dword ptr [eax + 0x50]
  1DCA5: add      edx, 0x1cf
  1DCAB: mov      eax, dword ptr [0xf8f0]
  1DCB0: xor      ebx, ebx
  1DCB2: call     0x2a342  ; file_seek
  1DCB7: mov      ecx, dword ptr [0xf8f0]
  1DCBD: mov      eax, dword ptr [0xfac8]
  1DCC2: add      eax, 0x1cf
  1DCC7: mov      ebx, 1
  1DCCC: mov      edx, ebx
  1DCCE: call     0x2a6b7  ; write_data_to_alfred1
  1DCD3: pop      edx
  1DCD4: pop      ecx
  1DCD5: pop      ebx
  1DCD6: ret      
```

</details>

### PICKUP Extra 60

**Handler:** Ghidra `0x1EE31` | File `0x23031` | Size: 182 bytes | 34 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x49D10] = 1
   2. Display sticker from ALFRED.6 offset=0x494A9, size=0xB6
   3. HIDE hotspot[2] @0x48F → (640, 400)
   4. JMP → 0x1E808

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x48F | 2 | 60 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (34 instructions)</summary>

```asm
  1EE31: push     0x10
  1EE36: call     0x2a218  ; __STK
  1EE3B: push     ebx
  1EE3C: push     ecx
  1EE3D: push     edx
  1EE3E: mov      byte ptr [0x9d10], 1
  1EE45: mov      edx, 0xb6
  1EE4A: mov      eax, 0x494a9
  1EE4F: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1EE54: mov      eax, dword ptr [0xfac8]
  1EE59: mov      word ptr [eax + 0x48f], 0x280
  1EE62: mov      eax, dword ptr [0xfac8]
  1EE67: mov      word ptr [eax + 0x491], 0x190
  1EE70: mov      ax, word ptr [0xfb94]
  1EE76: mov      word ptr [0xfb78], ax
  1EE7C: mov      word ptr [0xfb7a], 0x48f
  1EE85: mov      byte ptr [0xfb7c], 4
  1EE8C: mov      word ptr [0xfb7d], 0x280
  1EE95: mov      word ptr [0xfb7f], 0x190
  1EE9E: mov      ecx, dword ptr [0xf914]
  1EEA4: mov      ebx, 1
  1EEA9: mov      edx, 9
  1EEAE: mov      eax, 0xfb78
  1EEB3: call     0x2a6b7  ; write_data_to_alfred1
  1EEB8: mov      eax, dword ptr [0xfaac]
  1EEBD: mov      edx, dword ptr [eax + 0x50]
  1EEC0: add      edx, 0x48f
  1EEC6: mov      eax, dword ptr [0xf8f0]
  1EECB: xor      ebx, ebx
  1EECD: call     0x2a342  ; file_seek
  1EED2: mov      ecx, dword ptr [0xf8f0]
  1EED8: mov      eax, dword ptr [0xfac8]
  1EEDD: add      eax, 0x48f
  1EEE2: jmp      0x1e808
```

</details>

### PICKUP Extra 61

**Handler:** Ghidra `0x1EF81` | File `0x23181` | Size: 154 bytes | 28 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x49D1E] = 1
   2. Display sticker from ALFRED.6 offset=0x49615, size=0xB6
   3. HIDE hotspot[3] @0x498 → (640, 400)
   4. JMP → 0x1E7EC

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x498 | 3 | 61 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (28 instructions)</summary>

```asm
  1EF81: push     0x10
  1EF86: call     0x2a218  ; __STK
  1EF8B: push     ebx
  1EF8C: push     ecx
  1EF8D: push     edx
  1EF8E: mov      byte ptr [0x9d1e], 1
  1EF95: mov      edx, 0xb6
  1EF9A: mov      eax, 0x49615
  1EF9F: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1EFA4: mov      eax, dword ptr [0xfac8]
  1EFA9: mov      word ptr [eax + 0x498], 0x280
  1EFB2: mov      eax, dword ptr [0xfac8]
  1EFB7: mov      word ptr [eax + 0x49a], 0x190
  1EFC0: mov      ax, word ptr [0xfb94]
  1EFC6: mov      word ptr [0xfb78], ax
  1EFCC: mov      word ptr [0xfb7a], 0x4a1
  1EFD5: mov      byte ptr [0xfb7c], 4
  1EFDC: mov      word ptr [0xfb7d], 0x280
  1EFE5: mov      word ptr [0xfb7f], 0x190
  1EFEE: mov      ecx, dword ptr [0xf914]
  1EFF4: mov      ebx, 1
  1EFF9: mov      edx, 9
  1EFFE: mov      eax, 0xfb78
  1F003: call     0x2a6b7  ; write_data_to_alfred1
  1F008: mov      eax, dword ptr [0xfaac]
  1F00D: mov      edx, dword ptr [eax + 0x50]
  1F010: add      edx, 0x4a1
  1F016: jmp      0x1e7ec
```

</details>

### PICKUP Extra 62

**Handler:** Ghidra `0x1EEE7` | File `0x230E7` | Size: 154 bytes | 28 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x49D17] = 1
   2. Display sticker from ALFRED.6 offset=0x4955F, size=0xB6
   3. HIDE hotspot[4] @0x4A1 → (640, 400)
   4. JMP → 0x1E4D9

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x4A1 | 4 | 62 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (28 instructions)</summary>

```asm
  1EEE7: push     0x10
  1EEEC: call     0x2a218  ; __STK
  1EEF1: push     ebx
  1EEF2: push     ecx
  1EEF3: push     edx
  1EEF4: mov      byte ptr [0x9d17], 1
  1EEFB: mov      edx, 0xb6
  1EF00: mov      eax, 0x4955f
  1EF05: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1EF0A: mov      eax, dword ptr [0xfac8]
  1EF0F: mov      word ptr [eax + 0x4a1], 0x280
  1EF18: mov      eax, dword ptr [0xfac8]
  1EF1D: mov      word ptr [eax + 0x4a3], 0x190
  1EF26: mov      ax, word ptr [0xfb94]
  1EF2C: mov      word ptr [0xfb78], ax
  1EF32: mov      word ptr [0xfb7a], 0x498
  1EF3B: mov      byte ptr [0xfb7c], 4
  1EF42: mov      word ptr [0xfb7d], 0x280
  1EF4B: mov      word ptr [0xfb7f], 0x190
  1EF54: mov      ecx, dword ptr [0xf914]
  1EF5A: mov      ebx, 1
  1EF5F: mov      edx, 9
  1EF64: mov      eax, 0xfb78
  1EF69: call     0x2a6b7  ; write_data_to_alfred1
  1EF6E: mov      eax, dword ptr [0xfaac]
  1EF73: mov      edx, dword ptr [eax + 0x50]
  1EF76: add      edx, 0x498
  1EF7C: jmp      0x1e4d9
```

</details>

---

## Room 13

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 487 | 151 | 67 | 68 | 374 | Visible |
| 1 | 0x485 | 0x01 | 339 | 197 | 65 | 19 | 375 | Visible |
| 2 | 0x48E | 0x00 | 339 | 219 | 65 | 21 | 376 | Visible |

### OPEN Extra 374

**Handler:** Ghidra `0x1CBBD` | File `0x20DBD` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495C1] == 0
   2. Play ambient sound
   3. Set flag [0x495C1] = 1
   4. Display sticker from ALFRED.6 offset=0x19EDE, size=0x90E
   5. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1CBBD: push     0x2c
  1CBC2: call     0x2a218  ; __STK
  1CBC7: push     ebx
  1CBC8: push     ecx
  1CBC9: push     edx
  1CBCA: cmp      byte ptr [0x95c1], 0
  1CBD1: jne      0x1cc99
  1CBD7: xor      eax, eax
  1CBD9: mov      al, byte ptr [0x13002]
  1CBDE: push     eax
  1CBDF: mov      edx, dword ptr [0x13234]
  1CBE5: push     edx
  1CBE6: push     0x20
  1CBE8: push     0x100
  1CBED: push     0x100
  1CBF2: push     -1
  1CBF4: mov      ebx, dword ptr [0x13204]
  1CBFA: push     ebx
  1CBFB: call     0x27ce1  ; play_ambient_sound
  1CC00: mov      byte ptr [0x95c1], 1
  1CC07: mov      edx, 0x90e
  1CC0C: mov      eax, 0x19ede
  1CC11: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1CC16: mov      eax, dword ptr [0xfac8]
  1CC1B: mov      byte ptr [eax + 0x1c1], 1
  1CC22: mov      ax, word ptr [0xfb94]
  1CC28: mov      word ptr [0xfb70], ax
  1CC2E: mov      word ptr [0xfb72], 0x1c1
  1CC37: mov      dh, 1
  1CC39: mov      byte ptr [0xfb74], dh
  1CC3F: mov      byte ptr [0xfb75], dh
  1CC45: mov      ecx, dword ptr [0xf914]
  1CC4B: mov      ebx, 1
  1CC50: mov      edx, 6
  1CC55: mov      eax, 0xfb70
  1CC5A: call     0x2a6b7  ; write_data_to_alfred1
  1CC5F: mov      eax, dword ptr [0xfaac]
  1CC64: mov      edx, dword ptr [eax + 0x50]
  1CC67: add      edx, 0x1c1
  1CC6D: mov      eax, dword ptr [0xf8f0]
  1CC72: xor      ebx, ebx
  1CC74: call     0x2a342  ; file_seek
  1CC79: mov      ecx, dword ptr [0xf8f0]
  1CC7F: mov      eax, dword ptr [0xfac8]
  1CC84: add      eax, 0x1c1
  1CC89: mov      ebx, 1
  1CC8E: mov      edx, ebx
  1CC90: call     0x2a6b7  ; write_data_to_alfred1
  1CC95: pop      edx
  1CC96: pop      ecx
  1CC97: pop      ebx
  1CC98: ret      
```

</details>

### OPEN Extra 375

**Handler:** Ghidra `0x1CCA7` | File `0x20EA7` | Size: 35 bytes | 10 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495C2] == 0
   2. Display text (ref=[0x4BA84])

<details>
<summary>Raw disassembly (10 instructions)</summary>

```asm
  1CCA7: push     8
  1CCAC: call     0x2a218  ; __STK
  1CCB1: push     edx
  1CCB2: cmp      byte ptr [0x95c2], 0
  1CCB9: jne      0x1ccca
  1CCBB: mov      edx, dword ptr [0xba84]
  1CCC1: xor      eax, eax
  1CCC3: call     0x1b1a2  ; display_text_with_character_animation
  1CCC8: pop      edx
  1CCC9: ret      
```

</details>

### PULL Extra 374

**Handler:** Ghidra `0x1DCE5` | File `0x21EE5` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495C1] == 0
   2. Play ambient sound
   3. Set flag [0x495C1] = 13
   4. Display sticker from ALFRED.6 offset=0x1A7EC, size=0x90E
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1DCE5: push     0x2c
  1DCEA: call     0x2a218  ; __STK
  1DCEF: push     ebx
  1DCF0: push     ecx
  1DCF1: push     edx
  1DCF2: cmp      byte ptr [0x95c1], 0
  1DCF9: je       0x1ddc3
  1DCFF: xor      eax, eax
  1DD01: mov      al, byte ptr [0x13002]
  1DD06: push     eax
  1DD07: mov      edx, dword ptr [0x13238]
  1DD0D: push     edx
  1DD0E: push     0x20
  1DD10: push     0x100
  1DD15: push     0x100
  1DD1A: push     -1
  1DD1C: mov      ebx, dword ptr [0x13204]
  1DD22: push     ebx
  1DD23: call     0x27ce1  ; play_ambient_sound
  1DD28: xor      dl, dl
  1DD2A: mov      byte ptr [0x95c1], dl
  1DD30: mov      edx, 0x90e
  1DD35: mov      eax, 0x1a7ec
  1DD3A: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1DD3F: mov      eax, dword ptr [0xfac8]
  1DD44: mov      byte ptr [eax + 0x1c1], 0
  1DD4B: mov      ax, word ptr [0xfb94]
  1DD51: mov      word ptr [0xfb70], ax
  1DD57: mov      word ptr [0xfb72], 0x1c1
  1DD60: mov      byte ptr [0xfb74], 1
  1DD67: xor      bl, bl
  1DD69: mov      byte ptr [0xfb75], bl
  1DD6F: mov      ecx, dword ptr [0xf914]
  1DD75: mov      ebx, 1
  1DD7A: mov      edx, 6
  1DD7F: mov      eax, 0xfb70
  1DD84: call     0x2a6b7  ; write_data_to_alfred1
  1DD89: mov      eax, dword ptr [0xfaac]
  1DD8E: mov      edx, dword ptr [eax + 0x50]
  1DD91: add      edx, 0x1c1
  1DD97: mov      eax, dword ptr [0xf8f0]
  1DD9C: xor      ebx, ebx
  1DD9E: call     0x2a342  ; file_seek
  1DDA3: mov      ecx, dword ptr [0xf8f0]
  1DDA9: mov      eax, dword ptr [0xfac8]
  1DDAE: add      eax, 0x1c1
  1DDB3: mov      ebx, 1
  1DDB8: mov      edx, ebx
  1DDBA: call     0x2a6b7  ; write_data_to_alfred1
  1DDBF: pop      edx
  1DDC0: pop      ecx
  1DDC1: pop      ebx
  1DDC2: ret      
```

</details>

---

## Room 15

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x08 | 414 | 82 | 112 | 41 | 65 | Visible |
| 1 | 0x485 | 0x08 | 528 | 80 | 44 | 51 | 66 | Visible |
| 2 | 0x48E | 0x08 | 385 | 126 | 55 | 36 | 67 | Visible |
| 3 | 0x497 | 0x08 | 461 | 132 | 63 | 47 | 68 | Visible |
| 4 | 0x4A0 | 0x08 | 525 | 153 | 47 | 40 | 69 | Visible |
| 5 | 0x4A9 | 0x08 | 381 | 166 | 49 | 28 | 70 | Visible |
| 6 | 0x4B2 | 0x08 | 431 | 178 | 37 | 28 | 71 | Visible |
| 7 | 0x4BB | 0x08 | 467 | 186 | 43 | 32 | 72 | Visible |
| 8 | 0x4C4 | 0x08 | 393 | 207 | 40 | 24 | 73 | Visible |
| 9 | 0x4CD | 0x08 | 456 | 234 | 27 | 22 | 74 | Visible |
| 10 | 0x4D6 | 0x08 | 396 | 241 | 51 | 31 | 6 | Visible |
| 11 | 0x4DF | 0x08 | 448 | 261 | 55 | 30 | 7 | Visible |
| 12 | 0x4E8 | 0x00 | 442 | 132 | 17 | 37 | 382 | Visible |
| 13 | 0x4F1 | 0x00 | 434 | 214 | 21 | 26 | 383 | Visible |
| 14 | 0x4FA | 0x00 | 484 | 231 | 24 | 28 | 384 | Visible |
| 15 | 0x503 | 0x80 | 375 | 295 | 38 | 63 | 385 | Visible |

### PICKUP Extra 6

**Handler:** Ghidra `0x1FA41` | File `0x23C41` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EFA] = 1
   2. Display sticker from ALFRED.6 offset=0x210B3, size=0x633

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1FA41: push     0x10
  1FA46: call     0x2a218  ; __STK
  1FA4B: push     ebx
  1FA4C: push     ecx
  1FA4D: push     edx
  1FA4E: mov      eax, 5
  1FA53: call     0x1badf
  1FA58: test     al, al
  1FA5A: je       0x1fb1f
  1FA60: mov      byte ptr [0x9efa], 1
  1FA67: mov      edx, 0x633
  1FA6C: mov      eax, 0x210b3
  1FA71: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1FA76: mov      edx, dword ptr [0xfac8]
  1FA7C: mov      word ptr [edx + 0x4d7], 0x280
  1FA85: mov      edx, dword ptr [0xfac8]
  1FA8B: mov      word ptr [edx + 0x4d9], 0x190
  1FA94: mov      ax, word ptr [0xfb94]
  1FA9A: mov      word ptr [0xfb78], ax
  1FAA0: mov      word ptr [0xfb7a], 0x4d7
  1FAA9: mov      byte ptr [0xfb7c], 4
  1FAB0: mov      word ptr [0xfb7d], 0x280
  1FAB9: mov      word ptr [0xfb7f], 0x190
  1FAC2: mov      ecx, dword ptr [0xf914]
  1FAC8: mov      ebx, 1
  1FACD: mov      edx, 9
  1FAD2: mov      eax, 0xfb78
  1FAD7: call     0x2a6b7  ; write_data_to_alfred1
  1FADC: mov      edx, dword ptr [0xfaac]
  1FAE2: mov      edx, dword ptr [edx + 0x50]
  1FAE5: add      edx, 0x4d7
  1FAEB: mov      eax, dword ptr [0xf8f0]
  1FAF0: xor      ebx, ebx
  1FAF2: call     0x2a342  ; file_seek
  1FAF7: mov      ecx, dword ptr [0xf8f0]
  1FAFD: mov      eax, dword ptr [0xfac8]
  1FB02: add      eax, 0x4d7
  1FB07: mov      ebx, 1
  1FB0C: mov      edx, 4
  1FB11: call     0x2a6b7  ; write_data_to_alfred1
  1FB16: call     0x20722
  1FB1B: pop      edx
  1FB1C: pop      ecx
  1FB1D: pop      ebx
  1FB1E: ret      
```

</details>

### PICKUP Extra 7

**Handler:** Ghidra `0x1FB37` | File `0x23D37` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49F01] = 1
   2. Display sticker from ALFRED.6 offset=0x216E6, size=0x678

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1FB37: push     0x10
  1FB3C: call     0x2a218  ; __STK
  1FB41: push     ebx
  1FB42: push     ecx
  1FB43: push     edx
  1FB44: mov      eax, 5
  1FB49: call     0x1badf
  1FB4E: test     al, al
  1FB50: je       0x1fc15
  1FB56: mov      byte ptr [0x9f01], 1
  1FB5D: mov      edx, 0x678
  1FB62: mov      eax, 0x216e6
  1FB67: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1FB6C: mov      edx, dword ptr [0xfac8]
  1FB72: mov      word ptr [edx + 0x4e0], 0x280
  1FB7B: mov      edx, dword ptr [0xfac8]
  1FB81: mov      word ptr [edx + 0x4e2], 0x190
  1FB8A: mov      ax, word ptr [0xfb94]
  1FB90: mov      word ptr [0xfb78], ax
  1FB96: mov      word ptr [0xfb7a], 0x4e0
  1FB9F: mov      byte ptr [0xfb7c], 4
  1FBA6: mov      word ptr [0xfb7d], 0x280
  1FBAF: mov      word ptr [0xfb7f], 0x190
  1FBB8: mov      ecx, dword ptr [0xf914]
  1FBBE: mov      ebx, 1
  1FBC3: mov      edx, 9
  1FBC8: mov      eax, 0xfb78
  1FBCD: call     0x2a6b7  ; write_data_to_alfred1
  1FBD2: mov      edx, dword ptr [0xfaac]
  1FBD8: mov      edx, dword ptr [edx + 0x50]
  1FBDB: add      edx, 0x4e0
  1FBE1: mov      eax, dword ptr [0xf8f0]
  1FBE6: xor      ebx, ebx
  1FBE8: call     0x2a342  ; file_seek
  1FBED: mov      ecx, dword ptr [0xf8f0]
  1FBF3: mov      eax, dword ptr [0xfac8]
  1FBF8: add      eax, 0x4e0
  1FBFD: mov      ebx, 1
  1FC02: mov      edx, 4
  1FC07: call     0x2a6b7  ; write_data_to_alfred1
  1FC0C: call     0x20722
  1FC11: pop      edx
  1FC12: pop      ecx
  1FC13: pop      ebx
  1FC14: ret      
```

</details>

### PICKUP Extra 65

**Handler:** Ghidra `0x1F01B` | File `0x2321B` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EB4] = 1
   2. Display sticker from ALFRED.6 offset=0x1C644, size=0x11F6

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F01B: push     0x10
  1F020: call     0x2a218  ; __STK
  1F025: push     ebx
  1F026: push     ecx
  1F027: push     edx
  1F028: mov      eax, 5
  1F02D: call     0x1badf
  1F032: test     al, al
  1F034: je       0x1f0f9
  1F03A: mov      byte ptr [0x9eb4], 1
  1F041: mov      edx, 0x11f6
  1F046: mov      eax, 0x1c644
  1F04B: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F050: mov      edx, dword ptr [0xfac8]
  1F056: mov      word ptr [edx + 0x47d], 0x280
  1F05F: mov      edx, dword ptr [0xfac8]
  1F065: mov      word ptr [edx + 0x47f], 0x190
  1F06E: mov      ax, word ptr [0xfb94]
  1F074: mov      word ptr [0xfb78], ax
  1F07A: mov      word ptr [0xfb7a], 0x47d
  1F083: mov      byte ptr [0xfb7c], 4
  1F08A: mov      word ptr [0xfb7d], 0x280
  1F093: mov      word ptr [0xfb7f], 0x190
  1F09C: mov      ecx, dword ptr [0xf914]
  1F0A2: mov      ebx, 1
  1F0A7: mov      edx, 9
  1F0AC: mov      eax, 0xfb78
  1F0B1: call     0x2a6b7  ; write_data_to_alfred1
  1F0B6: mov      edx, dword ptr [0xfaac]
  1F0BC: mov      edx, dword ptr [edx + 0x50]
  1F0BF: add      edx, 0x47d
  1F0C5: mov      eax, dword ptr [0xf8f0]
  1F0CA: xor      ebx, ebx
  1F0CC: call     0x2a342  ; file_seek
  1F0D1: mov      ecx, dword ptr [0xf8f0]
  1F0D7: mov      eax, dword ptr [0xfac8]
  1F0DC: add      eax, 0x47d
  1F0E1: mov      ebx, 1
  1F0E6: mov      edx, 4
  1F0EB: call     0x2a6b7  ; write_data_to_alfred1
  1F0F0: call     0x20722
  1F0F5: pop      edx
  1F0F6: pop      ecx
  1F0F7: pop      ebx
  1F0F8: ret      
```

</details>

### PICKUP Extra 66

**Handler:** Ghidra `0x1F111` | File `0x23311` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EBB] = 1
   2. Display sticker from ALFRED.6 offset=0x1D83A, size=0x8CA

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F111: push     0x10
  1F116: call     0x2a218  ; __STK
  1F11B: push     ebx
  1F11C: push     ecx
  1F11D: push     edx
  1F11E: mov      eax, 5
  1F123: call     0x1badf
  1F128: test     al, al
  1F12A: je       0x1f1ef
  1F130: mov      byte ptr [0x9ebb], 1
  1F137: mov      edx, 0x8ca
  1F13C: mov      eax, 0x1d83a
  1F141: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F146: mov      edx, dword ptr [0xfac8]
  1F14C: mov      word ptr [edx + 0x486], 0x280
  1F155: mov      edx, dword ptr [0xfac8]
  1F15B: mov      word ptr [edx + 0x488], 0x190
  1F164: mov      ax, word ptr [0xfb94]
  1F16A: mov      word ptr [0xfb78], ax
  1F170: mov      word ptr [0xfb7a], 0x486
  1F179: mov      byte ptr [0xfb7c], 4
  1F180: mov      word ptr [0xfb7d], 0x280
  1F189: mov      word ptr [0xfb7f], 0x190
  1F192: mov      ecx, dword ptr [0xf914]
  1F198: mov      ebx, 1
  1F19D: mov      edx, 9
  1F1A2: mov      eax, 0xfb78
  1F1A7: call     0x2a6b7  ; write_data_to_alfred1
  1F1AC: mov      edx, dword ptr [0xfaac]
  1F1B2: mov      edx, dword ptr [edx + 0x50]
  1F1B5: add      edx, 0x486
  1F1BB: mov      eax, dword ptr [0xf8f0]
  1F1C0: xor      ebx, ebx
  1F1C2: call     0x2a342  ; file_seek
  1F1C7: mov      ecx, dword ptr [0xf8f0]
  1F1CD: mov      eax, dword ptr [0xfac8]
  1F1D2: add      eax, 0x486
  1F1D7: mov      ebx, 1
  1F1DC: mov      edx, 4
  1F1E1: call     0x2a6b7  ; write_data_to_alfred1
  1F1E6: call     0x20722
  1F1EB: pop      edx
  1F1EC: pop      ecx
  1F1ED: pop      ebx
  1F1EE: ret      
```

</details>

### PICKUP Extra 67

**Handler:** Ghidra `0x1F207` | File `0x23407` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EC2] = 1
   2. Display sticker from ALFRED.6 offset=0x1E104, size=0x7C2

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F207: push     0x10
  1F20C: call     0x2a218  ; __STK
  1F211: push     ebx
  1F212: push     ecx
  1F213: push     edx
  1F214: mov      eax, 5
  1F219: call     0x1badf
  1F21E: test     al, al
  1F220: je       0x1f2e5
  1F226: mov      byte ptr [0x9ec2], 1
  1F22D: mov      edx, 0x7c2
  1F232: mov      eax, 0x1e104
  1F237: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F23C: mov      edx, dword ptr [0xfac8]
  1F242: mov      word ptr [edx + 0x48f], 0x280
  1F24B: mov      edx, dword ptr [0xfac8]
  1F251: mov      word ptr [edx + 0x491], 0x190
  1F25A: mov      ax, word ptr [0xfb94]
  1F260: mov      word ptr [0xfb78], ax
  1F266: mov      word ptr [0xfb7a], 0x48f
  1F26F: mov      byte ptr [0xfb7c], 4
  1F276: mov      word ptr [0xfb7d], 0x280
  1F27F: mov      word ptr [0xfb7f], 0x190
  1F288: mov      ecx, dword ptr [0xf914]
  1F28E: mov      ebx, 1
  1F293: mov      edx, 9
  1F298: mov      eax, 0xfb78
  1F29D: call     0x2a6b7  ; write_data_to_alfred1
  1F2A2: mov      edx, dword ptr [0xfaac]
  1F2A8: mov      edx, dword ptr [edx + 0x50]
  1F2AB: add      edx, 0x48f
  1F2B1: mov      eax, dword ptr [0xf8f0]
  1F2B6: xor      ebx, ebx
  1F2B8: call     0x2a342  ; file_seek
  1F2BD: mov      ecx, dword ptr [0xf8f0]
  1F2C3: mov      eax, dword ptr [0xfac8]
  1F2C8: add      eax, 0x48f
  1F2CD: mov      ebx, 1
  1F2D2: mov      edx, 4
  1F2D7: call     0x2a6b7  ; write_data_to_alfred1
  1F2DC: call     0x20722
  1F2E1: pop      edx
  1F2E2: pop      ecx
  1F2E3: pop      ebx
  1F2E4: ret      
```

</details>

### PICKUP Extra 68

**Handler:** Ghidra `0x1F2FD` | File `0x234FD` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EC9] = 1
   2. Display sticker from ALFRED.6 offset=0x1E8C6, size=0xB97

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F2FD: push     0x10
  1F302: call     0x2a218  ; __STK
  1F307: push     ebx
  1F308: push     ecx
  1F309: push     edx
  1F30A: mov      eax, 5
  1F30F: call     0x1badf
  1F314: test     al, al
  1F316: je       0x1f3db
  1F31C: mov      byte ptr [0x9ec9], 1
  1F323: mov      edx, 0xb97
  1F328: mov      eax, 0x1e8c6
  1F32D: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F332: mov      edx, dword ptr [0xfac8]
  1F338: mov      word ptr [edx + 0x498], 0x280
  1F341: mov      edx, dword ptr [0xfac8]
  1F347: mov      word ptr [edx + 0x49a], 0x190
  1F350: mov      ax, word ptr [0xfb94]
  1F356: mov      word ptr [0xfb78], ax
  1F35C: mov      word ptr [0xfb7a], 0x498
  1F365: mov      byte ptr [0xfb7c], 4
  1F36C: mov      word ptr [0xfb7d], 0x280
  1F375: mov      word ptr [0xfb7f], 0x190
  1F37E: mov      ecx, dword ptr [0xf914]
  1F384: mov      ebx, 1
  1F389: mov      edx, 9
  1F38E: mov      eax, 0xfb78
  1F393: call     0x2a6b7  ; write_data_to_alfred1
  1F398: mov      edx, dword ptr [0xfaac]
  1F39E: mov      edx, dword ptr [edx + 0x50]
  1F3A1: add      edx, 0x498
  1F3A7: mov      eax, dword ptr [0xf8f0]
  1F3AC: xor      ebx, ebx
  1F3AE: call     0x2a342  ; file_seek
  1F3B3: mov      ecx, dword ptr [0xf8f0]
  1F3B9: mov      eax, dword ptr [0xfac8]
  1F3BE: add      eax, 0x498
  1F3C3: mov      ebx, 1
  1F3C8: mov      edx, 4
  1F3CD: call     0x2a6b7  ; write_data_to_alfred1
  1F3D2: call     0x20722
  1F3D7: pop      edx
  1F3D8: pop      ecx
  1F3D9: pop      ebx
  1F3DA: ret      
```

</details>

### PICKUP Extra 69

**Handler:** Ghidra `0x1F3F3` | File `0x235F3` | Size: 360 bytes | 72 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49ED0] = 1
   2. Display sticker from ALFRED.6 offset=0x1F45D, size=0x75E
   3. HIDE hotspot[4] @0x4A1 → (640, 400)
   4. Set room_data[0xFD] = 255

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x4A1 | 4 | 69 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (72 instructions)</summary>

```asm
  1F3F3: push     0x10
  1F3F8: call     0x2a218  ; __STK
  1F3FD: push     ebx
  1F3FE: push     ecx
  1F3FF: push     edx
  1F400: mov      eax, 5
  1F405: call     0x1badf
  1F40A: test     al, al
  1F40C: je       0x1f55b
  1F412: mov      byte ptr [0x9ed0], 1
  1F419: mov      edx, 0x75e
  1F41E: mov      eax, 0x1f45d
  1F423: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F428: mov      eax, dword ptr [0xfac8]
  1F42D: mov      word ptr [eax + 0x4a1], 0x280
  1F436: mov      eax, dword ptr [0xfac8]
  1F43B: mov      word ptr [eax + 0x4a3], 0x190
  1F444: mov      ax, word ptr [0xfb94]
  1F44A: mov      word ptr [0xfb78], ax
  1F450: mov      word ptr [0xfb7a], 0x4a1
  1F459: mov      byte ptr [0xfb7c], 4
  1F460: mov      word ptr [0xfb7d], 0x280
  1F469: mov      word ptr [0xfb7f], 0x190
  1F472: mov      ecx, dword ptr [0xf914]
  1F478: mov      ebx, 1
  1F47D: mov      edx, 9
  1F482: mov      eax, 0xfb78
  1F487: call     0x2a6b7  ; write_data_to_alfred1
  1F48C: mov      edx, dword ptr [0xfaac]
  1F492: mov      edx, dword ptr [edx + 0x50]
  1F495: add      edx, 0x4a1
  1F49B: mov      eax, dword ptr [0xf8f0]
  1F4A0: xor      ebx, ebx
  1F4A2: call     0x2a342  ; file_seek
  1F4A7: mov      ecx, dword ptr [0xf8f0]
  1F4AD: mov      eax, dword ptr [0xfac8]
  1F4B2: add      eax, 0x4a1
  1F4B7: mov      ebx, 1
  1F4BC: mov      edx, 4
  1F4C1: call     0x2a6b7  ; write_data_to_alfred1
  1F4C6: mov      eax, dword ptr [0xfac8]
  1F4CB: mov      byte ptr [eax + 0xfd], 0xff
  1F4D2: call     0x147c9
  1F4D7: xor      eax, eax
  1F4D9: call     0x15e4c
  1F4DE: mov      ax, word ptr [0xfb94]
  1F4E4: mov      word ptr [0xfb70], ax
  1F4EA: mov      word ptr [0xfb72], 0xfd
  1F4F3: mov      byte ptr [0xfb74], 1
  1F4FA: mov      byte ptr [0xfb75], 0xff
  1F501: mov      ecx, dword ptr [0xf914]
  1F507: mov      ebx, 1
  1F50C: mov      edx, 6
  1F511: mov      eax, 0xfb70
  1F516: call     0x2a6b7  ; write_data_to_alfred1
  1F51B: mov      edx, dword ptr [0xfaac]
  1F521: mov      edx, dword ptr [edx + 0x50]
  1F524: add      edx, 0xfd
  1F52A: mov      eax, dword ptr [0xf8f0]
  1F52F: xor      ebx, ebx
  1F531: call     0x2a342  ; file_seek
  1F536: mov      ecx, dword ptr [0xf8f0]
  1F53C: mov      eax, dword ptr [0xfac8]
  1F541: add      eax, 0xfd
  1F546: mov      ebx, 1
  1F54B: mov      edx, ebx
  1F54D: call     0x2a6b7  ; write_data_to_alfred1
  1F552: call     0x20722
  1F557: pop      edx
  1F558: pop      ecx
  1F559: pop      ebx
  1F55A: ret      
```

</details>

### PICKUP Extra 70

**Handler:** Ghidra `0x1F573` | File `0x23773` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49ED7] = 1
   2. Display sticker from ALFRED.6 offset=0x1FBBB, size=0x562

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F573: push     0x10
  1F578: call     0x2a218  ; __STK
  1F57D: push     ebx
  1F57E: push     ecx
  1F57F: push     edx
  1F580: mov      eax, 5
  1F585: call     0x1badf
  1F58A: test     al, al
  1F58C: je       0x1f651
  1F592: mov      byte ptr [0x9ed7], 1
  1F599: mov      edx, 0x562
  1F59E: mov      eax, 0x1fbbb
  1F5A3: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F5A8: mov      edx, dword ptr [0xfac8]
  1F5AE: mov      word ptr [edx + 0x4aa], 0x280
  1F5B7: mov      edx, dword ptr [0xfac8]
  1F5BD: mov      word ptr [edx + 0x4ac], 0x190
  1F5C6: mov      ax, word ptr [0xfb94]
  1F5CC: mov      word ptr [0xfb78], ax
  1F5D2: mov      word ptr [0xfb7a], 0x4aa
  1F5DB: mov      byte ptr [0xfb7c], 4
  1F5E2: mov      word ptr [0xfb7d], 0x280
  1F5EB: mov      word ptr [0xfb7f], 0x190
  1F5F4: mov      ecx, dword ptr [0xf914]
  1F5FA: mov      ebx, 1
  1F5FF: mov      edx, 9
  1F604: mov      eax, 0xfb78
  1F609: call     0x2a6b7  ; write_data_to_alfred1
  1F60E: mov      edx, dword ptr [0xfaac]
  1F614: mov      edx, dword ptr [edx + 0x50]
  1F617: add      edx, 0x4aa
  1F61D: mov      eax, dword ptr [0xf8f0]
  1F622: xor      ebx, ebx
  1F624: call     0x2a342  ; file_seek
  1F629: mov      ecx, dword ptr [0xf8f0]
  1F62F: mov      eax, dword ptr [0xfac8]
  1F634: add      eax, 0x4aa
  1F639: mov      ebx, 1
  1F63E: mov      edx, 4
  1F643: call     0x2a6b7  ; write_data_to_alfred1
  1F648: call     0x20722
  1F64D: pop      edx
  1F64E: pop      ecx
  1F64F: pop      ebx
  1F650: ret      
```

</details>

### PICKUP Extra 71

**Handler:** Ghidra `0x1F669` | File `0x23869` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EDE] = 1
   2. Display sticker from ALFRED.6 offset=0x2011D, size=0x412

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F669: push     0x10
  1F66E: call     0x2a218  ; __STK
  1F673: push     ebx
  1F674: push     ecx
  1F675: push     edx
  1F676: mov      eax, 5
  1F67B: call     0x1badf
  1F680: test     al, al
  1F682: je       0x1f747
  1F688: mov      byte ptr [0x9ede], 1
  1F68F: mov      edx, 0x412
  1F694: mov      eax, 0x2011d
  1F699: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F69E: mov      edx, dword ptr [0xfac8]
  1F6A4: mov      word ptr [edx + 0x4b3], 0x280
  1F6AD: mov      edx, dword ptr [0xfac8]
  1F6B3: mov      word ptr [edx + 0x4b5], 0x190
  1F6BC: mov      ax, word ptr [0xfb94]
  1F6C2: mov      word ptr [0xfb78], ax
  1F6C8: mov      word ptr [0xfb7a], 0x4b3
  1F6D1: mov      byte ptr [0xfb7c], 4
  1F6D8: mov      word ptr [0xfb7d], 0x280
  1F6E1: mov      word ptr [0xfb7f], 0x190
  1F6EA: mov      ecx, dword ptr [0xf914]
  1F6F0: mov      ebx, 1
  1F6F5: mov      edx, 9
  1F6FA: mov      eax, 0xfb78
  1F6FF: call     0x2a6b7  ; write_data_to_alfred1
  1F704: mov      edx, dword ptr [0xfaac]
  1F70A: mov      edx, dword ptr [edx + 0x50]
  1F70D: add      edx, 0x4b3
  1F713: mov      eax, dword ptr [0xf8f0]
  1F718: xor      ebx, ebx
  1F71A: call     0x2a342  ; file_seek
  1F71F: mov      ecx, dword ptr [0xf8f0]
  1F725: mov      eax, dword ptr [0xfac8]
  1F72A: add      eax, 0x4b3
  1F72F: mov      ebx, 1
  1F734: mov      edx, 4
  1F739: call     0x2a6b7  ; write_data_to_alfred1
  1F73E: call     0x20722
  1F743: pop      edx
  1F744: pop      ecx
  1F745: pop      ebx
  1F746: ret      
```

</details>

### PICKUP Extra 72

**Handler:** Ghidra `0x1F75F` | File `0x2395F` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EE5] = 1
   2. Display sticker from ALFRED.6 offset=0x2052F, size=0x566

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F75F: push     0x10
  1F764: call     0x2a218  ; __STK
  1F769: push     ebx
  1F76A: push     ecx
  1F76B: push     edx
  1F76C: mov      eax, 5
  1F771: call     0x1badf
  1F776: test     al, al
  1F778: je       0x1f83d
  1F77E: mov      byte ptr [0x9ee5], 1
  1F785: mov      edx, 0x566
  1F78A: mov      eax, 0x2052f
  1F78F: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F794: mov      edx, dword ptr [0xfac8]
  1F79A: mov      word ptr [edx + 0x4bc], 0x280
  1F7A3: mov      edx, dword ptr [0xfac8]
  1F7A9: mov      word ptr [edx + 0x4be], 0x190
  1F7B2: mov      ax, word ptr [0xfb94]
  1F7B8: mov      word ptr [0xfb78], ax
  1F7BE: mov      word ptr [0xfb7a], 0x4bc
  1F7C7: mov      byte ptr [0xfb7c], 4
  1F7CE: mov      word ptr [0xfb7d], 0x280
  1F7D7: mov      word ptr [0xfb7f], 0x190
  1F7E0: mov      ecx, dword ptr [0xf914]
  1F7E6: mov      ebx, 1
  1F7EB: mov      edx, 9
  1F7F0: mov      eax, 0xfb78
  1F7F5: call     0x2a6b7  ; write_data_to_alfred1
  1F7FA: mov      edx, dword ptr [0xfaac]
  1F800: mov      edx, dword ptr [edx + 0x50]
  1F803: add      edx, 0x4bc
  1F809: mov      eax, dword ptr [0xf8f0]
  1F80E: xor      ebx, ebx
  1F810: call     0x2a342  ; file_seek
  1F815: mov      ecx, dword ptr [0xf8f0]
  1F81B: mov      eax, dword ptr [0xfac8]
  1F820: add      eax, 0x4bc
  1F825: mov      ebx, 1
  1F82A: mov      edx, 4
  1F82F: call     0x2a6b7  ; write_data_to_alfred1
  1F834: call     0x20722
  1F839: pop      edx
  1F83A: pop      ecx
  1F83B: pop      ebx
  1F83C: ret      
```

</details>

### PICKUP Extra 73

**Handler:** Ghidra `0x1F855` | File `0x23A55` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EEC] = 1
   2. Display sticker from ALFRED.6 offset=0x20A95, size=0x3C6

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F855: push     0x10
  1F85A: call     0x2a218  ; __STK
  1F85F: push     ebx
  1F860: push     ecx
  1F861: push     edx
  1F862: mov      eax, 5
  1F867: call     0x1badf
  1F86C: test     al, al
  1F86E: je       0x1f933
  1F874: mov      byte ptr [0x9eec], 1
  1F87B: mov      edx, 0x3c6
  1F880: mov      eax, 0x20a95
  1F885: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F88A: mov      edx, dword ptr [0xfac8]
  1F890: mov      word ptr [edx + 0x4c5], 0x280
  1F899: mov      edx, dword ptr [0xfac8]
  1F89F: mov      word ptr [edx + 0x4c7], 0x190
  1F8A8: mov      ax, word ptr [0xfb94]
  1F8AE: mov      word ptr [0xfb78], ax
  1F8B4: mov      word ptr [0xfb7a], 0x4c5
  1F8BD: mov      byte ptr [0xfb7c], 4
  1F8C4: mov      word ptr [0xfb7d], 0x280
  1F8CD: mov      word ptr [0xfb7f], 0x190
  1F8D6: mov      ecx, dword ptr [0xf914]
  1F8DC: mov      ebx, 1
  1F8E1: mov      edx, 9
  1F8E6: mov      eax, 0xfb78
  1F8EB: call     0x2a6b7  ; write_data_to_alfred1
  1F8F0: mov      edx, dword ptr [0xfaac]
  1F8F6: mov      edx, dword ptr [edx + 0x50]
  1F8F9: add      edx, 0x4c5
  1F8FF: mov      eax, dword ptr [0xf8f0]
  1F904: xor      ebx, ebx
  1F906: call     0x2a342  ; file_seek
  1F90B: mov      ecx, dword ptr [0xf8f0]
  1F911: mov      eax, dword ptr [0xfac8]
  1F916: add      eax, 0x4c5
  1F91B: mov      ebx, 1
  1F920: mov      edx, 4
  1F925: call     0x2a6b7  ; write_data_to_alfred1
  1F92A: call     0x20722
  1F92F: pop      edx
  1F930: pop      ecx
  1F931: pop      ebx
  1F932: ret      
```

</details>

### PICKUP Extra 74

**Handler:** Ghidra `0x1F94B` | File `0x23B4B` | Size: 222 bytes | 45 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x49EF3] = 1
   2. Display sticker from ALFRED.6 offset=0x20E5B, size=0x258

<details>
<summary>Raw disassembly (45 instructions)</summary>

```asm
  1F94B: push     0x10
  1F950: call     0x2a218  ; __STK
  1F955: push     ebx
  1F956: push     ecx
  1F957: push     edx
  1F958: mov      eax, 5
  1F95D: call     0x1badf
  1F962: test     al, al
  1F964: je       0x1fa29
  1F96A: mov      byte ptr [0x9ef3], 1
  1F971: mov      edx, 0x258
  1F976: mov      eax, 0x20e5b
  1F97B: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1F980: mov      edx, dword ptr [0xfac8]
  1F986: mov      word ptr [edx + 0x4ce], 0x280
  1F98F: mov      edx, dword ptr [0xfac8]
  1F995: mov      word ptr [edx + 0x4d0], 0x190
  1F99E: mov      ax, word ptr [0xfb94]
  1F9A4: mov      word ptr [0xfb78], ax
  1F9AA: mov      word ptr [0xfb7a], 0x4ce
  1F9B3: mov      byte ptr [0xfb7c], 4
  1F9BA: mov      word ptr [0xfb7d], 0x280
  1F9C3: mov      word ptr [0xfb7f], 0x190
  1F9CC: mov      ecx, dword ptr [0xf914]
  1F9D2: mov      ebx, 1
  1F9D7: mov      edx, 9
  1F9DC: mov      eax, 0xfb78
  1F9E1: call     0x2a6b7  ; write_data_to_alfred1
  1F9E6: mov      edx, dword ptr [0xfaac]
  1F9EC: mov      edx, dword ptr [edx + 0x50]
  1F9EF: add      edx, 0x4ce
  1F9F5: mov      eax, dword ptr [0xf8f0]
  1F9FA: xor      ebx, ebx
  1F9FC: call     0x2a342  ; file_seek
  1FA01: mov      ecx, dword ptr [0xf8f0]
  1FA07: mov      eax, dword ptr [0xfac8]
  1FA0C: add      eax, 0x4ce
  1FA11: mov      ebx, 1
  1FA16: mov      edx, 4
  1FA1B: call     0x2a6b7  ; write_data_to_alfred1
  1FA20: call     0x20722
  1FA25: pop      edx
  1FA26: pop      ecx
  1FA27: pop      ebx
  1FA28: ret      
```

</details>

---

## Room 16

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 108 | 227 | 68 | 86 | 388 | Visible |
| 1 | 0x485 | 0x00 | 548 | 256 | 64 | 32 | 387 | Visible |

### OPEN Extra 388

**Handler:** Ghidra `0x1CD06` | File `0x20F06` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49F40] == 0
   2. Play ambient sound
   3. Set flag [0x49F40] = 1
   4. Display sticker from ALFRED.6 offset=0x21D5E, size=0x1645
   5. Set room_data[0x1DD] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1CD06: push     0x2c
  1CD0B: call     0x2a218  ; __STK
  1CD10: push     ebx
  1CD11: push     ecx
  1CD12: push     edx
  1CD13: cmp      byte ptr [0x9f40], 0
  1CD1A: jne      0x1cde2
  1CD20: xor      eax, eax
  1CD22: mov      al, byte ptr [0x13002]
  1CD27: push     eax
  1CD28: mov      edx, dword ptr [0x13234]
  1CD2E: push     edx
  1CD2F: push     0x20
  1CD31: push     0x100
  1CD36: push     0x100
  1CD3B: push     -1
  1CD3D: mov      ebx, dword ptr [0x13204]
  1CD43: push     ebx
  1CD44: call     0x27ce1  ; play_ambient_sound
  1CD49: mov      byte ptr [0x9f40], 1
  1CD50: mov      edx, 0x1645
  1CD55: mov      eax, 0x21d5e
  1CD5A: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1CD5F: mov      eax, dword ptr [0xfac8]
  1CD64: mov      byte ptr [eax + 0x1dd], 1
  1CD6B: mov      ax, word ptr [0xfb94]
  1CD71: mov      word ptr [0xfb70], ax
  1CD77: mov      word ptr [0xfb72], 0x1dd
  1CD80: mov      dh, 1
  1CD82: mov      byte ptr [0xfb74], dh
  1CD88: mov      byte ptr [0xfb75], dh
  1CD8E: mov      ecx, dword ptr [0xf914]
  1CD94: mov      ebx, 1
  1CD99: mov      edx, 6
  1CD9E: mov      eax, 0xfb70
  1CDA3: call     0x2a6b7  ; write_data_to_alfred1
  1CDA8: mov      eax, dword ptr [0xfaac]
  1CDAD: mov      edx, dword ptr [eax + 0x50]
  1CDB0: add      edx, 0x1dd
  1CDB6: mov      eax, dword ptr [0xf8f0]
  1CDBB: xor      ebx, ebx
  1CDBD: call     0x2a342  ; file_seek
  1CDC2: mov      ecx, dword ptr [0xf8f0]
  1CDC8: mov      eax, dword ptr [0xfac8]
  1CDCD: add      eax, 0x1dd
  1CDD2: mov      ebx, 1
  1CDD7: mov      edx, ebx
  1CDD9: call     0x2a6b7  ; write_data_to_alfred1
  1CDDE: pop      edx
  1CDDF: pop      ecx
  1CDE0: pop      ebx
  1CDE1: ret      
```

</details>

### PULL Extra 388

**Handler:** Ghidra `0x1DDD1` | File `0x21FD1` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49F40] == 0
   2. Play ambient sound
   3. Set flag [0x49F40] = 13
   4. Display sticker from ALFRED.6 offset=0x233A3, size=0x1645
   5. Set room_data[0x1DD] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1DDD1: push     0x2c
  1DDD6: call     0x2a218  ; __STK
  1DDDB: push     ebx
  1DDDC: push     ecx
  1DDDD: push     edx
  1DDDE: cmp      byte ptr [0x9f40], 0
  1DDE5: je       0x1deaf
  1DDEB: xor      eax, eax
  1DDED: mov      al, byte ptr [0x13002]
  1DDF2: push     eax
  1DDF3: mov      edx, dword ptr [0x13238]
  1DDF9: push     edx
  1DDFA: push     0x20
  1DDFC: push     0x100
  1DE01: push     0x100
  1DE06: push     -1
  1DE08: mov      ebx, dword ptr [0x13204]
  1DE0E: push     ebx
  1DE0F: call     0x27ce1  ; play_ambient_sound
  1DE14: xor      dl, dl
  1DE16: mov      byte ptr [0x9f40], dl
  1DE1C: mov      edx, 0x1645
  1DE21: mov      eax, 0x233a3
  1DE26: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1DE2B: mov      eax, dword ptr [0xfac8]
  1DE30: mov      byte ptr [eax + 0x1dd], 0
  1DE37: mov      ax, word ptr [0xfb94]
  1DE3D: mov      word ptr [0xfb70], ax
  1DE43: mov      word ptr [0xfb72], 0x1dd
  1DE4C: mov      byte ptr [0xfb74], 1
  1DE53: xor      bl, bl
  1DE55: mov      byte ptr [0xfb75], bl
  1DE5B: mov      ecx, dword ptr [0xf914]
  1DE61: mov      ebx, 1
  1DE66: mov      edx, 6
  1DE6B: mov      eax, 0xfb70
  1DE70: call     0x2a6b7  ; write_data_to_alfred1
  1DE75: mov      eax, dword ptr [0xfaac]
  1DE7A: mov      edx, dword ptr [eax + 0x50]
  1DE7D: add      edx, 0x1dd
  1DE83: mov      eax, dword ptr [0xf8f0]
  1DE88: xor      ebx, ebx
  1DE8A: call     0x2a342  ; file_seek
  1DE8F: mov      ecx, dword ptr [0xf8f0]
  1DE95: mov      eax, dword ptr [0xfac8]
  1DE9A: add      eax, 0x1dd
  1DE9F: mov      ebx, 1
  1DEA4: mov      edx, ebx
  1DEA6: call     0x2a6b7  ; write_data_to_alfred1
  1DEAB: pop      edx
  1DEAC: pop      ecx
  1DEAD: pop      ebx
  1DEAE: ret      
```

</details>

---

## Room 17

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 300 | 146 | 51 | 81 | 393 | Visible |
| 1 | 0x485 | 0x00 | 250 | 185 | 36 | 57 | 394 | Visible |

### OPEN Extra 393

**Handler:** Ghidra `0x1CDF0` | File `0x20FF0` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49FCC] == 0
   2. Play ambient sound
   3. Set flag [0x49FCC] = 1
   4. Display sticker from ALFRED.6 offset=0x249E8, size=0xD8F
   5. Set room_data[0x1CF] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1CDF0: push     0x2c
  1CDF5: call     0x2a218  ; __STK
  1CDFA: push     ebx
  1CDFB: push     ecx
  1CDFC: push     edx
  1CDFD: cmp      byte ptr [0x9fcc], 0
  1CE04: jne      0x1cecc
  1CE0A: xor      eax, eax
  1CE0C: mov      al, byte ptr [0x13002]
  1CE11: push     eax
  1CE12: mov      edx, dword ptr [0x13234]
  1CE18: push     edx
  1CE19: push     0x20
  1CE1B: push     0x100
  1CE20: push     0x100
  1CE25: push     -1
  1CE27: mov      ebx, dword ptr [0x13204]
  1CE2D: push     ebx
  1CE2E: call     0x27ce1  ; play_ambient_sound
  1CE33: mov      byte ptr [0x9fcc], 1
  1CE3A: mov      edx, 0xd8f
  1CE3F: mov      eax, 0x249e8
  1CE44: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1CE49: mov      eax, dword ptr [0xfac8]
  1CE4E: mov      byte ptr [eax + 0x1cf], 1
  1CE55: mov      ax, word ptr [0xfb94]
  1CE5B: mov      word ptr [0xfb70], ax
  1CE61: mov      word ptr [0xfb72], 0x1cf
  1CE6A: mov      dh, 1
  1CE6C: mov      byte ptr [0xfb74], dh
  1CE72: mov      byte ptr [0xfb75], dh
  1CE78: mov      ecx, dword ptr [0xf914]
  1CE7E: mov      ebx, 1
  1CE83: mov      edx, 6
  1CE88: mov      eax, 0xfb70
  1CE8D: call     0x2a6b7  ; write_data_to_alfred1
  1CE92: mov      eax, dword ptr [0xfaac]
  1CE97: mov      edx, dword ptr [eax + 0x50]
  1CE9A: add      edx, 0x1cf
  1CEA0: mov      eax, dword ptr [0xf8f0]
  1CEA5: xor      ebx, ebx
  1CEA7: call     0x2a342  ; file_seek
  1CEAC: mov      ecx, dword ptr [0xf8f0]
  1CEB2: mov      eax, dword ptr [0xfac8]
  1CEB7: add      eax, 0x1cf
  1CEBC: mov      ebx, 1
  1CEC1: mov      edx, ebx
  1CEC3: call     0x2a6b7  ; write_data_to_alfred1
  1CEC8: pop      edx
  1CEC9: pop      ecx
  1CECA: pop      ebx
  1CECB: ret      
```

</details>

### PULL Extra 393

**Handler:** Ghidra `0x1DEBD` | File `0x220BD` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x49FCC] == 0
   2. Play ambient sound
   3. Set flag [0x49FCC] = 13
   4. Display sticker from ALFRED.6 offset=0x25777, size=0xD8F
   5. Set room_data[0x1CF] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1DEBD: push     0x2c
  1DEC2: call     0x2a218  ; __STK
  1DEC7: push     ebx
  1DEC8: push     ecx
  1DEC9: push     edx
  1DECA: cmp      byte ptr [0x9fcc], 0
  1DED1: je       0x1df9b
  1DED7: xor      eax, eax
  1DED9: mov      al, byte ptr [0x13002]
  1DEDE: push     eax
  1DEDF: mov      edx, dword ptr [0x13238]
  1DEE5: push     edx
  1DEE6: push     0x20
  1DEE8: push     0x100
  1DEED: push     0x100
  1DEF2: push     -1
  1DEF4: mov      ebx, dword ptr [0x13204]
  1DEFA: push     ebx
  1DEFB: call     0x27ce1  ; play_ambient_sound
  1DF00: xor      dl, dl
  1DF02: mov      byte ptr [0x9fcc], dl
  1DF08: mov      edx, 0xd8f
  1DF0D: mov      eax, 0x25777
  1DF12: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1DF17: mov      eax, dword ptr [0xfac8]
  1DF1C: mov      byte ptr [eax + 0x1cf], 0
  1DF23: mov      ax, word ptr [0xfb94]
  1DF29: mov      word ptr [0xfb70], ax
  1DF2F: mov      word ptr [0xfb72], 0x1cf
  1DF38: mov      byte ptr [0xfb74], 1
  1DF3F: xor      bl, bl
  1DF41: mov      byte ptr [0xfb75], bl
  1DF47: mov      ecx, dword ptr [0xf914]
  1DF4D: mov      ebx, 1
  1DF52: mov      edx, 6
  1DF57: mov      eax, 0xfb70
  1DF5C: call     0x2a6b7  ; write_data_to_alfred1
  1DF61: mov      eax, dword ptr [0xfaac]
  1DF66: mov      edx, dword ptr [eax + 0x50]
  1DF69: add      edx, 0x1cf
  1DF6F: mov      eax, dword ptr [0xf8f0]
  1DF74: xor      ebx, ebx
  1DF76: call     0x2a342  ; file_seek
  1DF7B: mov      ecx, dword ptr [0xf8f0]
  1DF81: mov      eax, dword ptr [0xfac8]
  1DF86: add      eax, 0x1cf
  1DF8B: mov      ebx, 1
  1DF90: mov      edx, ebx
  1DF92: call     0x2a6b7  ; write_data_to_alfred1
  1DF97: pop      edx
  1DF98: pop      ecx
  1DF99: pop      ebx
  1DF9A: ret      
```

</details>

---

## Room 19

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 328 | 228 | 61 | 113 | 400 | Visible |

### OPEN Extra 400

**Handler:** Ghidra `0x1CEDA` | File `0x210DA` | Size: 233 bytes | 54 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4A0E4] == 0
   2. Check flag [0x4A0F9] == 0
   3. Play ambient sound
   4. Set flag [0x4A0F9] = 1
   5. Display sticker from ALFRED.6 offset=0x2C9D7, size=0x1AF3
   6. Set room_data[0x1CF] = 1

<details>
<summary>Raw disassembly (54 instructions)</summary>

```asm
  1CEDA: push     0x2c
  1CEDF: call     0x2a218  ; __STK
  1CEE4: push     ebx
  1CEE5: push     ecx
  1CEE6: push     edx
  1CEE7: cmp      byte ptr [0xa0e4], 0
  1CEEE: je       0x1cfcd
  1CEF4: cmp      byte ptr [0xa0f9], 0
  1CEFB: jne      0x1cfc3
  1CF01: xor      eax, eax
  1CF03: mov      al, byte ptr [0x13002]
  1CF08: push     eax
  1CF09: mov      edx, dword ptr [0x13234]
  1CF0F: push     edx
  1CF10: push     0x20
  1CF12: push     0x100
  1CF17: push     0x100
  1CF1C: push     -1
  1CF1E: mov      ebx, dword ptr [0x13204]
  1CF24: push     ebx
  1CF25: call     0x27ce1  ; play_ambient_sound
  1CF2A: mov      byte ptr [0xa0f9], 1
  1CF31: mov      edx, 0x1af3
  1CF36: mov      eax, 0x2c9d7
  1CF3B: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1CF40: mov      eax, dword ptr [0xfac8]
  1CF45: mov      byte ptr [eax + 0x1cf], 1
  1CF4C: mov      ax, word ptr [0xfb94]
  1CF52: mov      word ptr [0xfb70], ax
  1CF58: mov      word ptr [0xfb72], 0x1cf
  1CF61: mov      bl, 1
  1CF63: mov      byte ptr [0xfb74], bl
  1CF69: mov      byte ptr [0xfb75], bl
  1CF6F: mov      ecx, dword ptr [0xf914]
  1CF75: mov      ebx, 1
  1CF7A: mov      edx, 6
  1CF7F: mov      eax, 0xfb70
  1CF84: call     0x2a6b7  ; write_data_to_alfred1
  1CF89: mov      eax, dword ptr [0xfaac]
  1CF8E: mov      edx, dword ptr [eax + 0x50]
  1CF91: add      edx, 0x1cf
  1CF97: mov      eax, dword ptr [0xf8f0]
  1CF9C: xor      ebx, ebx
  1CF9E: call     0x2a342  ; file_seek
  1CFA3: mov      ecx, dword ptr [0xf8f0]
  1CFA9: mov      eax, dword ptr [0xfac8]
  1CFAE: add      eax, 0x1cf
  1CFB3: mov      ebx, 1
  1CFB8: mov      edx, ebx
  1CFBA: call     0x2a6b7  ; write_data_to_alfred1
  1CFBF: pop      edx
  1CFC0: pop      ecx
  1CFC1: pop      ebx
  1CFC2: ret      
```

</details>

### PULL Extra 400

**Handler:** Ghidra `0x1DFA9` | File `0x221A9` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4A0F9] == 0
   2. Play ambient sound
   3. Set flag [0x4A0F9] = 13
   4. Display sticker from ALFRED.6 offset=0x2E4CA, size=0x1AF3
   5. Set room_data[0x1CF] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1DFA9: push     0x2c
  1DFAE: call     0x2a218  ; __STK
  1DFB3: push     ebx
  1DFB4: push     ecx
  1DFB5: push     edx
  1DFB6: cmp      byte ptr [0xa0f9], 0
  1DFBD: je       0x1e087
  1DFC3: xor      eax, eax
  1DFC5: mov      al, byte ptr [0x13002]
  1DFCA: push     eax
  1DFCB: mov      edx, dword ptr [0x13238]
  1DFD1: push     edx
  1DFD2: push     0x20
  1DFD4: push     0x100
  1DFD9: push     0x100
  1DFDE: push     -1
  1DFE0: mov      ebx, dword ptr [0x13204]
  1DFE6: push     ebx
  1DFE7: call     0x27ce1  ; play_ambient_sound
  1DFEC: xor      dl, dl
  1DFEE: mov      byte ptr [0xa0f9], dl
  1DFF4: mov      edx, 0x1af3
  1DFF9: mov      eax, 0x2e4ca
  1DFFE: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1E003: mov      eax, dword ptr [0xfac8]
  1E008: mov      byte ptr [eax + 0x1cf], 0
  1E00F: mov      ax, word ptr [0xfb94]
  1E015: mov      word ptr [0xfb70], ax
  1E01B: mov      word ptr [0xfb72], 0x1cf
  1E024: mov      byte ptr [0xfb74], 1
  1E02B: xor      bl, bl
  1E02D: mov      byte ptr [0xfb75], bl
  1E033: mov      ecx, dword ptr [0xf914]
  1E039: mov      ebx, 1
  1E03E: mov      edx, 6
  1E043: mov      eax, 0xfb70
  1E048: call     0x2a6b7  ; write_data_to_alfred1
  1E04D: mov      eax, dword ptr [0xfaac]
  1E052: mov      edx, dword ptr [eax + 0x50]
  1E055: add      edx, 0x1cf
  1E05B: mov      eax, dword ptr [0xf8f0]
  1E060: xor      ebx, ebx
  1E062: call     0x2a342  ; file_seek
  1E067: mov      ecx, dword ptr [0xf8f0]
  1E06D: mov      eax, dword ptr [0xfac8]
  1E072: add      eax, 0x1cf
  1E077: mov      ebx, 1
  1E07C: mov      edx, ebx
  1E07E: call     0x2a6b7  ; write_data_to_alfred1
  1E083: pop      edx
  1E084: pop      ecx
  1E085: pop      ebx
  1E086: ret      
```

</details>

---

## Room 25

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x08 | 612 | 239 | 16 | 49 | 609 | Visible |
| 1 | 0x485 | 0x00 | 192 | 331 | 37 | 27 | 469 | Visible |
| 2 | 0x48E | 0x00 | 263 | 88 | 23 | 19 | 469 | Visible |

### PICKUP Extra 609

**Handler:** Ghidra `0x1FD8B` | File `0x23F8B` | Size: 254 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495D0] == 0
   2. Set flag [0x4A42C] = 1
   3. Display sticker from ALFRED.6 offset=0x496CB, size=0x316
   4. HIDE hotspot[0] @0x47D → (640, 400)
   5. Set flag [0x4964F] = 12
   6. Default verb response ("I can't do that")

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x47D | 0 | 609 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1FD8B: push     0x10
  1FD90: call     0x2a218  ; __STK
  1FD95: push     ebx
  1FD96: push     ecx
  1FD97: push     edx
  1FD98: cmp      byte ptr [0x95d0], 0
  1FD9F: je       0x1fe89
  1FDA5: mov      eax, 0x55
  1FDAA: call     0x24157
  1FDAF: mov      byte ptr [0xa42c], 1
  1FDB6: mov      edx, 0x316
  1FDBB: mov      eax, 0x496cb
  1FDC0: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1FDC5: mov      eax, dword ptr [0xfac8]
  1FDCA: mov      word ptr [eax + 0x47d], 0x280
  1FDD3: mov      eax, dword ptr [0xfac8]
  1FDD8: mov      word ptr [eax + 0x47f], 0x190
  1FDE1: mov      ax, word ptr [0xfb94]
  1FDE7: mov      word ptr [0xfb78], ax
  1FDED: mov      word ptr [0xfb7a], 0x47d
  1FDF6: mov      byte ptr [0xfb7c], 4
  1FDFD: mov      word ptr [0xfb7d], 0x280
  1FE06: mov      word ptr [0xfb7f], 0x190
  1FE0F: mov      ecx, dword ptr [0xf914]
  1FE15: mov      ebx, 1
  1FE1A: mov      edx, 9
  1FE1F: mov      eax, 0xfb78
  1FE24: call     0x2a6b7  ; write_data_to_alfred1
  1FE29: mov      eax, dword ptr [0xfaac]
  1FE2E: mov      edx, dword ptr [eax + 0x50]
  1FE31: add      edx, 0x47d
  1FE37: mov      eax, dword ptr [0xf8f0]
  1FE3C: xor      ebx, ebx
  1FE3E: call     0x2a342  ; file_seek
  1FE43: mov      ecx, dword ptr [0xf8f0]
  1FE49: mov      eax, dword ptr [0xfac8]
  1FE4E: add      eax, 0x47d
  1FE53: mov      ebx, 1
  1FE58: mov      edx, 4
  1FE5D: call     0x2a6b7  ; write_data_to_alfred1
  1FE62: mov      cl, byte ptr [0x964f]
  1FE68: inc      cl
  1FE6A: mov      byte ptr [0x964f], cl
  1FE70: xor      eax, eax
  1FE72: mov      al, cl
  1FE74: mov      eax, dword ptr [eax*4 + 0xbc64]
  1FE7B: call     0x25487  ; default_verb_response
  1FE80: call     0x26fab
  1FE85: pop      edx
  1FE86: pop      ecx
  1FE87: pop      ebx
  1FE88: ret      
```

</details>

---

## Room 28

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x08 | 640 | 400 | 52 | 24 | 87 | Hidden |
| 1 | 0x485 | 0x08 | 640 | 400 | 18 | 19 | 88 | Hidden |
| 2 | 0x48E | 0x08 | 640 | 400 | 31 | 34 | 89 | Hidden |
| 3 | 0x497 | 0x08 | 312 | 234 | 22 | 10 | 472 | Visible |
| 4 | 0x4A0 | 0x08 | 640 | 400 | 17 | 13 | 112 | Hidden |

### PICKUP Extra 87

**Handler:** Ghidra `0x2030C` | File `0x2450C` | Size: 35 bytes | 9 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x4A5D0] = 1
   2. JMP → 0x1D284

<details>
<summary>Raw disassembly (9 instructions)</summary>

```asm
  2030C: push     0x10
  20311: call     0x2a218  ; __STK
  20316: push     ebx
  20317: push     ecx
  20318: push     edx
  20319: mov      byte ptr [0xa5d0], 1
  20320: mov      edx, 0x3a2
  20325: mov      eax, 0x613c2
  2032A: jmp      0x1d284
```

</details>

### PICKUP Extra 88

**Handler:** Ghidra `0x2032F` | File `0x2452F` | Size: 40 bytes | 10 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x4A5D7] = 1
   2. Display sticker from ALFRED.6 offset=0x60E62, size=0x1D7
   3. JMP → 0x1FCF8

<details>
<summary>Raw disassembly (10 instructions)</summary>

```asm
  2032F: push     0x10
  20334: call     0x2a218  ; __STK
  20339: push     ebx
  2033A: push     ecx
  2033B: push     edx
  2033C: mov      byte ptr [0xa5d7], 1
  20343: mov      edx, 0x1d7
  20348: mov      eax, 0x60e62
  2034D: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  20352: jmp      0x1fcf8
```

</details>

### PICKUP Extra 89

**Handler:** Ghidra `0x20357` | File `0x24557` | Size: 35 bytes | 9 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x4A5DE] = 1
   2. JMP → 0x1EE4F

<details>
<summary>Raw disassembly (9 instructions)</summary>

```asm
  20357: push     0x10
  2035C: call     0x2a218  ; __STK
  20361: push     ebx
  20362: push     ecx
  20363: push     edx
  20364: mov      byte ptr [0xa5de], 1
  2036B: mov      edx, 0x389
  20370: mov      eax, 0x61039
  20375: jmp      0x1ee4f
```

</details>

### PICKUP Extra 112

**Handler:** Ghidra `0x2037A` | File `0x2457A` | Size: 213 bytes | 44 instructions | Ends: `ret`

**Operations:**

   1. Set flag [0x4A5EC] = 1
   2. Display sticker from ALFRED.6 offset=0x61764, size=0xE3
   3. HIDE hotspot[4] @0x4A1 → (640, 400)
   4. Update conversation state (room=23)

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x4A1 | 4 | 112 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (44 instructions)</summary>

```asm
  2037A: push     0x10
  2037F: call     0x2a218  ; __STK
  20384: push     ebx
  20385: push     ecx
  20386: push     edx
  20387: mov      byte ptr [0xa5ec], 1
  2038E: mov      edx, 0xe3
  20393: mov      eax, 0x61764
  20398: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  2039D: mov      eax, dword ptr [0xfac8]
  203A2: mov      word ptr [eax + 0x4a1], 0x280
  203AB: mov      eax, dword ptr [0xfac8]
  203B0: mov      word ptr [eax + 0x4a3], 0x190
  203B9: mov      ax, word ptr [0xfb94]
  203BF: mov      word ptr [0xfb78], ax
  203C5: mov      word ptr [0xfb7a], 0x4a1
  203CE: mov      byte ptr [0xfb7c], 4
  203D5: mov      word ptr [0xfb7d], 0x280
  203DE: mov      word ptr [0xfb7f], 0x190
  203E7: mov      ecx, dword ptr [0xf914]
  203ED: mov      ebx, 1
  203F2: mov      edx, 9
  203F7: mov      eax, 0xfb78
  203FC: call     0x2a6b7  ; write_data_to_alfred1
  20401: mov      eax, dword ptr [0xfaac]
  20406: mov      edx, dword ptr [eax + 0x50]
  20409: add      edx, 0x4a1
  2040F: mov      eax, dword ptr [0xf8f0]
  20414: xor      ebx, ebx
  20416: call     0x2a342  ; file_seek
  2041B: mov      ecx, dword ptr [0xf8f0]
  20421: mov      eax, dword ptr [0xfac8]
  20426: add      eax, 0x4a1
  2042B: mov      ebx, 1
  20430: mov      edx, 4
  20435: call     0x2a6b7  ; write_data_to_alfred1
  2043A: mov      ebx, 1
  2043F: xor      edx, edx
  20441: mov      eax, 0x17
  20446: call     0x1b666  ; update_conversation_state
  2044B: pop      edx
  2044C: pop      ecx
  2044D: pop      ebx
  2044E: ret      
```

</details>

### PICKUP Extra 472

**Handler:** Ghidra `0x1FED8` | File `0x240D8` | Size: 1076 bytes | 203 instructions | Ends: `jmp`

**Operations:**

   1. Play ambient sound
   2. Load palette from ALFRED.7 offset=0x1610CE
   3. Fade palette to target
   4. Set flag [0x495CB] = 1
   5. SHOW hotspot[0] @0x47D → (415, 171)
   6. SHOW hotspot[1] @0x486 → (305, 217)
   7. SHOW hotspot[2] @0x48F → (201, 239)
   8. SHOW hotspot[4] @0x4A1 → (261, 259)
   9. HIDE hotspot[3] @0x498 → (640, 400)
   10. Set room_data[0xA5] = 2
   11. JMP → 0x14A1B

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x47D | 0 | 87 | 415 | 171 | SHOW |
| 0x486 | 1 | 88 | 305 | 217 | SHOW |
| 0x48F | 2 | 89 | 201 | 239 | SHOW |
| 0x4A1 | 4 | 112 | 261 | 259 | SHOW |
| 0x498 | 3 | 472 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (203 instructions)</summary>

```asm
  1FED8: push     0x34
  1FEDD: call     0x2a218  ; __STK
  1FEE2: push     ebx
  1FEE3: push     ecx
  1FEE4: push     edx
  1FEE5: push     esi
  1FEE6: push     edi
  1FEE7: xor      eax, eax
  1FEE9: mov      al, byte ptr [0x13002]
  1FEEE: push     eax
  1FEEF: mov      edx, dword ptr [0x13234]
  1FEF5: push     edx
  1FEF6: push     0x20
  1FEF8: push     0x100
  1FEFD: push     0x100
  1FF02: push     -1
  1FF04: mov      ebx, dword ptr [0x13204]
  1FF0A: push     ebx
  1FF0B: call     0x27ce1  ; play_ambient_sound
  1FF10: mov      edi, dword ptr [0xfab8]
  1FF16: mov      eax, 0x300
  1FF1B: call     0x25e90  ; allocate_memory
  1FF20: mov      esi, eax
  1FF22: mov      eax, dword ptr [0xf908]
  1FF27: xor      ebx, ebx
  1FF29: mov      edx, 0x1610ce
  1FF2E: call     0x2a342  ; file_seek
  1FF33: mov      ecx, dword ptr [0xf908]
  1FF39: mov      ebx, 1
  1FF3E: mov      edx, 0x300
  1FF43: mov      eax, esi
  1FF45: call     0x2a43e  ; file_read
  1FF4A: push     1
  1FF4C: mov      ecx, 0x9508
  1FF51: mov      ebx, 0x100
  1FF56: mov      edx, esi
  1FF58: mov      eax, edi
  1FF5A: call     0x1bd53  ; fade_palette_to_target
  1FF5F: mov      ebx, 0x300
  1FF64: mov      edx, esi
  1FF66: mov      eax, edi
  1FF68: call     0x2a66b  ; memcpy_wrapper
  1FF6D: mov      byte ptr [0x95cb], 1
  1FF74: mov      eax, dword ptr [0xfac8]
  1FF79: mov      word ptr [eax + 0x47d], 0x19f
  1FF82: mov      eax, dword ptr [0xfac8]
  1FF87: mov      word ptr [eax + 0x47f], 0xab
  1FF90: mov      ax, word ptr [0xfb94]
  1FF96: mov      word ptr [0xfb78], ax
  1FF9C: mov      word ptr [0xfb7a], 0x47d
  1FFA5: mov      byte ptr [0xfb7c], 4
  1FFAC: mov      word ptr [0xfb7d], 0x19f
  1FFB5: mov      word ptr [0xfb7f], 0xab
  1FFBE: mov      ecx, dword ptr [0xf914]
  1FFC4: mov      ebx, 1
  1FFC9: mov      edx, 9
  1FFCE: mov      eax, 0xfb78
  1FFD3: call     0x2a6b7  ; write_data_to_alfred1
  1FFD8: mov      eax, dword ptr [0xfaac]
  1FFDD: mov      eax, dword ptr [eax + 0x50]
  1FFE0: lea      edx, [eax + 0x47d]
  1FFE6: mov      eax, dword ptr [0xf8f0]
  1FFEB: xor      ebx, ebx
  1FFED: call     0x2a342  ; file_seek
  1FFF2: mov      ecx, dword ptr [0xf8f0]
  1FFF8: mov      eax, dword ptr [0xfac8]
  1FFFD: add      eax, 0x47d
  20002: mov      ebx, 1
  20007: mov      edx, 4
  2000C: call     0x2a6b7  ; write_data_to_alfred1
  20011: mov      eax, dword ptr [0xfac8]
  20016: mov      word ptr [eax + 0x486], 0x131
  2001F: mov      eax, dword ptr [0xfac8]
  20024: mov      word ptr [eax + 0x488], 0xd9
  2002D: mov      ax, word ptr [0xfb94]
  20033: mov      word ptr [0xfb78], ax
  20039: mov      word ptr [0xfb7a], 0x486
  20042: mov      byte ptr [0xfb7c], 4
  20049: mov      word ptr [0xfb7d], 0x131
  20052: mov      word ptr [0xfb7f], 0xd9
  2005B: mov      ecx, dword ptr [0xf914]
  20061: mov      ebx, 1
  20066: mov      edx, 9
  2006B: mov      eax, 0xfb78
  20070: call     0x2a6b7  ; write_data_to_alfred1
  20075: mov      eax, dword ptr [0xfaac]
  2007A: mov      eax, dword ptr [eax + 0x50]
  2007D: lea      edx, [eax + 0x486]
  20083: mov      eax, dword ptr [0xf8f0]
  20088: xor      ebx, ebx
  2008A: call     0x2a342  ; file_seek
  2008F: mov      ecx, dword ptr [0xf8f0]
  20095: mov      eax, dword ptr [0xfac8]
  2009A: add      eax, 0x486
  2009F: mov      ebx, 1
  200A4: mov      edx, 4
  200A9: call     0x2a6b7  ; write_data_to_alfred1
  200AE: mov      eax, dword ptr [0xfac8]
  200B3: mov      word ptr [eax + 0x48f], 0xc9
  200BC: mov      eax, dword ptr [0xfac8]
  200C1: mov      word ptr [eax + 0x491], 0xef
  200CA: mov      ax, word ptr [0xfb94]
  200D0: mov      word ptr [0xfb78], ax
  200D6: mov      word ptr [0xfb7a], 0x48f
  200DF: mov      byte ptr [0xfb7c], 4
  200E6: mov      word ptr [0xfb7d], 0xc9
  200EF: mov      word ptr [0xfb7f], 0xef
  200F8: mov      ecx, dword ptr [0xf914]
  200FE: mov      ebx, 1
  20103: mov      edx, 9
  20108: mov      eax, 0xfb78
  2010D: call     0x2a6b7  ; write_data_to_alfred1
  20112: mov      eax, dword ptr [0xfaac]
  20117: mov      eax, dword ptr [eax + 0x50]
  2011A: lea      edx, [eax + 0x48f]
  20120: mov      eax, dword ptr [0xf8f0]
  20125: xor      ebx, ebx
  20127: call     0x2a342  ; file_seek
  2012C: mov      ecx, dword ptr [0xf8f0]
  20132: mov      eax, dword ptr [0xfac8]
  20137: add      eax, 0x48f
  2013C: mov      ebx, 1
  20141: mov      edx, 4
  20146: call     0x2a6b7  ; write_data_to_alfred1
  2014B: mov      eax, dword ptr [0xfac8]
  20150: mov      word ptr [eax + 0x4a1], 0x105
  20159: mov      eax, dword ptr [0xfac8]
  2015E: mov      word ptr [eax + 0x4a3], 0x103
  20167: mov      ax, word ptr [0xfb94]
  2016D: mov      word ptr [0xfb78], ax
  20173: mov      word ptr [0xfb7a], 0x4a1
  2017C: mov      byte ptr [0xfb7c], 4
  20183: mov      word ptr [0xfb7d], 0x105
  2018C: mov      word ptr [0xfb7f], 0x103
  20195: mov      ecx, dword ptr [0xf914]
  2019B: mov      ebx, 1
  201A0: mov      edx, 9
  201A5: mov      eax, 0xfb78
  201AA: call     0x2a6b7  ; write_data_to_alfred1
  201AF: mov      edx, dword ptr [0xfaac]
  201B5: mov      edx, dword ptr [edx + 0x50]
  201B8: add      edx, 0x4a1
  201BE: mov      eax, dword ptr [0xf8f0]
  201C3: xor      ebx, ebx
  201C5: call     0x2a342  ; file_seek
  201CA: mov      ecx, dword ptr [0xf8f0]
  201D0: mov      eax, dword ptr [0xfac8]
  201D5: add      eax, 0x4a1
  201DA: mov      ebx, 1
  201DF: mov      edx, 4
  201E4: call     0x2a6b7  ; write_data_to_alfred1
  201E9: mov      eax, dword ptr [0xfac8]
  201EE: mov      word ptr [eax + 0x498], 0x280
  201F7: mov      eax, dword ptr [0xfac8]
  201FC: mov      word ptr [eax + 0x49a], 0x190
  20205: mov      ax, word ptr [0xfb94]
  2020B: mov      word ptr [0xfb78], ax
  20211: mov      word ptr [0xfb7a], 0x498
  2021A: mov      byte ptr [0xfb7c], 4
  20221: mov      word ptr [0xfb7d], 0x280
  2022A: mov      word ptr [0xfb7f], 0x190
  20233: mov      ecx, dword ptr [0xf914]
  20239: mov      ebx, 1
  2023E: mov      edx, 9
  20243: mov      eax, 0xfb78
  20248: call     0x2a6b7  ; write_data_to_alfred1
  2024D: mov      edx, dword ptr [0xfaac]
  20253: mov      edx, dword ptr [edx + 0x50]
  20256: add      edx, 0x498
  2025C: mov      eax, dword ptr [0xf8f0]
  20261: xor      ebx, ebx
  20263: call     0x2a342  ; file_seek
  20268: mov      ecx, dword ptr [0xf8f0]
  2026E: mov      eax, dword ptr [0xfac8]
  20273: add      eax, 0x498
  20278: mov      ebx, 1
  2027D: mov      edx, 4
  20282: call     0x2a6b7  ; write_data_to_alfred1
  20287: mov      eax, dword ptr [0xfac8]
  2028C: mov      byte ptr [eax + 0xa5], 2
  20293: mov      ax, word ptr [0xfb94]
  20299: mov      word ptr [0xfb70], ax
  2029F: mov      word ptr [0xfb72], 0xa5
  202A8: mov      byte ptr [0xfb74], 1
  202AF: mov      byte ptr [0xfb75], 2
  202B6: mov      ecx, dword ptr [0xf914]
  202BC: mov      ebx, 1
  202C1: mov      edx, 6
  202C6: mov      eax, 0xfb70
  202CB: call     0x2a6b7  ; write_data_to_alfred1
  202D0: mov      edx, dword ptr [0xfaac]
  202D6: mov      edx, dword ptr [edx + 0x50]
  202D9: add      edx, 0xa5
  202DF: mov      eax, dword ptr [0xf8f0]
  202E4: xor      ebx, ebx
  202E6: call     0x2a342  ; file_seek
  202EB: mov      ecx, dword ptr [0xf8f0]
  202F1: mov      eax, dword ptr [0xfac8]
  202F6: add      eax, 0xa5
  202FB: mov      ebx, 1
  20300: mov      edx, ebx
  20302: call     0x2a6b7  ; write_data_to_alfred1
  20307: jmp      0x14a1b
```

</details>

---

## Room 29

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 139 | 213 | 80 | 103 | 434 | Visible |
| 1 | 0x485 | 0x00 | 73 | 264 | 36 | 33 | 643 | Visible |

### OPEN Extra 434

**Handler:** Ghidra `0x1CFD1` | File `0x211D1` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4A65C] == 0
   2. Play ambient sound
   3. Set flag [0x4A65C] = 1
   4. Display sticker from ALFRED.6 offset=0x4115D, size=0x41A6
   5. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1CFD1: push     0x2c
  1CFD6: call     0x2a218  ; __STK
  1CFDB: push     ebx
  1CFDC: push     ecx
  1CFDD: push     edx
  1CFDE: cmp      byte ptr [0xa65c], 0
  1CFE5: jne      0x1d0ad
  1CFEB: xor      eax, eax
  1CFED: mov      al, byte ptr [0x13002]
  1CFF2: push     eax
  1CFF3: mov      edx, dword ptr [0x13234]
  1CFF9: push     edx
  1CFFA: push     0x20
  1CFFC: push     0x100
  1D001: push     0x100
  1D006: push     -1
  1D008: mov      ebx, dword ptr [0x13204]
  1D00E: push     ebx
  1D00F: call     0x27ce1  ; play_ambient_sound
  1D014: mov      byte ptr [0xa65c], 1
  1D01B: mov      edx, 0x41a6
  1D020: mov      eax, 0x4115d
  1D025: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D02A: mov      eax, dword ptr [0xfac8]
  1D02F: mov      byte ptr [eax + 0x1c1], 1
  1D036: mov      ax, word ptr [0xfb94]
  1D03C: mov      word ptr [0xfb70], ax
  1D042: mov      word ptr [0xfb72], 0x1c1
  1D04B: mov      dh, 1
  1D04D: mov      byte ptr [0xfb74], dh
  1D053: mov      byte ptr [0xfb75], dh
  1D059: mov      ecx, dword ptr [0xf914]
  1D05F: mov      ebx, 1
  1D064: mov      edx, 6
  1D069: mov      eax, 0xfb70
  1D06E: call     0x2a6b7  ; write_data_to_alfred1
  1D073: mov      eax, dword ptr [0xfaac]
  1D078: mov      edx, dword ptr [eax + 0x50]
  1D07B: add      edx, 0x1c1
  1D081: mov      eax, dword ptr [0xf8f0]
  1D086: xor      ebx, ebx
  1D088: call     0x2a342  ; file_seek
  1D08D: mov      ecx, dword ptr [0xf8f0]
  1D093: mov      eax, dword ptr [0xfac8]
  1D098: add      eax, 0x1c1
  1D09D: mov      ebx, 1
  1D0A2: mov      edx, ebx
  1D0A4: call     0x2a6b7  ; write_data_to_alfred1
  1D0A9: pop      edx
  1D0AA: pop      ecx
  1D0AB: pop      ebx
  1D0AC: ret      
```

</details>

### PULL Extra 434

**Handler:** Ghidra `0x1E095` | File `0x22295` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4A65C] == 0
   2. Play ambient sound
   3. Set flag [0x4A65C] = 13
   4. Display sticker from ALFRED.6 offset=0x45303, size=0x41A6
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1E095: push     0x2c
  1E09A: call     0x2a218  ; __STK
  1E09F: push     ebx
  1E0A0: push     ecx
  1E0A1: push     edx
  1E0A2: cmp      byte ptr [0xa65c], 0
  1E0A9: je       0x1e173
  1E0AF: xor      eax, eax
  1E0B1: mov      al, byte ptr [0x13002]
  1E0B6: push     eax
  1E0B7: mov      edx, dword ptr [0x13238]
  1E0BD: push     edx
  1E0BE: push     0x20
  1E0C0: push     0x100
  1E0C5: push     0x100
  1E0CA: push     -1
  1E0CC: mov      ebx, dword ptr [0x13204]
  1E0D2: push     ebx
  1E0D3: call     0x27ce1  ; play_ambient_sound
  1E0D8: xor      dl, dl
  1E0DA: mov      byte ptr [0xa65c], dl
  1E0E0: mov      edx, 0x41a6
  1E0E5: mov      eax, 0x45303
  1E0EA: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1E0EF: mov      eax, dword ptr [0xfac8]
  1E0F4: mov      byte ptr [eax + 0x1c1], 0
  1E0FB: mov      ax, word ptr [0xfb94]
  1E101: mov      word ptr [0xfb70], ax
  1E107: mov      word ptr [0xfb72], 0x1c1
  1E110: mov      byte ptr [0xfb74], 1
  1E117: xor      bl, bl
  1E119: mov      byte ptr [0xfb75], bl
  1E11F: mov      ecx, dword ptr [0xf914]
  1E125: mov      ebx, 1
  1E12A: mov      edx, 6
  1E12F: mov      eax, 0xfb70
  1E134: call     0x2a6b7  ; write_data_to_alfred1
  1E139: mov      eax, dword ptr [0xfaac]
  1E13E: mov      edx, dword ptr [eax + 0x50]
  1E141: add      edx, 0x1c1
  1E147: mov      eax, dword ptr [0xf8f0]
  1E14C: xor      ebx, ebx
  1E14E: call     0x2a342  ; file_seek
  1E153: mov      ecx, dword ptr [0xf8f0]
  1E159: mov      eax, dword ptr [0xfac8]
  1E15E: add      eax, 0x1c1
  1E163: mov      ebx, 1
  1E168: mov      edx, ebx
  1E16A: call     0x2a6b7  ; write_data_to_alfred1
  1E16F: pop      edx
  1E170: pop      ecx
  1E171: pop      ebx
  1E172: ret      
```

</details>

---

## Room 30

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x20 | 431 | 244 | 8 | 30 | 435 | Visible |
| 1 | 0x485 | 0x20 | 430 | 178 | 15 | 26 | 436 | Visible |
| 2 | 0x48E | 0x20 | 456 | 192 | 10 | 23 | 437 | Visible |
| 3 | 0x497 | 0x20 | 428 | 207 | 14 | 13 | 438 | Visible |
| 4 | 0x4A0 | 0x20 | 429 | 224 | 13 | 18 | 439 | Visible |
| 5 | 0x4A9 | 0x20 | 447 | 218 | 20 | 10 | 440 | Visible |
| 6 | 0x4B2 | 0x20 | 446 | 229 | 9 | 23 | 441 | Visible |
| 7 | 0x4BB | 0x20 | 440 | 253 | 32 | 4 | 439 | Visible |
| 8 | 0x4C4 | 0x20 | 450 | 260 | 22 | 35 | 440 | Visible |
| 9 | 0x4CD | 0x20 | 429 | 275 | 19 | 15 | 441 | Visible |

### LOOK Extra 435

**Handler:** Ghidra `0x1C065` | File `0x20265` | Size: 51 bytes | 15 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495E5] == 0
   2. OR flag [0x495C8] |= 0x1
   3. Set flag [0x495C8] = 13
   4. Check combined flags == 0xF
   5. Trigger statue_secret

<details>
<summary>Raw disassembly (15 instructions)</summary>

```asm
  1C065: push     8
  1C06A: call     0x2a218  ; __STK
  1C06F: push     edx
  1C070: cmp      byte ptr [0x95e5], 0
  1C077: je       0x1c096
  1C079: mov      dl, byte ptr [0x95c8]
  1C07F: or       dl, 1
  1C082: mov      byte ptr [0x95c8], dl
  1C088: xor      eax, eax
  1C08A: mov      al, dl
  1C08C: cmp      eax, 0xf
  1C08F: jne      0x1c096
  1C091: call     0x1c131  ; trigger_statue_secret
  1C096: pop      edx
  1C097: ret      
```

</details>

### LOOK Extra 436

**Handler:** Ghidra `0x1C098` | File `0x20298` | Size: 51 bytes | 15 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495E5] == 0
   2. OR flag [0x495C8] |= 0x2
   3. Set flag [0x495C8] = 13
   4. Check combined flags == 0xF
   5. Trigger statue_secret

<details>
<summary>Raw disassembly (15 instructions)</summary>

```asm
  1C098: push     8
  1C09D: call     0x2a218  ; __STK
  1C0A2: push     edx
  1C0A3: cmp      byte ptr [0x95e5], 0
  1C0AA: je       0x1c0c9
  1C0AC: mov      dl, byte ptr [0x95c8]
  1C0B2: or       dl, 2
  1C0B5: mov      byte ptr [0x95c8], dl
  1C0BB: xor      eax, eax
  1C0BD: mov      al, dl
  1C0BF: cmp      eax, 0xf
  1C0C2: jne      0x1c0c9
  1C0C4: call     0x1c131  ; trigger_statue_secret
  1C0C9: pop      edx
  1C0CA: ret      
```

</details>

### LOOK Extra 437

**Handler:** Ghidra `0x1C0CB` | File `0x202CB` | Size: 51 bytes | 15 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495E5] == 0
   2. OR flag [0x495C8] |= 0x4
   3. Set flag [0x495C8] = 13
   4. Check combined flags == 0xF
   5. Trigger statue_secret

<details>
<summary>Raw disassembly (15 instructions)</summary>

```asm
  1C0CB: push     8
  1C0D0: call     0x2a218  ; __STK
  1C0D5: push     edx
  1C0D6: cmp      byte ptr [0x95e5], 0
  1C0DD: je       0x1c0fc
  1C0DF: mov      dl, byte ptr [0x95c8]
  1C0E5: or       dl, 4
  1C0E8: mov      byte ptr [0x95c8], dl
  1C0EE: xor      eax, eax
  1C0F0: mov      al, dl
  1C0F2: cmp      eax, 0xf
  1C0F5: jne      0x1c0fc
  1C0F7: call     0x1c131  ; trigger_statue_secret
  1C0FC: pop      edx
  1C0FD: ret      
```

</details>

### LOOK Extra 438

**Handler:** Ghidra `0x1C0FE` | File `0x202FE` | Size: 51 bytes | 15 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495E5] == 0
   2. OR flag [0x495C8] |= 0x8
   3. Set flag [0x495C8] = 13
   4. Check combined flags == 0xF
   5. Trigger statue_secret

<details>
<summary>Raw disassembly (15 instructions)</summary>

```asm
  1C0FE: push     8
  1C103: call     0x2a218  ; __STK
  1C108: push     edx
  1C109: cmp      byte ptr [0x95e5], 0
  1C110: je       0x1c12f
  1C112: mov      dl, byte ptr [0x95c8]
  1C118: or       dl, 8
  1C11B: mov      byte ptr [0x95c8], dl
  1C121: xor      eax, eax
  1C123: mov      al, dl
  1C125: cmp      eax, 0xf
  1C128: jne      0x1c12f
  1C12A: call     0x1c131  ; trigger_statue_secret
  1C12F: pop      edx
  1C130: ret      
```

</details>

---

## Room 31

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 138 | 222 | 34 | 18 | 443 | Visible |
| 1 | 0x485 | 0x00 | 182 | 222 | 39 | 19 | 444 | Visible |
| 2 | 0x48E | 0x00 | 230 | 222 | 35 | 20 | 445 | Visible |
| 3 | 0x497 | 0x00 | 273 | 229 | 27 | 14 | 446 | Visible |
| 4 | 0x4A0 | 0x00 | 309 | 226 | 22 | 18 | 447 | Visible |
| 5 | 0x4A9 | 0x00 | 341 | 227 | 26 | 13 | 448 | Visible |
| 6 | 0x4B2 | 0x00 | 138 | 246 | 17 | 19 | 449 | Visible |
| 7 | 0x4BB | 0x00 | 170 | 247 | 38 | 25 | 450 | Visible |
| 8 | 0x4C4 | 0x00 | 220 | 247 | 40 | 26 | 451 | Visible |
| 9 | 0x4CD | 0x00 | 269 | 250 | 33 | 24 | 452 | Visible |
| 10 | 0x4D6 | 0x00 | 310 | 251 | 28 | 23 | 453 | Visible |
| 11 | 0x4DF | 0x00 | 350 | 250 | 31 | 24 | 454 | Visible |
| 12 | 0x4E8 | 0x00 | 149 | 281 | 39 | 23 | 455 | Visible |
| 13 | 0x4F1 | 0x00 | 210 | 283 | 47 | 21 | 456 | Visible |
| 14 | 0x4FA | 0x00 | 266 | 282 | 43 | 23 | 457 | Visible |
| 15 | 0x503 | 0x08 | 640 | 400 | 4 | 17 | 101 | Hidden |
| 16 | 0x50C | 0x00 | 275 | 168 | 37 | 24 | 459 | Visible |
| 17 | 0x515 | 0x00 | 324 | 171 | 30 | 30 | 460 | Visible |
| 18 | 0x51E | 0x00 | 394 | 213 | 67 | 58 | 461 | Visible |
| 19 | 0x527 | 0x00 | 220 | 247 | 40 | 26 | 462 | Visible |

### OPEN Extra 462

**Handler:** Ghidra `0x1D0BB` | File `0x212BB` | Size: 179 bytes | 40 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4A774] == 0
   2. Set flag [0x4A774] = 1
   3. Display sticker from ALFRED.6 offset=0x4A447, size=0x1626
   4. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (40 instructions)</summary>

```asm
  1D0BB: push     0x10
  1D0C0: call     0x2a218  ; __STK
  1D0C5: push     ebx
  1D0C6: push     ecx
  1D0C7: push     edx
  1D0C8: cmp      byte ptr [0xa774], 0
  1D0CF: jne      0x1d16e
  1D0D5: mov      byte ptr [0xa774], 1
  1D0DC: mov      edx, 0x1626
  1D0E1: mov      eax, 0x4a447
  1D0E6: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D0EB: mov      eax, dword ptr [0xfac8]
  1D0F0: mov      byte ptr [eax + 0x1c1], 1
  1D0F7: mov      ax, word ptr [0xfb94]
  1D0FD: mov      word ptr [0xfb70], ax
  1D103: mov      word ptr [0xfb72], 0x1c1
  1D10C: mov      dh, 1
  1D10E: mov      byte ptr [0xfb74], dh
  1D114: mov      byte ptr [0xfb75], dh
  1D11A: mov      ecx, dword ptr [0xf914]
  1D120: mov      ebx, 1
  1D125: mov      edx, 6
  1D12A: mov      eax, 0xfb70
  1D12F: call     0x2a6b7  ; write_data_to_alfred1
  1D134: mov      eax, dword ptr [0xfaac]
  1D139: mov      edx, dword ptr [eax + 0x50]
  1D13C: add      edx, 0x1c1
  1D142: mov      eax, dword ptr [0xf8f0]
  1D147: xor      ebx, ebx
  1D149: call     0x2a342  ; file_seek
  1D14E: mov      ecx, dword ptr [0xf8f0]
  1D154: mov      eax, dword ptr [0xfac8]
  1D159: add      eax, 0x1c1
  1D15E: mov      ebx, 1
  1D163: mov      edx, ebx
  1D165: call     0x2a6b7  ; write_data_to_alfred1
  1D16A: pop      edx
  1D16B: pop      ecx
  1D16C: pop      ebx
  1D16D: ret      
```

</details>

### PICKUP Extra 101

**Handler:** Ghidra `0x20682` | File `0x24882` | Size: 160 bytes | 30 instructions | Ends: `jmp`

**Operations:**

   1. HIDE hotspot[15] @0x504 → (640, 400)
   2. JMP → 0x1E808

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x504 | 15 | 101 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (30 instructions)</summary>

```asm
  20682: push     0x10
  20687: call     0x2a218  ; __STK
  2068C: push     ebx
  2068D: push     ecx
  2068E: push     edx
  2068F: mov      eax, dword ptr [0xfac8]
  20694: mov      word ptr [eax + 0x504], 0x280
  2069D: mov      eax, dword ptr [0xfac8]
  206A2: mov      word ptr [eax + 0x506], 0x190
  206AB: mov      ax, word ptr [0xfb94]
  206B1: mov      word ptr [0xfb78], ax
  206B7: mov      word ptr [0xfb7a], 0x504
  206C0: mov      byte ptr [0xfb7c], 4
  206C7: mov      word ptr [0xfb7d], 0x280
  206D0: mov      word ptr [0xfb7f], 0x190
  206D9: mov      ecx, dword ptr [0xf914]
  206DF: mov      ebx, 1
  206E4: mov      edx, 9
  206E9: mov      eax, 0xfb78
  206EE: call     0x2a6b7  ; write_data_to_alfred1
  206F3: mov      eax, dword ptr [0xfaac]
  206F8: mov      edx, dword ptr [eax + 0x50]
  206FB: add      edx, 0x504
  20701: mov      eax, dword ptr [0xf8f0]
  20706: xor      ebx, ebx
  20708: call     0x2a342  ; file_seek
  2070D: mov      ecx, dword ptr [0xf8f0]
  20713: mov      eax, dword ptr [0xfac8]
  20718: add      eax, 0x504
  2071D: jmp      0x1e808
```

</details>

---

## Room 32

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x01 | 382 | 218 | 34 | 39 | 473 | Visible |
| 1 | 0x485 | 0x08 | 382 | 218 | 34 | 39 | 100 | Visible |
| 2 | 0x48E | 0x00 | 179 | 220 | 67 | 67 | 473 | Visible |
| 3 | 0x497 | 0x00 | 130 | 318 | 49 | 32 | 100 | Visible |
| 4 | 0x4A0 | 0x00 | 201 | 106 | 24 | 22 | 473 | Visible |
| 5 | 0x4A9 | 0x00 | 401 | 110 | 22 | 21 | 100 | Visible |
| 6 | 0x4B2 | 0x00 | 487 | 271 | 30 | 29 | 473 | Visible |
| 7 | 0x4BB | 0x00 | 127 | 273 | 31 | 25 | 100 | Visible |
| 8 | 0x4C4 | 0x00 | 232 | 118 | 31 | 97 | 100 | Visible |

### OPEN Extra 473

**Handler:** Ghidra `0x1D266` | File `0x21466` | Size: 182 bytes | 34 instructions | Ends: `jmp`

**Operations:**

   1. Set flag [0x4A800] = 1
   2. Display sticker from ALFRED.6 offset=0x4BA6D, size=0x534
   3. HIDE hotspot[0] @0x47D → (640, 400)
   4. JMP → 0x1E808

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x47D | 0 | 473 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (34 instructions)</summary>

```asm
  1D266: push     0x10
  1D26B: call     0x2a218  ; __STK
  1D270: push     ebx
  1D271: push     ecx
  1D272: push     edx
  1D273: mov      byte ptr [0xa800], 1
  1D27A: mov      edx, 0x534
  1D27F: mov      eax, 0x4ba6d
  1D284: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D289: mov      eax, dword ptr [0xfac8]
  1D28E: mov      word ptr [eax + 0x47d], 0x280
  1D297: mov      eax, dword ptr [0xfac8]
  1D29C: mov      word ptr [eax + 0x47f], 0x190
  1D2A5: mov      ax, word ptr [0xfb94]
  1D2AB: mov      word ptr [0xfb78], ax
  1D2B1: mov      word ptr [0xfb7a], 0x47d
  1D2BA: mov      byte ptr [0xfb7c], 4
  1D2C1: mov      word ptr [0xfb7d], 0x280
  1D2CA: mov      word ptr [0xfb7f], 0x190
  1D2D3: mov      ecx, dword ptr [0xf914]
  1D2D9: mov      ebx, 1
  1D2DE: mov      edx, 9
  1D2E3: mov      eax, 0xfb78
  1D2E8: call     0x2a6b7  ; write_data_to_alfred1
  1D2ED: mov      eax, dword ptr [0xfaac]
  1D2F2: mov      edx, dword ptr [eax + 0x50]
  1D2F5: add      edx, 0x47d
  1D2FB: mov      eax, dword ptr [0xf8f0]
  1D300: xor      ebx, ebx
  1D302: call     0x2a342  ; file_seek
  1D307: mov      ecx, dword ptr [0xf8f0]
  1D30D: mov      eax, dword ptr [0xfac8]
  1D312: add      eax, 0x47d
  1D317: jmp      0x1e808
```

</details>

### PICKUP Extra 100

**Handler:** Ghidra `0x1FCEB` | File `0x23EEB` | Size: 160 bytes | 30 instructions | Ends: `jmp`

**Operations:**

   1. HIDE hotspot[1] @0x486 → (640, 400)
   2. JMP → 0x1E808

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x486 | 1 | 100 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (30 instructions)</summary>

```asm
  1FCEB: push     0x10
  1FCF0: call     0x2a218  ; __STK
  1FCF5: push     ebx
  1FCF6: push     ecx
  1FCF7: push     edx
  1FCF8: mov      eax, dword ptr [0xfac8]
  1FCFD: mov      word ptr [eax + 0x486], 0x280
  1FD06: mov      eax, dword ptr [0xfac8]
  1FD0B: mov      word ptr [eax + 0x488], 0x190
  1FD14: mov      ax, word ptr [0xfb94]
  1FD1A: mov      word ptr [0xfb78], ax
  1FD20: mov      word ptr [0xfb7a], 0x486
  1FD29: mov      byte ptr [0xfb7c], 4
  1FD30: mov      word ptr [0xfb7d], 0x280
  1FD39: mov      word ptr [0xfb7f], 0x190
  1FD42: mov      ecx, dword ptr [0xf914]
  1FD48: mov      ebx, 1
  1FD4D: mov      edx, 9
  1FD52: mov      eax, 0xfb78
  1FD57: call     0x2a6b7  ; write_data_to_alfred1
  1FD5C: mov      eax, dword ptr [0xfaac]
  1FD61: mov      edx, dword ptr [eax + 0x50]
  1FD64: add      edx, 0x486
  1FD6A: mov      eax, dword ptr [0xf8f0]
  1FD6F: xor      ebx, ebx
  1FD71: call     0x2a342  ; file_seek
  1FD76: mov      ecx, dword ptr [0xf8f0]
  1FD7C: mov      eax, dword ptr [0xfac8]
  1FD81: add      eax, 0x486
  1FD86: jmp      0x1e808
```

</details>

---

## Room 33

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x03 | 301 | 83 | 48 | 74 | 465 | Visible |
| 1 | 0x485 | 0x00 | 465 | 203 | 26 | 42 | 650 | Visible |
| 2 | 0x48E | 0x01 | 465 | 203 | 26 | 42 | 651 | Visible |

### OPEN Extra 465

**Handler:** Ghidra `0x1D17C` | File `0x2137C` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4A88C] == 0
   2. Play ambient sound
   3. Set flag [0x4A88C] = 1
   4. Display sticker from ALFRED.6 offset=0x3DEC9, size=0x194A
   5. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1D17C: push     0x2c
  1D181: call     0x2a218  ; __STK
  1D186: push     ebx
  1D187: push     ecx
  1D188: push     edx
  1D189: cmp      byte ptr [0xa88c], 0
  1D190: jne      0x1d258
  1D196: xor      eax, eax
  1D198: mov      al, byte ptr [0x13002]
  1D19D: push     eax
  1D19E: mov      edx, dword ptr [0x13234]
  1D1A4: push     edx
  1D1A5: push     0x20
  1D1A7: push     0x100
  1D1AC: push     0x100
  1D1B1: push     -1
  1D1B3: mov      ebx, dword ptr [0x13204]
  1D1B9: push     ebx
  1D1BA: call     0x27ce1  ; play_ambient_sound
  1D1BF: mov      byte ptr [0xa88c], 1
  1D1C6: mov      edx, 0x194a
  1D1CB: mov      eax, 0x3dec9
  1D1D0: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D1D5: mov      eax, dword ptr [0xfac8]
  1D1DA: mov      byte ptr [eax + 0x1c1], 1
  1D1E1: mov      ax, word ptr [0xfb94]
  1D1E7: mov      word ptr [0xfb70], ax
  1D1ED: mov      word ptr [0xfb72], 0x1c1
  1D1F6: mov      dh, 1
  1D1F8: mov      byte ptr [0xfb74], dh
  1D1FE: mov      byte ptr [0xfb75], dh
  1D204: mov      ecx, dword ptr [0xf914]
  1D20A: mov      ebx, 1
  1D20F: mov      edx, 6
  1D214: mov      eax, 0xfb70
  1D219: call     0x2a6b7  ; write_data_to_alfred1
  1D21E: mov      eax, dword ptr [0xfaac]
  1D223: mov      edx, dword ptr [eax + 0x50]
  1D226: add      edx, 0x1c1
  1D22C: mov      eax, dword ptr [0xf8f0]
  1D231: xor      ebx, ebx
  1D233: call     0x2a342  ; file_seek
  1D238: mov      ecx, dword ptr [0xf8f0]
  1D23E: mov      eax, dword ptr [0xfac8]
  1D243: add      eax, 0x1c1
  1D248: mov      ebx, 1
  1D24D: mov      edx, ebx
  1D24F: call     0x2a6b7  ; write_data_to_alfred1
  1D254: pop      edx
  1D255: pop      ecx
  1D256: pop      ebx
  1D257: ret      
```

</details>

### OPEN Extra 651

**Handler:** Ghidra `0x1D41A` | File `0x2161A` | Size: 293 bytes | 61 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495E7] == 0
   2. Display sticker from ALFRED.6 offset=0x62535, size=0x816
   3. Default verb response ("I can't do that")
   4. Update conversation state (room=26)
   5. Update conversation state (room=26)
   6. Update conversation state (room=27)
   7. Update conversation state (room=27)

<details>
<summary>Raw disassembly (61 instructions)</summary>

```asm
  1D41A: push     0x10
  1D41F: call     0x2a218  ; __STK
  1D424: push     ebx
  1D425: push     ecx
  1D426: push     edx
  1D427: cmp      byte ptr [0x95e7], 0
  1D42E: je       0x1d53f
  1D434: mov      edx, 0x816
  1D439: mov      eax, 0x62535
  1D43E: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D443: mov      edx, dword ptr [0xfac8]
  1D449: mov      word ptr [edx + 0x48f], 0x280
  1D452: mov      edx, dword ptr [0xfac8]
  1D458: mov      word ptr [edx + 0x491], 0x190
  1D461: mov      ax, word ptr [0xfb94]
  1D467: mov      word ptr [0xfb78], ax
  1D46D: mov      word ptr [0xfb7a], 0x48f
  1D476: mov      byte ptr [0xfb7c], 4
  1D47D: mov      word ptr [0xfb7d], 0x280
  1D486: mov      word ptr [0xfb7f], 0x190
  1D48F: mov      ecx, dword ptr [0xf914]
  1D495: mov      ebx, 1
  1D49A: mov      edx, 9
  1D49F: mov      eax, 0xfb78
  1D4A4: call     0x2a6b7  ; write_data_to_alfred1
  1D4A9: mov      edx, dword ptr [0xfaac]
  1D4AF: mov      edx, dword ptr [edx + 0x50]
  1D4B2: add      edx, 0x48f
  1D4B8: mov      eax, dword ptr [0xf8f0]
  1D4BD: xor      ebx, ebx
  1D4BF: call     0x2a342  ; file_seek
  1D4C4: mov      ecx, dword ptr [0xf8f0]
  1D4CA: mov      eax, dword ptr [0xfac8]
  1D4CF: add      eax, 0x48f
  1D4D4: mov      ebx, 1
  1D4D9: mov      edx, 4
  1D4DE: call     0x2a6b7  ; write_data_to_alfred1
  1D4E3: mov      eax, dword ptr [0xbb64]
  1D4E8: call     0x25487  ; default_verb_response
  1D4ED: mov      eax, 0x52
  1D4F2: call     0x24157
  1D4F7: mov      ebx, 1
  1D4FC: xor      edx, edx
  1D4FE: mov      eax, 0x1a
  1D503: call     0x1b666  ; update_conversation_state
  1D508: mov      ebx, 1
  1D50D: mov      edx, ebx
  1D50F: mov      eax, 0x1a
  1D514: call     0x1b666  ; update_conversation_state
  1D519: mov      ebx, 1
  1D51E: xor      edx, edx
  1D520: mov      eax, 0x1b
  1D525: call     0x1b666  ; update_conversation_state
  1D52A: mov      ebx, 1
  1D52F: mov      edx, ebx
  1D531: mov      eax, 0x1b
  1D536: call     0x1b666  ; update_conversation_state
  1D53B: pop      edx
  1D53C: pop      ecx
  1D53D: pop      ebx
  1D53E: ret      
```

</details>

### PULL Extra 465

**Handler:** Ghidra `0x1E181` | File `0x22381` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4A88C] == 0
   2. Play ambient sound
   3. Set flag [0x4A88C] = 13
   4. Display sticker from ALFRED.6 offset=0x3F813, size=0x194A
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1E181: push     0x2c
  1E186: call     0x2a218  ; __STK
  1E18B: push     ebx
  1E18C: push     ecx
  1E18D: push     edx
  1E18E: cmp      byte ptr [0xa88c], 0
  1E195: je       0x1e25f
  1E19B: xor      eax, eax
  1E19D: mov      al, byte ptr [0x13002]
  1E1A2: push     eax
  1E1A3: mov      edx, dword ptr [0x13238]
  1E1A9: push     edx
  1E1AA: push     0x20
  1E1AC: push     0x100
  1E1B1: push     0x100
  1E1B6: push     -1
  1E1B8: mov      ebx, dword ptr [0x13204]
  1E1BE: push     ebx
  1E1BF: call     0x27ce1  ; play_ambient_sound
  1E1C4: xor      dl, dl
  1E1C6: mov      byte ptr [0xa88c], dl
  1E1CC: mov      edx, 0x194a
  1E1D1: mov      eax, 0x3f813
  1E1D6: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1E1DB: mov      eax, dword ptr [0xfac8]
  1E1E0: mov      byte ptr [eax + 0x1c1], 0
  1E1E7: mov      ax, word ptr [0xfb94]
  1E1ED: mov      word ptr [0xfb70], ax
  1E1F3: mov      word ptr [0xfb72], 0x1c1
  1E1FC: mov      byte ptr [0xfb74], 1
  1E203: xor      bl, bl
  1E205: mov      byte ptr [0xfb75], bl
  1E20B: mov      ecx, dword ptr [0xf914]
  1E211: mov      ebx, 1
  1E216: mov      edx, 6
  1E21B: mov      eax, 0xfb70
  1E220: call     0x2a6b7  ; write_data_to_alfred1
  1E225: mov      eax, dword ptr [0xfaac]
  1E22A: mov      edx, dword ptr [eax + 0x50]
  1E22D: add      edx, 0x1c1
  1E233: mov      eax, dword ptr [0xf8f0]
  1E238: xor      ebx, ebx
  1E23A: call     0x2a342  ; file_seek
  1E23F: mov      ecx, dword ptr [0xf8f0]
  1E245: mov      eax, dword ptr [0xfac8]
  1E24A: add      eax, 0x1c1
  1E24F: mov      ebx, 1
  1E254: mov      edx, ebx
  1E256: call     0x2a6b7  ; write_data_to_alfred1
  1E25B: pop      edx
  1E25C: pop      ecx
  1E25D: pop      ebx
  1E25E: ret      
```

</details>

---

## Room 37

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 391 | 262 | 12 | 16 | 90 | Visible |
| 1 | 0x485 | 0x00 | 188 | 217 | 50 | 40 | 502 | Visible |
| 2 | 0x48E | 0x00 | 246 | 211 | 44 | 35 | 502 | Visible |
| 3 | 0x497 | 0x00 | 293 | 208 | 40 | 27 | 502 | Visible |
| 4 | 0x4A0 | 0x00 | 338 | 204 | 36 | 23 | 502 | Visible |
| 5 | 0x4A9 | 0x00 | 379 | 200 | 30 | 17 | 502 | Visible |
| 6 | 0x4B2 | 0x00 | 413 | 198 | 21 | 15 | 502 | Visible |
| 7 | 0x4BB | 0x00 | 441 | 195 | 15 | 11 | 502 | Visible |
| 8 | 0x4C4 | 0x00 | 437 | 220 | 26 | 29 | 502 | Visible |
| 9 | 0x4CD | 0x00 | 405 | 227 | 29 | 34 | 502 | Visible |
| 10 | 0x4D6 | 0x00 | 341 | 246 | 44 | 40 | 502 | Visible |
| 11 | 0x4DF | 0x00 | 287 | 256 | 52 | 28 | 502 | Visible |
| 12 | 0x4E8 | 0x00 | 192 | 274 | 87 | 50 | 502 | Visible |

### PICKUP Extra 90

**Handler:** Ghidra `0x2044F` | File `0x2464F` | Size: 125 bytes | 25 instructions | Ends: `jmp`

**Operations:**

   1. Display sticker from ALFRED.6 offset=0x6C2C9, size=0x584
   2. Set flag [0x5176A] = 10
   3. Set flag [0x4961D] = 10
   4. Set flag [0x4964F] = 13
   5. Default verb response ("I can't do that")
   6. Default verb response ("I can't do that")
   7. Set flag [0x4FB9A] = 2
   8. Default verb response ("I can't do that")
   9. JMP → 0x11662

<details>
<summary>Raw disassembly (25 instructions)</summary>

```asm
  2044F: push     8
  20454: call     0x2a218  ; __STK
  20459: push     edx
  2045A: mov      edx, 0x584
  2045F: mov      eax, 0x6c2c9
  20464: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  20469: mov      ah, 1
  2046B: mov      byte ptr [0x1176a], ah
  20471: mov      byte ptr [0x961d], ah
  20477: mov      dh, byte ptr [0x964f]
  2047D: add      dh, ah
  2047F: mov      byte ptr [0x964f], dh
  20485: xor      eax, eax
  20487: mov      al, dh
  20489: mov      eax, dword ptr [eax*4 + 0xbc64]
  20490: call     0x25487  ; default_verb_response
  20495: call     0x26fab
  2049A: mov      eax, dword ptr [0xbafc]
  2049F: call     0x25487  ; default_verb_response
  204A4: mov      byte ptr [0xfb9a], 2
  204AB: mov      eax, dword ptr [0xbaf8]
  204B0: call     0x25487  ; default_verb_response
  204B5: mov      word ptr [0xfb9c], 0x250
  204BE: mov      word ptr [0xfb9e], 0x132
  204C7: jmp      0x11662
```

</details>

---

## Room 38

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 399 | 222 | 9 | 8 | 443 | Visible |
| 1 | 0x485 | 0x00 | 422 | 225 | 12 | 5 | 444 | Visible |
| 2 | 0x48E | 0x00 | 415 | 231 | 27 | 5 | 445 | Visible |
| 3 | 0x497 | 0x08 | 435 | 226 | 6 | 4 | 99 | Visible |
| 4 | 0x4A0 | 0x00 | 322 | 224 | 75 | 12 | 447 | Visible |
| 5 | 0x4A9 | 0x08 | 435 | 226 | 6 | 4 | 81 | Visible |

### PICKUP Extra 81

**Handler:** Ghidra `0x1FC2D` | File `0x23E2D` | Size: 190 bytes | 36 instructions | Ends: `jmp`

**Operations:**

   1. Default verb response ("I can't do that")
   2. HIDE hotspot[5] @0x4AA → (640, 400)
   3. JMP → 0x1E808

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x4AA | 5 | 81 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (36 instructions)</summary>

```asm
  1FC2D: push     0x10
  1FC32: call     0x2a218  ; __STK
  1FC37: push     ebx
  1FC38: push     ecx
  1FC39: push     edx
  1FC3A: inc      byte ptr [0x964f]
  1FC40: xor      eax, eax
  1FC42: mov      al, byte ptr [0x964f]
  1FC47: mov      eax, dword ptr [eax*4 + 0xbc64]
  1FC4E: call     0x25487  ; default_verb_response
  1FC53: call     0x26fab
  1FC58: mov      eax, dword ptr [0xfac8]
  1FC5D: mov      word ptr [eax + 0x4aa], 0x280
  1FC66: mov      eax, dword ptr [0xfac8]
  1FC6B: mov      word ptr [eax + 0x4ac], 0x190
  1FC74: mov      ax, word ptr [0xfb94]
  1FC7A: mov      word ptr [0xfb78], ax
  1FC80: mov      word ptr [0xfb7a], 0x498
  1FC89: mov      byte ptr [0xfb7c], 4
  1FC90: mov      word ptr [0xfb7d], 0x280
  1FC99: mov      word ptr [0xfb7f], 0x190
  1FCA2: mov      ecx, dword ptr [0xf914]
  1FCA8: mov      ebx, 1
  1FCAD: mov      edx, 9
  1FCB2: mov      eax, 0xfb78
  1FCB7: call     0x2a6b7  ; write_data_to_alfred1
  1FCBC: mov      eax, dword ptr [0xfaac]
  1FCC1: mov      edx, dword ptr [eax + 0x50]
  1FCC4: add      edx, 0x498
  1FCCA: mov      eax, dword ptr [0xf8f0]
  1FCCF: xor      ebx, ebx
  1FCD1: call     0x2a342  ; file_seek
  1FCD6: mov      ecx, dword ptr [0xf8f0]
  1FCDC: mov      eax, dword ptr [0xfac8]
  1FCE1: add      eax, 0x4aa
  1FCE6: jmp      0x1e808
```

</details>

### PICKUP Extra 99

**Handler:** Ghidra `0x205FE` | File `0x247FE` | Size: 132 bytes | 24 instructions | Ends: `jmp`

**Operations:**

   1. HIDE hotspot[3] @0x498 → (640, 400)
   2. JMP → 0x1E7EC

**Hotspot Move Details:**

| Offset | Hotspot Idx | Extra | New X | New Y | Action |
|--------|-------------|-------|-------|-------|--------|
| 0x498 | 3 | 99 | 640 | 400 | HIDE |

<details>
<summary>Raw disassembly (24 instructions)</summary>

```asm
  205FE: push     0x10
  20603: call     0x2a218  ; __STK
  20608: push     ebx
  20609: push     ecx
  2060A: push     edx
  2060B: mov      eax, dword ptr [0xfac8]
  20610: mov      word ptr [eax + 0x498], 0x280
  20619: mov      eax, dword ptr [0xfac8]
  2061E: mov      word ptr [eax + 0x49a], 0x190
  20627: mov      ax, word ptr [0xfb94]
  2062D: mov      word ptr [0xfb78], ax
  20633: mov      word ptr [0xfb7a], 0x4aa
  2063C: mov      byte ptr [0xfb7c], 4
  20643: mov      word ptr [0xfb7d], 0x280
  2064C: mov      word ptr [0xfb7f], 0x190
  20655: mov      ecx, dword ptr [0xf914]
  2065B: mov      ebx, 1
  20660: mov      edx, 9
  20665: mov      eax, 0xfb78
  2066A: call     0x2a6b7  ; write_data_to_alfred1
  2066F: mov      eax, dword ptr [0xfaac]
  20674: mov      edx, dword ptr [eax + 0x50]
  20677: add      edx, 0x4aa
  2067D: jmp      0x1e7ec
```

</details>

---

## Room 42

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x08 | 38 | 326 | 33 | 23 | 605 | Visible |
| 1 | 0x485 | 0x08 | 265 | 280 | 18 | 11 | 606 | Visible |
| 2 | 0x48E | 0x08 | 471 | 310 | 33 | 23 | 607 | Visible |
| 3 | 0x497 | 0x08 | 551 | 380 | 88 | 19 | 608 | Visible |

### PICKUP Extra 605

**Handler:** Ghidra `0x204CC` | File `0x246CC` | Size: 34 bytes | 8 instructions | Ends: `jmp`

**Shares handler with:** PICKUP extra 606, PICKUP extra 607

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (8 instructions)</summary>

```asm
  204CC: push     4
  204D1: call     0x2a218  ; __STK
  204D6: mov      eax, 0x5b
  204DB: call     0x1badf
  204E0: test     al, al
  204E2: je       0x204ee
  204E4: mov      eax, dword ptr [0xbb14]
  204E9: jmp      0x25487
```

</details>

### PICKUP Extra 606

**Handler:** Ghidra `0x204CC` | File `0x246CC` | Size: 34 bytes | 8 instructions | Ends: `jmp`

**Shares handler with:** PICKUP extra 605, PICKUP extra 607

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (8 instructions)</summary>

```asm
  204CC: push     4
  204D1: call     0x2a218  ; __STK
  204D6: mov      eax, 0x5b
  204DB: call     0x1badf
  204E0: test     al, al
  204E2: je       0x204ee
  204E4: mov      eax, dword ptr [0xbb14]
  204E9: jmp      0x25487
```

</details>

### PICKUP Extra 607

**Handler:** Ghidra `0x204CC` | File `0x246CC` | Size: 34 bytes | 8 instructions | Ends: `jmp`

**Shares handler with:** PICKUP extra 605, PICKUP extra 606

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (8 instructions)</summary>

```asm
  204CC: push     4
  204D1: call     0x2a218  ; __STK
  204D6: mov      eax, 0x5b
  204DB: call     0x1badf
  204E0: test     al, al
  204E2: je       0x204ee
  204E4: mov      eax, dword ptr [0xbb14]
  204E9: jmp      0x25487
```

</details>

### PICKUP Extra 608

**Handler:** Ghidra `0x20528` | File `0x24728` | Size: 32 bytes | 9 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x495D4] == 0
   2. Default verb response ("I can't do that")

<details>
<summary>Raw disassembly (9 instructions)</summary>

```asm
  20528: push     8
  2052D: call     0x2a218  ; __STK
  20532: push     edx
  20533: cmp      byte ptr [0x95d4], 0
  2053A: jne      0x20548
  2053C: mov      eax, dword ptr [0xbb1c]
  20541: call     0x25487  ; default_verb_response
  20546: pop      edx
  20547: ret      
```

</details>

---

## Room 46

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 124 | 75 | 54 | 155 | 619 | Visible |
| 1 | 0x485 | 0x00 | 375 | 76 | 54 | 150 | 620 | Visible |
| 2 | 0x48E | 0x03 | 533 | 117 | 81 | 226 | 621 | Visible |

### OPEN Extra 621

**Handler:** Ghidra `0x1D330` | File `0x21530` | Size: 220 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4AFA8] == 0
   2. Play ambient sound
   3. Set flag [0x4AFA8] = 1
   4. Display sticker from ALFRED.6 offset=0x75454, size=0x3D86
   5. Set room_data[0x1DD] = 1

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1D330: push     0x2c
  1D335: call     0x2a218  ; __STK
  1D33A: push     ebx
  1D33B: push     ecx
  1D33C: push     edx
  1D33D: cmp      byte ptr [0xafa8], 0
  1D344: jne      0x1d40c
  1D34A: xor      eax, eax
  1D34C: mov      al, byte ptr [0x13002]
  1D351: push     eax
  1D352: mov      edx, dword ptr [0x13234]
  1D358: push     edx
  1D359: push     0x20
  1D35B: push     0x100
  1D360: push     0x100
  1D365: push     -1
  1D367: mov      ebx, dword ptr [0x13204]
  1D36D: push     ebx
  1D36E: call     0x27ce1  ; play_ambient_sound
  1D373: mov      byte ptr [0xafa8], 1
  1D37A: mov      edx, 0x3d86
  1D37F: mov      eax, 0x75454
  1D384: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D389: mov      eax, dword ptr [0xfac8]
  1D38E: mov      byte ptr [eax + 0x1dd], 1
  1D395: mov      ax, word ptr [0xfb94]
  1D39B: mov      word ptr [0xfb70], ax
  1D3A1: mov      word ptr [0xfb72], 0x1dd
  1D3AA: mov      dh, 1
  1D3AC: mov      byte ptr [0xfb74], dh
  1D3B2: mov      byte ptr [0xfb75], dh
  1D3B8: mov      ecx, dword ptr [0xf914]
  1D3BE: mov      ebx, 1
  1D3C3: mov      edx, 6
  1D3C8: mov      eax, 0xfb70
  1D3CD: call     0x2a6b7  ; write_data_to_alfred1
  1D3D2: mov      eax, dword ptr [0xfaac]
  1D3D7: mov      edx, dword ptr [eax + 0x50]
  1D3DA: add      edx, 0x1dd
  1D3E0: mov      eax, dword ptr [0xf8f0]
  1D3E5: xor      ebx, ebx
  1D3E7: call     0x2a342  ; file_seek
  1D3EC: mov      ecx, dword ptr [0xf8f0]
  1D3F2: mov      eax, dword ptr [0xfac8]
  1D3F7: add      eax, 0x1dd
  1D3FC: mov      ebx, 1
  1D401: mov      edx, ebx
  1D403: call     0x2a6b7  ; write_data_to_alfred1
  1D408: pop      edx
  1D409: pop      ecx
  1D40A: pop      ebx
  1D40B: ret      
```

</details>

### PULL Extra 621

**Handler:** Ghidra `0x1E26D` | File `0x2246D` | Size: 222 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4AFA8] == 0
   2. Play ambient sound
   3. Set flag [0x4AFA8] = 13
   4. Display sticker from ALFRED.6 offset=0x791DA, size=0x3D86
   5. Set room_data[0x1DD] = 0

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1E26D: push     0x2c
  1E272: call     0x2a218  ; __STK
  1E277: push     ebx
  1E278: push     ecx
  1E279: push     edx
  1E27A: cmp      byte ptr [0xafa8], 0
  1E281: je       0x1e34b
  1E287: xor      eax, eax
  1E289: mov      al, byte ptr [0x13002]
  1E28E: push     eax
  1E28F: mov      edx, dword ptr [0x13238]
  1E295: push     edx
  1E296: push     0x20
  1E298: push     0x100
  1E29D: push     0x100
  1E2A2: push     -1
  1E2A4: mov      ebx, dword ptr [0x13204]
  1E2AA: push     ebx
  1E2AB: call     0x27ce1  ; play_ambient_sound
  1E2B0: xor      dl, dl
  1E2B2: mov      byte ptr [0xafa8], dl
  1E2B8: mov      edx, 0x3d86
  1E2BD: mov      eax, 0x791da
  1E2C2: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1E2C7: mov      eax, dword ptr [0xfac8]
  1E2CC: mov      byte ptr [eax + 0x1dd], 0
  1E2D3: mov      ax, word ptr [0xfb94]
  1E2D9: mov      word ptr [0xfb70], ax
  1E2DF: mov      word ptr [0xfb72], 0x1dd
  1E2E8: mov      byte ptr [0xfb74], 1
  1E2EF: xor      bl, bl
  1E2F1: mov      byte ptr [0xfb75], bl
  1E2F7: mov      ecx, dword ptr [0xf914]
  1E2FD: mov      ebx, 1
  1E302: mov      edx, 6
  1E307: mov      eax, 0xfb70
  1E30C: call     0x2a6b7  ; write_data_to_alfred1
  1E311: mov      eax, dword ptr [0xfaac]
  1E316: mov      edx, dword ptr [eax + 0x50]
  1E319: add      edx, 0x1dd
  1E31F: mov      eax, dword ptr [0xf8f0]
  1E324: xor      ebx, ebx
  1E326: call     0x2a342  ; file_seek
  1E32B: mov      ecx, dword ptr [0xf8f0]
  1E331: mov      eax, dword ptr [0xfac8]
  1E336: add      eax, 0x1dd
  1E33B: mov      ebx, 1
  1E340: mov      edx, ebx
  1E342: call     0x2a6b7  ; write_data_to_alfred1
  1E347: pop      edx
  1E348: pop      ecx
  1E349: pop      ebx
  1E34A: ret      
```

</details>

---

## Room 47

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 365 | 113 | 58 | 41 | 623 | Visible |
| 1 | 0x485 | 0x00 | 431 | 110 | 67 | 44 | 624 | Visible |
| 2 | 0x48E | 0x00 | 505 | 109 | 60 | 45 | 625 | Visible |
| 3 | 0x497 | 0x00 | 363 | 162 | 60 | 58 | 626 | Visible |
| 4 | 0x4A0 | 0x00 | 45 | 236 | 51 | 65 | 627 | Visible |
| 5 | 0x4A9 | 0x00 | 221 | 202 | 50 | 56 | 628 | Visible |
| 6 | 0x4B2 | 0x00 | 278 | 152 | 60 | 71 | 629 | Visible |
| 7 | 0x4BB | 0x00 | 431 | 162 | 66 | 58 | 622 | Visible |
| 8 | 0x4C4 | 0x00 | 507 | 162 | 60 | 58 | 629 | Visible |
| 9 | 0x4CD | 0x03 | 104 | 174 | 62 | 104 | 800 | Visible |

### OPEN Extra 800

**Handler:** Ghidra `0x1D54D` | File `0x2174D` | Size: 221 bytes | 53 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4B034] == 0
   2. Play ambient sound
   3. Set flag [0x4B034] = 13
   4. Display sticker from ALFRED.6 offset=0x62D4B, size=0x21C6
   5. Set room_data[0x1C1] = 1

<details>
<summary>Raw disassembly (53 instructions)</summary>

```asm
  1D54D: push     0x2c
  1D552: call     0x2a218  ; __STK
  1D557: push     ebx
  1D558: push     ecx
  1D559: push     edx
  1D55A: cmp      byte ptr [0xb034], 0
  1D561: je       0x1d62a
  1D567: xor      eax, eax
  1D569: mov      al, byte ptr [0x13002]
  1D56E: push     eax
  1D56F: mov      edx, dword ptr [0x13234]
  1D575: push     edx
  1D576: push     0x20
  1D578: push     0x100
  1D57D: push     0x100
  1D582: push     -1
  1D584: mov      ebx, dword ptr [0x13204]
  1D58A: push     ebx
  1D58B: call     0x27ce1  ; play_ambient_sound
  1D590: xor      dl, dl
  1D592: mov      byte ptr [0xb034], dl
  1D598: mov      edx, 0x21c6
  1D59D: mov      eax, 0x62d4b
  1D5A2: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1D5A7: mov      eax, dword ptr [0xfac8]
  1D5AC: mov      byte ptr [eax + 0x1c1], 1
  1D5B3: mov      ax, word ptr [0xfb94]
  1D5B9: mov      word ptr [0xfb70], ax
  1D5BF: mov      word ptr [0xfb72], 0x1c1
  1D5C8: mov      dh, 1
  1D5CA: mov      byte ptr [0xfb74], dh
  1D5D0: mov      byte ptr [0xfb75], dh
  1D5D6: mov      ecx, dword ptr [0xf914]
  1D5DC: mov      ebx, 1
  1D5E1: mov      edx, 6
  1D5E6: mov      eax, 0xfb70
  1D5EB: call     0x2a6b7  ; write_data_to_alfred1
  1D5F0: mov      eax, dword ptr [0xfaac]
  1D5F5: mov      edx, dword ptr [eax + 0x50]
  1D5F8: add      edx, 0x1c1
  1D5FE: mov      eax, dword ptr [0xf8f0]
  1D603: xor      ebx, ebx
  1D605: call     0x2a342  ; file_seek
  1D60A: mov      ecx, dword ptr [0xf8f0]
  1D610: mov      eax, dword ptr [0xfac8]
  1D615: add      eax, 0x1c1
  1D61A: mov      ebx, 1
  1D61F: mov      edx, ebx
  1D621: call     0x2a6b7  ; write_data_to_alfred1
  1D626: pop      edx
  1D627: pop      ecx
  1D628: pop      ebx
  1D629: ret      
```

</details>

### PULL Extra 800

**Handler:** Ghidra `0x1E359` | File `0x22559` | Size: 221 bytes | 52 instructions | Ends: `ret`

**Operations:**

   1. Check flag [0x4B034] == 0
   2. Play ambient sound
   3. Set flag [0x4B034] = 1
   4. Display sticker from ALFRED.6 offset=0x64F11, size=0x21C6
   5. Set room_data[0x1C1] = 0

<details>
<summary>Raw disassembly (52 instructions)</summary>

```asm
  1E359: push     0x2c
  1E35E: call     0x2a218  ; __STK
  1E363: push     ebx
  1E364: push     ecx
  1E365: push     edx
  1E366: cmp      byte ptr [0xb034], 0
  1E36D: jne      0x1e436
  1E373: xor      eax, eax
  1E375: mov      al, byte ptr [0x13002]
  1E37A: push     eax
  1E37B: mov      edx, dword ptr [0x13238]
  1E381: push     edx
  1E382: push     0x20
  1E384: push     0x100
  1E389: push     0x100
  1E38E: push     -1
  1E390: mov      ebx, dword ptr [0x13204]
  1E396: push     ebx
  1E397: call     0x27ce1  ; play_ambient_sound
  1E39C: mov      byte ptr [0xb034], 1
  1E3A3: mov      edx, 0x21c6
  1E3A8: mov      eax, 0x64f11
  1E3AD: call     0x1ba45  ; load_and_render_sticker_from_alfred6
  1E3B2: mov      eax, dword ptr [0xfac8]
  1E3B7: mov      byte ptr [eax + 0x1c1], 0
  1E3BE: mov      ax, word ptr [0xfb94]
  1E3C4: mov      word ptr [0xfb70], ax
  1E3CA: mov      word ptr [0xfb72], 0x1c1
  1E3D3: mov      byte ptr [0xfb74], 1
  1E3DA: xor      bl, bl
  1E3DC: mov      byte ptr [0xfb75], bl
  1E3E2: mov      ecx, dword ptr [0xf914]
  1E3E8: mov      ebx, 1
  1E3ED: mov      edx, 6
  1E3F2: mov      eax, 0xfb70
  1E3F7: call     0x2a6b7  ; write_data_to_alfred1
  1E3FC: mov      eax, dword ptr [0xfaac]
  1E401: mov      edx, dword ptr [eax + 0x50]
  1E404: add      edx, 0x1c1
  1E40A: mov      eax, dword ptr [0xf8f0]
  1E40F: xor      ebx, ebx
  1E411: call     0x2a342  ; file_seek
  1E416: mov      ecx, dword ptr [0xf8f0]
  1E41C: mov      eax, dword ptr [0xfac8]
  1E421: add      eax, 0x1c1
  1E426: mov      ebx, 1
  1E42B: mov      edx, ebx
  1E42D: call     0x2a6b7  ; write_data_to_alfred1
  1E432: pop      edx
  1E433: pop      ecx
  1E434: pop      ebx
  1E435: ret      
```

</details>

### PICKUP Extra 628

**Handler:** Ghidra `0x20566` | File `0x24766` | Size: 152 bytes | 32 instructions | Ends: `jmp`

**Operations:**

   1. JMP → 0x1E812

<details>
<summary>Raw disassembly (32 instructions)</summary>

```asm
  20566: push     0x10
  2056B: call     0x2a218  ; __STK
  20570: push     ebx
  20571: push     ecx
  20572: push     edx
  20573: mov      eax, 0x62
  20578: call     0x24157
  2057D: mov      edx, dword ptr [0xfac8]
  20583: mov      byte ptr [edx + 0x4a9], 0
  2058A: mov      ax, word ptr [0xfb94]
  20590: mov      word ptr [0xfb70], ax
  20596: mov      word ptr [0xfb72], 0x4a9
  2059F: mov      ah, 1
  205A1: mov      byte ptr [0xfb74], ah
  205A7: mov      byte ptr [0xfb75], ah
  205AD: mov      ecx, dword ptr [0xf914]
  205B3: mov      ebx, 1
  205B8: mov      edx, 6
  205BD: mov      eax, 0xfb70
  205C2: call     0x2a6b7  ; write_data_to_alfred1
  205C7: mov      edx, dword ptr [0xfaac]
  205CD: mov      edx, dword ptr [edx + 0x50]
  205D0: add      edx, 0x4a9
  205D6: mov      eax, dword ptr [0xf8f0]
  205DB: xor      ebx, ebx
  205DD: call     0x2a342  ; file_seek
  205E2: mov      ecx, dword ptr [0xf8f0]
  205E8: mov      eax, dword ptr [0xfac8]
  205ED: add      eax, 0x4a9
  205F2: mov      ebx, 1
  205F7: mov      edx, ebx
  205F9: jmp      0x1e812
```

</details>

---

## Room 55

### Hotspot Data (from ALFRED.1)

| Idx | Offset | Type | X | Y | W | H | Extra | State |
|-----|--------|------|---|---|---|---|-------|-------|
| 0 | 0x47C | 0x00 | 640 | 400 | 2 | 2 | 613 | Hidden |

### OPEN Extra 613

**Handler:** Ghidra `0x1D31C` | File `0x2151C` | Size: 20 bytes | 4 instructions | Ends: `jmp`

**Operations:**

   1. JMP → default_verb_response

<details>
<summary>Raw disassembly (4 instructions)</summary>

```asm
  1D31C: push     4
  1D321: call     0x2a218  ; __STK
  1D326: mov      eax, dword ptr [0xbb24]
  1D32B: jmp      0x25487
```

</details>
