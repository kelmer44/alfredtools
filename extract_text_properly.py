#!/usr/bin/env python3
"""Extract room names from JUEGO.EXE with proper structure"""

# Read JUEGO.EXE
with open('files/JUEGO.EXE', 'rb') as f:
    data = f.read()

print("=== EXTRACTING ROOM NAMES FROM JUEGO.EXE ===\n")

# Room names have pattern: fd 00 08 02 + name (space-padded)
marker = b'\xfd\x00\x08\x02'

rooms = []
i = 0
while i < len(data):
    idx = data.find(marker, i)
    if idx == -1:
        break

    # Extract room name after marker
    name_start = idx + 4
    # Find next marker or read up to 30 chars
    name_end = name_start
    for j in range(name_start, min(name_start + 30, len(data))):
        if data[j:j+4] == marker or data[j] == 0:
            name_end = j
            break
    else:
        name_end = name_start + 30

    try:
        room_name = data[name_start:name_end].decode('latin-1').strip()
        if room_name and len(room_name) > 2:  # Skip very short matches
            rooms.append((idx, room_name))
            print(f"0x{idx:05x}: {room_name}")
    except:
        pass

    i = idx + 4

print(f"\nTotal room names found: {len(rooms)}")

# Save to file
with open('room_names_list.txt', 'w', encoding='utf-8') as out:
    out.write("ROOM NAMES FROM JUEGO.EXE\n")
    out.write("=" * 60 + "\n")
    out.write(f"Total rooms: {len(rooms)}\n\n")

    for idx, name in rooms:
        out.write(f"0x{idx:05x}: {name}\n")

print(f"\n✓ Saved to: room_names_list.txt")

# Now extract standard character responses
print("\n=== CHARACTER DIALOGUE RESPONSES ===\n")

# Extract all dialogue responses by scanning for readable text strings
# Character responses are typically found in sections without the fd 00 08 02 marker
responses = []

# Scan specific ranges where dialogue is stored
dialogue_ranges = [
    (0x44000, 0x48000),  # Main dialogue section
]

for start_range, end_range in dialogue_ranges:
    i = start_range
    while i < end_range:
        # Look for start of printable text (ASCII or Spanish chars)
        if 0x20 <= data[i] < 0x7f or data[i] in (0xf3, 0xe1, 0xe9, 0xed, 0xf1, 0xfa, 0xfc):
            text_start = i
            j = i
            # Continue while we have printable characters
            while j < end_range and (0x20 <= data[j] < 0x7f or data[j] in (0xf3, 0xe1, 0xe9, 0xed, 0xf1, 0xfa, 0xfc, 0xfd)):
                j += 1

            # If string is substantial (at least 10 chars)
            if j - i >= 10:
                try:
                    text = data[i:j].decode('latin-1').strip()
                    # Filter for dialogue-like content (contains common Spanish words)
                    if any(word in text.lower() for word in ['no ', 'se ', 'esta', 'hay', 'puedo', 'tengo', 'el ', 'la ', 'que ', 'pero', 'si ', 'ya ']):
                        # Remove control characters like ý (0xfd)
                        text = text.replace('ý', '').replace('xx', '').strip()
                        if len(text) >= 10 and text not in [r[1] for r in responses]:
                            responses.append((i, text))
                except:
                    pass
            i = j
        i += 1

# Sort and display
responses.sort(key=lambda x: x[0])
for idx, text in responses:
    # Clean up display
    display_text = text[:100] + ('...' if len(text) > 100 else '')
    print(f"0x{idx:05x}: {display_text}")

# Save responses
with open('character_responses.txt', 'w', encoding='utf-8') as out:
    out.write("CHARACTER DIALOGUE RESPONSES FROM JUEGO.EXE\n")
    out.write("=" * 60 + "\n\n")

    for idx, text in responses:
        out.write(f"0x{idx:05x}: {text}\n")

print(f"\n✓ Saved to: character_responses.txt")
print(f"Total responses found: {len(responses)}")
