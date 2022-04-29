import os
import ipfsApi


def upload_ipfs(file_path, file_name):
    with open(file_path, "rb") as f:
        file = f.read()
        with open(file_name, "wb") as f:
            f.write(file)
            api = ipfsApi.Client("http://ipfs", 5001)
            res = api.add(file_name)
            print(res)
            os.remove(file_name)
            return res
