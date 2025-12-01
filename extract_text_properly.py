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

# Look for common response patterns from pattern_results.txt
# These typically don't have the fd 00 08 02 marker
responses = []

# Scan for Spanish phrases
spanish_patterns = [
    b"No funciona",
    b"No puedo",
    b"Est\xe1 cerrado",
    b"No hay nada",
    b"No tengo",
    b"Cerrado",
    b"Abierto", 
    b"Vac\xedo",
    b"No veo nada"
]

for pattern in spanish_patterns:
    i = 0
    while i < len(data):
        idx = data.find(pattern, i)
        if idx == -1:
            break
        
        # Extract full sentence (up to null or newline)
        end = idx
        for j in range(idx, min(idx + 100, len(data))):
            if data[j] in (0, 0x0a, 0xfd):
                end = j
                break
        else:
            end = idx + 100
        
        try:
            text = data[idx:end].decode('latin-1').strip()
            if text and text not in [r[1] for r in responses]:
                responses.append((idx, text))
        except:
            pass
        
        i = idx + len(pattern)

# Sort and display
responses.sort(key=lambda x: x[0])
for idx, text in responses[:50]:  # Limit to first 50
    print(f"0x{idx:05x}: {text}")

# Save responses
with open('character_responses.txt', 'w', encoding='utf-8') as out:
    out.write("CHARACTER DIALOGUE RESPONSES FROM JUEGO.EXE\n")
    out.write("=" * 60 + "\n\n")
    
    for idx, text in responses:
        out.write(f"0x{idx:05x}: {text}\n")

print(f"\n✓ Saved to: character_responses.txt")
print(f"Total responses found: {len(responses)}")
