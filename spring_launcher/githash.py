from hashlib import sha1
from io import BytesIO

class githash(object):
    def __init__(self):
        self.buf = BytesIO()

    def update(self, data):
        self.buf.write(data)

    def hexdigest(self):
        data = self.buf.getvalue()
        h = sha1()
        h.update(("blob %u\0" % len(data)).encode())
        h.update(data)

        return h.hexdigest()

def githash_data(data):
    h = githash()
    h.update(data)
    return h.hexdigest()

def githash_fileobj(fileobj):
    return githash_data(fileobj.read())

def calc_file_checksum(path):
    fileobj = open(path, "rb")
    return githash_fileobj(fileobj)
