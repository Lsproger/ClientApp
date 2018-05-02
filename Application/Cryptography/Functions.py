from Application.Cryptography.Curve import Curve
from Application.Cryptography.Curve import curve_P256
from Application.Cryptography.Operations import multiply, inverse_of, points_sum, Point



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




def get_random_k(curve: Curve=curve_P256):
    import random
    return random.randint(2, curve.n - 1)


def get_public_key(private_key, curve: Curve=curve_P256):
    return multiply(curve.g, private_key, curve.a)


def get_secret(private_key, public_key: Point, curve: Curve=curve_P256):
    return multiply(public_key, private_key, curve.a)



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



