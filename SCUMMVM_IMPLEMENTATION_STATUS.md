# ScummVM Implementation Status — Complete Cross-Reference

This document cross-references every documented action handler from the original JUEGO.EXE against the ScummVM pelrock engine implementation. It covers three dispatch systems plus room init handlers, identifying what is **complete**, **incomplete**, or **missing**.

---

## Summary

| System | Total Entries | Unique Handlers | Complete | Incomplete | Missing |
|--------|--------------|-----------------|----------|------------|---------|
| F8 Action Codes | 116 | ~85 | 83 | 2 | 31 |
| Item Combinations | 113 (42 unique) | 42 | 27 | 3 | 12 |
| Verb Actions | 94 | 94 | 80 | 0 | 14 |
| Room Init Dispatch | 35 | ~20 | 13 | 2 | 20 |
| **Total** | **358** | — | **203** | **7** | **77** |

---

## 1. F8 Action Codes (Dialog Triggers)

These are triggered via the `0xF8` control code in conversation data. Implemented in `dialogActionTrigger()` and `performActionTrigger()`.

### Status Key
- **Complete**: Handler exists and matches documented behavior
- **Incomplete**: Handler exists but missing some behavior
- **Missing**: No handler in ScummVM

### Complete Actions (83)

| Action | Room | Description | ScummVM Location |
|--------|------|-------------|------------------|
| 257 | 0 | Intro cutscene (portrait view) | `performActionTrigger` |
| 258 | 4 | Flag + conv advance (door kicking) | `dialogActionTrigger` |
| 259 | 5 | NPC dialog (statues) | `dialogActionTrigger` |
| 260 | 5 | NPC dialog (statues) | `dialogActionTrigger` |
| 261 | 5 | NPC dialog (statues) | `dialogActionTrigger` |
| 262 | 5 | NPC dialog (statues) | `dialogActionTrigger` |
| 263 | 5 | NPC dialog (statues) | `dialogActionTrigger` |
| 264 | 7 | Conv advance (time traveler) | `dialogActionTrigger` |
| 268 | 7 | NPC dialog (statue description) | `performActionTrigger` |
| 270 | 9 | Library computer system | `performActionTrigger` → `COMPUTER` state |
| 271 | 9 | NPC dialog (librarian) | `performActionTrigger` |
| 272 | 14 | Conv advance (negotiation) | `dialogActionTrigger` |
| 274 | 18 | Conv advance (newspaper editor) | `dialogActionTrigger` |
| 275 | 18 | Conv advance (newspaper editor) | `dialogActionTrigger` |
| 276 | 18 | Conv advance (newspaper editor) | `dialogActionTrigger` |
| 277 | 18 | Conv advance + flags (Fidel Castro headline) | `dialogActionTrigger` |
| 278 | 20 | Conv advance (travel agency) | `dialogActionTrigger` |
| 279 | 20 | Travel to Egypt sequence | `dialogActionTrigger` → `travelToEgypt()` |
| 280 | 20 | NPC dialog (hotel description) | `performActionTrigger` |
| 281 | 20 | NPC dialog (hotel description) | `performActionTrigger` |
| 282 | 20 | NPC dialog (hotel description) | `performActionTrigger` |
| 285 | 26 | Arrest (shared handler) | `dialogActionTrigger` → `toJail()` |
| 286 | 27 | Conv + give item 83 | `dialogActionTrigger` |
| 287 | 27 | Give items + counter (merchant) | `dialogActionTrigger` |
| 288 | 27 | Give items + counter (merchant) | `dialogActionTrigger` |
| 289 | 27 | Give items + counter (merchant) | `dialogActionTrigger` |
| 290 | 27 | Give items + counter (merchant) | `dialogActionTrigger` |
| 291 | 30 | Arrest (shared handler) | `dialogActionTrigger` → `toJail()` |
| 292 | 31 | Conv advance (prison cellmate) | `dialogActionTrigger` |
| 293 | 31 | Persist + conv (cellmate reveals tunnel) | `dialogActionTrigger` |
| 295 | 26 | Conv + give item 84 | `dialogActionTrigger` |
| 296 | 22 | Conv advance (market NPC 1) | (not directly in switch but covered via combo gate) |
| 314 | 43 | Give item 93 (sand liquor) | `dialogActionTrigger` |
| 316 | 43 | Give item 94 (sun cream) | `dialogActionTrigger` |
| 317 | 43 | Give item 95 | `dialogActionTrigger` |
| 318 | 43 | Give item 96 | `dialogActionTrigger` |
| 319 | 43 | Give item 97 (pyramid map) + conv | `dialogActionTrigger` |
| 320 | 43 | Conv advance (return map) | `dialogActionTrigger` |
| 321 | 45 | Conv + sound (girls invite bath) | `dialogActionTrigger` |
| 324 | 43 | Conv + persist (architect proof) | `dialogActionTrigger` |
| 325 | 49 | Counter gate (mummy recognition) | `dialogActionTrigger` |
| 326 | 49 | Conv advance (mummy directions) | `dialogActionTrigger` |
| 327 | 29 | Set visited flag (museum) | `performActionTrigger` |
| 328 | 2 | Conv advance (girlfriend) | `dialogActionTrigger` |
| 329 | 2 | Set flag (girlfriend state) | `dialogActionTrigger` |
| 330 | 22 | Give item 102 (market merchant) | `dialogActionTrigger` |
| 331 | 22 | NPC dialog (market merchant) | `dialogActionTrigger` |
| 332 | 22 | Conditional give item 104 | `dialogActionTrigger` |
| 333 | 22 | NPC dialog (market merchant) | `dialogActionTrigger` |
| 334 | 22 | Conv + give item 86 | `dialogActionTrigger` |
| 335 | 22 | Give item 103 (oranges) | `dialogActionTrigger` |
| 336 | 22 | NPC dialog (market merchant) | `dialogActionTrigger` |
| 337–347 | 22 | Conv advance (branches 2–12) | `dialogActionTrigger` |
| 348 | 22 | Anti-piracy effect | `dialogActionTrigger` → `antiPiracyEffect()` |
| 349 | 22 | Combo gate bit 0 | `dialogActionTrigger` |
| 350 | 22 | Combo gate bit 1 | `dialogActionTrigger` |
| 351 | 22 | 18-line cutscene dialog | `dialogActionTrigger` |
| 352 | 23 | Arrest (shared handler) | `dialogActionTrigger` → `toJail()` |
| 353 | 23 | Conv advance (farewell kiss) | `dialogActionTrigger` |
| 354 | 23 | Give item 105 (photocopy) | `dialogActionTrigger` |
| 355 | 23 | Arrest (shared handler) | `dialogActionTrigger` → `toJail()` |
| 356 | 23 | Conv advance (condom exchange) | `dialogActionTrigger` |
| 357 | 25 | Wrong answer -1 (poetry quiz) | `dialogActionTrigger` |
| 358 | 25 | Wrong answer -2 (poetry quiz) | `dialogActionTrigger` |
| 359 | 25 | Correct answer (poetry quiz) | `dialogActionTrigger` |
| 360 | 25 | Reset counter (poetry quiz) | `dialogActionTrigger` |
| 361 | 25 | "I don't know" (poetry quiz) | `dialogActionTrigger` |
| 362 | 25 | Special trigger (cheat code flag) | `dialogActionTrigger` |
| 363 | 25 | Arrest (shared handler) | `dialogActionTrigger` → `toJail()` |
| 364 | 25 | Riddle wrong answer | `dialogActionTrigger` |
| 365 | 25 | Riddle correct answer | `dialogActionTrigger` |
| 366 | 25 | Conv advance (philosopher) | `dialogActionTrigger` |
| 367 | 25 | Accept riddle | `dialogActionTrigger` |
| 369 | 26 | Conv advance (prostitute haggling) | `dialogActionTrigger` |
| 370 | 27 | Give item 111 | `dialogActionTrigger` |
| 371 | 27 | Give items 111+110 + conv | `dialogActionTrigger` |
| 375 | 52 | Endgame cutscene | `performActionTrigger` → `teletransportToPrincess()` |
| 376 | 45 | Fight animation + conv | `dialogActionTrigger` |
| 377 | 45 | Conv advance (oasis) | `dialogActionTrigger` |
| 378 | 49 | Conv advance (father confession) | `dialogActionTrigger` |
| 380 | — | Turn lights off (screen effect) | `dialogActionTrigger` → `turnLightsOff()` |
| 383 | 26 | Conv advance (romantico exchange) | `dialogActionTrigger` |

### Incomplete Actions (2)

| Action | Room | Description | What's Missing |
|--------|------|-------------|----------------|
| 267 | 7 | Animation + conv + give item 8 (time traveler gives secret code) | Only conv advance is implemented (`case 267: setCurrentRoot(7, 2, 0)`). Missing: sprite animation sequence before giving item, and `addInventoryItem(8)`. Original performs sprite anim loop, then advances conv, then gives item 8. |
| 273 | 14 | Persist conversation (Baiona/Galicia exchange) | Partially implemented — adds walkboxes but falls through to case 274 without `break`. Missing: persistence to ALFRED.1 file I/O and flag settings `[0xFB74]=1, [0xFB75]=3`. Also the walkbox add logic runs then falls through. |

### Missing Actions (31)

| Action | Room | Description | Original Behavior |
|--------|------|-------------|-------------------|
| 294 | 31 | Persist flag (toilet examined) | Sets room data byte `[0x527]=1`, persists to ALFRED.1. Marks toilet as examined in prison cell so the game remembers on reload. |
| 297 | 34 | Conv + persist (show magazine to palace guard) | `update_conversation_state(room=34, npc=0, branch=2)` + sets room data `[0x1C1]=1` → persists to ALFRED.1. Opens new guard dialog path after seeing the magazine. |
| 298 | 25 | Conv + sprite recheck | `update_conversation_state(room=25, npc=0, branch=3)` + `check_sprite_hover(2, 0)`. Used in philosopher room to advance conversation and recheck sprite hover state. |
| 299 | 25 | Conv + flag (philosopher state) | `update_conversation_state(room=25, npc=0, branch=1)` + sets `[0x95D0]=1`. Sets philosopher state flag for tracking conversation progress. |
| 300 | 25 | Conv advance to branch 5 | `update_conversation_state(room=25, npc=0, branch=5)`. Part of philosopher conversation progression. |
| 301 | 25 | Conv advance to branch 6 | `update_conversation_state(room=25, npc=0, branch=6)`. |
| 302 | 25 | Conv advance to branch 7 | `update_conversation_state(room=25, npc=0, branch=7)`. |
| 303 | 25 | Conv advance to branch 8 | `update_conversation_state(room=25, npc=0, branch=8)`. |
| 304 | 25 | Conv advance to branch 9 | `update_conversation_state(room=25, npc=0, branch=9)`. |
| 305 | 25 | Conv advance to branch 10 | `update_conversation_state(room=25, npc=0, branch=10)`. |
| 306 | 25 | Conv advance to branch 3 (loop back) | `update_conversation_state(room=25, npc=0, branch=3)`. Loops philosopher conversation back. |
| 307 | 37 | Persist room data (hotspot count) | Sets `room_data[0x47C]=8` → persists to ALFRED.1. Reveals hidden hotspots in maze/passage room after puzzle trigger. Critical for making the stone pickup (item 90) accessible. |
| 308 | 41 | NPC text swap (guard dialog change) | `setup_npc_conversation_text(room=41, npc=0, expected=16, new=2)`. Changes which conversation root the prison guard NPC uses after various interactions. Without this, the guard's dialog trees don't progress. |
| 313 | 41 | Conv advance (guard conversation) | `update_conversation_state(room=41, npc=0, branch=1)`. Advances the guard's conversation after Egyptian riddle, beer jar, or flirting dialog options. |
| 322 | 47 | NPC dialog (examine pyramid plans) | Displays dialog from text pointer `[0xBB28]`. Description-triggered dialog when examining the pyramid plans in the architect's room. |
| 323 | 47 | Dual conv advance (architect door puzzle) | `update_conversation_state(room=47, npc=0, branch=1)` + `update_conversation_state(room=43, npc=0, branch=3)`. After the architect reveals the door puzzle — advances both room 47 and room 43 conversations simultaneously. |
| 368 | 26 | No-op placeholder | Documented as a dead placeholder handler. Does nothing. Not critical. |
| 372 | 34 | Conv advance (palace guard branch 2) | `update_conversation_state(room=34, npc=0, branch=2)`. Guard dialog branch after various excuses. |
| 373 | 34 | Conv advance (palace guard branch 3) | `update_conversation_state(room=34, npc=0, branch=3)`. |
| 374 | 34 | Conv advance (palace guard branch 1) | `update_conversation_state(room=34, npc=0, branch=1)`. |
| 381 | — | Mid-function code (lights sequence) | Part of a larger routine related to actions 380/382. Likely a continuation of the screen effect sequence. |
| 382 | — | Sound sequence (lights sound) | Loads sound 361 into slot 6, plays 3× loop, waits for completion. Audio companion to the lights-off effect (380). |

#### Missing Room 25 Actions (298–306) — Implementation Notes

Actions 298–306 are all simple conversation advances for the philosopher room. They follow the same pattern:

```cpp
case 298:
    _state->setCurrentRoot(25, 3, 0);
    // TODO: check_sprite_hover(2, 0) - recheck if sprite 2 is hovered
    break;
case 299:
    _state->setCurrentRoot(25, 1, 0);
    _state->setFlag(FLAG_PHILOSOPHER_STATE, 1); // needs new flag
    break;
case 300: _state->setCurrentRoot(25, 5, 0); break;
case 301: _state->setCurrentRoot(25, 6, 0); break;
case 302: _state->setCurrentRoot(25, 7, 0); break;
case 303: _state->setCurrentRoot(25, 8, 0); break;
case 304: _state->setCurrentRoot(25, 9, 0); break;
case 305: _state->setCurrentRoot(25, 10, 0); break;
case 306: _state->setCurrentRoot(25, 3, 0); break;
```

#### Missing Room 34 Actions (297, 372–374) — Implementation Notes

These handle the palace guard conversation. The guard has multiple dialog branches:

```cpp
case 297:
    _state->setCurrentRoot(34, 2, 0);
    // TODO: persist room_data[0x1C1]=1 to ALFRED.1
    break;
case 372: _state->setCurrentRoot(34, 2, 0); break;
case 373: _state->setCurrentRoot(34, 3, 0); break;
case 374: _state->setCurrentRoot(34, 1, 0); break;
```

#### Missing Room 41 Actions (308, 313) — Implementation Notes

These manage the pyramid guard/slave dialog progression:

```cpp
case 308:
    // Change NPC conversation root: setup_npc_conversation_text(41, 0, 16, 2)
    // This swaps which conversation tree the NPC shows
    _state->setCurrentRoot(41, 2, 0); // approximate
    break;
case 313:
    _state->setCurrentRoot(41, 1, 0);
    break;
```

---

## 2. Item Combinations

These are triggered when the player uses an inventory item on a hotspot or on itself. Implemented in `combinationTable[]` and `useOnAlfred()`.

### Complete (27 unique handlers)

| # | Items | Handler | ScummVM Function |
|---|-------|---------|-----------------|
| 0 | credit_card(2) + ATM(281) | `0x227B2` | `useCardWithATM` |
| 1 | brick(4) + shop_window(294) | `0x2284B` | `useBrickWithWindow` |
| 2 | brick(4) + storefront(295) | `0x22AF7` | `useBrickWithShopWindow` |
| 3 | cord(6) + plug(315) | `0x22B0B` | `useCordWithPlug` |
| 4 | money(5) + guard(309) | `0x22C58` | `giveMoneyToGuard` |
| 5 | ID(1) + guard(309) | `0x22BF9` | `showIdToGuard` |
| 6 | amulet(7) + statue(353) | `0x22CC1` | `useAmuletWithStatue` |
| 7 | secret_code(8) + librarian(347) | `0x22E10` | `giveSecretCodeToLibrarian` |
| 9 | secret_code(8) + merchant(358) | `0x22E51` | `useBrickWithLibrarian` (repurposed) |
| 10 | brick(4) + merchant(358) | `0x22EA1` | `useBrickWithLibrarian` |
| 14 | spicy_sauce(62) + counter(373) | `0x22EC0` | `useSpicySauceWithBurger` |
| 8 | letter(9) self-use | `0x22E3D` | `useOnAlfred` case 9 |
| 17 | item 34 self-use | `0x22F7B` | `useOnAlfred` case 34 |
| 18 | recipe(59) self-use | `0x22F96` | `useOnAlfred` case 59 |
| 19 | item 17 self-use | `0x22FD5` | `useOnAlfred` case 17 |
| 21 | newspaper(83) + desk(461) | `0x23108` | `useDollWithBed` |
| 22 | pumpkin(76) + travel_agency(469) | `0x231C9` | `usePumpkinWithRiver` |
| 23 | computer(88) self-use | `0x23310` | `useOnAlfred` case 88 (SpellBook) |
| 24 | museum_pass(87) self-use | `0x2387E` | `useOnAlfred` case 87 |
| 25 | photo(84) + Egypt(503) | `0x23892` | `giveMagazineToGuard` |
| 26–28, 37 | items 85/86/90/81 + temple(506) | `0x2395D` | `magicFormula` |
| 29 | item 99 + temple(506) | `0x2446C` | `useWigWithPot` |
| 30–31 | stone(91)/mud(92) + slave(601) | `0x239DD` | `giveStoneToSlaves` |
| 34 | pumpkin(76) + pyramid(617) | `0x2413E` | `usePumpkinWithPond` |
| 36 | orange(86) + egypt_merch(500) | `0x24245` | `giveWaterToGuard` |
| 39 | key(100) + portrait(650) | `0x2454C` | `useKeyWithPortrait` |
| 33 | orange(86) + bazaar(614) | `0x23F83` | `useWaterOnFakeStone` |
| 43 | CD_player(95) self-use | `0x246F4` | `useOnAlfred` case 95 (CDPlayer) |
| 45–78 | store items 11–47 self-use | `0x25471` | `useOnAlfred` default (11–47 range) |
| 79–112 | store items 11–47 + merchant | `0x25525` | `noOpItem` (handles 11–47 + 358) |

### Incomplete (3 unique handlers)

| # | Items | Handler | What's Missing |
|---|-------|---------|----------------|
| 11 | recipe(63) self-use | `0x22FF7` | `useOnAlfred` case 63 triggers cooking anim. **Missing**: Full cooking cutscene sequence — original performs `playAlfredSpecialAnim(1)`, loads extra screen #3, updates conversation states for rooms 17 and 18. Current impl loads extra screen but may be missing conv updates to rooms 17/18. |
| 38 | photo(84) self-use | `0x2448A` | `useOnAlfred` case 84 loads extra screen #7. **Missing**: Original also displays NPC dialog text from pointer table — may need additional dialog lines. |
| 40 | item 101 self-use | `0x2462B` | `useOnAlfred` case 101 reads letter with `playAlfredSpecialAnim(1)` and says dialog. Currently sets flag but **missing**: may need to show the combination text (original reads from text pointer and displays with character anim). |

### Missing (12 unique handlers)

| # | Items | Handler | Type | Original Behavior |
|---|-------|---------|------|-------------------|
| 12–13 | soda(60)/cola(61) + counter(373) | `0x22EB5` | HOTSPOT+ITEM | **Give drink at fast-food counter.** Shows Alfred putting the drink on the counter. Calls `display_text_with_voice` (Alfred asks "¿Quiere tomar algo?"). Important for triggering the boss's meal sequence — the boss needs a drink with the hamburger. Without this, the boss arrest cutscene can't trigger correctly. |
| 15 | item 0 self-use | `0x22F07` | SELF-USE | **Guard check / "nothing" item.** Checks if guard is present; if yes, triggers a dialog about pretending to be busy. Context unclear — may be triggered from the travel agency or prison room. |
| 16 | ketchup(24) self-use | `0x22F22` | SELF-USE | **Use ketchup on hamburger (combine items).** Reads intelligence book item and combines ketchup with hamburger. Calls `playAlfredSpecialAnim(0)`, updates conversation state, may transform items. Related to the cooking puzzle — Alfred needs to put ketchup on the hamburger to serve the boss. |
| 20 | hamburger(64) self-use | `0x23088` | SELF-USE | **Use hamburger (feeding cutscene).** Complex 415-byte handler. Performs a multi-step feeding sequence: Alfred plays eating animation, camera movement, NPC reaction dialog. This is the boss-eating-hamburger cutscene that can trigger the arrest if the spicy sauce was added. |
| 32 | fight_item(97) self-use | `0x23F03` | SELF-USE | **Use fight item (fight cutscene).** Triggers a fight animation cutscene. 128 bytes. Calls `play_fight_animation()` with specific parameters for the fight sequence. Context: likely used in a room where Alfred needs to fight an NPC. |
| 35 | item 98 self-use | `0x241E8` | SELF-USE | **Use pyramid map on self.** 93 bytes. Displays the pyramid map as an overlay screen. Alfred reads the map showing which door is correct in the pyramid. Calls `loadExtraScreen` to show map graphic, then returns. Important for the pyramid puzzle navigation. |
| 41 | item 108 self-use | `0x2464E` | SELF-USE | **Puzzle pieces mini-game screen (patches).** 108 bytes. One of the components for repairing the doll. When used alone, checks if the other repair items (109, 110) are in inventory. If all three present (108+109+110), combines them into item 83 (repaired doll). Otherwise shows dialog about missing parts. |
| 42 | item 109 self-use | `0x246BA` | SELF-USE | **Puzzle pieces mini-game screen (glue).** 58 bytes. Same logic as item 108 — checks for items 108 and 110 to combine into item 83. |
| 44 | art_gallery(96) self-use | `0x24ED7` | SELF-USE | **Background Art Gallery viewer.** 1500+ bytes, very complex. Displays a full-screen art gallery with scrollable background images from the game's rooms. Player can browse through room backgrounds as "art pieces." Loads backgrounds from ALFRED.1, displays with palette. Needs custom UI loop with keyboard/mouse navigation. |

#### Missing Drink Combination (12-13) — Implementation Notes

```cpp
void PelrockEngine::giveDrinkAtCounter(int inventoryObject, HotSpot *hotspot) {
    // Both orange soda (60) and cola (61) use the same handler
    // Original: display_text_with_voice(text) — Alfred offers drink
    _room->addSticker(/* drink-on-counter sticker */);
    _state->removeInventoryItem(inventoryObject);
    // This is part of the burger-serving puzzle sequence
}
```

#### Missing Hamburger Cutscene (20) — Implementation Notes

This is a critical puzzle handler. The hamburger + spicy sauce sequence triggers the boss arrest:

```cpp
void PelrockEngine::useHamburger(int inventoryObject, HotSpot *hotspot) {
    // 415-byte handler at 0x23088
    // 1. Play eating animation (Alfred serves hamburger to boss)
    // 2. If FLAG_PUESTA_SALSA_PICANTE is set:
    //    - Boss eats, reacts to spicy sauce
    //    - Boss runs out screaming
    //    - Dialog sequence
    //    - Sets FLAG_JEFE_ENCARCELADO
    //    - Room state changes (boss NPC removed)
    // 3. If not spicy: Boss eats normally, dialog only
    _state->removeInventoryItem(64); // remove hamburger
}
```

#### Missing Art Gallery (44) — Implementation Notes

The art gallery is a bonus feature viewer — low priority but adds completeness:

```cpp
void PelrockEngine::showArtGallery() {
    // 1500+ byte handler at 0x24ED7
    // Loads room backgrounds from ALFRED.1 as "gallery art"
    // Custom UI: arrow keys to browse, ESC to exit
    // Renders background at full screen with room palette
    // Shows room name/number as title text
}
```

---

## 3. Verb Actions (OPEN / CLOSE / PICKUP / PULL / LOOK / PUSH)

These are triggered by using verbs on hotspots. Implemented in `actionTable[]`.

### Complete (80)

All door OPEN/CLOSE handlers, all PICKUP handlers for rooms 0–4, 8–9, 12–13, 15–17, 19, 25, 28–33, 37–38, 42, 46–47 are implemented. This includes:

- All 12 store item pickups (Room 15)
- All door open/close pairs (Rooms 0, 2, 3, 4, 8, 9, 12, 13, 16, 17, 19, 29, 33, 46, 47)
- Symbol push handlers (Room 30)
- Prison/tunnel handlers (Rooms 31, 32, 33)
- Egypt room pickups (Rooms 37, 38, 42)

### Missing Verb Actions (14)

| Room | Verb | Extra | Handler | Description |
|------|------|-------|---------|-------------|
| -1 | OPEN | 9 | `0x1C9D5` | **Default open response.** Jump to `default_verb_response`. Non-critical — just shows "already open/closed" text for generic hotspots. |
| -1 | PICKUP | 0 | `0x1E444` | **Yellow book pickup (complex).** 787 bytes, 144 instructions. Sets flag, adds sticker, hides hotspots 4/8/9/10, shows hotspot 0, plays pickup animation. This is a complex generic pickup handler for room 0's drawer items. Currently handled by `pickYellowBook` but the original has much more logic (hotspot show/hide, sticker placement, animation). **Likely incomplete rather than missing.** |
| -1 | PICKUP | 273 | `0x1E81B` | **Garbage can pickup response.** Jump to `default_verb_response`. Already handled by `pickupGarbageCan` dialog response. |
| 4 | OPEN | 312 | `0x1C7B5` | **Open museum door (guard check).** Displays text from `[0x4BA20]`. Currently `openMuseumDoor` checks flags but the original handler at this address just shows a text line — may be a different code path for when the guard hasn't been bribed. **Check if existing handler covers this.** |
| 4 | PICKUP | 310 | `0x1EB8A` | **Pickup fruit (default response).** Jump to `default_verb_response` — shows "I can't pick that up." Already handled by `pickupFruit` dialog. |
| 4 | PICKUP | 311 | `0x1EB8A` | **Pickup fruit (default response).** Same handler as 310. Already handled. |
| 38 | PICKUP | 99 | `0x205FE` | **Pickup wig (item 99).** Hides hotspot, jumps to item add. This is the wig pickup in the temple area. Not in `actionTable` but the item might be acquired through a different path. **Need to verify if item 99 can be picked up in ScummVM.** |
| 42 | PICKUP | 605 | `0x204CC` | **Can't pickup slave 1.** Default response. Currently `pickUpStones` is mapped for stones, but extra 605–607 (slave NPCs) should show rejection text. |
| 42 | PICKUP | 606 | `0x204CC` | **Can't pickup slave 2.** Same default handler. |
| 42 | PICKUP | 607 | `0x204CC` | **Can't pickup slave 3.** Same default handler. |
| 42 | PICKUP | 608 | `0x20528` | **Conditional pickup from slaves.** Checks flag `[0x495D4]` — if slaves are drunk (after 3 stone deliveries), may allow picking up something. Different from 605–607. |
| 55 | OPEN | 613 | `0x1D31C` | **Open pyramid door (rejection).** Jump to `default_verb_response`. Currently `openPyramidDoor` shows rejection text — **likely already covered.** |
| 13 | OPEN | 375 | `0x1CCA7` | **Open kitchen drawer (boss check).** Checks flag `[0x495C2]` then displays text from `[0x4BA84]`. Currently `openKitchenDrawer` checks `FLAG_JEFE_ENCARCELADO` which is the same logic. **Likely already covered.** |
| 13 | PULL | 374 | `0x1DCE5` | **Close kitchen door from inside.** Check flag, play sound, reset, sticker. Not in `actionTable` — CLOSE/PULL for kitchen inner door might be missing. |

#### Truly Missing (Need Implementation)

After filtering out entries that are already functionally covered by existing handlers:

| Room | Verb | Extra | Priority | What to Implement |
|------|------|-------|----------|-------------------|
| 38 | PICKUP | 99 | **HIGH** | Add wig pickup to `actionTable`. Without this, item 99 (wig) cannot be obtained, blocking the magic formula puzzle. Add: `{99, PICKUP, &PelrockEngine::pickUpWig}` |
| 42 | PICKUP | 608 | **MEDIUM** | Add conditional mud/item pickup from drunk slaves. Checks if slaves are drunk (`FLAG_GUARDIAS_BORRACHOS`), then allows pickup. |
| 13 | PULL | 374 | **LOW** | Add close handler for kitchen inner door (PULL verb = close). Minor — door works for OPEN but PULL/close may not be wired. |

---

## 4. Room Init Dispatch Table

These run once when entering a room. Implemented in `doExtraActions()`.

### Complete (13)

| Room | Description | ScummVM Status |
|------|-------------|----------------|
| 0, 4 | Boss arrested cutscene trigger | Implemented |
| 15 | First time entering shop dialog | Implemented |
| 38 | Arrival animation from desert | Implemented |
| 32 | Arrival animation from room 31 | Implemented |
| 27 | Arrival animation from room 33 | Implemented |
| 28 | Alternate palette for crocodile lighter | Implemented |
| 26 | Prison guard encounter | Implemented |
| 30 | Princess hair thief confrontation | Implemented |
| 36 | Pyramid collapse trigger | Implemented |
| 39, 40 | Goodbye disabled | Implemented |
| 48 | Endgame handler | Implemented |
| 51–54 | Flight room init | Implemented (`initGodsSequences`) |

### Incomplete (2)

| Room | Description | What's Missing |
|------|-------------|----------------|
| 0 | Shared handler with room 4 | Missing: cheat code input display when `FLAG_CHEAT_CODE_ENABLED` set. The boss cutscene part works but the easter egg input doesn't trigger. |
| 15 | Shop first visit | Missing `break` statement — falls through to case 38 (arrival anim). This means entering room 15 also plays the desert arrival animation from room 38 erroneously. **Bug.** |

### Missing Room Init Handlers (20)

| Room | Handler | Priority | Description |
|------|---------|----------|-------------|
| 3 | `0x25889` | **MEDIUM** | If `[0x9840]==1`: calls shop init function. If `[0x9824]==1`: hides sprite #12. Sets up shop state based on game progress (items purchased, etc.). |
| 7 | `0x2587A` | **HIGH** | Calls `init_or_stop_sound()` — starts CD audio track for Room 7 (Egypt theme music). Without this, room 7 has no background music. |
| 9 | `0x258BD` | **MEDIUM** | Clears door state flag `[0x95BF]` (library door = closed on entry). Sets `room_data[0x1C1]=0`. Also calls NPC sprite blit handler. Without this, the library door may incorrectly appear open on re-entry. |
| 12 | `0x25C49` | **MEDIUM** | Clears kitchen door state `[0x95C0]`. Sets `room_data[0x1CF]=0`. Ensures kitchen door starts closed on entry. |
| 13 | `0x25C68` | **MEDIUM** | Clears kitchen inner door state. If `[0x9DA3]==1`: repositions sprite #3 (NPC moved based on game progress). Characters appear in wrong positions without this. |
| 5 | `0x25A3D` | **HIGH** | Enables all 4 conversation roots for room 5's seller: `[0x98D3]`, `[0x98DA]`, `[0x98E1]`, `[0x98E8]` + `[0x95EA]=1`. **Without this, the player cannot talk to any NPCs in room 5.** |
| 19 | `0x25A68` | **LOW** | Sets sprite #4's animation frame byte to 9. Minor visual setup — travel agency NPC idle animation. |
| 24 | `0x25A96` | **LOW** | Sets sprite #3's animation state to 1. Minor visual — NPC animation state. |
| 41 | `0x25AF0` | **MEDIUM** | Sets sprite #3's walking frame to 3. Initializes slave animation state in pyramid room. Without this, slaves may display wrong animation frame initially. |
| 2 | `0x25C22` | **LOW** | Clears temp flag `[0x961D]=0`. Shared with room 37. Minor state cleanup. |
| 37 | `0x25C22` | **LOW** | Same as room 2. Clears temp flag. |
| 22 | `0x25C35` | **LOW** | Sets `room_data[0x21]=0xFF`. Hides Alfred rendering overlay for cutscene. Market room setup. |
| 34 | `0x25C35` | **LOW** | Same as room 22. Hides Alfred overlay. |
| 17 | `0x25BEC` | **MEDIUM** | NPC sprite blit handler. Sets `[0x961D]=1`, blits 256×256 NPC overlay with transparency. Creates walking pedestrian/NPC sprites. Without this, NPC characters in room 17 don't appear. |
| 13 | `0x25BEC` | **MEDIUM** | Same NPC blit handler as room 17. |
| 19 | `0x25BEC` | **MEDIUM** | Same NPC blit handler. |
| 49 | `0x25BEC` | **MEDIUM** | Same NPC blit handler. |
| 50 | `0x25BEC` | **MEDIUM** | Same NPC blit handler. |

### Missing Per-Frame Update Handlers

These run every frame while in the matching room. Not currently tracked in `doExtraActions` but need a separate per-frame dispatch.

| Room | Handler | Priority | Description |
|------|---------|----------|-------------|
| 26 | `0x1087C` | **HIGH** | Prison guard patrol timer. Increments counter; at 100 shows guard sprite. Checks guard position for reset. Handles guard bribery dialog. **Without this, the guard never appears in the prison street.** |
| 30 | `0x1094B` | **MEDIUM** | One-time wig pickup dialog trigger. If wig in inventory and flag not set, plays dialog and sound. |
| 36 | `0x1098F` | **HIGH** | Pyramid construction cutscene (multi-phase). Already partially handled by `pyramidCollapse()` but the per-frame handler has additional NPC waypoint movement logic. |
| 48 | `0x10D4C` | **MEDIUM** | Swimming pool / guard room per-frame logic. |
| 19 | `0x115EF` | **LOW** | Travel agency per-frame update (NPC animation). |
| 24 | `0x25CD7` | **LOW** | Room 24 sprite animation update. |
| 51–54 | `0x113DC` | **HIGH** | Flight animation per-frame handler. Updates airplane position across map screens. Without this, the flight sequence doesn't animate. Possibly already handled by flight system. |
| 1,2,3,8,14,17,12 | `0x118AD` | **MEDIUM** | Shared idle animation handler for outdoor/indoor rooms. Handles ambient NPC movement (pedestrians walking by, etc.). Without this, rooms feel static. |
| 15 | `0x11DE5` | **LOW** | Shop per-frame handler. Unknown specific function. |

### Missing Render Scene Handlers

These run during `render_scene()` every frame.

| Room | Handler | Priority | Description |
|------|---------|----------|-------------|
| 21 | `0x107C2` | **LOW** | Background character walking animation (passerby). |
| 9 | `0x1167A` | **LOW** | Library interior — character passing by window. |
| 29 | `0x11919` | **LOW** | Desert corridor NPC passing. |
| 46 | `0x11A29` | **LOW** | Corridor NPC passing. |
| 47 | `0x11B41` | **LOW** | Corridor NPC passing. |
| 50 | `0x11C4E` | **LOW** | Corridor NPC passing. |
| 31 | `0x11D66` | **LOW** | Corridor NPC passing. |

### Missing Palette Cycling

Palette cycling is configured per-room via a config table. 13 rooms use it.

| Room | Config Ptr | Priority | Description |
|------|-----------|----------|-------------|
| 0 | `0x1868C` | **MEDIUM** | Clock/lamp animation in Alfred's bedroom |
| 2 | `0x18660` | **MEDIUM** | Neon signs at McDowell's |
| 9 | `0x18674` | **LOW** | Lamp flicker in library |
| 17 | `0x1866C` | **LOW** | Monitor glow in boss office |
| 18 | `0x18670` | **LOW** | Ambient lighting |
| 19 | `0x18678` | **LOW** | Sign animation at travel agency |
| 21 | `0x18684` | **LOW** | Traffic lights |
| 25 | `0x18690` | **LOW** | Heat shimmer in desert |
| 32 | `0x18698` | **LOW** | Torchlight in pyramid entrance |
| 33 | `0x1869C` | **LOW** | Torchlight in pyramid interior |
| 38 | `0x18694` | **LOW** | Cave light effects |
| 39 | `0x18688` | **LOW** | Torchlight in guard room |
| 46 | `0x186A0` | **LOW** | Corridor torch/ambient |

---

## 5. Priority Implementation Roadmap

### Critical (Game-Breaking if Missing)

1. **Room 5 conversation enable** (Room Init) — Without this, NPCs in room 5 can't be talked to
2. **Item 99 (wig) pickup** (Verb Action, Room 38) — Blocks magic formula puzzle, blocking endgame
3. **Actions 308, 313** (F8, Room 41) — Guard dialog doesn't progress in pyramid room
4. **Action 307** (F8, Room 37) — Hidden hotspots never revealed, blocking stone pickup
5. **Room 15 fallthrough bug** (Room Init) — Add missing `break` after case 15

### High Priority (Significant Gameplay Impact)

6. **Action 267 completion** (F8, Room 7) — Time traveler never gives item 8 (secret code)
7. **Room 7 music** (Room Init) — No background music in Room 7
8. **Actions 297, 372–374** (F8, Room 34) — Palace guard dialog doesn't progress
9. **Actions 298–306** (F8, Room 25) — Philosopher conversation branches incomplete
10. **Hamburger cutscene** (#20, Item Combo) — Boss feeding sequence missing
11. **Ketchup on hamburger** (#16, Item Combo) — Part of boss arrest puzzle chain
12. **Drink at counter** (#12–13, Item Combo) — Part of boss meal puzzle chain
13. **Action 323** (F8, Room 47) — Architect dual-conv advance missing
14. **Prison guard patrol** (Per-Frame, Room 26) — Guard never appears
15. **Flight per-frame animation** (Per-Frame, Rooms 51–54) — May already be handled

### Medium Priority (Important but Non-Blocking)

16. **Room 9, 12, 13 door state resets** (Room Init) — Doors may appear in wrong state
17. **NPC sprite blit** (Room Init, Rooms 17/13/19/49/50) — NPCs don't appear
18. **Room 3 shop init** (Room Init) — Shop state incorrect
19. **Room 41 slave animation init** (Room Init) — Wrong initial frame
20. **Action 294** (F8, Room 31) — Toilet examined flag doesn't persist
21. **Action 322** (F8, Room 47) — Pyramid plans dialog missing
22. **Item 608 conditional pickup** (Verb, Room 42) — Can't get items from drunk slaves
23. **Idle NPC animations** (Per-Frame, Rooms 1/2/3/8/14/17/12) — Rooms feel static
24. **Item 98 self-use** (#35, pyramid map) — Can't view pyramid map
25. **Items 108/109 self-use** (#41–42, doll repair) — Doll repair combo check logic

### Low Priority (Polish / Bonus Features)

26. **Palette cycling** — 13 rooms missing ambient palette animations
27. **Render scene handlers** — 7 rooms missing background NPC walking
28. **Art gallery viewer** (#44) — Bonus content viewer
29. **Action 368** — Dead placeholder (no-op)
30. **Actions 381–382** — Sound sequence for lights-off effect
31. **Room 2/37 temp flag clear** — Minor state cleanup
32. **Room 22/34 Alfred overlay hide** — Cutscene rendering detail
33. **Room 19 sprite frame init** — Minor visual
34. **Room 24 sprite state init** — Minor visual

---

## Appendix: Flag Mapping

Flags referenced in missing handlers that may need new constants in `offsets.h`:

| Original Address | Suggested Constant | Used By |
|-----------------|-------------------|---------|
| `[0x95D0]` | `FLAG_PHILOSOPHER_STATE` | Action 299 |
| `[0x961D]` | `FLAG_NPC_OVERLAY_ACTIVE` | Room init (17/13/19/49/50) |
| `[0x9840]` | `FLAG_SHOP_INIT_STATE` | Room 3 init |
| `[0x9824]` | `FLAG_SHOP_SPRITE_HIDDEN` | Room 3 init |
| `[0x9DA3]` | `FLAG_NPC_POSITION_CHANGED` | Room 13 init |
| `[0x95BF]` | `FLAG_LIBRARY_DOOR_STATE` | Room 9 init |
| `[0x95C0]` | `FLAG_KITCHEN_DOOR_STATE` | Room 12 init |
| `[0x95C1]` | `FLAG_KITCHEN_INNER_DOOR` | Room 13 init |
| `[0x95FA]` | `FLAG_GUARD_PATROL_COUNTER` | Room 26 per-frame |
| `[0x95FB]` | `FLAG_GUARD_VISIBLE` | Room 26 per-frame |
| `[0x95C9]` | `FLAG_GUARD_BRIBED` | Room 26 per-frame |
| `[0x95CA]` | `FLAG_GUARD_BRIBE_DIALOG` | Room 26 per-frame |
