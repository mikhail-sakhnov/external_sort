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
        lines.append((line))
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
        out.writelines(map(str, lines))


def merge_chunks(original_file_path, index_list, out_file):

    files = dict((idx, open("%s.%s" % (original_file_path, idx)))
                 for idx in index_list)
    values = dict((idx, (files[idx].readline())) for idx in index_list)
    done = set()

    def select_next():
        value = None
        chunk = None
        for idx in index_list:
            if idx in done:
                continue
            if value is None:
                value = values[idx]
                chunk = idx
                continue
            if values[idx] < value:
                value = values[idx]
                chunk = idx
        if chunk is not None:
            line = files[chunk].readline()
            if line == "":
                done.add(chunk)
            else:
                values[chunk] = (line)
        return value

    while True:
        next_value = select_next()
        if next_value is None:
            break
        out_file.write(str(next_value))
    for file in files.values():
        file.close()


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
        chunk = (chunk)
    except ValueError:
        print "Usage: python %s <target> <chunk_size>" % sys.argv[0]
        sys.exit(-1)

    sort_external(target, chunk)
