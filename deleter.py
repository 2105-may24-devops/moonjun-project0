from pathlib import Path
from project_logging import ProjectLogging
import shutil
import os

class Deleter():

    # Has only one property that holds the list of paths read from files-to-delete.txt
    def __init__(self):

        self.deletion_list = []
        self.d_option = False
    
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

    # Delete all paths in deletion_list and ask user for input.
    def delete_from_list(self):
        p_log = ProjectLogging()

        # if -d option is given, it will skip the prompt.
        if self.d_option and Path.is_dir(Path.cwd().joinpath('logs')):
            self.delete_loop(p_log)
            return
        elif self.d_option and Path.is_dir(Path.cwd().joinpath('logs')) == False:
            Path.mkdir(Path.cwd().joinpath('logs'))
            self.delete_loop(p_log)

        flag = input('Are you sure you want to delete? [Y/n]: ')

        # if -d option was not given.
        if flag == 'Y':
            
            if Path.is_dir(Path.cwd().joinpath('logs')):
                self.delete_loop(p_log)

            else:
                Path.mkdir(Path.cwd().joinpath('logs'))
                self.delete_loop(p_log)
      
        elif flag == 'n':
            print("No files were deleted.")
        else:
            print('Incorrect input. Try again.')
        return

    # Deletes files and directories with the builtin Path or shutil modules.
    # Dangerous. Please know what you are deleting.
    def delete_loop(self, p_log):
        
        os.chdir('./logs')

        # Logging class to log what is being deleted.
        p_log.write_log(self.deletion_list)

        for i in self.deletion_list:
            if Path.is_dir(Path(i)):
                shutil.rmtree(Path(i), ignore_errors=True)
            elif Path.is_file(Path(i)):
                Path.unlink(Path(i))
