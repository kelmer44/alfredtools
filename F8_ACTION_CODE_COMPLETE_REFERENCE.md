# F8 Action Code Complete Reference

## Overview

This document catalogs **all 116 F8 action codes** found in the dispatch table of `JUEGO.EXE`, along with their handler behaviors as determined through Ghidra reverse engineering. These action codes are triggered via the `0xF8` control code in room conversation/description data (ALFRED.1 Pair 12).

### Dispatch Table Location
- **File offset**: `0x4B058` in JUEGO.EXE  
- **Ghidra address**: `0x47E58 - 0x1000 = 0x47D58` (table base)
- **Format**: 116 entries × 6 bytes (2-byte action ID + 4-byte stored pointer)
- **Pointer fixup**: `ghidra_address = stored_pointer + 0x10000`
- **Terminator**: `0xFFFF` sentinel after last entry

### Common Handler Patterns

| Pattern | Description |
|---------|-------------|
| **Conv advance** | Calls `update_conversation_state(room, npc, branch)` to move NPC dialog forward |
| **Give item** | Calls `process_inventory_action(item_id)` to add item to inventory |
| **Set flag** | Writes to a game state byte (addresses in `0x95xx` range) |
| **NPC text** | Calls `setup_npc_conversation_text()` to change which dialog an NPC shows |
| **Combo gate** | XORs bits in a flag byte; only fires when all required bits are set |
| **Counter** | Increments/decrements a counter; triggers event at threshold |
| **Persist** | Writes modified room data back to ALFRED.1 file |
| **Arrest** | Shared handler that sends player to jail (room 31) |
| **Cutscene** | Complex animation/visual sequence with loops |

### Shared Handler: Arrest/Jail (0x2151D)
Used by actions **285, 291, 352, 355, 363**. Fades screen, calls `update_conversation_state(26, 1, 1)`, loads room 31 at position (342, 277). On first arrest, also persists NPC position data.

---

## Room 0 — City Panorama

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 257 | 0x0101 | 0x20C76 | **Intro cutscene**: Loads room 9 graphics, starts CD audio, loops calling action 353 + render_scene until flag `[0xFB8C]` is set. Restores palette and stops sound on exit. |

**Context**: Triggered from a description ("Es solo un cajón").

---

## Room 2 — Girlfriend's House

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 328 | 0x0148 | 0x21D74 | **Conv advance**: `update_conversation_state(room=2, npc=0, branch=1)` |
| 329 | 0x0149 | 0x21D91 | **Set flag**: Sets `[0x95E8] = 1` |

**Context**: 328 triggers after agreeing to get condoms. 329 is a state flag.

---

## Room 4 — Door Kicking

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 258 | 0x0102 | 0x20D04 | **Flag + conv**: Sets bit 0 of `[0x95B8]`, then `update_conversation_state(room=4, npc=0, branch=2)` |

**Context**: Triggered after threatening to use "the kick method" on a door.

---

## Room 5 — Statues

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 259 | 0x0103 | 0x20D28 | **NPC dialog**: Plays two NPC dialog sequences from `[0xBA2C]` and `[0xBA30]` |
| 260 | 0x0104 | 0x20D50 | **NPC dialog**: Plays two NPC dialog sequences from `[0xBA34]` and `[0xBA38]` |
| 261 | 0x0105 | 0x20D76 | **NPC dialog**: Single NPC dialog from `[0xBA3C]` |
| 262 | 0x0106 | 0x20D89 | **NPC dialog**: Single NPC dialog from `[0xBA40]` |
| 263 | 0x0107 | 0x20D9C | **NPC dialog**: Single NPC dialog from `[0xBA44]` |

**Context**: Conversation with mysterious statues that only show their right profile. Each action plays different dialog responses about the statues' nature.

---

## Room 7 — Time Traveler / Philosopher

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 264 | 0x0108 | 0x20DAF | **Conv advance**: `update_conversation_state(room=7, npc=0, branch=2)` |
| 267 | 0x010B | 0x20DCC | **Animation + conv + item**: Performs sprite animation, advances to `update_conversation_state(room=7, npc=0, branch=3)`, gives **item 8** |
| 268 | 0x010C | 0x20E18 | **NPC dialog**: Displays dialog from `[0xBA58]` |

**Context**: 264 after learning about time travel. 267 after receiving a poem riddle — gives an item and advances dialog. 268 is a description-context dialog.

---

## Room 9 — Library Computer

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 270 | 0x010E | 0x20E2E | **Library computer system**: Allocates 13,700 bytes, loads the 125-book database from ALFRED.7 offset 0x309E0, renders computer UI, enters interactive keyboard loop (keys '1'/'2'/'3'). Chains to action 354 via `wait_or_process_input`. |
| 271 | 0x010F | 0x21221 | **NPC dialog**: Displays dialog from `[0xBA78]` |

**Context**: 270 is the full interactive library computer system (triggered from description). 271 is another description dialog.

---

## Room 14 — Negotiation

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 272 | 0x0110 | 0x21237 | **Conv advance**: `update_conversation_state(room=14, npc=0, branch=1)` |
| 273 | 0x0111 | 0x21254 | **Persist conversation**: Complex file I/O — writes conversation state to ALFRED.1, sets `[0xFB74]=1, [0xFB75]=3`. Saves dialog progress to disk. |

**Context**: 272 after being told the price (100,000 pesetas). 273 after the Baiona/Galicia exchange — persists conversation progress.

---

## Room 18 — Newspaper Editor

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 274 | 0x0112 | 0x213BB | **Conv advance**: `update_conversation_state(room=18, npc=0, branch=1)` |
| 275 | 0x0113 | 0x213DB | **Conv advance**: `update_conversation_state(room=18, npc=0, branch=2)` |
| 276 | 0x0114 | 0x213EE | **Conv advance**: `update_conversation_state(room=18, npc=0, branch=3)` |
| 277 | 0x0115 | 0x21401 | **Conv advance + flags**: `update_conversation_state(room=18, npc=0, branch=5)`, sets `[0x95B9]=1`, increments `[0x95C4]` |

**Context**: 274-276 are sequential advances through the editor's conversation (offering different news headlines). 277 triggers when Alfred finds the juicy story (Fidel Castro headline) — sets completion flags and advances past branch 4 directly to 5.

---

## Room 20 — Travel Agency

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 278 | 0x0116 | 0x2142F | **Conv advance**: `update_conversation_state(room=20, npc=0, branch=1)` |
| 279 | 0x0117 | 0x21449 | **Arrest sequence**: Confiscates **item 75**, runs cutscene, loads room 21 at (575, 210), gives **items 17, 64, 24, 59** |
| 280 | 0x0118 | 0x214DB | **NPC dialog**: Displays dialog from `[0xBACC]` |
| 281 | 0x0119 | 0x214F1 | **NPC dialog**: Displays dialog from `[0xBAD0]` |
| 282 | 0x011A | 0x21507 | **NPC dialog**: Displays dialog from `[0xBAD4]` |

**Context**: 278 after refusing to go to Catarroja. 279 is a specific arrest — confiscates an item and sends player to a new location with new inventory. 280-282 are description dialogs (hotel/room items with "Me recuerda a alguien").

---

## Room 22 — Market / Multiple NPCs

This room has the most complex action system with a 12-branch conversation tree for NPC 0, plus a combo gate puzzle for NPC 1.

### NPC 0 — Market Merchant (Escalating Confrontation)

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 330 | 0x014A | 0x21DA3 | **Give item**: Gives **item 102** (0x66) |
| 331 | 0x014B | 0x21DB7 | **NPC dialog**: Shows text from `[0xBB74]` |
| 332 | 0x014C | 0x21DCB | **Conditional give**: Gives **item 104** (0x68) only if not already in inventory |
| 333 | 0x014D | 0x21DED | **NPC dialog**: Shows text from `[0xBB78]` |
| 334 | 0x014E | 0x21E01 | **Conv + item**: `update_conversation_state(room=22, npc=0, branch=1)` + gives **item 76** |
| 335 | 0x014F | 0x21E28 | **Give item**: Gives **item 103** (0x67) — oranges |
| 336 | 0x0150 | 0x21E3C | **NPC dialog**: Shows text from `[0xBB7C]` |
| 337 | 0x0151 | 0x21E50 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=2)` |
| 338 | 0x0152 | 0x21E70 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=3)` |
| 339 | 0x0153 | 0x21E83 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=4)` |
| 340 | 0x0154 | 0x21E96 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=5)` |
| 341 | 0x0155 | 0x21EA9 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=6)` |
| 342 | 0x0156 | 0x21EBC | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=7)` |
| 343 | 0x0157 | 0x21ECF | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=8)` |
| 344 | 0x0158 | 0x21EE5 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=9)` |
| 345 | 0x0159 | 0x21EFB | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=10)` |
| 346 | 0x015A | 0x21F11 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=11)` |
| 347 | 0x015B | 0x21F27 | **Conv advance**: `update_conversation_state(room=22, npc=0, branch=12)` |

### NPC 1 — Anti-Piracy + Combo Gate

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 296 | 0x0128 | 0x218F3 | **Conv advance**: `update_conversation_state(room=22, npc=1, branch=1)` |
| 348 | 0x015C | 0x21F3D | **⚠️ ANTI-PIRACY**: Infinite loop with PC speaker noise + random screen corruption. Any keypress triggers intentional divide-by-zero crash. No normal exit. |
| 349 | 0x015D | 0x21FC8 | **Combo gate**: XOR bit 0 of `[0x95F0]`; if result == 3 → `update_conversation_state(room=22, npc=1, branch=1)` |
| 350 | 0x015E | 0x21FFB | **Combo gate**: XOR bit 1 of `[0x95F0]`; if result == 3 → `update_conversation_state(room=22, npc=1, branch=1)` |
| 351 | 0x015F | 0x2202F | **18-line cutscene dialog**: Long NPC dialog between two characters using text pointer table `[0xBB80-0xBBC4]` |

**Context**: The market has a long escalating confrontation (12 branches where the merchant gets increasingly angry). The anti-piracy action (348) crashes pirated copies. Actions 349+350 are a dual-trigger gate — both must be selected to advance NPC 1's conversation.

---

## Room 23 — Girlfriend / Princess Quest

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 352 | 0x0160 | 0x2151D | **Arrest** (shared handler): Sends player to jail in room 31 |
| 353 | 0x0161 | 0x2215E | **Conv advance**: `update_conversation_state(room=23, npc=0, branch=2)` |
| 354 | 0x0162 | 0x2217B | **Give item**: Gives **item 105** (0x69) — photocopy |
| 355 | 0x0163 | 0x2151D | **Arrest** (shared handler): Sends player to jail in room 31 |
| 356 | 0x0164 | 0x2218F | **Conv advance**: `update_conversation_state(room=23, npc=0, branch=3)` |

**Context**: 352 triggers when threatening assault (police called → jail). 353 after farewell kiss. 354 when NPC gives photocopy. 355 after final police encounter. 356 after condom exchange conversation ends.

---

## Room 25 — River Philosopher / Poetry Quiz

This room features a complex **poetry quiz puzzle** with a counter mechanic.

### Quiz Mechanics
- Counter at `[0x95F2]`, starts at 0
- **Correct answer** (action 359): increments counter; at 15 → gives **item 106** + resets counter
- **Wrong answer -1** (action 357): decrements counter by 1
- **Wrong answer -2** (action 358): decrements counter by 2
- **"I don't know"** (action 361): resets NPC text via `setup_npc_conversation_text(room=25, npc=0, flag=1, idx=25)`

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 357 | 0x0165 | 0x221A2 | **Wrong answer**: Decrements `[0x95F2]` by 1, shows NPC reaction |
| 358 | 0x0166 | 0x221C5 | **Wrong answer**: Decrements `[0x95F2]` by 2, shows NPC reaction |
| 359 | 0x0167 | 0x22200 | **Correct answer**: Increments `[0x95F2]`; if reaches 15 → gives **item 106**, resets counter |
| 360 | 0x0168 | 0x2222D | **Reset counter**: Clears `[0x95F2]` to 0, resets NPC text |
| 361 | 0x0169 | 0x2223E | **"I don't know"**: Resets NPC text via `setup_npc_conversation_text()` |
| 362 | 0x016A | 0x2224D | **Special trigger**: Sets `[0x95F3]=1`, resets NPC text |
| 363 | 0x016B | 0x2151D | **Arrest** (shared handler): Sends player to jail |
| 364 | 0x016C | 0x22263 | **Riddle wrong**: `setup_npc_conversation_text(room=25, npc=0, flag=27, idx=43)` — changes NPC dialog after wrong riddle answer |
| 365 | 0x016D | 0x22286 | **Riddle correct**: `update_conversation_state(room=25, npc=0, branch=1)` |
| 366 | 0x016E | 0x22290 | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=1)` |
| 367 | 0x016F | 0x222AA | **Accept riddle**: `update_conversation_state(room=25, npc=0, branch=27)` + triggers sprite hover recheck |

**Context**: The philosopher asks Alfred to identify authors of river-related quotes. Each correct guess (359) adds to the counter. Wrong guesses subtract (357 by 1, 358 by 2). Getting 15 correct answers rewards item 106. Actions 363-367 handle the Egyptian riddle ("If all Egyptians lie...") sub-puzzle.

### Other Room 25 Actions (from dispatch table, not in conversations)

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 298 | 0x012A | 0x219A8 | **Conv + sprite**: `update_conversation_state(room=25, npc=0, branch=3)` + `check_sprite_hover(2, 0)` |
| 299 | 0x012B | 0x219D4 | **Conv + flag**: `update_conversation_state(room=25, npc=0, branch=1)`, sets `[0x95D0]=1` |
| 300 | 0x012C | 0x219FB | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=5)` |
| 301 | 0x012D | 0x21A18 | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=6)` |
| 302 | 0x012E | 0x21A2B | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=7)` |
| 303 | 0x012F | 0x21A3E | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=8)` |
| 304 | 0x0130 | 0x21A51 | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=9)` |
| 305 | 0x0131 | 0x21A64 | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=10)` |
| 306 | 0x0132 | 0x21A77 | **Conv advance**: `update_conversation_state(room=25, npc=0, branch=3)` |

---

## Room 26 — Street with Police / Prostitute

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 285 | 0x011D | 0x2151D | **Arrest** (shared handler): Sends player to jail in room 31 via `update_conversation_state(room=26, npc=1, branch=1)` |
| 295 | 0x0127 | 0x218CC | **Conv + item**: `update_conversation_state(room=26, npc=0, branch=3)` + gives **item 84** |
| 368 | 0x0170 | 0x222C0 | **No-op**: Placeholder handler, does nothing |
| 369 | 0x0171 | 0x222CB | **Conv advance**: `update_conversation_state(room=26, npc=0, branch=1)` |
| 383 | 0x017F | 0x2279C | **Conv advance**: `update_conversation_state(room=26, npc=0, branch=2)` |

**Context**: 285 triggers when insulting the policeman (multiple dialog paths lead to arrest). 295 when buying from prostitute (gives item, likely magazine). 369 after haggling. 383 after the "romantico" exchange. 368 is a dead placeholder.

---

## Room 27 — Egyptian Shop

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 286 | 0x011E | 0x21787 | **Conv + item**: `update_conversation_state(room=27, npc=0, branch=2)` + gives **item 83** |
| 287 | 0x011F | 0x217B1 | **Item + counter**: Gives **item(s)**, increments counter `[0x95F4]`; at 4 → `update_conversation_state(room=27, npc=1, branch=2)` |
| 288 | 0x0120 | 0x217FA | **Item + counter**: Gives **item(s)**, increments `[0x95F4]`; at 4 → unlock |
| 289 | 0x0121 | 0x21839 | **Item + counter**: Gives **item(s)**, increments `[0x95F4]`; at 4 → unlock |
| 290 | 0x0122 | 0x21882 | **Item + counter**: Gives **item(s)**, increments `[0x95F4]`; at 4 → unlock |
| 370 | 0x0172 | 0x222EB | **Give item**: Gives **item 111** |
| 371 | 0x0173 | 0x222FF | **Give items + conv**: Gives **items 111 + 110**, then `update_conversation_state(room=27, npc=0, branch=2)` |

**Context**: 286 inflates a purchase. 287-290 form an evidence collection system — each purchase increments a counter; after 4 purchases, NPC 1's conversation unlocks. 370-371 are purchases with haggling (370 after first haggle, 371 after accepting price + tip).

---

## Room 29 — Egyptian Museum

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 327 | 0x0147 | 0x21D62 | **Set flag**: Sets `[0x95E5] = 1` |

**Context**: Triggered from description ("Un museo Egipcio en Egipto. Mira que bien!"). Sets a visited flag.

---

## Room 30 — Travesti Discovery

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 291 | 0x0123 | 0x2151D | **Arrest** (shared handler): Sends player to jail in room 31 |

**Context**: Triggered during the stuttering confession scene ("Ya! Un travesti, eh?"). All 7 dialog branches lead to the same arrest.

---

## Room 31 — Prison Cell

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 292 | 0x0124 | 0x2161D | **Conv advance**: `update_conversation_state(room=31, npc=0, branch=1)` |
| 293 | 0x0125 | 0x2163A | **Persist + conv**: Writes NPC position (640, 400) at room data offset +0x4C5 → persists to ALFRED.1, then `update_conversation_state(room=31, npc=0, branch=2)` |
| 294 | 0x0126 | 0x216F5 | **Persist flag**: Sets room data byte `[0x527]=1` → persists to ALFRED.1 |

**Context**: 292 after cellmate's first outburst. 293 after cellmate reveals tunnel escape — moves an NPC offscreen (640,400) and advances dialog. 294 sets a persistent room state flag (likely marks toilet as examined).

---

## Room 34 — Palace Guard

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 297 | 0x0129 | 0x21910 | **Conv + persist**: `update_conversation_state(room=34, npc=0, branch=2)` + sets room data `[0x1C1]=1` → persists to ALFRED.1 |
| 372 | 0x0174 | 0x2232B | **Conv advance**: `update_conversation_state(room=34, npc=0, branch=2)` |
| 373 | 0x0175 | 0x22345 | **Conv advance**: `update_conversation_state(room=34, npc=0, branch=3)` |
| 374 | 0x0176 | 0x22358 | **Conv advance**: `update_conversation_state(room=34, npc=0, branch=1)` |

**Context**: 297 when showing the magazine to the guard (persists state + opens new dialog). 372-374 handle different dialog branches with the guard (trying various excuses to get past).

---

## Room 37 — Maze/Passage

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 307 | 0x0133 | 0x21A8A | **Persist room data**: Sets room data `[0x47C]=8` (hotspot count) → persists to ALFRED.1 |

**Context**: From a description trigger. Modifies the room's hotspot count (likely reveals hidden hotspots after a puzzle).

---

## Room 41 — Prison / Guard

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 308 | 0x0134 | 0x21B11 | **NPC text swap**: `setup_npc_conversation_text(room=41, npc=0, expected=16, new=2)` — changes which conversation root the NPC uses |
| 313 | 0x0139 | 0x21B34 | **Conv advance**: `update_conversation_state(room=41, npc=0, branch=1)` |

**Context**: 308 updates the guard's dialog (triggered from many conversation branches). 313 advances the guard's conversation (after the Egyptian riddle, beer jar, or flirting).

---

## Room 43 — Desert Vendor

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 314 | 0x013A | 0x21B4E | **Give item**: Gives **item 93** (0x5D) — sand liquor bottle |
| 316 | 0x013C | 0x21B62 | **Give item**: Gives **item 94** (0x5E) — sun cream |
| 317 | 0x013D | 0x21B76 | **Give item**: Gives **item 95** (0x5F) — another product |
| 318 | 0x013E | 0x21B8A | **Give item**: Gives **item 96** (0x60) — another product |
| 319 | 0x013F | 0x21B9E | **Give item + conv**: Gives **item 97** (0x61) — pyramid map + `update_conversation_state(room=43, npc=0, branch=2)` |
| 320 | 0x0140 | 0x21BC8 | **Conv advance**: `update_conversation_state(room=43, npc=0, branch=2)` |
| 324 | 0x0144 | 0x21C5E | **Conv + persist**: `update_conversation_state(room=43, npc=0, branch=2)` + writes persistent state (value 8) to room 47 in ALFRED.1 |

**Context**: 314-318 are sequential purchases from the vendor (liquor, sun cream, etc.). 319 is buying the pyramid map (key item, advances dialog). 320 after trying to return the map. 324 after the vendor proves he's the real architect — persists changes to the pyramid room (47).

---

## Room 45 — Oasis / Bathing Girls

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 321 | 0x0141 | 0x21BD6 | **Conv + sound**: `update_conversation_state(room=45, npc=0, branch=1)` + starts looping ambient sound |
| 376 | 0x0178 | 0x22579 | **Fight animation**: Plays fight animation sequence via `play_fight_animation`, reloads room 12 graphics, `update_conversation_state(room=45, npc=0, branch=2)` |
| 377 | 0x0179 | 0x2253F | **Conv advance**: `update_conversation_state(room=45, npc=0, branch=3)` |

**Context**: 321 after girls invite Alfred to bathe (repeated in many branches). 376 when Alfred finally agrees — fight animation plays, then dialog advances. 377 when choosing not to join. Note: Action 0x7878 (30840) found in room 45 data is likely a data artifact (two consecutive 0x78 bytes), not a real action.

---

## Room 47 — Pyramid Interior / Architect

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 322 | 0x0142 | 0x21C21 | **NPC dialog**: Displays dialog from text pointer `[0xBB28]` |
| 323 | 0x0143 | 0x21C37 | **Dual conv advance**: `update_conversation_state(room=47, npc=0, branch=1)` + `update_conversation_state(room=43, npc=0, branch=3)` |

**Context**: 322 triggered from description (examining pyramid plans). 323 after the architect reveals the door puzzle — advances both room 47 and room 43 conversations simultaneously.

---

## Room 49 — Mummy / Father

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 325 | 0x0145 | 0x21D1C | **Counter gate**: Increments `[0x95D8]`; only triggers `update_conversation_state(room=49, npc=0, branch=1)` on the **2nd** interaction |
| 326 | 0x0146 | 0x21D4F | **Conv advance**: `update_conversation_state(room=49, npc=0, branch=2)` |
| 378 | 0x017A | 0x2255C | **Conv advance**: `update_conversation_state(room=49, npc=0, branch=3)` |

**Context**: 325 after recognizing the mummy (needs 2 triggers to advance). 326 after getting directions to the princess. 378 during the father confession scene.

---

## Room 52 — Endgame

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 375 | 0x0177 | 0x2236B | **Endgame cutscene**: 5-phase sequence with line drawing, sticker overlays, sprite animations, then warps player to **room 48** |

**Context**: Triggered from a description. The game's endgame transition sequence.

---

## Actions Not Referenced in Room Conversations

These actions exist in the dispatch table but were not found in any room's Pair 12 text data. They may be triggered by room handler scripts, item-use handlers, or other mechanisms.

| Action | Hex | Handler | Description |
|--------|-----|---------|-------------|
| 296 | 0x0128 | 0x218F3 | Conv advance: room 22, NPC 1, branch 1 |
| 298 | 0x012A | 0x219A8 | Conv + sprite: room 25, NPC 0, branch 3 |
| 299 | 0x012B | 0x219D4 | Conv + flag: room 25, NPC 0, branch 1 + `[0x95D0]=1` |
| 300 | 0x012C | 0x219FB | Conv advance: room 25, NPC 0, branch 5 |
| 301 | 0x012D | 0x21A18 | Conv advance: room 25, NPC 0, branch 6 |
| 302 | 0x012E | 0x21A2B | Conv advance: room 25, NPC 0, branch 7 |
| 303 | 0x012F | 0x21A3E | Conv advance: room 25, NPC 0, branch 8 |
| 304 | 0x0130 | 0x21A51 | Conv advance: room 25, NPC 0, branch 9 |
| 305 | 0x0131 | 0x21A64 | Conv advance: room 25, NPC 0, branch 10 |
| 306 | 0x0132 | 0x21A77 | Conv advance: room 25, NPC 0, branch 3 |
| 380 | 0x017C | 0x2260E | Screen effect: Clears all graphics buffers, sets palette entries 0x0D and 0xF2 |
| 381 | 0x017D | 0x226F3 | Mid-function code: Part of a larger routine (likely related to 380/382) |
| 382 | 0x017E | 0x22705 | Sound sequence: Loads sound 361 into slot 6, plays 3× loop, waits for completion |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total dispatch entries | 116 |
| Unique handler addresses | ~85 |
| Actions in conversations | 103 |
| Actions not in conversations | 13 |
| Rooms with actions | 27 of 56 |
| Shared arrest handler uses | 5 (actions 285, 291, 352, 355, 363) |
| Anti-piracy traps | 1 (action 348) |
| Items given | ~20+ different items |
| Max branches (single NPC) | 12 (room 22, NPC 0) |
| Quiz counter threshold | 15 correct answers (room 25) |
| Purchase counter threshold | 4 items (room 27) |

## Key Game State Addresses

| Address | Purpose | Used By |
|---------|---------|---------|
| `[0x95B8]` | Room 4 door kick flag | Action 258 |
| `[0x95B9]` | Newspaper story found | Action 277 |
| `[0x95C4]` | General progress counter | Action 277 |
| `[0x95D0]` | Room 25 philosopher flag | Action 299 |
| `[0x95D8]` | Mummy recognition counter | Action 325 |
| `[0x95E5]` | Museum visited flag | Action 327 |
| `[0x95E8]` | Room 2 state flag | Action 329 |
| `[0x95F0]` | Anti-piracy combo gate | Actions 349, 350 |
| `[0x95F2]` | Poetry quiz counter (0-15) | Actions 357-360 |
| `[0x95F3]` | Special quiz trigger | Action 362 |
| `[0x95F4]` | Shop purchase counter (0-4) | Actions 287-290 |
