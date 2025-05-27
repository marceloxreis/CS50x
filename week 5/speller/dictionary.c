// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];  // Array to store the word
    struct node *next;      // Pointer to the next node
} node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // 1. Calculate the hash index for the input word using the hash function
    unsigned int index = hash(word);

    // 2. Access the linked list at the computed index in the hash table
    node *cursor = table[index];

    // 3. Traverse the linked list and compare the word with each node's word
    while (cursor != NULL)
    {
        // Use strcasecmp for case-insensitive comparison between the input word and the word in the current node
            if (strcasecmp(word, cursor->word) == 0)
        {
            return true;  // If a match is found, return true
        }
        cursor = cursor->next;  // Move to the next node in the list
    }

    // 4. If no match is found in the linked list, return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash_value = 0;  // Initialize the hash value to 0

    // Loop through each character in the word until the null terminator
    for (int i = 0; word[i] != '\0'; i++)
    {
        // Add the ASCII value of the current character to hash_value
        hash_value += tolower(word[i]);
    }

    return hash_value % N;  // Return the final sum of ASCII values
}


// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary) // ok
{
    // Open dictionary file
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }

    // Buffer to store each word
    char word[LENGTH + 1];

    // Read one word at a time from the dictionary
    while (fscanf(source, "%s", word) != EOF)
    {
        // Allocate memory for a new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;  // Handle memory allocation failure
        }

        // Copy the word into the node's word field
        strcpy(new_node->word, word);

        // Hash the word to get an index
        unsigned int index = hash(word);

        // Insert the new node into the hash table
        new_node->next = table[index];  // Point to the current first node in the list
        table[index] = new_node;        // Insert the new node at the beginning of the list
    }

    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{

    unsigned int word_count = 0;  // Initialize the word value to 0

    // Loop through each character in the word until the null terminator
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            cursor = cursor->next;
            word_count++;
        }
        // Add the ASCII value of the current character to hash_value

    }

    return word_count;  // Return the final sum of ASCII values

}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (unsigned int i = 0; i < N; i++)
    {
    // TODO
    node *cursor = table[i];
    while(cursor != NULL)
    {

        node *tmp = cursor;
        cursor = cursor-> next;
        free(tmp);
    }
    }
    return true;

}
