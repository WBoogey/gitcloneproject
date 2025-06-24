import os
import json
from commands import hash_object

INDEX_PATH = os.path.join(".git", "index.json")

def read_index():
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r") as f:
            return json.load(f)
    return []

def write_index(entries):
    with open(INDEX_PATH, "w") as f:
        json.dump(entries, f, indent=2)

def git_add(path):
    if not os.path.isfile(path):
        print(f"Error: file '{path}' does not exist.")
        return

    oid = hash_object.hash_object(path, write=True)

    index = read_index()

    # Retirer les anciennes entrées pour ce fichier
    index = [entry for entry in index if entry["path"] != path]

    index.append({
        "path": path,
        "oid": oid,
        "type": "blob"
    })

    write_index(index)
    print(f"Added '{path}' to index.")
