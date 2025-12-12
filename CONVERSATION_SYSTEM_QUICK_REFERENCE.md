# Conversation System - Quick Reference

## Files Created

| File | Purpose |
|------|---------|
| `CONVERSATION_LOOP_ARCHITECTURE.md` | Complete technical documentation of loop structure, text advancement, and state management |
| `ANIMATION_CODE_DUPLICATION_ANALYSIS.md` | Detailed analysis proving animation code runs during conversations |
| `CONVERSATION_ANALYSIS_SUMMARY.md` | Quick summary of key findings and discoveries |
| `conversation_system.c` | Clean C implementation of the conversation system |
| `simulate_conversation.py` | Interactive Python simulator for testing conversations |
| `CONVERSATION_SIMULATOR_USAGE.md` | Usage guide and examples for the simulator |

## Quick Answers

### Q: Does the conversation system have a separate while loop from the main render loop?

**A: YES** - It has its own nested while loop inside `handle_conversation_tree()` that **blocks** the main game loop until the conversation ends.

### Q: Is animation advancement code duplicated in the conversation loop?

**A: YES** - The full `update_npc_sprite_animations()` function runs every frame during conversations. Sprites continue animating, moving, and updating normally.

### Q: How does text advance through conversation lines?

**A: Automatically timed** with three exit conditions:
1. Time-based: ~`text_length/2` frames elapsed
2. Voice-based: Voice sample finishes playing (if enabled)
3. User skip: Mouse click to advance immediately

Each line **blocks** in `display_talk_animation_and_wait()` until one condition is met.

## Architecture Overview

```
Main Game Loop (paused)
    ↓
handle_conversation_tree() [blocks here]
    │
    ├─ OUTER LOOP: Conversation flow
    │   ├─ Display text
    │   ├─ INNER LOOP: Text segments
    │   │   └─ ANIMATION LOOP: Show with timing
    │   │       └─ render_scene() → update_npc_sprite_animations()
    │   ├─ Parse choices
    │   └─ CHOICE LOOP: Wait for selection (if needed)
    │       └─ render_scene() → update_npc_sprite_animations()
    │
    └─ Returns when conversation ends (0xF4)
```

## Key Functions (Ghidra Addresses)

| Function | Address | Purpose |
|----------|---------|---------|
| `handle_conversation_tree` | 0x00018690 | Main conversation loop |
| `display_text_description` | 0x0001a298 | Format text with word wrap |
| `trigger_dialog_or_action` | 0x0001a683 | Render text to bubble |
| `display_talk_animation_and_wait` | 0x000193a8 | Show text with timing |
| `render_dialog_choices_overlay` | 0x0001ab91 | Render choice menu |
| `update_conversation_state` | 0x0001b666 | Restore saved state |
| `render_scene` | 0x00015e4c | Full rendering pipeline |
| `update_npc_sprite_animations` | 0x0001628d | Advance all sprite animations |

## Control Bytes

| Hex | Name | Purpose |
|-----|------|---------|
| 0x08 | SPEAKER_ID | Followed by character ID (0x0D = ALFRED) |
| 0xFB | DIALOGUE_MARKER | Choice/dialogue (followed by index) |
| 0xF1 | DIALOGUE_MARKER_2 | Alternative to 0xFB |
| 0xFD | END_TEXT | End of dialogue line |
| 0xF4 | END_CONVERSATION | Completely ends conversation |
| 0xFA | DISABLED_CHOICE | Choice already selected |
| 0xF8 | ACTION_TRIGGER | Followed by 2 param bytes |

## Choice Detection Algorithm

**Critical Discovery**: 0xFB/0xF1 don't always mean "player choice"

1. Scan for all 0xFB/0xF1 markers
2. Count occurrences of each choice index
3. If index appears **once**: Auto-dialogue (ALFRED speaks automatically)
4. If index appears **2+ times**: Real player choice menu

## Using the Simulator

```bash
# From file
python simulate_conversation.py ALFRED1 12345

# From hex data
python simulate_conversation.py --hex "08 0D 48 6F 6C 61 FD F4"

# Interactive
# - Press Enter to advance dialogue
# - Type number to select choices
# - Disabled choices are marked
```

## Ghidra Improvements Made

Renamed variables in `handle_conversation_tree`:
- `pcVar12` → `conversation_text_ptr`
- `pcVar4` → `current_text_ptr`
- `uStack_28` → `selected_choice_index`

## Key Implementation Details

### Text Advancement Timing
```c
frame_count = 0;
display_frames = text_length / 2;

while (frame_count < display_frames) {
    if (!is_sound_playing() || user_clicked()) {
        return;  // Advance
    }
    render_scene();
    frame_count++;
}
```

### Choice Selection
```c
do {
    wait_or_process_input();
    process_game_state(0);
    render_scene(1);  // 1 = show dialog overlay
} while (!clicked_on_valid_choice());

selected = (mouse_y - choice_start_y) / 16;
```

### State Persistence
```c
// Mark choice as used
*choice_marker = 0xFA;
file_seek(handle, resource_offset + choice_offset);
file_write_byte(handle, 0xFA);
save_conversation_state(room, offset, 0xFA);
```

## Performance Notes

During conversations:
- ✅ Full sprite animation system runs
- ✅ All sprites update (frames, positions, sequences)
- ✅ Palette cycling continues
- ✅ Mouse cursor updates
- ✅ Background rendering
- ❌ No performance optimizations
- ❌ No "lightweight" text mode

The conversation system IS the game loop temporarily.
