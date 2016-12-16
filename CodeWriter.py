from Commands import Commands as C

class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output):
        """
        Opens the output file/stream and gets ready to write into it.
        :param output: The output file/stream
        """
        self.output = output
        # self.output.write("@256\nD=A\n@SP\nM=D\n")
        self.file_name = ""

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
        commands = {'add': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D+M\nM=D\n'
                    ,'sub': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\nM=D\n'
                    ,'neg': '@SP\nA=M-1\nM=-M\n'
                    ,'eq':  '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\nA=D\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=A>>\nD=D|A\nA=1\nD=D&A\n@SP\nA=M-1\nM=-D\n'
                    ,'gt':  '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nM=D\n\n'
                    ,'lt': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nD=D>>\nM=D\n\n'
                    , 'and': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D&M\nM=D\n'
                    ,'or': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D|M\nM=D\n'
                    ,'not': '@SP\nA=M-1\nM=!M\n'}
        self.output.write(commands[command])

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or
        C_POP.
        :param command: C_PUSH or C_POP
        :param segment: String
        :param index: int
        """
        segments = {'constant': '',
                    'argument': '@ARG\nA=M+D\n',
                    'local': '@LCL\nA=M+D\n',
                    'this': '@THIS\nA=M+D\n',
                    'that': '@THAT\nA=M+D\n',
                    'pointer': '@3\nA=A+D\n',
                    'temp': '@5\nA=A+D\n'}
        shortcuts = {'argument': 'ARG', 'local': 'LCL', 'this': 'THIS\nA=M', 'that': 'THAT\nA=M', 'pointer': '3',
                     'temp': '5'}

        #TODO: Figure out why commented form isn't working, get rid of double D=A
        # set_value = 'D=A\n' if segment is 'constant' else 'D=M\n'
        set_value = '' if segment is 'constant' else 'D=M\n'
        set_index = "@{0}\nD=A\n"

        if command is C.C_PUSH:
            self.output.write(set_index.format(index)+segments[segment]+set_value+"@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        elif command is C.C_POP:
            self.output.write((set_index+'@').format(index)+shortcuts[segment]
                + '\nD=D+A\n@R15\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R15\nA=M\nM=D\n')
