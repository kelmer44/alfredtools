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

| Index | Enum Name | Original Location | Context | ScummVM Bug? |
|-------|-----------|-------------------|---------|--------------|
| 30 | DEPIEDRANO_DEHIELO | 0x20D33 | Room 3 (street) room script — NPC retort in escalating dialog sequence | See §10 |
| 43 | AQUIENENTONCES | 0x22E2D | Library/book handler | |
| 44 | LIBROSSECRETOS | 0x22E34 | Library handler | |
| 55 | YAESTA_ABIERTO | 0x1CCFA | Room 13 kitchen drawer — "already opened" third path | **YES** — §10.1 |
| 84 | LEESTOYVIGILANDO | 0x1FE92 | Room 25 watchman — repeat encounter alertness response | See §10 |
| 139 | AQUI_NO_NECESITO | 0x23870 | Spellbook self-use in wrong room (not 28/51-54) | **YES** — §10.4 |
| 170 | TITULOJUEGO | 0x113A5 | Title screen display (conditional on counter 20 < x < 150) | |
| 174 | DOSINGREDIENTES | scaled index (counter=2) | Potion: "Two ingredients" | |
| 175 | TRESINGREDIENTES | scaled index (counter=3) | Potion: "Three ingredients" | |
| 176 | CUATROINGREDIENTES | scaled index (counter=4) | Potion: "Four ingredients" | |
| 182 | DEMO_FINAL | 0x26FD2 | Demo version end handler | |

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

---

## 10. Ingame Text Handler Analysis — Full Decompilation

Binary analysis of the dispatch table handlers containing text indices 30, 55, 84, and 139. All handlers were located by tracing dispatch table function pointers from the data section, then manually decoding x86-32 instructions from the LE executable. Ghidra does not recognize these addresses as functions because they are called exclusively via indirect function pointers in the dispatch tables.

### 10.1. YAESTA_ABIERTO (text[55]) — Kitchen Drawer, Room 13

**Dispatch**: Extra 375, Script Table type 0x40 (table at `0x47C18`)
**Handler address**: `0x1CCA7` — 94 bytes (to `0x1CD05`)
**Room**: 13 (Kitchen — inside the restaurant)
**Action**: OPEN on kitchen drawer hotspot
**ScummVM function**: `openKitchenDrawer()` in [actions.cpp](actions.cpp)

#### Original Handler — Full Pseudocode
```c
void handler_extra375_open_drawer(void) {     // 0x1CCA7
    if (flag[0x495C2] == 0) {                  // FLAG_JEFE_ENCARCELADO
        // Boss chef is still free — blocks access
        npc_say(text[52]);                     // QUITA_ESAS_MANOS: "¡Quita esas manos de ahí!"
        return;
    }

    if (flag[0x49D9C] == 0) {                  // item-taken flag (never resets)
        // First time opening after boss imprisoned
        flag[0x49D9C] = 1;                     // Mark item as taken
        load_sticker(0x07CA);                  // Sticker: open drawer graphic
        add_inventory_item(63);                // Recipe (item 63)
        alfred_say(text[54]);                  // QUESESTO_RECETA: "¿Qué es esto? Parece una receta."
    } else {
        // Already took the recipe — drawer is empty
        alfred_say(text[55]);                  // YAESTA_ABIERTO: "Ya está abierto"
    }
}
```

#### Key x86 Decode
```
0x1CCA7: push 0x08; call __STK; push edx       ; function prologue
0x1CCB2: cmp byte [0x95C2], 0                   ; FLAG_JEFE_ENCARCELADO
0x1CCB9: jnz 0x1CCCA                            ; → boss imprisoned path
0x1CCBB: mov edx, [0xBA84]                      ; text_ptrs[52] = QUITA_ESAS_MANOS
0x1CCC1: xor eax, eax                           ; character 0 = NPC
0x1CCC3: call display_text_with_character_animation ; (0x1B1A2)
0x1CCC8: pop edx; ret
0x1CCCA: cmp byte [0x9D9C], 0                   ; item-taken flag
0x1CCD1: jnz 0x1CCFA                            ; → already taken
0x1CCD3: mov byte [0x9D9C], 1                   ; SET item-taken
0x1CCDA: mov edx, 0x7CA; mov eax, 0x1B0FA       ; sticker params
0x1CCE4: call load_sticker_from_alfred6          ; (0x1BA45)
0x1CCE9: mov eax, 0x3F                           ; item 63 = recipe
0x1CCEE: call process_inventory_action           ; (0x24157)
0x1CCF3: mov eax, [0xBA8C]                       ; text_ptrs[54] = QUESESTO_RECETA
0x1CCF8: jmp 0x1CCFF                             ; → common display
0x1CCFA: mov eax, [0xBA90]                       ; text_ptrs[55] = YAESTA_ABIERTO
0x1CCFF: call display_text_with_voice            ; (0x25487)
0x1CD04: pop edx; ret
```

#### ScummVM Bug: Missing "Already Opened" Check

Current ScummVM implementation:
```cpp
void PelrockEngine::openKitchenDrawer(HotSpot *hotspot) {
    if (!_state->getFlag(FLAG_JEFE_ENCARCELADO)) {
        _dialog->say(_res->_ingameTexts[QUITA_ESAS_MANOS]);
    } else {
        _room->addSticker(36);
        addInventoryItem(63);
        _dialog->say(_res->_ingameTexts[QUESESTO_RECETA]);
    }
}
```

**Bug**: The ScummVM code is missing the third path. It should check whether the recipe has already been taken. Without this check:
1. The sticker is re-added every time (harmless, but redundant)
2. `addInventoryItem(63)` is called repeatedly (may duplicate the recipe in inventory)
3. The text "¿Qué es esto? Parece una receta." plays every time instead of "Ya está abierto" on subsequent opens

**Fix**: Add a state flag check (e.g. `FLAG_RECIPE_TAKEN`) before the item-granting branch, and show `YAESTA_ABIERTO` when the recipe was already taken.

#### Speaker Note
- Path 1 (QUITA_ESAS_MANOS): **NPC speaks** — uses `display_text_with_character_animation` (EAX=0 = NPC). The chef/boss character says this.
- Paths 2/3 (QUESESTO_RECETA / YAESTA_ABIERTO): **Alfred speaks** — uses `display_text_with_voice`. Alfred comments on the drawer contents.

---

### 10.2. LEESTOYVIGILANDO (text[84]) — Watchman, Room 25

**Dispatch**: Extra 609, Room-Specific Script type 0x01 (table at `0x47D24`, entry 32)
**Handler address**: `0x1FD8B` — ~333 bytes (to ~`0x1FED8`)
**Room**: 25 (Riverbank / Buddhist monk area)
**Action**: Room-specific script triggered by interacting with the sunflower / approaching the watchman
**ScummVM function**: `pickupSunflower()` in [actions.cpp](actions.cpp)

#### Original Handler — Dialog Branch Pseudocode

The handler at `0x1FD8B` has two major branches:

```c
void handler_extra609_room_script(void) {       // 0x1FD8B
    if (flag[0x495D0] != 0) {                    // FLAG_PARADOJA_RESUELTA (puzzle solved)
        // === MAIN BRANCH: Item acquisition ===
        // Complex logic: sticker rendering, file loading,
        // inventory item add, scene update.
        // (This is the "puzzle already solved, pick up sunflower" path)
        return;
    }

    // === DIALOG BRANCH: Watchman interaction ===
    // flag[0x495D0] == 0 → puzzle NOT yet solved

    if (flag[0x495D1] != 0) {                    // "watchman alertness" flag
        // Watchman ALREADY alerted — repeat encounter
        npc_say(text[84]);                       // LEESTOYVIGILANDO: "Le estoy vigilando"
        return;
    }

    // First encounter — watchman NOT yet alerted
    npc_say(text[85]);                           // OIGA: "¡Oiga...!"
    flag[0x495D1] = 1;                           // SET alertness flag
    setCurrentRoot(25, 26, 0);                   // conversation state: room 25, root 26
    trigger_conversation(2, 0);                  // start conversation type 2
}
```

#### Key x86 Decode (Dialog Branch at 0x1FE89)
```
0x1FE89: cmp byte [0x95D1], 0                   ; watchman alertness flag
0x1FE90: jz 0x1FEA3                             ; → first encounter (not alerted)
; REPEAT ENCOUNTER:
0x1FE92: mov edx, [0xBB04]                      ; text_ptrs[84] = LEESTOYVIGILANDO
0x1FE98: xor eax, eax                           ; character 0 = NPC (watchman)
0x1FE9A: call display_text_with_character_animation ; (0x1B1A2)
0x1FE9F: pop edx; pop ecx; pop ebx; ret
; FIRST ENCOUNTER:
0x1FEA3: mov edx, [0xBB08]                      ; text_ptrs[85] = OIGA
0x1FEA9: xor eax, eax                           ; character 0 = NPC (watchman)
0x1FEAB: call display_text_with_character_animation ; (0x1B1A2)
0x1FEB0: mov byte [0x95D1], 1                   ; SET alertness flag
0x1FEB7: mov ebx, 0x1A                          ; 26 (conversation root)
0x1FEBC: xor edx, edx                           ; 0
0x1FEBE: mov eax, 0x19                          ; 25 (room number)
0x1FEC3: call setCurrentRoot                    ; (0x1B666) → setCurrentRoot(25, 26, 0)
0x1FEC8: xor edx, edx                           ; 0
0x1FECA: mov eax, 0x02                          ; conversation type 2
0x1FECF: call trigger_conversation              ; (0x18DCE)
0x1FED4: pop edx; pop ecx; pop ebx; ret
```

#### Watchman Alertness Mechanism

The watchman near the sunflower in Room 25 has a two-state dialog system:

| State | Flag `0x495D1` | Response | What Happens Next |
|-------|----------------|----------|-------------------|
| **First time** | 0 | "¡Oiga...!" (text[85]) | Sets flag to 1, starts conversation with monk (root 25/26) about the riddle |
| **Repeat** | 1 | "Le estoy vigilando" (text[84]) | Returns immediately — no conversation triggered |

The flag `0x495D1` acts as a permanent watchman alertness state. Once the watchman has warned the player ("¡Oiga!"), all subsequent attempts to interact show "Le estoy vigilando" until the puzzle is solved (flag `0x495D0` set), which unlocks the main branch where the sunflower can actually be picked up.

#### Speaker Note
Both paths use `display_text_with_character_animation` with EAX=0 → **NPC (the watchman) speaks** in both cases.

#### ScummVM Comparison
The ScummVM `pickupSunflower()` checks `FLAG_PARADOJA_RESUELTA` and shows `OIGA` on the first attempt, matching the first-encounter path. However, it uses `FLAG_RIDDLE_PRESENTED` to gate subsequent attempts rather than the original's alertness flag. The LEESTOYVIGILANDO text is not referenced — the ScummVM implementation may rely on the conversation system itself to handle repeat encounters differently.

---

### 10.3. DEPIEDRANO_DEHIELO (text[30]) — Room 3 Street NPC Dialog

**Dispatch**: Extra 308, Room-Specific Script type 0x01 (table at `0x47D24`, entry 47 — last entry)
**Handler address**: `0x20C17` — ~1952 bytes (to ~`0x213B7`), the largest single handler in the game
**Room**: 3 (Street — outside the shop, with lamppost)
**Action**: Room-specific script — a massive handler managing all Room 3 NPC interactions
**ScummVM function**: `moveCable()` handles hotspot PICKUP on Extra 308 (lamppost cable), but the room script is a separate dispatch path

#### Handler Structure Overview

The Extra 308 handler at `0x20C17` is an enormous room script containing **multiple sub-handlers** separated by `ret` instructions. The entry point (`0x20C17`) initializes room state flags, and subsequent sub-handlers (reached via internal jumps from the room script's dispatch logic) manage individual interactions.

**Text references found in this handler:**

| Address | Text Index | Text Content | Speaker |
|---------|------------|--------------|---------|
| 0x20CFB | 8 | "¡Qué buena está!" | NPC |
| 0x20D33 | **30** | **"De piedra no. DE HIELO"** | **NPC** |
| 0x20D40 | 31 | "¡OYE! No empecemos" | Alfred |
| 0x20D5D | 32 | "Ya está la 'cuerpo danone' vacilando" | NPC |
| 0x20D6D | 33 | "Cállate. Cabeza hueca!" | Alfred |
| 0x20D83 | 34 | "¡Eso lo serás tú!" | NPC |
| 0x20D96 | 35 | "¡Demasiado! No me dejas pensar" | Alfred |
| 0x20DA9 | 36 | "Un poco de respeto por favor" | NPC |
| 0x20E25 | 41 | "¿Tú crees?" | NPC |
| 0x2122E | 49 | "Trabajaría mejor si no me molestara" | NPC |

#### Sub-Handler at 0x20D28 (contains text[30])
```
0x20D28: push 0x08; call __STK; push edx        ; sub-handler prologue
0x20D33: mov edx, [0xBA2C]                       ; text_ptrs[30] = DEPIEDRANO_DEHIELO
0x20D39: xor eax, eax                            ; character 0 = NPC
0x20D3B: call display_text_with_character_animation
0x20D40: mov edx, [0xBA30]                       ; text_ptrs[31] = NO_EMPECEMOS
0x20D46: mov eax, 0x01                           ; character 1 = Alfred
0x20D4B: jmp display_and_return                  ; display text[31] then return
```

#### Game Context

Text[30] is part of an **escalating NPC banter sequence** in Room 3. The NPC (likely a female character at the lamppost or doorway) makes progressively more pointed remarks, and Alfred responds with increasing annoyance:

1. NPC: "¡Qué buena está!" (She's so fine!) — text[8]
2. **NPC: "De piedra no. DE HIELO" (Not made of stone. OF ICE) — text[30]** ← *this one*
3. Alfred: "¡OYE! No empecemos" (HEY! Don't start!) — text[31]
4. NPC: "Ya está la 'cuerpo danone' vacilando" (There goes 'hot body' teasing) — text[32]
5. Alfred: "Cállate. Cabeza hueca!" (Shut up. Airhead!) — text[33]
6. NPC: "¡Eso lo serás tú!" (That's what YOU are!) — text[34]
7. Alfred: "¡Demasiado! No me dejas pensar" (Too much! You don't let me think) — text[35]
8. NPC: "Un poco de respeto por favor" (A little respect please) — text[36]

The room script likely increments a counter each time the player interacts, selecting the next dialog pair in the sequence. The previous exchange context: "Not made of stone" (implying Alfred is cold) → "DE HIELO" (OF ICE — emphasizing the point) → Alfred's retort "Don't start!"

#### Entry Point Handler (0x20C17)
The room entry sub-handler at `0x20C17` initializes 4 flags to 1 (`0x49847`, `0x4984E`, `0x49855`, `0x498BE`) and loads 3 visual resources via `load_sticker_from_alfred6`. This sets up Room 3's initial visual state each time the player enters.

#### Not a Sphinx/Ice Puzzle
The previous table description ("Sphinx/ice puzzle dialog") was incorrect. This is a **flirtatious NPC banter** sequence in Room 3's street scene, not a puzzle dialog.

---

### 10.4. AQUI_NO_NECESITO (text[139]) — Spellbook Self-Use

**Dispatch**: Complex Item table type 0x200 (table at `0x48118`), items 88×88 (use item on itself)
**Handler address**: `0x23310` — 1447 bytes (to `0x238B7`)
**Room**: Any (handler checks current room)
**Action**: Player uses the **spellbook** (inventory item 88) on itself (i.e., reads/casts from it)
**ScummVM function**: `useOnAlfred()` case 88 in [actions.cpp](actions.cpp)

#### Original Handler — Pseudocode
```c
void handler_use_spellbook_on_self(void) {          // 0x23310
    uint16 room = current_room_id;                    // [0x4FB94], 16-bit read

    if (room >= 51 && room <= 54) {
        goto flight_spell_handling;                   // → 0x23346
    }
    if (room == 28) {
        goto room28_spell_handling;                   // → 0x23346 (shared entry)
    }
    // ALL OTHER ROOMS:
    alfred_say(text[139]);                            // AQUI_NO_NECESITO: "Aquí no lo necesito"
    return;

flight_spell_handling:                                // 0x23346
    // Open spellbook UI, select spell page
    // Play hawk-god incantation: text[140+page] (DIOSHALCON variants)
    // Check if correct spell for current flight room
    // If correct: defeat sorcerer animation, update FLAG_COMO_ESTAN_LOS_DIOSES
    // ...extensive flight combat spell logic...
    return;

room28_spell_handling:
    // Open spellbook UI, select spell page
    // Play hawk-god incantation: text[200+page] (DIOSHALCON_2 variants)
    // If page 12 (correct spell): teleport to Room 25
    //   → alfred_say(text[78]): MENUDAAVENTURA "¡Menuda aventura!"
    return;
}
```

#### Key x86 Decode (Room Check at 0x23310)
```
0x23310: push 0x40; call __STK                     ; 64 bytes stack check
0x2331A: push ebx/ecx/edx/esi/edi/ebp; sub esp, 8 ; save all + 8 local bytes
0x23325: xor eax, eax
0x23327: mov ax, [0xFB94]                           ; current_room_id (16-bit word)
0x2332B: cmp eax, 0x33                              ; room 51
0x2332E: jl 0x23335                                 ; if < 51, skip range check
0x23330: cmp eax, 0x36                              ; room 54
0x23333: jle 0x23346                                ; if 51 <= room <= 54, → spell handling
0x23335: xor eax, eax
0x23337: mov ax, [0xFB94]                           ; reload room ID
0x2333D: cmp eax, 0x1C                              ; room 28
0x23340: jnz 0x2386F                                ; if NOT room 28, → AQUI_NO_NECESITO
; Rooms 28, 51-54 fall through to spell handling at 0x23346

; ...1300+ bytes of spellbook/flight/teleport logic...

; AQUI_NO_NECESITO path:
0x23870: mov eax, [0xBBE0]                          ; text_ptrs[139] = AQUI_NO_NECESITO
0x23875: call display_text_with_voice               ; (0x25488) — Alfred speaks
0x2387A: jmp cleanup_and_return                     ; (0x243BF)
```

#### Room Check Logic
```
Room 51-54 (flight rooms) ──→ Flight spell combat (DIOSHALCON incantations)
Room 28 (witchcraft cave)  ──→ Cave spell casting (DIOSHALCON_2 + teleport on page 12)
Any other room             ──→ "Aquí no lo necesito" (I don't need it here)
```

The original checks rooms 51-54 as a **range** (`cmp 51; jl; cmp 54; jle`), correctly covering all 4 flight rooms. This matches the ScummVM `case 51: case 52: case 53: case 54:` implementation.

#### ScummVM Bug: Missing AQUI_NO_NECESITO Text

Current ScummVM implementation in `useOnAlfred()`:
```cpp
case 88: {
    SpellBook spellBook(_events, _res);
    playAlfredSpecialAnim(0);
    Spell *spell = spellBook.run();
    if (spell) {
        _alfredState.direction = ALFRED_LEFT;
        switch (_room->_currentRoomNumber) {
        case 28: /* ... room 28 handling ... */ break;
        case 51: case 52: case 53: case 54: /* ... flight handling ... */ break;
        default:
            break;  // ← BUG: should show AQUI_NO_NECESITO
        }
    }
    break;
}
```

**Bug**: The `default` case does nothing. In the original, using the spellbook in any room besides 28 or 51-54 displays "Aquí no lo necesito." Additionally, in the original, the room check happens **before** opening the spellbook UI — the player never sees the spellbook interface if they're in the wrong room. The ScummVM code opens the spellbook first, lets the player select a spell, and then silently ignores it in the wrong room.

**Fix**: Move the room check *before* the SpellBook UI, and show `AQUI_NO_NECESITO` if the room doesn't match:
```cpp
case 88: {
    if (_room->_currentRoomNumber != 28 &&
        (_room->_currentRoomNumber < 51 || _room->_currentRoomNumber > 54)) {
        _dialog->say(_res->_ingameTexts[AQUI_NO_NECESITO]);
        break;
    }
    SpellBook spellBook(_events, _res);
    // ... rest of spell handling ...
}
```

#### Text References in Handler
| Address | Text Index | Content | Context |
|---------|------------|---------|---------|
| 0x2353A | 200 | "Dios-halcón, rey de los cielos..." | DIOSHALCON_2 — room 28 incantation |
| 0x23665 | 140 | "Dios-halcón, rey de los cielos..." | DIOSHALCON — flight room incantation |
| 0x2385A | 78 | "¡Menuda aventura!" | MENUDAAVENTURA — after teleport to Room 25 |
| 0x23870 | **139** | **"Aquí no lo necesito"** | **AQUI_NO_NECESITO — wrong room rejection** |

---

### 10.5. Summary of ScummVM Bugs Found

| Bug | Severity | Text Missing | Fix Difficulty |
|-----|----------|--------------|----------------|
| `openKitchenDrawer` missing "already opened" check | **Medium** — item/sticker duplicated on repeat opens | YAESTA_ABIERTO (text[55]) | Easy — add flag check |
| `useOnAlfred` case 88 missing wrong-room rejection | **Low** — spellbook UI opens silently in wrong rooms | AQUI_NO_NECESITO (text[139]) | Easy — add room guard before SpellBook UI |
| `pickupSunflower` missing repeat-encounter alertness text | **Low** — uses different mechanism (conversation system) | LEESTOYVIGILANDO (text[84]) | Investigate — may be handled by conversation tree |

---

## 11. Inventory Item Sound Table Corrections

### Background
The `inventorySounds[113]` table in `menu.h` maps each item ID to a sound filename
played when the player clicks an item in the inventory menu. The original table is at
EXE offset `0x439CB` (Ghidra `0x407CB`), 113 entries × 13 bytes each.

### Issue
19 entries were incorrectly set to `HOJASZZZ.SMP` (leaf rustle, "hojas" = leaves in
Spanish) when they should be `11ZZZZZZ.SMP` (generic click SFX). The error likely
arose from defaulting unknown items to `HOJASZZZ.SMP` instead of verifying against
the EXE data.

### Corrected Items
| Item ID | Was (ScummVM) | Should Be (EXE) |
|---------|---------------|-----------------|
| 9 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 70 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 71 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 72 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 74 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 75 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 77 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 78 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 81 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 82 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 85 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 90 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 92 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 99 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 102 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 103 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 105 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 107 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |
| 109 | HOJASZZZ.SMP | 11ZZZZZZ.SMP |

### Verification Method
Extracted directly from JUEGO.EXE at file offset `0x439CB` (data segment Ghidra
address `0x407CB`). The pointer table at Ghidra `0x490F8` indexes into this table via
`[item_id * 4 + 0x490F8]`, and each entry stores `0x7CB + item_id * 13`.

The inventory click handler at Ghidra `0x12DA7` loads the sound into slot 7 via:
```asm
MOV EAX, [EBX*4 + 0x490F8]   ; sound filename for item_id
CALL load_sound_file           ; loads into slot 7
CALL play_ambient_sound        ; plays via Miles Sound System
```

### Note on Sound Names
- `HOJASZZZ.SMP` = "hojas" (leaves) → leaf rustle sound
- `11ZZZZZZ.SMP` = generic click SFX (effectively a neutral selection sound)
- The game does NOT play any sound during item pickup (`process_inventory_action`
  at `0x24157` has no sound call). Sounds only play in the inventory menu.

---

## 12. Sliding Puzzle Shuffle Scaling

### Background
The screensaver sliding puzzle (`screensaver_sliding_puzzle` at Ghidra `0x26879`)
cycles through 4 tile sizes on each activation: 80, 40, 20, 10 pixels. This produces
grids of 40, 160, 640, and 2560 tiles respectively.

### Original Behavior (Ghidra)
The shuffle loop performs exactly **1 swap per iteration** with no artificial delay:
```c
do {
    wait_or_process_input();
    pos1 = random() & mask;  // bitmask rejection sampling
    pos2 = random() & mask;
    while (pos1 >= tile_count || pos2 >= tile_count) { ... retry ... }
    puzzle_swap_tiles(pos1, pos2);
    present_frame_to_screen();
    play_ambient_sound();
} while (!check_keyboard_input());
```

On 1997 hardware, the VGA blit (`present_frame_to_screen` copies 256KB to video
memory) dominated the loop timing. The pixel swap in `puzzle_swap_tiles` copies
`tile_size - 1` squared pixels per swap. With no delay, the loop runs as fast as
rendering allows.

### Issue in ScummVM
ScummVM's `shuffleLoop()` had a fixed `g_system->delayMillis(10)` per swap,
giving ~100 swaps/second regardless of tile size. For 80px tiles (40 tiles),
this looked reasonable. For 10px tiles (2560 tiles), each swap affects only
~100 pixels out of 256,000 — the visual scrambling was imperceptibly slow
compared to the original where rendering dominated and swaps were rapid.

### Fix
Scale the number of swaps per visual frame proportionally to tile count:
```
swapsPerFrame = totalTiles / baseTileCount
```
where `baseTileCount = 40` (the count for the largest tile size). This gives:

| Tile Size | Tiles | Swaps/Frame | Equivalent Visual Rate |
|-----------|-------|-------------|----------------------|
| 80px | 40 | 1 | Same as before |
| 40px | 160 | 4 | 4× more swaps per frame |
| 20px | 640 | 16 | 16× more swaps per frame |
| 10px | 2560 | 64 | 64× more swaps per frame |

This approximates the original's behavior where smaller tiles (less work per swap)
resulted in proportionally more swaps being visible per time unit.

### Mask Table (Ghidra 0x4B7B0)
The original uses bitmask rejection sampling instead of modular arithmetic:

| Index | Tile Size | Tiles | Mask | Purpose |
|-------|-----------|-------|------|---------|
| 0 | 80 | 40 | 0x3F | Next power-of-2 − 1 above 40 |
| 1 | 40 | 160 | 0xFF | Next power-of-2 − 1 above 160 |
| 2 | 20 | 640 | 0x3FF | Next power-of-2 − 1 above 640 |
| 3 | 10 | 2560 | 0xFFF | Next power-of-2 − 1 above 2560 |

---

## 13. Anti-Piracy Effect (Action 348) — Bug Fixes

### Background
Action 348 is triggered in Room 22 when the player agrees to pirate the game. The
handler at Ghidra `0x21F3D` (not a recognized function boundary) simulates a system
crash with screen corruption and PC speaker noise, then performs an intentional
divide-by-zero to crash to DOS.

### Original Behavior (from Ghidra disassembly at 0x21F3D)
1. **Setup**: Set `room_buffer[5] = 2`, call `init_or_stop_sound(0)` to stop all audio
2. **Corruption loop** (runs until keypress):
   - `random() * (random() & 0xF)` → write result to `[0x4FADC]` (background buffer
     pointer), corrupting where `copy_background_to_front_buffer` reads from
   - `present_frame_to_screen()` → shows garbage memory on screen
   - Read sequential memory byte `[EBX]` (EBX starts at 0, increments each frame)
     → write to I/O port `0x61` (PC speaker) → produces buzzy, semi-periodic noise
3. **On keypress**: Clear flag at `[0x1179E]`, then `IDIV EBX` with `EBX=0` → divide
   by zero → crash to DOS

### Bugs in Previous ScummVM Implementation
1. **Use-after-free**: `noiseData` buffer passed with `DisposeAfterUse::YES` to
   `makeRawStream`, which frees it when playback ends. The loop then re-passes
   the freed pointer to `playSound` on subsequent iterations.
2. **WAV header fed as raw PCM**: The `playSound(byte*, uint32, int)` overload
   treats the entire buffer as raw unsigned 8-bit PCM at 11025Hz, but the code
   included a 44-byte WAV header declaring 8000Hz — the header bytes played as
   audio garbage, and the sample rate was wrong.
3. **Audible gaps**: 1-second noise buffer at 11025Hz with 50ms polling delay
   caused periodic silence gaps between noise bursts.
4. **Visual mismatch**: Pure random pixels don't match the original's behavior
   of reading from corrupted memory addresses, which produces structured visual
   patterns (code segments, data tables, IVT).

### Fix
- Use `Audio::makeLoopingAudioStream` with raw PCM data for continuous, gap-free
  noise playback. The looping stream owns the buffer and avoids use-after-free.
- Generate noise as a sawtooth pattern (sequential byte increment `0x00→0xFF→...`)
  matching the original's `MOV DL, [EBX]; INC EBX` behavior that reads sequential
  memory bytes. At 8000Hz sample rate this produces the characteristic buzzy tone.
- Visual corruption uses structured patterns from the composite buffer (current
  screen state) read at shifting offsets, simulating the original's corrupted
  background buffer pointer reading from arbitrary memory addresses.
- Access mixer directly via `g_system->getMixer()` instead of through private
  `SoundManager::_mixer`.
- On keypress: `Engine::quitGame()` returns to launcher (ScummVM equivalent of
  the original's divide-by-zero crash to DOS).
