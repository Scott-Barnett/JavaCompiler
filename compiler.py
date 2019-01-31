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
    with open(filename, 'r') as f:
        data = f.read()
    curdir = os.listdir('./')
    newf = []
    for f in range(len(curdir)):
        if curdir[f][-4:] == "java":
            if curdir[f] not in files and data.find(curdir[f][:-5]) != -1:
                newf.append(curdir[f])
    files.extend(newf)
    for f in newf:
        get_list_of_files(f, files)
    return files

for f in get_list_of_files(filePath, [filePath]):
    subprocess.call(["javac",f])