import hashlib

def hash_object(data: bytes) -> str:
    import zlib
    header = f"blob {len(data)}\0".encode()
    full_data = header + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    compressed = zlib.compress(full_data)
    return sha1
