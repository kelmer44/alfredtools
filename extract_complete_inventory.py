#!/usr/bin/env python3
"""
Final extraction: 69 icons with all their descriptions and metadata
"""

import os
import struct
from PIL import Image

# VGA palette
def get_vga_palette():
    vga_colors = [
        (0,0,0), (0,0,170), (0,170,0), (0,170,170), 
        (170,0,0), (170,0,170), (170,85,0), (170,170,170),
        (85,85,85), (85,85,255), (85,255,85), (85,255,255),
        (255,85,85), (255,85,255), (255,255,85), (255,255,255)
    ]
    palette = []
    for r,g,b in vga_colors:
        palette.extend([r, g, b])
    return palette

# Parse all 113 descriptions
def parse_all_descriptions():
    with open('files/JUEGO.EXE', 'rb') as f:
        data = f.read()
    
    start = 0x4715D
    end = 0x49018
    region = data[start:end]
    
    descriptions = []
    i = 0
    
    while i < len(region):
        if i + 3 < len(region) and region[i:i+3] == b'\xfd\x00\x08':
            color = region[i+3]
            text_start = i + 4
            
            # Find next description
            next_desc = region.find(b'\xfd\x00\x08', text_start)
            if next_desc == -1:
                text_end = len(region)
            else:
                text_end = next_desc
            
            # Trim trailing control chars
            while text_end > text_start and region[text_end-1] in [0, 0xF4, 0xF8, 0xF0]:
                text_end -= 1
            
            text_bytes = region[text_start:text_end]
            try:
                text = text_bytes.decode('cp850')
            except:
                text = text_bytes.decode('latin1', errors='replace')
            
            descriptions.append({
                'id': len(descriptions),
                'offset': start + i,
                'color': color,
                'text': text
            })
            
            i = text_end
        else:
            i += 1
    
    return descriptions

# Extract all 69 icons
def extract_all_icons():
    with open('files/ALFRED.4', 'rb') as f:
        data = f.read()
    
    icon_offset = 0xA57E
    icon_size = 0xE10  # 3600 bytes = 60x60 pixels
    num_icons = 69
    
    icons = []
    for icon_id in range(num_icons):
        offset = icon_offset + (icon_id * icon_size)
        icon_data = data[offset:offset + icon_size]
        
        img = Image.new('P', (60, 60))
        img.putpalette(get_vga_palette())
        img.putdata(icon_data)
        
        icons.append((icon_id, img))
    
    return icons

# Icon remapping formula from render_inventory_items @ 0x00012F06
def get_icon_for_object_id(obj_id):
    if obj_id < 59:
        if 11 < obj_id < 59:
            return ((obj_id - 11) & 3) + 11
        else:
            return obj_id
    else:
        return obj_id - 44

# Build reverse mapping: icon_id -> [object_ids]
def build_icon_to_objects_map():
    icon_map = {i: [] for i in range(69)}
    
    # We know there are 113 object IDs (0-112)
    for obj_id in range(113):
        icon_id = get_icon_for_object_id(obj_id)
        if 0 <= icon_id < 69:
            icon_map[icon_id].append(obj_id)
    
    return icon_map

# Main extraction
def main():
    print("Extracting 69 icons with descriptions...")
    
    descriptions = parse_all_descriptions()
    print(f"Loaded {len(descriptions)} descriptions")
    
    icons = extract_all_icons()
    print(f"Extracted {len(icons)} icons")
    
    icon_to_objects = build_icon_to_objects_map()
    
    # Create output structure
    output_dir = 'inventory_complete'
    os.makedirs(output_dir, exist_ok=True)
    
    for icon_id, img in icons:
        icon_dir = os.path.join(output_dir, f'icon_{icon_id:02d}')
        os.makedirs(icon_dir, exist_ok=True)
        
        # Save icon
        img_path = os.path.join(icon_dir, 'icon.png')
        img.save(img_path)
        
        # Get all objects using this icon
        object_ids = icon_to_objects[icon_id]
        
        # Save descriptions for each object
        for obj_id in object_ids:
            if obj_id < len(descriptions):
                desc = descriptions[obj_id]
                desc_file = os.path.join(icon_dir, f'description_obj{obj_id:03d}.txt')
                with open(desc_file, 'w', encoding='utf-8') as f:
                    f.write(f"Object ID: {obj_id}\n")
                    f.write(f"Icon ID: {icon_id}\n")
                    f.write(f"Color: 0x{desc['color']:02X}\n")
                    f.write(f"Offset: 0x{desc['offset']:05X}\n")
                    f.write("\n")
                    f.write(desc['text'])
        
        # Create metadata JSON
        import json
        metadata = {
            'icon_id': icon_id,
            'object_ids': object_ids,
            'num_objects': len(object_ids),
            'icon_file': 'icon.png',
            'icon_offset': 0xA57E + (icon_id * 0xE10)
        }
        
        meta_path = os.path.join(icon_dir, 'metadata.json')
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
    
    print(f"\nExtraction complete!")
    print(f"Created {len(icons)} icon folders in {output_dir}/")
    print(f"\nSummary:")
    print(f"  Total icons: 69")
    print(f"  Total objects: 113")
    print(f"  Icons with multiple objects: {sum(1 for objs in icon_to_objects.values() if len(objs) > 1)}")
    
    # Show which icons have multiple objects
    print(f"\nIcons shared by multiple objects:")
    for icon_id, object_ids in icon_to_objects.items():
        if len(object_ids) > 1:
            print(f"  Icon {icon_id:2d}: Objects {object_ids}")

if __name__ == '__main__':
    main()
