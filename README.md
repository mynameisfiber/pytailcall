```
$ python benchmark.py 
Testing all functions work
Testing with small N so we can compare with real recursion
true_recursion  : 0.367547988892 ms/call 
unrecursed      : 0.204323768616 ms/call (1.79885086978x speedup)
pure_python     : 3.1942358017 ms/call (0.115066016321x speedup)
partial_func    : 0.721967697144 ms/call (0.509092013875x speedup)
return_tuple    : 0.691271781921 ms/call (0.531698238672x speedup)
internal_loop   : 0.219355583191 ms/call (1.6755807331x speedup)
Testing with large N
unrecursed      : 2.03670024872 ms/call 
pure_python     : 22.5807189941 ms/call 
partial_func    : 5.42726039886 ms/call 
return_tuple    : 5.31271934509 ms/call 
internal_loop   : 2.11229801178 ms/call 
```

Notes

- internal_loop can be faster than unrecursed depending on how many fxn params
  there are
  - with #params<=3, you don't need to create a tuple to do tuple expansion
    (uses rot_two and rot_three and the stack instead)... this makes unrecursed
    for fib faster
  - with more params, both fxns need to do tuple expand but internal_loop can
    skip the while conditional evaluation and go faster!
