from Algorithms.Functions import *
from base.Point import Point


def get_secret(private_key, public_key: Point, curve: Curve=curve_P256):
    return multiply(public_key, private_key, curve.a)


