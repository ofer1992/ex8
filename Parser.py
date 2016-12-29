import re
from Commands import Commands as C

ARITHMETIC = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}


class Parser(object):
    __COMMENT_REGEX = re.compile(r"//.*")
    __BLANK_LINE_REGEX = re.compile(r"^\s+$")

    def __init__(self, filename):
        self.f = open(filename)
        self.current_command = ''

    def __peek(self):
        """
        Checks what the next line is without moving past it
        :return: the next line
        """
        loc = self.f.tell()
        line = self.f.readline()
        self.f.seek(loc)
        return line


    def hasMoreCommands(self):
        """
        Tests if there are lines left in script
        :return: true iff there are more lines
        """
        next_line = self.__peek()
        if next_line == "": return False
        next_line = re.sub(self.__COMMENT_REGEX, "", next_line)
        next_line = re.sub(self.__BLANK_LINE_REGEX, "", next_line)
        if next_line == "":
            self.f.readline()
            return self.hasMoreCommands()
        else:
            return True

    def advance(self):
        """
        Move parser to the next line.
        It removes all white space and comments in the process.
        If the remaining text is empty, it calls itself again.
        :return:
        """
        self.current_command = self.f.readline()

    def commandType(self):
        """
        Returns the current line's command type
        :return:
        """
        command = self.current_command.split()
        if command[0] in ARITHMETIC:
            return C.C_ARITHMETIC
        elif command[0] == "push":
            return C.C_PUSH
        elif command[0] == "pop":
            return C.C_POP
        else:
            return -1

    def arg1(self):
        """
        Returns the first argument given. If called while parsing an arithmetic command, returns the name of the
        arithmetic command.
        :return:
        """
        command = self.current_command.split()
        if command[0] in ARITHMETIC:
            return command[0]
        return command[1]

    def arg2(self):
        """
        Returns the second argument given. Should not be called if not parsing a POP/PUSH command.
        :return:
        """
        command = self.current_command.split()
        return command[2]




