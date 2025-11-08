
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "lodepng.h"
#include "functions.h"

unsigned int index4=0;

int extractAlfred4()
{
    unsigned char *palette = getPalette();

    unsigned char *finalbuffer=(unsigned char *)malloc(10000*10000*4);
    unsigned char *workingbuffer=(unsigned char *)malloc(10000*10000*4);

	// Read input file
	FILE *fp1 = fopen("files/ALFRED.4", "rb");
	if (!fp1) {
		fprintf(stderr, "Failed to open input file %s\n", "files/ALFRED.4");
		exit(1);
	}
	fseek(fp1, 0L, SEEK_END);
	int size = ftell(fp1);
	fseek(fp1, 0L, SEEK_SET);
	unsigned char *bufferFile=(unsigned char *)malloc(size);
	if (!bufferFile) {
		fprintf(stderr, "Out of memory reading input file\n");
		fclose(fp1);
		exit(1);
	}
	fread(bufferFile, 1, size, fp1);
	fclose(fp1);

	// Decompress run-length data (same logic as original commented code)
	unsigned int indexWorkingBuffer=0;
	unsigned int indexFile=0;
	unsigned int off=0;
	unsigned int supercount=0;

	while (indexFile < (unsigned)size)
	{
		workingbuffer[indexWorkingBuffer]=bufferFile[indexFile];
		indexWorkingBuffer++;
		indexFile++;
		supercount++;

		if (indexFile + 4 <= (unsigned)size &&
			bufferFile[indexFile]=='B' && bufferFile[indexFile+1]=='U' && bufferFile[indexFile+2]=='D' && bufferFile[indexFile+3]=='A')
		{
			unsigned char count;
			unsigned char color;
			unsigned int k;

			for (k=0;k<indexWorkingBuffer-1;k+=2)
			{
				count=workingbuffer[k];
				color=workingbuffer[k+1];
				memset(&finalbuffer[off],color,count);
				off+=count;
			}

			supercount=0;
			indexWorkingBuffer=0;
			indexFile+=4; // skip B U D A
		}
		else if (indexFile>= (unsigned)size)
		{
			memcpy(&finalbuffer[off],&workingbuffer[0],supercount);
			off+=supercount;
			supercount=0;
			indexWorkingBuffer=0;
		}
	}

	// Parameters used in the original commented code
	const unsigned int frame_w = 60;
	const unsigned int frame_h = 60;
	const unsigned int nframes = 69; // 60*69 used in original
	const unsigned int img_w = frame_w * nframes;
	const unsigned int img_h = frame_h;
	const unsigned int total = frame_w * frame_h;
	const unsigned int data_start_offset = 212979; // preserved from original example

	// Build indexed image data (one byte per pixel, indexed into palette)
	unsigned char *image_data = (unsigned char*)malloc(img_w * img_h);
	if (!image_data) {
		fprintf(stderr, "Out of memory allocating image buffer\n");
		free(bufferFile);
		free(finalbuffer);
		free(workingbuffer);
		exit(1);
	}

	for (unsigned int y=0; y<img_h; ++y) {
		for (unsigned int x=0; x<img_w; ++x) {
			unsigned int frame = x / frame_w;
			unsigned int sx = x - (frame * frame_w);
			unsigned int sy = y;
			unsigned int src_index = data_start_offset + (frame * total) + (sy * frame_w) + sx;
			if (src_index < off) {
				image_data[y * img_w + x] = finalbuffer[src_index];
			} else {
				image_data[y * img_w + x] = 0; // fallback
			}
		}
	}

	// Setup LodePNG state for palette encoding
	LodePNGState state;
	lodepng_state_init(&state);
	state.info_raw.colortype = LCT_PALETTE;
	state.info_raw.bitdepth = 8;
	state.info_png.color.colortype = LCT_PALETTE;
	state.info_png.color.bitdepth = 8;

	// Fill lodepng palette from palette returned by getPalette()
	// getPalette() is expected to return 256*4 bytes (RGBA)
	for (int i = 0; i < 256; ++i) {
		unsigned char r = palette[i*4 + 0];
		unsigned char g = palette[i*4 + 1];
		unsigned char b = palette[i*4 + 2];
		unsigned char a = palette[i*4 + 3];
		lodepng_palette_add(&state.info_png.color, r, g, b, a);
		lodepng_palette_add(&state.info_raw, r, g, b, a);
	}

	// Encode and save PNG
	unsigned char* png_data = NULL;
	size_t png_size = 0;
	unsigned error = lodepng_encode(&png_data, &png_size, image_data, img_w, img_h, &state);
	if (error) {
		fprintf(stderr, "PNG encoding error %u: %s\n", error, lodepng_error_text(error));
	} else {
		const char *outname = "output/4/alfred4.png";
		error = lodepng_save_file(png_data, png_size, outname);
		if (error) fprintf(stderr, "PNG save error %u: %s\n", error, lodepng_error_text(error));
		else printf("Saved %s (%zu bytes)\n", outname, png_size);
	}

	// Cleanup
	if (png_data) free(png_data);
	lodepng_state_cleanup(&state);
	free(image_data);
	free(bufferFile);
	free(finalbuffer);
	free(workingbuffer);
	free(palette);
	return 0;
}
