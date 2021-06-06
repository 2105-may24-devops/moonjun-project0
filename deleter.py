from pathlib import Path
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

    def delete_from_list(self):
        flag = input('Are you sure you want to delete? [Y/n]: ')
        if flag == 'Y':
            for i in self.deletion_list:
                print(i)
                if Path.is_dir(Path(i)):
                    shutil.rmtree(Path(i), ignore_errors=True)
                elif Path.is_file(Path(i)):
                    Path.unlink(Path(i))
        elif flag == 'n':
            print("No files were deleted.")
        else:
            print('Incorrect input. Try again.')
