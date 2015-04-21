from internal_loop import tail_optimize


@tail_optimize
def reverse_string(normal, reverse=""):
    try:
        return reverse_string(normal[:-1], reverse + normal[-1])
    except IndexError:
        return reverse

@tail_optimize
def gcd(a, b):
    remainder = a % b
    if remainder:
        return gcd(b, remainder)
    return b

@tail_optimize
def modulo(val, div):
    if val < div:
        return val
    return modulo(val - div, div)

@tail_optimize
def string_merge(a, b, merge=""):
    if not a:
        return merge + b
    elif not b:
        return merge + a
    if a[0] > b[0]:
        return string_merge(a, b[1:], merge + b[0])
    else:
        return string_merge(a[1:], b, merge + a[0])

@tail_optimize
def to_binary(n, result=""):
    if n < 2:
        return str(n) + result
    return to_binary(n/2, str(n%2) + result)

@tail_optimize
def collatz(n, i=0):
    if n == 1:
        return i
    elif n % 2 == 0 :
        return collatz(n/2, i+1)
    else:
        return collatz(n*3+1, i+1)


if __name__ == "__main__":
    print "reverse('qwertyuiop') = ", reverse_string('qwertyuiop')
    print "gcd(123,543) = ", gcd(123,543)
    print "modulo(15, 5) = ", modulo(15, 5)
    print "string_merge('abdeg', 'dfij') = ", string_merge('abdeg', 'dfij')
    print "to_binary(50) = ", to_binary(50)
    print "collatz(502423423) = ", collatz(502423423)
