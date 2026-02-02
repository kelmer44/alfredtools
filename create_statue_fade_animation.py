#!/usr/bin/env python3
"""
Create an animated GIF showing the statue palette fade effect from room 7.
This animates the palette transition when using the amulet on the statue.
"""

from PIL import Image
import os

# Palette indices to modify (from documentation)
PALETTE_INDICES = [30, 37, 39, 41, 44, 62, 74, 79, 83, 89, 105, 120, 152, 179, 217, 238]

# Source colors (6-bit VGA values, need to multiply by 4 for 8-bit)
SOURCE_COLORS = [
    (44, 44, 40),  # Index 30
    (36, 36, 36),  # Index 37
    (16, 16, 16),  # Index 39
    (20, 20, 20),  # Index 41
    (36, 36, 32),  # Index 44
    (28, 32, 28),  # Index 62
    (32, 32, 32),  # Index 74
    (16, 16, 12),  # Index 79
    (16, 20, 20),  # Index 83
    (52, 52, 44),  # Index 89
    (12, 12, 12),  # Index 105
    (36, 40, 40),  # Index 120
    (45, 44, 40),  # Index 152
    (48, 52, 44),  # Index 179
    (24, 24, 24),  # Index 217
    (24, 28, 28),  # Index 238
]

# Target colors (6-bit VGA values)
TARGET_COLORS = [
    (53, 34, 23),  # Index 30
    (62, 39, 3),   # Index 37
    (46, 5, 1),    # Index 39
    (9, 3, 0),     # Index 41
    (48, 22, 15),  # Index 44
    (30, 16, 25),  # Index 62
    (63, 43, 16),  # Index 74
    (60, 25, 0),   # Index 79
    (16, 20, 20),  # Index 83 (no change)
    (63, 38, 20),  # Index 89
    (0, 0, 0),     # Index 105
    (36, 40, 40),  # Index 120 (no change)
    (27, 6, 20),   # Index 152
    (48, 52, 44),  # Index 179 (no change)
    (29, 5, 0),    # Index 217
    (50, 13, 7),   # Index 238
]


def vga6_to_rgb8(r, g, b):
    """Convert 6-bit VGA color to 8-bit RGB."""
    return (r * 4, g * 4, b * 4)


def interpolate_color(src, tgt, t):
    """Interpolate between source and target colors. t ranges from 0.0 to 1.0."""
    return tuple(int(src[i] + (tgt[i] - src[i]) * t) for i in range(3))


def create_frame(base_image, palette, t):
    """Create a single animation frame with interpolated palette."""
    # Copy the image
    frame = base_image.copy()
    
    # Get the palette as a list
    pal_data = list(palette)
    
    # Modify only the specified palette indices
    for i, idx in enumerate(PALETTE_INDICES):
        src = vga6_to_rgb8(*SOURCE_COLORS[i])
        tgt = vga6_to_rgb8(*TARGET_COLORS[i])
        
        # Interpolate
        new_color = interpolate_color(src, tgt, t)
        
        # Update palette (each index has R, G, B at positions idx*3, idx*3+1, idx*3+2)
        pal_data[idx * 3] = new_color[0]
        pal_data[idx * 3 + 1] = new_color[1]
        pal_data[idx * 3 + 2] = new_color[2]
    
    # Apply modified palette
    frame.putpalette(pal_data)
    
    return frame


def main():
    # Load the room 7 background
    img_path = "backgrounds_color/room_07.png"
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found!")
        return
    
    base_image = Image.open(img_path)
    
    if base_image.mode != 'P':
        print(f"Error: Image is not palettized (mode={base_image.mode})")
        return
    
    # Get original palette
    original_palette = base_image.getpalette()
    
    # Animation parameters
    num_frames = 20  # Frames for fade
    frame_duration = 100  # ms per frame (100ms = 10fps)
    hold_duration = 500  # ms to hold at end states
    
    frames = []
    durations = []
    
    # Hold at original state
    frame = create_frame(base_image, original_palette, 0.0)
    frames.append(frame.convert('P'))
    durations.append(hold_duration)
    
    # Forward fade (gray -> red/warm)
    print("Generating forward fade frames...")
    for i in range(num_frames + 1):
        t = i / num_frames
        frame = create_frame(base_image, original_palette, t)
        frames.append(frame.convert('P'))
        durations.append(frame_duration)
    
    # Hold at target state
    frame = create_frame(base_image, original_palette, 1.0)
    frames.append(frame.convert('P'))
    durations.append(hold_duration)
    
    # Reverse fade (red/warm -> gray)
    print("Generating reverse fade frames...")
    for i in range(num_frames, -1, -1):
        t = i / num_frames
        frame = create_frame(base_image, original_palette, t)
        frames.append(frame.convert('P'))
        durations.append(frame_duration)
    
    # Hold at original state again
    frame = create_frame(base_image, original_palette, 0.0)
    frames.append(frame.convert('P'))
    durations.append(hold_duration)
    
    # Save as animated GIF
    output_path = "output_statue_fade/statue_palette_fade.gif"
    os.makedirs("output_statue_fade", exist_ok=True)
    
    print(f"Saving animation to {output_path}...")
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0  # Loop forever
    )
    
    print(f"Animation saved! Total frames: {len(frames)}")
    
    # Also save the before and after static images
    before_path = "output_statue_fade/statue_before.png"
    after_path = "output_statue_fade/statue_after.png"
    
    create_frame(base_image, original_palette, 0.0).save(before_path)
    create_frame(base_image, original_palette, 1.0).save(after_path)
    
    print(f"Saved static images: {before_path}, {after_path}")


if __name__ == "__main__":
    main()
