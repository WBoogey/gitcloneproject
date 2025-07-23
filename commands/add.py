import os
import hashlib
import zlib

def git_add(path):
    """Ajoute un fichier à l'index ou gère sa suppression"""
    
    # Vérifier si le fichier existe
    if not os.path.isfile(path):
        # Vérifier si le fichier était dans l'index (pour gérer les suppressions)
        index_path = os.path.join(".gitC", "index")
        
        if os.path.exists(index_path):
            # Lire l'index existant
            entries = {}
            file_was_tracked = False
            
            with open(index_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split()
                        if len(parts) >= 4:
                            filename = " ".join(parts[3:])
                            if filename == path:
                                file_was_tracked = True
                                # Ne pas ajouter cette entrée (= suppression)
                                continue
                            entries[filename] = line
            
            if file_was_tracked:
                # Le fichier était suivi mais n'existe plus -> "stage" la suppression
                with open(index_path, "w") as f:
                    for entry in sorted(entries.values()):
                        f.write(entry + "\n")
                
                print(f"Staged deletion of '{path}'")
                return
            else:
                print(f"Error: file '{path}' not found and was not being tracked.")
                return
        else:
            print(f"Error: file '{path}' not found.")
            return
    
    # Lire le fichier
    with open(path, "rb") as f:
        data = f.read()
    
    # Créer l'objet blob
    header = f"blob {len(data)}\0".encode()
    full_data = header + data
    oid = hashlib.sha1(full_data).hexdigest()
    
    # Sauvegarder l'objet blob
    compressed = zlib.compress(full_data)
    object_dir = os.path.join(".gitC", "objects", oid[:2])
    object_path = os.path.join(object_dir, oid[2:])
    os.makedirs(object_dir, exist_ok=True)
    
    with open(object_path, "wb") as f:
        f.write(compressed)
    
    # Ajouter à l'index
    index_path = os.path.join(".gitC", "index")
    
    # Lire l'index existant
    entries = {}
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 4:
                        filename = " ".join(parts[3:])
                        entries[filename] = line
    
    # Ajouter/mettre à jour l'entrée
    entries[path] = f"100644 blob {oid} {path}"
    
    # Réécrire l'index
    with open(index_path, "w") as f:
        for entry in sorted(entries.values()):
            f.write(entry + "\n")
    
    print(f"Added {path} to index")