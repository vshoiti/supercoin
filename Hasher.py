from Crypto.Hash import SHA256


def hash_string(string):
    string = string.encode('utf-8')
    return SHA256.new(string).hexdigest()