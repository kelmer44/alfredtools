#include <stdio.h>
#include <stdlib.h>
#include "lodepng.h"
#include "functions.h"

unsigned char *getPalette() {
	/*
	 * Build a default 256-color VGA-like palette (commonly used in 256-color terminals):
	 * - First 16: standard EGA/VGA system colors
	 * - Next 216: 6x6x6 color cube with levels {0,95,135,175,215,255}
	 * - Last 24: grayscale ramp
	 * The palette is returned as an allocated buffer of 256*4 bytes (RGBA).
	 */
	unsigned char *palette = (unsigned char *)malloc(256 * 4);
	if (!palette) {
		fprintf(stderr, "getPalette: out of memory allocating palette\n");
		return NULL;
	}

	// 1) First 16 system colors (approximate standard VGA/EGA palette)
	const unsigned char sys16[16][3] = {
		{0x00,0x00,0x00}, // 0 black
		{0x80,0x00,0x00}, // 1 maroon
		{0x00,0x80,0x00}, // 2 green
		{0x80,0x80,0x00}, // 3 olive
		{0x00,0x00,0x80}, // 4 navy
		{0x80,0x00,0x80}, // 5 purple
		{0x00,0x80,0x80}, // 6 teal
		{0xc0,0xc0,0xc0}, // 7 silver
		{0x80,0x80,0x80}, // 8 gray
		{0xff,0x00,0x00}, // 9 red
		{0x00,0xff,0x00}, // 10 lime
		{0xff,0xff,0x00}, // 11 yellow
		{0x00,0x00,0xff}, // 12 blue
		{0xff,0x00,0xff}, // 13 fuchsia
		{0x00,0xff,0xff}, // 14 aqua
		{0xff,0xff,0xff}  // 15 white
	};

	for (int i = 0; i < 16; ++i) {
		palette[i*4 + 0] = sys16[i][0];
		palette[i*4 + 1] = sys16[i][1];
		palette[i*4 + 2] = sys16[i][2];
		palette[i*4 + 3] = 255;
	}

	// 2) 6x6x6 color cube (216 colors)
	const int levels[6] = {0, 95, 135, 175, 215, 255};
	int idx = 16;
	for (int r = 0; r < 6; ++r) {
		for (int g = 0; g < 6; ++g) {
			for (int b = 0; b < 6; ++b) {
				if (idx >= 16 + 216) break;
				palette[idx*4 + 0] = (unsigned char)levels[r];
				palette[idx*4 + 1] = (unsigned char)levels[g];
				palette[idx*4 + 2] = (unsigned char)levels[b];
				palette[idx*4 + 3] = 255;
				++idx;
			}
		}
	}

	// 3) Grayscale ramp: 24 values
	for (int i = 0; i < 24; ++i) {
		int v = 8 + i * 10; // 8,18,...,238
		int p = 16 + 216 + i; // starting index 232
		palette[p*4 + 0] = (unsigned char)v;
		palette[p*4 + 1] = (unsigned char)v;
		palette[p*4 + 2] = (unsigned char)v;
		palette[p*4 + 3] = 255;
	}

	return palette;
}
