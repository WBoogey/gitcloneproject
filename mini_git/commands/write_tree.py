import os
import json
import hashlib
import zlib

INDEX_PATH = os.path.join(".git", "index.json")

def write_tree(return_oid=False):
    # Lire l'index
    if not os.path.exists(INDEX_PATH):
        print("Index not found.")
        return None

    with open(INDEX_PATH, "r") as f:
        entries = json.load(f)

    # Construire le contenu de l'objet tree
    lines = []
    for entry in entries:
        mode = "100644"  # mode Unix pour un fichier normal
        type_ = entry["type"]
        oid = entry["oid"]
        path = entry["path"]
        lines.append(f"{mode} {type_} {oid}\t{path}")

    tree_content = "\n".join(lines).encode()
    header = f"tree {len(tree_content)}\0".encode()
    full_data = header + tree_content

    # SHA-1 et compression
    oid = hashlib.sha1(full_data).hexdigest()
    compressed = zlib.compress(full_data)

    # Écrire dans .git/objects/<sha>
    object_dir = os.path.join(".git", "objects", oid[:2])
    object_path = os.path.join(object_dir, oid[2:])
    os.makedirs(object_dir, exist_ok=True)
    with open(object_path, "wb") as f:
        f.write(compressed)

    # Soit retourner, soit afficher le SHA
    if return_oid:
        return oid
    else:
        print(oid)
