from pathlib import Path
from project_logging import ProjectLogging
import shutil
import os

class Deleter():

    def __init__(self):

        self.deletion_list = []
    
    def read_file(self, file):
        os.chdir('./deletion')
        files_to_delete = Path.cwd() / file
        if Path.is_file(files_to_delete):
            with open(str(files_to_delete), 'r') as f:
                for line in f:
                    line = line.strip()
                    self.deletion_list.append(line)
            f.close()
        os.chdir('../')
        return

    def delete_from_list(self):
        flag = input('Are you sure you want to delete? [Y/n]: ')
        if flag == 'Y':
            p_log = ProjectLogging()
            if Path.is_dir(Path.cwd().joinpath('logs')):
                os.chdir('./logs')
                p_log.write_log(self.deletion_list)
                self.delete_loop()
            else:
                Path.mkdir(Path.cwd().joinpath('logs'))
                print(Path.cwd())
                os.chdir('./logs')
                p_log.write_log(self.deletion_list)
                self.delete_loop()
                
        elif flag == 'n':
            print("No files were deleted.")
        else:
            print('Incorrect input. Try again.')
        return

    def delete_loop(self):
        for i in self.deletion_list:
            if Path.is_dir(Path(i)):
                shutil.rmtree(Path(i), ignore_errors=True)
            elif Path.is_file(Path(i)):
                Path.unlink(Path(i))
