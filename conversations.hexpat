#pragma endian little

// Spanish character decoding
fn decode_char(u8 b) {
    if (b == 0x80) return "ñ";
    if (b == 0x81) return "í";
    if (b == 0x82) return "¡";
    if (b == 0x83) return "¿";
    if (b == 0x84) return "ú";
    if (b == 0x7B) return "á";
    if (b == 0x7C) return "é";
    if (b == 0x7D) return "í";
    if (b == 0x7E) return "ó";
    if (b == 0x7F) return "ú";
    if (b >= 0x20 && b <= 0x7A) return str::to_string(char(b));
    return "";
};

// Control bytes enum
enum ControlByte : u8 {
    SPEAKER = 0x08,
    SPACE = 0x20,
    END_TEXT = 0xFD,
    TEXT_TERMINATOR = 0xFC,
    CHOICE_MARKER = 0xFB,
    DISABLED_CHOICE = 0xFA,
    PAGE_BREAK = 0xF9,
    ACTION_TRIGGER = 0xF8,
    END_BRANCH = 0xF7,
    LINE_CONTINUATION = 0xF6,
    END_CONV_ALT = 0xF5,
    END_CONV = 0xF4,
    CHOICE_MARKER_ALT = 0xF1,
    GO_BACK = 0xF0,
    END_ALT2 = 0xEB
};

// Speaker IDs
enum SpeakerID : u8 {
    ALFRED = 0x0D,
    NPC = 0x20
};

// Variable-length text until control byte
// Variable-length text until control byte (0xFD)
struct ConvText {
    u8 text_bytes[while(std::mem::read_unsigned($, 1) != 0xFD)];
} [[sealed]];

// Sprite/Hotspot Description
struct Description {
    u8 marker [[comment("Should be 0xFF")]];
    u32 item_id;
    u8 index;

    ConvText text;

    ControlByte end_marker [[comment("Should be 0xFD")]];
};

// Speaker declaration
struct Speaker {
    ControlByte marker [[comment("0x08 = SPEAKER")]];
    SpeakerID speaker_id;
};

// Dialogue line (speaker + text)
struct DialogueLine {
    Speaker speaker;
    ConvText text;
    ControlByte end_marker [[comment("Should be 0xFD")]];
};

// Choice marker (0xFB/0xF1 + index + speaker + text)
struct ChoiceMarker {
    ControlByte marker [[comment("0xFB or 0xF1")]];
    u8 choice_index [[comment("Index groups choices; count>1=real choice, count=1=auto-dialogue")]];
    Speaker speaker [[comment("Usually ALFRED for choices")]];
    ConvText text;
    ControlByte end_marker [[comment("0xFD")]];
};

// Action trigger
struct ActionTrigger {
    ControlByte marker [[comment("0xF8")]];
    u8 param1;
    u8 param2;
};

// End marker
struct EndMarker {
    ControlByte marker [[comment("0xF4/0xF7/0xF5/0xFE/0xEB/0xF0")]];
};

// Single conversation element (can be dialogue, choice, action, or end)
struct ConversationElement {
    u8 peek = std::mem::read_unsigned($, 1) [[hidden]];

    if (peek == 0x08) {
        DialogueLine dialogue;
    } else if (peek == 0xFB || peek == 0xF1) {
        ChoiceMarker choice;
    } else if (peek == 0xF8) {
        ActionTrigger action;
    } else if (peek == 0xF4 || peek == 0xF7 || peek == 0xF5 ||
               peek == 0xFE || peek == 0xEB || peek == 0xF0) {
        EndMarker end;
    } else if (peek == 0xFD || peek == 0xFC) {
        u8 skip [[comment("Stray end marker")]];
    } else {
        u8 unknown [[comment("Unknown byte")]];
    }
};

// Full conversation structure for a room
struct RoomConversations {
    // First, all descriptions (sprites + hotspots)
    Description descriptions[while(std::mem::read_unsigned($, 1) == 0xFF)];

    // Then conversation elements until end of data
    ConversationElement elements[while($ < std::mem::size())];
};

// Example: Room 2 conversations at the appropriate offset in pair 12
// You would need to position this at the correct offset in ALFRED.1
// For Room 2, pair 12 data starts after header, and conversations start
// after the sprite/hotspot descriptions
//
// Usage:
// 1. Navigate to Room 2's pair 12 offset in ALFRED.1
// 2. Skip to the descriptions/conversation data section
// 3. Place this struct:
// RoomConversations room2_conversations @ 0xXXXXXXXX;
