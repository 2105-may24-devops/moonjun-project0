from pathlib import Path
from deleter import Deleter
import curses
import sys
import os

# 
class FileNavigator():
    
    #Global variables used to move the cursor up or down.
    UP = -1
    DOWN = 1
    
    # Constructor that accepts a Path object containing the ROOT path of the project.
    def __init__(self, directory: Path):
        self.ROOT = directory

        # Path of the current directory.
        self.curr_dir = directory

        # List of subdirectories and files. 
        self.menu = get_directories(self.curr_dir) + get_files(self.curr_dir)

        # Default is 0. Changes when in directory containing more rows than width of the terminal.
        self.min_row = 0
        
        # Cannot go past this line. Prevents cursor from going downward infinitely.
        self.max_row = len(self.menu)

        # Acts as the visual cursor.
        self.curr_row = 0

        # Initializing the curses terminal.
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.w, self.h = self.stdscr.getmaxyx()
        self.max_lines_per_page = curses.LINES
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(False)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

        # Store items to be written to .txt file.
        self.to_delete = []

    # Main program loop
    def run_program(self):

        while True:

            # Print screen based on the current directory.
            self.print_screen(self.menu)
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP:
                self.scrolling(self.UP)

            elif key == curses.KEY_DOWN:
                self.scrolling(self.DOWN)

            # When ENTER key is pressed.
            elif key == key in [10, 13]:
                
                # Check to see if position of cursor where ENTER was pressed is a directory.
                if Path.is_dir(Path(self.curr_dir).joinpath(self.menu[self.curr_row])):
                    self.change_directory()
            
            # When 'd' key is pressed.
            elif key == 100:

                # Selected row is to be deleted after calling select_file().
                selected = Path(self.curr_dir).joinpath(self.menu[self.curr_row])
                self.select_file(selected)
                
            # When 'q' is pressed, program ends.
            elif key == 113:
                self.stdscr.keypad(False)
                curses.nocbreak()
                curses.echo()
                curses.curs_set(True)
                curses.endwin()
                return

    # Allows screen to scroll when number of items in directory exeeds that of the width of the terminal.
    #
    # Arguments:    Global constant UP(-1) or DOWN(1)
    # Returns:      None
    def scrolling(self, direction):

        next_row = self.curr_row + direction

        # Scroll up a row past the min-width of the terminal.
        if direction == self.UP and (self.min_row > 0 and self.curr_row == 0):
            self.min_row += direction
            return
                                                
        # Scroll down a row past the max-width of the terminal.
        if direction == self.DOWN and (next_row == self.max_lines_per_page) and (self.min_row + self.max_lines_per_page < self.max_row):
            self.min_row += direction
            return

        # Move the cursor(current row) up a row.
        if (direction == self.UP) and (self.min_row > 0 or self.curr_row > 0):
            self.curr_row = next_row
            return

        # Move the cursor(current row) down a row.                                      
        if direction == self.DOWN and (next_row < self.max_row) and (self.min_row + next_row < self.max_row):
            self.curr_row = next_row
            return

    #Given a Path to the directory/file, it will be added to a .txt for deletion.
    def select_file(self, selected: Path):

        # Initialize new window for prompt at the bottom of the terminal.
        win = curses.newwin(2,self.h, self.w - 2, 0)

        if Path.is_file(selected):

            # If file is not marked for deletion, mark it.
            if str(selected) not in self.to_delete:
                self.to_delete.append(str(selected))
                win.addstr(0, 0, "File marked for deletion.")
                win.addstr(1,0, "Press any key to continue.")

            # If it is marked, unmark it.
            else:
                self.to_delete.remove(str(selected))
                win.addstr(0, 0, "File unmarked for deletion.")
                win.addstr(1,0, "Press any key to continue.")

        # If Path is a directory.
        else:
            # If directory is not marked for deletion, mark it.
            if str(selected) not in self.to_delete:
                self.to_delete.append(str(selected))
                win.addstr(0, 0, "File marked for deletion.")
                win.addstr(1,0, "Press any key to continue.")
            # If it is marked, unmark it.
            else:
                self.to_delete.remove(str(selected))
                win.addstr(0, 0, "File unmarked for deletion.")
                win.addstr(1,0, "Press any key to continue.")

        # Remove the window from the screen.
        win.touchwin()
        win.refresh()
        win.getch()
        del win
        return

    # Change directories and update all variables related to update the screen.
    def change_directory(self):

        t_dir = Path(self.curr_dir).joinpath(self.menu[self.curr_row])
        os.chdir(t_dir)
        self.curr_dir = Path.cwd()
        self.menu = get_directories(self.curr_dir) + get_files(self.curr_dir)
        self.max_row = len(self.menu)
        self.curr_row = 0
        return
    
    # Prints the screen to reflect the new directory and adds highlighting for the cursor.
    def print_screen(self, menu):
        self.stdscr.erase()
        for i, row in enumerate(menu[self.min_row:self.min_row + self.max_lines_per_page]):
            if i == self.curr_row:
                self.stdscr.addstr(i,0, row, curses.color_pair(1))            
            else:
                self.stdscr.addstr(i,0, row)
        self.stdscr.refresh()

# Generates a list of files within a directory
# os.walk creates a 3-tuple (dirpath, dirnames, filenames)
# 
# Arguments:    path to directory as a string 
# Returns:      List of files
def get_files(dir: str):
    files = next(os.walk(dir))[2]
    return files

# Generates child directories within a parent directory
# os.walk creates a 3-tuple (dirpath, dirnames, filenames)
# 
# Arguments:    path to directory as a string 
# Returns:      List of subdirectories
def get_directories(dir: str):
    dir = next(os.walk(dir))[1]
    dir.insert(0, '..')
    return dir

# Creates the .txt file containing the directories/files to be deleted
#
# Arguments:    FileNavigator Object
# Return:       None 
def create_delete_file(Object: FileNavigator):

    # If ./deletion folder exists
    if Path.is_dir(Path(Object.ROOT).joinpath('deletion')):
        os.chdir('./deletion')
        write_to_file_delete(Object)

    # when ./deletion folder does not exist, create it
    else:
        Path.mkdir(Path(Object.ROOT).joinpath('deletion'))
        os.chdir('./deletion')
        write_to_file_delete(Object)
    return

# Loop to write files/directory to files-to-delete.txt
#
# Arguments:    FileNavigator Object
# Return:       None
def write_to_file_delete(Object: FileNavigator):

    file_object = open('files-to-delete.txt', 'w')
    for i in Object.to_delete:
        file_object.write(i + '\n')
    file_object.close()

def main():
    
    if len(sys.argv) < 2:
        start_folder = Path.cwd()
        test = FileNavigator(start_folder)
        test.run_program()
        os.chdir(test.ROOT)
        create_delete_file(test)
    else:
        d_object = Deleter()
        d_object.read_file(sys.argv[1])
        d_object.delete_from_list()

if __name__=='__main__':
    main()
