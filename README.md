```
$ python benchmark.py 
Testing all functions work
Testing with very small N so we can see overheads
true_recursion  : 0.00178813934326 ms/call 
unrecursed      : 0.00132465362549 ms/call (1.34989200864x speedup)
pure_python     : 0.0200395584106 ms/call (0.0892304763718x speedup)
partial_func    : 0.00706005096436 ms/call (0.253275699041x speedup)
return_tuple    : 0.00528430938721 ms/call (0.338386572821x speedup)
internal_loop   : 0.00106811523438 ms/call (1.67410714286x speedup)
Testing with small N so we can compare with real recursion
true_recursion  : 0.366339683533 ms/call 
unrecursed      : 0.204155921936 ms/call (1.79441125224x speedup)
pure_python     : 3.19842815399 ms/call (0.114537412096x speedup)
partial_func    : 0.76759147644 ms/call (0.477258665288x speedup)
return_tuple    : 0.702055931091 ms/call (0.52180982641x speedup)
internal_loop   : 0.173764228821 ms/call (2.10825718284x speedup)
Testing with large N
unrecursed      : 2.07274436951 ms/call 
pure_python     : 22.873840332 ms/call 
partial_func    : 5.42766094208 ms/call 
return_tuple    : 5.28703689575 ms/call 
internal_loop   : 1.80456161499 ms/call 
```
