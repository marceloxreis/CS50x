from cs50 import get_int

while True:
    n = get_int("Height: ")
    if 9 > n > 0:
        break

for i in range(n):
    print(" " * (n - i - 1), end="")
    print("#" * (i + 1), end="")
    print("  ", end="")
    print("#" * (i + 1), end="")
    print()
