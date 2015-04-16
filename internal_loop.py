from utils import find_tail_call
import opcode


absolute_jump_opcodes = set((
    opcode.opmap['JUMP_ABSOLUTE'], 
    opcode.opmap['POP_JUMP_IF_TRUE'], 
    opcode.opmap['POP_JUMP_IF_FALSE'], 
    opcode.opmap['JUMP_IF_TRUE_OR_POP'], 
    opcode.opmap['JUMP_IF_FALSE_OR_POP'], 
))

def fix_absolute_jumps(opcodes, offset):
    new_opcodes = ""
    i = 0
    while i < len(opcodes):
        op = ord(opcodes[i])
        if op < opcode.HAVE_ARGUMENT: #90, as mentioned earlier
            new_opcodes += opcodes[i]
            i += 1
        else:
            if op in absolute_jump_opcodes:
                new_opcodes += opcodes[i] + chr(ord(opcodes[i+1])+offset) + opcodes[i+2]
            else:
                new_opcodes += opcodes[i:i+3]
            i += 3
    return new_opcodes
            
def internal_loop(fxn):
    fco = fxn.__code__
    opcodes = fco.co_code
    arg_count = fco.co_argcount
    opcode_offset = 0
    NULL = chr(0)
    for fxn_load, fxn_call, cur_num_args in find_tail_call(fxn):
        if cur_num_args > arg_count:
            print "Cannot tail call optimize functions with variadic parameters"
            continue
        fxn_load += opcode_offset
        fxn_call += opcode_offset
        store_fast_args = "".join([
            chr(opcode.opmap['STORE_FAST']) + \
            chr(var_idx) + \
            NULL
            for var_idx in xrange(cur_num_args)
        ])
        prev_opcode_lenth = len(opcodes)
        opcodes = opcodes[:fxn_load] + \
                  opcodes[fxn_load+3:fxn_call] + \
                  chr(opcode.opmap['BUILD_TUPLE']) + \
                  chr(cur_num_args) + \
                  NULL + \
                  chr(opcode.opmap['UNPACK_SEQUENCE']) + \
                  chr(cur_num_args) + \
                  NULL + \
                  store_fast_args + \
                  opcodes[fxn_call+8:] + \
                  chr(opcode.opmap['JUMP_ABSOLUTE']) + \
                  chr(0) + \
                  NULL
        opcode_offset = len(opcodes) - prev_opcode_lenth

    # we are adding 9 opcodes but must loop until the last 3
    # opcodes, ergo the offset of 6
    opcodes = chr(opcode.opmap['SETUP_LOOP']) + \
              chr(len(opcodes)) + \
              NULL + \
              fix_absolute_jumps(opcodes, 3) + \
              chr(opcode.opmap['POP_BLOCK']) + \
              chr(opcode.opmap['LOAD_CONST']) + \
              chr(0) + \
              NULL + \
              chr(opcode.opmap['RETURN_VALUE'])

    fxn.__code__ = type(fco)(
        fco.co_argcount,
        fco.co_nlocals,
        fco.co_stacksize,
        fco.co_flags,
        bytes(opcodes),
        fco.co_consts,
        fco.co_names,
        fco.co_varnames,
        fco.co_filename,
        fco.co_name,
        fco.co_firstlineno,
        fco.co_lnotab,
        fco.co_freevars,
        fco.co_cellvars
    )
    return fxn

@internal_loop
def fib(i, current = 0, next = 1):
    if i == 0:
        return current
    else:
        return fib(i - 1, next, current + next)

