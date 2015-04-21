
def fib(i, current = 0, next = 1):
    while True:
        if i == 0:
            return current
        i, current, next = i-1, next, current+next


