# alfredtools

A minimal C program that generates PNG images. Uses [LodePNG](https://github.com/lvandeve/lodepng) for encoding (included in source).

## Build

```bash
make
```

This will create `bin/alfredcli`.

Note: the build now compiles `src/alfred2.c` as part of the program (it contains `extractAlfredAnims()` / `saveAnim()` used by `main.c`).

## Usage

```bash
./bin/alfredcli [output.png]
```

If no output path is specified, writes to `out.png` in the current directory.

Example:
```bash
./bin/alfredcli gradient.png
```

This creates a 256x256 RGB gradient pattern saved as PNG.

## Project Structure

- `src/main.c` - Main program (PNG generator)
- `src/lodepng.c` - PNG encoder implementation
- `src/lodepng.h` - PNG encoder header
- `Makefile` - Build configuration
 - `src/alfred2.c` - Alfred .2 extraction and palette-based PNG saving (compiled into the binary)

## Development

Clean and rebuild:
```bash
make clean && make
```

### VS Code: build & debug

The project includes VS Code launch/tasks config so you can build and debug the CLI from the editor.

1. Install one of the debuggers:
	- CodeLLDB (`vadimcn.vscode-lldb`) — recommended on macOS
	- Microsoft C/C++ (`ms-vscode.cpptools`) to use the `cppdbg` configuration

2. Open the folder in VS Code.
3. Press F5 or open the Run view and choose "Build & Launch (CodeLLDB)" (or the `cppdbg` configuration).
	This will run the `build` task (runs `make`) then start the debugger with `bin/alfredcli test.png` as the default argument.

If you need to pass different arguments, edit `.vscode/launch.json` or change the args before launching.


## License

- Project code is available under the MIT license
- LodePNG is included under its zlib license
