import sys
import string
import random
import os


def random_char():
    return random.choice(["0", "1",
                          "2", "3",
                          "4", "5",
                          "6", "7",
                          "8", "9"])


def generate(line_count, line_max_size, out):
    for i in range(line_count):
        line_size = random.randint(1, line_max_size)
        for j in range(line_size):
            out.write(random_char())
        out.write(os.linesep)
        out.flush()


if __name__ == "__main__":
    try:
        line_count, line_max_size, output = sys.argv[1:]
        line_count = int(line_count)
        line_max_size = int(line_max_size)
    except ValueError:
        print "Usage: python %s <line_count> <line_max_size> <output_file>" % sys.argv[0]
        sys.exit(-1)
    with open(output, 'w') as out:
        generate(line_count, line_max_size, out)
