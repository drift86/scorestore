import hashlib
thing = hashlib.md5(b'Hello World')
thing = thing.hexdigest()
print(thing)

