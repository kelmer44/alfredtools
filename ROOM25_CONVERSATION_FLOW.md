# Room 25 — Buddhist Monk Conversation System

## Overview

Room 25 is the riverbank where Alfred meets a Buddhist monk (NPC #1). The conversation has **4 phases** plus special events, governed by 11 action handlers (357–367) and managed through a quiz score counter, a riddle-solved flag, and a hidden cheat code system.

**Key memory addresses:**

| Ghidra Addr | Name | Type | Purpose |
|---|---|---|---|
| `0x495F2` | `quiz_score_counter` | byte | Tracks correct quiz answers (0–15) |
| `0x495F3` | `cheat_code_checking_enabled` | byte | Enables cheat code input detection |
| `0x495D0` | `riddle_solved_flag` | byte | Set when Egyptian riddle is answered correctly |
| `0x495C9` | `kicked_out_to_room26_flag` | byte | Set when monk calls police |
| `0x495E6` | `kickout_animation_played_flag` | byte | Prevents re-triggering kick-out animation |
| `0x5178D` | `cheat_code_progress_counter` | byte | Position in cheat code sequence |
| `0x5178F` | `cheat_mode_active` | byte | 1 = free movement debug mode active |
| `0x4B79C` | `ptr_cheat_code_string` | ptr | Points to "HIJODELAGRANPUTA" at `0x40F41` |
| `0x4B7A0` | `cheat_code_length` | byte | 16 (length of cheat string) |

---

## Phase 1: Initial Dialog (Root 1)

The first conversation root uses `FB-ONCE` branches — each topic can only be selected once. Topics include:
- Buddhism and meditation
- The lagarto (lizard) → leads to ACTION **366**
- Religion and philosophy
- General small talk

After exhausting topics, the quiz phase begins.

### Action 366 — Lagarto Branch End
- **Handler:** `0x222E3`
- **Logic:** Calls `update_conversation_state(room=25, npc=0, branch=1)` to mark the lagarto topic complete and return to the main dialog tree.
- **ScummVM:** `setRootDisabledState(room, rootIndex, true)`

---

## Phase 2: Quiz — "Who Said It?" (Roots 2–15)

The monk quotes famous authors and Alfred must guess who said it. There are **14 quiz questions** (roots 2–15), each with **5 options**: 4 author names + "No sé" (I don't know).

The quiz uses a **score counter** at `[0x495F2]` (flag index 54 / `FLAG_RESPUESTAS_ACERTADAS`). Each root is of type `F1-REPEAT`, meaning it can be re-visited, but in practice the action handler disables it after answering.

### Scoring Actions

#### Action 359 — Correct Answer (`+1`)
- **Handler:** `0x22200`
- **Logic:**
  1. `quiz_score_counter++`
  2. If counter == **15**: call `process_inventory_action(0x6A)` → **adds item 106 (pin) to inventory**, then reset counter to 0
  3. If counter != 15: advance to next quiz question
- **Key detail:** The counter must reach exactly 15 across multiple conversation visits. Getting 15 correct answers total earns the pin.

#### Action 357 — Wrong Answer (`−1`)
- **Handler:** `0x221A2`
- **Logic:**
  1. Read `quiz_score_counter`
  2. If counter > 0: `counter--`
  3. If counter == 0: no change (floor at zero)
  4. Advance to next quiz question
- **⚠ ScummVM bug:** Current code does `counter - 1` without checking if > 0, potentially going negative.

#### Action 358 — Very Wrong Answer (`−2`)
- **Handler:** `0x221C5`
- **Logic:**
  1. Read `quiz_score_counter`
  2. If counter > 1: `counter -= 2`
  3. If counter ≤ 1: no change (floor at zero, won't subtract below 0)
  4. Advance to next quiz question
- **⚠ ScummVM bug:** Current code does `counter - 2` without floor check.

#### Action 361 — "No sé" / I Don't Know
- **Handler:** `0x2223E`
- **Logic:** Advance to next quiz question. **No counter change.**
- **⚠ ScummVM bug:** Current code resets counter to 0 (falls through from case 360). Should be no-op on counter.

#### Action 360 — Neutral Reset
- **Handler:** `0x2222D`
- **Logic:** `quiz_score_counter = 0` (full reset), then advance to next question.
- **Note:** This is triggered by selecting a particularly absurd but non-offensive answer. It completely resets progress.

#### Action 362 — Special Trigger (Cheat Code Enabler)
- **Handler:** `0x2224D`
- **Logic:** Sets `cheat_code_checking_enabled` (`[0x495F3]`) to **1**, then advance to next question. No counter change.
- **Trigger:** Selected when Alfred says: *"Rafael Tevoyadarunalechequetetevoyapartirlacaraytevanatenerquehacertelacirugia"* (a veiled threat disguised as an author name)
- **NPC Response:** "Bien dicho!" (Well said!)
- **Effect:** Enables the hidden **HIJODELAGRANPUTA** cheat code (see Easter Eggs below)
- **⚠ ScummVM:** Not implemented at all.

### Shared Epilogue (Quiz Advancement)

All quiz actions (357–362) share a common epilogue at `0x221E9`:
```
ECX = 1        ; branch index  
EBX = 0x19     ; room 25  
EDX = 0        ; npc 0  
EAX = 0x19     ; room 25  
CALL update_conversation_state  ; at 0x1B723
```
This disables the current quiz root and advances to the next one. The conversation tree cycles through roots 2–15.

---

## Phase 3: Sunflower Negotiation (Root 16)

After the quiz, Alfred can ask about the monk's sunflower (girasol). The monk agrees to trade the sunflower if Alfred can answer an Egyptian riddle.

### Action 367 — Accept Riddle Challenge
- **Handler:** `0x222AA` → jumps to `0x219B9`
- **Logic:**
  1. `update_conversation_state(room=25, npc=0, branch=27)` — switches conversation to root 27 (riddle section)
  2. Calls `check_sprite_hover_and_trigger_conversation(2)` at `0x18DCE` — triggers the first riddle question
- **ScummVM:** Partially implemented (missing conversation root switch to 27).

---

## Phase 4: Egyptian Riddle (Roots 17–30)

The monk presents riddles. Wrong answers cycle through more riddles; the correct answer ends the riddle phase.

### Action 364 — Riddle Wrong Answer
- **Handler:** `0x22263`
- **Logic:** Calls `update_conversation_state(room=25, npc=27, branch=43)` — advances within the riddle roots.
- **⚠ ScummVM:** Not implemented (falls through to default).

### Action 365 — Riddle Correct Answer
- **Handler:** `0x22286` → pushes `0xC`, jumps to `0x219D9`
- **Logic:**
  1. Calls `stack_check` with param `0xC`
  2. `update_conversation_state(room=25, npc=0, branch=1)` with EBX=1
  3. Sets `riddle_solved_flag` (`[0x495D0]`) = **1**
  4. This flag likely controls whether the sunflower can be obtained
- **⚠ ScummVM:** Not implemented (falls through to default).

---

## Special Event: Police / Kicked Out

### Action 363 — Monk Calls Police
- **Handler:** `0x2151D` (~600 bytes, most complex handler)
- **Trigger:** Insulting the monk too much during conversation
- **Logic:**
  1. Call `fade_palette_to_black()` at `0x1B8B3`
  2. Clear conversation state via `0x1B8B3` (shared function)
  3. Set Alfred position: X=342, Y=277, facing=DOWN
  4. Call `update_conversation_state(room=26, npc=1, branch=1)` — **transitions to Room 26**
  5. Set `kicked_out_to_room26_flag` (`[0x495C9]`) = 1
  6. Set `kickout_animation_played_flag` (`[0x495E6]`) = 1
  7. Reposition NPC sprites offscreen (640,400 and 444,166)
- **ScummVM:** `toJail()` — simplified version (fade, set position, change screen to 31)

---

## Conversation Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ROOM 25 ENTRY                            │
│              (Buddhist Monk by River)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────┐
        │   PHASE 1: INITIAL      │
        │   Root 1 (FB-ONCE)      │
        │                         │
        │  Topics:                │
        │  • Buddhism             │
        │  • Lagarto ──→ ACT 366  │
        │  • Religion             │
        │  • Small talk           │
        └────────────┬────────────┘
                     │ (exhaust topics)
                     ▼
        ┌─────────────────────────┐
        │   PHASE 2: QUIZ         │
        │   Roots 2-15 (F1-RPT)   │    quiz_score_counter
        │                         │    ┌──────────────┐
        │   "Who said it?"        │    │  starts at 0  │
        │   5 options each        │    └──────┬───────┘
        │                         │           │
        │  Correct  → ACT 359    ─┼──→  counter++ ──→ if == 15:
        │  Wrong    → ACT 357    ─┼──→  counter--      ADD ITEM 106 (pin)
        │  V.Wrong  → ACT 358   ─┼──→  counter-=2     counter = 0
        │  "No sé"  → ACT 361   ─┼──→  (no change)
        │  Neutral  → ACT 360   ─┼──→  counter = 0 (RESET!)
        │  Special  → ACT 362   ─┼──→  enable cheat code
        │                         │
        │  Insult   → ACT 363   ─┼──→  POLICE! → Room 26
        └────────────┬────────────┘
                     │ (ask about sunflower)
                     ▼
        ┌─────────────────────────┐
        │   PHASE 3: NEGOTIATE    │
        │   Root 16               │
        │                         │
        │  "I want the sunflower" │
        │  Monk: "Answer riddle"  │
        │                         │
        │  Accept → ACT 367      ─┼──→  Switch to Root 27
        └────────────┬────────────┘
                     │
                     ▼
        ┌─────────────────────────┐
        │   PHASE 4: RIDDLE       │
        │   Roots 17-30 (F1-RPT)  │
        │                         │
        │  Egyptian riddle         │
        │                         │
        │  Wrong   → ACT 364     ─┼──→  Next riddle attempt
        │  Correct → ACT 365     ─┼──→  riddle_solved_flag = 1
        └─────────────────────────┘
```

---

## Easter Eggs

### Cheat Code: HIJODELAGRANPUTA

**Activation flow:**
1. During the quiz, select the answer *"Rafael Tevoyadarunalechequetetevoyapartirlacaraytevanatenerquehacertelacirugia"*
2. Monk responds: "Bien dicho!" → Action 362 fires → `cheat_code_checking_enabled = 1`
3. In the main game loop (at `0x10500` in `main_game_loop`), the game now monitors every keypress
4. Type **H-I-J-O-D-E-L-A-G-R-A-N-P-U-T-A** (16 characters)
5. Each correct key advances `cheat_code_progress_counter`; wrong key resets to 0
6. When all 16 match: `cheat_mode_active = 1`

**Effect:** Free movement debug mode — arrow keys move Alfred directly, bypassing walkbox constraints and pathfinding. Also loads sound `9ZZZZZZZ.SMP`.

**Implementation in main_game_loop:**
```
0x10500: CMP [cheat_code_checking_enabled], 0    ; skip if not enabled
0x10507: JZ skip
0x1050D: CALL get_last_keypress                   ; 0x15258
0x10514: MOV BL, [cheat_code_progress_counter]    ; current position
0x1051A: MOV EDX, [ptr_cheat_code_string]         ; → "HIJODELAGRANPUTA"
0x10520: CMP AL, [EDX + EBX]                      ; compare keypress vs expected
0x10523: JNZ reset_counter                        ; wrong key → reset
0x10525: INC position                             ; right key → advance
0x10538: CMP position, [cheat_code_length]        ; all 16 matched?
0x10543: JNZ skip                                 ; not yet
0x10549: → ACTIVATE CHEAT MODE                    ; done!
```

### Room 2 Easter Egg
In Room 2 (address `0x104B8`–`0x104F3`), pressing 'X' **250 times** (`naked_easter_egg_counter` at `0x495E9` reaching `0xFA`) triggers a joke response — likely Alfred's NPC companion commenting on his behavior.

---

## Handler Address Table

| Action | Hex | Ghidra Addr | Purpose | Counter Effect |
|--------|------|-------------|---------|----------------|
| 357 | 0x0165 | `0x221A2` | Wrong answer | `−1` (min 0) |
| 358 | 0x0166 | `0x221C5` | Very wrong answer | `−2` (min 0) |
| 359 | 0x0167 | `0x22200` | Correct answer | `+1` (triggers item at 15) |
| 360 | 0x0168 | `0x2222D` | Neutral reset | `= 0` |
| 361 | 0x0169 | `0x2223E` | "I don't know" | no change |
| 362 | 0x016A | `0x2224D` | Special trigger | no change (sets cheat flag) |
| 363 | 0x016B | `0x2151D` | Police / kicked out | N/A (exits room) |
| 364 | 0x016C | `0x22263` | Riddle wrong | N/A |
| 365 | 0x016D | `0x22286` | Riddle correct | N/A (sets riddle flag) |
| 366 | 0x016E | `0x22290` | Lagarto end | N/A |
| 367 | 0x016F | `0x222AA` | Start riddle | N/A |

**Shared epilogue at `0x221E9`:** Calls `update_conversation_state` at `0x1B723` with room=25, npc=0 to advance to the next conversation root.

---

## ScummVM Implementation Bugs

### Bug 1: Action 361 incorrectly resets counter
**File:** `actions.cpp` line ~420
**Problem:** Case 360 falls through to case 361. Both execute `setFlag(FLAG_RESPUESTAS_ACERTADAS, 0)`. In the original, action 361 ("No sé") does **not** change the counter — it only advances the conversation.
**Fix:** Add `break;` after case 360's logic, and make case 361 a no-op on the counter.

### Bug 2: Actions 357/358 can go below zero
**File:** `actions.cpp` lines 403, 407
**Problem:** `counter - 1` and `counter - 2` are applied without checking if the counter is large enough. The original x86 code checks `AH != 0` before decrementing (357) and `AL > 1` before subtracting 2 (358).
**Fix:** Add floor check: `max(0, counter - N)`.

### Bug 3: Action 362 not implemented
**Problem:** Falls through to default. Should set `cheat_code_checking_enabled` flag.
**Fix:** Set the flag (and implement the cheat code system in the game loop).

### Bug 4: Action 364 not implemented
**Problem:** Falls through to default. Should call `update_conversation_state` to advance riddle roots.

### Bug 5: Action 365 not implemented
**Problem:** Falls through to default. Should set `riddle_solved_flag` = 1 and update conversation state.

### Bug 6: Action 363 (toJail) simplified
**Problem:** ScummVM `toJail()` goes to screen 31, but original goes to room 26 with NPC repositioning and multiple flag sets. This may cause state inconsistencies.

---

## Key Functions Referenced

| Address | Name | Purpose |
|---------|------|---------|
| `0x1B723` | `update_conversation_state` | Advances conversation: disables current root, enables next. Called with room/npc/branch in EAX/EDX/EBX+ECX |
| `0x1B666` | `update_conversation_state_alt` | Alternative conversation update (used by action 363) |
| `0x1B8B3` | `fade_palette_to_black` | Decrements all palette entries until fully black |
| `0x24157` | `process_inventory_action` | Adds item to inventory (param on stack = item ID) |
| `0x18DCE` | `check_sprite_hover_and_trigger_conversation` | Used by action 367 to trigger riddle dialog |
| `0x15258` | (unnamed) | Gets last keypress from input buffer |
| `0x152B6` | (unnamed) | Checks if keyboard input is available |
