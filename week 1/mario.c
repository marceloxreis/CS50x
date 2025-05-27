#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Get size of grid
    int n;
    do
    {
        n = get_int("Size: ");
    }
    while (n < 1 || n > 15);  // Ensure n is between 1 and 9 inclusive

    // Print grid of bricks
    for (int i = 0; i < n; i++)
    {
        // Print leading spaces
        for (int f = 0; f < n - i - 1; f++)
        {
            printf("");
        }

        // Print left pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // Print gap
        printf("  ");

        // Print right pyramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // Move to next row
        printf("\n");
    }
}
