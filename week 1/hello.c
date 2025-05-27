#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string a = get_string("what's your name? ");
    printf("Hello, %s\n", a);
}
