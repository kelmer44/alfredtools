#!/usr/bin/env python3
"""
Parse ALFRED.8 and ALFRED.B completely and generate ScummVM-ready C++ code.

ALFRED.8 Format (verified from hex dump):
  Entries: [room:2 LE][offset:2 LE][type:1][data:varies]
  Types:
    0x01 = 1-byte value  
    0x04 = 4-byte value (2x uint16 LE, typically X,Y)
    0x12 = 14-byte walkbox/structured data
  Terminator: 0xFFFF

ALFRED.B Format (from hex analysis):
  Entries: [room:2 LE][offset:2 LE][type:1][value:1]
  All entries are type=0x01 value=0x08 (conversation state reset flag)
  1180 entries total, 7082 bytes
"""

import struct
import json

def parse_alfred8_strict(filepath):
    """Parse ALFRED.8 using the confirmed format.
    
    Format: [room_id:2 LE][offset:2 LE][size:1][data:size bytes]
    
    The 'type' byte is actually the SIZE of the data that follows:
      0x01 = 1 byte value
      0x04 = 4 bytes (two u16 LE values, typically X,Y coordinates)
      0x12 = 18 bytes (0x12 decimal = 18) for walkbox/structured data
    
    Terminator: 0xFFFF as room ID
    """
    with open(filepath, 'rb') as f:
        data = f.read()
    
    entries = []
    pos = 0
    
    while pos + 5 <= len(data):
        # Read room ID (2 bytes LE)
        room_id = struct.unpack('<H', data[pos:pos+2])[0]
        
        # Check for terminator
        if room_id == 0xFFFF:
            break
        
        # Sanity check
        if room_id > 55:
            print(f"ERROR: Invalid room ID {room_id} at offset 0x{pos:x}")
            break
        
        # Read offset (2 bytes LE)
        offset = struct.unpack('<H', data[pos+2:pos+4])[0]
        
        # Read size/type (1 byte) - this IS the data size
        data_size = data[pos+4]
        
        pos += 5
        
        # Read data
        if pos + data_size > len(data):
            print(f"ERROR: Not enough data at offset 0x{pos:x}")
            break
            
        entry_data = list(data[pos:pos+data_size])
        pos += data_size
        
        entries.append({
            'room': room_id,
            'offset': offset,
            'type': data_size,  # Keep calling it type for compatibility
            'data': entry_data
        })
    
    return entries


def parse_alfred_b_strict(filepath):
    """Parse ALFRED.B - all entries are 6 bytes: room:2, offset:2, type:1, value:1"""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    entries = []
    pos = 0
    
    # Each entry is exactly 6 bytes
    while pos + 6 <= len(data):
        room_id = struct.unpack('<H', data[pos:pos+2])[0]
        offset = struct.unpack('<H', data[pos+2:pos+4])[0]
        entry_type = data[pos+4]
        value = data[pos+5]
        
        # Basic sanity check
        if room_id > 55:
            break
            
        entries.append({
            'room': room_id,
            'offset': offset,
            'type': entry_type,
            'value': value
        })
        
        pos += 6
    
    return entries


def generate_scummvm_code(alfred8_entries, alfred_b_entries):
    """Generate C++ code for ScummVM integration."""
    
    # Group by room
    alfred8_by_room = {}
    for e in alfred8_entries:
        room = e['room']
        if room not in alfred8_by_room:
            alfred8_by_room[room] = []
        alfred8_by_room[room].append(e)
    
    alfred_b_by_room = {}
    for e in alfred_b_entries:
        room = e['room']
        if room not in alfred_b_by_room:
            alfred_b_by_room[room] = []
        alfred_b_by_room[room].append(e)
    
    lines = []
    lines.append('// Auto-generated from ALFRED.8 and ALFRED.B')
    lines.append('// Default room state values for ScummVM Alfred Pelrock implementation')
    lines.append('//')
    lines.append('// USAGE:')
    lines.append('//   When loading a room from ALFRED.1:')
    lines.append('//   1. Load room data from ALFRED.1')
    lines.append('//   2. Call applyAlfred8Defaults(roomId, roomData, roomSize) to apply default state')
    lines.append('//   3. Call applyAlfredBDefaults(roomId, roomData, roomSize) to reset conversation flags')
    lines.append('//   4. Apply any save-game state on top')
    lines.append('//')
    lines.append('// This allows clean state reset without needing to re-read ALFRED.1 from disk.')
    lines.append('')
    lines.append('#ifndef ALFRED_ROOM_DEFAULTS_H')
    lines.append('#define ALFRED_ROOM_DEFAULTS_H')
    lines.append('')
    lines.append('#include "common/scummsys.h"')
    lines.append('#include <string.h>')
    lines.append('')
    lines.append('namespace Alfred {')
    lines.append('')
    lines.append('// Entry types/sizes for ALFRED.8')
    lines.append('// The "type" byte is actually the data size in bytes:')
    lines.append('//   0x01 = 1 byte value (state flag)')
    lines.append('//   0x04 = 4 bytes (X,Y coordinate pair, two u16 LE)')
    lines.append('//   0x12 = 18 bytes (walkbox/special structured data)')
    lines.append('')
    lines.append('// Maximum data size for any entry')
    lines.append('#define ALFRED8_MAX_DATA_SIZE 18')
    lines.append('')
    lines.append('struct Alfred8Entry {')
    lines.append('    uint16 offset;           // Offset within room data')
    lines.append('    uint8 size;              // Data size in bytes (was called "type")')
    lines.append('    byte data[ALFRED8_MAX_DATA_SIZE];')
    lines.append('};')
    lines.append('')
    
    # Generate ALFRED.8 per-room arrays
    for room in sorted(alfred8_by_room.keys()):
        entries = alfred8_by_room[room]
        lines.append(f'// Room {room}: {len(entries)} default state entries')
        lines.append(f'static const Alfred8Entry kRoom{room}Alfred8[] = {{')
        
        for e in entries:
            size = len(e['data'])
            data_str = ', '.join(f'0x{b:02x}' for b in e['data'])
            # Pad to 18 bytes (max size)
            if size < 18:
                data_str += ', ' + ', '.join(['0x00'] * (18 - size))
            lines.append(f'    {{0x{e["offset"]:04x}, {size}, {{{data_str}}}}},')
        
        lines.append('};')
        lines.append('')
    
    # Generate ALFRED.8 room index
    lines.append('// Index mapping room numbers to their ALFRED.8 default entries')
    lines.append('struct Alfred8RoomIndex {')
    lines.append('    int roomId;')
    lines.append('    const Alfred8Entry *entries;')
    lines.append('    int count;')
    lines.append('};')
    lines.append('')
    lines.append('static const Alfred8RoomIndex kAlfred8Index[] = {')
    
    for room in sorted(alfred8_by_room.keys()):
        count = len(alfred8_by_room[room])
        lines.append(f'    {{{room}, kRoom{room}Alfred8, {count}}},')
    
    lines.append('    {-1, nullptr, 0}  // Terminator')
    lines.append('};')
    lines.append('')
    
    # Generate ALFRED.B data
    lines.append('// ALFRED.B: Conversation state reset flags')
    lines.append('// All entries write value 0x08 at specified offset (type 0x01)')
    lines.append('// This resets conversation "already seen" flags')
    lines.append('')
    lines.append('struct AlfredBEntry {')
    lines.append('    uint16 offset;  // Offset within room data to write 0x08')
    lines.append('};')
    lines.append('')
    
    for room in sorted(alfred_b_by_room.keys()):
        entries = alfred_b_by_room[room]
        lines.append(f'// Room {room}: {len(entries)} conversation flag resets')
        lines.append(f'static const AlfredBEntry kRoom{room}AlfredB[] = {{')
        
        for e in entries:
            lines.append(f'    {{0x{e["offset"]:04x}}},')
        
        lines.append('};')
        lines.append('')
    
    # Generate ALFRED.B room index
    lines.append('// Index mapping room numbers to their ALFRED.B entries')
    lines.append('struct AlfredBRoomIndex {')
    lines.append('    int roomId;')
    lines.append('    const AlfredBEntry *entries;')
    lines.append('    int count;')
    lines.append('};')
    lines.append('')
    lines.append('static const AlfredBRoomIndex kAlfredBIndex[] = {')
    
    for room in sorted(alfred_b_by_room.keys()):
        count = len(alfred_b_by_room[room])
        lines.append(f'    {{{room}, kRoom{room}AlfredB, {count}}},')
    
    lines.append('    {-1, nullptr, 0}  // Terminator')
    lines.append('};')
    lines.append('')
    
    # Generate helper functions
    lines.append('/**')
    lines.append(' * Apply ALFRED.8 default state values to room data.')
    lines.append(' * Call after loading room from ALFRED.1, before applying save state.')
    lines.append(' *')
    lines.append(' * ALFRED.8 contains default values for:')
    lines.append(' * - Sprite positions (size 0x04: X,Y coordinates)')
    lines.append(' * - State flags (size 0x01: single byte)')
    lines.append(' * - Walkbox configurations (size 0x12: 18-byte blocks)')
    lines.append(' *')
    lines.append(' * @param roomId Room number (0-55)')
    lines.append(' * @param roomData Pointer to room data buffer')
    lines.append(' * @param roomSize Size of room data buffer')
    lines.append(' */')
    lines.append('inline void applyAlfred8Defaults(int roomId, byte *roomData, uint32 roomSize) {')
    lines.append('    for (int i = 0; kAlfred8Index[i].roomId >= 0; i++) {')
    lines.append('        if (kAlfred8Index[i].roomId == roomId) {')
    lines.append('            const Alfred8Entry *entries = kAlfred8Index[i].entries;')
    lines.append('            int count = kAlfred8Index[i].count;')
    lines.append('')
    lines.append('            for (int j = 0; j < count; j++) {')
    lines.append('                uint16 offset = entries[j].offset;')
    lines.append('                uint8 size = entries[j].size;')
    lines.append('')
    lines.append('                // Bounds check before writing')
    lines.append('                if (offset + size <= roomSize) {')
    lines.append('                    memcpy(roomData + offset, entries[j].data, size);')
    lines.append('                }')
    lines.append('            }')
    lines.append('            return;')
    lines.append('        }')
    lines.append('    }')
    lines.append('}')
    lines.append('')
    lines.append('/**')
    lines.append(' * Apply ALFRED.B conversation state resets to room data.')
    lines.append(' * This resets "conversation already seen" flags by writing 0x08 at each offset.')
    lines.append(' *')
    lines.append(' * @param roomId Room number (0-55)')
    lines.append(' * @param roomData Pointer to room data buffer')
    lines.append(' * @param roomSize Size of room data buffer')
    lines.append(' */')
    lines.append('inline void applyAlfredBDefaults(int roomId, byte *roomData, uint32 roomSize) {')
    lines.append('    for (int i = 0; kAlfredBIndex[i].roomId >= 0; i++) {')
    lines.append('        if (kAlfredBIndex[i].roomId == roomId) {')
    lines.append('            const AlfredBEntry *entries = kAlfredBIndex[i].entries;')
    lines.append('            int count = kAlfredBIndex[i].count;')
    lines.append('')
    lines.append('            for (int j = 0; j < count; j++) {')
    lines.append('                uint16 offset = entries[j].offset;')
    lines.append('')
    lines.append('                // Bounds check before writing')
    lines.append('                if (offset < roomSize) {')
    lines.append('                    roomData[offset] = 0x08;')
    lines.append('                }')
    lines.append('            }')
    lines.append('            return;')
    lines.append('        }')
    lines.append('    }')
    lines.append('}')
    lines.append('')
    lines.append('/**')
    lines.append(' * Apply all default state (both ALFRED.8 and ALFRED.B) to room data.')
    lines.append(' * Convenience function that calls both applyAlfred8Defaults and applyAlfredBDefaults.')
    lines.append(' *')
    lines.append(' * @param roomId Room number (0-55)')
    lines.append(' * @param roomData Pointer to room data buffer')
    lines.append(' * @param roomSize Size of room data buffer')
    lines.append(' */')
    lines.append('inline void applyAllRoomDefaults(int roomId, byte *roomData, uint32 roomSize) {')
    lines.append('    applyAlfred8Defaults(roomId, roomData, roomSize);')
    lines.append('    applyAlfredBDefaults(roomId, roomData, roomSize);')
    lines.append('}')
    lines.append('')
    lines.append('} // namespace Alfred')
    lines.append('')
    lines.append('#endif // ALFRED_ROOM_DEFAULTS_H')
    
    return '\n'.join(lines)


def main():
    base_path = '/Users/gabriel/Desktop/source/alfredtools/files'
    output_path = '/Users/gabriel/Desktop/source/alfredtools'
    
    # Parse ALFRED.8
    print("Parsing ALFRED.8...")
    alfred8_entries = parse_alfred8_strict(f'{base_path}/ALFRED.8')
    print(f"  Found {len(alfred8_entries)} entries")
    
    # Group and summarize
    rooms8 = set(e['room'] for e in alfred8_entries)
    print(f"  Rooms: {sorted(rooms8)}")
    
    # Parse ALFRED.B
    print("\\nParsing ALFRED.B...")
    alfred_b_entries = parse_alfred_b_strict(f'{base_path}/ALFRED.B')
    print(f"  Found {len(alfred_b_entries)} entries")
    
    roomsB = set(e['room'] for e in alfred_b_entries)
    print(f"  Rooms: {sorted(roomsB)}")
    
    # Verify ALFRED.B format (all type=0x01 value=0x08)
    types = set(e['type'] for e in alfred_b_entries)
    values = set(e['value'] for e in alfred_b_entries)
    print(f"  All types: {[hex(t) for t in types]}")
    print(f"  All values: {[hex(v) for v in values]}")
    
    # Save JSON for reference - grouped by room
    alfred8_by_room = {}
    for e in alfred8_entries:
        room = str(e['room'])
        if room not in alfred8_by_room:
            alfred8_by_room[room] = []
        alfred8_by_room[room].append({
            'offset': e['offset'],
            'size': e['type'],
            'data': e['data']
        })
    
    alfred_b_by_room = {}
    for e in alfred_b_entries:
        room = str(e['room'])
        if room not in alfred_b_by_room:
            alfred_b_by_room[room] = []
        alfred_b_by_room[room].append(e['offset'])  # Just offsets, all values are 0x08
    
    json_data = {
        'alfred8': alfred8_by_room,
        'alfredB': alfred_b_by_room
    }
    with open(f'{output_path}/alfred_defaults.json', 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"\\nSaved JSON: {output_path}/alfred_defaults.json")
    
    # Generate C++ code
    print("\\nGenerating C++ code...")
    cpp_code = generate_scummvm_code(alfred8_entries, alfred_b_entries)
    
    cpp_path = f'{output_path}/alfred_room_defaults.h'
    with open(cpp_path, 'w') as f:
        f.write(cpp_code)
    print(f"Saved: {cpp_path}")
    
    # Print summary
    print("\\n=== SUMMARY ===")
    print(f"ALFRED.8: {len(alfred8_entries)} entries across {len(rooms8)} rooms")
    print(f"ALFRED.B: {len(alfred_b_entries)} entries across {len(roomsB)} rooms")
    
    # Show some sample entries from ALFRED.8
    print("\\n=== ALFRED.8 Sample Entries ===")
    for room in sorted(rooms8)[:5]:
        room_entries = [e for e in alfred8_entries if e['room'] == room]
        print(f"\\nRoom {room}:")
        for e in room_entries:
            data_hex = ' '.join(f'{b:02x}' for b in e['data'])
            print(f"  offset=0x{e['offset']:04x} type=0x{e['type']:02x} data=[{data_hex}]")


if __name__ == '__main__':
    main()
