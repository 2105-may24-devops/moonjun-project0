import curses
import os
from pathlib import Path

class FileNavigator(object):
    UP = -1
    DOWN = 1
    IN = 0

    def __init__(self, directory):
        self.root = directory
        self.menu = get_directories(self.root) + get_files(self.root)

        # Initializing the terminal
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()

        #self.w, self.h = self.stdscr.getmaxyx()
        self.min_row = 0
        #
        self.max_row = 1000
        # Max number of rows of the terminal
        self.max_lines_per_page = curses.LINES
        self.curr_row = 0
        self.page = self.min_row // self.max_lines_per_page

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

    def run_program(self):

        while True:
            self.print_screen(self.menu)
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.scrolling(self.UP)
            elif key == curses.KEY_DOWN:
                self.scrolling(self.DOWN)
            elif key == key in [10, 13]:
                self.entering(self.IN, self.menu)

    def scrolling(self, direction):
        next_row = self.curr_row + direction

        if direction == self.UP and (self.min_row > 0 and self.curr_row == 0):
            self.min_row += direction
            return

        # Scroll down one row
        if direction == self.DOWN and (next_row == self.max_lines_per_page) and (self.min_row + self.max_lines_per_page < self.max_row):
            self.min_row += direction
            return

        if direction == self.UP and self.min_row > 0 or self.curr_row > 0:
            self.curr_row = next_row
            return
        
        if direction == self.DOWN and (next_row < self.max_lines_per_page) and (self.min_row + next_row < self.max_row):
            self.curr_row = next_row
            return

    def entering(self, direction, menu):
        # ['..', '.vscode', 'directory1', 'directory2', ..., 'test.txt' ]
        t_dir = Path(self.root).joinpath(menu[self.curr_row])
        if direction == self.IN and Path.is_dir(t_dir):
            #change_directories(self, t_dir)
            os.chdir(t_dir)
            self.menu = get_directories(Path.cwd()) + get_files(Path.cwd())

    def print_screen(self, menu):
        self.stdscr.erase()
        for i, row in enumerate(menu[self.min_row:self.min_row + self.max_lines_per_page]):
            if i == self.curr_row:
                self.stdscr.addstr(i,0, row, curses.color_pair(1))            
            else:
                self.stdscr.addstr(i,0, row)
        self.stdscr.refresh()

def change_directories(Object, directory):
    #Object.menu = directory
    pass

def get_files(dir: str):
    files = next(os.walk(dir))[2]
    return files
    
def get_directories(dir: str):
    dir = next(os.walk(dir))[1]
    dir.insert(0, '..')
    return dir


def main():
    start_folder = Path.cwd()#'/mnt/c'
    test = FileNavigator(start_folder)
    test.run_program()
    #pathd = get_directories(start_folder) + get_files(start_folder)
    #print(Path.is_dir(Path(start_folder).joinpath('directory1')))

if __name__=='__main__':
    main()