#include <stdio.h>
#include <stdlib.h>
#include "lodepng.h"

int index2=0;
unsigned char *pic;

unsigned char *getPalette() {

	// Prepare a simple 256-color palette (RGBA). Replace with real palette when available.
	unsigned char *palette = (unsigned char *)malloc(256 * 4);
	if (!palette) {
		fprintf(stderr, "saveAnim: out of memory allocating palette\n");
		return NULL;
	}
	for (int i = 0; i < 256; ++i) {
		palette[i * 4 + 0] = (unsigned char)i; // R
		palette[i * 4 + 1] = (unsigned char)i; // G
		palette[i * 4 + 2] = (unsigned char)i; // B
		palette[i * 4 + 3] = 255;              // A
	}
}

void saveAnim(unsigned char *bufferFile, int indexCab, unsigned int offset, char extra)
{

	int w = bufferFile[0];
	int h = bufferFile[1];
	int n = bufferFile[4];

	if ((w == 0) || (h == 0) || (n == 0))
		return;

        // QImage *image=new QImage(w*n,h,QImage::Format_Indexed8);

		// int p=indexCab/55;
		// int p2=(p*13)+11;
		// memset(bufpal,0,3);
		// itoa(p2,bufpal,10);

	unsigned superwidth = (unsigned)(w * n);
	unsigned height = (unsigned)h;
	unsigned total = (unsigned)(w * h);

	unsigned char *indices = (unsigned char *)malloc((size_t)superwidth * height);
	if (!indices) {
		fprintf(stderr, "saveAnim: out of memory allocating indices\n");
		return;
	}

	// Fill indices from global pic buffer using the same layout as the original code
	for (unsigned y = 0; y < height; ++y) {
		for (unsigned x = 0; x < superwidth; ++x) {
			unsigned frame = x / (unsigned)w;
			unsigned sx = x - frame * (unsigned)w;
			unsigned idx = (unsigned)offset + (frame * total) + (y * (unsigned)w) + sx;
			indices[y * superwidth + x] = pic[idx];
		}
	}

    unsigned char *palette = getPalette();
    if(palette == NULL) {
        free(palette);
        free(indices);
        return;
    }

	// Setup LodePNG state for palette encoding
	LodePNGState state;
	lodepng_state_init(&state);
	state.info_raw.colortype = LCT_PALETTE;
	state.info_raw.bitdepth = 8;
	state.info_png.color.colortype = LCT_PALETTE;
	state.info_png.color.bitdepth = 8;

	state.info_png.color.palettesize = 256;
	state.info_png.color.palette = (unsigned char *)malloc(256 * 4);
	if (!state.info_png.color.palette) {
		fprintf(stderr, "saveAnim: out of memory allocating state palette\n");
		lodepng_state_cleanup(&state);
		free(palette);
		free(indices);
		return;
	}
	memcpy(state.info_png.color.palette, palette, 256 * 4);
    // state.info_png.color.palette = palette;
    for ( int i = 0; i< 768; i++){
        lodepng_palette_add(
            &state.info_png.color,
            palette[i * 4 + 0],
            palette[i * 4 + 1],
            palette[i * 4 + 2],
            palette[i * 4 + 3]
        );
        lodepng_palette_add(
            &state.info_raw,
            palette[i * 4 + 0],
            palette[i * 4 + 1],
            palette[i * 4 + 2],
            palette[i * 4 + 3]
        );
    }

	unsigned char *png = NULL;
	size_t pngsize = 0;
	unsigned error = lodepng_encode(&png, &pngsize, indices, superwidth, height, &state);
	if (error) {
		fprintf(stderr, "saveAnim: lodepng_encode error %u: %s\n", error, lodepng_error_text(error));
	} else {
		// Build a filename (placeholder) — you may want to customize naming
		char filename[128];
		snprintf(filename, sizeof(filename), "anim_%d_%c.png", indexCab, extra ? extra : '0');
		lodepng_save_file(png, pngsize, filename);
	}

	// cleanup
	lodepng_state_cleanup(&state);
	// free(palette);
	free(indices);
	if (png) free(png);


    // -------------------------------------------------

		// int p=indexCab/55;
		// int p2=(p*13)+11;
		// memset(bufpal,0,3);
		// itoa(p2,bufpal,10);

		// memcpy(&paleta[69],&bufpal[0],3);

		// FILE *fp2=fopen(paleta,"rb");
		// unsigned char *bufferPaleta=(unsigned char *)malloc(768);
		// fread(bufferPaleta, 1, 768, fp2);
		// fclose(fp2);

		// ctable=new QVector<QRgb>;

		// unsigned int c, a,r,g,b;
		// for(int i = 0; i < 256; ++i)
		// {
		// 	a=0xFF000000;
		// 	r=bufferPaleta[i*3] *2;
		// 	g=bufferPaleta[(i*3) + 1] *2;
		// 	b=bufferPaleta[(i*3) + 2] *2;
		// 	c=a | (r<<16) | (g<<8) | b;
		// 	ctable->append(c);
		// }

		// image->setColorCount(256);
		// image->setColorTable(*ctable);

		// memset(bufpan,0,3);
		// itoa(p,bufpan,10);

		// bool kk;
		// int index3=0;
		// unsigned int superancho,frame,sx,sy,total;
		// total=w*h;
		// superancho=w*n;
		// for (int y=0;y<h;y++)
		// {
		// 	for (int x=0;x<superancho;x++)
		// 	{
		// 		frame=x/w;
		// 		sy=y;
		// 		sx=x-(frame*w);
		// 		image->setPixel(x,y,pic[offset+(frame*total)+(sy*w)+sx]);
		// 	}
		// }

		// QString pp("C:/proyectos/test2/debug/talking");//.png");
		// pp.append(bufpan);
		// if (extra!=NULL)
		// 	pp.append(extra);

		// pp.append(".png");

		// kk=image->save(pp,"PNG");
}

int extractAlfredAnims()
{
    char *name = "./files/alfred.2";
    pic = (unsigned char *)malloc(10000*10000*4);
    FILE *fp1 = fopen(name, "rb");

    if (fp1 == NULL)
    {
        printf("failed to fopen %s\n", name);
        return -1;
    }

    fseek(fp1, 0L, SEEK_END);
    int size = ftell(fp1);
    fseek(fp1, 0L, SEEK_SET);

    unsigned char *bufferFile = (unsigned char *)malloc(size);
    fread(bufferFile, 1, size, fp1);

    int indexCab = 0;
    unsigned int index = 0;

    index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256);
    while (index == 0)
    {
        indexCab += 55;
        index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256);
    }

    while (index < size)
    {

        if ((bufferFile[index] == 'B') && (bufferFile[index + 1] == 'U') && (bufferFile[index + 2] == 'D') && (bufferFile[index + 3] == 'A'))
        {

            saveAnim(&bufferFile[indexCab + 9], indexCab, 0, 'a');
            saveAnim(&bufferFile[indexCab + 21], indexCab, bufferFile[indexCab + 9] * bufferFile[indexCab + 10] * bufferFile[indexCab + 13], 'b');

            memset(pic, 0, 72 * 10000 * 4);

            index2 = 0;
            indexCab += 55;

            index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256) + (bufferFile[indexCab + 2] * 65536);
            while (index == 0)
            {
                indexCab += 55;
                index = bufferFile[indexCab] + (bufferFile[indexCab + 1] * 256) + (bufferFile[indexCab + 2] * 65536);
            }
        }
        else
        {
            unsigned char count = bufferFile[index];
            unsigned char color = bufferFile[index + 1];
            int k;
            for (k = index2; k < index2 + count; k++)
                pic[k] = color;

            pic[k] = (unsigned char)color;

            index2 += count;
            index += 2;
        }
    }

    exit(0);
}
