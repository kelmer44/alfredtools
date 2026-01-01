#pragma author gsanmartin
#pragma description Trick or Treat Room reader
#pragma MIME application/octet
import std.mem;
import std.string;

struct DataChunk {
  u16 roomId;
  u16 offset;
  u8 dataSize;
 u8 data[dataSize];
};

DataChunk chunks[while(!std::mem::eof())] @ 0x00;