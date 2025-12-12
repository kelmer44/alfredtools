# Conversation Loop Architecture

## Overview

The game handles conversations with a **separate nested loop** within the main game loop. When a conversation starts, the main game loop is essentially suspended and control transfers to `handle_conversation_tree()`, which implements its own rendering and input processing loop.

## Main Game Loop vs Conversation Loop

### Main Game Loop (`main_game_loop @ 0x00010442`)

The main game loop runs continuously and handles:
- Input processing via `wait_or_process_input()`
- Game state updates via `process_game_state()`
- Scene rendering via `render_scene()`
- Hotspot interaction detection
- Idle animations (hair combing, screensaver)

**Key Point**: When a conversation starts, this loop is **paused** - it does not continue to execute.

### Conversation Entry Point

When the player interacts with a sprite that has the TALK action:

1. User long-clicks on sprite → Action popup menu appears
2. User clicks talk icon → `check_sprite_hover_and_trigger_conversation()` is called
3. This function calls → `handle_conversation_tree()` which **blocks** until conversation ends

## The Conversation Loop Architecture

### Function: `handle_conversation_tree @ 0x00018690`

This function implements a **separate while loop** that runs for the entire duration of the conversation. It does NOT return to the main game loop until the conversation is completely finished.

### High-Level Structure

```c
void handle_conversation_tree(void) {
    // Initialize conversation state
    DAT_00051785 = 1;  // conversation_active_flag

    // Get pointer to conversation data in resource file
    conversation_text_ptr = get_conversation_start_pointer();

    // OUTER LOOP: Continues until conversation ends (0xF4 byte encountered)
    while (true) {
        // 1. DISPLAY INITIAL TEXT
        wait_or_process_input();
        display_text_description(conversation_text_ptr);

        // 2. PROCESS TEXT SEGMENTS (inner loop)
        while (control_byte != 0xFD && control_byte != 0xF4 && ...) {
            trigger_dialog_or_action(current_text_ptr);
            display_sprite_talk_animation(text_length);
            current_text_ptr++;
        }

        // 3. CHECK END CONDITIONS
        if (control_byte == 0xF4) break;  // End conversation

        // 4. PARSE CHOICE OPTIONS
        // Scan ahead to find all dialogue markers (0xFB/0xF1) with same choice index
        dialog_choice_count = parse_choices();

        // 5. CHOICE RENDERING LOOP (if multiple choices)
        if (dialog_choice_count > 1) {
            // Wait for user to select a choice
            do {
                wait_or_process_input();
                process_game_state(0);      // Still processes input!
                setup_alfred_frame_from_state();
                render_scene(1);            // Renders scene + dialog overlay
            } while (mouse_button_not_clicked_on_choice());

            selected_choice_index = calculate_choice_from_mouse_y();
        }

        // 6. DISPLAY SELECTED/AUTO CHOICE TEXT
        conversation_text_ptr = choice_text_pointers[selected_choice_index];
        display_text_description(conversation_text_ptr);

        // 7. LOOP BACK TO STEP 1 with new text pointer
    }

    DAT_00051785 = 0;  // conversation_active_flag
}
```

## Key Architectural Points

### 1. No Separate Thread or Async Execution

The conversation system does NOT run in a separate thread. It's a **blocking synchronous loop** that runs on the main execution thread.

### 2. Nested Rendering Loop for Choices

When presenting player choices, `handle_conversation_tree()` has its own rendering loop:

```c
// This loop runs INSIDE handle_conversation_tree
do {
    wait_or_process_input();
    process_game_state(0);           // Process input/timing
    setup_alfred_frame_from_state(); // Update sprite state
    render_scene(1);                 // Render with overlay flag
} while (mouse_button_held == 0 || !clicked_on_choice);
```

**Important**: `render_scene()` is called from within the conversation loop, not from the main game loop. The parameter `1` tells it to render the dialog overlay on top.

### 3. The `wait_or_process_input()` Function

This critical function appears throughout the code. It:
- Processes system events (prevents UI freeze)
- Updates timers
- Handles keyboard/mouse input
- Allows the program to remain responsive

**It does NOT wait for user input** - it's more like a "yield" or "pump messages" call.

### 4. Text Advancement Mechanism

#### Displaying a Line of Dialogue

When displaying text, the system:

1. **Parses text into dialog bubble**: `display_text_description()` takes the conversation text and formats it
2. **Renders to cursor buffer**: `trigger_dialog_or_action()` renders the text into a special buffer (`mouse_cursor_frame_ptr`)
3. **Shows animation**: `display_talk_animation_and_wait()` or `display_sprite_talk_animation()` displays the text with character talking animation

#### The Animation/Wait Loop

```c
void display_talk_animation_and_wait(int text_length) {
    DAT_0004fb8e = mouse_button_held;  // Remember if button already held
    DAT_0005300c = 0;  // Frame counter

    while (true) {
        wait_or_process_input();

        // Track mouse button state
        if (mouse_button_held == 0) {
            DAT_0004fb8e = 0;
        }

        // Exit conditions:
        // 1. If no voice: exit when enough frames passed
        // 2. If voice enabled: exit when sound finishes playing
        if ((no_voice && frame_count > text_length/2) ||
            (voice_enabled && !sound_is_playing())) {
            return;  // Advance to next text segment
        }

        // Render the dialog bubble
        render_queue_frame_ptr = mouse_cursor_frame_ptr;
        setup_alfred_frame_from_state();
        render_scene(0);
        process_game_state(1);

        // Early exit: user clicks to skip
        if ((mouse_button_held != 0 || DAT_00051788 != 0) &&
            DAT_0004fb8e == 0) {
            return;  // User clicked - advance immediately
        }

        DAT_0005300c++;  // Increment frame counter
    }
}
```

#### Advancing Through Lines

The conversation advances through multiple dialogue lines in the inner loop:

```c
current_text_ptr = conversation_text_ptr;
control_byte = 0;

// Loop through text segments until hitting a terminator
while (control_byte != 0xFD &&  // End of text
       control_byte != 0xF4 &&  // End conversation
       control_byte != 0xF8 &&  // Action trigger
       control_byte != 0xF0 &&  // Go back
       control_byte != 0xEB) {  // Alt end

    // Render next text segment
    next_ptr = trigger_dialog_or_action(current_text_ptr);

    // Show it with animation (this blocks until done/clicked)
    display_sprite_talk_animation(next_ptr - current_text_ptr);

    // Advance to next segment
    current_text_ptr = next_ptr + 1;
    control_byte = *next_ptr;
}
```

**Key Insight**: Each call to `display_sprite_talk_animation()` **blocks** until:
- Enough time has passed for the text (frames ~ text_length/2)
- Voice finishes playing (if voice enabled)
- User clicks mouse button (skip)

So the advancement is **automatic but timed** - the system shows each line for a duration based on its length, then automatically proceeds to the next line.

## Choice Detection and Parsing

### The Critical Discovery: Not All 0xFB Markers Are Choices

The conversation parser must distinguish between:
- **Player choice menus**: Multiple options with same choice index
- **Auto-dialogue**: Single dialogue lines that ALFRED automatically says

### Parsing Algorithm

```c
// Starting from current position, scan for all 0xFB/0xF1 markers
choice_count = 0;
first_choice_index = -1;

for (scan_ptr = current_text_ptr; *scan_ptr != 0xF5 && *scan_ptr != 0xF7; scan_ptr++) {
    if (*scan_ptr == 0xFB || *scan_ptr == 0xF1) {
        choice_index = *(scan_ptr + 1);

        // If this is a continuation of same choice group
        if (choice_index == first_choice_index) {
            choice_text_pointers[choice_count] = scan_ptr + 2;
            choice_count++;
        }
        // If this is first occurrence
        else if (first_choice_index == -1) {
            first_choice_index = choice_index;
            choice_text_pointers[0] = scan_ptr + 2;
            choice_count = 1;
        }
        // Different choice index - stop scanning
        else if (choice_index < first_choice_index) {
            break;
        }
    }
}

// Determine if it's a real choice or auto-dialogue
if (choice_count == 1) {
    // Auto-dialogue: ALFRED automatically speaks this line
    selected_choice_index = 0;
    // Skip choice rendering loop
} else {
    // Real choice: show menu and wait for player selection
    DAT_00051694 = choice_count;  // Store choice count
    dialog_choice_count = choice_count;

    // Enter choice rendering loop (see section 2 above)
}
```

### Choice Rendering

When `choice_count > 1`, the game enters the choice rendering loop:

```c
do {
    wait_or_process_input();
    process_game_state(0);
    setup_alfred_frame_from_state();

    // Render the scene with dialog choices overlay
    render_scene(1);  // Parameter 1 = render dialog overlay

} while (mouse_button_held == 0 || mouse_y < choice_area_start);

// Calculate which choice was clicked
selected_choice_index = (mouse_y - choice_area_start) / 16;
```

The `render_scene(1)` call knows to render the dialog choices overlay via `render_dialog_choices_overlay()`.

## Conversation State Persistence

### Marking Choices as Used

When a player selects a choice, the game marks it as "used" by writing 0xFA to the resource file:

```c
if (selected_choice_index != auto_choice_special_value) {
    // Find the choice marker in the original text
    *choice_marker_ptr = 0xFA;  // Mark as disabled

    // Write to file
    file_seek(file_handle, resource_offset + choice_offset);
    write_byte(file_handle, 0xFA);

    // Also write to save file
    save_conversation_state(current_room, choice_offset, 0xFA);
}
```

This ensures that:
- The choice won't appear again in future conversations
- The conversation state persists across save/load
- Choices can be "one-time only"

### Update Function: `update_conversation_state @ 0x0001b666`

This function is called when loading a saved game or changing rooms:

```c
void update_conversation_state(int room, int choice_index, byte value) {
    // Store the state in memory array
    conversation_state_array[room * 4 + choice_index] = value;

    // If we're in the same room, update the text data
    if (room == current_room_number) {
        // Find the conversation data in memory
        // Scan through to find the choice marker and update it
        byte* text_ptr = room_text_data_ptr;

        // Complex scanning to find the right 0xFB marker
        while (*text_ptr != 0xFE || *(text_ptr+1) != choice_index) {
            text_ptr++;
        }

        // Update the marker based on how deep in conversation tree
        // (implementation handles nested conversation states)
    }
}
```

## Flow Diagram

```
Main Game Loop
    │
    ├─→ User clicks on sprite with TALK action
    │
    └─→ check_sprite_hover_and_trigger_conversation()
            │
            └─→ handle_conversation_tree()  ← BLOCKS HERE
                    │
                    ├─→ [OUTER LOOP START]
                    │
                    ├─→ Display initial/current text
                    │   └─→ display_text_description()
                    │
                    ├─→ [INNER LOOP: Process text segments]
                    │   │
                    │   ├─→ trigger_dialog_or_action()
                    │   │
                    │   ├─→ display_talk_animation_and_wait()
                    │   │   │
                    │   │   └─→ [ANIMATION LOOP]
                    │   │       │
                    │   │       ├─→ wait_or_process_input()
                    │   │       ├─→ render_scene()
                    │   │       ├─→ Check if done (time/voice/click)
                    │   │       │
                    │   │       └─→ Loop or exit
                    │   │
                    │   └─→ Advance to next segment
                    │
                    ├─→ Parse choices (0xFB/0xF1 markers)
                    │
                    ├─→ If choice_count > 1:
                    │   │
                    │   └─→ [CHOICE RENDERING LOOP]
                    │       │
                    │       ├─→ wait_or_process_input()
                    │       ├─→ process_game_state()
                    │       ├─→ render_scene(1)  ← Renders overlay
                    │       │
                    │       └─→ Wait for click on choice
                    │
                    ├─→ Get selected choice text pointer
                    │
                    ├─→ Mark choice as used (0xFA)
                    │
                    ├─→ Check for end markers (0xF4, etc.)
                    │   │
                    │   ├─→ If end: break outer loop
                    │   └─→ Else: loop back to start
                    │
                    └─→ [LOOP BACK TO OUTER LOOP START]

                    ← Returns when conversation ends

        ← Returns to main game loop

Main Game Loop continues
```

## Animation and Rendering Code Duplication

**Critical Discovery**: YES, all animation advancement code is duplicated/executed within the conversation nested loop!

When `render_scene()` is called from within the conversation loop, it executes:
- `update_npc_sprite_animations()` - Advances animation frames, sequences, and sprite positions
- Full rendering pipeline including sprite drawing, cursor updates, palette cycling
- All the same code that runs in the main game loop

This means:
- Sprite animations continue to play during conversations
- NPCs can move and animate while talking
- The entire game world remains "alive" during dialogue
- Frame counters increment, sequences advance, movement flags are processed

The conversation loop essentially **becomes** the main game loop temporarily, executing all the same rendering and animation logic, just with additional conversation-specific overlays and input handling.

## Summary

1. **No separate while loop from main render loop**: The conversation system DOES have a separate while loop, but it's nested **inside** the main loop, not parallel to it.

2. **Blocking execution**: When a conversation starts, the main game loop is blocked/paused. The `handle_conversation_tree()` function takes over completely.

3. **Text advancement**: Lines advance through:
   - Automatic timing based on text length (frame counter)
   - Voice playback completion (if voice enabled)
   - User mouse click (skip)

4. **Multiple nested loops**:
   - Outer loop: Conversation flow (choice → response → next choice)
   - Inner loop: Text segments within a dialogue
   - Animation loop: Showing each text segment with timing
   - Choice loop: Waiting for player to select an option

5. **Rendering during conversation**: `render_scene()` is called from within the conversation loop, not from the main game loop. It receives a parameter telling it to render dialog overlays.

6. **Animation code duplication**: The full animation and rendering pipeline (`update_npc_sprite_animations()`, sprite rendering, palette cycling, etc.) executes within the conversation loop, keeping the game world animated during dialogue.

7. **State persistence**: Conversation choices are written to both memory and the resource file, ensuring choices persist across sessions.
