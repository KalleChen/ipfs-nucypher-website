# ipfs-nucypher-website

Use nucypher to encrypt and upload to ipfs.

## Usage
```
mkdir ipfs files crypto
docker compose up -d
```

Flask website is hosted on http://0.0.0.0:3000

IPFS webUI is hosted on http://0.0.0.0:5001/webui

IPFS api server is listening on /ip4/0.0.0.0/tcp/5001

## How it works

After the containers start, it will generate Alice and Box's public/private key in `crypto` folder. All the en/decrypt will use these keys

### Upload

It will use Alice's public key to generate two files, capsule and the ciphertext. Zip these files and upload to the IPFS, you will see the HASH after the upload process is finished on the screen. 

Then it will use Alice's private key and Bob's public key to grant that Bob can access the file. It will generate 3 kfrag stored in `crypto` folder

### Download

It will use the HASH you provide and download the zip file and unzip it. Then use Bob's private to decrypt the ciphertext.

