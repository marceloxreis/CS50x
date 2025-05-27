#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // validate

    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    string key = argv[1];
    //  strlen to verificate the lenght
    if (strlen(key) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    // isalnum to verificate numbers

    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("key must contain alphabetic characters.\n");
            return 1;
        }
    }
    // chech for duplicates
    for (int i = 0; i < 25; i++)
    {
        for (int j = i + 1; j < 26; j++)
        {
            if (tolower(argv[1][i]) == tolower(argv[1][j]))
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }
    // get key
    string text = get_string("plaintext: ");
    char transformed;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // lower casee
        if (islower(text[i]))
        {
            transformed = tolower(key[text[i] - 'a']); // store the transformed character in transformed
            text[i] = transformed;           // then assign it back to text[i]
        }
        // upper case
        else if (isupper(text[i]))
        {
            transformed = toupper(key[text[i] - 'A']); // store the transformed character in transformed
            text[i] = transformed;           // then assign it back to text[i]
        }
        else
        {
            text[i] = text[i];
        }
    }
    printf("ciphertext: %s\n", text);
}
