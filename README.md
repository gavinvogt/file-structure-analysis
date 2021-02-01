# File Structure Analysis
The `analyze_structure.py` program will analyze the given directory, searching for files with
the specified extension (defaults to .py files). It will find the line count for each file,
as well as any additional information as specified below.

Regardless of which options are selected, the program will print out which extensions it is searching
for, the number of directories and files found, and the total line count.

### Usage:
Command: `analyze_structure analyze_structure [dir_name] [options]`  

Options and arguments for file structure analysis:  
`dir_name`       : absolute or relative path to directory to analyze (DEFAULT = current working directory)  
`-a`             : show all directories instead of just those containing files with the correct extension  
`-e [...exts]`   : file extensions to search for (DEFAULT = `py`)  
`-h`             : print this help message and exit (also `--help`)  
`-if [...files]` : names of files to ignore (no absolute paths, must include file extension)  
`-id [...dirs]`  : names of directories to ignore (no absolute paths)  
`-l`             : long analysis (line count, non-empty line count, char count)  
`-r`             : recurse through all subdirectories  
`-s`             : include file sizes  
`-t`             : display graphical file tree  

Ex: `analyze_structure -r -l -s -t -e py txt -id ignoreme -if README.txt`  

### Customizing Display
The important options for customizing the display are `-t`, which displays a text representation
of the file structure, `-a`, which forces the tree to show all subdirectories instead of leaving
out subdirectories that don't have any files of the specified extension.

### Customizing Data
The important options for customizing the data found are `-r`, which tells the program to recurse through
subdirectories, `-l`, which does a long analysis including non-blank line count and character count in
addition to the line counts, and `-s`, which tells the program to include the file sizes.

### Filtering Data
The importand commands for filtering data are `-e`, which allows the user to select the extensions
the program searches for, `-if`, which tells the program which file names to ignore, and `-id`, which
tells the program which directory names to ignore.
