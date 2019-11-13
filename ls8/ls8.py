#!/usr/bin/env python3

"""Main."""

import sys
import argparse
from cpu import *

# instantiate the argument parser
parser = argparse.ArgumentParser()

# add the filename argument to the parser
parser.add_argument("filename", help="The name of the file to be executed")

# parse to get the argument
args = parser.parse_args()

# instantiate the CPU
cpu = CPU()

# load a program with name <filename>
cpu.load(args.filename)

# execute the program by calling the run method
cpu.run()
