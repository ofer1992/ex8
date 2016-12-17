import sys
from os.path import isfile, join, splitext
from os import listdir
from Parser import Parser
from CodeWriter import CodeWriter
from Commands import Commands as C
import os

OUTPUT_FILE_SUFFIX = '.asm'
INPUT_FILE_SUFFIX = "vm"


def process(parser, codewriter):
    """
    Parses file and generates assembly code
    :param codewriter: CodeWriter object
    :param parser: Current file's parser
    :return:
    """

    while parser.hasMoreCommands():
        parser.advance()
        command = parser.commandType()
        if command is C.C_PUSH or command is C.C_POP:
            arg1 = parser.arg1()
            arg2 = parser.arg2()
            codewriter.write_push_pop(command,arg1,arg2)
        elif command is C.C_ARITHMETIC:
            operator = parser.arg1()
            codewriter.write_arithmetic(operator)
        else:
            print("unexpected")


def main():
    """
    The main method. Checks for valid input.
    Executes parsing on given file/dir and uses the codeWriter to create an assembly
    file in given path.
    :return:
    """
    if len(sys.argv) != 2:
        print("This script takes 1 argument: a filename or a directory name.")
        return

    current_path = sys.argv[1]

    if isfile(current_path):
        if not current_path.endswith(INPUT_FILE_SUFFIX):
            print("Not an asm file.")
            return
        vm_files = [current_path]
        current_path = current_path[:-3]+OUTPUT_FILE_SUFFIX

    else:
        if not current_path.endswith('/'):
            current_path += '/'
        vm_files = [current_path + f for f in listdir(current_path) if isfile(join(current_path, f))
                    and f.endswith(INPUT_FILE_SUFFIX)]
        dir_name = current_path.split('/')
        output_name = dir_name[-2]
        current_path += output_name + OUTPUT_FILE_SUFFIX

    if not vm_files:
        print("No files with the .vm file extension found.")
        return

    code_writer = CodeWriter(open(current_path, 'w'))

    for file in vm_files:
        curr_parser = Parser(file)
        filename = file.split('/')[-1]
        filename = filename[:filename.rfind('.')]
        code_writer.set_filename(filename)
        process(curr_parser, code_writer)

    code_writer.close()

if __name__ == "__main__":
    main()
