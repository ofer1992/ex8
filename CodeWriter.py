from enum import Enum

class Commands(Enum):
    C_PUSH = 1
    C_POP = 2

class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    file_name = "Default"

    def __init__(self, output):
        """
        Opens the output file/stream and gets ready to write into it.
        :param output: The output file/stream
        """
        self.output = output
        #self.output.write("@256\nD=A\n@SP\nM=D\n")

    def set_filename(self, file_name):
        """
        Infroms the code writer that the translation of a new VM file is started.
        :param file_name:
        """
        self.file_name = file_name

    def write_arithmetic(self, command):
        """
        Writes the assembly code that is the translation of the given arithmetic command.
        :param command: A VM command
        """
        commands = {'add': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D+M\nM=D\n'
                    ,'sub': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\nM=D\n'
                    ,'neg': '@SP\nA=M\nM=-M\n'
                    ,'eq':  '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\n@EQ\nD;JEQ\n@SP\nA=M-1\nM=0\n@NEQ\n0;JMP\n(EQ)\n@SP\nA=M-1\nM=-1\n(NEQ)\n'
                    ,'gt':  '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\n@GT\nD;JGT\n@SP\nA=M-1\nM=0\n@NGT\n0;JMP\n(GT)\n@SP\nA=M-1\nM=-1\n(NGT)\n'
                    ,'lt': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\n@LT\nD;JLT\n@SP\nA=M-1\nM=0\n@NLT\n0;JMP\n(LT)\n@SP\nA=M-1\nM=-1\n(NLT)\n'
                    , 'and': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D&M\nM=D\n'
                    ,'or': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D|M\nM=D\n'
                    ,'not': '@SP\nA=M\nM=!M\n'}
        self.output.write(commands[command])


    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or
        C_POP.
        :param command: C_PUSH or C_POP (Enum?)
        :param segment: String
        :param index: int
        """
        push_segments = {'constant': '',
                    'argument': '@ARG\nA=M+D\n',
                    'local': '@LCL\nA=M+D\n',
                    'this': '@THIS\nA=M+D\n',
                    'that': '@THAT\nA=M+D\n',
                    'pointer': '@R3\nA=A+D\n',
                    'temp': '@R5\nA=A+D\n',
                    'static': '@'+self.file_name+".{0}\nD=M\n".format(index)}
        pop_segments = {'argument': '@ARG\nD=D+M\n',
                        'local': '@LCL\nD=D+M\n',
                        'this': '@THIS\n\nD=D+M\n',
                        'that': '@THAT\n\nD=D+M\n',
                        'pointer': '@R3\nD=D+A\n',
                        'temp': '@R5\nD=D+A\n',
                        'static': '@'+self.file_name+".{0}\nD=A\n".format(index)}

        set_value = 'D=M\n' if segment is not 'constant' else ''
        set_index = "@{0}\nD=A\n".format(index)

        if command is Commands.C_PUSH:
            self.output.write(set_index+push_segments[segment]+set_value+"@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        elif command is Commands.C_POP:
            self.output.write(set_index+pop_segments[segment]+"@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n")
