reverse_string_params = (
    ("asdf",),
    ("",),
    ("qwertyuiop" * 100,),
)
def reverse_string(normal, reverse=""):
    try:
        return reverse_string(normal[:-1], reverse + normal[-1])
    except IndexError:
        return reverse

gcd_params = (
    (5,3),
    (436523451,7),
    (23305295513, 3)
)
def gcd(a, b):
    remainder = a % b
    if remainder:
        return gcd(b, remainder)
    return b

modulo_params = (
    (5, 3),
    (43652, 7),
    (2330523, 7)
)
def modulo(val, div):
    if val < div:
        return val
    return modulo(val - div, div)

string_merge_params = (
    ("qwertyuiop", "asdfghkjl"),
    ("zxcvbnm", "zxcvbnm"),
    ("acegik"*100, "bdfhjl"*100)
)
def string_merge(a, b, merge=""):
    if not a:
        return merge + b
    elif not b:
        return merge + a
    if a[0] > b[0]:
        return string_merge(a, b[1:], merge + b[0])
    else:
        return string_merge(a[1:], b, merge + a[0])

to_binary_params = (
    (5,),
    (53423451,),
    (2394871865782648123658023746415,),
)
def to_binary(n, result=""):
    if n < 2:
        return str(n) + result
    return to_binary(n/2, str(n%2) + result)

collatz_params = (
    (635,),
    (83451,),
    (9780657631,),
)
def collatz(n, i=0):
    if n == 1:
        return i
    elif n % 2 == 0 :
        return collatz(n/2, i+1)
    else:
        return collatz(n*3+1, i+1)

fib_params = (
    (5,),
    (500,),
    (5000,),
    (50000,),
)
def fib(i, current = 0, next = 1):
  if i == 0:
    return current
  else:
    return fib(i - 1, next, current + next)


examples = (
    (reverse_string, reverse_string_params),
    (gcd, gcd_params),
    (modulo, modulo_params),
    (string_merge, string_merge_params),
    (to_binary, to_binary_params),
    (collatz, collatz_params),
    (fib, fib_params),
)
