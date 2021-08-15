# Author: Jordy Araujo <https://github.com/64bit-awesome/>
# Requires: Python 3.6+

# Version: 0.1-dev
# Codename: vm-magic-2x
# 'DVD' VOB/MPEG file discover, sort, and merge -> single file.

import os
import sys
import glob
import pathlib
import argparse

parser =  argparse.ArgumentParser(description='\'DVD\' VOB/MPEG file discover, sort, and merge to a single file.')

# Script arguments:
parser.add_argument('-d', '--directory', type=str, metavar='',
                    help='Start scanning in a specific directory.')
parser.add_argument('-o', '--out', type=str, metavar='',
                    help='Directory to output files; otherwise output will be in current directory.')

parser.add_argument('-l', '--local', action='store_true',
                    help='Do not scan inside folders.')
parser.add_argument('-x', '--delete', type=str, metavar='',
                    help='Delete individual files after mergining.')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Show more details.')
parser.add_argument('-s', '--sort', type=str, metavar='',
                    help='Sort the files in: ascending [default], descending')

args = parser.parse_args() # parse arguments.
out_directory = os.getcwd() if args.out == None else args.out

# Change directory if required:
if args.directory != None:
    os.chdir(args.directory)

# Build glob-path:   
glob_path = pathlib.Path('.' if args.local == True else '**').absolute() / '*.*'

if args.verbose:
    print("Glob path: {0}".format(glob_path))

# Get files:
files = glob.glob(str(glob_path), recursive = not args.local)

# Sort files:
if args.sort == None or args.sort == 'ascending':
    files.sort()
elif args.sort == 'descending':
    files.sort(reverse=True)

# Process files Nd directories:
directories = {}
for filepath in files:
    folder = os.path.basename(os.path.dirname(filepath))
    if folder in directories:
        directories[folder].append(filepath)
    else:
        directories[folder] = [filepath]

print(directories)