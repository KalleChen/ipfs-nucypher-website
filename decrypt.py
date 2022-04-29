from umbral import (
    reencrypt,
    SecretKey,
    PublicKey,
    Capsule,
    VerifiedKeyFrag,
    decrypt_reencrypted,
)
import requests
import shutil
import os

with open("crypto/alices_pk.txt", "rb") as f:
    alices_public_key = PublicKey._from_exact_bytes(f.read())
with open("crypto/bob_sk.txt", "rb") as f:
    bob_private_key = SecretKey._from_exact_bytes(f.read())

kfrags = []
for i in range(3):
    with open("crypto/kfrag{}.txt".format(i), "rb") as f:
        kfrags.append(VerifiedKeyFrag.from_verified_bytes(f.read()))


def decrypt_file(file_url):
    res = requests.get(file_url)
    print(res.content)
    with open("download.zip", "wb") as f:
        f.write(res.content)
    os.mkdir("download")
    shutil.unpack_archive("download.zip", "./download")
    os.remove("download.zip")

    with open("download/capsule", "rb") as f:
        capsule = Capsule._from_exact_bytes(f.read())
    with open("download/ciphertext", "rb") as f:
        ciphertext = f.read()
    with open("download/file_name", "r") as f:
        file_name = f.read()

    cfrags = [reencrypt(capsule=capsule, kfrag=kfrag) for kfrag in kfrags]
    cleartext = decrypt_reencrypted(
        receiving_sk=bob_private_key,
        delegating_pk=alices_public_key,
        capsule=capsule,
        verified_cfrags=cfrags,
        ciphertext=ciphertext,
    )
    with open("files/" + file_name, "wb") as f:
        f.write(cleartext)
    shutil.rmtree("download")
    return file_name
