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
        self.current_function = ""
        self.return_counter = 1
        command_names = ['add','sub','neg','eq','gt','lt','and','or','not']
        for command in command_names:
            with open(command, 'r') as myfile:
                self.commands[command] = myfile.read()
        self.write_init()


    def write_init(self):
        """

        :return:
        """
        code = "@256\n" \
               "D=A\n" \
               "@SP\n" \
               "M=D\n"
        self.output.write(code)
        self.write_call("Sys.init",0)

    def write_label(self, label):
        """
        Writes assembly code that effects the label command.
        :param label: String representing label name
        :return:
        """
        self.labeler(self.current_function+"$"+label)

    def labeler(self,label):
        """
        Generic code to insert label in assembly
        :param label:
        :return:
        """
        self.output.write("({0})\n".format(label))

    def write_goto(self, label):
        """

        :param label:
        :return:
        """
        label = self.current_function+"$"+label
        code = "@{0}\n" \
               "0;JMP\n".format(label)
        self.output.write(code)

    def write_if(self,label):
        """

        :param label:
        :return:
        """
        label = self.current_function+"$"+label
        code = "@SP\n" \
               "M=M-1\n" \
               "A=M\n" \
               "D=M\n" \
               "@{0}\n" \
               "D;JNE\n".format(label)
        self.output.write(code)

    def write_call(self,func_name, num_args):
        return_address = "return$"+str(self.return_counter)
        push_code = "@SP\n" \
               "A=M\n" \
               "M=D\n" \
               "@SP\n" \
               "M=M+1\n"
        code = "@{0}\n" \
                "D=A\n".format(return_address) \
                +push_code+ \
               "@LCL\n" \
               "D=M\n" \
                +push_code+ \
               "@ARG\n" \
               "D=M\n" \
               +push_code+ \
               "@THIS\n" \
               "D=M\n" \
               +push_code+ \
               "@THAT\n" \
               "D=M\n" \
               +push_code+ \
               "@{0}\n" \
               "D=A\n" \
               "@5\n" \
               "D=D+A\n" \
               "@SP\n" \
               "D=M-D\n" \
               "@ARG\n" \
               "M=D\n" \
               "@SP\n" \
               "D=M\n" \
               "@LCL\n" \
               "M=D\n" \
               "@{1}\n" \
               "0;JMP\n".format(num_args,func_name)
        self.output.write(code)
        self.labeler(return_address)
        self.return_counter += 1

    def write_return(self):
        code_1 = "@LCL\n" \
               "D=M\n" \
               "@R13\n" \
               "M=D\n" \
               "@5\n" \
               "D=D-A\n" \
                 "A=D\n" \
                 "D=M\n" \
               "@R14\n" \
               "M=D\n"
        self.output.write(code_1)

        self.write_push_pop(C.C_POP,"argument",0)

        code2 = "@ARG\n" \
                "D=M+1\n" \
                "@SP\n" \
                "M=D\n" \
                "@R13\n" \
                "M=M-1\n" \
                "A=M\n" \
                "D=M\n" \
                "@THAT\n" \
                "M=D\n" \
                "@R13\n" \
                "M=M-1\n" \
                "A=M\n" \
                "D=M\n" \
                "@THIS\n" \
                "M=D\n" \
                "@R13\n" \
                "M=M-1\n" \
                "A=M\n" \
                "D=M\n" \
                "@ARG\n" \
                "M=D\n" \
                "@R13\n" \
                "M=M-1\n" \
                "A=M\n" \
                "D=M\n" \
                "@LCL\n" \
                "M=D\n" \
                "@R13\n" \
                "M=M-1\n" \
                "A=M\n" \
                "D=M\n" \
                "@R14\n" \
                "A=M\n" \
                "0;JMP\n"
        self.output.write(code2)

    def write_function(self,func_name, num_locals):
        """

        :param func_name:
        :param num_locals:
        :return:
        """
        self.current_function = func_name
        self.labeler(self.current_function)
        for i in range(num_locals):
            self.write_push_pop(C.C_PUSH,"constant",0)

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
