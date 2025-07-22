import os

def git_rm(path, cached=False):
    """
    Supprime un fichier de l'index et optionnellement du système de fichiers
    
    Args:
        path (str): Chemin vers le fichier à supprimer
        cached (bool): Si True, supprime seulement de l'index, pas du système de fichiers
    """
    index_path = os.path.join(".gitC", "index")
    
    # Vérifier que le dépôt est initialisé
    if not os.path.exists(".gitC"):
        print("Error: Not a git repository (no .gitC directory found)")
        return
    
    # Vérifier que l'index existe
    if not os.path.exists(index_path):
        print("Error: No index found. Nothing to remove.")
        return
    
    # Lire l'index existant
    entries = {}
    found_file = False
    
    with open(index_path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) >= 4:
                    filename = " ".join(parts[3:])
                    if filename == path:
                        found_file = True
                        continue  # Ne pas ajouter cette entrée (= suppression)
                    entries[filename] = line
    
    # Vérifier que le fichier était dans l'index
    if not found_file:
        print(f"Error: pathspec '{path}' did not match any files in the index.")
        return
    
    # Supprimer le fichier du système de fichiers si nécessaire
    if not cached:
        if os.path.exists(path):
            try:
                os.remove(path)
                print(f"rm '{path}'")
            except OSError as e:
                print(f"Error: Cannot remove '{path}': {e}")
                return
        else:
            print(f"Warning: '{path}' not found in working directory")
    
    # Réécrire l'index sans le fichier supprimé
    with open(index_path, "w") as f:
        for entry in sorted(entries.values()):
            f.write(entry + "\n")
    
    if cached:
        print(f"Removed '{path}' from index (file kept in working directory)")
    else:
        print(f"Removed '{path}' from index and working directory")

def git_rm_cached(path):
    """Supprime un fichier seulement de l'index (garde le fichier sur disque)"""
    git_rm(path, cached=True)
