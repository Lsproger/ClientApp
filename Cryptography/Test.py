from Cryptography.Functions import (generate_keys, get_secret)
from Cryptography.PSEC_KEM import *
da, Qa = generate_keys()
db, Qb = generate_keys()

print(da, Qa.x)
print(db, Qb.x)

sec1 = get_secret(db, Qa)
sec2 = get_secret(da, Qb)

print(sec1.x, sec2.x)

print('\n\n\n\n')
print('PSEC')

s, T, c_Text = encrypt(Qa, 'Hello, mtfckr')
print(c_Text)
text = decrypt(da, s, T, c_Text)

print(text)
