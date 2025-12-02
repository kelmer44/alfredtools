# DOSBox-X Debugger Guide for HIJODELAGRANPUTA Cheat Code

## Quick Start

1. Launch DOSBox-X and mount your game directory:
   ```
   dosbox-x
   ```

2. In DOSBox-X, mount the game folder:
   ```
   mount c /Users/gabriel/Desktop/source/alfredtools/files
   c:
   ```

3. Run the game:
   ```
   ALFRED.COM
   ```

## Debugging the Cheat Code

### Method 1: Set Breakpoint (Recommended)

1. **Open debugger**: Press `Alt+Pause` (or `Alt+F12` on some keyboards)

2. **Set breakpoint at cheat check**:
   ```
   BP 10500
   ```

3. **Continue execution**:
   ```
   F5
   ```

4. **Type 'H' in the game** (first letter of cheat)

5. **If debugger breaks**, you're in the right place:
   - Type `D 495F3` to see the flag value
   - If it shows `00`, patch it: `E 495F3 01`
   - Type `G` to continue

6. **Try the full cheat code**: HIJODELAGRANPUTA

### Method 2: Direct Memory Patch

If the breakpoint doesn't trigger, the address might be different:

1. Open debugger: `Alt+Pause`

2. Search for the cheat string in memory:
   ```
   S 40000 L FFFF "HIJODELAGRANPUTA"
   ```

3. This will show you where the string is in memory

4. Set breakpoint at that address range

### Method 3: Jump Directly to Jukebox

If you want to skip the cheat entirely and go straight to jukebox:

1. Open debugger during gameplay: `Alt+Pause`

2. Jump to the jukebox activation code:
   ```
   R EIP 10549
   ```

3. Continue:
   ```
   F5
   ```

This should load the jukebox mode directly.

## Debugger Commands Reference

- `BP <address>` - Set breakpoint
- `BL` - List breakpoints
- `BC <number>` - Clear breakpoint
- `D <address>` - Display memory
- `E <address> <value>` - Edit memory
- `U <address>` - Unassemble (show code)
- `R` - Show registers
- `R <register> <value>` - Set register value
- `G` - Go (continue execution)
- `F5` - Continue
- `F10` - Step over
- `F11` - Step into
- `Q` - Quit debugger

## Expected Behavior

When the cheat works, you should:
1. Hear sound effect "9ZZZZZZZ.SMP"
2. See music selection UI
3. Use arrow keys to navigate tracks
4. Press ESC to exit

## Troubleshooting

If nothing happens:
1. Make sure you're typing during gameplay (not in menu/cutscenes)
2. Try typing faster (no delays between letters)
3. Check if you're in a specific room that matters
4. Use Method 3 to jump directly to jukebox
