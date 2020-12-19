from functools import reduce
from itertools import takewhile, dropwhile, chain


"""
The prefix "l_" means the function returns a list instead of a map
The suffix "_r" means the function starts from the right of the list, e.g. reduce_r is foldr in Haskell
"""


def flatmap(f, *args) -> list:
    return reduce(lambda a, b: list(a) + list(b), map(f, *args))


def flatmap_indexed(f, *args) -> list:
    fst, *rst = [*args]
    return flatmap(lambda x, *y: f(*x, *y), enumerate(fst), *rst)


def l_map(f, *args):
    return list(map(f, *args))


def map_indexed(f, *args):
    fst, *rst = [*args]
    return map(lambda x, *y: f(*x, *y), enumerate(fst), *rst)


def l_map_indexed(f, *args):
    return list(map_indexed(f, *args))


def l_print(xs, separator=", ", brackets="[]", end="\n"):
    if len(brackets) == 2:
        r = brackets[0] + separator.join(map(lambda x: x.__str__(), xs)) + brackets[1]
        print(r, end=end)
        return r
    r = separator.join(map(lambda x: x.__str__(), xs))
    print(r, end=end)
    return r


def reduce_r(f, xs, initial=None):
    if initial is None:
        if type(xs) == list:
            return __reduce_r_list(f, xs[:-1], xs[-1])
        return __reduce_r1(f, iter(xs))
    if type(xs) == list:
        return __reduce_r_list(f, xs, initial)
    return __reduce_r(f, iter(xs), initial)


def scan(f, xs, initial=None):
    if initial is None:
        return __scan1(f, iter(xs))
    return __scan(f, xs, initial)


def l_scan(f, xs, initial=None):
    return list(scan(f, xs, initial))


def foreach(f, xs):
    for e in xs:
        f(e)


def foreach_indexed(f, xs):
    for i, e in enumerate(xs):
        f(i, e)


def apply(f, *args):
    return f(*args)


def filter_indexed(f, xs):
    return (x for i, x in enumerate(xs) if f(i, x))


def l_filter_indexed(f, xs):
    return [x for i, x in enumerate(xs) if f(i, x)]


def filter_acc(f, xs, acc=None):
    """
    :param f: A function taking an element from xs and an accumulator, returning a bool and the updated accumulator
    :param xs: The iterable to be filtered
    :param acc: The original accumulator
    :return: An iterable containing the elements x where f(x, acc)[0] == True
    There is an example about this function below in the Examples Section
    """
    cur = True, acc
    for x in xs:
        cur = f(x, cur[1])
        if cur[0]:
            yield x


def l_filter_acc(f, xs, acc=None):
    return list(filter_acc(f, xs, acc))


def l_takewhile(f, xs):
    return list(takewhile(f, xs))


def l_dropwhile(f, xs):
    return list(dropwhile(f, xs))


"""
None-handling
"""


def elvis(x, default):
    if x is None:
        return default
    return x


# Apply a function if all the arguments are not None; otherwise return the default
def safe_apply(f, *args, default=None):
    if any(True for arg in args if arg is None):
        return default
    return f(*args)


"""
Examples
"""


def prime_iter(n: int):
    return filter_acc(__is_prime_acc, range(2, n + 1))


"""
Helpers
"""


def __reduce_r_list(f, xs, initial):
    if not xs:
        return initial
    return f(xs[0], reduce_r(f, xs[1:], initial))


def __reduce_r(f, xs, initial):
    fst = next(xs, None)
    if fst is None:
        return initial
    return f(fst, reduce_r(f, xs, initial))


def __reduce_r1(f, xs):
    fst = next(xs)
    snd = next(xs, None)
    if snd is None:
        return fst
    return f(fst, __reduce_r1(f, chain([snd], xs)))


def __scan(f, xs, initial):
    for x in xs:
        yield initial
        initial = f(initial, x)
    yield initial


def __scan1(f, xs):
    fst = next(xs)
    yield fst
    for x in xs:
        fst = f(fst, x)
        yield fst


def __is_prime_acc(n: int, acc=None):
    if acc is None:
        acc = []
    if n < 2:
        return False, acc
    for p in acc:
        if p * p > n:
            return True, acc + [n]
        if n % p == 0:
            return False, acc
    return True, acc + [n]
