# Author: Jordy Araujo <https://github.com/64bit-awesome/>
# Requires: Python 3.6+

# Version: 0.1-rc
# Codename: vm-magic-x2
# 'DVD' VOB/MPEG file discover, sort, and merge -> single file.

import os
import glob
import pathlib
import argparse

parser =  argparse.ArgumentParser(description='\'DVD\' VOB/MPEG file discover, sort, and merge to a single file.')
safe_extensions = ['.vob', '.mpeg', '.mpg']

# Script arguments:
parser.add_argument('-d', '--directory', type=str, metavar='',
                    help='start scanning in another directory')
parser.add_argument('-o', '--out', type=str, metavar='',
                    help='directory to output files')

parser.add_argument('-i', '--ignore', action='store_true',
                    help='ignore files without VOB/MPEG extensions')
parser.add_argument('-l', '--local', action='store_true',
                    help='do not scan inside folders')
parser.add_argument('-c', '--clean', action='store_true',
                    help='delete individual files after mergining')
parser.add_argument('-x', '--extension', type=str, metavar='',
                    help='extension of output file / default: mpeg')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='show more details')
parser.add_argument('-s', '--sort', type=str, metavar='',
                    help='sort the files in: ascending [default], descending')

args = parser.parse_args() # parse arguments.
out_directory = os.getcwd() if args.out == None else os.path.abspath(args.out)

# Change directory if required:
if args.directory != None:
    os.chdir(args.directory)

# Build glob-path:   
glob_path = pathlib.Path('.' if args.local == True else '**').absolute() / '*.*'

if args.verbose:
    print("Glob path: {0}".format(glob_path))
    print("Output path: {0}".format(out_directory))

# Get files:
files = glob.glob(str(glob_path), recursive = not args.local)

# Sort files:
if args.sort == None or args.sort == 'ascending':
    files.sort()
elif args.sort == 'descending':
    files.sort(reverse=True)

# Process files Nd directories:
directories = {}
for file_path in files: # order of iteration is not guaranteed for dictionaries, -> not a problem.
    folder = os.path.basename(os.path.dirname(file_path))
    if folder in directories:
        directories[folder].append(file_path)
    else:
        directories[folder] = [file_path]

# Process files:
for directory_name, file_paths in directories.items():
    output_file = open(os.path.join(out_directory, directory_name + '.' + 
        ('mpeg' if args.extension == None else args.extension)), 'xb') # 'xb' create binary-mode.
    
    print("--/{root}".format(root=directory_name))

    for file_path in file_paths: # order of iteration is guaranteed for lists.
        filename, extension = os.path.splitext(file_path)
    
        if (extension not in safe_extensions) and (args.ignore):
            print("\t Ignoring file: \'{0}\'".format(file_path))
        else:
            file = open(file_path, 'rb') # 'rb' read binary-mode.
            output_file.write(file.read())
            file.close()

            print("\t Merged: {file}".format(file=file_path))

            if args.clean:
                os.remove(file_path)
                print("\t Deleted: {file}".format(file=file_path))
                print('')
        
    output_file.seek(0, os.SEEK_END)
    print("\t Total file size: {size} bytes".format(size=output_file.tell()))
    output_file.close()
