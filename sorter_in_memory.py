import sys
import os

if __name__ == "__main__":
    try:
        file = sys.argv[1]
    except IndexError:
        print "Usage: python %s <file>" % sys.argv
        sys.exit(-1)
    with open(file, "r") as inp:
        with open("%s.sorted-inmemory" % file, "w'") as out:
            lines = sorted(inp.readlines())
            out.writelines(lines)
