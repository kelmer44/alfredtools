#pragma description Alfred Pelrock - ALFRED.1 Room Structure
#pragma endian little

import std.mem;


/*Offset   Size   Type      Description
------   ----   ----      -----------
+0x00    4      uint32    Chunk size (including header)
+0x04    2      uint16    Unknown/reserved
+0x06    2      uint16    Unknown/reserved
+0x08    1      uint8     Chunk type (1 = RLE, 2 = Block Copy)
+0x09    4      uint32    Frame data offset (relative to chunk start)
+0x0D    ...    bytes     Frame data begins here*/
    
struct ChunkHeader {
    u8 numChunks;
    u8 unknown[3];
    u32 chunkSize;
    u16 u1;
    u16 u2;
    u8 chunkType;
    u32 frameDataOffset;
};

struct Chunk {
    ChunkHeader header;
    u8 data[header.chunkSize - sizeof(header)];
};

struct FileHeader {
    u8 bytes[9];
};
    
struct Color {
    u8 r;
    u8 g;
    u8 b;
} [[hex::inline_visualize("color", r * 4, g * 4, b *4 , 255)]];

struct Palette {
    Color colors[256];
} ;

struct File {
    FileHeader header;
    Palette palette;
    padding[19703];
    Chunk chunk;
    
    Chunk delta1 @ 0x64000;
    Chunk delta2 @ 0x69000;
    Chunk delta3 @ 0x6E000;
    Chunk delta4 @ 0x73000;
    Chunk delta5 @ 0x78000; 
    Chunk delta6 @ 0x7D000; 
    Chunk delta7 @ 0x82000; 
    Chunk delta8 @ 0x87000;
};
 
File intro @0x00;