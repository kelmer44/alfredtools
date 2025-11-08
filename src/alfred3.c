#include <stdio.h>
#include <stdlib.h>
#include "lodepng.h"
#include "functions.h"

int index3 = 0;

int nFrames[] = {60, 18, 25, 10, 1, 1,1 ,1 , 1,1, 1 , 1,1};
int dimensions[10][2] =
    {
        {51, 102},
        {130, 55},
        {51, 100},
        {51, 100},
        {51, 100},
        {51, 100},
        {51, 100},
        {51, 100},
        {51, 100},
        {51, 100},
};

int extractAlfred3()
{
    int bytesWritten = 0;
    int jj = 0;
    int w = 0;
    int h = 0;
    int offset = 0;
    int nframes = 0;

    int maxAnim = 3;

    char *name = "./files/ALFRED.3";

    FILE *fp1 = fopen(name, "rb");

    if (fp1 == NULL)
    {
        printf("failed to fopen %s\n", name);
        return -1;
    }

    fseek(fp1, 0L, SEEK_END);
    int size = ftell(fp1);
    printf("File size = %d\n", size);
    fseek(fp1, 0L, SEEK_SET);

    unsigned char *bufferFile = (unsigned char *)malloc(size);
    fread(bufferFile, 1, size, fp1);
    int picSize = 10000 * 10000 * 4;
    unsigned char *pic = (unsigned char *)malloc(picSize);

    unsigned int index = 0;
    while (index < (unsigned int)size)
    {
        if ((bufferFile[index] == 'B') && (bufferFile[index + 1] == 'U') && (bufferFile[index + 2] == 'D') && (bufferFile[index + 3] == 'A'))
        {
            printf("found buda");
            break;
        }
        else
        {
            printf("index = %d\n", index);
            unsigned char count = bufferFile[index];
            unsigned char color = bufferFile[index + 1];
            unsigned int k;
            for (k = index3; k < index3 + count; k++)
                pic[k] = color;

            pic[k] = (unsigned char)color;

            index3 += count;
            index += 2;
        }
    }

    printf("pic size =  %d,  index3 = %d, file size = %d\n", picSize, index3, size);

    unsigned char *palette = getPalette();

    for (int jj = 0; jj < 3; jj++)
    {
        // int jj=0;
        // int w=51;
        // int h=102;
        // int offset=0;
        // int nframes=60;

        //  jj = 1;
        //  w = 130;
        //  h = 55;
        //  offset = (60 * 51 * 102);
        //  nframes = 18;


        w = dimensions[jj][0];
        h = dimensions[jj][1];
        nframes = nFrames[jj];

        offset += jj == 0 ? 0 : nFrames[jj - 1] * dimensions[jj - 1][0] * dimensions[jj - 1][1];
        printf("frame=%d, w=%d, h=%d, nframes=%d, offset = %d * %d * %d = %d\n", jj, w, h, nframes, nFrames[jj - 1], dimensions[jj - 1][0], dimensions[jj - 1][1], offset);

        (void)index;

        // Setup LodePNG state for palette encoding
        LodePNGState state;
        lodepng_state_init(&state);
        state.info_raw.colortype = LCT_PALETTE;
        state.info_raw.bitdepth = 8;
        state.info_png.color.colortype = LCT_PALETTE;
        state.info_png.color.bitdepth = 8;

        state.info_png.color.palettesize = 256;
        state.info_png.color.palette = (unsigned char *)malloc(256 * 4);
        if (!state.info_png.color.palette)
        {
            fprintf(stderr, "saveAnim: out of memory allocating state palette\n");
            lodepng_state_cleanup(&state);
            free(palette);
            return -1;
        }
        memcpy(state.info_png.color.palette, palette, 256 * 4);
        state.info_png.color.palette = palette;
        for (int i = 0; i < 256; ++i)
        {
            lodepng_palette_add(&state.info_png.color,
                                palette[i * 4 + 0],
                                palette[i * 4 + 1],
                                palette[i * 4 + 2],
                                palette[i * 4 + 3]);
            lodepng_palette_add(&state.info_raw,
                                palette[i * 4 + 0],
                                palette[i * 4 + 1],
                                palette[i * 4 + 2],
                                palette[i * 4 + 3]);
        }

        // Prepare output image buffer for all frames
        unsigned char *image_data = (unsigned char *)malloc(w * nframes * h);
        if (!image_data)
        {
            fprintf(stderr, "Failed to allocate memory for image data\n");
            lodepng_state_cleanup(&state);
            free(palette);
            return -1;
        }

        // Copy frame data to image buffer
        unsigned int total = w * h;
        for (int frame = 0; frame < nframes; frame++)
        {
            for (int y = 0; y < h; y++)
            {
                for (int x = 0; x < w; x++)
                {
                    // Calculate source and destination positions
                    unsigned int src_pos = offset + (frame * total) + (y * w) + x;
                    unsigned int dst_pos = y * (w * nframes) + (frame * w) + x;
                    image_data[dst_pos] = pic[src_pos];
                }
            }
        }


        // Generate output filename
        char filename[256];
        snprintf(filename, sizeof(filename), "output/3/frame_%d.png", jj);

        // Encode and save the PNG
        unsigned char *png_data = NULL;
        size_t png_size = 0;
        unsigned error = lodepng_encode(&png_data, &png_size, image_data, w * nframes, h, &state);

        if (error)
        {
            fprintf(stderr, "PNG encoding error %u: %s\n", error, lodepng_error_text(error));
        }
        else
        {
            // Save the PNG file
            error = lodepng_save_file(png_data, png_size, filename);
            if (error)
            {
                fprintf(stderr, "PNG save error %u: %s\n", error, lodepng_error_text(error));
            }
        }

        // Cleanup
        free(image_data);
        if (png_data)
            free(png_data);
    }
    return 0;
}
