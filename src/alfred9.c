
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "lodepng.h"
#include "functions.h"

int count = 0;
int written = 0;

unsigned int index9 = 0;
int w = 102;
int h = 51;
unsigned int offset;

int extractAlfred9()
{
    unsigned char *pic = (unsigned char *)malloc(640 * 480 * 600);

    // No Qt: use LodePNG to write output files

    // for (int jj=1;jj<50;jj++)
    //{

    // int jj=0;
    // w=130;
    // h=55;
    // offset=(60*51*102);
    // int nframes=18;

    /*
        int jj=0;
        w=51;
        h=102;
        offset=0;
        int nframes=60;
    */

    FILE *fp1 = fopen("files/ALFRED.9", "rb");

    fseek(fp1, 0L, SEEK_END);
    int size = ftell(fp1);
    fseek(fp1, 0L, SEEK_SET);

    unsigned char *bufferFile = (unsigned char *)malloc(size);
    fread(bufferFile, 1, size, fp1);

    unsigned int index = 0;
    int blok = 0;
    index = 0; // 0x00186dbc;//0x15c2c8;//0x14fa66;//578943;//0x6411d+1702;//0x6411d;//0x67389;//0x6411d;
    int iIndex = index;
    // bool nextBuda=false;
    int counter;

    while (index < size) // size)
    {

        // while (bufferFile[index]==0)
        //	index++;

        // if ((bufferFile[index]=='B') && (bufferFile[index+1]=='U') && (bufferFile[index+2]=='D') && (bufferFile[index+3]=='A'))
        {
            /*
            if (nextBuda==true)
            {

                counter--;
                if (counter==0)
                    break;
            }
            */
            /*
            index+=4;
            blok++;
            index2++;
            //if (blok==30)
            {

                break;
                blok=0;
                //index+=768;
                //nextBuda=true;
                counter=2;
            }
            */
        }
        // else
        {

            pic[index9] = bufferFile[index];
            index9++;
            index++;

            /*
            unsigned char count=bufferFile[index];
            unsigned char color=bufferFile[index+1];
            unsigned int k;
            for (k=index2;k<index2+count;k++)
                pic[k]=color;

            index2+=count;

            index+=2;
            */
        }
    }

    // int alto=(index2-iIndex)/640;
    unsigned int superancho, frame, sx, sy, total;
    w = 51;
    h = 102;
    offset = 0; //(60*51*102);
    int nframes = 11;
    total = w * h;



    // We'll export the first 8 rows x 640 columns as an indexed PNG using lodepng.
    const unsigned int img_w = 640;
    const unsigned int img_h = 8;
    size_t img_size = (size_t)img_w * img_h;
    unsigned char *image_data = (unsigned char *)malloc(img_size);
    if (!image_data) {
        fprintf(stderr, "Out of memory allocating image buffer\n");
        free(pic);
        free(bufferFile);
        return -1;
    }

    int index3 = 0;
    for (unsigned int y = 0; y < img_h; ++y) {
        for (unsigned int x = 0; x < img_w; ++x) {
            image_data[y * img_w + x] = pic[index3++];
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
        fprintf(stderr, "lodepng encode error: %s\n", lodepng_error_text(error));
    } else {
        const char *outname = "kk.png";
        error = lodepng_save_file(png, pngsize, outname);
        if (error) fprintf(stderr, "lodepng save error for %s: %s\n", outname, lodepng_error_text(error));
        else printf("Saved %s (%zu bytes)\n", outname, pngsize);
    }

    if (png) free(png);
    lodepng_state_cleanup(&state);
    free(image_data);
    if (palette) free(palette);
    free(pic);
    free(bufferFile);

    return 0;
}
