#!/usr/bin/env python3
"""
Conversation Simulator for the Game

This script simulates the conversation system, allowing you to:
- View dialogue lines (press Enter to advance)
- Make choices when presented (type choice number)
- Follow the conversation flow as it appears in the game

Usage:
    python simulate_conversation.py <resource_file> <room_number>

Or interactively select a conversation from loaded data.
"""

import sys
import struct
from typing import List, Tuple, Optional
from dataclasses import dataclass
from collections import Counter

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

    def decode_text(self, data: bytes) -> str:
        """Decode text using the game's character encoding"""
        result = []
        for byte in data:
            if byte in CHAR_MAP:
                result.append(CHAR_MAP[byte])
            elif 0x20 <= byte < 0x7F:
                result.append(chr(byte))
            else:
                result.append(f'[{byte:02X}]')
        return ''.join(result)

    def read_text_segment(self, start_pos: int) -> Tuple[str, int, int]:
        """
        Read a text segment from the conversation data

        Returns: (text, speaker_id, end_position)
        """
        pos = start_pos
        speaker_id = None
        text_bytes = []

        # Check for speaker ID
        if pos < len(self.data) and self.data[pos] == CTRL_SPEAKER_ID:
            speaker_id = self.data[pos + 1]
            pos += 2

        # Read text until control byte
        while pos < len(self.data):
            byte = self.data[pos]

            # End markers
            if byte in (CTRL_END_TEXT, CTRL_END_CONVERSATION, CTRL_ACTION_TRIGGER,
                       CTRL_GO_BACK, CTRL_ALT_END_MARKER_2, CTRL_END_BRANCH,
                       CTRL_ALT_END_MARKER_1, CTRL_ALT_END_MARKER_3):
                break

            # Skip certain control bytes
            if byte == CTRL_SPEAKER_ID:
                speaker_id = self.data[pos + 1]
                pos += 2
                continue

            if byte == CTRL_LINE_CONTINUE or byte == CTRL_PAGE_BREAK:
                text_bytes.append(ord('\n'))
                pos += 1
                continue

            # Regular text
            text_bytes.append(byte)
            pos += 1

        text = self.decode_text(bytes(text_bytes))
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

        Implements the critical discovery: if a choice index appears
        multiple times, it's a real choice. If only once, it's auto-dialogue.
        """
        pos = start_pos
        choices = []
        choice_indices = []
        first_choice_index = None

        # Scan ahead to find all dialogue markers
        while pos < len(self.data):
            byte = self.data[pos]

            # Stop at end markers
            if byte in (CTRL_ALT_END_MARKER_1, CTRL_END_BRANCH, CTRL_ALT_END_MARKER_3):
                break

            # Found a dialogue marker
            if byte in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2):
                if pos + 1 < len(self.data):
                    choice_index = self.data[pos + 1]
                    choice_indices.append(choice_index)

                    # Check if disabled
                    is_disabled = (pos in self.disabled_choices or
                                 (pos + 2 < len(self.data) and
                                  self.data[pos + 2] == CTRL_DISABLED_CHOICE))

                    # First choice or same index group
                    if first_choice_index is None:
                        first_choice_index = choice_index
                        text, speaker_id, end_pos = self.read_text_segment(pos + 2)
                        choices.append(ChoiceOption(
                            index=choice_index,
                            text=text.strip(),
                            is_disabled=is_disabled,
                            data_offset=pos
                        ))
                    elif choice_index == first_choice_index:
                        text, speaker_id, end_pos = self.read_text_segment(pos + 2)
                        choices.append(ChoiceOption(
                            index=choice_index,
                            text=text.strip(),
                            is_disabled=is_disabled,
                            data_offset=pos
                        ))
                    elif choice_index < first_choice_index:
                        # Different index group - stop
                        break

            pos += 1

        # Determine if real choice or auto-dialogue
        index_counts = Counter(choice_indices)

        # Filter out choices that only appear once (auto-dialogue)
        if choices and index_counts[first_choice_index] == 1:
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
        input()

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
            input()
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
            except KeyboardInterrupt:
                print("\n\nConversation interrupted.")
                sys.exit(0)

    def run_conversation(self):
        """Main conversation loop - simulates handle_conversation_tree()"""
        print("\n" + "="*60)
        print("CONVERSATION START")
        print("="*60)

        self.position = 0

        # OUTER LOOP: Continue until conversation ends
        while self.position < len(self.data):
            # 1. Read and display current dialogue
            text, speaker_id, end_pos = self.read_text_segment(self.position)

            if text.strip():
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
            if control_byte in (CTRL_END_TEXT, CTRL_ACTION_TRIGGER, CTRL_GO_BACK):
                self.position += 1
                if control_byte == CTRL_ACTION_TRIGGER:
                    # Skip action parameters
                    self.position += 2

            # 3. Parse choices
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

            # 6. Move to selected choice text
            # Find the choice marker in the data
            search_pos = self.position
            choice_count = 0

            while search_pos < len(self.data):
                byte = self.data[search_pos]

                if byte in (CTRL_DIALOGUE_MARKER, CTRL_DIALOGUE_MARKER_2):
                    if search_pos + 1 < len(self.data):
                        idx = self.data[search_pos + 1]
                        if idx == selected_choice.index or selected_choice.index == -1:
                            if choice_count == selected_index:
                                # Found it - move to text after marker + index
                                self.position = search_pos + 2
                                break
                            choice_count += 1

                search_pos += 1

            # Display the selected choice as dialogue
            text, speaker_id, end_pos = self.read_text_segment(self.position)
            if text.strip():
                self.display_dialogue(text, speaker_id)

            self.position = end_pos

            # Skip past end marker
            if self.position < len(self.data):
                control_byte = self.data[self.position]
                if control_byte == CTRL_END_TEXT:
                    self.position += 1

        print("\n" + "="*60)
        print("CONVERSATION ENDED")
        print("="*60)


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
        print("Usage: python simulate_conversation.py <data_file> [offset]")
        print()
        print("Or provide conversation data in hex format:")
        print("  python simulate_conversation.py --hex <hex_data>")
        sys.exit(1)

    if sys.argv[1] == '--hex':
        # Read hex data from command line
        hex_data = ''.join(sys.argv[2:]).replace(' ', '')
        conversation_data = bytes.fromhex(hex_data)
    else:
        # Load from file
        filename = sys.argv[1]
        offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0

        try:
            conversation_data = load_conversation_from_file(filename, offset)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)

    # Run the simulation
    simulator = ConversationSimulator(conversation_data)
    simulator.run_conversation()


if __name__ == '__main__':
    main()
