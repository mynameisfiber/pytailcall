```
$ python benchmark.py 
Testing all functions work
Testing with very small N so we can see overheads
true_recursion  : 0.00179576873779 ms/call 
unrecursed      : 0.00148391723633 ms/call (1.21015424165x speedup)
pure_python     : 0.0193719863892 ms/call (0.0926992566337x speedup)
partial_func    : 0.00718784332275 ms/call (0.249834151519x speedup)
return_tuple    : 0.00528430938721 ms/call (0.339830355531x speedup)
internal_loop   : 0.000999450683594 ms/call (1.79675572519x speedup)
Testing with small N so we can compare with real recursion
true_recursion  : 0.371507644653 ms/call 
unrecursed      : 0.204587936401 ms/call (1.81588245714x speedup)
pure_python     : 3.21255588531 ms/call (0.115642391266x speedup)
partial_func    : 0.763095855713 ms/call (0.486842697247x speedup)
return_tuple    : 0.696663856506 ms/call (0.533266712754x speedup)
internal_loop   : 0.161427497864 ms/call (2.30139009506x speedup)
Testing with large N
unrecursed      : 2.04267978668 ms/call 
pure_python     : 22.5751781464 ms/call 
partial_func    : 5.73617935181 ms/call 
return_tuple    : 5.29965877533 ms/call 
internal_loop   : 1.74531936646 ms/call 
```

Useful references

- http://www.jonathon-vogel.com/posts/patching_function_bytecode_with_python/
- https://docs.python.org/2/library/dis.html
- http://unpyc.sourceforge.net/Opcodes.html
