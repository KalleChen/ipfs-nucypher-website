from umbral import SecretKey, encrypt, generate_kfrags, Signer

alices_secret_key = SecretKey.random()
alices_public_key = alices_secret_key.public_key()
alices_signer = Signer(alices_secret_key)

bob_secret_key = SecretKey.random()
bob_public_key = bob_secret_key.public_key()

with open("crypto/alices_pk.txt", "wb") as f:
    f.write(alices_public_key.__bytes__())
with open("crypto/bob_sk.txt", "wb") as f:
    f.write(bob_secret_key.to_secret_bytes())

with open("test.txt", "rb") as f:
    message = f.read()
    capsule, ciphertext = encrypt(alices_public_key, message)
    with open("crypto/test.capsule", "wb") as f:
        f.write(capsule.__bytes__())
    with open("crypto/test.ciphertext", "wb") as f:
        f.write(ciphertext)

kfrags = generate_kfrags(
    delegating_sk=alices_secret_key,
    receiving_pk=bob_public_key,
    signer=alices_signer,
    threshold=2,
    shares=3,
)

for i in range(3):
    with open("crypto/kfrag{}.txt".format(i), "wb") as f:
        f.write(kfrags[i].__bytes__())
