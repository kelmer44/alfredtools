#pragma description Alfred Pelrock - ALFRED.1 Room Structure
#pragma endian little

import std.mem;

struct Pair {
    u32 offset;
    u32 size;
};

struct RoomHeader {
    Pair pairs[10];
};

struct Headers {
    RoomHeader rooms[55];
};

Headers roomHeaders@0x00;


struct ThisAnimHeader {
    u16 x;                  // Bytes 0-1
    u16 y;                  // Bytes 2-3
    u8 w;                   // Byte 4
    u8 h;                   // Byte 5
    u8 extra;               // Byte 6
    u8 unknown1;            // Byte 7
    u8 numAnims;            // Byte 8
    u8 unknown3;            // Byte 9
    u8 numFramesAnim1;      // Byte 10
    u8 numFramesAnim2;      // Byte 11
    u8 numFramesAnim3;      // Byte 12
    u8 numFramesAnim4;      // Byte 13
    u8 repeatAnim1;         // Byte 14
    u8 repeatAnim2;         // Byte 15
    u8 repeatAnim3;         // Byte 16
    u8 repeatAnim4;         // Byte 17
    u8 speedAnim1;          // Byte 18
    u8 speedAnim2;          // Byte 19
    u8 speedAnim3;          // Byte 20
    u8 speedAnim4;          // Byte 21
    u8 unknown_22_to_32[11]; // Bytes 22-32 (11 bytes)
    // Byte 33 (offset 0x21): Sprite type/layer - must be != 0xFF to be hotspot eligible
    u8 sprite_type;         // Byte 33
    // Byte 34 (offset 0x22): ACTION FLAGS bitmask
    // Bit 0 (0x01): Unknown action
    // Bit 1 (0x02): Unknown action
    // Bit 2 (0x04): Unknown action
    // Bit 3 (0x08): Unknown action
    // Bit 4 (0x10): TALK action available
    // Bit 5 (0x20): Unknown action
    // Bit 6 (0x40): Unknown action
    // Bit 7 (0x80): Unknown action
    u8 action_flags;        // Byte 34
    u8 unknown_35_to_37[3]; // Bytes 35-37 (3 bytes)
    // Byte 38 (offset 0x26): HOTSPOT FLAG
    // 0x00 = This sprite IS a clickable hotspot
    // 0x01 = This sprite is NOT a hotspot (decoration/non-interactive)
    u8 is_hotspot;          // Byte 38
    u8 unknown_39_to_43[5]; // Bytes 39-43
    // NOTE: Text descriptions indexed by combined order:
    // [selectable_sprites_in_order] + [static_hotspots_in_order]
    // NOT stored per-sprite! Position in list = text pointer index
};

struct Hotspot {
u8 type;
    u16 x;
    u16 y;
    u8 w;
    u8 h;
    u16 extra;
};


ThisAnimHeader chefSprite @0x253147;
ThisAnimHeader burgerSprite @0x253173;
ThisAnimHeader gatoSprite @0x25319F;

ThisAnimHeader putaSprite @0xB187C;
ThisAnimHeader cajeroSprite @0xB18A8;
ThisAnimHeader freddySprite @0xB18D4;
ThisAnimHeader walkerSprite @0xB1900;

ThisAnimHeader ventanasmuseoSprite @0x126C06;

u8 hostpotCountRoom0 @0x0230C6;
Hotspot cajonHostpost @0x230C8;
Hotspot twoHostpost @0x230D1;
Hotspot librosHostpost @0x230DA;
Hotspot fourHostpost @0x230E3;
Hotspot fiveHostpost @0x230EC;
Hotspot sixHostpost @0x230F5;
Hotspot bedHotspot @0x230FE;
Hotspot doorHotspot @0x23107;
Hotspot documentacionHotspot @0x23110;
Hotspot tarjetaHotspot @0x23119;
Hotspot fotoHotspot @0x23122;
Hotspot ventanaHotspot @0x2312B;

u8 room2HostpotCount @0xB1C94;
Hotspot cajeroHotspot @0xB1C96;
Hotspot puertaHotspot @0xB1C9F;
Hotspot planta1Hotspot @0xB1CA8;
Hotspot planta2Hotspot @0xB1CB1;
Hotspot unknown1Hotspot @0xB1CBA;
Hotspot unknown2Hotspot @0xB1CC3;

// Room 2 Text Descriptions
// Indexed by order: [selectable_sprites] + [static_hotspots]
// Text data starts after 0xFF marker (+ 2 bytes)
char room2_text0_putaSprite[100] @0x000B2050;      // Index 0: puta sprite
char room2_text1_cajeroSprite[100] @0x000B207B;    // Index 1: cajero sprite
char room2_text2_freddySprite[100] @0x000B209A;    // Index 2: freddy sprite
char room2_text3_walkerSprite[100] @0x000B20A9;    // Index 3: walker sprite
char room2_text4_cajeroHotspot[100] @0x000B20C1;   // Index 4: cajero static hotspot
char room2_text5_puertaHotspot[100] @0x000B20E4;   // Index 5: puerta hotspot
char room2_text6_planta1Hotspot[100] @0x000B2102;  // Index 6: planta1 hotspot
char room2_text7_planta2Hotspot[100] @0x000B211B;  // Index 7: planta2 hotspot
char room2_text8_unknown1Hotspot[100] @0x000B2134; // Index 8: unknown1 hotspot
char room2_text9_unknown2Hotspot[100] @0x000B2154; // Index 9: unknown2 hotspot
