import os
import zlib

def cat_file(oid):
    path = os.path.join(".gitC", "objects", oid[:2], oid[2:])
    
    print(f"[DEBUG] Looking for object at: {path}")

    if not os.path.exists(path):
        print(f"Error: object {oid} not found.")
        return

    with open(path, "rb") as f:
        compressed_data = f.read()

    print(f"[DEBUG] Compressed size: {len(compressed_data)} bytes")

    try:
        full_data = zlib.decompress(compressed_data)
    except Exception as e:
        print(f"Decompression failed: {e}")
        return

    print(f"[DEBUG] Decompressed size: {len(full_data)} bytes")

    try:
        zero_index = full_data.index(b'\x00')
    except ValueError:
        print("[ERROR] No null byte found in decompressed data.")
        return

    header = full_data[:zero_index]
    content = full_data[zero_index + 1:]

    print(f"[DEBUG] Header: {header}")
    print(f"[DEBUG] Raw content: {repr(content)}")

    try:
        print(content.decode(errors="replace"))
    except Exception as e:
        print(f"[ERROR] Failed to decode content: {e}")
