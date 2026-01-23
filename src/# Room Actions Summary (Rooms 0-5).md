# Room Actions Summary (Rooms 0-5)

Based on extracted hotspot data from ALFRED.1 and existing ScummVM implementation.

## Dispatch Flag Legend
| Flag | Meaning | Dispatch Function |
|------|---------|-------------------|
| 0x01 | ROOM_SCRIPT | execute_room_specific_script() |
| 0x02 | CONVERSATION | handle_conversation_tree() |
| 0x03 | ROOM_SCRIPT + CONVERSATION | Both above |
| 0x08 | DIALOG | handle_dialog_interaction() |
| 0x10 | HOTSPOT_ACTION | dispatch_hotspot_action_by_extra_id() |
| 0x20 | TAKE | execute_script_table_0x47c10() |
| 0x40 | PICKUP | execute_script_table_0x47c18() |

---

## Room 0 - Alfred's Bedroom

### Hotspots with Actions
| Extra | Type | Position | Size | Actions | ScummVM Status |
|-------|------|----------|------|---------|----------------|
| 261 | 0x03 | (191,243) | 32x11 | ROOM_SCRIPT, CONV | ✅ openRoomDrawer/closeRoomDrawer |
| 263 | 0x01 | (191,258) | 32x11 | ROOM_SCRIPT | ❓ Unknown (below drawer?) |
| 268 | 0x03 | (231,138) | 65x136 | ROOM_SCRIPT, CONV | ✅ openRoomDoor/closeRoomDoor |

### Look-Only Hotspots (descriptions only)
| Extra | Position | Size | What |
|-------|----------|------|------|
| 262 | (123,146) | 100x49 | ? |
| 264 | (303,138) | 121x22 | Bed? |
| 260 | (303,164) | 90x28 | ? |
| 267 | (299,233) | 190x49 | ? |

### Dialog Hotspots (text responses)
| Extra | Position | Notes |
|-------|----------|-------|
| 0 | (174,206) | Yellow book? |
| 1 | (191,243) | ID Card |
| 2 | (191,243) | Credit Card |
| 3 | (191,243) | Photo |

### Known Items to Pick Up
- **Yellow Book** (extra=0): pickYellowBook → adds sticker 95
- **Photo** (extra=3): pickUpPhoto → enables hotspot 261
- **ID Card** (extra=1): Unknown implementation
- **Credit Card** (extra=2): Unknown implementation

### Stickers Used
- 91: Open drawer graphic
- 93: Open door graphic
- 95: Yellow book taken (removed from shelf)

---

## Room 1 - Street Outside Alfred's House

### Hotspots with Actions
| Extra | Type | Position | Size | Actions | ScummVM Status |
|-------|------|----------|------|---------|----------------|
| 277 | 0x01 | (247,266) | 45x76 | ROOM_SCRIPT | ❓ Unknown |

### Look-Only Hotspots
| Extra | Position | Size |
|-------|----------|------|
| 276 | (21,216) | 89x124 |
| 278 | (184,101) | 63x86 |

### Dialog Hotspots
| Extra | Position | Notes |
|-------|----------|-------|
| 4 | (355,344) | Brick on ground |

### Known Items
- **Brick** (extra=4): pickUpBrick → adds sticker 133

---

## Room 2 - Street with ATM & McDowell's

### Hotspots with Actions
| Extra | Type | Position | Size | Actions | ScummVM Status |
|-------|------|----------|------|---------|----------------|
| 282 | 0x03 | (354,262) | 68x85 | ROOM_SCRIPT, CONV | ✅ openMcDoor/closeMcDoor |
| 285 | 0x20 | (640,400) | 10x5 | TAKE | ❓ Hidden/disabled? |
| 286 | 0x20 | (640,400) | 10x5 | TAKE | ❓ Hidden/disabled? |

### Look-Only Hotspots
| Extra | Position | Size | What |
|-------|----------|------|------|
| 281 | (214,293) | 32x15 | ATM |

### Dialog Hotspots
| Extra | Position | Notes |
|-------|----------|-------|
| 283 | (294,265) | ? |
| 284 | (558,273) | ? |

### Item Combinations
- **ATM Card (2) + ATM (281)**: useCardWithATM → withdraw money

### Stickers Used
- 7: McDowell's door open

---

## Room 3 - Shop Front Street

### Hotspots with Actions
| Extra | Type | Position | Size | Actions | ScummVM Status |
|-------|------|----------|------|---------|----------------|
| 290 | 0x03 | (189,255) | 50x87 | ROOM_SCRIPT, CONV | ✅ openShopDoor/closeShopDoor |
| 308 | 0x88 | (640,400) | 3x16 | DIALOG | ✅ moveCable (lamppost cable) |

### Look-Only Hotspots (Shop window items)
| Extra | Position | Size | What |
|-------|----------|------|------|
| 291 | (126,258) | 40x55 | Shop window left |
| 292 | (144,59) | 36x33 | ? |
| 293 | (210,59) | 47x33 | ? |
| 294 | (392,28) | 58x66 | Upper window |
| 295 | (260,257) | 175x57 | Shop front |
| 296-307 | various | various | Shop display items |

### Item Combinations
- **Brick (4) + Window (294)**: useBrickWithWindow → breaks window, opens shop
- **Brick (4) + Storefront (295)**: useBrickWithShopWindow → rejection text

### Stickers Used
- 11: Broken window
- 13: Shop door open
- 14: Lamppost open
- 15,16,17: Cable placed

---

## Room 4 - Alley with Junction Box

### Hotspots with Actions
| Extra | Type | Position | Size | Actions | ScummVM Status |
|-------|------|----------|------|---------|----------------|
| 312 | 0x03 | (275,95) | 74x102 | ROOM_SCRIPT, CONV | ❓ Unknown |
| 315 | 0x01 | (372,182) | 10x8 | ROOM_SCRIPT | ✅ openPlug (junction box) |

### Look-Only Hotspots
| Extra | Position | Size |
|-------|----------|------|
| 313 | (296,46) | 29x29 |
| 314 | (640,400) | 29x29 | Hidden |

### Dialog Hotspots
| Extra | Position | Notes |
|-------|----------|-------|
| 310 | (0,159) | Left building |
| 311 | (525,150) | Right building |
| 316 | (640,400) | Cables (hidden until placed) |

### Known Actions
- **Open Plug (315)**: openPlug → adds sticker 18
- **Pick Cables (316)**: pickCables → special animation + shock + sticker 21
- **Cord (6) + Plug (315)**: useCordWithPlug → sticker 19

### Stickers Used
- 18: Plug box open
- 19: Cord connected
- 20: Cable from room 3
- 21: Cables taken

---

## Room 5 - Courtyard/Patio

### Hotspots (all Look-Only)
| Extra | Type | Position | Size | What |
|-------|------|----------|------|------|
| 319 | 0x00 | (53,59) | 41x67 | ? |
| 320 | 0x00 | (57,141) | 45x81 | ? |
| 321 | 0x00 | (73,233) | 23x42 | ? |
| 322 | 0x00 | (528,67) | 38x76 | ? |
| 323 | 0x00 | (531,167) | 41x59 | ? |
| 324 | 0x00 | (524,227) | 28x53 | ? |

Room 5 appears to be primarily a transition room with no interactive actions.

---

## Implementation Notes

### Type Flag Mapping to Verbs
The hotspot `type` byte determines which dispatcher handles the action, but does NOT determine which verb icons appear. The verb icons come from:
1. **Sprites**: The `action_flags` byte at offset +0x22 (34) determines available verbs
2. **Static Hotspots**: Always have LOOK; other verbs depend on the dispatcher routing

### Hidden Hotspots
Hotspots at position (640,400) are typically hidden/disabled until a flag is set:
- They're placed off-screen to prevent interaction
- Game logic moves them on-screen when needed
- Example: Cable hotspot (316) in Room 4

### Sticker System
Stickers modify the room appearance:
- Adding a sticker overlays a graphic (e.g., open door)
- Removing a sticker restores the original (e.g., close door)
- Some stickers persist across room transitions (via `onlyPersistSticker`)
