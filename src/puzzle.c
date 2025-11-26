#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Alfred Pelrock Slider Puzzle Shuffler
// Extracted from puzzle_minigame_handler @ 0x00026879

#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 400

// Global puzzle state
unsigned short tile_positions[1000];  // Maps position to tile ID
unsigned char puzzle_width = 8;       // Number of columns (DAT_0004b7a6)
unsigned char puzzle_height = 5;      // Number of rows (DAT_0004b7a8)
unsigned char tile_width = 80;        // Width per tile (DAT_0004b7aa)
unsigned char tile_height = 80;       // Height per tile
unsigned short empty_tile_pos = 0;    // Position of empty tile (DAT_0005179c)

// Simple random number generator (simplified from game's version)
unsigned short random_in_range(unsigned short max) {
    return rand() % max;
}

// Initialize puzzle in solved state
void init_puzzle() {
    int total_tiles = puzzle_width * puzzle_height;

    // Initialize tiles in order: 0, 1, 2, 3, ...
    for (int i = 0; i < total_tiles; i++) {
        tile_positions[i] = i;
    }

    empty_tile_pos = puzzle_width;  // Empty tile starts at a specific position
}

// Swap two tiles (core shuffle function from FUN_00026ba3)
void swap_tiles(unsigned short pos1, unsigned short pos2) {
    unsigned short temp = tile_positions[pos1];
    tile_positions[pos1] = tile_positions[pos2];
    tile_positions[pos2] = temp;

    printf("Swapped positions %d <-> %d (tiles %d <-> %d)\n",
           pos1, pos2, tile_positions[pos1], tile_positions[pos2]);
}

// Main shuffle routine (from puzzle_minigame_handler)
void shuffle_puzzle(int num_swaps) {
    unsigned short pos1, pos2;

    printf("Shuffling puzzle with %d random swaps...\n\n", num_swaps);

    for (int i = 0; i < num_swaps; i++) {
        // Generate two random positions
        do {
            pos1 = random_in_range(puzzle_width * puzzle_height);
            pos2 = random_in_range(puzzle_width * puzzle_height);
        } while (pos1 == pos2 || pos1 >= puzzle_width * puzzle_height ||
                 pos2 >= puzzle_width * puzzle_height);

        // Swap the tiles
        swap_tiles(pos1, pos2);
    }

    printf("\nShuffle complete!\n\n");
}

// Print puzzle state
void print_puzzle() {
    printf("Current puzzle state:\n");
    printf("---------------------\n");

    for (int y = 0; y < puzzle_height; y++) {
        for (int x = 0; x < puzzle_width; x++) {
            int pos = y * puzzle_width + x;
            printf("%3d ", tile_positions[pos]);
        }
        printf("\n");
    }
    printf("\n");
}

// Check if puzzle is solved
int is_solved() {
    int total_tiles = puzzle_width * puzzle_height;

    for (int i = 0; i < total_tiles - 1; i++) {
        if (i != tile_positions[i]) {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char *argv[]) {
    int num_swaps = 100;

    if (argc > 1) {
        num_swaps = atoi(argv[1]);
    }

    // Seed random number generator
    srand(time(NULL));

    printf("Alfred Pelrock - Slider Puzzle Shuffler\n");
    printf("========================================\n\n");
    printf("Puzzle size: %dx%d tiles (%dx%d pixels per tile)\n\n",
           puzzle_width, puzzle_height, tile_width, tile_height);

    // Initialize puzzle
    init_puzzle();
    printf("Initial state (solved):\n");
    print_puzzle();

    // Shuffle
    shuffle_puzzle(num_swaps);

    // Show result
    printf("Shuffled state:\n");
    print_puzzle();

    if (is_solved()) {
        printf("Puzzle is solved!\n");
    } else {
        printf("Puzzle is scrambled!\n");
    }

    return 0;
}
