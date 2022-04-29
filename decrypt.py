from umbral import (
    reencrypt,
    SecretKey,
    PublicKey,
    Capsule,
    VerifiedKeyFrag,
    decrypt_reencrypted,
)

with open("crypto/alices_pk.txt", "rb") as f:
    alices_public_key = PublicKey._from_exact_bytes(f.read())

with open("crypto/bob_sk.txt", "rb") as f:
    bob_private_key = SecretKey._from_exact_bytes(f.read())

with open("crypto/test.capsule", "rb") as f:
    capsule = Capsule._from_exact_bytes(f.read())

with open("crypto/test.ciphertext", "rb") as f:
    ciphertext = f.read()

kfrags = []
for i in range(3):
    with open("crypto/kfrag{}.txt".format(i), "rb") as f:
        kfrags.append(VerifiedKeyFrag.from_verified_bytes(f.read()))

cfrags = [reencrypt(capsule=capsule, kfrag=kfrag) for kfrag in kfrags]
cleartext = decrypt_reencrypted(
    receiving_sk=bob_private_key,
    delegating_pk=alices_public_key,
    capsule=capsule,
    verified_cfrags=cfrags,
    ciphertext=ciphertext,
)

print(cleartext)
