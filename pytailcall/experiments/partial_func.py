"""
from http://tomforb.es/adding-tail-call-optimization-to-python
"""

import functools
 
 
def tail_optimize(func):
    def _optimize_partial(*args, **kwargs):
        """
        I replace the reference to the wrapped function with a functools.partial object
        so that it doesn't actually call itself upon returning, allowing us to do it instead.
    
        Advantages: Theoretically needs no code changes and is more understandable
        Disadvantages: Its startup overhead is higher and its a bit slower. Also can only call
                       recursively when returning, so return func(1) + func(2) will not work.
        """
        old_reference = func.func_globals[func.func_name]
        func.func_globals[func.func_name] = functools.partial(functools.partial, func)
    
        to_execute = functools.partial(func, *args, **kwargs)
    
        while isinstance(to_execute, functools.partial):
            to_execute = to_execute()
    
        func.func_globals[func.func_name] = old_reference
        return to_execute

    functools.update_wrapper(_optimize_partial, func)
    return _optimize_partial
