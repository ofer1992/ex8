import re
from Commands import Commands as C

ARITHMETIC = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}


class Parser(object):
    __COMMENT_REGEX = re.compile(r"//.*")
    __SPACE_REGEX = re.compile(r"^\s+$")

    def __init__(self, filename):
        # self.location = -1
        self.f = open(filename)
        # self.filename = filename
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

    # def resetLoc(self):
    #     """
    #     Returns parser to the beginning of the file.
    #     :return:
    #     """
    #     self.f.seek(0)

    def hasMoreCommands(self):
        """
        Tests if there are lines left in script
        :return: true iff there are more lines
        """
        return self.__peek() != ""

    def advance(self):
        """
        Move parser to the next line.
        It removes all white space and comments in the process.
        If the remaining text is empty, it calls itself again.
        :return:
        """
        self.current_command = self.f.readline()
        self.current_command = re.sub(self.__COMMENT_REGEX, "", self.current_command)
        self.current_command = re.sub(self.__SPACE_REGEX, "", self.current_command)
        print(self.current_command)
        if self.current_command == "": self.advance()
    #
    # def hasMoreCommands(self):
    #     loc = self.f.tell()
    #     if loc != self.location:
    #         self.location = loc
    #         return True
    #     else:
    #         return False
    #
    # def advance(self):
    #     return self.f.readline().strip()

    def commandType(self):
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
        command = self.current_command.split()
        # print(self.current_command)
        # print(command)
        if command[0] in ARITHMETIC:
            return command[0]
        return command[1]

    def arg2(self):
        command = self.current_command.split()
        return command[2]




