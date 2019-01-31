#!/usr/bin/env python3
import os,sys,subprocess

def show_argument_help():
    print("Usage: base.py <main java file>")

def show_invalid_file_error():
    print("The file specified does not exist")

arguments = sys.argv[1:]

if len(arguments) != 1:
    show_argument_help()
    sys.exit(1)

filePath = arguments[0]

if not os.path.isfile(filePath):
    show_invalid_file_error()
    sys.exit(1)

def get_list_of_files(filename, files):
    with open(filename, 'r') as file:
        file_data = file.read()
    current_dir = os.listdir('./')
    new_files = []
    for file_counter in range(len(current_dir)):
        if current_dir[file_counter][-4:] == "java":
            if current_dir[file_counter] not in files and file_data.find(current_dir[file_counter][:-5]) != -1:
                new_files.append(current_dir[file_counter])
    files.extend(new_files)
    for file in new_files:
        files = get_list_of_files(file, files)
    return files

for java_file in get_list_of_files(filePath, [filePath]):
    subprocess.call(["javac",java_file])