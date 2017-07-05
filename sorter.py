import sys
import os


def read_next_chunk(file, chunk_size):
    start = 0
    end = 0
    lines = []
    while True:
        line = file.readline()
        if line == "":
            break
        lines.append(line)
        end += 1
        if len(lines) == chunk_size:
            yield lines, start
            lines = []
            start = end + 1
    if lines:
        yield lines, start


def sort_chunk(chunk):
    chunk.sort()


def save_chunk(original_file_path, lines, start_index):
    with open("%s.%s" % (original_file_path, start_index), "w") as out:
        out.writelines(lines)


def merge_chunks(original_file_path, index_list, out_file):
    pass


def cleanup(original_file_path, indexes):
    for idx in indexes:
        os.remove("%s.%s" % (original_file_path, idx))


def sort_external(file_path, chunk_size):
    with open(file_path, "r") as file:
        chunks_count = 0
        indexes = []
        for chunk, start_index in read_next_chunk(file, chunk_size):
            chunks_count += 1
            sort_chunk(chunk)
            save_chunk(file_path, chunk, start_index)
            indexes.append(start_index)
    with open("%s.sorted" % file_path, "w") as out:
        merge_chunks(file_path, indexes, out)
    cleanup(file_path, indexes)


if __name__ == "__main__":
    try:
        target, chunk = sys.argv[1:]
        chunk = int(chunk)
    except ValueError:
        print "Usage: python %s <target> <chunk_size>" % sys.argv[0]
        sys.exit(-1)

    sort_external(target, chunk)
