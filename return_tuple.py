from utils import find_tail_call
import opcode

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
                num_args = opcodes[i+1] + opcodes[i+2]
                yield (fxn_loaded_idx, i, num_args)
        if cur_code < opcode.HAVE_ARGUMENT: #90, as mentioned earlier
            i += 1
        else:
            i += 3

def replace_recurse(fxn):
    fco = fxn.__code__
    opcodes = fco.co_code
    # none_loc should always be 0, but check just incase
    none_loc = fco.co_consts.index(None)
    for fxn_load, fxn_call, num_args in find_tail_call(fxn):
        # first delete the loading of the current function
        opcodes = opcodes[:fxn_load] + \
                  opcodes[fxn_load+3:fxn_call] + \
                  chr(opcode.opmap['LOAD_CONST']) + \
                  chr(none_loc) + \
                  chr(opcode.opmap['STOP_CODE']) + \
                  chr(opcode.opmap['BUILD_TUPLE']) + \
                  chr(num_args + 1) + \
                  chr(opcode.opmap['STOP_CODE']) + \
                  opcodes[fxn_call+3:]

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
    def wrapper(*args):
        repeat = True
        while repeat:
            result = fxn(*args)
            if isinstance(result, tuple) and result[-1] is None:
                args = result[:-1]
            else:
                repeat = False
        return result
    return wrapper

@replace_recurse
def fib(i, current = 0, next = 1):
  if i == 0:
    return current
  else:
    return fib(i - 1, next, current + next)
