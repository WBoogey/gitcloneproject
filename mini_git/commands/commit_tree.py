import os
import time
import hashlib
import zlib

def commit_tree(tree_oid, message, parent=None):
    lines = [f"tree {tree_oid}"]

    if parent:
        lines.append(f"parent {parent}")

    # Auteur (simplifié)
    author = "You <you@example.com>"
    timestamp = int(time.time())
    lines.append(f"author {author} {timestamp} +0000")
    lines.append(f"committer {author} {timestamp} +0000")
    lines.append("")  # ligne vide
    lines.append(message)

    content = "\n".join(lines).encode()
    header = f"commit {len(content)}\0".encode()
    full_data = header + content

    oid = hashlib.sha1(full_data).hexdigest()
    compressed = zlib.compress(full_data)

    # Sauvegarde dans .git/objects/
    object_dir = os.path.join(".git", "objects", oid[:2])
    object_path = os.path.join(object_dir, oid[2:])
    os.makedirs(object_dir, exist_ok=True)
    with open(object_path, "wb") as f:
        f.write(compressed)

    print(oid)  # SHA du commit
    return oid  # ✅ C'est ici qu'on retourne le SHA du commit
