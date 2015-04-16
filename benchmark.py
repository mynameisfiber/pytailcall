import timeit

def benchmark(name, number=100):
    t = min(timeit.repeat(name + ".fib(500)", setup="import " + name, number=number, repeat=5))
    print "{:16s}: {} ms/call".format(name, t * 1000.0 / number)

if __name__ == "__main__":
    attempts = ("pure_python", "return_tuple", "internal_loop")
    for a in attempts:
        benchmark(a)
