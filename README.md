```
Testing all functions work
Testing with N=5 so we can see overheads
fib             : 0.00156784057617 ms/call
fib_unrecursed  : 0.00127983093262 ms/call (1.22503725782x speedup)
partial_func    : 0.0037317276001 ms/call (0.420138001533x speedup)
return_tuple    : 0.00255966186523 ms/call (0.612518628912x speedup)
internal_loop   : 0.000455856323242 ms/call (3.43933054393x speedup)
Testing with N=750 so we can compare with real recursion
fib             : 0.273247718811 ms/call
fib_unrecursed  : 0.101056098938 ms/call (2.70392110603x speedup)
partial_func    : 0.384927749634 ms/call (0.709867550653x speedup)
return_tuple    : 0.352784156799 ms/call (0.774546457217x speedup)
internal_loop   : 0.0800123214722 ms/call (3.41507050144x speedup)
Testing with N=5000 (greater than recursion limit)
fib_unrecursed  : 0.995644569397 ms/call
partial_func    : 2.86069869995 ms/call
return_tuple    : 2.64175891876 ms/call
internal_loop   : 0.862798690796 ms/call
```

![][benchmark.png]

| example          | native           | partial_func     | return_tuple     | internal_loop    |
| ---------------- | ---------------- | ---------------- | ---------------- | ---------------- |
| reverse_string_0 |    0.01001358 ms |    0.02193451 ms |    0.01692772 ms |    0.00786781 ms |
| reverse_string_1 |    0.00500679 ms |    0.01192093 ms |    0.00691414 ms |    0.00500679 ms |
| reverse_string_2 | recursion errror |    3.18813324 ms |    2.99882889 ms |    0.92697144 ms |
| gcd_0            |    0.00190735 ms |    0.01096725 ms |    0.00691414 ms |    0.00190735 ms |
| gcd_1            |    0.00095367 ms |    0.00596046 ms |    0.00286102 ms |    0.00095367 ms |
| gcd_2            |    0.00190735 ms |    0.01096725 ms |    0.00691414 ms |    0.00095367 ms |
| modulo_0         |    0.00095367 ms |    0.00882149 ms |    0.00381470 ms |    0.00095367 ms |
| modulo_1         | recursion errror |   13.32211494 ms |   11.75117493 ms |    1.47104263 ms |
| modulo_2         | recursion errror |  675.41694641 ms |  648.26607704 ms |   85.57391167 ms |
| string_merge_0   |    0.01502037 ms |    0.03504753 ms |    0.03004074 ms |    0.01096725 ms |
| string_merge_1   |    0.01096725 ms |    0.02694130 ms |    0.02193451 ms |    0.00786781 ms |
| string_merge_2   |    1.34706497 ms |    1.98984146 ms |    2.02202797 ms |    0.77509880 ms |
| to_binary_0      |    0.00882149 ms |    0.02598763 ms |    0.02002716 ms |    0.00596046 ms |
| to_binary_1      |    0.04696846 ms |    0.08583069 ms |    0.07987022 ms |    0.03504753 ms |
| to_binary_2      |    0.28991699 ms |    0.43010712 ms |    0.42605400 ms |    0.24604797 ms |
| collatz_0        |    0.03504753 ms |    0.08010864 ms |    0.07200241 ms |    0.02002716 ms |
| collatz_1        |    0.11801720 ms |    0.26297569 ms |    0.25796890 ms |    0.07295609 ms |
| collatz_2        | recursion errror |    2.82096863 ms |    2.65693665 ms |    0.74100494 ms |
| fib_0            |    0.00381470 ms |    0.01692772 ms |    0.01287460 ms |    0.00190735 ms |
| fib_1            |    0.54287910 ms |    1.23190880 ms |    1.08289719 ms |    0.23794174 ms |
| fib_2            | recursion errror |   13.90886307 ms |   12.44997978 ms |    4.19306755 ms |
| fib_3            | recursion errror |  292.69194603 ms |  282.84502029 ms |  193.64714622 ms |

Useful references

- http://www.jonathon-vogel.com/posts/patching_function_bytecode_with_python/
- https://docs.python.org/2/library/dis.html
- http://unpyc.sourceforge.net/Opcodes.html
