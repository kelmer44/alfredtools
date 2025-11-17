#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "lodepng.h"
#include "functions.h"

int tablapaletas[140]=
{
	0,0,0,0,0,0,0,
	2,2,
	3,3,3,3,3,3,3,3,
	4,4,4,4,4,
	5,5,
	7,
	8,8,
	9,9,9,9,9,
	12,12,
	13,13,13,
	12,
	15,15,15,15,15,15,15,15,15,15,15,15,
	16,16,
	17,17,
	19,19,19,19,19,

	0,0,0,0,0,0,0,
	33,33,

	29,29,
	0,0,0,

	34,35,31,25,
	31,
	32,
	21,25,
	0,
	0,0,0,0,0,
	4,4,4,4,
	0,0,0,0,
	0,0,0,0,0,0,
	33,33,
	47,47,
	52,52,52,52,52,
	52,52,52,52,52,52,
	41,
	0,
	30,
	44,44,44,44,
	31,
	46,46,
	31,
	51,52,53,54,

};

int extractAlfred6()
{
    unsigned char *finalbuffer=(unsigned char *)malloc(10000*10000*4);

	FILE *fp1=fopen("files/ALFRED.6","rb");


	fseek(fp1, 0L, SEEK_END);
	int size = ftell(fp1);
	fseek(fp1, 0L, SEEK_SET);

	unsigned char *bufferFile=(unsigned char *)malloc(size);
	fread(finalbuffer, 1, size, fp1);


/*
	FILE *fp2=fopen(paleta,"rb");
	unsigned char *bufferPaleta=(unsigned char *)malloc(768);


	fread(bufferPaleta, 1, 768, fp2);
	fclose(fp2);

	ctable=new QVector<QRgb>;

	unsigned int cc, aa,rr,gg,bb;
	for(int i = 0; i < 256; ++i)
	{
		aa=0xFF000000;
		rr=bufferPaleta[i*3] *2;
		gg=bufferPaleta[(i*3) + 1] *2;
		bb=bufferPaleta[(i*3) + 2] *2;
		cc=aa | (rr<<16) | (gg<<8) | bb;
		ctable->append(cc);
	}
*/



		unsigned int offset=0;
		unsigned int index=0;
		unsigned int ww;
		unsigned int hh;
		unsigned int xx;
		unsigned int yy;
		unsigned int start;
		unsigned int off=0;
		unsigned char count, color;
		char buf[3];

		int j=0;
		offset=0;//223875;//214743;//0x4376;
		//j=62;
		for (;;)
		{
			if (j==37)
				offset=0x1b8c4;
			if (j==67)
				offset=0x3f813;
			if (j==68)
				offset=0x4115d;
			if (j==88)
				offset=0x58969;


		xx=finalbuffer[offset+0]+(finalbuffer[offset+1]*256);
		yy=finalbuffer[offset+2]+(finalbuffer[offset+3]*256);
		ww=finalbuffer[offset+4];
		hh=finalbuffer[offset+5];



		if ((ww>0) && (hh>0))
		{

			// Get room number from tablapaletas array
			int room_num = 0;
			if (j < 140) {
				room_num = tablapaletas[j];
			}

			// Get palette for this room
			unsigned char *palette = getRoomPalette(room_num);
			if (!palette) {
				fprintf(stderr, "Failed to get palette for pegatina %d (room %d)\n", j, room_num);
				j++;
				continue;
			}

			size_t img_size = (size_t)ww * (size_t)hh;
			unsigned char *image_data = (unsigned char*)malloc(img_size);
			if (!image_data) {
				fprintf(stderr, "Out of memory allocating image buffer for pegatina %d\n", j);
				free(palette);
			} else {
				for (unsigned int y = 0; y < hh; ++y) {
					for (unsigned int x = 0; x < ww; ++x) {
						unsigned int src = offset + 6 + (y * ww) + x;
						unsigned int dst = y * ww + x;
						if (src < (unsigned)size) image_data[dst] = finalbuffer[src];
						else image_data[dst] = 0;
					}
				}

				// Prepare lodepng state for indexed palette PNG
				LodePNGState state;
				lodepng_state_init(&state);
				state.info_raw.colortype = LCT_PALETTE;
				state.info_raw.bitdepth = 8;
				state.info_png.color.colortype = LCT_PALETTE;
				state.info_png.color.bitdepth = 8;

				// Fill palette (expecting 256*4 RGBA bytes)
				if (palette) {
					for (int p = 0; p < 256; ++p) {
						unsigned char r = palette[p*4 + 0];
						unsigned char g = palette[p*4 + 1];
						unsigned char b = palette[p*4 + 2];
						unsigned char a = palette[p*4 + 3];
						lodepng_palette_add(&state.info_png.color, r, g, b, a);
						lodepng_palette_add(&state.info_raw, r, g, b, a);
					}
				}

				unsigned char *png = NULL;
				size_t pngsize = 0;
				unsigned error = lodepng_encode(&png, &pngsize, image_data, ww, hh, &state);
				if (error) {
					fprintf(stderr, "lodepng encode error for pegatina %d: %s\n", j, lodepng_error_text(error));
				} else {
					char outname[256];
					snprintf(outname, sizeof(outname), "output/6/pegatina%02d.png", j);
					error = lodepng_save_file(png, pngsize, outname);
					if (error) fprintf(stderr, "lodepng save error for %s: %s\n", outname, lodepng_error_text(error));
					else printf("Saved %s (%zu bytes) [room %d]\n", outname, pngsize, room_num);
				}

				// write metadata txt file
				char txtname[256];
				snprintf(txtname, sizeof(txtname), "output/6/pegatina%02d.txt", j);
				FILE *tf = fopen(txtname, "w");
				if (tf) {
					fprintf(tf, "x=%u\n", xx);
					fprintf(tf, "y=%u\n", yy);
					fprintf(tf, "width=%u\n", ww);
					fprintf(tf, "height=%u\n", hh);
					fprintf(tf, "room=%d\n", room_num);
					fclose(tf);
				}

				if (png) free(png);
				lodepng_state_cleanup(&state);
				free(image_data);
			}

			if (palette) free(palette);

			j++;
		}
		//else
		//	offset+=1;


			offset+=(ww*hh)+6;//+6+ww;
			if (j<6)
			{
			while (finalbuffer[offset]!=0xbf)
				offset++;
			}
			while (finalbuffer[offset]==0xbf)
				offset++;


			if (offset>=size)
				break;

		}


	exit(0);


}
