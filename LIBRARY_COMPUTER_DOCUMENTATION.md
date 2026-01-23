# Library Computer System Documentation

## Overview

The library computer in Room 9 (Biblioteca) of Alfred Pelrock allows players to search the library's catalog of books by title or author. This document describes the original DOS implementation and the ScummVM reimplementation.

## Original DOS Implementation

### Action Handler

- **F8 Action ID**: 270 (0x010E)
- **Handler Address**: Ghidra 0x10E2E (file offset 0x1502E in JUEGO.EXE)
- **Dispatch Table**: 0x47E58

The computer is activated via the F8 opcode system when the player interacts with the computer hotspot in Room 9.

### Data Sources

1. **ALFRED.7 Book Database** (offset 0x33043)
   - Raw book entries for search functionality
   - Format: Title (55 bytes) | Author (30 bytes) | Genre (22 bytes) | Shelf (1 byte)
   - Entry delimiters: 0x01 (standard) or 0x02/0x03 patterns
   - 26 books total

2. **JUEGO.EXE Display Strings** (offset 0x473A8)
   - Pre-formatted book data with "Titulo:", "Autor:", "Genero:" labels
   - Used for on-screen display

3. **UI Menu Strings** (offset 0x4901D)
   - "MENU PRINCIPAL"
   - "CONSULTAR POR TITULO"
   - "CONSULTAR POR AUTOR"
   - "SALIR"
   - "Disponible" / "Prestado"

### Computer Background

The computer UI background is loaded from ALFRED.7 as "Extra Screen 1", using the same mechanism as other special screens.

## ScummVM Implementation

### Files

- `engines/pelrock/library_books.h` - Book database extracted from ALFRED.7
- `engines/pelrock/pelrock.cpp` - computerLoop() function implementation

### LibraryBook Structure

```cpp
struct LibraryBook {
    const char *title;
    const char *author;
    const char *genre;
    char shelf;       // A-H shelf location, '?' if unknown
    bool available;   // true = Disponible, false = Prestado
};
```

### Computer States

1. **STATE_MAIN_MENU** - Shows main menu with three options:
   - Press 1: Search by title
   - Press 2: Search by author
   - Press 3 or ESC: Exit

2. **STATE_SEARCH_BY_TITLE** / **STATE_SEARCH_BY_AUTHOR**
   - User enters a letter (A-Z)
   - System searches for books where title/author starts with that letter

3. **STATE_SHOW_RESULTS**
   - Displays matching books one at a time
   - Navigation: Space/Right/Down = Next, Left/Up = Previous
   - ESC returns to main menu

### Key Bindings

| Key | Action |
|-----|--------|
| 1 | Select "Search by Title" |
| 2 | Select "Search by Author" |
| 3 | Exit |
| A-Z | Enter search letter |
| Space/Right/Down | Next result |
| Left/Up | Previous result |
| ESC | Back/Exit |

## Book Database

26 books extracted from ALFRED.7:

| # | Title | Author | Genre | Shelf |
|---|-------|--------|-------|-------|
| 1 | Pinocho en el Parlamento | Carmen Tirosa | Cronica Social | ? |
| 2 | Hagase famoso gracias a la energia de las petunias | Carmelo Cuelo | Esoterismo | ? |
| 3 | Dios mio, ¡Que cruz! | Jesus de Nazaret | Autobiografia | ? |
| 4 | Psicologia de la motivacion inmotivada | Dr. Chemi | Psicologia | ? |
| 5 | Un mundo Feliz | Aldous Huxley | Novela | ? |
| 6 | Sexo oral y por escrito | Franz Masturmann | Sexologia | ? |
| 7 | Vida sexual del escarabajo de la Patagonia | Dr. Tedio Plomez | Botanica | ? |
| 8 | Manual del necrofago | Jesus Gil | Manual | ? |
| 9 | Canticos espirituales en formato *.ZIP | Doctor Chip | Poesia | B |
| 10 | Plopuestas colelacionales... | Senadol Chan Chu Yo | Politica | ? |
| 11 | Ereh un fistro | Chiquito de la casa | Humor | ? |
| 12 | El hacedor de la Lluvia | Herman Hesse | Cuentos | ? |
| 13 | Pasiones recalcitrantes | Corin Tellado | Novela rosa | C |
| 14 | El valenciano en los albores del siglo XXI | Jaume i Pascual | Nacionalismo | D |
| 15 | Valencia: mes que mai | Jaume i Pascual | Nacionalismo | ? |
| 16 | Sistema inmunitario de los cefalopodos (v. I) | Dr. Tedio Plomez | Biologia | E |
| 17 | Sistema inmunitario de los cefalopodos (v. III) | Dr. Tedio Plomez | Biologia | ? |
| 18 | Sistema inmunitario de los cefalopodos (v. IV) | Dr. Tedio Plomez | Biologia | ? |
| 19 | Sistema inmunitario de los cefalopodos (v. V) | Dr. Tedio Plomez | Biologia | ? |
| 20 | Dos mas dos son cinco | Joan Josep Climent Colomer | Matematicas | F |
| 21 | Autobiografia de una miseria humana | Joan Josep Climent Colomer | Esperpento | ? |
| 22 | El arte mundial antes y despues de mi | Nacho Taulet Perman | Arte | ? |
| 23 | Llamame cuando se muera tu abuelo | Jose Bart Carrion | Teatro | ? |
| 24 | Soy un incomprendido | Jose Bart Carrion | Autobiografia | ? |
| 25 | El arte de limpiar botijos por dentro | Varios autores | Manualidades | ? |
| 26 | Aprenda Egipcio en 10 dias | Varios autores | Manual | H |

### Known Shelf Assignments

- Shelf B: Poesia
- Shelf C: Novela rosa
- Shelf D: Nacionalismo
- Shelf E: Biologia
- Shelf F: Matematicas
- Shelf H: Manual

## Notes

1. The book titles include many Spanish cultural references and humor (e.g., Chiquito de la Calzada, Corin Tellado, Karlos Arguiñano parodies)

2. Some shelf assignments are marked as '?' because they weren't found in the data - the original game may determine these dynamically or they may exist in JUEGO.EXE's formatted data

3. The "Disponible/Prestado" (Available/On Loan) status appears to be set dynamically based on game state - in the current implementation all books are marked as available

## Future Improvements

1. Parse shelf letters more accurately from ALFRED.7 data
2. Implement dynamic availability based on game state
3. Add "Memorizar" (Memorize) functionality to store book locations
4. Better text wrapping for long titles
