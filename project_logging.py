from datetime import datetime
import re

# Filename format: Y-M-D-H-m-s-ms
# Creates a .txt file in the above format that logs which files were deleted.
class ProjectLogging():

    def __init__(self):
        self.filename = ''

    def write_log(self, d_list: list):
        self.filename = datetime.now()
        self.filename = re.sub("[^0-9]","", str(self.filename))
        file_object = open(self.filename + '.txt', 'w')
        file_object.write("Created: "+ str(datetime.now()) + '\n')
        file_object.write("Deleted files:\n")
        for i in d_list:
            file_object.write(i + '\n')
        file_object.close()

