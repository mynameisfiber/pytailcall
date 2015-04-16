```
$ python2.7 benchmark.py
Testing with small N so we can compare with real recursion
true_recursion  : 0.170969963074 ms/call
pure_python     : 0.910181999207 ms/call
return_tuple    : 0.193557739258 ms/call
internal_loop   : 0.0610184669495 ms/call
Testing with large N
pure_python     : 9.62756156921 ms/call
return_tuple    : 2.21788406372 ms/call
internal_loop   : 0.885553359985 ms/call
```
