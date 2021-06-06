from pathlib import Path
from curses import ascii
import curses
import os

class FileNavigator(object):
    UP = -1
    DOWN = 1
    IN = 0
    OUT = -2

    def __init__(self, directory):
        self.root = directory
        self.curr_dir = directory
        self.menu = get_directories(self.curr_dir) + get_files(self.curr_dir)

        # Initializing the terminal
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.curs_set(False)

        self.w, self.h = self.stdscr.getmaxyx()
        self.min_row = 0
        self.max_row = 1000
        # Max number of rows of the terminal
        self.max_lines_per_page = curses.LINES
        self.curr_row = 0
        self.page = self.min_row // self.max_lines_per_page

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_MAGENTA)

        #I might need to make a new class for these.
        self.to_delete = []

    def run_program(self):

        while True:
            self.print_screen(self.menu)
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                self.scrolling(self.UP)
            elif key == curses.KEY_DOWN:
                self.scrolling(self.DOWN)
            elif key == key in [10, 13]:
                if Path.is_dir(Path(self.curr_dir).joinpath(self.menu[self.curr_row])):
                    self.change_directory()
            elif key == 100:
                selected = Path(self.curr_dir).joinpath(self.menu[self.curr_row])
                self.select_file(selected)

                #if Path.is_file(selected):#Path(self.curr_dir).joinpath(self.menu[self.curr_row])):
                #    #selected = Path(self.curr_dir).joinpath(self.menu[self.curr_row])
                #    self.select_file(selected)
                #elif Path.is_dir(selected):
                #    self.select_dir(selected)
                
            # Breaks out of fullscreen after pressing 'q'
            elif key == 113:
                curses.nocbreak()
                self.stdscr.keypad(False)
                curses.echo()
                curses.curs_set(True)
                curses.endwin()
                return

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

    # curses.newwwin(nlines, ncol, begin_y, begin_x)
    # curses.addstr(y, x, str[,attr])

    def select_file(self, selected):

        # Initialize new window for prompt.
        win = curses.newwin(2,self.h, self.w - 2, 0)

        if Path.is_file(selected):
            if str(selected) not in self.to_delete:
                self.to_delete.append(str(selected))
                win.addstr(0, 0, "File marked for deletion.")
                win.addstr(1,0, "Press any key to continue.")
            else:
                self.to_delete.remove(str(selected))
                win.addstr(0, 0, "File unmarked for deletion.")
                win.addstr(1,0, "Press any key to continue.")
        else:
            if str(selected) not in self.to_delete:
                self.to_delete.append(str(selected))
                win.addstr(0, 0, "File marked for deletion.")
                win.addstr(1,0, "Press any key to continue.")
            else:
                self.to_delete.remove(str(selected))
                win.addstr(0, 0, "File unmarked for deletion.")
                win.addstr(1,0, "Press any key to continue.")

        win.touchwin()
        win.refresh()
        win.getch()
        del win
        return

    def change_directory(self):

        t_dir = Path(self.curr_dir).joinpath(self.menu[self.curr_row])
        os.chdir(t_dir)
        self.curr_dir = Path.cwd()
        self.menu = get_directories(self.curr_dir) + get_files(self.curr_dir)
        self.curr_row = 0
        return
    
    def print_screen(self, menu):
        self.stdscr.erase()
        for i, row in enumerate(menu[self.min_row:self.min_row + self.max_lines_per_page]):
            if i == self.curr_row:
                self.stdscr.addstr(i,0, row, curses.color_pair(1))            
            else:
                self.stdscr.addstr(i,0, row)
        self.stdscr.refresh()

def get_files(dir: str):
    files = next(os.walk(dir))[2]
    return files
    
def get_directories(dir: str):
    dir = next(os.walk(dir))[1]
    dir.insert(0, '..')
    return dir

def create_delete_file(Object):

    if Path.is_dir(Path(Object.root).joinpath('deletion')):
        os.chdir('./deletion')
        write_to_file_delete(Object)
    else:
        Path.mkdir(Path(Object.root).joinpath('deletion'))
        os.chdir('./deletion')
        write_to_file_delete(Object)
    return

def write_to_file_delete(Object):
    file_object = open('files-to-delete.txt', 'w')
    for i in Object.to_delete:
        file_object.write(i + '\n')
    file_object.close()

def main():
    start_folder = Path.cwd()
    test = FileNavigator(start_folder)
    test.run_program()
    os.chdir(test.root)
    create_delete_file(test)

if __name__=='__main__':
    main()