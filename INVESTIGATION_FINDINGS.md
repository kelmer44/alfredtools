# Investigation Findings: Unused Assets, Easter Eggs & Code Verification

## 1. Ingame Texts (_ingameTexts) Audit

### Texts Used via Indexed Access (NOT explicitly named in code but reachable)
- **Indices 141-152** (OHGRANOSIRIS → LASPUERTASDELCIELO): Accessed via `DIOSHALCON + spell->page` (page 0-12). These are the 13 spell incantation lines for the Psalm of the Dead.
- **Indices 154-166** (PARAQUE_2 → NOSEQUEPRETENDES): Accessed via `154 + getRandomNumber(12)` — random rejection responses when using wrong item combinations.

### Bug Found: Random Response Range Mismatch
The **original game** generates random rejection responses with:
```asm
call rng
and eax, 0x0F       ; range 0-15 (16 possible values!)
mov eax, [eax*4 + text_base + 154*4]
```
ScummVM currently uses:
```cpp
byte response = (byte)getRandomNumber(12);  // range 0-12 (13 values)
```
This means **indices 167 (COSASRARAS), 168 (ARTE_O_LOCURA), 169 (UTILIDADES)** are reachable in the original but NOT in ScummVM. These texts look like **library catalog category labels** rather than proper rejection dialog — likely a **bug in the original game** where `& 0xF` was used instead of `% 13`, causing occasional nonsensical responses.

**Decision**: Keep ScummVM's `getRandomNumber(12)` as a deliberate bug fix, or match original with `getRandomNumber(15)` for accuracy.

### Texts Used in Original But Missing from ScummVM Implementation

| Index | Enum Name | Original Location | Context |
|-------|-----------|-------------------|---------|
| 30 | DEPIEDRANO_DEHIELO | 0x20D35 | Sphinx/ice puzzle dialog |
| 43 | AQUIENENTONCES | 0x22E2D | Library/book handler |
| 44 | LIBROSSECRETOS | 0x22E34 | Library handler |
| 55 | YAESTA_ABIERTO | 0x1CCFF | Door/container already open |
| 84 | LEESTOYVIGILANDO | 0x1FE94 | Room 27-28 guard watching |
| 139 | AQUI_NO_NECESITO | 0x23874 | Item not needed here |
| 170 | TITULOJUEGO | 0x113A5 | Title screen display (conditional on counter 20 < x < 150) |
| 174 | DOSINGREDIENTES | scaled index (counter=2) | Potion: "Two ingredients" |
| 175 | TRESINGREDIENTES | scaled index (counter=3) | Potion: "Three ingredients" |
| 176 | CUATROINGREDIENTES | scaled index (counter=4) | Potion: "Four ingredients" |
| 182 | DEMO_FINAL | 0x26FD2 | Demo version end handler |

### Texts Confirmed Unused in Both Original and ScummVM

| Index | Enum Name | Notes |
|-------|-----------|-------|
| 1 | HOY_NO_DISPONIBLES | Never referenced. Dead text. |
| 9 | BOTONVERDEPARASACAR_BOTONVERDEPARACANCELAR | Never referenced. ATM text, system cut. |
| 10 | PRIMEROMETA_TARJETA | Never referenced. ATM text, system cut. |
| 26 | ESPOCO | Never referenced. |
| 28 | NIPARAEMPEZAR | Never referenced. |
| 69 | PARECECERRADO | Never referenced. |
| 97 | AMISBRAZOS | Never referenced. Princess rescue lines, cut. |
| 98 | DIOSMIOQUEESESTO | Never referenced. Princess rescue lines, cut. |
| 99 | QUEPASA | Never referenced. Princess rescue lines, cut. |
| 100 | OLVIDECERRARTRAMPILLA | Never referenced. Princess rescue lines, cut. |
| 101 | NOTEPREOCUPES_VOLVERE | Never referenced. Princess rescue lines, cut. |
| 183-195 | DIOSHALCON_2 → LASPUERTAS_DELCIELO | Never referenced. Duplicate psalm set, completely unused. |

---

## 2. Room 3, Animation 2 (Sprite 4) — 12×5, 1 frame, pos 640×400
**Status: NEVER USED — Dead asset**

- Position is off-screen (640×400), dimensions are tiny (12×5 px), zIndex=255 (hidden)
- No code anywhere writes to sprite 4's zIndex field in room 3 context
- No item combination triggers modification of this sprite
- Even if zIndex were changed, it wouldn't be visible due to off-screen position
- **Conclusion**: Development artifact/placeholder, never enabled in any code path

---

## 3. Room 3, Animation 5 (Sprite 7) — 38×31, 2 frames, zIndex=255
**Status: USED — Broken window overlay**

- **Trigger**: Player uses **Brick (item 4) on Window (extra 294)** — handler at 0x2284B
- Handler animates sprite 9 (NPC walks upward), displays broken window sticker from ALFRED.6, sets flag [0x9824]=1, permanently disables Window and Storefront hotspots
- **Room init handler** at 0x25889 checks flag [0x9824]: if set, enables sprite 7 by setting zIndex to 100 (visible)
- **Narrative**: Throwing the brick breaks the shop window. Sprite 7 shows the broken/cracked window effect (38×31, 2 animation frames at position 261,275)

---

## 4. Room 45, NPC Conversation Root 3
**Status: NOT an oversight — Properly reachable**

Room 45's single NPC (the bathing girls) has a 4-state conversation system:

| Root | Content | How to reach |
|------|---------|--------------|
| 0 | Initial flirtatious invitation (elaborate dialogue tree, 83 choices) | Talk to girls first time |
| 1 | Second chance — 3 options (2 rejections, 1 acceptance) | After any rejection in Root 0 (ACTION 321 → branch=1) |
| 2 | Post-bathing: "¿Otro bañito?" | After accepting in Root 1 (ACTION 376 → branch=2) |
| **3** | **Permanent rejection: "¡Déjanos tranquilas! Has tenido tu oportunidad"** | **After rejecting in Root 1 (ACTION 377 → branch=3)** |

Root 3 is the final "you blew it" state — reached when the player refuses BOTH opportunities (Root 0 rejection → Root 1 rejection). This is intentional game design, not a bug.

---

## 5. Alfred7 Code Images (offsets 2321064, 2361388, 2669050, 2688168)

| Offset | Status | Details |
|--------|--------|---------|
| **2321064** (0x236AA8) | **USED** | 768-byte VGA palette shared by extraScreens[12] (CENSORED scene) and extraScreens[13] (Background book). Loaded when ACTION 376 fires in Room 45. |
| **2361388** (0x24062C) | **UNUSED** | Dead data at Ghidra 0x4B7BC. Zero code references. |
| **2669050** (0x28B5FA) | **UNUSED** | Dead data at Ghidra 0x4B7C8. Zero code references. |
| **2688168** (0x290228) | **UNUSED** | Dead data at Ghidra 0x4B7CC. Zero code references. |

The three unused offsets are stored in a data block near fight animation parameters but are never loaded or referenced. Likely leftover development assets that were cut.

---

## 6. Alfred7 Crocodile Sketches (offset 2381082)
**Status: UNUSED — Dead asset**

- Located at Ghidra data address 0x4B7C0
- Stored in the same dead data block as the code images
- Contains hand-drawn sketches of Alfred being eaten by a crocodile
- Zero references in the entire binary — not loaded, not displayed
- Likely concept art or prototype animation frames that were included in ALFRED.7 during development but never wired into the game

---

## 7. Alfred Fighting Animation
**Status: ONLY used by HIJODELAGRANPUTA cheat code**

- `play_fight_animation` at 0x26420 has exactly **ONE caller**: `main_game_loop` at 0x105AC
- Called with parameters: ALFRED.7 offset 0x2207FA, 71×102 px, 11 frames
- Triggered by pressing Space while in cheat mode (after typing HIJODELAGRANPUTA)
- **Never used in normal gameplay** — exclusively a debug/easter egg feature

---

## 8. HIJODELAGRANPUTA Cheat Code

### Activation
1. Player must be in **Room 25** (riverbank with Buddhist monk)
2. During the **"Who Said It?" quiz** (Phase 2), pick the absurd long answer: *"Rafael Tevoyadarunalechequetetevoyapartirlacaraytevanatenerquehacertelacirugia"*
3. Monk responds: **"Bien dicho!"**
4. **Action 362** fires at address 0x2224D → sets flag `[0x495F3]` (cheat_code_checking_enabled) to 1
5. This is the **ONLY** code path that enables the cheat

### How it works (global, persistent)
- Once enabled, the check runs **every frame** in `main_game_loop` regardless of current room
- Player types HIJODELAGRANPUTA (16 characters, checked sequentially against `ptr_cheat_code_string` at 0x4B79C)
- Each correct keypress advances `cheat_code_progress_counter` (0x5178D); wrong key resets to 0
- The flag **persists** in the game state flag array and survives save/load

### Effect: Debug free-movement mode
- Loads sound file "9ZZZZZZZ.SMP" (slot 6)
- **Left/Right arrows**: Move Alfred directly (bypassing walkbox constraints and pathfinding)
- **Space**: Play fight animation (ALFRED.7 @ 0x2207FA)
- **ESC**: Exit cheat mode

### Key Variables (Ghidra)
| Address | Name | Purpose |
|---------|------|---------|
| 0x495F3 | cheat_code_checking_enabled | Gate flag (flag array index 55) |
| 0x5178D | cheat_code_progress_counter | Position in string (0-15) |
| 0x5178F | DAT_0005178f | 1 = free movement active |
| 0x4B79C | ptr_cheat_code_string | → "HIJODELAGRANPUTA" at 0x40F41 |
| 0x4B7A0 | cheat_code_length | 16 |

---

## 9. Alfred7 Offset 1042757 (0xFE945) — UI Element
**Status: LOADED at startup, NEVER USED — Dead code**

- `load_fonts_and_graphics` (0x14EE3) reads 0x129E bytes from ALFRED.7 @ 0xFE945
- Data is RLE-decompressed (~0xC216 = 49,686 bytes) into buffer at 0x4FA5C
- **That buffer has ZERO read references** in the entire binary
- The game faithfully loads and decompresses this every startup, but nothing ever displays it
- Likely a cut UI popup/overlay element (possibly a dialog frame or information panel)

---

## Ghidra Annotations Made

### Comments Added
| Address | Description |
|---------|-------------|
| 0x14EE3 | Dead load documentation on load_fonts_and_graphics |
| 0x14EF9 | Specific dead load annotation for ALFRED.7 @ 0xFE945 |
| 0x105AC | Cheat code documentation on main_game_loop |
| 0x26420 | Fight animation — cheat-only documentation |
| 0x258B0 | Room 3 init — broken window sprite enable |
| 0x2284B | Brick+Window action handler documentation |
| 0x1B666 | Conversation state update — Room 45 root 3 reachability |
| 0x2224D | Action 362 — cheat code enabler |
| 0x4B7BC | Dead data block — unused ALFRED.7 offsets |

### Data Renamed
| Address | New Name |
|---------|----------|
| 0x4FA5C | unused_ui_sprite_buffer |
| 0x4FA58 | unused_ui_sprite_compressed_buffer |
| 0x4B7BC | DEAD_alfred7_offset_code_images_2361388 |
| 0x4B7C0 | DEAD_alfred7_offset_croc_sketches_2381082 |
| 0x4B7C8 | DEAD_alfred7_offset_code_images_2669050 |
| 0x4B7CC | DEAD_alfred7_offset_code_images_2688168 |
