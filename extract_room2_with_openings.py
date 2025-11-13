#!/usr/bin/env python3
"""
Complete Room 2 Conversation Extractor - WITH OPENING LINES
Handles:
- FD FE pattern (initial greeting with index 0x0A)
- FD patterns (normal conversation flow)
- F7 patterns (return greeting and other entry points)
- F4 FB patterns (alternative player choices)

Key insight: The "speaker_id" field is actually a "choice_group_id".
Lines with the same choice_group_id are alternative responses at the same decision point.
"""

CONV_START = 0xB21DD  # Start BEFORE to catch FD FE opening
CONV_END = 0xB3078

data = open('files/ALFRED.1', 'rb').read()

conversations = []
i = CONV_START

print("Scanning Room 2 conversation data (including opening lines)...")
print("=" * 80)

while i < CONV_END:
    byte = data[i]

    # FD = line separator, can be followed by FE or control codes directly
    if byte == 0xFD:
        # Check what comes after FD
        if i + 1 < CONV_END:
            next_byte = data[i + 1]

            # FD FE pattern - opening greeting
            if next_byte == 0xFE:
                if i + 7 < CONV_END:
                    unknown = data[i + 2]  # Always 01?
                    control = data[i + 3]
                    speaker_id = data[i + 4]
                    marker = data[i + 5]
                    sep = data[i + 6]
                    index = data[i + 7]
                    term = data[i + 8]

                    if marker == 0x08 and term == 0x00:
                        speaker = "ALFRED" if sep == 0x0D else "NPC"

                        print(f"Offset 0x{i:08X}: FD FE {unknown:02X} {control:02X} {speaker_id:02X} 08 {sep:02X} {index:02X} 00 -> Idx 0x{index:02X} ({speaker}) [OPENING LINE]")

                        # Text starts after the 00 terminator
                        text_start = i + 9
                        text_bytes = bytearray()
                        j = text_start

                        while j < CONV_END:
                            b = data[j]
                            if b == 0xFD or (b >= 0xF0 and b != 0xF8):
                                break
                            if b < 0x20:
                                j += 1
                                continue
                            text_bytes.append(b)
                            j += 1

                        text = text_bytes.decode('latin-1', errors='replace').strip()
                        conversations.append({
                            'index': index,
                            'speaker': speaker,
                            'text': text,
                            'embedded': False,
                            'entry_point': 'initial',  # First conversation
                            'offset': i
                        })
                        i = j - 1
                i += 1
                continue

            # Normal FD pattern
            if i + 6 < CONV_END:
                control = data[i + 1]
                choice_group_id = data[i + 2]  # Links alternatives with F4 FB lines
                marker = data[i + 3]
                sep = data[i + 4]
                index = data[i + 5]
                term = data[i + 6]

                if marker == 0x08 and term == 0x00:
                    speaker = "ALFRED" if sep == 0x0D else "NPC"

                    print(f"Offset 0x{i:08X}: FD {control:02X} {choice_group_id:02X} 08 {sep:02X} {index:02X} 00 -> Idx 0x{index:02X} ({speaker}) [group:0x{choice_group_id:02X}]")

                    # Extract text
                    text_start = i + 7
                    text_bytes = bytearray()
                    j = text_start

                    has_embedded = False

                    while j < CONV_END:
                        b = data[j]

                        # Check for F8 embedding
                        if b == 0xF8 and j + 8 < CONV_END:
                            pot_ctrl = data[j + 3]
                            if pot_ctrl in [0xFB, 0xFC, 0xF1]:
                                emb_mark = data[j + 5]
                                emb_sep = data[j + 6]
                                emb_idx = data[j + 7]
                                emb_term = data[j + 8]

                                if emb_mark == 0x08 and emb_term == 0x00:
                                    # Save main line
                                    main_text = text_bytes.decode('latin-1', errors='replace').strip()
                                    conversations.append({
                                        'index': index,
                                        'speaker': speaker,
                                        'text': main_text,
                                        'embedded': False,
                                        'choice_group_id': choice_group_id,
                                        'entry_point': 'normal',
                                        'offset': i
                                    })

                                    # Extract embedded
                                    emb_speaker = "ALFRED" if emb_sep == 0x0D else "NPC"
                                    emb_text_start = j + 9
                                    emb_text_bytes = bytearray()
                                    k = emb_text_start

                                    while k < CONV_END:
                                        eb = data[k]
                                        if eb == 0xFD or eb == 0xFE or eb < 0x20 or eb >= 0xF0:
                                            break
                                        emb_text_bytes.append(eb)
                                        k += 1

                                    emb_text = emb_text_bytes.decode('latin-1', errors='replace').strip()

                                    # F8 structure: F8 [XX] [XX] [control] [choice_group_id] 08 [sep] [idx] 00
                                    # So choice_group_id is at position +4 from F8
                                    emb_choice_gid = pot_ctrl  # Wait, this is wrong position
                                    # Actually: F8 is at j, so structure is:
                                    # j+0: F8
                                    # j+1: XX
                                    # j+2: XX
                                    # j+3: control (pot_ctrl)
                                    # j+4: choice_group_id (we need to read this!)
                                    if j + 4 < CONV_END:
                                        emb_choice_gid = data[j + 4]
                                    else:
                                        emb_choice_gid = None

                                    conversations.append({
                                        'index': emb_idx,
                                        'speaker': emb_speaker,
                                        'text': emb_text,
                                        'embedded': True,
                                        'choice_group_id': emb_choice_gid,
                                        'entry_point': 'normal',
                                        'parent': index,
                                        'offset': j
                                    })

                                    print(f"  → Embedded line 0x{emb_idx:02X} ({emb_speaker})")

                                    has_embedded = True
                                    i = k - 1
                                    break

                        # Stop on control codes
                        if b == 0xFD or b == 0xFE or (b >= 0xF0 and b != 0xF8):
                            break
                        if b < 0x20:
                            j += 1
                            continue

                        text_bytes.append(b)
                        j += 1

                    if not has_embedded:
                        text = text_bytes.decode('latin-1', errors='replace').strip()
                        conversations.append({
                            'index': index,
                            'speaker': speaker,
                            'text': text,
                            'embedded': False,
                            'choice_group_id': choice_group_id,
                            'entry_point': 'normal',
                            'offset': i
                        })
                        i = j - 1

    # F4 FB = alternative player choice (same choice_group_id as another line)
    elif byte == 0xF4:
        if i + 1 < CONV_END and data[i + 1] == 0xFB:
            if i + 6 < CONV_END:
                choice_group_id = data[i + 2]  # This links alternatives together!
                marker = data[i + 3]
                sep = data[i + 4]
                index = data[i + 5]
                term = data[i + 6]

                if marker == 0x08 and term == 0x00:
                    speaker = "ALFRED" if sep == 0x0D else "NPC"

                    print(f"Offset 0x{i:08X}: F4 FB {choice_group_id:02X} 08 {sep:02X} {index:02X} 00 -> Idx 0x{index:02X} ({speaker}) [ALT CHOICE group:0x{choice_group_id:02X}]")

                    # Extract text
                    text_start = i + 7
                    text_bytes = bytearray()
                    j = text_start

                    while j < CONV_END:
                        b = data[j]
                        if b == 0xFD or (b >= 0xF0 and b != 0xF8):
                            break
                        if b < 0x20:
                            j += 1
                            continue
                        text_bytes.append(b)
                        j += 1

                    text = text_bytes.decode('latin-1', errors='replace').strip()
                    conversations.append({
                        'index': index,
                        'speaker': speaker,
                        'text': text,
                        'embedded': False,
                        'alternative_choice': True,  # Alternative player response
                        'choice_group_id': choice_group_id,  # Links to other choices
                        'entry_point': 'normal',
                        'offset': i
                    })
                    i = j - 1

        # Also check for F4 F1 pattern (similar alternative choice but with F1 control)
        elif i + 1 < CONV_END and data[i + 1] == 0xF1:
            if i + 6 < CONV_END:
                choice_group_id = data[i + 2]  # Same position as F4 FB
                marker = data[i + 3]
                sep = data[i + 4]
                index = data[i + 5]
                term = data[i + 6]

                if marker == 0x08 and term == 0x00:
                    speaker = "ALFRED" if sep == 0x0D else "NPC"

                    print(f"Offset 0x{i:08X}: F4 F1 {choice_group_id:02X} 08 {sep:02X} {index:02X} 00 -> Idx 0x{index:02X} ({speaker}) [ALT CHOICE group:0x{choice_group_id:02X}]")

                    # Extract text
                    text_start = i + 7
                    text_bytes = bytearray()
                    j = text_start

                    while j < CONV_END:
                        b = data[j]
                        if b == 0xFD or (b >= 0xF0 and b != 0xF8):
                            break
                        if b < 0x20:
                            j += 1
                            continue
                        text_bytes.append(b)
                        j += 1

                    text = text_bytes.decode('latin-1', errors='replace').strip()
                    conversations.append({
                        'index': index,
                        'speaker': speaker,
                        'text': text,
                        'embedded': False,
                        'alternative_choice': True,  # Alternative player response
                        'choice_group_id': choice_group_id,  # Links to other choices
                        'entry_point': 'normal',
                        'offset': i
                    })
                    i = j - 1

    # F7 = alternate entry point marker (like return greeting)
    elif byte == 0xF7:
        if i + 6 < CONV_END:
            control = data[i + 1]
            speaker_id = data[i + 2]
            marker = data[i + 3]
            sep = data[i + 4]
            index = data[i + 5]
            term = data[i + 6]

            if marker == 0x08 and term == 0x00:
                speaker = "ALFRED" if sep == 0x0D else "NPC"

                print(f"Offset 0x{i:08X}: F7 {control:02X} {speaker_id:02X} 08 {sep:02X} {index:02X} 00 -> Idx 0x{index:02X} ({speaker}) [RETURN ENTRY]")

                # Extract text
                text_start = i + 7
                text_bytes = bytearray()
                j = text_start

                while j < CONV_END:
                    b = data[j]
                    if b == 0xFD or b == 0xF7 or (b >= 0xF0 and b != 0xF8):
                        break
                    if b < 0x20:
                        j += 1
                        continue
                    text_bytes.append(b)
                    j += 1

                text = text_bytes.decode('latin-1', errors='replace').strip()
                conversations.append({
                    'index': index,
                    'speaker': speaker,
                    'text': text,
                    'embedded': False,
                    'entry_point': 'return',  # Return conversation
                    'offset': i
                })
                i = j - 1

    i += 1

print("=" * 80)
print()

# Sort by index
conversations.sort(key=lambda x: x['index'])

print(f"Total lines extracted: {len(conversations)}")
print()

# Show all lines
print("=" * 80)
print("ALL CONVERSATION LINES (sorted by index):")
print("=" * 80)

for i, conv in enumerate(conversations):
    idx = conv['index']
    speaker = conv['speaker']
    text = conv['text'][:70]
    entry = conv.get('entry_point', 'normal')
    is_emb = conv.get('embedded', False)
    is_alt = conv.get('alternative_choice', False)
    choice_gid = conv.get('choice_group_id', None)

    flags = []
    if entry == 'initial':
        flags.append("INITIAL GREETING")
    elif entry == 'return':
        flags.append("RETURN GREETING")
    if is_emb:
        flags.append("EMBEDDED")
        # For embedded lines, also show their choice group
        if choice_gid is not None:
            flags.append(f"grp:0x{choice_gid:02X}")
    elif is_alt and choice_gid is not None:
        flags.append(f"ALT CHOICE grp:0x{choice_gid:02X}")
    elif choice_gid is not None:
        flags.append(f"grp:0x{choice_gid:02X}")

    flag_str = f" [{', '.join(flags)}]" if flags else ""

    print(f"[{i:2d}] Idx:0x{idx:02X} | {speaker:6s} | {text}{flag_str}")

print()
print("=" * 80)
print(f"Statistics:")
print(f"  Total: {len(conversations)}")
print(f"  NPC: {len([c for c in conversations if c['speaker'] == 'NPC'])}")
print(f"  ALFRED: {len([c for c in conversations if c['speaker'] == 'ALFRED'])}")
print(f"  Initial greeting: {len([c for c in conversations if c.get('entry_point') == 'initial'])}")
print(f"  Return greeting: {len([c for c in conversations if c.get('entry_point') == 'return'])}")
print(f"  Embedded (F8): {len([c for c in conversations if c.get('embedded')])}")
print(f"  Alternative choices (F4 FB): {len([c for c in conversations if c.get('alternative_choice')])}")

# Show choice groups
print()
print("Choice Groups (lines with same choice_group_id are alternatives):")
from collections import defaultdict
choice_groups = defaultdict(list)
for c in conversations:
    gid = c.get('choice_group_id')
    if gid is not None:
        choice_groups[gid].append(c)

for gid in sorted(choice_groups.keys()):
    group = choice_groups[gid]
    if len(group) > 1:  # Only show groups with alternatives
        print(f"  Group 0x{gid:02X}: {len(group)} alternatives")
        for c in group:
            is_alt = " [F4 FB]" if c.get('alternative_choice') else " [FD]"
            print(f"    - Idx 0x{c['index']:02X}{is_alt}: {c['text'][:50]}")

print("=" * 80)
