#!/usr/bin/env python3
"""
Alfred Pelrock - Text Display Algorithm
Decompiled from the game executable at address 0x0001a298 (display_dialog_text)

This algorithm handles word wrapping and text display for dialog and hotspot descriptions.
The text is rendered in pink (color 13 in palette) when examining hotspots.
"""

# Constants found in the decompiled code
MAX_CHARS_PER_LINE = 0x2F  # 47 characters
MAX_LINES = 4  # Maximum number of lines before showing next page

# Control character codes (negative values in signed char)
CHAR_SPACE = 0x20          # ' '
CHAR_END_MARKER_1 = 0xFD   # -3 (end of text marker)
CHAR_END_MARKER_2 = 0xF4   # -0xC (alternate end marker)
CHAR_END_MARKER_3 = 0xF8   # -8 (another end marker)
CHAR_END_MARKER_4 = 0xF0   # -0x10 (another end marker)
CHAR_NEWLINE = 0xF6        # -10 (newline marker)
CHAR_PAGE_BREAK = 0xF9     # marker inserted when switching pages


def is_end_marker(char_byte):
    """Check if a character is an end-of-text marker"""
    return char_byte in [CHAR_END_MARKER_1, CHAR_END_MARKER_2,
                         CHAR_END_MARKER_3, CHAR_END_MARKER_4]


def is_word_boundary(char_byte):
    """Check if a character marks the end of a word"""
    return (char_byte == CHAR_SPACE or
            is_end_marker(char_byte))


def calculate_word_length(text, position):
    """
    Calculate the length of the current word starting at position.

    Returns:
        word_length: Number of characters in the word (including space)
        is_end: Whether this is the end of the text
    """
    word_length = 0
    pos = position
    is_end = False

    # Count characters until we hit a space or end marker
    while pos < len(text):
        char = text[pos]

        if char == CHAR_SPACE or is_end_marker(char):
            break

        word_length += 1
        pos += 1

    # Check if we hit an end marker
    if pos < len(text) and is_end_marker(text[pos]):
        is_end = True

    # Add 1 for the space (or 3 if it's the special -8 marker)
    if pos < len(text):
        if text[pos] == CHAR_END_MARKER_3:  # 0xF8 (-8)
            word_length += 3
        else:
            word_length += 1

    return word_length, is_end


def word_wrap_text(text, max_chars_per_line=MAX_CHARS_PER_LINE, max_lines=MAX_LINES):
    """
    Wrap text using the Alfred Pelrock algorithm.

    The algorithm:
    1. Process text word by word
    2. If word fits on current line, add it
    3. If word doesn't fit (chars_remaining < word_length), move to next line
    4. Maximum 4 lines per page, then insert page break
    5. Center shorter lines by padding with spaces

    Args:
        text: Input text as bytes or string
        max_chars_per_line: Maximum characters per line (default 47)
        max_lines: Maximum lines per page (default 4)

    Returns:
        List of pages, where each page is a list of lines
    """
    if isinstance(text, str):
        text = text.encode('latin-1')

    pages = []
    current_page = []
    current_line = []
    chars_remaining = max_chars_per_line
    current_line_num = 0
    position = 0

    while position < len(text):
        word_length, is_end = calculate_word_length(text, position)

        # Extract the word (including the space at the end)
        word = text[position:position + word_length].decode('latin-1', errors='replace')

        # Key decision: if chars_remaining < word_length, wrap to next line
        if chars_remaining < word_length:
            # Word doesn't fit - move to next line

            # Save current line (strip trailing space)
            current_page.append(''.join(current_line).rstrip())
            current_line = []
            chars_remaining = max_chars_per_line
            current_line_num += 1

            # Check if we need a new page
            if current_line_num >= max_lines:
                pages.append(current_page)
                current_page = []
                current_line_num = 0

        # Add word to current line
        current_line.append(word)
        chars_remaining -= word_length
        position += word_length

        if is_end:
            break

    # Save remaining line and page
    if current_line:
        current_page.append(''.join(current_line).rstrip())
    if current_page:
        pages.append(current_page)

    return pages


def center_line(line, max_width=MAX_CHARS_PER_LINE):
    """
    Center a line by adding spaces (as done in the second part of display_dialog_text).
    This is only done for lines that are shorter than max_width - 2.
    """
    line_len = len(line)
    if line_len < max_width - 1:
        padding = (max_width - line_len) // 2
        return ' ' * padding + line
    return line


def display_text_example(text_bytes):
    """
    Example of how text is displayed in the game.
    """
    pages = word_wrap_text(text_bytes)

    print("Text wrapped into {} page(s):\n".format(len(pages)))

    for page_num, page in enumerate(pages, 1):
        print(f"Page {page_num}:")
        print("-" * 50)
        for line_num, line in enumerate(page, 1):
            # The game centers shorter lines
            if len(line) < MAX_CHARS_PER_LINE - 2:
                line = center_line(line)
            print(f"Line {line_num}: {line}")
        print()


# Example: The text from room 0, last hotspot
# "¡ Ahh ! Noches de la gran ciudad... Como dijo el poeta"
example_text = bytes([
    0xAD, 0x20,  # ¡ (inverted exclamation) + space
    0x41, 0x68, 0x68, 0x20, 0x21, 0x20, 0x4E, 0x6F, 0x63, 0x68, 0x65, 0x73, 0x20, 0x64, 0x65, 0x20,
    0x6C, 0x61, 0x20, 0x67, 0x72, 0x61, 0x6E, 0x20, 0x63, 0x69, 0x75, 0x64, 0x61, 0x64, 0x2E, 0x2E,
    0x2E, 0x20, 0x43, 0x6F, 0x6D, 0x6F, 0x20, 0x64, 0x69, 0x6A, 0x6F, 0x20, 0x65, 0x6C, 0x20, 0x70,
    0x6F, 0x65, 0x74, 0x61, 0xFD  # 0xFD = end marker
])


if __name__ == "__main__":
    print("=" * 70)
    print("Alfred Pelrock - Text Display Algorithm")
    print("=" * 70)
    print()
    print("Algorithm constants:")
    print(f"  MAX_CHARS_PER_LINE = {MAX_CHARS_PER_LINE}")
    print(f"  MAX_LINES = {MAX_LINES}")
    print()
    print("Word wrapping strategy:")
    print("  1. Process text word by word")
    print("  2. Words are defined by spaces or control characters")
    print("  3. If word fits on current line (chars_remaining >= word_length):")
    print("     - Add word to current line")
    print("     - Decrease chars_remaining by word_length")
    print("  4. If word doesn't fit on current line:")
    print("     - Move to next line (reset chars_remaining to 47)")
    print("     - Increment line counter")
    print("  5. After 4 lines, create new page")
    print("  6. Shorter lines may be centered")
    print()
    print("=" * 70)
    print()

    # Decode example text
    text_str = example_text[:-1].decode('latin-1')  # Exclude end marker
    print(f"Example text: {text_str}")
    print()

    display_text_example(example_text)

    print()
    print("The actual output in the game:")
    print("Line 1: ¡ Ahh ! Noches de la gran ciudad... Como dijo")
    print("Line 2: el poeta.")
