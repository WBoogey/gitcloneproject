import os
import hashlib
import zlib

def write_tree(return_oid=False):
    """Crée un objet tree à partir de l'index"""
    index_path = os.path.join(".gitC", "index")
    
    if not os.path.exists(index_path):
        print("Error: No index found. Use 'git add' to add files first.")
        return None if return_oid else None
    
    # Lire l'index
    entries = []
    with open(index_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) >= 2:
                    # Format attendu: <mode> <type> <hash> <filename>
                    # Ou format simple: <hash> <filename>
                    if len(parts) == 2:
                        # Format simple: hash filename
                        hash_val, filename = parts
                        entries.append({
                            "mode": "100644",  # Mode par défaut pour un fichier normal
                            "type": "blob",    # Type par défaut
                            "hash": hash_val,
                            "name": filename
                        })
                    elif len(parts) >= 4:
                        # Format complet: mode type hash filename
                        mode, type_, hash_val = parts[0], parts[1], parts[2]
                        filename = " ".join(parts[3:])  # Au cas où le nom contient des espaces
                        entries.append({
                            "mode": mode,
                            "type": type_,
                            "hash": hash_val,
                            "name": filename
                        })
    
    if not entries:
        print("Error: Index is empty. Use 'git add' to add files first.")
        return None if return_oid else None
    
    # Trier les entrées par nom (comme Git le fait)
    entries.sort(key=lambda x: x["name"])
    
    # Construire le contenu du tree
    tree_content = b""
    for entry in entries:
        mode = entry["mode"]
        name = entry["name"]
        hash_bytes = bytes.fromhex(entry["hash"])
        
        # Format: "<mode> <name>\0<hash_bytes>"
        entry_line = f"{mode} {name}".encode() + b"\0" + hash_bytes
        tree_content += entry_line
    
    # Créer l'objet tree
    header = f"tree {len(tree_content)}\0".encode()
    full_data = header + tree_content
    
    # Calculer le SHA-1
    tree_oid = hashlib.sha1(full_data).hexdigest()
    
    # Sauvegarder l'objet
    compressed = zlib.compress(full_data)
    object_dir = os.path.join(".gitC", "objects", tree_oid[:2])
    object_path = os.path.join(object_dir, tree_oid[2:])
    os.makedirs(object_dir, exist_ok=True)
    
    with open(object_path, "wb") as f:
        f.write(compressed)
    
    if return_oid:
        return tree_oid
    else:
        print(tree_oid)
        return tree_oid
    
def parse_tree(data):
    """
    Parse les données brutes d'un objet tree Git et retourne une liste
    d'entrées au format dict {mode, path, oid}

    Format d'une entrée dans un tree Git:
    <mode> SPACE <filename> NULL <20 bytes SHA binaire>

    Args:
      data (bytes): données décompressées du tree (sans l'en-tête)

    Returns:
      list of dict: [{mode, path, oid}, ...]
    """
    entries = []
    i = 0
    while i < len(data):
        space = data.find(b" ", i)
        mode = data[i:space].decode("utf-8")

        null = data.find(b"\x00", space)
        path = data[space + 1:null].decode("utf-8")

        oid_bin = data[null + 1:null + 21]
        oid = oid_bin.hex()

        entries.append({"mode": mode, "path": path, "oid": oid})

        i = null + 21

    return entries
