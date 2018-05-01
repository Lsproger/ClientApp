from Cryptography.base.Curve import Curve
from Cryptography.base.Curve import curve_P256
from Cryptography.base.Operations import multiply


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



