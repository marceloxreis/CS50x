#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file %s\n", argv[1]);
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    FILE *img = NULL;
    int file_number = 0;
    char filename[12]; // Buffer to hold the filename

    // While there's still data left to read from the memory card
    while (fread(buffer, sizeof(uint8_t), 512, card) == 512)
    {
        // Check if this block is the start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // Close the previous JPEG file (if any)
            if (img != NULL)
            {
                fclose(img);
            }

            // Create a new filename (e.g., 001.jpg, 002.jpg, etc.)
            sprintf(filename, "%03d.jpg", file_number);
            file_number++; // Increment file counter

            // Open the new JPEG file for writing
            img = fopen(filename, "w");
        }

        // If a JPEG file is currently open, write the block to it
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), 512, img);
        }
    }

    // Close the last JPEG file if it was opened
    if (img != NULL)
    {
        fclose(img);
    }

    // Close the memory card file
    fclose(card);
    return 0;
}
