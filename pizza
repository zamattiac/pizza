#! /Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5
import sys

filename = sys.argv[1]
# Output file
o = 'o' in sys.argv or '-o' in sys.argv
# Memory dump
m = 'm' in sys.argv or '-m' in sys.argv
# Warnings
w = 'w' in sys.argv or '-w' in sys.argv

from memory import *
from tree_parser import MainFileParser

if __name__ == '__main__':
    program = MainFileParser(filename)
    if o:
        print(program)
    else:
        program.run()
        if m:
            print('\nMemory arrays')
            for array in arrays:
                print(array + str(arrays[array]))