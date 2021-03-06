import opcode
from copy import deepcopy

def find_tail_call(fxn):
    i = 0
    self_reference_id = fxn.__code__.co_names.index(fxn.__code__.co_name)
    opcodes = [ord(o) for o in fxn.__code__.co_code]
    fxn_loaded = []
    while i < len(opcodes):
        cur_code = opcodes[i]
        if cur_code == opcode.opmap['LOAD_GLOBAL']:
            fxn_loaded.append((i, opcodes[i+1] == self_reference_id))
        elif cur_code == opcode.opmap['CALL_FUNCTION'] and fxn_loaded:
            fxn_loaded_idx, is_self = fxn_loaded.pop()
            if is_self and opcodes[i+3] == opcode.opmap['RETURN_VALUE']:
                num_pos_args = opcodes[i+1]
                num_kw_args = opcodes[i+2]
                yield (fxn_loaded_idx, i, num_pos_args, num_kw_args)
        if cur_code < opcode.HAVE_ARGUMENT:
            i += 1
        else:
            i += 3

def update_function_code(fxn, code):
    fco = fxn.__code__
    new_code = type(fco)(
        fco.co_argcount,
        fco.co_nlocals,
        fco.co_stacksize,
        fco.co_flags,
        bytes(code),
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
    new_fxn = type(fxn)(
        new_code,
        fxn.func_globals,
        fxn.func_name,
        fxn.func_defaults,
        fxn.func_closure
    )
    return new_fxn
