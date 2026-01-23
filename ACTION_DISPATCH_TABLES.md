# Action Dispatch Tables Extracted from JUEGO.EXE

## Overview

This document contains all action dispatch tables extracted from the game executable.
Each table maps hotspot 'extra' IDs to handler function addresses.

## Action System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ACTION FLOW                             │
├─────────────────────────────────────────────────────────────┤
│ 1. Player clicks hotspot                                    │
│    └─> hotspot's extra_id saved to current_hotspot_extra_id │
│                                                             │
│ 2. Available verbs shown (based on action_flags bitmask):   │
│    ├─ Bit 0 (0x01): OPEN                                    │
│    ├─ Bit 1 (0x02): CLOSE                                   │
│    ├─ Bit 2 (0x04): UNKNOWN                                 │
│    ├─ Bit 3 (0x08): PICKUP                                  │
│    ├─ Bit 4 (0x10): TALK                                    │
│    ├─ Bit 5 (0x20): PUSH                                    │
│    └─ Bit 7 (0x80): PULL                                    │
│    (LOOK is always available implicitly)                    │
│                                                             │
│ 3. Player selects verb -> dispatcher routes by verb code:  │
│    ├─ 0x01 OPEN  -> search table at 0x47D24                 │
│    ├─ 0x02 TALK  -> handle_conversation_tree()              │
│    ├─ 0x08 CLOSE -> handle_dialog_interaction()             │
│    ├─ 0x10 LOOK  -> search table at 0x47BF0                 │
│    ├─ 0x20 PUSH  -> search table at 0x47C10                 │
│    ├─ 0x40 ???   -> search table at 0x47C18                 │
│    ├─ 0x80 PULL  -> search table at 0x47CBC                 │
│    └─ 0x200 ITEM -> search table at 0x48118                 │
│                                                             │
│ 4. Dispatcher searches table for matching extra_id          │
│    └─> Calls associated handler function                    │
└─────────────────────────────────────────────────────────────┘
```

## Standard Dispatch Tables (6 bytes/entry)

Format: `[uint16 extra_id][uint32 function_ptr]`, terminated by 0xFFFF

### Table 1 at file offset 0x4AFF0

**14 entries**

| Extra ID | Function | Room/Context |
|----------|----------|-------------|
| 87 | 0x1030C | Inventory/Special (87) |
| 88 | 0x1032F | Inventory/Special (88) |
| 89 | 0x10357 | Inventory/Special (89) |
| 90 | 0x1044F | Inventory/Special (90) |
| 605 | 0x104CC | Room 17-20 |
| 606 | 0x104CC | Room 17-20 |
| 607 | 0x104CC | Room 17-20 |
| 608 | 0x10528 | Room 17-20 |
| 628 | 0x10566 | Room 17-20 |
| 99 | 0x105FE | Inventory/Special (99) |
| 101 | 0x10682 | Room 0 |
| 112 | 0x1037A | Room 0 |
| 700 | 0x10781 | Room 26-35 |
| 308 | 0x10C17 | Room 3-4 (Shop/Alley) |

### Table 2 at file offset 0x4B058

**116 entries**

| Extra ID | Function | Room/Context |
|----------|----------|-------------|
| 257 | 0x10C76 | Room 7 |
| 258 | 0x10D04 | Room 7 |
| 259 | 0x10D28 | Room 7 |
| 260 | 0x10D50 | Room 0 (Alfred's Bedroom) |
| 261 | 0x10D76 | Room 0 (Alfred's Bedroom) |
| 262 | 0x10D89 | Room 0 (Alfred's Bedroom) |
| 263 | 0x10D9C | Room 0 (Alfred's Bedroom) |
| 264 | 0x10DAF | Room 0 (Alfred's Bedroom) |
| 267 | 0x10DCC | Room 0 (Alfred's Bedroom) |
| 268 | 0x10E18 | Room 0 (Alfred's Bedroom) |
| 270 | 0x10E2E | Room 0 (Alfred's Bedroom) |
| 271 | 0x11221 | Room 0 (Alfred's Bedroom) |
| 272 | 0x11237 | Room 0 (Alfred's Bedroom) |
| 273 | 0x11254 | Room 0 (Alfred's Bedroom) |
| 274 | 0x113BB | Room 0 (Alfred's Bedroom) |
| 275 | 0x113DB | Room 0 (Alfred's Bedroom) |
| 276 | 0x113EE | Room 0 (Alfred's Bedroom) |
| 277 | 0x11401 | Room 0 (Alfred's Bedroom) |
| 278 | 0x1142F | Room 0 (Alfred's Bedroom) |
| 279 | 0x11449 | Room 0 (Alfred's Bedroom) |
| 280 | 0x114DB | Room 1-2 (Streets) |
| 281 | 0x114F1 | Room 1-2 (Streets) |
| 282 | 0x11507 | Room 1-2 (Streets) |
| 285 | 0x1151D | Room 1-2 (Streets) |
| 286 | 0x11787 | Room 1-2 (Streets) |
| 287 | 0x117B1 | Room 1-2 (Streets) |
| 288 | 0x117FA | Room 1-2 (Streets) |
| 289 | 0x11839 | Room 1-2 (Streets) |
| 290 | 0x11882 | Room 3-4 (Shop/Alley) |
| 291 | 0x1151D | Room 3-4 (Shop/Alley) |
| 292 | 0x1161D | Room 3-4 (Shop/Alley) |
| 293 | 0x1163A | Room 3-4 (Shop/Alley) |
| 294 | 0x116F5 | Room 3-4 (Shop/Alley) |
| 295 | 0x118CC | Room 3-4 (Shop/Alley) |
| 296 | 0x118F3 | Room 3-4 (Shop/Alley) |
| 297 | 0x11910 | Room 3-4 (Shop/Alley) |
| 298 | 0x119A8 | Room 3-4 (Shop/Alley) |
| 299 | 0x119D4 | Room 3-4 (Shop/Alley) |
| 300 | 0x119FB | Room 3-4 (Shop/Alley) |
| 301 | 0x11A18 | Room 3-4 (Shop/Alley) |
| 302 | 0x11A2B | Room 3-4 (Shop/Alley) |
| 303 | 0x11A3E | Room 3-4 (Shop/Alley) |
| 304 | 0x11A51 | Room 3-4 (Shop/Alley) |
| 305 | 0x11A64 | Room 3-4 (Shop/Alley) |
| 306 | 0x11A77 | Room 3-4 (Shop/Alley) |
| 307 | 0x11A8A | Room 3-4 (Shop/Alley) |
| 308 | 0x11B11 | Room 3-4 (Shop/Alley) |
| 313 | 0x11B34 | Room 3-4 (Shop/Alley) |
| 314 | 0x11B4E | Room 3-4 (Shop/Alley) |
| 316 | 0x11B62 | Room 3-4 (Shop/Alley) |
| 317 | 0x11B76 | Room 3-4 (Shop/Alley) |
| 318 | 0x11B8A | Room 3-4 (Shop/Alley) |
| 319 | 0x11B9E | Room 3-4 (Shop/Alley) |
| 320 | 0x11BC8 | Room 5-6 |
| 321 | 0x11BD6 | Room 5-6 |
| 322 | 0x11C21 | Room 5-6 |
| 323 | 0x11C37 | Room 5-6 |
| 324 | 0x11C5E | Room 5-6 |
| 325 | 0x11D1C | Room 5-6 |
| 326 | 0x11D4F | Room 5-6 |
| 327 | 0x11D62 | Room 5-6 |
| 328 | 0x11D74 | Room 5-6 |
| 329 | 0x11D91 | Room 5-6 |
| 330 | 0x11DA3 | Room 5-6 |
| 331 | 0x11DB7 | Room 5-6 |
| 332 | 0x11DCB | Room 5-6 |
| 333 | 0x11DED | Room 5-6 |
| 334 | 0x11E01 | Room 5-6 |
| 335 | 0x11E28 | Room 5-6 |
| 336 | 0x11E3C | Room 5-6 |
| 337 | 0x11E50 | Room 5-6 |
| 338 | 0x11E70 | Room 5-6 |
| 339 | 0x11E83 | Room 5-6 |
| 340 | 0x11E96 | Room 5-6 |
| 341 | 0x11EA9 | Room 5-6 |
| 342 | 0x11EBC | Room 5-6 |
| 343 | 0x11ECF | Room 5-6 |
| 344 | 0x11EE5 | Room 5-6 |
| 345 | 0x11EFB | Room 5-6 |
| 346 | 0x11F11 | Room 5-6 |
| 347 | 0x11F27 | Room 5-6 |
| 348 | 0x11F3D | Room 5-6 |
| 349 | 0x11FC8 | Room 5-6 |
| 350 | 0x11FFB | Room 7-8 |
| 351 | 0x1202F | Room 7-8 |
| 352 | 0x1151D | Room 7-8 |
| 353 | 0x1215E | Room 7-8 |
| 354 | 0x1217B | Room 7-8 |
| 355 | 0x1151D | Room 7-8 |
| 356 | 0x1218F | Room 7-8 |
| 357 | 0x121A2 | Room 7-8 |
| 358 | 0x121C5 | Room 7-8 |
| 359 | 0x12200 | Room 7-8 |
| 360 | 0x1222D | Room 7-8 |
| 361 | 0x1223E | Room 7-8 |
| 362 | 0x1224D | Room 7-8 |
| 363 | 0x1151D | Room 7-8 |
| 364 | 0x12263 | Room 7-8 |
| 365 | 0x12286 | Room 7-8 |
| 366 | 0x12290 | Room 7-8 |
| 367 | 0x122AA | Room 7-8 |
| 368 | 0x122C0 | Room 7-8 |
| 369 | 0x122CB | Room 7-8 |
| 370 | 0x122EB | Room 7-8 |
| 371 | 0x122FF | Room 7-8 |
| 372 | 0x1232B | Room 7-8 |
| 373 | 0x12345 | Room 7-8 |
| 374 | 0x12358 | Room 7-8 |
| 375 | 0x1236B | Room 7-8 |
| 377 | 0x1253F | Room 7-8 |
| 378 | 0x1255C | Room 7-8 |
| 376 | 0x12579 | Room 7-8 |
| 380 | 0x1260E | Room 7-8 |
| 381 | 0x126F3 | Room 7-8 |
| 382 | 0x12705 | Room 7-8 |
| 383 | 0x1279C | Room 7-8 |

### Table 3 at file offset 0x4B6EA

**34 entries**

| Extra ID | Function | Room/Context |
|----------|----------|-------------|
| 3 | 0x15889 | Inventory/Special (3) |
| 4 | 0x1561F | Inventory/Special (4) |
| 7 | 0x1587A | Inventory/Special (7) |
| 9 | 0x158BD | Inventory/Special (9) |
| 12 | 0x15C49 | Inventory/Special (12) |
| 13 | 0x15C68 | Inventory/Special (13) |
| 28 | 0x158E1 | Inventory/Special (28) |
| 36 | 0x1592B | Inventory/Special (36) |
| 30 | 0x15959 | Inventory/Special (30) |
| 48 | 0x15994 | Inventory/Special (48) |
| 51 | 0x159E9 | Inventory/Special (51) |
| 52 | 0x159E9 | Inventory/Special (52) |
| 53 | 0x159E9 | Inventory/Special (53) |
| 54 | 0x159E9 | Inventory/Special (54) |
| 5 | 0x15A3D | Inventory/Special (5) |
| 19 | 0x15A68 | Inventory/Special (19) |
| 9 | 0x15A7F | Inventory/Special (9) |
| 24 | 0x15A96 | Inventory/Special (24) |
| 38 | 0x15AAD | Inventory/Special (38) |
| 41 | 0x15AF0 | Inventory/Special (41) |
| 32 | 0x15B07 | Inventory/Special (32) |
| 27 | 0x15B5B | Inventory/Special (27) |
| 39 | 0x15BA5 | Inventory/Special (39) |
| 40 | 0x15BA5 | Inventory/Special (40) |
| 26 | 0x15BB7 | Inventory/Special (26) |
| 2 | 0x15C22 | Inventory/Special (2) |
| 17 | 0x15BEC | Inventory/Special (17) |
| 13 | 0x15BEC | Inventory/Special (13) |
| 19 | 0x15BEC | Inventory/Special (19) |
| 37 | 0x15C22 | Inventory/Special (37) |
| 49 | 0x15BEC | Inventory/Special (49) |
| 50 | 0x15BEC | Inventory/Special (50) |
| 22 | 0x15C35 | Inventory/Special (22) |
| 34 | 0x15C35 | Inventory/Special (34) |

## Item Combination Tables (8 bytes/entry)

Format: `[uint16 item1][uint16 item2][uint32 function_ptr]`
Used when using inventory item on hotspot.

### Combination Table 1 at file offset 0x4B380

**100 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 373 (Extra 373) | 61 (Inv#61) | 0x12EB5 | |
| 373 (Extra 373) | 62 (Inv#62) | 0x12EC0 | |
| 0 (Inv#0) | 0 (Inv#0) | 0x12F07 | |
| 24 (Inv#24) | 24 (Inv#24) | 0x12F22 | |
| 34 (Inv#34) | 34 (Inv#34) | 0x12F7B | |
| 59 (Inv#59) | 59 (Inv#59) | 0x12F96 | |
| 17 (Inv#17) | 17 (Inv#17) | 0x12FD5 | |
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 2 at file offset 0x4B388

**99 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 373 (Extra 373) | 62 (Inv#62) | 0x12EC0 | |
| 0 (Inv#0) | 0 (Inv#0) | 0x12F07 | |
| 24 (Inv#24) | 24 (Inv#24) | 0x12F22 | |
| 34 (Inv#34) | 34 (Inv#34) | 0x12F7B | |
| 59 (Inv#59) | 59 (Inv#59) | 0x12F96 | |
| 17 (Inv#17) | 17 (Inv#17) | 0x12FD5 | |
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 3 at file offset 0x4B390

**98 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 0 (Inv#0) | 0 (Inv#0) | 0x12F07 | |
| 24 (Inv#24) | 24 (Inv#24) | 0x12F22 | |
| 34 (Inv#34) | 34 (Inv#34) | 0x12F7B | |
| 59 (Inv#59) | 59 (Inv#59) | 0x12F96 | |
| 17 (Inv#17) | 17 (Inv#17) | 0x12FD5 | |
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 4 at file offset 0x4B398

**97 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 24 (Inv#24) | 24 (Inv#24) | 0x12F22 | |
| 34 (Inv#34) | 34 (Inv#34) | 0x12F7B | |
| 59 (Inv#59) | 59 (Inv#59) | 0x12F96 | |
| 17 (Inv#17) | 17 (Inv#17) | 0x12FD5 | |
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 5 at file offset 0x4B3A0

**96 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 34 (Inv#34) | 34 (Inv#34) | 0x12F7B | |
| 59 (Inv#59) | 59 (Inv#59) | 0x12F96 | |
| 17 (Inv#17) | 17 (Inv#17) | 0x12FD5 | |
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 6 at file offset 0x4B3A8

**95 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 59 (Inv#59) | 59 (Inv#59) | 0x12F96 | |
| 17 (Inv#17) | 17 (Inv#17) | 0x12FD5 | |
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 7 at file offset 0x4B3B0

**94 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 17 (Inv#17) | 17 (Inv#17) | 0x12FD5 | |
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 8 at file offset 0x4B3B8

**93 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 64 (Inv#64) | 64 (Inv#64) | 0x13088 | |
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 9 at file offset 0x4B3C0

**92 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 83 (Inv#83) | 461 (Extra 461) | 0x13108 | |
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 10 at file offset 0x4B3C8

**91 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 469 (Extra 469) | 76 (Inv#76) | 0x131C9 | |
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 11 at file offset 0x4B3D0

**90 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 88 (Inv#88) | 88 (Inv#88) | 0x13310 | |
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 12 at file offset 0x4B3D8

**89 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 87 (Inv#87) | 87 (Inv#87) | 0x1387E | |
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 13 at file offset 0x4B3E0

**88 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 84 (Inv#84) | 503 (Extra 503) | 0x13892 | |
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 14 at file offset 0x4B3E8

**87 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 85 (Inv#85) | 506 (Extra 506) | 0x1395D | |
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 15 at file offset 0x4B3F0

**86 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 86 (Inv#86) | 506 (Extra 506) | 0x1395D | |
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 16 at file offset 0x4B3F8

**85 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 90 (Inv#90) | 506 (Extra 506) | 0x1395D | |
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 17 at file offset 0x4B400

**84 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 99 (Inv#99) | 506 (Extra 506) | 0x1446C | |
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 18 at file offset 0x4B408

**83 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 91 (Inv#91) | 601 (Extra 601) | 0x139DD | |
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 19 at file offset 0x4B410

**82 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 92 (Inv#92) | 601 (Extra 601) | 0x139DD | |
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 20 at file offset 0x4B418

**81 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 97 (Inv#97) | 97 (Inv#97) | 0x13F03 | |
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 21 at file offset 0x4B420

**80 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 614 (Extra 614) | 86 (Inv#86) | 0x13F83 | |
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 22 at file offset 0x4B428

**79 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 617 (Extra 617) | 76 (Inv#76) | 0x1413E | |
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 23 at file offset 0x4B430

**78 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 98 (Inv#98) | 98 (Inv#98) | 0x141E8 | |
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 24 at file offset 0x4B438

**77 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 86 (Inv#86) | 500 (Extra 500) | 0x14245 | |
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 25 at file offset 0x4B440

**76 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 81 (Inv#81) | 506 (Extra 506) | 0x1395D | |
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 26 at file offset 0x4B448

**75 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 84 (Inv#84) | 84 (Inv#84) | 0x1448A | |
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 27 at file offset 0x4B450

**74 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 650 (Extra 650) | 100 (Extra 100) | 0x1454C | |
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 28 at file offset 0x4B458

**73 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 101 (Extra 101) | 101 (Extra 101) | 0x1462B | |
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 29 at file offset 0x4B460

**72 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 108 (Extra 108) | 108 (Extra 108) | 0x1464E | |
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 30 at file offset 0x4B468

**71 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 109 (Extra 109) | 109 (Extra 109) | 0x146BA | |
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 31 at file offset 0x4B470

**70 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 95 (Inv#95) | 95 (Inv#95) | 0x146F4 | |
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 32 at file offset 0x4B478

**69 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 96 (Inv#96) | 96 (Inv#96) | 0x14ED7 | |
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 33 at file offset 0x4B480

**68 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 11 (Inv#11) | 11 (Inv#11) | 0x15471 | |
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 34 at file offset 0x4B488

**67 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 12 (Inv#12) | 12 (Inv#12) | 0x15471 | |
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 35 at file offset 0x4B490

**66 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 13 (Inv#13) | 13 (Inv#13) | 0x15471 | |
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 36 at file offset 0x4B498

**65 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 14 (Inv#14) | 14 (Inv#14) | 0x15471 | |
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 37 at file offset 0x4B4A0

**64 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 15 (Inv#15) | 15 (Inv#15) | 0x15471 | |
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 38 at file offset 0x4B4A8

**63 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 16 (Inv#16) | 16 (Inv#16) | 0x15471 | |
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 39 at file offset 0x4B4B0

**62 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 18 (Inv#18) | 18 (Inv#18) | 0x15471 | |
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 40 at file offset 0x4B4B8

**61 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 19 (Inv#19) | 19 (Inv#19) | 0x15471 | |
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 41 at file offset 0x4B4C0

**60 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 20 (Inv#20) | 20 (Inv#20) | 0x15471 | |
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 42 at file offset 0x4B4C8

**59 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 21 (Inv#21) | 21 (Inv#21) | 0x15471 | |
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 43 at file offset 0x4B4D0

**58 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 22 (Inv#22) | 22 (Inv#22) | 0x15471 | |
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 44 at file offset 0x4B4D8

**57 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 23 (Inv#23) | 23 (Inv#23) | 0x15471 | |
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 45 at file offset 0x4B4E0

**56 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 25 (Inv#25) | 25 (Inv#25) | 0x15471 | |
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 46 at file offset 0x4B4E8

**55 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 26 (Inv#26) | 26 (Inv#26) | 0x15471 | |
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 47 at file offset 0x4B4F0

**54 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 27 (Inv#27) | 27 (Inv#27) | 0x15471 | |
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 48 at file offset 0x4B4F8

**53 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 28 (Inv#28) | 28 (Inv#28) | 0x15471 | |
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 49 at file offset 0x4B500

**52 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 29 (Inv#29) | 29 (Inv#29) | 0x15471 | |
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 50 at file offset 0x4B508

**51 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 30 (Inv#30) | 30 (Inv#30) | 0x15471 | |
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 51 at file offset 0x4B510

**50 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 31 (Inv#31) | 31 (Inv#31) | 0x15471 | |
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 52 at file offset 0x4B518

**49 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 32 (Inv#32) | 32 (Inv#32) | 0x15471 | |
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 53 at file offset 0x4B520

**48 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 33 (Inv#33) | 33 (Inv#33) | 0x15471 | |
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 54 at file offset 0x4B528

**47 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 35 (Inv#35) | 35 (Inv#35) | 0x15471 | |
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 55 at file offset 0x4B530

**46 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 36 (Inv#36) | 36 (Inv#36) | 0x15471 | |
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 56 at file offset 0x4B538

**45 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 37 (Inv#37) | 37 (Inv#37) | 0x15471 | |
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 57 at file offset 0x4B540

**44 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 38 (Inv#38) | 38 (Inv#38) | 0x15471 | |
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 58 at file offset 0x4B548

**43 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 39 (Inv#39) | 39 (Inv#39) | 0x15471 | |
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 59 at file offset 0x4B550

**42 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 40 (Inv#40) | 40 (Inv#40) | 0x15471 | |
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 60 at file offset 0x4B558

**41 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 41 (Inv#41) | 41 (Inv#41) | 0x15471 | |
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 61 at file offset 0x4B560

**40 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 42 (Inv#42) | 42 (Inv#42) | 0x15471 | |
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 62 at file offset 0x4B568

**39 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 43 (Inv#43) | 43 (Inv#43) | 0x15471 | |
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 63 at file offset 0x4B570

**38 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 44 (Inv#44) | 44 (Inv#44) | 0x15471 | |
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 64 at file offset 0x4B578

**37 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 45 (Inv#45) | 45 (Inv#45) | 0x15471 | |
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 65 at file offset 0x4B580

**36 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 46 (Inv#46) | 46 (Inv#46) | 0x15471 | |
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 66 at file offset 0x4B588

**35 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 47 (Inv#47) | 47 (Inv#47) | 0x15471 | |
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 67 at file offset 0x4B590

**34 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 11 (Inv#11) | 358 (Extra 358) | 0x15525 | |
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 68 at file offset 0x4B598

**33 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 12 (Inv#12) | 358 (Extra 358) | 0x15525 | |
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 69 at file offset 0x4B5A0

**32 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 13 (Inv#13) | 358 (Extra 358) | 0x15525 | |
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 70 at file offset 0x4B5A8

**31 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 14 (Inv#14) | 358 (Extra 358) | 0x15525 | |
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 71 at file offset 0x4B5B0

**30 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 15 (Inv#15) | 358 (Extra 358) | 0x15525 | |
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 72 at file offset 0x4B5B8

**29 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 16 (Inv#16) | 358 (Extra 358) | 0x15525 | |
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 73 at file offset 0x4B5C0

**28 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 18 (Inv#18) | 358 (Extra 358) | 0x15525 | |
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 74 at file offset 0x4B5C8

**27 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 19 (Inv#19) | 358 (Extra 358) | 0x15525 | |
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 75 at file offset 0x4B5D0

**26 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 20 (Inv#20) | 358 (Extra 358) | 0x15525 | |
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 76 at file offset 0x4B5D8

**25 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 21 (Inv#21) | 358 (Extra 358) | 0x15525 | |
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 77 at file offset 0x4B5E0

**24 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 22 (Inv#22) | 358 (Extra 358) | 0x15525 | |
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 78 at file offset 0x4B5E8

**23 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 23 (Inv#23) | 358 (Extra 358) | 0x15525 | |
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 79 at file offset 0x4B5F0

**22 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 25 (Inv#25) | 358 (Extra 358) | 0x15525 | |
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 80 at file offset 0x4B5F8

**21 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 26 (Inv#26) | 358 (Extra 358) | 0x15525 | |
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 81 at file offset 0x4B600

**20 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 27 (Inv#27) | 358 (Extra 358) | 0x15525 | |
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 82 at file offset 0x4B608

**19 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 28 (Inv#28) | 358 (Extra 358) | 0x15525 | |
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 83 at file offset 0x4B610

**18 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 29 (Inv#29) | 358 (Extra 358) | 0x15525 | |
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 84 at file offset 0x4B618

**17 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 30 (Inv#30) | 358 (Extra 358) | 0x15525 | |
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 85 at file offset 0x4B620

**16 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 31 (Inv#31) | 358 (Extra 358) | 0x15525 | |
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 86 at file offset 0x4B628

**15 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 32 (Inv#32) | 358 (Extra 358) | 0x15525 | |
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 87 at file offset 0x4B630

**14 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 33 (Inv#33) | 358 (Extra 358) | 0x15525 | |
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 88 at file offset 0x4B638

**13 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 35 (Inv#35) | 358 (Extra 358) | 0x15525 | |
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 89 at file offset 0x4B640

**12 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 36 (Inv#36) | 358 (Extra 358) | 0x15525 | |
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 90 at file offset 0x4B648

**11 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 37 (Inv#37) | 358 (Extra 358) | 0x15525 | |
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 91 at file offset 0x4B650

**10 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 38 (Inv#38) | 358 (Extra 358) | 0x15525 | |
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 92 at file offset 0x4B658

**9 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 39 (Inv#39) | 358 (Extra 358) | 0x15525 | |
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 93 at file offset 0x4B660

**8 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 40 (Inv#40) | 358 (Extra 358) | 0x15525 | |
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 94 at file offset 0x4B668

**7 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 41 (Inv#41) | 358 (Extra 358) | 0x15525 | |
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 95 at file offset 0x4B670

**6 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 42 (Inv#42) | 358 (Extra 358) | 0x15525 | |
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 96 at file offset 0x4B678

**5 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 43 (Inv#43) | 358 (Extra 358) | 0x15525 | |
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 97 at file offset 0x4B680

**4 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 44 (Inv#44) | 358 (Extra 358) | 0x15525 | |
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

### Combination Table 98 at file offset 0x4B688

**3 combinations**

| Item 1 | Item 2 | Function | Notes |
|--------|--------|----------|-------|
| 45 (Inv#45) | 358 (Extra 358) | 0x15525 | |
| 46 (Inv#46) | 358 (Extra 358) | 0x15525 | |
| 47 (Inv#47) | 358 (Extra 358) | 0x15525 | |

## Pseudocode: Action Dispatch Flow

```c
// Called when player selects a verb from the popup menu
void room_specific_action_dispatcher(uint16 verb_code) {
    action_pending_flag = 0;
    
    switch (verb_code) {
        case 0x01:  // OPEN
            dispatch_from_table(OPEN_TABLE_0x47D24);
            break;
        case 0x02:  // TALK  
            handle_conversation_tree();
            break;
        case 0x08:  // CLOSE
            handle_dialog_interaction();
            break;
        case 0x10:  // LOOK
            dispatch_from_table(LOOK_TABLE_0x47BF0);
            break;
        case 0x20:  // PUSH
            dispatch_from_table(PUSH_TABLE_0x47C10);
            break;
        case 0x40:  // UNKNOWN VERB
            dispatch_from_table(UNKNOWN_TABLE_0x47C18);
            break;
        case 0x80:  // PULL
            dispatch_from_table(PULL_TABLE_0x47CBC);
            break;
        case 0x200: // USE INVENTORY ITEM
            dispatch_item_combination();
            break;
    }
}

// Generic dispatch from a standard table
void dispatch_from_table(DispatchEntry* table) {
    // Walk Alfred to hotspot first
    if (!walk_to_target_and_execute_queued_action()) {
        return;  // Walk was cancelled
    }
    
    // Play interaction animation (Alfred reaching out)
    animate_talk_bubble();
    
    // Search table for matching extra_id
    for (int i = 0; table[i].extra_id != 0xFFFF; i++) {
        if (table[i].extra_id == current_hotspot_extra_id) {
            // Found match - call handler
            table[i].handler_func();
            return;
        }
    }
    
    // No handler found - show generic response
    show_default_response();
}
```

## Notes

1. **LOOK action** is always available on any hotspot - no flag needed
2. **TALK action** (flag 0x10) routes to conversation system, not dispatch table
3. **Item combinations** use a separate 8-byte table format
4. **Function pointers** are Ghidra virtual addresses (add 0x10000 to file offset)
5. **Extra IDs** are unique per hotspot across all rooms
