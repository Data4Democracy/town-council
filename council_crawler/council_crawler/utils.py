import hashlib


def url_to_md5(url):
    m = hashlib.md5()
    m.update(url.encode())
    return m.hexdigest()
