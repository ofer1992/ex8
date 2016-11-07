import CodeWriter

PUSH = CodeWriter.Commands.C_PUSH
POP = CodeWriter.Commands.C_POP
f = open('../../MemoryAccess/PointerTest/PointerTest.asm','w')
cw = CodeWriter.CodeWriter(f)

cw.write_push_pop(PUSH,'constant',3030)
cw.write_push_pop(POP,'pointer',0)
cw.write_push_pop(PUSH,'constant',3040)
cw.write_push_pop(POP,'pointer',1)
cw.write_push_pop(PUSH,'constant',32)
cw.write_push_pop(POP,'this',2)
cw.write_push_pop(PUSH,'constant',46)
cw.write_push_pop(POP,'that',6)
cw.write_push_pop(PUSH,'pointer',0)
cw.write_push_pop(PUSH,'pointer',1)
cw.write_arithmetic('add')
cw.write_push_pop(PUSH,'this',2)
cw.write_arithmetic('sub')
cw.write_push_pop(PUSH,'that',6)
cw.write_arithmetic('add')
