# Library Computer System Documentation

## Overview

The library computer in Room 9 (Biblioteca) of Alfred Pelrock allows players to search the library's catalog of **125 books** by title or author. When a physical book is found, players can "Memorizar" (memorize) its shelf location to later pick it up from the library shelves.

This document describes the complete book database format, the original DOS implementation, and the ScummVM reimplementation.

## Original DOS Implementation

### Action Handler

- **F8 Action ID**: 270 (0x010E)
- **Handler Address**: Ghidra 0x10E2E (function not yet defined in Ghidra)
- **Dispatch Table Entry**: File offset 0x4B058 (action_dispatch_tables_extracted.json)
- **Room**: 9 (Biblioteca)

The computer is activated via the F8 opcode system when the player interacts with the computer hotspot in Room 9.

### Data Sources

#### 1. ALFRED.7 Book Database (0x309E0 - 0x33F05)

**Complete book catalog**: 125 books, 13,605 bytes (0x3525)

**Entry Format** (108 bytes per book):

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 55 | Title | Space-padded string (may contain 0xC8 line breaks) |
| 55 | 30 | Author | Space-padded string |
| 85 | 20 | Genre | Space-padded string |
| 105 | 1 | Shelf Letter | A-Z for physical shelf, 0x20 (space) if catalog-only |
| 106 | 1 | Shelf Row | 1-3 for row number, 0x20 (space) if catalog-only |
| 107 | 1 | Status | 0x01 = catalog-only, 0x02 = physical copy on shelf |

**Special Characters**:
- `0xC8` (╚ in CP437) - Line break marker within title text
- `0xAD` - Soft hyphen
- `0xA4` - ñ character

**Book Distribution**:
- **78 books**: Catalog-only (status 0x01) - can search but cannot pick up
- **47 books**: Physical copies (status 0x02) - can be memorized and picked up from shelves
- **Shelf letters**: I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z (physical books only)
- **Rows per shelf**: 1, 2, or 3

#### 2. JUEGO.EXE Display Strings (0x473A8 - 0x48903)

Pre-formatted book data with display codes for approximately 50 books. Used for text rendering with color/formatting:
- `0x08 0x07` - Start label (e.g., "Titulo:")
- `0x08 0x0F` - Start content
- `0xC8` - Newline
- `0xFD 0x00` - End of entry

#### 3. UI Menu Strings in JUEGO.EXE

| Offset | String | Purpose |
|--------|--------|---------|
| 0x49038 | "CONSULTAR POR TITULO" | Menu option 1 |
| 0x49058 | "CONSULTAR POR AUTOR" | Menu option 2 |
| 0x490B9 | "Titulo    : " | Result label |
| 0x49102 | "Autor     : " | Result label |
| 0x49132 | "Genero    : " | Result label |
| 0x491A3 | "Disponible" | Unused (catalog books shown differently) |
| 0x491AF | "Prestado" | Unused (physical books shown with shelf) |
| 0x491BB | "TITULO" | Search option |
| 0x491C3 | "AUTOR" | Search option |
| 0x49271 | "CANCELAR" | Cancel/exit option |
| 0x491CD | "xxBueno... Tendre que buscar en la estanteria de la" | Dialog after Memorizar |

### Computer UI Flow

1. **Main Menu**
   - Option 1: CONSULTAR POR TITULO (Search by title)
   - Option 2: CONSULTAR POR AUTOR (Search by author)
   - Option 3: CANCELAR (Cancel/exit)

2. **Search Input**
   - Prompt: "Teclea una letra (A-Z):"
   - User enters a letter
   - System searches for matching books

3. **Results Display**
   - Shows: Title, Author, Genre, Situacion
   - **Catalog-only books**: "Situacion: Solo en catalogo"
   - **Physical books**: "Situacion: Estante X, fila N" (Shelf X, row N)
   - Navigation options:
     - **(M)emorizar** - Only for physical books; memorizes shelf location
     - **(S)eguir** - Continue to next result
     - **(C)ancelar** - Return to main menu

4. **After Memorizar**
   - Alfred speaks: "Bueno... Tendre que buscar en la estanteria de la X" (I'll have to look at shelf X)
   - Game sets flag allowing the book to be picked up from that shelf in the library
   - Computer interface exits

### Computer Background

The computer UI background is loaded from ALFRED.7 as "Extra Screen 1", using the same mechanism as other special screens in the game.

## ScummVM Implementation

### Files

- `engines/pelrock/library_books.h` - Complete book database (125 books)
- `engines/pelrock/computer.h` - Computer class interface
- `engines/pelrock/computer.cpp` - Computer class implementation
- `engines/pelrock/pelrock.cpp` - computerLoop() wrapper function

### LibraryBook Structure

```cpp
struct LibraryBook {
    const char *title;
    const char *author;
    const char *genre;
    char shelfLetter;      // A-Z for shelf location, space if catalog-only
    byte shelfRow;         // 1-3 for row number, 0 if catalog-only
    bool hasPhysicalCopy;  // true = can be found on shelf, false = catalog only
};
```

### Computer Class

```cpp
class Computer {
public:
    Computer(PelrockEngine *engine);
    void run();  // Main computer interface loop

private:
    enum ComputerState {
        STATE_MAIN_MENU,
        STATE_SEARCH_BY_TITLE,
        STATE_SEARCH_BY_AUTHOR,
        STATE_SHOW_RESULTS,
        STATE_EXIT
    };

    int _memorizedBookIndex;  // Book player memorized (-1 if none)

    void handleMainMenu();
    void handleSearchInput();
    void handleResultsDisplay();
    void performSearch();
    void memorizeBook(int bookIndex);
};
```

### Key Bindings

| Key | Action |
|-----|--------|
| 1 | Select "Search by Title" |
| 2 | Select "Search by Author" |
| 3, C | Exit / Cancel |
| A-Z | Enter search letter |
| M | Memorize book location (physical books only) |
| S, Space, Right, Down | Next result / Continue |
| Left, Up | Previous result |
| ESC | Back/Exit |

## Complete Book Database (125 Books)

Extracted from ALFRED.7 offset 0x309E0. See `library_books.json` for full machine-readable data.

### Physical Books by Shelf (47 total)

Books that can be memorized and picked up from library shelves:

**Shelf I** (Row 1): Gato por liebre (Karlos Arguiñano)

**Shelf J** (Row 1): Enrique de Ofterdingen (Novalis)

**Shelf K** (Row 1): Codigo Maquina a pelo (Programadores reunidos)

**Shelf L** (Row 1): Te parto la cara ¡ Capuyo ! (Jhonny Rapper)

**Shelf M** (Row 1): En las selvas de Londres (Coronel Tapioca)

**Shelf N** (Row 1): El ultimo paso para la cuadratura del circulo (Anonimo)

**Shelf O** (Row 1): Enciclopedia de bolsillo (Profesor Lumbreras)

**Shelf P** (Row 1-3): Multiple books including sports and self-help

**Shelf Q-Z**: Various fiction, science, and reference books

*See library_books.json for complete shelf mappings*

### Catalog-Only Books (78 total)

Books that can be searched but have no physical copy to pick up:
- Los hombres: ¡ Como caparlos ! (Herminia Gutierrez)
- Mujeres del mundo: ¡ No os depileis las axilas ! (Herminia Gutierrez)
- Hamlet (William Shakespeare)
- Fausto (Goethe)
- Many more classics and humorous titles

### Sample Book Entries (First 10)

| # | Title | Author | Genre | Shelf | Type |
|---|-------|--------|-------|-------|------|
| 1 | Los hombres: ¡ Como caparlos ! | Herminia Gutierrez | Feminismo | - | Catalog |
| 2 | Mujeres del mundo: ¡ No os depileis las axilas ! | Herminia Gutierrez | Feminismo | - | Catalog |
| 3 | Gato por liebre | Karlos Arguiñano | Cocina | I1 | Physical |
| 4 | Hamlet | William Shakespeare | Teatro | - | Catalog |
| 5 | Fausto | Goethe | Novela | - | Catalog |
| 6 | Enrique de Ofterdingen | Novalis | Novela | J1 | Physical |
| 7 | Guia de desobediencia civica | Azagra | Ensayo | - | Catalog |
| 8 | Literatura en la edad de piedra | Profesor Cebollo | Ensayo | - | Catalog |
| 9 | Turbo C ++ con Intratex | Programadores reunidos | Informatica | - | Catalog |
| 10 | Codigo Maquina a pelo | Programadores reunidos | Informatica | K1 | Physical |

## Technical Notes

### Character Encoding

Books use CP437 (DOS) encoding:
- Standard ASCII for most text
- Extended characters for Spanish accents (á, é, í, ó, ú, ñ, ¿, ¡)
- 0xC8 (╚) used as internal line break marker for long titles

### Book Title Humor

Many books are parodies or references to Spanish culture:
- **Karlos Arguiñano**: Famous Spanish TV chef
- **Corin Tellado**: Prolific Spanish romance novelist
- **Chiquito de la Calzada**: Spanish comedian known for invented words
- **Doctor Chip**: Reference to Spanish computer magazine
- **Jaume i Pascual**: Parody name for Valencian nationalism books
- **Joan Josep Climent Colomer**: Self-referential humor (team member?)

### ALFRED.7 File Structure Context

The book database sits between other data in ALFRED.7:
- Before: Various graphics and animation data
- **0x309E0 - 0x33F05**: Book database (125 entries × 108 bytes)
- After: More graphics data

## Future Improvements / TODO

1. **Ghidra Reverse Engineering**
   - Define function at 0x10E2E as `library_computer_handler`
   - Trace how Memorizar sets game flags
   - Find shelf interaction code that checks memorized books

2. **ScummVM Implementation**
   - Play Alfred's dialog after Memorizar
   - Set game state flag for memorized book
   - Implement shelf interaction to pick up memorized books
   - Optional: Load books from ALFRED.7 at runtime instead of static array

3. **Documentation**
   - Map all 47 physical books to their exact shelf locations
   - Document the shelf pickup interaction system
   - Find game flags that track which books are borrowed/available

## References

- `action_dispatch_tables_extracted.json` - Action 270 dispatch entry
- `library_books.json` - Machine-readable book database
- `library_books_full.h` - ScummVM C++ header with all books
- `extract_alfred7_books_full.py` - Python extraction script
