#!/usr/bin/env python3
"""
Alfred Pelrock - Text Display Algorithm
Decompiled from the game executable at address 0x0001a298 (display_dialog_text)

This algorithm handles word wrapping and text display for dialog and hotspot descriptions.
The text is rendered in pink (color 13 in palette) when examining hotspots.
"""

# Constants found in the decompiled code
MAX_CHARS_PER_LINE = 0x2F  # 47 characters
MAX_LINES = 5  # Maximum number of lines per page (0-indexed check against 4)

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
    A word includes: non-space characters + ALL trailing spaces

    Returns:
        word_length: Number of characters in the word (including trailing spaces)
        is_end: Whether this is the end of the text
    """
    word_length = 0
    pos = position
    is_end = False

    # Count non-space characters until we hit a space or end marker
    while pos < len(text):
        char = text[pos]

        if char == CHAR_SPACE or is_end_marker(char):
            break

        word_length += 1
        pos += 1

    # Check if we hit an end marker
    if pos < len(text) and is_end_marker(text[pos]):
        is_end = True

    # Count ALL trailing spaces as part of this word
    if pos < len(text) and not is_end:
        if text[pos] == CHAR_END_MARKER_3:  # 0xF8 (-8) special case
            word_length += 3
        else:
            # Count all consecutive spaces
            while pos < len(text) and text[pos] == CHAR_SPACE:
                word_length += 1
                pos += 1

    return word_length, is_end


def word_wrap_text(text, max_chars_per_line=MAX_CHARS_PER_LINE, max_lines=MAX_LINES):
    """
    Wrap text using the Alfred Pelrock algorithm.

    The algorithm:
    1. Process text word by word
    2. A word = non-space chars + ALL trailing spaces
    3. If word fits on current line (chars_remaining >= word_length), add it
    4. If adding the word would exceed the line, wrap to next line
    5. Special case: If word exactly fills the line, trailing spaces move to next line
    6. Maximum 5 lines per page

    Args:
        text: Input text as bytes or string
        max_chars_per_line: Maximum characters per line (default 47)
        max_lines: Maximum lines per page (default 5)

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

        # Extract the word (including trailing spaces)
        word = text[position:position + word_length].decode('latin-1', errors='replace')

        # Key decision: if word_length > chars_remaining, wrap to next line
        if word_length > chars_remaining:
            # Word doesn't fit - move to next line

            # Save current line (strip trailing spaces)
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

        # Special case: If line is exactly full (0 remaining),
        # move trailing spaces to next line
        if chars_remaining == 0 and not is_end:
            # Strip trailing spaces from current line
            line_text = ''.join(current_line).rstrip()
            trailing_spaces = len(''.join(current_line)) - len(line_text)

            if trailing_spaces > 0:
                # Save line without trailing spaces
                current_page.append(line_text)

                # Start new line with the trailing spaces
                current_line = [' ' * trailing_spaces]
                chars_remaining = max_chars_per_line - trailing_spaces
                current_line_num += 1

                # Check if we need a new page
                if current_line_num >= max_lines:
                    pages.append(current_page)
                    current_page = []
                    current_line_num = 0

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


def format_text(text_input):
    """
    Format text using the Alfred Pelrock algorithm.

    Args:
        text_input: String or bytes to format

    Returns:
        Formatted text as a string
    """
    if isinstance(text_input, str):
        # Convert to bytes, add end marker
        text_bytes = text_input.encode('latin-1') + bytes([CHAR_END_MARKER_1])
    else:
        text_bytes = text_input

    pages = word_wrap_text(text_bytes)

    output_lines = []
    for page_num, page in enumerate(pages, 1):
        if len(pages) > 1:
            output_lines.append(f"=== Page {page_num} ===")
        for line in page:
            output_lines.append(line)
        if page_num < len(pages):
            output_lines.append("")  # Blank line between pages

    return '\n'.join(output_lines)


if __name__ == "__main__":
    import sys

    # Check if text was provided as argument
    if len(sys.argv) > 1:
        # Join all arguments as input text
        input_text = ' '.join(sys.argv[1:])

        print("=" * 70)
        print("Alfred Pelrock - Text Display Algorithm")
        print("=" * 70)
        print()
        print(f"Input text ({len(input_text)} chars):")
        print(f'  "{input_text}"')
        print()
        print("Wrapped output:")
        print("-" * 70)
        print(format_text(input_text))
        print("-" * 70)
        print()

        # Show stats
        pages = word_wrap_text(input_text.encode('latin-1') + bytes([CHAR_END_MARKER_1]))
        total_lines = sum(len(page) for page in pages)
        print(f"Statistics:")
        print(f"  Pages: {len(pages)}")
        print(f"  Total lines: {total_lines}")
        print(f"  Max chars per line: {MAX_CHARS_PER_LINE}")

    else:
        # Show help and example
        print("=" * 70)
        print("Alfred Pelrock - Text Display Algorithm")
        print("=" * 70)
        print()
        print("Usage:")
        print("  python text_display_algorithm.py <text>")
        print()
        print("Example:")
        print('  python text_display_algorithm.py "¡ Ahh ! Noches de la gran ciudad..."')
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
        print("Running built-in example...")
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
