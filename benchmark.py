import timeit
import sys

import true_recursion
import pure_python
import partial_func
import return_tuple
import internal_loop
import unrecursed


def benchmark(name, N, number=250, baseline=None):
    t = min(timeit.repeat(name + ".fib(%d)" % N, setup="import " + name, number=number, repeat=5))
    speedup = ""
    if baseline:
        speedup = "({}x speedup)".format(baseline / t)
    print("{:16s}: {} ms/call {}".format(name, t * 1000.0 / number, speedup))
    return t

if __name__ == "__main__":
    methods = (unrecursed, pure_python, partial_func, return_tuple, internal_loop)

    print("Testing all functions work")
    real_value = true_recursion.fib(50)
    for m in methods:
        if m.fib(50) != real_value:
            print "{} failed".format(m.__name__)
            sys.exit()

    print("Testing with very small N so we can see overheads")
    baseline = benchmark("true_recursion", 5)
    for m in methods:
        benchmark(m.__name__, 5, baseline=baseline)

    print("Testing with small N so we can compare with real recursion")
    baseline = benchmark("true_recursion", 750)
    for m in methods:
        benchmark(m.__name__, 750, baseline=baseline)

    print("Testing with large N")
    for m in methods:
        benchmark(m.__name__, 5000, number=50)
