# y2 = x3 + a x + b (mod m)
# 4a^3 + 27b^2 ≠ 0 (mod m)
from Cryptography.base.Point import Point


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



