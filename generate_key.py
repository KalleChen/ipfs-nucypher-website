from umbral import SecretKey

alices_secret_key = SecretKey.random()
alices_public_key = alices_secret_key.public_key()

bob_secret_key = SecretKey.random()
bob_public_key = bob_secret_key.public_key()

with open("crypto/alices_pk.txt", "wb") as f:
    f.write(alices_public_key.__bytes__())
with open("crypto/alices_sk.txt", "wb") as f:
    f.write(alices_secret_key.to_secret_bytes())
with open("crypto/bob_pk.txt", "wb") as f:
    f.write(bob_public_key.__bytes__())
with open("crypto/bob_sk.txt", "wb") as f:
    f.write(bob_secret_key.to_secret_bytes())
