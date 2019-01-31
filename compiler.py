#!/usr/bin/env python3
import os,sys, subprocess

headers = ['new','implements','inherits', 'class']
bracket_types = {'(':')','<':'>'}

def invalid_file_argument():
    print("Usage: ./compiler.py <java file>")
    sys.exit(1)

def get_file_contents(filepath):
    with open(filepath,'r') as open_file:
        data = open_file.readlines()
    for line in range(len(data)):
        commentstart = data[line].find('//')
        data[line] = data[line][:commentstart]
    data = '\n'.join(data)
    multiline_comment_start = data.find('/*')
    while multiline_comment_start != -1:
        comment_end = data.find('*/',multiline_comment_start) + 2
        data = data[:multiline_comment_start] + data[comment_end:]
        multiline_comment_start = data.find('/*',comment_end)
    multiline_comment_start = data.find('/**')
    while multiline_comment_start != -1:
        comment_end = data.find('*/',multiline_comment_start) + 2
        data = data[:multiline_comment_start] + data[comment_end:]
        multiline_comment_start = data.find('/**',comment_end)
    return data

def get_start_pointer(data, header, end_pointer=0):
    front_pointer = data.find(header + ' ', end_pointer)
    return front_pointer + len(header) + 1

def get_end_pointer(data, front_pointer):
    new_line = data.find('\n',front_pointer)
    semicolon = data.find(';',front_pointer)
    space = data.find(' ',front_pointer)
    returnData = [new_line, semicolon, space]
    returnData.sort()
    return returnData[0]

def remove_brackets(classname):
    for bracket in bracket_types:
        start_pointer = classname.find(bracket)
        while start_pointer != -1:
            end_pointer = len(classname) - classname[::-1].find(bracket_types[bracket])
            classname = classname[:start_pointer] + classname[end_pointer:]
            start_pointer = classname.find(bracket, start_pointer)
    return classname

def get_class_names(filename, classes=[]):
    data = get_file_contents(filename)
    for header in headers:
        front_pointer = get_start_pointer(data, header)
        while front_pointer != (-1 + len(header) + 1):
            end_pointer = get_end_pointer(data, front_pointer)
            classname = remove_brackets(data[front_pointer:end_pointer])
            if classname not in classes and os.path.isfile(classname + '.java'):
                classes.append(classname)
                get_class_names(classname + '.java', classes)
            front_pointer = get_start_pointer(data, header, end_pointer)
    return classes

if __name__ == '__main__':
    if len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]):
        invalid_file_argument()

    local_classes = get_class_names(sys.argv[1])
    for local_class in local_classes:
        print("Compiling {}".format(local_class))
        subprocess.call(['javac',local_class + '.java'])
    print("All local java files compiled")
