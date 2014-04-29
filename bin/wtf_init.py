#!/usr/bin/env python
##########################################################################
# This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

from __future__ import print_function

from optparse import OptionParser
import os.path

import wtframework
from wtframework.wtf._devtools_.filetemplates import _default_yaml_, \
    _root_folder_placeholder_, _runtests_py_, _examples_


################# UTILITY METHODS ######################
def ensure_dir(dir_path): 
    if not os.path.exists(dir_path):
        print("Creating {0}".format(dir_path))
        os.makedirs(dir_path)
    else: 
        print("{0} already exists".format(dir_path))

def create_file(filepath, contents, overwrite=False):
    if not os.path.exists(filepath) or overwrite:
        print("Creating {0}".format(filepath))
        text_file = open(filepath, "w")
        text_file.write(contents)
        text_file.close()
    else:
        print("{0} already exists.".format(filepath))

def create_tests_folders(tests_path):
    """Create each subdirectory and initialize the its __init__.py file."""
    tests_subdirectories = [
        ("flows", "'Put reusable multi-page flows here.'"),
        ("models", "'Put models like database abstractions here.'"),
        ("pages", "'Put your PageObjects here.'"),
        ("support", "'Put various utility functions you want to reuse here.'"),
        ("testdata", "'Put reuseable functions for generating and handling test data here.'"),
        ("tests", "'Put your high level tests here.'"),
    ]

    # Create the root level init file.
    base_init_path = os.path.join(tests_path, "__init__.py")
    base_init_content = "'Top level tests folder.  Organize your items in the subfolders below.'"
    create_file(base_init_path, base_init_content)

    # Iterate through each tuple and initialize contents.
    for subdirectory_name, init_contents in tests_subdirectories:
        subdirectory_path = os.path.join(tests_path, subdirectory_name)
        ensure_dir(subdirectory_path)

        init_path = os.path.join(subdirectory_path, "__init__.py")
        create_file(init_path, init_contents)


################# MAIN SETUP SCRIPT ######################
if __name__ == '__main__':

    # Specify params.
    usage = "usage: %prog NameOfProject [--withexamples]"
    parser = OptionParser(usage=usage)
    parser.add_option("--withexamples", action="store_true",
                      default=False, dest="examples",
                      help="Include example web test.")
    parser.add_option("--version", action="store_true",
                      default=False, dest="version_flag",
                      help="Version info.")

    (options, args) = parser.parse_args()
    
    if(options.version_flag):
        print(wtframework.__VERSION__)
        exit()

    # Handle project directory argument, or prompt to use current directory.
    if len(args) != 1:
        use_cwd = raw_input('Would you like to initialize your wtframework project here: {0}? (Y/n)'.format(os.getcwd()))
        if use_cwd.lower() in ['n', 'no']:
            exit(1)
        else:
            project_dir = os.getcwd()
    else:
        project_dir = os.getcwd() + "/" + args[0]
        ensure_dir(project_dir)

    # create folder root file
    create_file(os.path.join(project_dir, ".wtf_root_folder"), _root_folder_placeholder_.contents)
    
    # create runtest script.
    runtests_path = os.path.join(project_dir, "runtests.py")
    create_file(runtests_path, _runtests_py_.contents)
    # make file executable
    os.chmod(runtests_path, 0755)

    # Create project folders as needed
    project_subdirectories = [
        "assets", "data", "configs", "reference-screenshots", 
        "reports", "screenshots", "tests"
    ]
    for subdirectory in project_subdirectories:
        ensure_dir(os.path.join(project_dir, subdirectory))
    
    # create default config file
    create_file(os.path.join(project_dir,"configs", "default.yaml"), _default_yaml_.contents)
    
    tests_dir = os.path.join(project_dir, "tests")
    create_tests_folders(tests_dir)

    create_file(os.path.join(project_dir,"requirements.txt"), """
# Requirements.txt file
# This file contains a list of packages to be installed by PIP
# when setting up this project.

# Wiredrive Test Framework - WTF
wtframework=={version}

    """.format(version=wtframework.__VERSION__))

    if options.examples == True:
        print("Generating example files.")

        for key in _examples_.examples.keys():
            create_file( os.path.join(project_dir,key), _examples_.examples[key], overwrite=True)



