import hashlib
import os
import zlib

def hash_object(path, write=False):
    if not os.path.isfile(path):
        print(f"Error: file '{path}' not found.")
        return

    with open(path, "rb") as f:
        data = f.read()

    header = f"blob {len(data)}\0".encode()
    full_data = header + data

    oid = hashlib.sha1(full_data).hexdigest()
    print(oid)

    if write:
        compressed = zlib.compress(full_data)
        object_dir = os.path.join(".gitC", "objects", oid[:2])
        object_path = os.path.join(object_dir, oid[2:])
        os.makedirs(object_dir, exist_ok=True)
        with open(object_path, "wb") as f:
            f.write(compressed)

    return oid

