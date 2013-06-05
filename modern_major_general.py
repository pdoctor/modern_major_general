import os

class MMG(object):

    def __init__(self, **kwargs):
        self.match_function = self._build_match_pattern(kwargs["find_pattern"])
        self.input_source = self._get_input_source(kwargs)
        self.get_item_generator = self._get_item_generator()
        self.__current_file_name = ""

    def _build_match_pattern(self, *patterns):
        """Initializes the pattern match criteria
    
           Currently only supports plain text matches"""
    
        def match_in_line(line):
            """Inner function using a closure on pattern"""
            return reduce(lambda x, y: x and y, map(lambda x: x in line, patterns))
    
        return match_in_line

    def _get_input_source(self, kwargs):
        """Returns a data source as either a single file or all files in the directory"""

        in_file = kwargs.get("in_file", 0)
        in_directory = kwargs.get("in_directory", 0)

        if in_file and in_directory:
            raise ValueError("May not pass both file and directory.")
        
        if not (in_file or in_directory):
            raise ValueError("Must pass either file or directory.")

        if in_file:
            if not os.path.isfile(in_file):
                raise IOError("File does not exist.")

            return self._read_file(in_file)
        else:
            if not os.path.exists(in_directory):
                raise IOError("Directory does not exist.")

            return self._read_files_in_directory(in_directory)    

    def _get_files(self, directory_name):
        """Finds all files in a given directory and sub directory"""

        for root, dirs, files in os.walk(directory_name): # Walk directory tree
            for f in files:
                yield os.path.join(root, f)
        
    def _read_file(self, file_name):
        """Open a file and return a line at a time"""

        self.__current_file_name = file_name

        with open(file_name, 'r') as file_handle:
            for line in file_handle:
                yield line
    
    def _read_files_in_directory(self, directory_name):
        """For each file in the directory, open the file and read a line at a time"""

        for file_name in self._get_files(directory_name):
            for line in self._read_file(file_name):
                yield line    

    def _get_item_generator(self):
        """Returns a generator function with the match applied."""
        return ({ "Match" : item } for item in self.input_source if self.match_function(item))    

    def with_file_name(self):
        """Generator will print both match and the file name containing the match"""
        self.get_item_generator = ( dict(item.items() + { "File Name" : self.__current_file_name }.items()) for item in self.get_item_generator)
        return self

    def only_file_name(self):
        """Generator will only print the file name containing the match"""
        self.get_item_generator = ({ "File Name" : self.__current_file_name } for item in self.get_item_generator)
        return self

    def print_matches_to_screen(self):
        """Prints the matches to the screen."""

        for print_item in self.get_item_generator:
            for key, value in print_item.iteritems():
                print "%s: %s" % (key, value)

if __name__ == "__main__":
    mmg = MMG(find_pattern="0C00000O6S", in_directory="./missed_deltas/")
    #mmg.only_file_name.print_matches_to_screen()
    mmg.with_file_name().print_matches_to_screen()