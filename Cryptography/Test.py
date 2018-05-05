from Cryptography.Functions import (generate_keys, get_secret)

da, Qa = generate_keys()
db, Qb = generate_keys()

print(da, Qa.x)
print(db, Qb.x)

sec1 = get_secret(db, Qa)
sec2 = get_secret(da, Qb)

print(sec1.x, sec2.x)
