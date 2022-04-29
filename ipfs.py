import ipfsApi
import os


def upload_ipfs():
    api = ipfsApi.Client("http://ipfs", 5001)
    res = api.add("zip_file.zip")
    print(res)
    os.remove("zip_file.zip")
    return res
