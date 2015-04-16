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

