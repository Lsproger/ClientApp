__a = curve_P256.a


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

# 21 * P = 10101 * P = (((((2 * P) * 2) + P) * 2) * 2 + P)


