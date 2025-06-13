import os
import sys
import hashlib

GIT_DIR = ".git"

def hash_object(data):
    import hashlib
    header = f"blob {len(data)}\0".encode()
    full_data = header + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    return sha1, full_data

def write_object(sha1, full_data):
    dir_path = os.path.join(GIT_DIR, "objects", sha1[:2])
    file_path = os.path.join(dir_path, sha1[2:])
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(full_data)

def update_index(file_path, sha1):
    index_path = os.path.join(GIT_DIR, "index")
    lines = []
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            lines = f.readlines()
    # Supprimer l'entrée existante si déjà là
    lines = [line for line in lines if not line.startswith(file_path + " ")]
    lines.append(f"{file_path} {sha1}\n")
    with open(index_path, "w") as f:
        f.writelines(lines)

def run(args):
    if not args:
        print("Erreur : veuillez spécifier au moins un fichier.")
        return
    for file_path in args:
        if not os.path.isfile(file_path):
            print(f"Erreur : {file_path} n'est pas un fichier valide.")
            continue
        with open(file_path, "rb") as f:
            data = f.read()
        sha1, full_data = hash_object(data)
        write_object(sha1, full_data)
        update_index(file_path, sha1)
        print(f"Ajouté {file_path} avec hash {sha1}")
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add.py <fichier1> [fichier2 ...]")
    else:
        run(sys.argv[1:])
#     run(sys.argv[1:])