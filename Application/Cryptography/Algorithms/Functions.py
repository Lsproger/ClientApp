# from Curve import Curve
# from Curve import curve_P256
# from Operations import multiply



class Point:

    def __init__(self, x, y):
        self.__point = [x, y]

    @property
    def x(self):
        return self.__point[0]

    @property
    def y(self):
        return self.__point[1]

    @x.setter
    def x(self, value):
        self.__point[0] = value

    @y.setter
    def y(self, value):
        self.__point[1] = value





class Curve:

    def __init__(self, a=-3,
                 b=0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
                 m=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
                 n=0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
                 g: Point = Point(
                     0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                     0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
                 ):
        self.__curve = (a, b, m, n, g)

    @property
    def a(self):
        return self.__curve[0]

    @property
    def b(self):
        return self.__curve[1]

    @property
    def m(self):
        return self.__curve[2]

    @property
    def n(self):
        return self.__curve[3]

    @property
    def g(self):
        return self.__curve[4]


# Curve P-256(a,b,m,n,g):
curve_P256 = Curve(-3,
                   0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
                   0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
                   0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
                   Point(0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
                         0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)
                   )



__a = curve_P256.a


def extended_euclidean_algorithm(a, b):
    """
    Возвращает кортеж из трёх элементов (gcd, x, y), такой, что
    a * x + b * y == gcd, где gcd - наибольший
    общий делитель a и b.

    В этой функции реализуется расширенный алгоритм
    Евклида и в худшем случае она выполняется O(log b).
    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def inverse_of(n, p):
    """
    Возвращает обратную величину
    n по модулю p.

    Эта функция возвращает такое целое число m, при котором
    (n * m) % p == 1.
    """
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        # Или n равно 0, или p не является простым.
        raise ValueError(
            '{} has no multiplicative inverse '
            'mod {}'.format(n, p))
    else:
        return x % p




def multiply(p: Point, k, a=__a):
    """

    Умножение методом сложения с удвоением:
    Представление k в двоичном виде
    1 - удвоение результата
    0 - прибавление к результату
    """
    res = p
    _k = bin(k)[3:]  # int in bin like '0b1....' (1st bit always = 1)
    for n in _k:    # so we don't need 3 first bits and res = p on 1st iteration
        if int(n):
            res = points_sum(p, points_sum(res, res, a), a)
        else:
            res = points_sum(res, res, a)
    return res


def points_sum(p1: Point, p2: Point, a=__a):
    mod_m = curve_P256.m
    if p1.x != p2.x:
        s = ((p1.y - p2.y) * inverse_of((p1.x - p2.x), mod_m)) % mod_m
    else:
        if p1.y == -p2.y:
            return Point(0, 0)
        elif p1.y == p2.y and p1.y == 0:
            return None
        else:
            s = (((3 * p1.x * p1.x) + a) * inverse_of((2 * p1.y), mod_m)) % mod_m
    if s != 0:
            r_x = ((s * s) - p1.x - p2.x) % mod_m
            r_y = (-p1.y + s * (p1.x - r_x)) % mod_m
    assert s != 0, 's is 0'
    res = Point(r_x, r_y)
    assert is_on_curve(res), 'Result point is not on curve'
    return res


def is_on_curve(point: Point, curve: Curve = curve_P256):
    if point is None:  # point at INF
        return True
    x, y = point.x, point.y
    return ((y * y - x * x * x - curve.a * x - curve.b) % curve.m) == 0




def get_random_k(curve: Curve=curve_P256):
    import random
    return random.randint(2, curve.n - 1)


def get_public_key(private_key, curve: Curve=curve_P256):
    return multiply(curve.g, private_key, curve.a)


def generate_keys(curve: Curve=curve_P256):
    private = get_random_k(curve)
    public = get_public_key(private, curve)
    return private, public


def get_hash(data, n):
    """Returns the truncated SHA521 hash of the message."""
    import hashlib
    message_hash = hashlib.sha512(data).digest()
    e = int.from_bytes(message_hash, 'big')

    # FIPS 180 says that when a hash needs to be truncated, the rightmost bits
    # should be discarded.
    z = e >> (e.bit_length() - n.bit_length())

    assert z.bit_length() <= n.bit_length()

    return z



