# alfredtools

A minimal C program that generates PNG images. Uses [LodePNG](https://github.com/lvandeve/lodepng) for encoding (included in source).

## Build

```bash
make
```

This will create `bin/alfredcli`.

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

## Development

Clean and rebuild:
```bash
make clean && make
```

## License

- Project code is available under the MIT license
- LodePNG is included under its zlib license