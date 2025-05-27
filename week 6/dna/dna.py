import csv
import sys

def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python filename.py data.csv")
        sys.exit()

    # Read database file into a variable
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        database = list(reader)

    # Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        dna_sequence = file.read().strip()

    # Extract STRs from the database header
    with open(sys.argv[1]) as file:
        reader = csv.reader(file)
        header = next(reader)
    strs = header[1:]

    # Find longest match of each STR in DNA sequence
    longest_matches = {str_sequence: longest_match(dna_sequence, str_sequence) for str_sequence in strs}

    # Check database for matching profiles
    for profile in database:
        if all(int(profile[str_sequence]) == longest_matches[str_sequence] for str_sequence in strs):
            print(profile['name'])
            sys.exit()

    print("No match")


def longest_match(sequence, subsequence):
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):
        count = 0
        while True:
            start = i + count * subsequence_length
            end = start + subsequence_length
            if sequence[start:end] == subsequence:
                count += 1
            else:
                break
        longest_run = max(longest_run, count)

    return longest_run

main()
