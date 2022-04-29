from umbral import SecretKey, encrypt, generate_kfrags, Signer, PublicKey
import shutil

with open("crypto/alices_pk.txt", "rb") as f:
    alices_public_key = PublicKey._from_exact_bytes(f.read())
with open("crypto/alices_sk.txt", "rb") as f:
    alices_secret_key = SecretKey._from_exact_bytes(f.read())
with open("crypto/bob_pk.txt", "rb") as f:
    bob_public_key = PublicKey._from_exact_bytes(f.read())

alices_signer = Signer(alices_secret_key)


def encrypt_file(file_path, file_name):
    with open(file_path, "rb") as f:
        message = f.read()
        capsule, ciphertext = encrypt(alices_public_key, message)
        with open("files/capsule", "wb") as f:
            f.write(capsule.__bytes__())
        with open("files/ciphertext", "wb") as f:
            f.write(ciphertext)
        with open("files/file_name", "w") as f:
            f.write(file_name)
        shutil.make_archive("zip_file", "zip", "files")

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
