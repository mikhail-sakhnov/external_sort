import sys
import os

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print "Usage: python %s <file> <reverse:optional>" % sys.argv
        sys.exit(-1)
    try:
        file, reverse = sys.argv[1:]
        if reverse not in ("true", "True", "1"):
            reverse = False
        else:
            reverse = True
    except ValueError:
        file = sys.argv[1]
        reverse = False

    with open(file, "r") as inp:
        with open("%s.sorted-inmemory" % file, "w'") as out:
            lines = sorted(inp.readlines(), reverse=reverse)
            out.writelines(lines)
