
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "lodepng.h"
#include "functions.h"

static int n;
// int count = 0;
// int written = 0;

// unsigned int index2 = 0;
// 212743

// int w = 51;
// int h = 102;
// unsigned int offset;

unsigned char getExtraCharacters(unsigned char t)
{
	unsigned char ex[] =
		{
			0x80, 0x82, 0x83, 0x7b, 0x7c, 0x7d, 0x7e, 0x7f, 0xc8, 0xad, 1, 2};
	unsigned char cex[] =
		{
			// '�', '�', '�', '�', '�', '�', '�', '�', ' ', '�', ' ', ' '
			0xE1, 0xE9, 0xED, 0xF3, 0xFA, 0xE1, 0xE1, 0xE1, ' ', 0xF1, ' ', ' '};

	unsigned char ret = t;
	for (int i = 0; i < 12; i++)
	{
		if (t == ex[i])
		{
			ret = cex[i];
			break;
		}
	}

	return ret;
}

void checkChar(unsigned char *buf2, int size)
{

	for (int i = 0; i < size; i++)
	{
		buf2[i] = getExtraCharacters(buf2[i]);
	}
}

int extractAlfred7()
{

	unsigned int index = 0x0031eb1e; // 0x00182a56;//0x00174aa0;//0x152a88;//0x922cb+176;//0x9392b;//

	unsigned char *pic = (unsigned char *)malloc(307200 * 100);

	int jj = 0;

	FILE *fp1 = fopen("files/ALFRED.7", "rb");

	fseek(fp1, 0L, SEEK_END);
	int size = ftell(fp1);
	fseek(fp1, 0L, SEEK_SET);

	unsigned char *bufferFile = (unsigned char *)malloc(size);
	fread(bufferFile, 1, size, fp1);

	unsigned char *buf2 = (unsigned char *)malloc(56);
	unsigned int lofsset = 199136;

	fseek(fp1, lofsset, 0);

	for (int l = 0; l < 126; l++)
	{

		memset(buf2, 0, 56);
		fread(buf2, 1, 55, fp1);
		checkChar(buf2, 56);
		printf("%s\n", buf2);

		memset(buf2, 0, 56);
		fread(buf2, 1, 30, fp1);
		checkChar(buf2, 56);
		printf("%s\n", buf2);

		memset(buf2, 0, 56);
		fread(buf2, 1, 23, fp1);
		checkChar(buf2, 56);
		printf("%s\n", buf2);

		l += 0;
	}

	// exit(0);

	int blok = 0;
	// index=0x1a9ee;
	unsigned int index2 = 0;
	int i = 0;
	int j = 0;

	int w = 100; //-202;//90-26;
	int h = 90;  //-42;//120-23;
	// offset=(60*51*102);
	int nframes = 3;

	unsigned int indexb = index;
	while (j < 90)
	{
		printf("%d", j);
	    // while (bufferFile[index]==0)
	    //	index++;

	    /*

	    while ((bufferFile[index2]!='B') || (bufferFile[index2+1]!='U') || (bufferFile[index2+2]!='D') || (bufferFile[index2+3]!='A'))
	        index2++;

	    unsigned int sizeBlock=(index2-index);

	    index2+=4;

	    printf("bloque = %d, size = %d\n",i,sizeBlock);
	    i++;
	    index=index2;

	    */

	    // if (j==8)
	    //{
	    //	index+=768;
	    // }

	    if ((bufferFile[index] == 'B') && (bufferFile[index + 1] == 'U') && (bufferFile[index + 2] == 'D') && (bufferFile[index + 3] == 'A'))
	    {

	        blok++;
	        if (blok == 1) // || (index2>=256000))
	        {

				{
					const unsigned int img_w = 640;
					const unsigned int img_h = 468;
					size_t img_size = (size_t)img_w * img_h;
					unsigned char *image_data = (unsigned char *)malloc(img_size);
					if (!image_data) {
						fprintf(stderr, "Out of memory allocating image buffer for frame %d\n", j);
					} else {
						int idx = 0;
						for (unsigned int y = 0; y < img_h; ++y) {
							for (unsigned int x = 0; x < img_w; ++x) {
								image_data[y * img_w + x] = pic[idx++];
							}
						}

						unsigned char *palette = getPalette();

						LodePNGState state;
						lodepng_state_init(&state);
						state.info_raw.colortype = LCT_PALETTE;
						state.info_raw.bitdepth = 8;
						state.info_png.color.colortype = LCT_PALETTE;
						state.info_png.color.bitdepth = 8;

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
						unsigned error = lodepng_encode(&png, &pngsize, image_data, img_w, img_h, &state);
						if (error) {
							fprintf(stderr, "lodepng encode error for frame %d: %s\n", j, lodepng_error_text(error));
						} else {
							char outname[256];
							snprintf(outname, sizeof(outname), "output/7/kk%d.png", j);
							error = lodepng_save_file(png, pngsize, outname);
							if (error) fprintf(stderr, "lodepng save error for %s: %s\n", outname, lodepng_error_text(error));
							else printf("Saved %s (%zu bytes)\n", outname, pngsize);
						}

						if (png) free(png);
						lodepng_state_cleanup(&state);
						free(image_data);
						if (palette) free(palette);
					}

					index2 = 0;
					memset(pic, 0, 307200 * 100);
					j++;
				}
	        }
	        else
	            index2++;

	        index += 4;

	        // index2=((blok)*(32768));

	        // index=indexb;
	        // index2=0;
	        // w-=1;
	        // h-=1;
	    }
	    else
	    {

	        pic[index2] = bufferFile[index];
	        index2++;
	        index++;

	        /*
	        unsigned char count=bufferFile[index];
	        unsigned char color=bufferFile[index+1];
	        unsigned int k;
	        for (k=index2;k<index2+count;k++)
	            pic[k]=color;

	        pic[k]=(unsigned char)color;

	        index2+=count;
	        index+=2;
	        */
	    }
	}

	exit(0);
}
