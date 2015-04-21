from utils import find_tail_call, update_function_code
import opcode


def replace_recurse(fxn):
    fco = fxn.__code__
    opcodes = fco.co_code
    # none_loc should always be 0, but check just incase
    none_loc = fco.co_consts.index(None)
    NULL = chr(0)
    for fxn_load, fxn_call, num_args, num_kw_args in find_tail_call(fxn):
        if num_kw_args != 0:
            print "Current tail call optimization does not support keyword arguments in recursive call"
            continue
        # first delete the loading of the current function then replace the old
        # function call with building a new tuple using the function arguments
        # and end it with a magic None value
        opcodes = opcodes[:fxn_load] + \
                  opcodes[fxn_load+3:fxn_call] + \
                  chr(opcode.opmap['LOAD_CONST']) + \
                  chr(none_loc) + \
                  NULL + \
                  chr(opcode.opmap['BUILD_TUPLE']) + \
                  chr(num_args + 1) + \
                  NULL + \
                  opcodes[fxn_call+3:]
    fxn = update_function_code(fxn, opcodes)
    def wrapper(*args):
        repeat = True
        while repeat:
            result = fxn(*args)
            # if the returned value was a tuple with a None as the last value,
            # we know it was the magic value returned form our hacked bytecode.
            # This tuple actually contains the new arguments to the "recursed"
            # function call.
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
