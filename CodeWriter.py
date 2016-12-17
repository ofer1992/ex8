from Commands import Commands as C


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output):
        """
        Opens the output file/stream and gets ready to write into it.
        :param output: The output file/stream
        """
        self.output = output
        self.file_name = ""
        self.commands = {}
        command_names = ['add','sub','neg','eq','gt','lt','and','or','not']
        for command in command_names:
            with open(command, 'r') as myfile:
                self.commands[command] = myfile.read()

    def set_filename(self, file_name):
        """
        Informs the code writer that the translation of a new VM file is started.
        :param file_name:
        """
        self.file_name = file_name

    def write_arithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given arithmetic command.
        :param command: A VM command
        """
        self.output.write(self.commands[command])

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or
        C_POP.
        :param command: C_PUSH or C_POP
        :param segment: String
        :param index: int
        :return:
        """
        shortcuts = {'argument': 'ARG', 'local': 'LCL', 'this': 'THIS', 'that': 'THAT', 'pointer': '3',
                     'temp': '5', 'constant': '', 'static': ''}
        if command is C.C_PUSH:
            push_code = "@SP\nA=M\nM=D\n@SP\nM=M+1\n"

            # Segment is this, that, arguments or local
            case_a = "@{0}\nD=A\n@{1}\nA=D+M\nD=M\n".format(index,shortcuts[segment])
            # Segment is pointer or temp
            case_b = "@{0}\nD=A\n@{1}\nA=D+A\nD=M\n".format(index,shortcuts[segment])
            # Segment is constant
            case_c = "@{0}\nD=A\n".format(index)
            # Segment is static
            case_d = "@{0}.{1}\nD=M\n".format(self.file_name,index)

            segments = {'argument': case_a,
                        'local': case_a,
                        'this': case_a,
                        'that': case_a,
                        'pointer': case_b,
                        'temp': case_b,
                        'constant': case_c,
                        'static': case_d}

            self.output.write(segments[segment]+push_code)

        elif command is C.C_POP:
            pop_code = "@SP\nM=M-1\nA=M\nD=M\n@R15\nA=M\nM=D\n"

            # Segment is this, that, arguments or local
            case_a = "@{0}\nD=A\n@{1}\nD=D+M\n@R15\nM=D\n".format(index,shortcuts[segment])
            # Segment is pointer or temp
            case_b = "@{0}\nD=A\n@{1}\nD=D+A\n@R15\nM=D\n".format(index, shortcuts[segment])
            # Segment is static
            case_c = "@{0}.{1}\nD=A\n@R15\nM=D\n".format(self.file_name,index)

            segments = {'argument': case_a,
                        'local': case_a,
                        'this': case_a,
                        'that': case_a,
                        'pointer': case_b,
                        'temp': case_b,
                        'static': case_c}

            self.output.write(segments[segment]+pop_code)

    def close(self):
        self.output.close()
