from utils import find_tail_call, update_function_code
import opcode


absolute_jump_opcodes = set((
    opcode.opmap['JUMP_ABSOLUTE'], 
    opcode.opmap['POP_JUMP_IF_TRUE'], 
    opcode.opmap['POP_JUMP_IF_FALSE'], 
    opcode.opmap['JUMP_IF_TRUE_OR_POP'], 
    opcode.opmap['JUMP_IF_FALSE_OR_POP'], 
))

def fix_absolute_jumps(opcodes, offsets):
    """
    When we mess with the bytecode and change offsets, any jumps that use
    absolute bytecode positions will be messed up.  This will go through and
    add relevant offsets to any absolute bytecode positions.
    """
    new_opcodes = ""
    i = 0
    while i < len(opcodes):
        op = ord(opcodes[i])
        if op < opcode.HAVE_ARGUMENT: #90, as mentioned earlier
            new_opcodes += opcodes[i]
            i += 1
        else:
            if op in absolute_jump_opcodes:
                jump_to = ord(opcodes[i+1])
                offset = sum(off[1] for off in offsets if off[0] <= jump_to)
                print "changing {} => {}".format(jump_to, jump_to+offset)
                new_opcodes += opcodes[i] + chr(ord(opcodes[i+1])+offset) + opcodes[i+2]
            else:
                new_opcodes += opcodes[i:i+3]
            i += 3
    return new_opcodes
            
def internal_loop(fxn):
    fco = fxn.__code__
    opcodes = fco.co_code
    arg_count = fco.co_argcount
    NULL = chr(0)
    new_opcodes = ""
    last_idx = 0
    jump_offsets = []
    for fxn_load, fxn_call, cur_num_args in find_tail_call(fxn):
        if cur_num_args > arg_count:
            print "Cannot tail call optimize functions with variadic parameters"
            continue
        # create the tuple expansion of the first `cur_num_args` arguments to
        # the function
        store_fast_args = "".join([
            chr(opcode.opmap['STORE_FAST']) + \
            chr(var_idx) + \
            NULL
            for var_idx in xrange(cur_num_args)
        ])

        # load up actual code
        new_opcodes += opcodes[last_idx:fxn_load]

        # skip over the loading of the recursed function onto the stack
        jump_offsets.append((fxn_load, -3))
        new_opcodes += opcodes[fxn_load+3:fxn_call]

        # now we replace the function call with building a tuple from the
        # arguments that would have been used when calling the function.  This
        # then gets unpacked into co_names which holds the current function
        # parameters and we finally do an absolute jump to the beginning of the
        # function to start it all over again!
        # NOTE: offset is 5 here because we add 9 extra opcodes, but then
        # remove 4 when updating `last_idx`
        jump_offsets.append((fxn_call, 5 + len(store_fast_args)))
        new_opcodes += chr(opcode.opmap['BUILD_TUPLE']) + \
                       chr(cur_num_args) + \
                       NULL + \
                       chr(opcode.opmap['UNPACK_SEQUENCE']) + \
                       chr(cur_num_args) + \
                       NULL + \
                       store_fast_args
        new_opcodes += chr(opcode.opmap['JUMP_ABSOLUTE']) + \
                       chr(0) + \
                       NULL
        last_idx = fxn_call+4
    new_opcodes += opcodes[last_idx:]
    new_opcodes = fix_absolute_jumps(new_opcodes, jump_offsets)
    fxn = update_function_code(fxn, new_opcodes)
    return fxn

@internal_loop
def fib(i, current = 0, next = 1):
    if i > 0:
        return fib(i - 1, next, current + next)
    elif i == 0:
        return current
