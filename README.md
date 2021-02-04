# File Structure Analysis
The `analyze_structure.py` program will analyze the given directory, searching for files with
the specified extension (defaults to .py files). It will find the line count for each file,
as well as any additional information as specified below.

Regardless of which options are selected, the program will print out which extensions it is searching
for, the number of directories and files found, and the total line count.

### Usage:
Command: `analyze_structure analyze_structure [dir_name] [options]`  

Options and arguments for file structure analysis:  
`dir_name`          absolute or relative path to directory to analyze (DEFAULT = current working directory)  
`-a`                show all directories instead of just those containing relevant files  
`-c`                include character count in each file  
`-d`                turn on debug mode for debug messages  
`-e` EXT [EXT ...]  file extensions to search for  
`--fav`             favorite settings, acts as shortcut for `-rtw` (recursive, tree, words)  
`-h`, `--help`      show help message and exit  
`--id` ID [ID ...]  names of directories to ignore  
`--if` IF [IF ...]  names of files to ignore (must include extension)  
`-l`                long analysis, acts as shortcut for `--nb` `-wcs` (non-blank, words, chars, and sizes)  
`--nb`              include non-blank line count in each file  
`-r`                recurse through all subdirectories  
`-s`                include file sizes  
`-t`                display graphical file tree  
`-w`                include word count in each file  


Ex: `analyze_structure -r -l -s -t -e py txt -id ignoreme -if README.txt`  
The `--fav` flag is a shortcut for common settings, currently set to `-rtw` (recursive, tree, and words)

### Customizing Display
The important options for customizing the infomation displayed are `-t`, which displays a text
representation of the file structure, `-a`, which forces the tree to show all subdirectories
instead of leaving out subdirectories that don't have any files of the specified extension.

### Statistics Shown
The `-r` option is very common to use, and tells the program to recurse through all subdirectories
in the directory analyzed. The flags for adding statistics to show are `--nb` (non-blank lines),
`-w` (word count), `c` (char count), and `s` (file sizes). The `l` flag is a shortcut for all four,
showing non-blank lines, word count, character count, and file sizes (long analysis).

### Filtering Data
The importand commands for filtering data are `-e`, which allows the user to select the extensions
the program searches for, `-if`, which tells the program which file names to ignore, and `-id`, which
tells the program which directory names to ignore.
