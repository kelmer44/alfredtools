#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "lodepng.h"
#include "functions.h"

#define SCREEN_WIDTH 640
#define SCREEN_HEIGHT 400
#define HEADER_SIZE 0x180
#define MAX_RLE_BUFFER (SCREEN_WIDTH * SCREEN_HEIGHT)

#pragma pack(push, 1)  // Ensure structures are packed without padding
typedef struct {
    uint16_t num_images;    // Number of background images (should be 56)
    uint16_t reserved1;     // Reserved/unknown
    uint32_t offset_table;  // Offset to the table of image offsets
    uint8_t reserved2[0x178]; // Rest of header
} FileHeader;

typedef struct {
    uint32_t size;       // Size of compressed data
    uint16_t width;      // Should be 640
    uint16_t height;     // Should be 400
    uint16_t type;       // Image type/flags
    uint16_t reserved;   // Reserved/padding
} ImageHeader;
#pragma pack(pop)

int extractAlfred1() {
    FILE *fp = fopen("files/ALFRED.1", "rb");
    if (!fp) {
        fprintf(stderr, "Could not open ALFRED.1\n");
        return 1;
    }

    // Read file header
    FileHeader header;
    if (fread(&header, sizeof(FileHeader), 1, fp) != 1) {
        fprintf(stderr, "Failed to read file header\n");
        fclose(fp);
        return 1;
    }

    printf("File info:\n");
    printf("Number of images: %d\n", header.num_images);
    printf("Offset table at: %08X\n", header.offset_table);

    if (header.num_images != 56) {
        fprintf(stderr, "Warning: Expected 56 images, found %d\n", header.num_images);
    }

    // Read offset table
    uint32_t *offsets = malloc(header.num_images * sizeof(uint32_t));
    if (!offsets) {
        fprintf(stderr, "Failed to allocate offset table\n");
        fclose(fp);
        return 1;
    }

    fseek(fp, header.offset_table, SEEK_SET);
    if (fread(offsets, sizeof(uint32_t), header.num_images, fp) != header.num_images) {
        fprintf(stderr, "Failed to read offset table\n");
        free(offsets);
        fclose(fp);
        return 1;
    }

    // Process each image
    for (uint32_t i = 0; i < header.num_images; i++) {
        printf("\nProcessing image %d/%d at offset %08X\n", i + 1, header.num_images, offsets[i]);

        // Seek to image header
        fseek(fp, offsets[i], SEEK_SET);

        ImageHeader imgHeader;
        if (fread(&imgHeader, sizeof(ImageHeader), 1, fp) != 1) {
            fprintf(stderr, "Failed to read image header\n");
            continue;
        }        printf("Size: %d bytes\n", imgHeader.size);
        printf("Type: %04X\n", imgHeader.type);
        printf("Dimensions: %dx%d\n", imgHeader.width, imgHeader.height);

        // Verify dimensions
        if (imgHeader.width != SCREEN_WIDTH || imgHeader.height != SCREEN_HEIGHT) {
            fprintf(stderr, "Warning: Image %d has unexpected dimensions: %dx%d\n",
                    i, imgHeader.width, imgHeader.height);
            continue;
        }

        // Read the compressed data
        uint8_t *compData = malloc(imgHeader.size);
        if (!compData) {
            fprintf(stderr, "Failed to allocate compressed buffer\n");
            continue;
        }

        if (fread(compData, imgHeader.size, 1, fp) != 1) {
            fprintf(stderr, "Failed to read compressed data\n");
            free(compData);
            continue;
        }

        // Allocate decompression buffer
        uint8_t *data = malloc(SCREEN_WIDTH * SCREEN_HEIGHT);
        if (!data) {
            fprintf(stderr, "Failed to allocate decompression buffer\n");
            free(compData);
            continue;
        }

        // Print first few bytes to understand the compression
        printf("First bytes: %02X %02X %02X %02X %02X %02X %02X %02X\n",
               compData[0], compData[1], compData[2], compData[3],
               compData[4], compData[5], compData[6], compData[7]);

        // Try alternative RLE decompression
        int decompSize = 0;
        int compIndex = 0;

        while (compIndex < imgHeader.size && decompSize < SCREEN_WIDTH * SCREEN_HEIGHT) {
            if (compIndex + 1 >= imgHeader.size) break;

            uint8_t count = compData[compIndex++];

            if (count == 0) { // Special case - could be end marker or length byte
                continue;
            }

            if (count & 0x80) { // Run of same pixel
                count &= 0x7F;
                if (compIndex >= imgHeader.size) break;
                uint8_t pixel = compData[compIndex++];

                for (int j = 0; j < count && decompSize < SCREEN_WIDTH * SCREEN_HEIGHT; j++) {
                    data[decompSize++] = pixel;
                }
            } else { // Literal sequence of pixels
                for (int j = 0; j < count && decompSize < SCREEN_WIDTH * SCREEN_HEIGHT; j++) {
                    if (compIndex >= imgHeader.size) break;
                    data[decompSize++] = compData[compIndex++];
                }
            }
        }

        printf("Decompressed size: %d bytes (expected %d)\n",
               decompSize, SCREEN_WIDTH * SCREEN_HEIGHT);

        // Convert to RGBA
        uint8_t *rgbaData = malloc(SCREEN_WIDTH * SCREEN_HEIGHT * 4);
        if (!rgbaData) {
            fprintf(stderr, "Failed to allocate RGBA buffer\n");
            free(data);
            free(compData);
            continue;
        }

        // Get the default VGA palette
        unsigned char *palette = getPalette();
        if (!palette) {
            fprintf(stderr, "Failed to get palette\n");
            free(rgbaData);
            free(data);
            free(compData);
            continue;
        }

        // Convert indexed color to RGBA
        if (decompSize >= SCREEN_WIDTH * SCREEN_HEIGHT) {
            for (int p = 0; p < SCREEN_WIDTH * SCREEN_HEIGHT; p++) {
                uint8_t index = data[p];
                rgbaData[p * 4 + 0] = palette[index * 4 + 0];
                rgbaData[p * 4 + 1] = palette[index * 4 + 1];
                rgbaData[p * 4 + 2] = palette[index * 4 + 2];
                rgbaData[p * 4 + 3] = 255;
            }

            // Save as PNG
            char filename[256];
            snprintf(filename, sizeof(filename), "output/1/background_%02d.png", i);
            unsigned error = lodepng_encode32_file(filename, rgbaData, SCREEN_WIDTH, SCREEN_HEIGHT);
            if (error) {
                fprintf(stderr, "PNG encoding error %u: %s\n", error, lodepng_error_text(error));
            } else {
                printf("Saved %s\n", filename);
            }
        } else {
            printf("Warning: Decompressed size (%d) smaller than expected (%d)\n",
                   decompSize, SCREEN_WIDTH * SCREEN_HEIGHT);
        }

        free(palette);
        free(rgbaData);
        free(data);
        free(compData);
    }

    free(offsets);
    fclose(fp);
    return 0;
}
