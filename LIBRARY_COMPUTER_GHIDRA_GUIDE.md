# Library Computer - Ghidra Reverse Engineering Guide

## Function to Define

### library_computer_handler (0x10E2E)

**Address**: 0x10E2E (Ghidra)  
**Dispatch**: F8 Action 270 (0x010E)  
**Purpose**: Main handler for the library computer interface in Room 9

**To create the function in Ghidra:**
1. Navigate to address 0x10E2E
2. Press 'D' to disassemble if needed
3. Press 'F' or right-click → "Create Function"
4. Rename to `library_computer_handler`

**Expected behavior:**
- Loads Extra Screen 1 from ALFRED.7 (computer UI background)
- Displays menu with CONSULTAR POR TITULO/AUTOR/CANCELAR
- Handles keyboard input for search
- Reads book database from ALFRED.7 at 0x309E0
- Displays book results with shelf locations
- Implements Memorizar functionality for physical books

## Data References to Find

### Book Database (ALFRED.7)

```
kBookDatabaseOffset = 0x309E0
kBookDatabaseEnd = 0x33F05
kBookEntrySize = 108  // bytes per book
kTotalBooks = 125
```

Look for:
- File seek operations to 0x309E0 in ALFRED.7
- Buffer reads of 108 bytes
- Loops that iterate 125 times

### UI Strings (JUEGO.EXE)

| Address | String | Variable Name Suggestion |
|---------|--------|--------------------------|
| 0x49038 | "CONSULTAR POR TITULO" | str_ConsultarPorTitulo |
| 0x49058 | "CONSULTAR POR AUTOR" | str_ConsultarPorAutor |
| 0x490B9 | "Titulo    : " | str_LabelTitulo |
| 0x49102 | "Autor     : " | str_LabelAutor |
| 0x49132 | "Genero    : " | str_LabelGenero |
| 0x491A3 | "Disponible" | str_Disponible (unused?) |
| 0x491AF | "Prestado" | str_Prestado (unused?) |
| 0x491BB | "TITULO" | str_Titulo |
| 0x491C3 | "AUTOR" | str_Autor |
| 0x49271 | "CANCELAR" | str_Cancelar |
| 0x491CD | "xxBueno... Tendre que buscar en la estanteria de la" | str_MemorizarDialog |

### Display Book Data (JUEGO.EXE)

**Address**: 0x473A8 - 0x48903  
**Purpose**: Pre-formatted book display text with formatting codes

Look for xrefs to this region from:
- handle_conversation_tree (0x18690) - uses offset 0x47E58
- handle_dialog_interaction (0x18F10) - uses offset 0x47E58

Note: Address 0x47E58 appears to be within the formatted book data region

## Variables to Rename

### In library_computer_handler (0x10E2E)

Look for local variables that likely represent:

```c
char search_letter;           // Letter entered by user (A-Z)
int search_type;              // 0 = by title, 1 = by author
int current_result_index;     // Index into search results
int result_count;             // Number of matching books
int book_index;               // Current book being displayed
int memorized_book_index;     // Book that was memorized (-1 if none)
byte* book_buffer;            // Buffer for reading book entries
char shelf_letter;            // A-Z shelf letter
byte shelf_row;               // 1-3 shelf row
byte status_byte;             // 0x01 or 0x02
```

### Global Variables

Look for global/static variables:

```c
// ALFRED.7 file handle (if separate from main handle)
int alfred7_file_handle;  // Likely near 0x4F908

// Memorized book state (persistent across computer sessions)
int g_memorized_book_shelf_letter;
byte g_memorized_book_shelf_row;
bool g_has_memorized_book;
```

## Functions Called By Handler

The computer handler likely calls these existing functions:

1. **getExtraScreen** or similar (loads Extra Screen 1)
2. **file_seek** / **file_read** (reads from ALFRED.7)
3. **display_text** / text rendering functions
4. **check_keyboard_input** or keyboard handler
5. **display_alfred_talking** (for Memorizar dialog)

Search for calls within the handler to identify these.

## Nearby Handler Functions

From action_dispatch_tables_extracted.json, nearby entries:

| Action | Address | Suggested Name |
|--------|---------|----------------|
| 268 | 0x10E18 | unknown_handler_268 |
| 270 | 0x10E2E | library_computer_handler |
| 271 | 0x11221 | unknown_handler_271 |

These might be other Room 0 (bedroom) handlers. Check if 268 is defined.

## Reverse Engineering Steps

### Step 1: Locate File Operations
```
Search for: 0x309E0 (as immediate value or data reference)
Expected: lseek/seek call with ALFRED.7 file handle
```

### Step 2: Find String References
```
Search for xrefs to: 0x49038, 0x49058, 0x49271
These should appear in the main menu display code
```

### Step 3: Identify Search Loop
```
Look for:
- Loop that compares search_letter with book.title[0] or book.author[0]
- Buffer operations with 108-byte increments
- Array/list building for search results
```

### Step 4: Trace Memorizar
```
Look for:
- Code that handles 'M' key press
- Writes to game state/flags
- Calls to display_alfred_talking with string at 0x491CD
- Game state variable that stores (shelf_letter, shelf_row, book_id)
```

### Step 5: Find Shelf Interaction
```
In room handlers for Room 9:
- Look for code that checks g_has_memorized_book flag
- Hotspot handlers for shelf columns I-Z
- Item pickup code triggered by memorized book
```

## Book Entry Parsing Code Pattern

Expected pseudocode in the handler:

```c
void search_books(char search_letter, int search_type) {
    byte book_buffer[108];
    int result_count = 0;
    
    file_seek(alfred7_handle, 0x309E0, SEEK_SET);
    
    for (int i = 0; i < 125; i++) {
        file_read(alfred7_handle, book_buffer, 108);
        
        char* search_field = search_type == 0 ? 
            &book_buffer[0] :   // title offset
            &book_buffer[55];   // author offset
        
        // Compare first letter (case-insensitive)
        if (toupper(search_field[0]) == search_letter) {
            results[result_count++] = i;
        }
    }
}
```

## Memorizar Implementation Pattern

Expected pseudocode:

```c
void memorize_book(int book_index) {
    byte book_buffer[108];
    
    // Read the book entry
    file_seek(alfred7_handle, 0x309E0 + (book_index * 108), SEEK_SET);
    file_read(alfred7_handle, book_buffer, 108);
    
    char shelf_letter = book_buffer[105];
    byte shelf_row = book_buffer[106];
    byte status = book_buffer[107];
    
    // Only physical books can be memorized
    if (status == 0x02) {
        g_memorized_book_shelf = shelf_letter;
        g_memorized_book_row = shelf_row;
        g_has_memorized_book = true;
        
        // Display Alfred's dialog
        char dialog[100];
        sprintf(dialog, str_MemorizarDialog, shelf_letter);
        display_alfred_talking(dialog);
    }
}
```

## Testing in Ghidra

After renaming functions and variables:

1. Check decompiled code for readability
2. Verify parameter types (file handles, buffers, etc.)
3. Look for calls to renamed functions from other handlers
4. Check if memorized book state is used in shelf interaction code
5. Document any game state flags or global variables found

## Related Systems to Investigate

1. **Library shelf hotspots** - Room 9 has multiple shelf columns
2. **Item pickup system** - How physical books enter inventory
3. **Dialog system** - How memorize message is spoken by Alfred
4. **Game state persistence** - Is memorized book saved with game?

## Documentation Updates Needed

After Ghidra work, update:
- LIBRARY_COMPUTER_DOCUMENTATION.md with function addresses
- SAVE_GAME_SYSTEM_ANALYSIS.md if book state is in save games
- Add new .md file if shelf interaction deserves separate doc
