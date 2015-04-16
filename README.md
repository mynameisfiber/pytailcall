```
$ python2.7 benchmark.py 
Testing all functions work
Testing with small N so we can compare with real recursion
true_recursion  : 0.152552604675 ms/call 
pure_python     : 1.39134788513 ms/call (0.10964375359x speedup)
return_tuple    : 0.295040130615 ms/call (0.517057135099x speedup)
internal_loop   : 0.0935878753662 ms/call (1.63004667088x speedup)
Testing with large N
pure_python     : 9.72774028778 ms/call 
return_tuple    : 2.22536087036 ms/call 
internal_loop   : 0.899343490601 ms/call 
```
