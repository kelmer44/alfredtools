#pragma description Alfred Pelrock - ALFRED.1 Room Structure
#pragma endian little
#pragma array_limit 100000

import std.mem;
import std.core;
import std.string;

struct AnimationSetHeader {
    u32 data_offset;        // +0x00: Offset to start of pixel data (little-endian)
    u8  unknown2[3];        // +0x03-0x08: Unknown fields

    u8 offsetXA;
    u8 offsetYA;
    // Animation A (typically mouth position 1 or closed mouth)
    u8  anim_a_width;       // +0x09: Width in pixels
    u8  anim_a_height;      // +0x0A: Height in pixels
    u8 unknown3[2];           // +0x0B-0x0C: Unknown
    u8  anim_a_frames;      // +0x0D: Number of animation frames
    u8  unknown4[5];        // +0x0E-0x14: Unknown fields
    u8 offsetXB;
    u8 offsetYB;
    // Animation B (typically mouth position 2 or open mouth)
    u8  anim_b_width;       // +0x15: Width in pixels
    u8  anim_b_height;      // +0x16: Height in pixels
    u16 unknown5;           // +0x17-0x18: Unknown
    u8  anim_b_frames;      // +0x19: Number of animation frames
    u8  unknown6[29];       // +0x1A-0x36: Unknown/padding fields
};

struct Anim {
    AnimationSetHeader header;
    if(header.data_offset > 0) {
        u8 pixelDataA[while(
           !std::mem::eof() &&                        
    
           std::mem::read_string($, 4) != "BUDA"  )
       ] @ header.data_offset;
       char markerA[4] @ header.data_offset + sizeof(pixelDataA);
       
       /*if(header.anim_b_frames > 0) {
            u8 pixelDataB[while(
               !std::mem::eof() &&                        
        
               std::mem::read_string($, 4) != "BUDA"  )
               ] @ header.data_offset + sizeof(pixelDataA) + 4;
           char markerB[4] @ header.data_offset + sizeof(pixelDataA) + 4 + sizeof(pixelDataB);
       
       }*/
    }
};


struct File {
    Anim anims[55];
};

File alfred2 @ 0x00;