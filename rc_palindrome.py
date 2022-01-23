"""
TODO (Credit):
    This algorithm is discovered by Javier Cilleruelo, Florian Luca and Lewis Baxter in 2016;
    I am merely implementing this algorithm; I play absolutely no parts in its discovery.
    Check out their full paper here: https://arxiv.org/abs/1602.06208.
"""

from enum import Enum
from rc_func import l_map, l_print, reduce_r, dropwhile, l_dropwhile, map_indexed


def is_palindrome(num, base=10):
    try:
        digits = Digits(num, base)._Digits__digits
    except TypeError:
        raise Exception("Must pass in a valid number and a valid base!")
    except ValueError:
        raise Exception("Must pass in a valid number and a valid base!")

    if digits == [*reversed(digits)]:
        return True
    return False


def sum_of_palindromes(num, base=10, show=False, check=True) -> list:
    try:
        digits = Digits(num, base)
    except TypeError:
        raise Exception("Must pass in a valid number and a valid base!")
    except ValueError:
        raise Exception("Must pass in a valid number and a valid base!")

    if is_palindrome(num, base):
        if show:
            print(num)
        return [num]

    def parser(d: Digits):
        if base == 10:
            return int(d.__str__())
        if base <= 36:
            return d.__str__()
        return l_map(lambda x: int(x.strip()), d.__str__()[1:-1].split(','))

    raw = digits._Digits__summerpark()
    result = l_map(parser, raw)
    if check and reduce_r(lambda x, y: x + y, raw) != Digits(num, base):
        raise Exception(f"{result.__str__()} is not the correct answer for {num} at base {base}! "
                        f"Please contact me at https://github.com/sorrowfulT-Rex or via e-mail: yc4120@ic.ac.uk")
    if show:
        l_print(result, brackets="", separator=" + ")
    return result


class DigitsType(Enum):
    SMALL = 0
    A1 = 1
    A2 = 2
    A3 = 3
    A4 = 4
    A5 = 5
    A6 = 6
    B1 = 11
    B2 = 12
    B3 = 13
    B4 = 14
    B5 = 15
    B6 = 16
    B7 = 17


class Digits:
    """
        :param: num can be a list of digits (in base 10, each representing one digit in the corresponding base system),
        an integer, or a string. The class will try to parse it.
        :param: base. Just base.
    """

    def __init__(self, num, base: int = 10):
        self.__base = base
        self.__digits = []
        self.__length = 0

        def invalid_msg():
            return f"{num} is not a valid base {self.__base} number!"

        if type(num) == int:
            self.__digits = l_map(lambda x: int(x), str(num))
            if self.__base < 2:
                raise Exception(f"{base} is not a correct base!")
            if any(True for d in self.__digits if d >= self.__base):
                raise Exception(invalid_msg())
            self.__length = len(str(num))
        elif type(num) == str:
            if num.startswith("0b"):
                if self.__base != 2:
                    raise Exception(f"The base of {num} should be 2 instead of {self.__base}!")
                try:
                    self.__init__(int(num[2:]), self.__base)
                except ValueError:
                    raise Exception(invalid_msg())
            elif num.startswith("0o"):
                if self.__base != 8:
                    raise Exception(f"The base of {num} should be 8 instead of {self.__base}!")
                try:
                    self.__init__(int(num[2:]), self.__base)
                except ValueError:
                    raise Exception(invalid_msg())
            elif num.startswith("0x"):
                if self.__base != 16:
                    raise Exception(f"The base of {num} should be 16 instead of {self.__base}!")
                try:
                    self.__init__(num[2:], self.__base)
                except ValueError:
                    raise Exception(invalid_msg())
            else:
                def letter_to_digits(ch: str):
                    ordinal = ord(ch)
                    if ord('0') <= ordinal <= ord("9"):
                        return int(ch)
                    return ord(ch.upper()) - ord('A') + 10

                self.__digits = l_map(letter_to_digits, num)
                if any(True for d in self.__digits if d >= self.__base):
                    raise Exception(invalid_msg())
        else:
            try:
                self.__digits = l_map(lambda x: int(x), num)
            except ValueError:
                raise Exception(invalid_msg())
            if any(True for d in self.__digits if d >= self.__base):
                raise Exception(invalid_msg())

        self.__length = len(self.__digits)

    def __str__(self):
        if self.__base <= 10:
            return "".join(map(str, self.__digits))
        if self.__base <= 36:
            def helper(d):
                if d < 10:
                    return str(d)
                return chr(d - 10 + ord('A'))

            return "".join(map(helper, self.__digits))
        return self.__digits.__str__()

    def __add__(self, other):
        if self.__base != other.__base:
            raise Exception("Cannot operate between numbers of different base!")
        if self.__length < other.__length:
            return other.__add__(self)
        raw = [0] + l_map(
            lambda x, y: x + y,
            self.__digits,
            [0 for _ in range(self.__length - other.__length)] + other.__digits
        )

        for ii in range(self.__length):
            i = self.__length - ii
            if raw[i] >= self.__base:
                raw[i] -= self.__base
                raw[i - 1] += 1

        if raw[0] == 0:
            raw = raw[1:]

        return Digits(raw, self.__base)

    def __sub__(self, other):
        if self.__base != other.__base:
            raise Exception("Cannot operate between numbers of different base!")
        if self.__length < other.__length:
            return
        raw = [0] + l_map(
            lambda x, y: x - y,
            self.__digits,
            [0 for _ in range(self.__length - other.__length)] + other.__digits
        )

        for ii in range(self.__length):
            i = self.__length - ii
            if raw[i] < 0:
                raw[i] += self.__base
                raw[i - 1] -= 1

        if raw[0] < 0:
            return
        raw = l_dropwhile(lambda x: x == 0, raw)
        if not raw:
            return Digits(0, self.__base)
        return Digits(raw, self.__base)

    def __mul__(self, other):
        if self.__base != other.__base:
            raise Exception("Cannot operate between numbers of different base!")

        def mul_one_sig_fig(zeros, one_sig):
            raw = [0] + l_map(lambda x: x * one_sig, self.__digits) + [0 for _ in range(zeros)]
            for ii in range(self.__length + zeros):
                i = self.__length - ii + zeros
                if raw[i] >= self.__base:
                    raw[i - 1] += raw[i] // self.__base
                    raw[i] %= self.__base
            raw = l_dropwhile(lambda x: x == 0, raw)
            if not raw:
                return Digits(0, self.__base)
            return Digits(raw, self.__base)

        if self.__length < other.__length:
            return other * self
        return reduce_r(
            lambda x, y: x + y,
            map_indexed(lambda i, x: mul_one_sig_fig(other.__length - i - 1, x), other.__digits)
        )

    def __eq__(self, other):
        if self.__length != other.__length:
            return False
        if self.__base != other.__base:
            return False
        return not l_dropwhile(lambda i: self.__digit_at(i) == other.__digit_at(i), range(self.__length))

    def __hash__(self):
        return sum(self.__digits)

    def __summerpark(self):
        if self.__base < 5:
            raise Exception("The algorithm is not applicable to a base less than 5!")

        typ = self.__get_type()
        if typ == DigitsType.SMALL:
            if self.__length == 1:
                return [self]
            if self.__length == 2:
                if self.__digit_at(0) <= self.__digit_at(1):
                    return [
                        Digits([self.__digit_at(0), self.__digit_at(0)], self.__base),
                        Digits([self.__digit_at(1) - self.__digit_at(0)], self.__base)
                    ]
                if self.__digit_at(0) == 1 and self.__digit_at(1) == 0:
                    return [
                        Digits([self.__base - 1], self.__base),
                        Digits([1], self.__base)
                    ]
                if self.__digit_at(0) == self.__digit_at(1) + 1:
                    return [
                        Digits([self.__digit_at(1), self.__digit_at(1)], self.__base),
                        Digits([self.__base - 1], self.__base),
                        Digits([1], self.__base)
                    ]
                return [
                    Digits([self.__digit_at(0) - 1, self.__digit_at(0) - 1], self.__base),
                    Digits([self.__base + self.__digit_at(1) - self.__digit_at(0) + 1], self.__base)
                ]
            if self.__length == 3:
                if self.__digit_at(0) <= self.__digit_at(2):
                    return [
                        Digits([self.__digit_at(0), self.__digit_at(1), self.__digit_at(0)], self.__base),
                        Digits([self.__digit_at(2) - self.__digit_at(0)], self.__base)
                    ]
                if self.__digit_at(1) != 0:
                    return [
                        Digits([self.__digit_at(0), self.__digit_at(1) - 1, self.__digit_at(0)], self.__base),
                        Digits([self.__base + self.__digit_at(2) - self.__digit_at(0)], self.__base)
                    ]
                if (self.__digit_at(0) - self.__digit_at(2) - 1) % self.__base != 0:
                    return [
                        Digits([self.__digit_at(0) - 1, self.__base - 1, self.__digit_at(0) - 1], self.__base),
                        Digits([self.__base + self.__digit_at(2) - self.__digit_at(0) + 1], self.__base)
                    ]
                if self.__digit_at(0) >= 3:
                    return [
                        Digits([self.__digit_at(0) - 2, self.__base - 1, self.__digit_at(0) - 2], self.__base),
                        Digits(111, self.__base)
                    ]
                if self.__digit_at(0) == 2:
                    return [
                        Digits(101, self.__base),
                        Digits([self.__base - 1, self.__base - 1], self.__base),
                        Digits(1, self.__base)
                    ]
                return [
                    Digits([self.__base - 1, self.__base - 1], self.__base),
                    Digits(1, self.__base)
                ]
            if self.__length == 4:
                diff = self - Digits([self.__digit_at(0), 0, 0, self.__digit_at(0)], self.__base)
                if diff is None:
                    if self.__digit_at(0) != 1:
                        if self.__digit_at(3) != self.__digit_at(0) - 1:
                            return [
                                Digits([
                                    self.__digit_at(0) - 1,
                                    self.__base - 1,
                                    self.__base - 1,
                                    self.__digit_at(0) - 1
                                ], self.__base),
                                Digits([self.__base + self.__digit_at(3) - self.__digit_at(0) + 1], self.__base)
                            ]
                        return [
                            Digits([
                                self.__digit_at(0) - 1,
                                self.__base - 1,
                                self.__base - 1,
                                self.__digit_at(0) - 1
                            ], self.__base),
                            Digits([self.__base + self.__digit_at(3) - self.__digit_at(0)], self.__base),
                            Digits(1, self.__base)
                        ]
                    return [
                        Digits([self.__base - 1, self.__base - 1, self.__base - 1], self.__base),
                        Digits(1, self.__base)
                    ]
                if diff == Digits(201, self.__base):
                    if self.__digit_at(0) == 1:
                        return [
                            Digits(1111, self.__base),
                            Digits([self.__base - 2, self.__base - 2], self.__base),
                            Digits(3, self.__base)
                        ]
                    if self.__digit_at(0) == self.__base - 1:
                        return [
                            Digits([self.__base - 1, 1, 1, self.__base - 1], self.__base),
                            Digits([self.__base - 2, self.__base - 2], self.__base),
                            Digits(3, self.__base)
                        ]
                    return [
                        Digits([
                            self.__digit_at(0) - 1,
                            self.__base - 1,
                            self.__base - 1,
                            self.__digit_at(0) - 1
                        ], self.__base),
                        Digits(212, self.__base)
                    ]
                if diff.__length == 2 and diff.__digit_at(1) == diff.__digit_at(0) - 1 != 0:
                    if diff.__digit_at(1) + self.__digit_at(0) == self.__digit_at(3) and self.__digit_at(0) == 1:
                        return [
                            Digits([self.__base - 1, self.__base - 1, self.__base - 1], self.__base),
                            Digits([diff.__digit_at(1) + 1, diff.__digit_at(1) + 1], self.__base),
                            Digits(1, self.__base)
                        ]
                    return [
                        Digits([
                            self.__digit_at(0) - 1,
                            self.__base - 2,
                            self.__base - 2,
                            self.__digit_at(0) - 1
                        ], self.__base),
                        Digits(131, self.__base),
                        Digits([diff.__digit_at(1), diff.__digit_at(1)], self.__base)
                    ]
                return [Digits([self.__digit_at(0), 0, 0, self.__digit_at(0)], self.__base)] + diff.__summerpark()
            if self.__length == 5:
                if self.__digit_at(0) == 1:
                    diff = self - Digits([1, self.__digit_at(1), 0, self.__digit_at(1), 1], self.__base)
                    if diff is None:
                        if self.__digit_at(1) == 0:
                            return [
                                Digits([
                                    self.__base - 1,
                                    self.__base - 1,
                                    self.__base - 1,
                                    self.__base - 1
                                ], self.__base),
                                Digits(1, self.__base)
                            ]
                        diff = self - Digits([
                            1,
                            self.__digit_at(1) - 1,
                            self.__base - 1,
                            self.__digit_at(1) - 1,
                            1
                        ], self.__base)
                        if diff.__length == 2 and diff.__digit_at(0) == diff.__digit_at(1) + 1:
                            if diff.__digit_at(1) == 1:
                                return [
                                    Digits([
                                        1,
                                        self.__digit_at(1) - 1,
                                        self.__base - 2,
                                        self.__digit_at(1) - 1,
                                        1
                                    ], self.__base),
                                    Digits(121, self.__base)
                                ]
                            return [
                                Digits([
                                    1,
                                    self.__digit_at(1) - 1,
                                    self.__base - 2,
                                    self.__digit_at(1) - 1,
                                    1
                                ], self.__base),
                                Digits([1, diff.__digit_at(0), 1], self.__base),
                                Digits([diff.__digit_at(1) - 1], self.__base)
                            ]
                        return [Digits([
                            1,
                            self.__digit_at(1) - 1,
                            self.__base - 1,
                            self.__digit_at(1) - 1,
                            1
                        ], self.__base)] + diff.__summerpark()
                    if diff == Digits(201, self.__base):
                        return [
                            Digits([1, self.__digit_at(1), 1, self.__digit_at(1), 1], self.__base),
                            Digits(101, self.__base)
                        ]
                    if diff.__length == 2 and 1 != diff.__digit_at(0) == diff.__digit_at(1) + 1:
                        if self.__digit_at(1) != 0:
                            return [
                                Digits([
                                    1,
                                    self.__digit_at(1) - 1,
                                    1,
                                    self.__digit_at(1) - 1,
                                    1
                                ], self.__base),
                                Digits([self.__base - 1, diff.__digit_at(0), self.__base - 1], self.__base),
                                Digits([diff.__digit_at(0)], self.__base)
                            ]
                        return [
                            Digits([
                                self.__base - 1,
                                self.__base - 1,
                                self.__base - 1,
                                self.__base - 1
                            ], self.__base),
                            Digits([diff.__digit_at(0), diff.__digit_at(0)], self.__base),
                            Digits(1, self.__base)
                        ]
                    return [Digits(
                        [1, self.__digit_at(1), 0, self.__digit_at(1), 1],
                        self.__base
                    )] + diff.__summerpark()
                return self.__algorithm_selector(
                    Digits(self.__digits + [0, self.__digit_at(-1)], self.__base).__get_type()
                )
            if self.__length == 6:
                if self.__digit_at(0) == 1:
                    def partition(s: int, can_zero: bool = True):
                        if can_zero:
                            return next(dropwhile(lambda a: a[1] >= self.__base, ((x0, s - x0) for x0 in range(s + 1))))
                        return next(dropwhile(lambda a: a[1] >= self.__base, ((x0, s - x0) for x0 in range(1, s + 1))))

                    z = (self.__digit_at(-1) - self.__digit_at(1) + 1) % self.__base
                    if z != 0 and z != self.__base - 1:
                        x1, y1 = partition(self.__base + self.__digit_at(1) - 1, False)
                        c = (x1 + y1 + z) // self.__base
                        x2, y2 = partition(self.__base + self.__digit_at(2) - 1)
                        z2 = (self.__digit_at(-2) - x2 - y2 - c) % self.__base
                        c = (x2 + y2 + z2 + c - self.__digit_at(-2)) // self.__base
                        x3, y3 = partition(self.__base + self.__digit_at(3) - c - z)
                        p1 = [x1, x2, x3, x2, x1]
                        p2 = [y1, y2, y3, y2, y1]
                        p3 = [z, z2, z]
                        return [Digits(p2, self.__base), Digits(p1, self.__base), Digits(p3, self.__base)]
                    if z == self.__base - 1:
                        if self.__digit_at(3) != 0:
                            z = self.__base - 1
                            x1, y1 = partition(self.__base + self.__digit_at(1) - 1, False)
                            c = (x1 + y1 + z - self.__digit_at(-1)) // self.__base
                            x2, y2 = partition(self.__base + self.__digit_at(2) - 1)
                            z2 = (self.__digit_at(-2) - x2 - y2 - c) % self.__base
                            c = (x2 + y2 + z2 + c - self.__digit_at(-2)) // self.__base
                            x3, y3 = partition(1 + self.__digit_at(3) - c)
                            p1 = [x1, x2, x3, x2, x1]
                            p2 = [y1, y2, y3, y2, y1]
                            p3 = [z, z2, z]
                            return [Digits(p2, self.__base), Digits(p1, self.__base), Digits(p3, self.__base)]
                        if self.__digit_at(1) == 0 or self.__digit_at(1) == 1:
                            x2, y2 = partition(self.__digit_at(2))
                            z2 = (self.__digit_at(-2) - self.__digit_at(2) - 1) % self.__base
                            c = (self.__digit_at(2) + z2 + 1 - self.__digit_at(-2)) // self.__base
                            x3, y3 = partition(self.__base - c - z2)
                            p1 = [
                                self.__base - 2 + self.__digit_at(1),
                                x2,
                                x3,
                                x2,
                                self.__base - 2 + self.__digit_at(1)
                            ]
                            p2 = [1, y2, y3, y2, 1]
                            p3 = [self.__base - 1, z2, z2, self.__base - 1]
                            return [Digits(p2, self.__base), Digits(p1, self.__base), Digits(p3, self.__base)]
                        if self.__digit_at(1) == 2:
                            x2, y2 = partition(self.__digit_at(2))
                            z2 = (self.__digit_at(-2) - self.__digit_at(2) - 2) % self.__base
                            c = (self.__digit_at(2) + z2 + 2 - self.__digit_at(-2)) // self.__base
                            if c == 2:
                                return [
                                    Digits([1, 2, self.__base - 2, self.__base - 2, 2, 1], self.__base),
                                    Digits([1, self.__base - 3, 1], self.__base),
                                    Digits([self.__base - 2], self.__base)
                                ]
                            x3, y3 = partition(self.__base - c - z2)
                            p1 = [
                                self.__base - 1,
                                x2,
                                x3,
                                x2,
                                self.__base - 1
                            ]
                            p2 = [2, y2, y3, y2, 2]
                            p3 = [self.__base - 1, z2, z2, self.__base - 1]
                            return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]
                        d = (self.__digit_at(2) - 1) % self.__base
                        c4 = (d + 1 - self.__digit_at(2)) // self.__base
                        z = (self.__digit_at(-2) - self.__digit_at(2) - 1 + c4) % self.__base
                        c2 = (2 - c4 + d + z - self.__digit_at(-2)) // self.__base
                        p1 = [1, 1 - c4, 0, 0, 1 - c4, 1]
                        p2 = [self.__digit_at(-1) + 1, d, 2 - c2, d, self.__digit_at(-1) + 1]
                        p3 = [self.__base - 2, z, self.__base - 2]
                        return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]
                    if self.__digit_at(2) != 0:
                        if self.__digit_at(1) + 1 != self.__base:
                            x1, y1 = partition(self.__base + self.__digit_at(1), False)
                            c = (x1 + y1 + self.__base - 1) // self.__base
                            x2, y2 = partition(self.__digit_at(2) - 1)
                            z2 = (self.__digit_at(-2) - x2 - y2 - c) % self.__base
                            c = (x2 + y2 + z2 + c - self.__digit_at(-2)) // self.__base
                            x3, y3 = partition(1 + self.__digit_at(3) - c)
                            p1 = [x1, x2, x3, x2, x1]
                            p2 = [y1, y2, y3, y2, y1]
                            p3 = [self.__base - 1, z2, self.__base - 1]
                            return [Digits(p2, self.__base), Digits(p1, self.__base), Digits(p3, self.__base)]
                        y = 3
                        for i in [1, 2]:
                            d = (self.__digit_at(-2) - 3 - i) % self.__base
                            if d < self.__base - 2:
                                y = i
                                break
                        d = (self.__digit_at(-2) - 3 - y) % self.__base
                        x = (self.__digit_at(2) - y) % self.__base
                        c1 = (3 + y + d - self.__digit_at(-2)) // self.__base
                        c2 = (x + (self.__digit_at(3) - x - c1 - 1) % self.__base
                              + c1 + 1 - self.__digit_at(3)) // self.__base
                        u = 0
                        if c2 > 1:
                            u = 1
                            c2 = 1
                        c3 = (x + y - self.__digit_at(2)) // self.__base
                        p1 = [1, 3 - c3, x - u, x - u, 3 - c3, 1]
                        p2 = [
                            self.__base - 4,
                            y - c2 + u,
                            (self.__digit_at(3) - x - c1 - 1 + u) % self.__base,
                            y - c2 + u,
                            self.__base - 4
                        ]
                        p3 = [1, d + c2 + c3 - u, 1]
                        return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]
                    if self.__digit_at(1) == 0:
                        diff = self - Digits(100001, self.__base)
                        if self.__digit_at(3) != 0:
                            return [Digits(100001, self.__base)] + diff.__summerpark()
                        if self.__digit_at(-2) == 0:
                            return [Digits(100001, self.__base), Digits([self.__base - 2], self.__base)]
                        if self.__digit_at(-2) == self.__base - 1:
                            return [
                                Digits([self.__base - 1, 0, 1, 0, self.__base - 1], self.__base),
                                Digits(
                                    [self.__base - 1, self.__base - 2, self.__base - 2, self.__base - 1],
                                    self.__base
                                ),
                                Digits(101, self.__base)
                            ]
                        return [Digits(100001, self.__base)] + diff.__summerpark()
                    if self.__digit_at(1) == 1:
                        diff = self - Digits(110011, self.__base)
                        if self.__digit_at(3) == 1:
                            if self.__digit_at(-2) == 0:
                                return [
                                    Digits([1, 0, self.__base - 1, self.__base - 1, 0, 1], self.__base),
                                    Digits([1, self.__base - 1, 1], self.__base),
                                    Digits([self.__base - 2], self.__base)
                                ]
                            if self.__digit_at(-2) == 1:
                                return [
                                    Digits(110011, self.__base),
                                    Digits([self.__base - 1, self.__base - 1], self.__base)
                                ]
                            return [Digits(110011, self.__base)] + diff.__summerpark()
                        if self.__digit_at(3) == 0:
                            if self.__digit_at(-2) == 1:
                                return [
                                    Digits(100001, self.__base),
                                    Digits(10001, self.__base),
                                    Digits([self.__base - 2], self.__base)
                                ]
                            if self.__digit_at(-2) == 0:
                                return [
                                    Digits(100001, self.__base),
                                    Digits([
                                        self.__base - 1,
                                        self.__base - 1,
                                        self.__base - 1,
                                        self.__base - 1
                                    ], self.__base)
                                ]
                            if self.__digit_at(-2) == 2:
                                return [
                                    Digits(110011, self.__base),
                                    Digits([self.__base - self.__digit_at(-2) + 1], self.__base)
                                ]
                            return [
                                Digits(110011, self.__base),
                                Digits([self.__digit_at(-2) - 2, self.__digit_at(-2) - 2], self.__base),
                                Digits([self.__base - self.__digit_at(-2) + 1], self.__base)
                            ]
                        return [Digits(110011, self.__base)] + diff.__summerpark()
                    if self.__digit_at(1) == 2:
                        diff = self - Digits(120021, self.__base)
                        if self.__digit_at(3) >= 2:
                            return [Digits(120021, self.__base)] + diff.__summerpark()
                        if self.__digit_at(3) == 0:
                            if self.__digit_at(-2) == 0:
                                return [
                                    Digits([1, 1, self.__base - 1, self.__base - 1, 1, 1], self.__base),
                                    Digits([self.__base - 2, self.__base - 2], self.__base),
                                    Digits(2, self.__base)
                                ]
                            if self.__digit_at(-2) == 1:
                                return [
                                    Digits(100001, self.__base),
                                    Digits(20002, self.__base),
                                    Digits([self.__base - 2], self.__base)
                                ]
                            if self.__digit_at(-2) == 3:
                                return [
                                    Digits(120021, self.__base),
                                    Digits([self.__base - 1], self.__base),
                                    Digits(1, self.__base)
                                ]
                            return [
                                Digits(120021, self.__base),
                                Digits([self.__digit_at(-2) - 3, self.__digit_at(-2) - 3], self.__base),
                                Digits([self.__base - self.__digit_at(-2) + 3], self.__base)
                            ]
                        if self.__digit_at(-2) == 0:
                            return [
                                Digits([1, 1, self.__base - 1, self.__base - 1, 1, 1], self.__base),
                                Digits([1, self.__base - 2, 1], self.__base),
                                Digits([self.__base - 1], self.__base)
                            ]
                        if self.__digit_at(-2) == 1:
                            return [
                                Digits([1, 1, self.__base - 1, self.__base - 1, 1, 1], self.__base),
                                Digits([1, self.__base - 1, 1], self.__base),
                                Digits([self.__base - 1], self.__base)
                            ]
                        return [Digits(120021, self.__base)] + diff.__summerpark()
                    if self.__digit_at(1) == 3:
                        y = 3
                        for i in [1, 2]:
                            d = (self.__digit_at(-2) - 1 - i) % self.__base
                            if d != 0 and d != self.__base - 1:
                                y = i
                                break
                        d = (self.__digit_at(-2) - 1 - y) % self.__base
                        c1 = (2 + y + d - self.__digit_at(-2)) // self.__base
                        c2 = (2 * self.__base - y - 2 + (self.__digit_at(3) + y + 2) % self.__base
                              - self.__digit_at(3)) // self.__base
                        p1 = [1, 0, self.__base - y - 1 - c1, self.__base - y - 1 - c1, 0, 1]
                        p2 = [2, y - c2 + 1 + c1, (self.__digit_at(3) + y + 2) % self.__base, y - c2 + 1 + c1, 2]
                        p3 = [self.__base - 1, d + c2 - c1 - 1, self.__base - 1]
                        return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]
                    y = 3
                    for i in [1, 2]:
                        d = (self.__digit_at(-2) - 1 - i) % self.__base
                        if d != 0 and d != self.__base - 1:
                            y = i
                            break
                    d = (self.__digit_at(-2) - 1 - y) % self.__base
                    c1 = (1 + y + d - self.__digit_at(-2)) // self.__base
                    c2 = (self.__base - y + 1 + (self.__digit_at(3) + y - 1) % self.__base
                          - self.__digit_at(3)) // self.__base
                    p1 = [1, 2, self.__base - y - c1, self.__base - y - c1, 2, 1]
                    p2 = [
                        self.__digit_at(1) - 3,
                        y - c2 + c1,
                        (self.__digit_at(3) + y - 1) % self.__base,
                        y - c2 + c1,
                        self.__digit_at(1) - 3
                    ]
                    p3 = [1, (self.__digit_at(-2) - 2 - y) % self.__base + c2 - c1, 1]
                    return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]
                return self.__algorithm_selector(
                    Digits(self.__digits + [self.__digit_at(-1)], self.__base).__get_type(),
                    True
                )
        return self.__algorithm_selector(typ)

    def __get_type(self) -> DigitsType:
        if self.__length < 7:
            return DigitsType.SMALL
        z1 = (self.__digit_at(-1) - self.__digit_at(0) - self.__digit_at(1) + 1) % self.__base
        z2 = (self.__digit_at(-1) - self.__digit_at(0) + 2) % self.__base
        z3 = (self.__digit_at(-1) - self.__digit_at(2)) % self.__base
        if self.__digit_at(1) > 2:
            if z1 != 0:
                return DigitsType.A1
            return DigitsType.A2
        if self.__digit_at(0) != 1:
            if z2 != 0:
                return DigitsType.A3
            return DigitsType.A4
        if self.__digit_at(1) == 0 and self.__digit_at(2) <= 3 and z3 != 0:
            return DigitsType.A5
        if self.__digit_at(1) == 0 and self.__digit_at(2) <= 2 and z3 == 0:
            return DigitsType.A6
        if self.__digit_at(2) >= 4 and z3 != 0:
            return DigitsType.B1
        if self.__digit_at(2) >= 3 and z3 == 0:
            return DigitsType.B2
        if self.__digit_at(-1) == 0:
            if self.__digit_at(2) <= 1:
                return DigitsType.B3
            return DigitsType.B4
        if self.__digit_at(2) <= 2:
            return DigitsType.B5
        if self.__digit_at(-1) != 3:
            return DigitsType.B6
        return DigitsType.B7

    def __digit_at(self, index: int) -> int:
        return self.__digits[index]

    def __is_special(self) -> bool:
        if self.__get_type() == DigitsType.A5 or self.__get_type() == DigitsType.A6:
            if self.__length % 2 == 1 and \
                    self.__digit_at(self.__length // 2) * self.__digit_at(self.__length // 2 + 1) == 0:
                return True
            return False
        if self.__length % 2 == 0 and \
                self.__digit_at(self.__length // 2) * self.__digit_at(self.__length // 2 - 1) == 0:
            return True
        return False

    def __get_config(self, typ):
        if typ == DigitsType.A1:
            z = (self.__digit_at(-1) - self.__digit_at(0) - self.__digit_at(1) + 1) % self.__base
            return [
                [self.__digit_at(0)] + [0 for _ in range(self.__length - 2)] + [self.__digit_at(0)],
                [self.__digit_at(1) - 1] + [0 for _ in range(self.__length - 3)] + [self.__digit_at(1) - 1],
                [z] + [0 for _ in range(self.__length - 4)] + [z]
            ]
        if typ == DigitsType.A2:
            return [
                [self.__digit_at(0)] + [0 for _ in range(self.__length - 2)] + [self.__digit_at(0)],
                [self.__digit_at(1) - 2] + [0 for _ in range(self.__length - 3)] + [self.__digit_at(1) - 2],
                [1] + [0 for _ in range(self.__length - 4)] + [1]
            ]
        if typ == DigitsType.A3:
            z = (self.__digit_at(-1) - self.__digit_at(0) + 2) % self.__base
            return [
                [self.__digit_at(0) - 1] + [0 for _ in range(self.__length - 2)] + [self.__digit_at(0) - 1],
                [self.__base - 1] + [0 for _ in range(self.__length - 3)] + [self.__base - 1],
                [z] + [0 for _ in range(self.__length - 4)] + [z]
            ]
        if typ == DigitsType.A4:
            return [
                [self.__digit_at(0) - 1] + [0 for _ in range(self.__length - 2)] + [self.__digit_at(0) - 1],
                [self.__base - 2] + [0 for _ in range(self.__length - 3)] + [self.__base - 2],
                [1] + [0 for _ in range(self.__length - 4)] + [1]
            ]
        z = (self.__digit_at(-1) - self.__digit_at(2)) % self.__base
        if typ == DigitsType.A5:
            return [
                [self.__base - 1] + [0 for _ in range(self.__length - 3)] + [self.__base - 1],
                [self.__digit_at(2) + 1] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(2) + 1],
                [z] + [0 for _ in range(self.__length - 5)] + [z]
            ]
        if typ == DigitsType.A6:
            return [
                [self.__base - 1] + [0 for _ in range(self.__length - 3)] + [self.__base - 1],
                [self.__digit_at(2) + 2] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(2) + 2],
                [self.__base - 1] + [0 for _ in range(self.__length - 5)] + [self.__base - 1]
            ]
        if typ == DigitsType.B1:
            return [
                [1, self.__digit_at(1)] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(1), 1],
                [self.__digit_at(2) - 1] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(2) - 1],
                [z] + [0 for _ in range(self.__length - 5)] + [z]
            ]
        if typ == DigitsType.B2:
            return [
                [1, self.__digit_at(1)] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(1), 1],
                [self.__digit_at(2) - 2] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(2) - 2],
                [1] + [0 for _ in range(self.__length - 5)] + [1]
            ]
        if typ == DigitsType.B3:
            return [
                [1, self.__digit_at(1) - 1] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(1) - 1, 1],
                [self.__base - 2] + [0 for _ in range(self.__length - 4)] + [self.__base - 2],
                [1] + [0 for _ in range(self.__length - 5)] + [1]
            ]
        if typ == DigitsType.B4:
            return [
                [1, self.__digit_at(1)] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(1), 1],
                [1] + [0 for _ in range(self.__length - 4)] + [1],
                [self.__base - 2] + [0 for _ in range(self.__length - 5)] + [self.__base - 2]
            ]
        if typ == DigitsType.B5:
            return [
                [1, self.__digit_at(1) - 1] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(1) - 1, 1],
                [self.__base - 1] + [0 for _ in range(self.__length - 4)] + [self.__base - 1],
                [self.__digit_at(-1)] + [0 for _ in range(self.__length - 5)] + [self.__digit_at(-1)]
            ]
        if typ == DigitsType.B6:
            z = (self.__digit_at(-1) - 3) % self.__base
            return [
                [1, self.__digit_at(1)] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(1), 1],
                [2] + [0 for _ in range(self.__length - 4)] + [2],
                [z] + [0 for _ in range(self.__length - 5)] + [z]
            ]
        return [
            [1, self.__digit_at(1)] + [0 for _ in range(self.__length - 4)] + [self.__digit_at(1), 1],
            [1] + [0 for _ in range(self.__length - 4)] + [1],
            [1] + [0 for _ in range(self.__length - 5)] + [1]
        ]

    def __algorithm_selector(self, typ, must_normal=False):
        config = self.__get_config(typ)
        val = typ.value
        if self.__is_special() and not must_normal:
            return self.__algorithm5()
        if val < 10:
            if (self.__length % 2 == 0) == (val == 5 or val == 6):
                return self.__algorithm1(config)
            return self.__algorithm2(config)
        if self.__length % 2 == 1:
            return self.__algorithm3(config)
        return self.__algorithm4(config)

    def __algorithm1(self, configs: list):
        # print(self.__get_type())
        m = (self.__length - 1) // 2
        p1 = configs[0]
        p2 = configs[1]
        p3 = configs[2]
        x = p1[0]
        y = p2[0]
        z = p3[0]
        c = (x + y + z) // self.__base

        if z < self.__digit_at(1 - 2 * m):
            x = (self.__digit_at(-2 * m) - y) % self.__base
        else:
            x = (self.__digit_at(-2 * m) - y - 1) % self.__base
        y = (self.__digit_at(1 - 2 * m) - z - 1) % self.__base
        z = (self.__digit_at(-2) - x - y - c) % self.__base
        c = (x + y + z + c - self.__digit_at(-2)) // self.__base
        p1[1] = p1[-2] = x
        p2[1] = p2[-2] = y
        p3[1] = p3[-2] = z

        for i in range(2, m):
            if z < self.__digit_at(i - 2 * m):
                x = 1
            else:
                x = 0
            y = (self.__digit_at(i - 2 * m) - z - 1) % self.__base
            z = (self.__digit_at(-i - 1) - x - y - c) % self.__base
            c = (x + y + z + c - self.__digit_at(-i - 1)) // self.__base
            p1[i] = p1[-i - 1] = x
            p2[i] = p2[-i - 1] = y
            p3[i] = p3[-i - 1] = z

        if c == 0:
            p1[m] = 1
        elif c == 1:
            p1[m] = 0
        else:
            p1[m] = self.__base - z
            p2[m - 1] -= self.__base - z
            p2[m] -= self.__base - z
            p3[m - 1] = 0

        return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]

    def __algorithm2(self, configs: list):
        m = self.__length // 2
        p1 = configs[0]
        p2 = configs[1]
        p3 = configs[2]
        x = p1[0]
        y = p2[0]
        z = p3[0]
        c = (x + y + z) // self.__base

        if z < self.__digit_at(2 - 2 * m):
            x = (self.__digit_at(1 - 2 * m) - y) % self.__base
        else:
            x = (self.__digit_at(1 - 2 * m) - y - 1) % self.__base
        y = (self.__digit_at(2 - 2 * m) - z - 1) % self.__base
        z = (self.__digit_at(-2) - x - y - c) % self.__base
        c = (x + y + z + c - self.__digit_at(-2)) // self.__base
        p1[1] = p1[-2] = x
        p2[1] = p2[-2] = y
        p3[1] = p3[-2] = z

        for i in range(2, m - 1):
            if z < self.__digit_at(i + 1 - 2 * m):
                x = 1
            else:
                x = 0
            y = (self.__digit_at(i + 1 - 2 * m) - z - 1) % self.__base
            z = (self.__digit_at(-i - 1) - x - y - c) % self.__base
            c = (x + y + z + c - self.__digit_at(-i - 1)) // self.__base
            p1[i] = p1[-i - 1] = x
            p2[i] = p2[-i - 1] = y
            p3[i] = p3[-i - 1] = z
        p1[m - 1] = 0
        p2[m - 1] = (self.__digit_at(-m) - z - c) % self.__base
        c = (p1[m - 1] + p2[m - 1] + z + c - self.__digit_at(-m)) // self.__base
        if c == 0:
            if p2[m - 1] != 0:
                p1[m - 1] = 1
                p1[m] = 1
                p2[m - 1] -= 1
            elif y != 0:
                p1[m - 1] = 1
                p1[m] = 1
                p2[m - 2] = y - 1
                p2[m - 1] = self.__base - 2
                p2[m] = y - 1
                p3[m - 2] = z + 1
                p3[m - 1] = z + 1
            elif z == 0:
                if self.__length == 6:
                    if x != 0:
                        p1[1] -= 1
                        p1[2] = p1[3] = self.__base - 1
                        p1[4] -= 1
                        p2[1] = p2[2] = p2[3] = 1
                    elif p1[0] == 1:
                        p1[0] = p1[5] = 2
                        p2 = [1, 1]
                        p3 = [self.__base - 4]
                    elif p2[0] != self.__base - 1:
                        p1[0] -= 1
                        p1[1] = p1[4] = self.__base - 1
                        p1[5] -= 1
                        p2[0] += 1
                        p2[4] += 1
                        p2[2] = self.__base - 2
                        p3[1] = p3[2] = 1
                    elif p1[0] != self.__base - 1:
                        p1[0] += 1
                        p1[5] += 1
                        p2 = [1, 1]
                        p3 = [self.__base - 4]
                    else:
                        print("7?!")
                else:
                    p1[m - 2] = x - 1
                    p1[m - 1] = 1
                    p1[m] = 1
                    p1[m + 1] = x - 1
                    p2[m - 2] = self.__base - 1
                    p2[m - 1] = self.__base - 4
                    p2[m] = self.__base - 1
                    p3[m - 2] = p3[m - 1] = 2
            else:
                p2[m - 2] = p2[m - 1] = p2[m] = 1
                p3[m - 2] = p3[m - 1] = z - 1
        elif c == 2:
            p1[m - 1] = p1[m] = 1
            p2[m - 2] = p2[m] = y - 1
            p2[m - 1] = self.__base - 2
            p3[m - 2] = p3[m - 1] = 0

        return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]

    def __algorithm3(self, configs: list):
        m = self.__length // 2
        p1 = configs[0]
        p2 = configs[1]
        p3 = configs[2]
        x = p1[1]
        y = p2[0]
        z = p3[0]
        c = (1 + y + z) // self.__base

        if z < self.__digit_at(2 - 2 * m):
            x_ = (self.__digit_at(1 - 2 * m) - y) % self.__base
        else:
            x_ = (self.__digit_at(1 - 2 * m) - y - 1) % self.__base
        y = (self.__digit_at(2 - 2 * m) - z - 1) % self.__base
        z = (self.__digit_at(-2) - x - y - c) % self.__base
        c = (x + y + z + c - self.__digit_at(-2)) // self.__base
        x = x_
        p1[2] = p1[-3] = x
        p2[1] = p2[-2] = y
        p3[1] = p3[-2] = z

        for i in range(2, m - 1):
            if z < self.__digit_at(i + 1 - 2 * m):
                x_ = 1
            else:
                x_ = 0
            y = (self.__digit_at(i + 1 - 2 * m) - z - 1) % self.__base
            z = (self.__digit_at(-i - 1) - x - y - c) % self.__base
            c = (x + y + z + c - self.__digit_at(-i - 1)) // self.__base
            x = x_
            p1[i + 1] = p1[-i - 2] = x
            p2[i] = p2[-i - 1] = y
            p3[i] = p3[-i - 1] = z
        p1[m] = 0
        p2[m - 1] = (self.__digit_at(-m) - z - x - c) % self.__base
        c = (x + p2[m - 1] + z + c - self.__digit_at(-m)) // self.__base

        if c == 0:
            p1[m] = 1
        elif c == 2:
            if y != 0:
                if z != self.__base - 1:
                    p2[m - 2] -= 1
                    p2[m - 1] -= 1
                    p2[m] -= 1
                    p3[m - 2] += 1
                    p3[m - 1] += 1
                else:
                    p1[m] = 1
                    p2[m - 2] -= 1
                    p2[m] -= 1
                    p3[m - 2] = p3[m - 1] = 0
            elif z != self.__base - 1:
                p1[m - 1] -= 1
                p1[m + 1] -= 1
                p2[m - 2] = p2[m] = self.__base - 1
                p2[m - 1] -= 1
                p3[m - 2] += 1
                p3[m - 1] += 1
            else:
                p1[m - 1] -= 1
                p1[m] = 1
                p1[m + 1] -= 1
                p2[m - 2] = p2[m] = self.__base - 1
                p3[m - 2] = p3[m - 1] = 0

        return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]

    def __algorithm4(self, configs: list):
        m = self.__length // 2
        p1 = configs[0]
        p2 = configs[1]
        p3 = configs[2]
        x = p1[1]
        y = p2[0]
        z = p3[0]
        c = (1 + y + z) // self.__base
        if z < self.__digit_at(3 - 2 * m):
            x_ = (self.__digit_at(2 - 2 * m) - y) % self.__base
        else:
            x_ = (self.__digit_at(2 - 2 * m) - y - 1) % self.__base
        y = (self.__digit_at(3 - 2 * m) - z - 1) % self.__base
        z = (self.__digit_at(-2) - x - y - c) % self.__base
        c = (x + y + z + c - self.__digit_at(-2)) // self.__base
        x = x_
        p1[2] = p1[-3] = x
        p2[1] = p2[-2] = y
        p3[1] = p3[-2] = z
        for i in range(2, m - 2):
            if z < self.__digit_at(i + 2 - 2 * m):
                x_ = 1
            else:
                x_ = 0
            y = (self.__digit_at(i + 2 - 2 * m) - z - 1) % self.__base
            z = (self.__digit_at(-i - 1) - x - y - c) % self.__base
            c = (x + y + z + c - self.__digit_at(-i - 1)) // self.__base
            x = x_
            p1[i + 1] = p1[-i - 2] = x
            p2[i] = p2[-i - 1] = y
            p3[i] = p3[-i - 1] = z
        if z < self.__digit_at(-m):
            p1[m - 1] = p1[m] = 1
        else:
            p1[m - 1] = p1[m] = 0
        p2[m - 2] = p2[m - 1] = (self.__digit_at(-m) - z - 1) % self.__base
        p3[m - 2] = (self.__digit_at(1 - m) - x - p2[m - 2] - c) % self.__base
        c = (x + p2[m - 2] + p3[m - 2] + c - self.__digit_at(1 - m)) // self.__base

        if p1[m - 1] + c == 1:
            pass
        elif p1[m - 1] + c == 0:
            if p2[m - 2] < self.__base - 1:
                if p3[m - 2] > 0:
                    p2[m - 2] += 1
                    p2[m - 1] += 1
                    p3[m - 2] -= 1
                elif y > 0:
                    if p2[m - 1] == 1:
                        p1[m - 1] = p1[m] = 1
                        p2[m - 3] -= 1
                        p2[m - 2] = p2[m - 1] = self.__base - 1
                        p2[m] -= 1
                        p3[m - 3] = p3[m - 1] = 0
                        p3[m - 2] = 3
                    elif p3[m - 3] == self.__base - 1:
                        p1[m - 1] = p1[m] = 2
                        p2[m - 3] -= 1
                        p2[m - 2] -= 2
                        p2[m - 1] -= 2
                        p2[m] -= 1
                        p3[m - 3] = p3[m - 1] = 0
                        p3[m - 2] = 3
                    else:
                        p1[m - 1] = p1[m] = 1
                        p2[m - 3] -= 1
                        p2[m - 2] -= 1
                        p2[m - 1] -= 1
                        p2[m] -= 1
                        p3[m - 3] += 1
                        p3[m - 1] += 1
                        p3[m - 2] = 1
                elif z < self.__base - 1:
                    p1[m - 2] -= 1
                    p1[m - 1] = p1[m] = 1
                    p1[m + 1] -= 1
                    p2[m - 3] = p2[m] = self.__base - 1
                    p2[m - 2] -= 1
                    p2[m - 1] -= 1
                    p3[m - 3] += 1
                    p3[m - 2] = 1
                    p3[m - 1] += 1
                elif p2[m - 2] != 1:
                    p1[m - 2] -= 1
                    p1[m - 1] = p1[m] = 2
                    p1[m + 1] -= 1
                    p2[m - 3] = p2[m] = self.__base - 1
                    p2[m - 2] -= 2
                    p2[m - 1] -= 2
                    p3[m - 3] = p3[m - 1] = 0
                    p3[m - 2] = 3
                else:
                    p1[m - 2] -= 1
                    p1[m - 1] = p1[m] = 1
                    p1[m + 1] -= 1
                    p2[m - 3] = p2[m - 2] = p2[m - 1] = p2[m] = self.__base - 1
                    p3[m - 3] = p3[m - 1] = 0
                    p3[m - 2] = 3
            else:
                p1[m - 1] = p1[m] = 1
                p2[m - 3] -= 1
                p2[m - 2] = p2[m - 1] = self.__base - 2
                p2[m] -= 1
                p3[m - 3] += 1
                p3[m - 1] += 1
                p3[m - 2] = 1
        elif p1[m - 1] == 0 and c == 2:
            if p3[m - 2] < self.__base - 1:
                p2[m - 2] -= 1
                p2[m - 1] -= 1
                p3[m - 2] += 1
            elif z < self.__base - 1:
                if y > 0:
                    p1[m - 1] = p1[m] = 1
                    p2[m - 3] -= 1
                    p2[m - 2] -= 2
                    p2[m - 1] -= 2
                    p2[m] -= 1
                    p3[m - 3] += 1
                    p3[m - 2] = 1
                    p3[m - 1] += 1
                else:
                    p1[m - 2] -= 1
                    p1[m - 1] = p1[m] = 1
                    p1[m + 1] -= 1
                    p2[m - 3] = p2[m] = self.__base - 1
                    p2[m - 2] -= 2
                    p2[m - 1] -= 2
                    p3[m - 3] += 1
                    p3[m - 1] += 1
                    p3[m - 2] = 1
            elif p2[m - 2] < self.__base - 2:
                if y < self.__base - 1:
                    p1[m - 2] -= 1
                    p1[m - 1] = p1[m] = self.__base - 2
                    p1[m + 1] -= 1
                    p2[m - 3] += 1
                    p2[m - 2] += 2
                    p2[m - 1] += 2
                    p2[m] += 1
                    p3[m - 3] = p3[m - 2] = p3[m - 1] = self.__base - 2
                else:
                    p1[m - 1] = p1[m] = self.__base - 2
                    p2[m - 3] = p2[m] = 0
                    p2[m - 2] += 2
                    p2[m - 1] += 2
                    p3[m - 3] = p3[m - 2] = p3[m - 1] = self.__base - 2
            elif y >= 1:
                p1[m - 1] = p1[m] = 2
                p2[m - 3] -= 1
                p2[m - 2] -= 3
                p2[m - 1] -= 3
                p2[m] -= 1
                p3[m - 3] = p3[m - 1] = 0
                p3[m - 2] = 3
            else:
                p1[m - 2] -= 1
                p1[m - 1] = p1[m] = 2
                p1[m + 1] -= 1
                p2[m - 3] = p2[m] = self.__base - 1
                p2[m - 2] -= 3
                p2[m - 1] -= 3
                p3[m - 3] = p3[m - 1] = 0
                p3[m - 2] = 3
        elif p1[m - 1] == c == 1:
            if p3[m - 2] < self.__base - 1:
                if p2[m - 2] > 0:
                    p2[m - 2] -= 1
                    p2[m - 1] -= 1
                    p3[m - 2] += 1
                else:
                    p1[m - 1] = p1[m] = 0
                    p2[m - 2] = p2[m - 1] = self.__base - 1
                    p3[m - 2] += 1
            elif z > 0:
                if y < self.__base - 1:
                    p1[m - 1] = p1[m] = 0
                    p2[m - 3] += 1
                    p2[m - 2] += 1
                    p2[m - 1] += 1
                    p2[m] += 1
                    p3[m - 3] -= 1
                    p3[m - 2] = self.__base - 2
                    p3[m - 1] -= 1
                elif p2[m - 2] == 0:
                    p2[m - 3] = p2[m - 2] = p2[m - 1] = p2[m] = self.__base - 2
                    p3[m - 3] += 1
                    p3[m - 2] = 1
                    p3[m - 1] += 1
                elif p2[m - 2] == 1:
                    p2[m - 3] = p2[m] = self.__base - 2
                    p2[m - 2] = p2[m - 1] = self.__base - 1
                    p3[m - 3] += 1
                    p3[m - 2] = 1
                    p3[m - 1] += 1
                else:
                    p1[m - 1] = p1[m] = 2
                    p2[m - 3] = p2[m] = self.__base - 2
                    p2[m - 2] -= 2
                    p2[m - 1] -= 2
                    p3[m - 3] += 1
                    p3[m - 2] = 1
                    p3[m - 1] += 1
            elif y > 0:
                if p2[m - 2] == 0:
                    p2[m - 3] -= 1
                    p2[m - 2] = p2[m - 1] = self.__base - 2
                    p2[m] -= 1
                    p3[m - 3] = p3[m - 2] = p3[m - 1] = 1
                elif p2[m - 2] == 1:
                    p2[m - 3] -= 1
                    p2[m - 2] = p2[m - 1] = self.__base - 1
                    p2[m] -= 1
                    p3[m - 3] = p3[m - 2] = p3[m - 1] = 1
                else:
                    p1[m - 1] = p1[m] = 2
                    p2[m - 3] -= 1
                    p2[m - 2] -= 2
                    p2[m - 1] -= 2
                    p2[m] -= 1
                    p3[m - 3] = p3[m - 2] = p3[m - 1] = 1
            elif p2[m - 2] == 0:
                p1[m - 2] -= 1
                p1[m + 1] -= 1
                p2[m - 3] = p2[m] = self.__base - 1
                p2[m - 2] = p2[m - 1] = self.__base - 2
                p3[m - 3] = p3[m - 2] = p3[m - 1] = 1
            elif p2[m - 2] == 1:
                p1[m - 2] -= 1
                p1[m + 1] -= 1
                p2[m - 3] = p2[m] = self.__base - 1
                p2[m - 2] = p2[m - 1] = self.__base - 1
                p3[m - 3] = p3[m - 2] = p3[m - 1] = 1
            else:
                p1[m - 2] -= 1
                p1[m + 1] -= 1
                p1[m - 1] = p1[m] = 2
                p2[m - 3] = p2[m] = self.__base - 1
                p2[m - 2] -= 2
                p2[m - 1] -= 2
                p3[m - 3] = p3[m - 2] = p3[m - 1] = 1
        else:
            p2[m - 2] -= 1
            p2[m - 1] -= 1
            p3[m - 2] = 0
        return [Digits(p1, self.__base), Digits(p2, self.__base), Digits(p3, self.__base)]

    def __algorithm5(self):
        s = Digits([1, 1] + [0 for _ in range(self.__length // 2 - 1)], self.__base)
        n = self - s
        k = 1
        if n.__is_special():
            n -= s
            k = 2
        temp = n.__summerpark()
        if temp[0].__length % 2 == 0:
            if k == 1:
                return [temp[0] + s, temp[1], temp[2]]
            return [temp[0] + s + s, temp[1], temp[2]]
        if (n.__digit_at(-1) - n.__digit_at(2)) % n.__base != 0:
            typ = DigitsType.B1
        else:
            typ = DigitsType.B2
        temp = n.__algorithm4(n.__get_config(typ))
        if k == 1:
            return [temp[0] + s, temp[1], temp[2]]
        return [temp[0] + s + s, temp[1], temp[2]]
