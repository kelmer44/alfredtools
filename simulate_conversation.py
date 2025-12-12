#!/usr/bin/env python3
"""
Conversation Simulator for the Game

This script simulates the conversation system, allowing you to:
- View dialogue lines (press Enter to advance)
- Make choices when presented (type choice number)
- Follow the conversation flow as it appears in the game

Usage:
    python simulate_conversation.py <alfred1_file> <room_number>
    python simulate_conversation.py ALFRED.1 2

Or provide hex data directly:
    python simulate_conversation.py --hex <hex_data>
"""

import sys
import struct
from typing import List, Tuple, Optional
from dataclasses import dataclass

# Control bytes (matching the game's conversation system)
CTRL_SPEAKER_ID = 0x08
CTRL_END_TEXT = 0xFD
CTRL_TEXT_TERMINATOR = 0xFC
CTRL_DIALOGUE_MARKER = 0xFB
CTRL_DISABLED_CHOICE = 0xFA
CTRL_PAGE_BREAK = 0xF9
CTRL_ACTION_TRIGGER = 0xF8
CTRL_END_BRANCH = 0xF7
CTRL_LINE_CONTINUE = 0xF6
CTRL_ALT_END_MARKER_1 = 0xF5
CTRL_END_CONVERSATION = 0xF4
CTRL_DIALOGUE_MARKER_2 = 0xF1
CTRL_GO_BACK = 0xF0
CTRL_ALT_END_MARKER_2 = 0xEB
CTRL_ALT_END_MARKER_3 = 0xFE

# Character ID
CHAR_ALFRED_ID = 0x0D

# Spanish character mapping (custom encoding)
CHAR_MAP = {
    0x80: 'ñ',
    0x81: 'í',
    0x82: '¡',
    0x83: '¿',
    0x84: 'ú',
    0x7B: 'á',
    0x7C: 'é',
    0x7D: 'í',
    0x7E: 'ó',
    0x7F: 'ú',
}

@dataclass
class ChoiceOption:
    """Represents a conversation choice option"""
    index: int
    text: str
    is_disabled: bool = False
    data_offset: int = 0

@dataclass
class ConversationState:
    """Tracks the current state of the conversation"""
    data: bytes
    position: int = 0
    conversation_active: bool = True
    disabled_choices: set = None

    def __post_init__(self):
        if self.disabled_choices is None:
            self.disabled_choices = set()


class ConversationSimulator:
    """Simulates the game's conversation system"""

    def __init__(self, conversation_data: bytes):
        self.data = conversation_data
        self.position = 0
        self.disabled_choices = set()

    def decode_byte(self, byte: int) -> Optional[str]:
        """Decode a single byte to character, return None for control bytes"""
        if byte in CHAR_MAP:
            return CHAR_MAP[byte]
        elif 0x20 <= byte <= 0x7A:  # Printable ASCII range
            return chr(byte)
        else:
            return None

    def decode_text(self, data: bytes) -> str:
        """Decode text using the game's character encoding"""
        result = []
        for byte in data:
            char = self.decode_byte(byte)
            if char:
                result.append(char)
        return ''.join(result)

    def clean_text(self, text: str) -> str:
        """Clean control sequences from text (matching export_trees_correct.py)"""
        text = text.strip()

        # Remove leading single control characters
        if len(text) > 1 and text[0] in 'AH' and (text[1].isupper() or text[1] in '¿¡['):
            text = text[1:].lstrip()
        elif len(text) > 1 and text[0] in '#%\')!+,.-"*&$(/' :
            text = text[1:].lstrip()

        return text.strip()

    def read_text_segment(self, start_pos: int) -> Tuple[str, int, int]:
        """
        Read a text segment from the conversation data

        Returns: (text, speaker_id, end_position)
        """
        pos = start_pos
        speaker_id = None
        text_bytes = []

        # Skip control bytes at start
        while (pos < len(self.data) and
               self.data[pos] in (CTRL_ALT_END_MARKER_1, CTRL_ALT_END_MARKER_2,
                                 CTRL_ALT_END_MARKER_3, CTRL_TEXT_TERMINATOR,
                                 CTRL_GO_BACK)):
            pos += 1

        # Check for speaker ID
        if pos < len(self.data) and self.data[pos] == CTRL_SPEAKER_ID:
            pos += 1
            if pos < len(self.data):
                speaker_id = self.data[pos]
                pos += 1
            # No skip after speaker ID - text follows immediately

        # Check for dialogue marker (choice text)
        elif pos < len(self.data) and self.data[pos] in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2):
            pos += 1  # Skip marker

            # Skip choice index
            if pos < len(self.data):
                pos += 1

            # Skip 2 bytes after choice index (speaker marker bytes)
            if pos < len(self.data):
                pos += 1
            if pos < len(self.data):
                pos += 1

            # Choice text is always spoken by ALFRED
            speaker_id = CHAR_ALFRED_ID

        # Read text until control byte
        while pos < len(self.data):
            byte = self.data[pos]

            # End markers - stop reading text
            if byte in (CTRL_END_TEXT, CTRL_END_CONVERSATION, CTRL_ACTION_TRIGGER,
                       CTRL_END_BRANCH, CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2,
                       CTRL_TEXT_TERMINATOR, CTRL_ALT_END_MARKER_1, CTRL_ALT_END_MARKER_2,
                       CTRL_ALT_END_MARKER_3, CTRL_GO_BACK, CTRL_SPEAKER_ID):
                break

            if byte == CTRL_LINE_CONTINUE or byte == CTRL_PAGE_BREAK:
                text_bytes.append(ord('\n'))
                pos += 1
                continue

            # Regular text (filtering happens in decode_byte)
            text_bytes.append(byte)
            pos += 1

        text = self.decode_text(bytes(text_bytes))
        text = self.clean_text(text)
        return text, speaker_id, pos

    def find_speaker_name(self, speaker_id: Optional[int]) -> str:
        """Get speaker name from ID"""
        if speaker_id is None:
            return "???"
        if speaker_id == CHAR_ALFRED_ID:
            return "ALFRED"
        return f"NPC_{speaker_id:02X}"

    def parse_choices(self, start_pos: int) -> List[ChoiceOption]:
        """
        Parse conversation choices from current position
        
        Algorithm matches game code @ 0x00018690:
        - Finds first choice marker (0xFB or 0xF1)
        - Scans forward collecting markers with SAME index only
        - Stops at: end markers (0xF5, 0xF7, 0xFE) OR lower index
        - If count == 1: auto-dialogue, if count > 1: real choice menu
        """
        pos = start_pos
        choices = []
        first_choice_index = None
        choice_count = 0

        # Find first choice marker
        while pos < len(self.data):
            byte = self.data[pos]
            
            # Stop at end markers (matching game: 0xF5, 0xF7, 0xFE)
            if byte in (CTRL_ALT_END_MARKER_1, CTRL_END_BRANCH, CTRL_ALT_END_MARKER_3):
                break
                
            # Found first choice marker
            if byte in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2):
                if pos + 1 < len(self.data):
                    # Skip if disabled marker
                    if pos + 2 < len(self.data) and self.data[pos + 2] == CTRL_DISABLED_CHOICE:
                        pos += 1
                        continue
                        
                    first_choice_index = self.data[pos + 1]
                    is_disabled = pos in self.disabled_choices
                    text, speaker_id, end_pos = self.read_text_segment(pos + 2)
                    choices.append(ChoiceOption(
                        index=first_choice_index,
                        text=text.strip(),
                        is_disabled=is_disabled,
                        data_offset=pos
                    ))
                    choice_count = 1
                    pos += 2  # Skip marker + index
                    break
            pos += 1
        
        # Now scan for additional choices with SAME index (matching game logic)
        while pos < len(self.data):
            byte = self.data[pos]
            
            # Stop at end markers
            if byte in (CTRL_ALT_END_MARKER_1, CTRL_END_BRANCH, CTRL_ALT_END_MARKER_3):
                break
            
            # Found a dialogue marker
            if byte in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2):
                if pos + 1 < len(self.data):
                    # Skip if disabled marker
                    if pos + 2 < len(self.data) and self.data[pos + 2] == CTRL_DISABLED_CHOICE:
                        pos += 1
                        continue
                    
                    choice_index = self.data[pos + 1]
                    
                    # Stop if index is LESS than first (game behavior)
                    if choice_index < first_choice_index:
                        break
                    
                    # Only add if index EQUALS first
                    if choice_index == first_choice_index:
                        is_disabled = pos in self.disabled_choices
                        text, speaker_id, end_pos = self.read_text_segment(pos + 2)
                        choices.append(ChoiceOption(
                            index=choice_index,
                            text=text.strip(),
                            is_disabled=is_disabled,
                            data_offset=pos
                        ))
                        choice_count += 1
            
            pos += 1

        # Determine if real choice or auto-dialogue (matching game: if count == 1)
        if choices and choice_count == 1:
            # This is auto-dialogue, not a real choice
            # Return single "choice" but mark it differently
            choices[0].index = -1  # Special marker for auto-dialogue

        return choices

    def display_dialogue(self, text: str, speaker_id: Optional[int]):
        """Display a line of dialogue"""
        speaker = self.find_speaker_name(speaker_id)
        print(f"\n{speaker}:")
        print(f"  {text}")
        print("\n[Press Enter to continue...]")
        try:
            input()
        except EOFError:
            pass  # Handle EOF gracefully

    def display_choices(self, choices: List[ChoiceOption]) -> int:
        """
        Display choices and get user selection

        Returns: index of selected choice in the choices list
        """
        # Check if this is auto-dialogue
        if len(choices) == 1 and choices[0].index == -1:
            print(f"\n{self.find_speaker_name(CHAR_ALFRED_ID)}: (automatically)")
            print(f"  {choices[0].text}")
            print("\n[Press Enter to continue...]")
            try:
                input()
            except EOFError:
                pass  # Handle EOF gracefully
            return 0

        print("\n" + "="*60)
        print("CHOICES:")
        print("="*60)

        valid_choices = []
        for i, choice in enumerate(choices):
            if choice.is_disabled:
                print(f"  [{i+1}] [DISABLED] {choice.text}")
            else:
                print(f"  [{i+1}] {choice.text}")
                valid_choices.append(i)

        # Get user selection
        while True:
            try:
                selection = input(f"\nSelect choice (1-{len(choices)}): ").strip()
                if not selection:  # Handle empty input
                    print("Please enter a number")
                    continue

                choice_num = int(selection) - 1

                if choice_num < 0 or choice_num >= len(choices):
                    print(f"Invalid choice. Please enter 1-{len(choices)}")
                    continue

                if choices[choice_num].is_disabled:
                    print("That choice is disabled. Please select another.")
                    continue

                return choice_num

            except ValueError:
                print("Please enter a number")
            except (KeyboardInterrupt, EOFError):
                print("\n\nConversation interrupted.")
                sys.exit(0)

    def run_conversation(self):
        """Main conversation loop - simulates handle_conversation_tree()"""
        print("\n" + "="*60)
        print("CONVERSATION START")
        print("="*60)

        self.position = 0

        # Skip any junk at start until we find a speaker marker or choice marker
        while (self.position < len(self.data) and
               self.data[self.position] not in (CTRL_SPEAKER_ID, CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2)):
            self.position += 1

        # OUTER LOOP: Continue until conversation ends
        while self.position < len(self.data):
            # Skip control bytes that should be ignored
            while (self.position < len(self.data) and 
                   self.data[self.position] in (CTRL_ALT_END_MARKER_1, CTRL_ALT_END_MARKER_2, 
                                                CTRL_ALT_END_MARKER_3, CTRL_TEXT_TERMINATOR, 
                                                CTRL_GO_BACK)):
                self.position += 1
            
            if self.position >= len(self.data):
                break

            # 1. Read and display current dialogue
            text, speaker_id, end_pos = self.read_text_segment(self.position)

            # Skip spurious single character artifacts (A, H, etc.)
            if text.strip() and len(text.strip()) > 1:
                self.display_dialogue(text, speaker_id)

            # Move to end of text
            self.position = end_pos

            # 2. Check for end of conversation
            if self.position >= len(self.data):
                break

            control_byte = self.data[self.position]

            if control_byte == CTRL_END_CONVERSATION:
                print("\n[Conversation ended normally]")
                break

            # Move past control byte
            if control_byte in (CTRL_END_TEXT, CTRL_ACTION_TRIGGER):
                self.position += 1
                if control_byte == CTRL_ACTION_TRIGGER:
                    # Skip action parameters
                    self.position += 2

            # 3. Before parsing choices, check if we're at a choice marker
            # Skip control bytes to peek at next meaningful byte
            peek_pos = self.position
            while (peek_pos < len(self.data) and
                   self.data[peek_pos] in (CTRL_ALT_END_MARKER_1, CTRL_ALT_END_MARKER_2,
                                           CTRL_ALT_END_MARKER_3, CTRL_TEXT_TERMINATOR,
                                           CTRL_GO_BACK)):
                peek_pos += 1

            # If not at a choice marker, there's more dialogue to read - continue outer loop
            if peek_pos < len(self.data) and self.data[peek_pos] not in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2, CTRL_END_CONVERSATION):
                continue

            # 4. Parse choices
            choices = self.parse_choices(self.position)

            if not choices:
                # No choices found - end conversation
                print("\n[No more dialogue - conversation ended]")
                break

            # 4. Display choices and get selection
            selected_index = self.display_choices(choices)
            selected_choice = choices[selected_index]

            # 5. Mark choice as used (if not auto-dialogue)
            if selected_choice.index != -1:
                self.disabled_choices.add(selected_choice.data_offset)

            # 6. Move to the selected choice marker in the data
            search_pos = self.position
            choice_count = 0

            while search_pos < len(self.data):
                byte = self.data[search_pos]

                if byte in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2):
                    if search_pos + 1 < len(self.data):
                        idx = self.data[search_pos + 1]
                        # For auto-dialogue (index==-1), match first occurrence
                        # For manual choices, match by index and count
                        if selected_choice.index == -1 or idx == selected_choice.index:
                            if choice_count == selected_index:
                                # Found it - move to the choice marker
                                self.position = search_pos
                                break
                            choice_count += 1

                search_pos += 1

            # Read and display the selected choice as dialogue
            text, speaker_id, end_pos = self.read_text_segment(self.position)
            if text.strip() and len(text.strip()) > 1:
                self.display_dialogue(text, speaker_id)

            self.position = end_pos

            # Skip past end marker
            if self.position < len(self.data):
                control_byte = self.data[self.position]
                if control_byte == CTRL_END_TEXT:
                    self.position += 1

            # 7. After displaying the choice (auto or manual), continue reading dialogue
            # This reads NPC responses and any other dialogue that follows
            while self.position < len(self.data):
                # Skip ignorable control bytes
                while (self.position < len(self.data) and 
                       self.data[self.position] in (CTRL_ALT_END_MARKER_1, CTRL_ALT_END_MARKER_2, 
                                                    CTRL_ALT_END_MARKER_3, CTRL_TEXT_TERMINATOR, 
                                                    CTRL_GO_BACK)):
                    self.position += 1
                
                if self.position >= len(self.data):
                    break
                
                # Check if we've hit a choice marker or end - if so, stop and let outer loop handle it
                next_byte = self.data[self.position]
                if next_byte in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2, CTRL_END_CONVERSATION):
                    break
                
                # Read and display the next dialogue segment
                text, speaker_id, end_pos = self.read_text_segment(self.position)
                if text.strip() and len(text.strip()) > 1:
                    self.display_dialogue(text, speaker_id)
                
                self.position = end_pos

                # Skip end marker
                if self.position < len(self.data) and self.data[self.position] == CTRL_END_TEXT:
                    self.position += 1

        print("\n" + "="*60)
        print("CONVERSATION ENDED")
        print("="*60)


def read_room_pair(data: bytes, room_num: int, pair_num: int) -> Optional[bytes]:
    """Read a specific pair from a room in ALFRED.1"""
    room_offset = room_num * 104
    pair_offset_pos = room_offset + (pair_num * 8)

    if pair_offset_pos + 8 > len(data):
        return None

    offset = struct.unpack('<I', data[pair_offset_pos:pair_offset_pos+4])[0]
    size = struct.unpack('<I', data[pair_offset_pos+4:pair_offset_pos+8])[0]

    if size == 0 or offset >= len(data):
        return None

    return data[offset:offset+size]


def extract_conversation_from_room(alfred1_data: bytes, room_num: int) -> Optional[bytes]:
    """
    Extract conversation data from a specific room

    Conversations are in resource pair 12.
    They start after sprite/hotspot descriptions.
    Description count = sprite_count + hotspot_count
    """
    # Get pair 12 (conversations)
    pair12 = read_room_pair(alfred1_data, room_num, 12)
    if pair12 is None:
        return None

    # Get pair 10 to read sprite/hotspot counts
    pair10 = read_room_pair(alfred1_data, room_num, 10)
    if pair10 is None:
        # If no pair 10, try to find conversation start heuristically
        return extract_conversations_heuristic(pair12)

    # Read sprite count (offset 0x05 in pair 10, subtract 2 for sprite table)
    if len(pair10) < 6:
        return extract_conversations_heuristic(pair12)

    sprite_count = pair10[5] - 2 if pair10[5] >= 2 else 0

    # Read hotspot count (offset 0x47A in pair 10)
    hotspot_count = 0
    if len(pair10) > 0x47A:
        hotspot_count = pair10[0x47A]

    description_count = sprite_count + hotspot_count

    # Skip descriptions to find conversation start
    # Each description: 0xFF + 4 bytes + text + 0xFD
    pos = 0
    descriptions_found = 0

    while pos < len(pair12) and descriptions_found < description_count:
        if pair12[pos] == 0xFF:
            pos += 5  # Skip 0xFF + 4 header bytes
            # Skip text until 0xFD
            while pos < len(pair12) and pair12[pos] != 0xFD:
                pos += 1
            if pos < len(pair12):
                pos += 1  # Skip 0xFD
                descriptions_found += 1
        else:
            pos += 1

    # Conversation data starts after descriptions
    if pos >= len(pair12):
        return None

    return pair12[pos:]


def extract_conversations_heuristic(pair12: bytes) -> Optional[bytes]:
    """
    Heuristically find conversation start when sprite count is unavailable

    Look for patterns that indicate conversation start:
    - 0x08 (speaker ID) followed by speaker byte
    - Or 0xFB/0xF1 (dialogue marker)
    """
    # Skip any leading 0xFF description blocks
    pos = 0
    while pos < len(pair12):
        if pair12[pos] == 0xFF:
            pos += 5
            while pos < len(pair12) and pair12[pos] != 0xFD:
                pos += 1
            if pos < len(pair12):
                pos += 1
        elif pair12[pos] in (0x08, 0xFB, 0xF1):
            # Found potential conversation start
            return pair12[pos:]
        else:
            pos += 1

    return None


def load_conversation_from_file(filename: str, offset: int = 0) -> bytes:
    """Load conversation data from a file"""
    with open(filename, 'rb') as f:
        f.seek(offset)
        # Read until we find a definitive end or reach EOF
        data = f.read(4096)  # Read a reasonable chunk
        return data


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Conversation Simulator")
        print()
        print("Usage:")
        print("  python simulate_conversation.py <alfred1_file> <room_number>")
        print("  python simulate_conversation.py ALFRED.1 2")
        print()
        print("Or provide hex data:")
        print("  python simulate_conversation.py --hex <hex_data>")
        sys.exit(1)

    if sys.argv[1] == '--hex':
        # Read hex data from command line
        hex_data = ''.join(sys.argv[2:]).replace(' ', '')
        conversation_data = bytes.fromhex(hex_data)
    else:
        # Load from ALFRED.1 file
        filename = sys.argv[1]

        if len(sys.argv) < 3:
            print("Error: Room number required")
            print("Usage: python simulate_conversation.py <alfred1_file> <room_number>")
            sys.exit(1)

        try:
            room_num = int(sys.argv[2])
        except ValueError:
            print(f"Error: Invalid room number '{sys.argv[2]}'")
            sys.exit(1)

        try:
            # Load entire ALFRED.1 file
            with open(filename, 'rb') as f:
                alfred1_data = f.read()

            # Extract conversation for this room
            conversation_data = extract_conversation_from_room(alfred1_data, room_num)

            if conversation_data is None:
                print(f"Error: No conversation data found for room {room_num}")
                sys.exit(1)



        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading file: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    # Run the simulation
    simulator = ConversationSimulator(conversation_data)
    simulator.run_conversation()


if __name__ == '__main__':
    main()
