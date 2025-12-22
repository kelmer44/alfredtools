Action Queueing System in the Game
I've analyzed the code in Ghidra and renamed key functions and variables. Here's how the system works:

The Mechanism:
1. Action Queue Setup (in main_game_loop):

When the player clicks on a hotspot/NPC, the game first checks if it's a long click (>3 frames) to show the action menu
If it's a quick click, it sets action_pending_flag = 1
Then calls walk_to_target_and_execute_queued_action()
2. Walking Phase (in walk_to_target_and_execute_queued_action):

Saves the action context into "queued" variables:

queued_mouse_hover_state - what was clicked (hotspot/sprite/etc)
queued_hotspot_action_flags - the action flags
queued_hotspot_sprite_index - which sprite/hotspot
queued_sprite_talk_count - conversation state
current_hotspot_extra_id - additional ID data
Walks Alfred to the target:

Calculates pathfinding to target_walk_x and target_walk_y
Iterates through pathfinding_steps_ptr (the path data)
This is a loop - it keeps calling process_game_state() and render_scene() each frame
Updates Alfred's position step by step until reaching destination
The loop checks if the current pathfinding step is -1 (end marker)
After walking completes:

Alfred faces the correct direction based on the hotspot position
Renders a final frame
3. Action Execution:

Checks action_pending_flag - if it's set, executes the queued action
There's a loop that checks for position-based triggers (special room events)
Then restores the mouse position and calls room_specific_action_dispatcher()
4. The Dispatcher:

room_specific_action_dispatcher() clears action_pending_flag = 0
Routes to the appropriate handler based on action type:
execute_room_specific_script - for room scripts
handle_conversation_tree - for conversations
handle_dialog_interaction - for dialogs
dispatch_hotspot_action_by_extra_id - for specific hotspot actions
Various script tables for inventory/item interactions
Key Insight:
There is NO separate queue data structure. Instead, the game uses a synchronous state machine:

Save the action context (what to do)
Execute a blocking walk loop (wait until Alfred reaches the target)
Check the saved flag and execute the queued action
The "queue" is just a set of global variables that preserve the action state during the walking animation. The walking loop is blocking - it doesn't return until Alfred finishes walking, ensuring the sequence is always: walk → then action.

This is simpler than a true queue system but works perfectly for the game's needs since only one action can be pending at a time.
