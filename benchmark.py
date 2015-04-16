import timeit

def benchmark(name, N, number=100):
    t = min(timeit.repeat(name + ".fib(%d)" % N, setup="import " + name, number=number, repeat=5))
    print("{:16s}: {} ms/call".format(name, t * 1000.0 / number))

if __name__ == "__main__":
    print("Testing with small N so we can compare with real recursion")
    attempts = ("true_recursion", "pure_python", "return_tuple", "internal_loop")
    for a in attempts:
        benchmark(a, 500)

    print("Testing with large N")
    attempts = ("pure_python", "return_tuple", "internal_loop")
    for a in attempts:
        benchmark(a, 5000, number=25)
