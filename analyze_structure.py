'''
File: analyze_structure.py
Author: Gavin Vogt
This program will analyze a file structure. It allows the user to select various
options that modify its behavior. The most important modifier is the -r option,
which tells the program to recurse through all subdirectories of the given directory.
If the directory name is not specified, it defaults to use the current working
directory.

Usage: analyze_structure [directory_name] [options]
Available options:
-a             : show all directories instead of just those containing files with the correct extension
-e [...exts]   : file extensions to search for (DEFAULT = `py`)
-h             : print this help message and exit (also --help)
-if [...files] : names of files to ignore (no absolute paths, must include file extension)
-id [...dirs]  : names of directories to ignore (no absolute paths)
-l             : long analysis (line count, non-blank line count, char count)
-r             : recurse through all subdirectories
-s             : include file sizes
-t             : display graphical file tree
'''

# dependencies
import os
import sys
import abc

# Define the help string
HELP_STRING = '''usage: analyze_structure [dir_name] [options]
Options and arguments for file structure analysis:
dir_name       : absolute or relative path to directory to analyze (DEFAULT = current working directory)
-a             : show all directories instead of just those containing files with the correct extension
-e [...exts]   : file extensions to search for (DEFAULT = `py`)
-h             : print this help message and exit (also --help)
-if [...files] : names of files to ignore (no absolute paths, must include file extension)
-id [...dirs]  : names of directories to ignore (no absolute paths)
-l             : long analysis (line count, non-blank line count, char count)
-r             : recurse through all subdirectories
-s             : include file sizes
-t             : display graphical file tree
Ex: analyze_structure -r -l -s -t -e py txt -id ignoreme -if README.txt'''

class StructureObject(metaclass=abc.ABCMeta):
    '''
    Abstract Base Class representing a File or Directory, providing
    some default functionality
    
    Methods that must be defined:
        - line_count()
        - non_blank_line_count()
        - char_count()
        - size()
    '''
    @property
    def name(self):
        '''
        Allows access to the `name` property (read-only)
        '''
        return self._name
    
    def __eq__(self, other):
        '''
        Checks if file names are equal
        '''
        return (self.name == other.name)
    
    def __ne__(self, other):
        '''
        Checks if file names are not equal
        '''
        return (self.name != other.name)
    
    def __lt__(self, other):
        '''
        Checks if this file name is less than the other file name
        '''
        return (self.name < other.name)
    
    def __le__(self, other):
        '''
        Checks if this file name is less than or equal to the other file name
        '''
        return (self.name <= other.name)
    
    def __gt__(self, other):
        '''
        Checks if this file name is greater than the other file name
        '''
        return (self.name > other.name)
    
    def __ge__(self, other):
        '''
        Checks if this file name is greater than or equal to the other file name
        '''
        return (self.name >= other.name)
    
    @abc.abstractmethod
    def line_count(self):
        '''
        Gets the total line count
        '''
        raise NotImplementedError
    
    @abc.abstractmethod
    def non_blank_line_count(self):
        '''
        Gets the total non-blank line count
        '''
        raise NotImplementedError
    
    @abc.abstractmethod
    def char_count(self):
        '''
        Gets the total char count
        '''
        raise NotImplementedError
    
    @abc.abstractmethod
    def size(self):
        '''
        Gets the total size
        '''
        raise NotImplementedError
    

class Directory(StructureObject):
    '''
    This class represents a file directory crawled, storing any relevant
    information about the directory and the files it holds
    '''
    def __init__(self, dir_name, **kwargs):
        '''
        Constructs a new Directory with the given properties
        '''
        self._name = os.path.basename(dir_name)
        self._items = []
    
    def __repr__(self):
        '''
        String representation of the Directory
        '''
        return f"Directory({self._name})"
    
    def __iadd__(self, item):
        '''
        Adds a file structure item to the list of items in the directory
        '''
        self._items.append(item)
        return self
    
    def line_count(self):
        '''
        Gets the total line count
        '''
        count = 0
        for item in self._items:
            count += item.line_count()
        return count
    
    def non_blank_line_count(self):
        '''
        Gets the total non-blank line count
        '''
        count = 0
        for item in self._items:
            count += item.non_blank_line_count()
        return count
    
    def char_count(self):
        '''
        Gets the total char count
        '''
        count = 0
        for item in self._items:
            count += item.char_count()
        return count
    
    def size(self):
        '''
        Gets the total size
        '''
        total_size = 0
        for item in self._items:
            total_size += item.size()
        return total_size
    
    def has_file(self):
        '''
        Checks if this Directory contains any File objects
        '''
        for item in self._items:
            if isinstance(item, File):
                # found a file
                return True
            elif isinstance(item, Directory):
                if item.has_file():
                    # found a directory with at least one file
                    return True
        return False
    
    def item_counts(self):
        '''
        Counts the number of directories and files in the structure,
        not including itself.
        Return: tuple (dir_count, file_count)
        '''
        dir_count = 0
        file_count = 0
        for item in self._items:
            if isinstance(item, File):
                file_count += 1
            elif isinstance(item, Directory):
                counts = item.item_counts()
                dir_count += 1 + counts[0]
                file_count += counts[1]
        return dir_count, file_count
    
    def num_hidden(self):
        '''
        Counts the number of hidden directories (don't have any files)
        '''
        count = 0
        for item in self._items:
            if isinstance(item, Directory):
                if not item.has_file():
                    count += 1
                count += item.num_hidden()
        return count
    
    def print(self, recurse, show_all, depth=0):
        '''
        Prints out the structure inside this Directory
        recurse: bool, representating whether to recurse into subdirectories
        show_all: bool, representing whether to show directories with no files
        depth: (optional) int, representing the current depth
        '''
        # Print out the name of the overarching directory
        self._print_depth(depth)
        print(self._name + "/")
        
        depth += 1
        for item in self._items:
            if isinstance(item, File):
                self._print_depth(depth)
                print(item.name + "  " + item.info_string())
            elif isinstance(item, Directory):
                if not recurse:
                    # Just print the directory name
                    self._print_depth(depth)
                    print(item.name + "/")
                elif recurse and (show_all or item.has_file()):
                    # Have the item recursively print
                    item.print(recurse, show_all, depth)
    
    def _print_depth(self, depth):
        '''
        Prints text to represent the given depth
        depth: int, representing the depth
        '''
        for i in range(depth - 1):
            print("|   ", end="")
        if depth > 0:
            print("|—— ", end="")
    

class File(StructureObject):
    '''
    This class represents a file crawled, storing any relevant information
    about the file
    '''
    def __init__(self, file_name, **kwargs):
        '''
        Constructs a new File with the given properties
        '''
        self._name = os.path.basename(file_name)
        self._line_count = kwargs.get('line_count')
        self._non_blank_line_count = kwargs.get('non_blank_line_count')
        self._char_count = kwargs.get('char_count')
        self._size = kwargs.get('size')
    
    def __repr__(self):
        '''
        String representation of the File
        '''
        return f"File({self._name})"
    
    def line_count(self):
        '''
        Gets the total line count
        '''
        return self._line_count
    
    def non_blank_line_count(self):
        '''
        Gets the total non-blank line count
        '''
        return self._non_blank_line_count
    
    def char_count(self):
        '''
        Gets the total char count
        '''
        return self._char_count
    
    def size(self):
        '''
        Gets the total file size
        '''
        return self._size
    
    def info_string(self):
        '''
        Returns the info string representing the File. Includes all
        information known about line counts, char counts, and size
        '''
        info = []
        if self._line_count:
            info.append(f"{self._line_count} lines")
        if self._non_blank_line_count:
            info.append(f"{self._non_blank_line_count} non-blank lines")
        if self._char_count:
            info.append(f"{self._char_count} chars")
        if self._size:
            info.append(f"{self._size} bytes")
        return ", ".join(info)

class FileCrawler:
    '''
    This class will crawl through directories and files, getting the word
    and line counts for each file.
    '''
    def __init__(self, **kwargs):
        '''
        Constructs a new FileCrawler with the provided settings
        '''
        self._dir = kwargs.get("dir", os.getcwd())
        self._ignore_files = kwargs.get("ignore_files", set())  # -if
        self._ignore_dirs = kwargs.get("ignore_dirs", set())    # -id
        self._extensions = kwargs.get("extensions", {"py"})     # -e
        self._all = kwargs.get("a", False)                      # -a
        self._long = kwargs.get("l", False)                     # -l
        self._recursive = kwargs.get("r", False)                # -r
        self._sizes = kwargs.get("s", False)                    # -s
        self._tree = kwargs.get("t", False)                     # -t
        
        if self._dir is not None:
            # verify that it is a directory
            assert os.path.isdir(self._dir), f"{self._dir} is not a valid directory path"
    
    def __repr__(self):
        '''
        String representation of the FileCrawler
        '''
        return f"FileCrawler({self._dir})"
    
    def crawl(self):
        '''
        Crawls the file structure and prints out the results
        '''
        # Load the structure inside the main directory
        structure = self._load_dir(self._dir)
        
        print()
        if self._tree:
            # print out the tree
            structure.print(self._recursive, self._all)
            print()
        
        # Print out the totals
        dir_count, file_count = structure.item_counts()
        print("Total directories:", dir_count, end="")
        if not self._all:
            num_hidden = structure.num_hidden()
            print(f" ({dir_count - num_hidden} shown, {num_hidden} hidden)")
        else:
            print()
        print("Total files:", file_count)
        print("Total lines:", structure.line_count())
        if self._long:
            print("Total non-blank lines:", structure.non_blank_line_count())
            print("Total chars:", structure.char_count())
        if self._sizes:
            print("Total size:", structure.size(), "bytes")
    
    def _load_dir(self, dir_path):
        '''
        Crawls a single directory, and recurses if the class is set to recurse
        dir_path: str, representing the path to the directory
        Return: list of StructureObject objects (mix of File and Directory)
        '''
        current_dir = Directory(dir_path)
        for item_name in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item_name)
            if os.path.isdir(item_path) and item_name not in self._ignore_dirs:
                # directory
                if self._recursive:
                    current_dir += self._load_dir(item_path)
                else:
                    current_dir += Directory(item_path)
            elif (os.path.isfile(item_path) and self.is_valid_ext(item_path)
                            and item_name not in self._ignore_files):
                # .py file
                current_dir += self.load_file(item_path)
        return current_dir
    
    def load_file(self, file_path):
        '''
        Loads the File object information for the given file
        file_path: str, representing the path to the file
        Return: File representing the file
        '''
        file_info = {}
        self._read_file(file_info, file_path)   # read the line / char counts
        if self._sizes:
            # include file sizes
            file_info['size'] = os.path.getsize(file_path)
        
        return File(file_path, **file_info)
    
    def _read_file(self, file_info, file_path):
        '''
        Reads the information in a file
        file_info: dict, to store file information in
        file_path: str, representing the path to the file
        '''
        file_info["line_count"] = 0
        if self._long:
            file_info["non_blank_line_count"] = 0
            file_info["char_count"] = 0
            def read_info(line):
                file_info["line_count"] += 1
                file_info["char_count"] += len(line)
                if len(line.strip()) > 0:
                    file_info["non_blank_line_count"] += 1
        else:
            def read_info(line):
                file_info["line_count"] += 1
        
        f = open(file_path, 'r', encoding='utf8')
        for line in f:
            line = line.strip("\n")
            read_info(line)
    
    @classmethod
    def from_args(cls):
        '''
        Returns a new FileCrawler object, instantiated using the settings
        specified on the command line
        
        Settings:
            [directory name] = directory to search
            -a = show all directories instead of just those containing .py files
            -e = file extensions to look for (DEFAULT = `py`)
            -if = relative names of files to ignore (automatically ignore self)
            -id = relative names of directories to ignore
            -l = long analysis (line count, non-blank line count, char count)
            -r = recurse through all subdirectories
            -s = include file sizes
            -t = display file tree
        '''
        options = {}
        options["ignore_files"] = { os.path.basename(sys.argv[0]) }
        options["ignore_dirs"] = set()
        extensions = set()
        
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i]
            if arg.startswith("-"):
                # setting for analysis
                option = arg.lstrip("-")
                if option == "if":
                    # Set of file names to ignore (MUST INCLUDE EXTENSION)
                    for file_name in cls._get_args(i + 1):
                        options["ignore_files"].add(os.path.basename(file_name))
                        i += 1
                elif option == "id":
                    # Set of directory names to ignore
                    for dir_name in cls._get_args(i + 1):
                        options["ignore_dirs"].add(os.path.basename(dir_name))
                        i += 1
                elif option == "e":
                    # Set of file extensions to look for
                    for ext in cls._get_args(i + 1):
                        extensions.add(ext)
                        i += 1
                else:
                    options[option] = True
            else:
                # directory to search
                options["dir"] = arg
            i += 1
        
        # Validate extensions
        options["extensions"] = set()
        for ext in extensions:
            stripped_ext = ext.lstrip(".")
            if len(stripped_ext) > 0:
                options["extensions"].add(stripped_ext)
        if len(options["extensions"]) == 0:
            # Automatically look for .py files
            options["extensions"].add("py")
        
        # Instantiate the new FileCrawler
        return FileCrawler(**options)
    
    @staticmethod
    def _get_args(index):
        '''
        Gets all the arguments from a given index on, until reaching
        another option (starting with a hyphen)
        '''
        args = []
        while index < len(sys.argv) and not sys.argv[index].startswith("-"):
            args.append(sys.argv[index])
            index += 1
        return args
    
    def is_valid_ext(self, file_name):
        '''
        Checks if the given file name is a file we are looking for
        '''
        extension = file_name.split(".")[-1]
        return (extension in self._extensions)
    
    def extensions(self):
        '''
        Returns the list of extensions the program is searching for
        '''
        return list(self._extensions)


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        # print the help string and exit
        print(HELP_STRING)
    else:
        fc = FileCrawler.from_args()
        print(f"""Searching for file extensions '.{"', '.".join(fc.extensions())}' ...""")
        fc.crawl()

if __name__ == "__main__":
    main()
