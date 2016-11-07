import CodeWriter

PUSH = CodeWriter.Commands.C_PUSH
POP = CodeWriter.Commands.C_POP
f = open('../../MemoryAccess/StaticTest/StaticTest.asm','w')
cw = CodeWriter.CodeWriter(f)

cw.write_push_pop(PUSH,'constant',111)
cw.write_push_pop(PUSH,'constant',333)
cw.write_push_pop(PUSH,'constant',888)
cw.write_push_pop(POP,'static',8)
cw.write_push_pop(POP,'static',3)
cw.write_push_pop(POP,'static',1)
cw.write_push_pop(PUSH,'static',3)
cw.write_push_pop(PUSH,'static',1)
cw.write_arithmetic('sub')
cw.write_push_pop(PUSH,'static',8)
cw.write_arithmetic('add')
