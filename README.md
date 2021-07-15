# FileCurs
## Project Description
FileCurs is a file system navigation application built with Python. The application allows the user to interactively navigate their file system and mark certain files for deletion. Log files are created detailing which files are marked for deletion and which have already been deleted. The application can be tested and deployed to virtual environments with the use of automation tools.

## Technologies
* Python
* Ansible
* Azure Devops (Pipelines)
* Jenkins
* Bash

## Getting Started
**Requirements:**
* Python 3.6+
* Python3-venv
* Pip

## Usage

Run the command `python3 file_navigator.py`.

* Interactive application is run when called without any command line arguments.
* Supplying `-d` option and `files-to-delete.txt` will delete all files inside the text file. User will get prompt:
  * `Are you sure you want to delete? [Y/n]:`
* Supplying `-d` and not supplying `files-to-delete.txt` will bypass the prompt.

**Valid Interactive Inputs**
* `UP` and `DOWN` array keys to move cursor
* `ENTER` to go into a folder. (At the top of each directory is `..` to back up directory.)
* `D` to mark file/folder for deletion
* `Q` to exit program

## Contributors
Moonjun Chung

## License
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
