#pragma description Alfred Pelrock - ALFRED.7 Structure
#pragma endian little
#pragma array_limit 100000

import std.mem;
import std.core;
import std.string;


struct Color {
    u8 r;
    u8 g;
    u8 b;
} [[hex::inline_visualize("color", r * 4, g * 4, b *4 , 255)]];
struct Palette {
    Color colors[256];
} ;


struct RleChunk {
    u8 pixelData[while(
           !std::mem::eof() &&                        
           std::mem::read_string($, 4) != "BUDA"  )
       ];
   char marker[4];
};


RleChunk cuadroCama[8] @ 0x00;
Palette pal0 @ 0x7984;

u8 largeFontData[4608] @ 0x7DC8;
RleChunk alfredCombRight @ 0x108AE;
RleChunk alfredCombLeft @ 0x15958;
RleChunk computer[8] @ 0x1A9EE;