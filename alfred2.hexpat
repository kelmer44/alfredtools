#pragma description Alfred Pelrock - ALFRED.1 Room Structure
#pragma endian little

import std.mem;
import std.core;
import std.string;


struct SingleAnim {
    u8 offsetX;
    u8 offsetY;
    u8 w;
    u8 h;
    padding[2];
    u8 numFrames;
};

struct RoomAnimations {
    u32 spritePointer;
    padding[3];
    SingleAnim animA;
    padding[5];
    SingleAnim animB;
    padding[29];
};

RoomAnimations anims[55] @ 0x00;