#pragma description Alfred Pelrock - ALFRED.1 Room Structure
#pragma endian little

import std.mem;
import std.core;

struct Pair {
    u32 offset;
    u32 size;
};

/*struct RoomHeader {
    Pair pairs[13];
};

struct Headers {
    RoomHeader rooms[55];
};

Headers roomHeaders@0x00;
*/

/*u8 room2sounds[10] @727056;



struct Hotspot {
u8 type;
    u16 x;
    u16 y;
    u8 w;
    u8 h;
    u16 extra;
};
*/
struct Color {
    u8 r;
    u8 g;
    u8 b;
} [[hex::inline_visualize("color", r * 4, g * 4, b *4 , 255)]];
struct Palette {
    Color colors[256];
} ;
/*
Palette room2palette @0xB1D4a;

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
*/
// FF [ITEM_ID] 08 0D [INDEX] 00 [TEXT...] FD
struct Description {
    u8 start;
    u8 itemId;
    u16 magic;
    u8 index;
    u8 zero;
    char data[while(std::mem::read_unsigned($, 1) != 0xFD)];
    u8 terminator;
};
/*
struct Texts {
    Description puta;
    Description cajeroSprite;
    Description johnny;
    Description walker;
    Description cajero;
    Description mcdowells;
    Description planta1;
    Description planta2;
    Description outside;
    Description outside2;
};

//u8 room2Texts[4142] @0xB204A;
Texts room2Texts @0xB204A;
u8 room3Start @0xB3078;


struct Room21Anims {
    ThisAnimHeader avion1;
    ThisAnimHeader palmera;
    ThisAnimHeader duna;
    ThisAnimHeader camello;
    ThisAnimHeader avion2;
};


struct Room9Anims {
    ThisAnimHeader bibliotecaria;
    ThisAnimHeader ordenador;
    ThisAnimHeader raton;
    ThisAnimHeader telefono;
    ThisAnimHeader black;
};


Room9Anims room9anims @0x1ECDB8;
Room21Anims room21anims @0x3B6181;

*/

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

struct Walkbox {
    u16 x;
    u16 y;
    u16 w;
    u16 h;
    u8 flags;

};

struct Exit {
    u16 targetRoom;
    u8 flags;
    u16 x;
    u16 y;
    u8 w;
    u8 h;
    u16 targetX;
    u16 targetY;
    u8 dir;
};

fn min(s32 a, s32 b) {
    if (a > b)
        return b;
    else
        return a;
};

fn max(s32 a, s32 b) {
    if (a > b)
        return a;
    else
        return b;
};

struct RoomMetadata {
    
    u8 metadataPadding[5];
    u8 numAnims;
    u8 zeroes[92];
    
    u8 isRoom3 = (numAnims - 2) * 44 > 336;
    
    // Only define anims if numAnims > 2
    if (numAnims > 2) {
        if(isRoom3) {
            ThisAnimHeader anims[numAnims - 3];
            u8 finalAnim[40];
        } 
        else { 
            ThisAnimHeader anims[numAnims - 2];
        }
    }
    
    // Conditional padding based on room index or numAnims
    if (!isRoom3) {
        u8 zeroes2[336 - (numAnims - 2) * 44];
        u8 zeroes3[12];
    }

    u8 numExits;
    Exit exits[numExits];
    
    if (numExits * 14 <= 84) {
        u8 zeroes4[84 - numExits * 14];
    }
    
    u8 numWalkboxes;
    u8 unknown[4];
    Walkbox boxes[numWalkboxes];
    
    if (numWalkboxes * 9 <= 603) {
        u8 zeroes6[603 - numWalkboxes * 9];
    }
    
    u8 zeroes7[7];
    u8 numHotspots;
    u8 unknown2[1];
    Hotspot hotspots[numHotspots];
};


struct Descriptions {
    

};


struct Room {
    Pair pairs[13];
    u8 bg1[pairs[0].size] @pairs[0].offset;
    u8 bg2[pairs[1].size] @pairs[1].offset;
    u8 bg3[pairs[2].size] @pairs[2].offset;
    u8 bg4[pairs[3].size] @pairs[3].offset;   
    u8 bg5[pairs[4].size] @pairs[4].offset;
    u8 bg6[pairs[5].size] @pairs[5].offset;
    u8 bg7[pairs[6].size] @pairs[6].offset;
    u8 bg8[pairs[7].size] @pairs[7].offset;
    u8 spritePixelData[pairs[8].size] @pairs[8].offset;
    u8 sounds[pairs[9].size] @pairs[9].offset;
    //u8 metadata[pairs[10].size] @pairs[10].offset;
    RoomMetadata metadata @pairs[10].offset;
    Palette palette @pairs[11].offset;
    //u8 palette[pairs[11].size] @pairs[11].offset;
    u8 conversations[pairs[12].size] @pairs[12].offset;
};


//ThisAnimHeader room3anims[8] @0xEB57A;


Room rooms[56] @0x00000;