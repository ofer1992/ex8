class CodeWriter:
    """Translates VM commands into Hack assembly code."""
    filename = ""

    def __init__(self, output):
        """
        Opens the output file/stream and gets ready to write into it.
        :param output: The output file/stream
        """
        self.output = output

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
        commands = {'add': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D+M\nM=D\n\n'
                    ,'sub': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\nM=D\n\n'
                    ,'neg': '@SP\nA=M\nM=-M\n'
                    ,'eq':  '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=D-M\n@EQ\nD;JEQ\n@SP\nA=M-1\nM=0\n@NEQ\n0;JMP\n(EQ)\n@SP\nA=M-1\nM=-1\n(NEQ)\n'
                    ,'gt':  '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\n@GT\nD;JGT\n@SP\nA=M-1\nM=0\n@NGT\n0;JMP\n(GT)\n@SP\nA=M-1\nM=-1\n(NGT)\n'
                    ,'lt': '@SP\nA=M-1\nD=M\n@SP\nM=M-1\nA=M-1\nD=M-D\n@LT\nD;JLT\n@SP\nA=M-1\nM=0\n@NLT\n0;JMP\n(LT)\n@SP\nA=M-1\nM=-1\n(NLT)\n'
                    , 'and': ""
                    ,'or': ""
                    ,'not': ""}
        self.output.write()


    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command, where command is either C_PUSH or
        C_POP.
        :param command: C_PUSH or C_POP (Enum?)
        :param segment: String
        :param index: int
        """