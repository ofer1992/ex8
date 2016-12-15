import sys
from os.path import isfile, join, splitext
from os import listdir
from Parser import Parser
from CodeWriter import CodeWriter
from Commands import Commands as C

VM = "vm"  # expected file ext


def process(parser, codewriter):
    """
    Parses file and generates assembly code
    :param codewriter: CodeWriter object
    :param parser: Current file's parser
    :return:
    """
    while(parser.hasMoreCommands()):
        parser.advance()
        command = parser.commandType()
        if command is C.C_PUSH or command is C.C_PUSH:
            arg1 = parser.arg1()
            arg2 = parser.arg2()
            codewriter.write_push_pop(command,arg1,arg2)
        elif command is C.C_ARITHMETIC:
            operator = parser.arg1()
            codewriter.write_arithmetic(operator)


def main():
    if len(sys.argv) != 2:
        print("This script takes 1 arg: a filename or a directory name.")
        return 1

    current_path = sys.argv[1]

    if isfile(current_path):
        vm_files = [current_path]

    else:
        if not current_path.endswith('/'):
            current_path += '/'

        vm_files = [current_path+f for f in listdir(current_path) if isfile(join(current_path, f)) and f.endswith(VM)]
    if not vm_files:
        print("No files with the .vm file extension found.")
        return 1

    code_writer = CodeWriter(open("test.asm",'w')) #TODO: Make it better
    for file in vm_files:
        print(file)
        p = Parser(file)
        process(p,code_writer)



if __name__ == "__main__":
    main()
