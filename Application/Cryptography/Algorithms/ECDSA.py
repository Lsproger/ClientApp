def get_signature(z, private_key, curve: Curve=curve_P256):
    s = r = k = 0
    _r = lambda __k: multiply(curve.g, k).x % curve.n
    while s == 0:
        k = get_random_k()
        while r == 0:
            r = _r(k)
        _k_ = inverse_of(k, curve.n)
        what = (z + r * private_key)
        s = (_k_ * what) % curve.n
    return r, s


def check_signature(public_key, z, signature, curve: Curve=curve_P256):
    u1 = (inverse_of(signature[1], curve.n) * z) % curve.n
    u2 = (inverse_of(signature[1], curve.n) * signature[0]) % curve.n
    u1G = multiply(curve.g, u1)
    u2Q = multiply(public_key, u2)
    P = points_sum(u1G, u2Q)
    _r = P.x % curve.n
    if signature[0] == _r:
        return 1
    else:
        return 0


