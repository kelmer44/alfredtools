#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include "lodepng.h"
#include "functions.h"

int extractAlfred5()
{
    unsigned char *palette = getPalette();

    unsigned char *finalbuffer = (unsigned char *)malloc(10000 * 10000 * 4);
    // QCoreApplication a(argc, argv);

    FILE *fp1 = fopen("files/ALFRED.5", "rb");

    fseek(fp1, 0L, SEEK_END);
    int size = ftell(fp1);
    fseek(fp1, 0L, SEEK_SET);

    unsigned char *bufferFile = (unsigned char *)malloc(size);
    fread(bufferFile, 1, size, fp1);
    fclose(fp1);

    // Decode and export each entry using lodepng
    for (int j = 0; j < 55; ++j)
    {
        unsigned int offset = bufferFile[j * 6] + (bufferFile[(j * 6) + 1] * 256) + (bufferFile[(j * 6) + 2] * 65536);
        unsigned int ww = 640; // as in original comment
        unsigned int hh = 400; // as in original comment
        unsigned int start = offset;
        unsigned int off = 0;

        // find end marker and expand RLE pairs into finalbuffer
        while (offset < (unsigned)size)
        {
            if (offset + 3 < (unsigned)size && bufferFile[offset] == 'B' && bufferFile[offset + 1] == 'U' && bufferFile[offset + 2] == 'D' && bufferFile[offset + 3] == 'A')
            {
                unsigned char count;
                unsigned char color;
                for (unsigned int k = start; k + 1 < offset; k += 2)
                {
                    count = bufferFile[k];
                    color = bufferFile[k + 1];
                    if (off + count <= 10000u * 10000u * 4u) {
                        memset(&finalbuffer[off], color, count);
                    }
                    off += count;
                }
                break;
            }
            offset++;
        }

        // Build indexed image buffer
        size_t img_size = (size_t)ww * (size_t)hh;
        unsigned char *image_data = (unsigned char *)malloc(img_size);
        if (!image_data) {
            fprintf(stderr, "Out of memory allocating image buffer for entry %d\n", j);
            continue;
        }
        // Copy pixels from finalbuffer into image_data
        for (unsigned int y = 0; y < hh; ++y)
        {
            for (unsigned int x = 0; x < ww; ++x)
            {
                unsigned int idx = (y * ww) + x;
                if (idx < off)
                    image_data[y * ww + x] = finalbuffer[idx];
                else
                    image_data[y * ww + x] = 0;
            }
        }

        // Setup LodePNG state for palette encoding
        LodePNGState state;
        lodepng_state_init(&state);
        state.info_raw.colortype = LCT_PALETTE;
        state.info_raw.bitdepth = 8;
        state.info_png.color.colortype = LCT_PALETTE;
        state.info_png.color.bitdepth = 8;

        // Fill palette (getPalette returns 256*4 RGBA bytes)
        for (int p = 0; p < 256; ++p)
        {
            unsigned char r = palette[p * 4 + 0];
            unsigned char g = palette[p * 4 + 1];
            unsigned char b = palette[p * 4 + 2];
            unsigned char a = palette[p * 4 + 3];
            lodepng_palette_add(&state.info_png.color, r, g, b, a);
            lodepng_palette_add(&state.info_raw, r, g, b, a);
        }

        // Encode
        unsigned char *png = NULL;
        size_t pngsize = 0;
        unsigned error = lodepng_encode(&png, &pngsize, image_data, ww, hh, &state);
        if (error) {
            fprintf(stderr, "lodepng encode error for entry %d: %s\n", j, lodepng_error_text(error));
        } else {
            char outname[256];
            snprintf(outname, sizeof(outname), "output/5/shadows_%02d.png", j);
            error = lodepng_save_file(png, pngsize, outname);
            if (error) fprintf(stderr, "lodepng save error for %s: %s\n", outname, lodepng_error_text(error));
            else printf("Saved %s (%zu bytes)\n", outname, pngsize);
        }

        if (png) free(png);
        lodepng_state_cleanup(&state);
        free(image_data);
    }

    exit(0);
}
