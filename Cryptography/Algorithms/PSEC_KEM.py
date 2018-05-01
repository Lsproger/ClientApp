from User import *
from Cryptography.base.Point import Point
from pbkdf2 import PBKDF2
from Crypto.Cipher import AES
from random import choice
from string import ascii_letters


# Key generation
def generate_keys(curve: Curve=curve_P256):
    private = get_random_k(curve)
    public = get_public_key(private, curve)
    return private, public


# Encryption
def encrypt(public_key: Point, msg, curve: Curve=curve_P256):
    l = 128
    r = int(bin(get_random_k())[2:l+2], 2)
    keylen = 256
    _t_len = keylen + 128
    len_ = (keylen + _t_len) / 8
    pre_key = PBKDF2(str(r), 'salt').read(int(len_))
    t_ = int.from_bytes(pre_key, 'big') >> keylen
    K = int(bin(int.from_bytes(pre_key, 'big') << _t_len)[2:keylen + 2], 2)
    t = t_ % curve.n
    T = multiply(curve.g, t, curve.a)
    U = multiply(public_key, t, curve.a)
    bytes_u_x_ = bytes(str(U.x)[:8], 'utf-8')
    kdf_T_U = int.from_bytes(PBKDF2(str(T.x), bytes_u_x_).read(int(l / 8)), 'big')
    s = r ^ kdf_T_U
    obj = AES.new(str(K)[:32], AES.MODE_CBC, "ABCDEFGHABCDEFGH")
    _n = 16 - msg.__len__() % 16
    rand_str = ''.join(choice(ascii_letters) for i in range(_n))
    c_text = obj.encrypt(msg+rand_str)
    return s, T, c_text


# Decryption
def decrypt(private_key, s, T: Point, c_text, curve: Curve=curve_P256):
    l = 128
    U = multiply(T, private_key)
    bytes_u_x_ = bytes(str(U.x)[:8], 'utf-8')
    kdf_T_U = int.from_bytes(PBKDF2(str(T.x), bytes_u_x_).read(int(l / 8)), 'big')
    r = s ^ kdf_T_U
    keylen = 256
    _t_len = keylen + 128
    len_ = (keylen + _t_len) / 8
    pre_key = PBKDF2(str(r), 'salt').read(int(len_))
    t_ = int.from_bytes(pre_key, 'big') >> keylen
    K = int(bin(int.from_bytes(pre_key, 'big') << _t_len)[2:keylen + 2], 2)
    t = t_ % curve.n
    T_ = multiply(curve.g, t, curve.a)
    if T_.x == T.x and T_.y == T.y:
        obj = AES.new(str(K)[:32], AES.MODE_CBC, "ABCDEFGHABCDEFGH")
        return obj.decrypt(c_text)
    else:
        return 'incorrect'

