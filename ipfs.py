import ipfsApi


def upload_ipfs(file_path):
    api = ipfsApi.Client("http://ipfs", 5001)
    res = api.add(file_path)
    print(res)
    return res
