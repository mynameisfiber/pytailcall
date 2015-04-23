import timeit
import sys
from functools import partial
from collections import OrderedDict
import numpy as np

import internal_loop
import examples
from experiments import partial_func
from experiments import return_tuple

def fib_unrecursed(i, current = 0, next = 1):
    while True:
        if i == 0:
            return current
        i, current, next = i-1, next, current+next

def native(fxn):
    return fxn

def benchmark(fxn, args, number=250, baseline=None, verbose=True, name=None):
    timer = timeit.Timer(partial(fxn, *args))
    t = min(timer.repeat(number=number, repeat=5))
    if verbose:
        speedup = ""
        if baseline:
            speedup = "({}x speedup)".format(baseline / t)
        name = name or fxn.__name__
        print("{:16s}: {} ms/call {}".format(name, t * 1000.0 / number, speedup))
    return t


if __name__ == "__main__":
    fib_methods = [
        (m.__name__.split('.')[-1], m.tail_optimize(examples.fib))
        for m in (partial_func, return_tuple, internal_loop)
    ]

    print("Testing all functions work")
    real_value = examples.fib(50)
    for _, m in fib_methods:
        if m(50) != real_value:
            print "{} failed".format(m.__name__)
            sys.exit()

    print("Testing with N=5 so we can see overheads")
    baseline = benchmark(examples.fib, (5,))
    benchmark(fib_unrecursed, (5,), baseline=baseline)
    for name, m in fib_methods:
        benchmark(m, (5,), baseline=baseline, name=name)

    print("Testing with N=750 so we can compare with real recursion")
    baseline = benchmark(examples.fib, (750,))
    benchmark(fib_unrecursed, (750,), baseline=baseline)
    for name, m in fib_methods:
        benchmark(m, (750,), baseline=baseline, name=name)

    print("Testing with N=5000 (greater than recursion limit)")
    benchmark(fib_unrecursed, (5000,))
    for name, m in fib_methods:
        benchmark(m, (5000,), number=50, name=name)

    print("Running all examples")
    methods = [("native", native)] + [
        (m.__name__.split('.')[-1], m.tail_optimize) 
        for m in (internal_loop, partial_func, return_tuple)
    ]
    header = "| {:16s} | ".format("example") + \
             " | ".join(["{:16s}".format(name) for name, _ in methods]) + \
             " |"
    print header
    print "| " + " | ".join("-"*16 for i in xrange(len(methods) + 1)) + " |"

    results = OrderedDict()
    benchmark_names = []
    for ex, ex_params in examples.examples:
        for i, params in enumerate(ex_params):
            ex_name = ex.__name__.split('.')[-1] + "_" + str(i)
            benchmark_names.append(ex_name)
            timings = ["{:16s}".format(ex_name)]
            for name, m in methods:
                fxn = m(ex)
                if name not in results:
                    results[name] = []
                try:
                    t = benchmark(fxn, params, baseline=baseline, name=name, number=5, verbose=False)
                    results[name].append(t * 1000000)
                    timings.append("{:13.4f} us".format(t * 1000000))
                except RuntimeError:
                    results[name].append(np.inf)
                    timings.append("{:>16s}".format("recursion errror"))
            print "| " + " | ".join(timings) + " |"

    import pylab as py
    index = np.arange(len(benchmark_names))
    bar_width = 0.7 / len(results)
    colors = iter("brgy")
    for i, (m, result) in enumerate(results.iteritems()):
        py.bar(
            index + bar_width * i, 
            result, 
            bar_width,
            alpha = 0.4,
            color = colors.next(),
            log = True,
            label = m,
        )

    py.xlim(xmax = index[-1] + bar_width * (i+1))
    py.xlabel('Benchmark')
    py.ylabel('Time (us)')
    py.title('Benchmark of different tailcall optimization schemes')
    py.xticks(index + bar_width, benchmark_names, rotation=70)
    py.legend(loc='upper left')

    py.tight_layout()
    py.savefig("benchmark.png")
    py.show()
    

