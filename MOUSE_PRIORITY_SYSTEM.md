# Mouse Hover Priority System

## Overview
The function `check_mouse_on_sprites_and_hotspots` @ 0x00019879 determines what icon/interaction is shown when hovering the mouse.

## Confirmed Priority Rules (from assembly)

### 1. Sprites (checked first, index 1 to sprite_count)
For each sprite, the function:
1. Checks bounding box (x, y, w, h)
2. Checks `offset +0x21 != 0xFF` (valid type) and `offset +0x30 == 0x00` (active)
3. Checks **pixel transparency**: reads actual sprite pixel data at the mouse position — pixel must NOT be 0xFF (transparent)

On a pixel-level hit:
- `mouse_hover_state = 0x01` (generic sprite)
- If sprite index == 1 (Alfred): `mouse_hover_state = 0x03` instead
- Stores `hotspot_action_flags`, `hotspot_id_or_data`, `hotspot_sprite_index`
- **If NOT sprite 1**: `break` — exits sprite loop, skips hotspot check entirely
- **If sprite 1 (Alfred)**: falls through — continues iterating remaining sprites

### 2. Hotspots (checked second, conditionally)
After the sprite loop, hotspots are checked **only if**:
```asm
00019b95: MOV CH,[0x00051755]    ; load mouse_hover_state
00019b9b: TEST CH,CH              ; is it 0?
00019b9d: JZ hotspot_loop         ; if 0 → check hotspots
00019ba3: CMP EAX,0x3             ; is it 3 (Alfred)?
00019ba6: JNZ skip_hotspots       ; if NOT 3 → skip hotspots
; fall through to hotspot_loop
```

So hotspots are checked when `mouse_hover_state == 0` (nothing found) OR `mouse_hover_state == 3` (Alfred found).

When a hotspot rectangle matches, the code **always** sets `mouse_hover_state = 0x02`, overriding Alfred:
```asm
00019c48: MOV byte ptr [0x00051755],0x2   ; mouse_hover_state = 2 (ALWAYS)
00019c4f: MOV DH,byte ptr [EAX + 0x47c]  ; load flags byte
00019c55: AND DH,0x7f                      ; strip bit 7 (for storage only)
00019c58: MOV byte ptr [0x00051757],DH    ; store as hotspot_action_flags
```
The `AND 0x7F` only affects the **stored action flags** — it does NOT affect the hover state assignment. `mouse_hover_state` is unconditionally set to 2.

### 3. Exits (always checked)
Exit detection is always checked at the end, regardless of sprite/hotspot results. Sets `exit_detected = 1` if found.

## Cursor Display Logic (in `render_scene`)

The cursor icon is determined in `render_scene` by cascading if-statements:

| Condition | Cursor | Icon |
|-----------|--------|------|
| `state == 0 && exit == 0` | `cursor_default_ptr` | Default arrow |
| `state == 0 && exit != 0` | `cursor_exit_ptr` | Exit arrow |
| `state == 3` (Alfred) | `cursor_animation_ptr` | Alfred/use icon |
| `state == 1 or 2, exit == 0` | `cursor_hotspot_ptr` | Interaction hand |
| `state == 1 or 2, exit != 0` | `cursor_combination_ptr` | Combined exit+hotspot |

## What the Code Actually Says About Occlusion

**Hotspots ALWAYS override Alfred.** If the mouse is within both Alfred's non-transparent pixels AND a hotspot rectangle, the detection function sets state to 3 (Alfred found) and then immediately overwrites it to 2 (hotspot found). The hotspot cursor will be shown.

**The only way Alfred "occludes" a hotspot is geometrically:** if Alfred's sprite covers a hotspot area, but the mouse is on a part of Alfred that is OUTSIDE the hotspot rectangle, then only Alfred is detected (state 3) and the Alfred cursor shows. The hotspot rect check simply doesn't match at those pixel positions.

## Action Menu Popup

When right-clicking (or holding), `setup_action_menu_icons` builds the action popup:
```c
if (mouse_hover_state != '\x03') {
    // Add LOOK icon — only for non-Alfred targets
}
// Then add icons based on hotspot_action_flags bits
```
When `mouse_hover_state == 0x03` (Alfred), the LOOK icon is skipped — only verb icons matching `hotspot_action_flags` are shown.

## Room 0 Hotspot Data (Correct)

| # | Flags | Actions | Rect | Extra |
|---|-------|---------|------|-------|
| 0 | 0x03 | OPEN, CLOSE | (191,243)-(223,254) | 261 |
| 1 | 0x00 | LOOK only | (123,146)-(223,195) | 262 |
| 2 | 0x01 | OPEN | (191,258)-(223,269) | 263 |
| 3 | 0x00 | LOOK only | (303,138)-(424,160) | 264 |
| 4 | 0x08 | PICKUP | (174,206)-(205,221) | 0 |
| 5 | 0x00 | LOOK only | (303,164)-(393,192) | 260 |
| 6 | 0x00 | LOOK only | (299,233)-(489,282) | 267 |
| 7 | 0x03 | OPEN, CLOSE | (231,138)-(296,274) | 268 |
| 8 | 0x08 | PICKUP | (191,243)-(223,254) | 1 |
| 9 | 0x08 | PICKUP | (191,243)-(223,254) | 2 |
| 10 | 0x08 | PICKUP | (191,243)-(223,254) | 3 |
| 11 | 0x00 | LOOK only | (58,176)-(99,230) | 3 |

## Hotspot Structure (9 bytes each, at room_data + 0x47C)

| Offset | Size | Field |
|--------|------|-------|
| +0 | 1 | Action flags (& 0x7F when stored in `hotspot_action_flags`) |
| +1 | 2 | X position (LE) |
| +3 | 2 | Y position (LE) |
| +5 | 1 | Width |
| +6 | 1 | Height |
| +7 | 2 | Extra/ID (LE) |

## Implementation Notes for ScummVM

1. Sprites are checked first, index 1 to sprite_count
2. Alfred (sprite 1) sets state 3 but does NOT break the sprite loop
3. Any other sprite sets state 1 and breaks (skips hotspots)
4. Hotspots checked only if state is 0 or 3 — always override Alfred when rect matches
5. Stored action flags have bit 7 masked off (`& 0x7F`)
6. Exits are checked independently after hotspots
7. Cursor icon is determined by final `mouse_hover_state` value in `render_scene`
