# Alfred Animation Timing System

## Overview

The original game uses an 18.2 Hz (55ms) base clock. However, different game states
cause `render_scene()` (and thus sprite frame advancement) to fire at different effective
rates. This is why walking and talking animations appear noticeably slower than background
animations.

## How `process_game_state(N)` Controls Speed

`process_game_state(N)` is a blocking wait:

```c
void process_game_state(void) {
    N = __STK();  // parameter
    target_tick = game_tick_counter + N;
    do {
        wait_or_process_input();  // ≈1 tick each call
    } while (game_tick_counter <= target_tick);
}
```

It advances the internal counter by `N` extra ticks before returning. Combined with the
mandatory `wait_or_process_input()` that precedes each loop iteration, the effective cost
per render loop iteration is `1 + N` game ticks.

## Render Rate per Game State

| Game State                  | `process_game_state(N)` | Ticks per render | ms per render | Factor vs normal |
|-----------------------------|-------------------------|-----------------|---------------|-----------------|
| Main game loop (idle)       | N=0                     | 1               | 55ms          | 1×              |
| Alfred **walking**          | N=1                     | 2               | 110ms         | 0.5×            |
| Alfred **talking**          | N=1                     | 2               | 110ms         | 0.5×            |
| NPC talking (sprite anim)   | N=`speedByte`           | 1+`speedByte`   | 55×(1+`speedByte`)ms | varies  |

Where `speedByte` = `ALFRED.2_header[talkSlot*12 + 0x12]` (one byte per talkable sprite slot).

## Effect on Animation Frame Advancement

Sprite frames advance **once per render call** (inside `update_npc_sprite_animations →
drawNextFrame`). With a per-frame delay counter also incremented per render, this means:

- At **55ms per render** (idle): a sprite with frame delay 2 advances every 110ms.
- At **110ms per render** (walking/Alfred talking): the same sprite advances every 220ms
  — it appears at half the normal speed in wall-clock time.

## Specific Cases

### Alfred Walking
- `walk_to_target_and_execute_queued_action` calls `process_game_state(1)`.
- Each step of Alfred's walk loop takes 2 ticks = 110ms.
- All sprites (background NPCs, decorations) on screen also appear at half speed.

### Alfred Talking
- `display_talk_animation_and_wait` calls `process_game_state(1)`.
- Same 110ms per loop iteration effect.

### NPC Talking (Sprite Talk Animation)
- `display_sprite_talk_animation` calls `process_game_state(bVar1)`.
- `bVar1` = byte at `alfred2_talk_anim_header_ptr + 0x12 + (talkSlot * 0x0C)`.
- If `bVar1 = 0`: 2 ticks per render (same as Alfred talking).
- If `bVar1 = 1`: 3 ticks per render = 165ms.
- Higher values = even slower.
- This value controls both the render throttle AND the lip-sync animation speed
  (they're coupled in the original).

## Dialog TTL Invariance

Despite the slower render rate, the dialog auto-dismiss timer is **invariant** to this
slowdown. From Ghidra:

- TTL condition: `text_length / (N+1) < frame_counter`
- Frame counter increments once per loop (not per tick)
- Each loop takes `1+N` ticks
- Total TTL = `(text_length / (N+1)) × (1+N) × 55ms = text_length × 55ms`

So dialog display time is always `≈ char_count × 55ms` regardless of `N`. The slowdown
only affects animation appearance, not how long text stays on screen.

## ScummVM Implementation Notes

The current ScummVM implementation renders at a consistent rate regardless of state.
To reproduce the original behavior:

1. **Walking**: During `walkLoop()`, add a 2-tick wait per iteration instead of the
   current 1-tick wait (or advance animation state every other tick).
   
2. **Alfred talking**: During `displayDialogue()`, render animations at half the speed
   (e.g., only advance sprite frames every 2 game ticks).

3. **NPC talking**: Would require reading `speedByte` from ALFRED.2 header per NPC
   and applying a corresponding per-frame skip.

## Notes

- The 55ms tick rate was confirmed from the DOS timer interrupt (18.2Hz ≈ 55ms/tick).
- `wait_or_process_input` effectively waits for the next 55ms tick boundary.
- The background animations run on the same render call, so they also slow down during
  walking/talking — this is faithful to the original.
