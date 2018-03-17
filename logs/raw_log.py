#!/usr/bin/python3
import glob, os

def main():
    unique = set()
    for filename in glob.glob("*.log"):
        with open(filename, 'r') as f:
            line = None
            while line != '':
                line = f.readline()
                attr = line.split('\t')

                unique.add('\t'.join(attr[0:2]))

    out = sorted(list(unique))
    for l in out:
        print(l)


if __name__ == "__main__":
    main()
