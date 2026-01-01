#!/usr/bin/env python3
"""
Extract ALFRED.8 room default state data for ScummVM implementation.
Generates C++ code that can be used in ScummVM to apply default room state.

ALFRED.8 Format:
  Packed entries: [room_id:2 LE][offset:2 LE][type:1][data:varies]
  
  Type values:
    0x01 = 1-byte value
    0x02 = 2-byte value (u16 LE)  
    0x04 = 4-byte value (two u16 LE values, typically X,Y coordinates)
    0x12 = 14-byte block (special structured data)
  
  Terminator: 0xFFFF at room_id position
"""

import struct
import os

def parse_alfred8(data):
    """Parse ALFRED.8 and return list of entries.
    
    Format: [room_id:2 LE][offset:2 LE][type:1][data:varies]
    
    Types:
      0x01 = 1 byte value
      0x04 = 4 bytes (two u16 LE values, typically X,Y coordinates)
      0x12 = 14 bytes (special walkbox/hotspot structured data)
    """
    entries = []
    pos = 0
    
    while pos < len(data) - 4:
        # Read room ID (2 bytes LE)
        room_id = struct.unpack('<H', data[pos:pos+2])[0]
        
        # Check for terminator
        if room_id == 0xFFFF:
            print(f"Found terminator 0xFFFF at offset 0x{pos:x}")
            break
        
        # Sanity check - room IDs should be 0-55
        if room_id > 55:
            print(f"Warning: Invalid room ID {room_id} at offset 0x{pos:x}")
            # This might be data from a type 0x12 block bleeding over
            # Try to skip and continue
            pos += 1
            continue
            
        pos += 2
        
        # Read offset in ALFRED.1 room data (2 bytes LE)
        offset = struct.unpack('<H', data[pos:pos+2])[0]
        pos += 2
        
        # Read type (1 byte)
        entry_type = data[pos]
        pos += 1
        
        # Read value based on type
        if entry_type == 0x01:
            # 1-byte value
            if pos >= len(data):
                break
            value = data[pos]
            pos += 1
            entries.append({
                'room': room_id,
                'offset': offset,
                'type': entry_type,
                'size': 1,
                'data': bytes([value])
            })
        elif entry_type == 0x04:
            # 4-byte value (two u16 LE - typically X,Y)
            if pos + 4 > len(data):
                break
            entries.append({
                'room': room_id,
                'offset': offset,
                'type': entry_type,
                'size': 4,
                'data': data[pos:pos+4]
            })
            pos += 4
        elif entry_type == 0x12:
            # 14-byte special block (walkbox default data)
            if pos + 14 > len(data):
                break
            entries.append({
                'room': room_id,
                'offset': offset,
                'type': entry_type,
                'size': 14,
                'data': data[pos:pos+14]
            })
            pos += 14
        else:
            print(f"Unknown type 0x{entry_type:02x} at offset 0x{pos-1:x}, room {room_id}, offset 0x{offset:x}")
            # Assume 1 byte and continue
            if pos < len(data):
                value = data[pos]
                pos += 1
                entries.append({
                    'room': room_id,
                    'offset': offset,
                    'type': entry_type,
                    'size': 1,
                    'data': bytes([value])
                })
    
    return entries


def generate_cpp_header(entries):
    """Generate C++ header with room default data."""
    
    # Group by room
    by_room = {}
    for entry in entries:
        room = entry['room']
        if room not in by_room:
            by_room[room] = []
        by_room[room].append(entry)
    
    cpp = """// Auto-generated from ALFRED.8
// Room default state values - apply after loading room from ALFRED.1

#ifndef ALFRED_ROOM_DEFAULTS_H
#define ALFRED_ROOM_DEFAULTS_H

#include "common/scummsys.h"

namespace Alfred {

struct RoomDefaultEntry {
    uint16 offset;     // Offset within room data in ALFRED.1
    uint8 type;        // 0x01=byte, 0x02=word, 0x04=dword, 0x12=14-byte block
    uint8 size;        // Data size in bytes
    byte data[14];     // Max 14 bytes for type 0x12
};

"""
    
    # Generate per-room data
    for room in sorted(by_room.keys()):
        room_entries = by_room[room]
        cpp += f"// Room {room} - {len(room_entries)} default entries\n"
        cpp += f"static const RoomDefaultEntry kRoom{room}Defaults[] = {{\n"
        
        for entry in room_entries:
            data_hex = ', '.join(f'0x{b:02x}' for b in entry['data'])
            # Pad to 14 bytes
            padding_count = 14 - len(entry['data'])
            if padding_count > 0:
                data_hex += ', ' + ', '.join(['0x00'] * padding_count)
            
            cpp += f"    {{0x{entry['offset']:04x}, 0x{entry['type']:02x}, {entry['size']}, {{{data_hex}}}}},\n"
        
        cpp += "};\n\n"
    
    # Generate room index
    cpp += "// Room index - maps room number to its defaults array\n"
    cpp += "struct RoomDefaultsIndex {\n"
    cpp += "    int roomId;\n"
    cpp += "    const RoomDefaultEntry *entries;\n"
    cpp += "    int count;\n"
    cpp += "};\n\n"
    
    cpp += "static const RoomDefaultsIndex kRoomDefaultsIndex[] = {\n"
    for room in sorted(by_room.keys()):
        count = len(by_room[room])
        cpp += f"    {{{room}, kRoom{room}Defaults, {count}}},\n"
    cpp += "    {-1, nullptr, 0}  // Terminator\n"
    cpp += "};\n\n"
    
    # Generate helper function
    cpp += """/**
 * Apply default room state from ALFRED.8 data.
 * Call this after loading room data from ALFRED.1 but before applying save state.
 * 
 * @param roomId The room number (0-55)
 * @param roomData Pointer to room data loaded from ALFRED.1
 * @param roomDataSize Size of room data
 */
inline void applyRoomDefaults(int roomId, byte *roomData, uint32 roomDataSize) {
    for (int i = 0; kRoomDefaultsIndex[i].roomId >= 0; i++) {
        if (kRoomDefaultsIndex[i].roomId == roomId) {
            const RoomDefaultEntry *entries = kRoomDefaultsIndex[i].entries;
            int count = kRoomDefaultsIndex[i].count;
            
            for (int j = 0; j < count; j++) {
                uint16 offset = entries[j].offset;
                uint8 size = entries[j].size;
                
                // Bounds check
                if (offset + size <= roomDataSize) {
                    memcpy(roomData + offset, entries[j].data, size);
                }
            }
            break;
        }
    }
}

} // namespace Alfred

#endif // ALFRED_ROOM_DEFAULTS_H
"""
    
    return cpp


def generate_json(entries):
    """Generate JSON for easier consumption."""
    import json
    
    by_room = {}
    for entry in entries:
        room = entry['room']
        if room not in by_room:
            by_room[room] = []
        by_room[room].append({
            'offset': entry['offset'],
            'type': entry['type'],
            'size': entry['size'],
            'data': list(entry['data'])
        })
    
    return json.dumps(by_room, indent=2)


def analyze_alfred_b(data):
    """Analyze ALFRED.B structure."""
    print(f"\n=== ALFRED.B Analysis ===")
    print(f"Size: {len(data)} bytes")
    
    # Look for patterns
    # From the hex dump, pattern seems to be:
    # [room:2 LE][offset:2 LE][type:1][value:1]
    # All entries appear to be type 0x01 with value 0x08
    
    pos = 0
    entries = []
    
    while pos < len(data) - 5:
        room = struct.unpack('<H', data[pos:pos+2])[0]
        
        # Check bounds
        if room > 55:
            print(f"Stopping at offset 0x{pos:x}, invalid room {room}")
            break
            
        offset = struct.unpack('<H', data[pos+2:pos+4])[0]
        entry_type = data[pos+4]
        value = data[pos+5]
        
        entries.append({
            'room': room,
            'offset': offset,
            'type': entry_type,
            'value': value
        })
        
        pos += 6
    
    # Group by room
    by_room = {}
    for e in entries:
        if e['room'] not in by_room:
            by_room[e['room']] = []
        by_room[e['room']].append(e)
    
    print(f"Parsed {len(entries)} entries")
    print(f"Rooms with entries: {sorted(by_room.keys())}")
    
    # Check if all values are the same
    unique_types = set(e['type'] for e in entries)
    unique_values = set(e['value'] for e in entries)
    print(f"Unique types: {[hex(t) for t in unique_types]}")
    print(f"Unique values: {[hex(v) for v in unique_values]}")
    
    # Print sample entries
    print("\nSample entries:")
    for e in entries[:10]:
        print(f"  Room {e['room']:2d}, offset 0x{e['offset']:04x}, type 0x{e['type']:02x}, value 0x{e['value']:02x}")
    
    return entries, by_room


def main():
    base_path = "/Users/gabriel/Desktop/source/alfredtools/files"
    
    # Parse ALFRED.8
    alfred8_path = os.path.join(base_path, "ALFRED.8")
    with open(alfred8_path, 'rb') as f:
        alfred8_data = f.read()
    
    print(f"=== ALFRED.8 Analysis ===")
    print(f"Size: {len(alfred8_data)} bytes")
    print(f"\nRaw hex (first 128 bytes):")
    for i in range(0, min(128, len(alfred8_data)), 16):
        hex_part = ' '.join(f'{b:02x}' for b in alfred8_data[i:i+16])
        print(f"  {i:04x}: {hex_part}")
    
    entries = parse_alfred8(alfred8_data)
    
    print(f"\nParsed {len(entries)} entries")
    
    # Group by room for analysis
    by_room = {}
    for entry in entries:
        room = entry['room']
        if room not in by_room:
            by_room[room] = []
        by_room[room].append(entry)
    
    print(f"Rooms with defaults: {sorted(by_room.keys())}")
    
    # Print room summaries
    for room in sorted(by_room.keys()):
        print(f"\n  Room {room}: {len(by_room[room])} entries")
        for e in by_room[room]:
            data_hex = ' '.join(f'{b:02x}' for b in e['data'])
            print(f"    offset=0x{e['offset']:04x}, type=0x{e['type']:02x}, data=[{data_hex}]")
    
    # Generate C++ header
    cpp_code = generate_cpp_header(entries)
    cpp_path = os.path.join(os.path.dirname(base_path), "alfred8_room_defaults.h")
    with open(cpp_path, 'w') as f:
        f.write(cpp_code)
    print(f"\nGenerated C++ header: {cpp_path}")
    
    # Generate JSON
    json_data = generate_json(entries)
    json_path = os.path.join(os.path.dirname(base_path), "alfred8_room_defaults.json")
    with open(json_path, 'w') as f:
        f.write(json_data)
    print(f"Generated JSON: {json_path}")
    
    # Analyze ALFRED.B
    alfred_b_path = os.path.join(base_path, "ALFRED.B")
    if os.path.exists(alfred_b_path) and os.path.getsize(alfred_b_path) > 0:
        with open(alfred_b_path, 'rb') as f:
            alfred_b_data = f.read()
        
        print(f"\nALFRED.B raw hex (first 128 bytes):")
        for i in range(0, min(128, len(alfred_b_data)), 16):
            hex_part = ' '.join(f'{b:02x}' for b in alfred_b_data[i:i+16])
            print(f"  {i:04x}: {hex_part}")
        
        b_entries, b_by_room = analyze_alfred_b(alfred_b_data)
        
        # ALFRED.B appears to be conversation/dialog state defaults
        # All entries are type 0x01 value 0x08, at various offsets
        # This likely sets initial "conversation not yet had" flags


if __name__ == "__main__":
    main()
