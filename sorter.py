import sys
import os


class ExternalSorter(object):

    def __init__(self, file_path, chunk_size, compare=None):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.compare = compare
        if self.compare is None:
            self.compare = self._default_compare
        self.indexes = []
        self.files = None
        self.values = None

    def _default_compare(self, a, b):
        if a == b:
            return 0
        if a < b:
            return -1
        return 1

    def sort(self):
        with open(self.file_path, "r") as file:
            for chunk, start_index in self.read_next_chunk(file):
                self.sort_chunk(chunk)
                self.save_chunk(chunk, start_index)
                self.indexes.append(start_index)
        with open("%s.sorted" % self.file_path, "w") as out:
            self.merge_chunks(out)
        self.cleanup()

    def read_next_chunk(self, file):
        start = 0
        end = 0
        lines = []
        while True:
            line = file.readline()
            if line == "":
                break
            lines.append((line))
            end += 1
            if len(lines) == self.chunk_size:
                yield lines, start
                lines = []
                start = end + 1
        if lines:
            yield lines, start

    def save_chunk(self, chunk, start_index):
        with open("%s.%s" % (self.file_path, start_index), "w") as out:
            out.writelines(chunk)

    def sort_chunk(self, chunk):
        chunk.sort(cmp=self.compare)

    def merge_chunks(self, out_file):

        self.files = dict((idx, open("%s.%s" % (self.file_path, idx)))
                          for idx in self.indexes)
        self.values = dict(
            (idx, (self.files[idx].readline())) for idx in self.indexes)
        for value in self.next_generator():
            out_file.write(value)

    def next_generator(self):
        done = set()
        while True:
            value = None
            chunk = None
            for idx in self.indexes:
                if idx in done:
                    continue
                if value is None:
                    value = self.values[idx]
                    chunk = idx
                    continue
                if self.compare(self.values[idx], value) == -1:
                    # if self.values[idx] < value:
                    value = self.values[idx]
                    chunk = idx
            if chunk is not None:
                line = self.files[chunk].readline()
                if line == "":
                    done.add(chunk)
                else:
                    self.values[chunk] = (line)
            if value is None:
                break
            yield value

    def cleanup(self):
        for file in self.files.values():
            file.close()
        for idx in self.indexes:
            os.remove("%s.%s" % (self.file_path, idx))


def parse_args():
    if len(sys.argv) not in (3, 4):
        print "Usage: python %s <target> <chunk_size>" % sys.argv[0]
        sys.exit(-1)
    try:
        target, chunk, reverse = sys.argv[1:]
        chunk = int(chunk)
        if reverse not in ("true", "True", "1"):
            reverse = False
        else:
            reverse = True
    except ValueError:
        target, chunk = sys.argv[1:]
        chunk = int(chunk)
        reverse = False

    return target, chunk, reverse

if __name__ == "__main__":

    target, chunk, reverse = parse_args()

    def reverse_cmp(a, b):
        if a == b:
            return 0
        if a < b:
            return 1
        return -1

    if not reverse:
        ExternalSorter(target, chunk).sort()
    else:
        ExternalSorter(target, chunk, reverse_cmp).sort()
