#!/usr/bin/env python3
"""Extract complete book database from ALFRED.7 with correct parsing"""

with open('files/ALFRED.7', 'rb') as f:
    data = f.read()

print("=== ALFRED.7 Book Database ===\n")

# The book table is delimited by 0x01 bytes
# Let's find all entries in a wider range

# First, find the start of the book region by looking for the header pattern
# Look for first 0x01 followed by text

# Search from offset 0x33000
start_search = 0x33000
end_search = 0x37000

region = data[start_search:end_search]

# Find all 0x01 delimiters
delimiters = []
for i, b in enumerate(region):
    if b == 0x01:
        delimiters.append(i)

print(f"Found {len(delimiters)} delimiter bytes (0x01) in region")
print(f"First 10 delimiter positions: {[hex(start_search + d) for d in delimiters[:10]]}")

# Extract entries between delimiters
books = []

for i in range(len(delimiters)):
    start = delimiters[i] + 1  # After the 0x01
    if i + 1 < len(delimiters):
        end = delimiters[i + 1]
    else:
        end = min(start + 200, len(region))

    entry_bytes = region[start:end]

    # Parse the entry - replace line break marker 0xC8 with space
    entry_str = entry_bytes.decode('latin-1', errors='replace')
    entry_str = entry_str.replace('\xc8', ' ')  # È is used as line break in titles

    # Split into title, author, genre, shelf
    # Title is ~55 chars, Author is ~30 chars, Genre is ~22 chars, then shelf letter

    # Strip trailing spaces to find fields
    entry_str = entry_str.rstrip()

    # The last 1-2 chars might be shelf code
    # Try to parse by finding long runs of spaces
    parts = []
    current = ""
    space_count = 0

    for c in entry_str:
        if c == ' ':
            space_count += 1
            current += c
        else:
            if space_count >= 3:  # Field separator
                parts.append(current.rstrip())
                current = c
            else:
                current += c
            space_count = 0

    if current.strip():
        parts.append(current.strip())

    # Clean up parts
    parts = [p.strip() for p in parts if p.strip()]

    if len(parts) >= 3:
        title = parts[0]
        author = parts[1] if len(parts) > 1 else ""
        genre_shelf = parts[2] if len(parts) > 2 else ""

        # Extract shelf letter from end of genre (if present)
        shelf = ""
        genre = genre_shelf
        if genre_shelf and len(genre_shelf) > 2:
            # Check if last char(s) are the shelf
            if genre_shelf[-1].isupper() and genre_shelf[-2] == ' ':
                shelf = genre_shelf[-1]
                genre = genre_shelf[:-1].strip()
            elif len(genre_shelf) >= 2 and genre_shelf[-2:].strip().isupper():
                shelf = genre_shelf[-1]
                genre = genre_shelf[:-2].strip()

        # Skip invalid entries
        if len(title) > 5 and not title.startswith('\xff'):
            books.append({
                'title': title,
                'author': author,
                'genre': genre,
                'shelf': shelf,
                'raw_offset': start_search + start
            })

print(f"\n=== Found {len(books)} valid book entries ===\n")

print(f"{'#':>3} {'Shelf':<6} {'Title':<50} {'Author':<30} {'Genre'}")
print("-" * 130)

for i, book in enumerate(books, 1):
    title = book['title'][:48]
    author = book['author'][:28]
    genre = book['genre'][:20]
    shelf = book['shelf'] or "?"
    print(f"{i:>3} {shelf:<6} {title:<50} {author:<30} {genre}")

# Also check where the first book actually starts
print(f"\n\n=== Table Boundaries ===")
if books:
    print(f"First book at offset: 0x{books[0]['raw_offset']:X}")
    print(f"Last book at offset: 0x{books[-1]['raw_offset']:X}")

# Generate ScummVM structure
print("\n\n=== ScummVM Book Data ===\n")

print("// Book database from ALFRED.7")
print("// Delimiter: 0x01 byte between entries")
print("// Format: Title (55) | Author (30) | Genre (22) | Shelf (1)")
print()
print("static const BookEntry kBookDatabase[] = {")
for book in books:
    title = book['title'].replace('"', '\\"').replace('\n', ' ')
    author = book['author'].replace('"', '\\"')
    genre = book['genre'].replace('"', '\\"')
    shelf = book['shelf'] or '?'
    print(f'    {{"{title}", "{author}", "{genre}", \'{shelf}\'}},')
print("};")
print(f"\nstatic const int kBookCount = {len(books)};")
