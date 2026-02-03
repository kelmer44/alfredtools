#pragma description Alfred Pelrock - ALFRED.1 Room Structure
#pragma endian little

import std.mem;
import std.core;
import std.string;


struct RleChunk {
    u8 pixelData[while(
           !std::mem::eof() &&                        
           std::mem::read_string($, 4) != "BUDA"  )
       ];
   char marker[4];
};


struct SingleAnim {
    u8 offsetX;
    u8 offsetY;
    u8 w;
    u8 h;
    padding[2];
    u8 numFrames;
};


struct RoomAnimations {
    u32 pointer;
    u8 unk[3];
    SingleAnim animA;
    u8 unkno[5];
    SingleAnim animB;
    u8 unknown[29];
    RleChunk data @ pointer;
};

RoomAnimations anims[55] @ 0x00;