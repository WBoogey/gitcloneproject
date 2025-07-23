import os
import hashlib
import zlib

GIT_DIR = ".gitC"

def get_git_path(path):
    return os.path.join(GIT_DIR, path)

def read_file(path):
    with open(path, "r") as f:
        return f.read().strip()

def write_file(path, data):
    with open(path, "w") as f:
        f.write(data)

def read_object(oid):
    path = get_git_path(os.path.join("objects", oid[:2], oid[2:]))
    with open(path, "rb") as f:
        compressed = f.read()
    return zlib.decompress(compressed)

def write_object(data):
    oid = hashlib.sha1(data).hexdigest()
    path = get_git_path(os.path.join("objects", oid[:2], oid[2:]))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(zlib.compress(data))
    return oid

def update_HEAD(ref_or_sha):
    head_path = get_git_path("HEAD")
    if ref_or_sha.startswith("refs/"):
        write_file(head_path, f"ref: {ref_or_sha}")
    else:
        write_file(head_path, ref_or_sha)

def get_oid(name):
    head_path = get_git_path("HEAD")
    refs_heads = get_git_path(os.path.join("refs", "heads", name))

    if name == "HEAD":
        value = read_file(head_path)
        if value.startswith("ref:"):
            return read_file(get_git_path(value[5:].strip()))
        return value
    elif os.path.exists(refs_heads):
        return read_file(refs_heads)
    elif len(name) == 40:
        return name
    else:
        print(f"fatal: Not a valid object name: {name}")
        exit(1)

def get_commit_tree_oid(commit_oid):
    raw = read_object(commit_oid)
    header, body = raw.split(b"\x00", 1)
    lines = body.decode().splitlines()
    for line in lines:
        if line.startswith("tree "):
            return line.split()[1]
    raise Exception("Invalid commit object: no tree")

def read_tree(tree_oid):
    from commands.write_tree import parse_tree
    raw = read_object(tree_oid)
    # Séparation header / contenu tree
    _, data = raw.split(b"\x00", 1)
    entries = parse_tree(data)

    # Nettoyer le répertoire de travail sauf .gitC
    for root, dirs, files in os.walk(".", topdown=False):
        if ".gitC" in root:
            continue
        for f in files:
            os.remove(os.path.join(root, f))

    # Écrire les fichiers du tree dans le système
    for entry in entries:
        blob_oid, path = entry["oid"], entry["path"]
        blob_raw = read_object(blob_oid)
        _, blob_data = blob_raw.split(b"\x00", 1)

        dir_path = os.path.dirname(path)
        if dir_path != "":
            os.makedirs(dir_path, exist_ok=True)

        with open(path, "wb") as f:
            f.write(blob_data)

def read_tree_into_index(tree_oid):
    from commands.write_tree import parse_tree

    raw = read_object(tree_oid)
    _, data = raw.split(b"\x00", 1)
    entries = parse_tree(data)

    index_path = get_git_path("index")
    with open(index_path, "w") as f:
        for entry in entries:
            # On écrit ligne mode type oid filename (ici mode 100644 et type blob par défaut)
            f.write(f"100644 blob {entry['oid']} {entry['path']}\n")
