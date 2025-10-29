#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "lodepng.h"

// Minimal CLI: create a simple gradient PNG using LodePNG
// Usage: ./alfredcli [out.png]

int extractAlfred1();
void extractAlfredAnims();
void extractAlfred3();
void extractAlfred4();
void extractAlfred5();
void extractAlfred6();
void extractAlfred7();
void extractAlfred9();

int main(int argc, char **argv) {
    // extractAlfred1();
    // extractAlfredAnims();
    // extractAlfred3();
    // extractAlfred4();
    extractAlfred5();
    extractAlfred6();
    // extractAlfred7();
    // extractAlfred9();
    // const char *out = "out.png";
    // if (argc > 1) out = argv[1];

    // const int width = 256;
    // const int height = 256;

    // // allocate image: 4 bytes per pixel (RGBA)
    // uint8_t *image = malloc(width * height * 4);
    // if (!image) {
    //     fprintf(stderr, "Out of memory\n");
    //     return 1;
    // }

    // // generate gradient pattern
    // for (int y = 0; y < height; ++y) {
    //     for (int x = 0; x < width; ++x) {
    //         uint8_t r = (uint8_t)x;
    //         uint8_t g = (uint8_t)y;
    //         uint8_t b = (uint8_t)((x + y) / 2);
    //         size_t idx = (y * width + x) * 4;
    //         image[idx + 0] = r;     // R
    //         image[idx + 1] = g;     // G
    //         image[idx + 2] = b;     // B
    //         image[idx + 3] = 255;   // A (fully opaque)
    //     }
    // }

    // // encode PNG to memory first
    // uint8_t *png = NULL;
    // size_t png_size = 0;
    // unsigned error = lodepng_encode32(&png, &png_size, image, width, height);
    // if (error) {
    //     fprintf(stderr, "PNG encoding error %u: %s\n", error, lodepng_error_text(error));
    //     free(image);
    //     return 2;
    // }

    // // write PNG to file
    // error = lodepng_save_file(png, png_size, out);
    // if (error) {
    //     fprintf(stderr, "Error saving to %s: %s\n", out, lodepng_error_text(error));
    //     free(png);
    //     free(image);
    //     return 3;
    // }

    // free(png);
    // free(image);
    // printf("Wrote %s (%dx%d)\n", out, width, height);
    return 0;
}
