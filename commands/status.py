import os
import hashlib

def get_file_hash(filepath):
    """Calcule le hash SHA-1 d'un fichier comme Git le fait"""
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        header = f"blob {len(data)}\0".encode()
        full_data = header + data
        return hashlib.sha1(full_data).hexdigest()
    except:
        return None

def read_index():
    """Lit l'index et retourne un dictionnaire des fichiers indexés"""
    index_path = os.path.join(".gitC", "index")
    indexed_files = {}
    
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split()
                    if len(parts) >= 4:
                        mode, type_, hash_val = parts[0], parts[1], parts[2]
                        filename = " ".join(parts[3:])
                        indexed_files[filename] = {
                            'mode': mode,
                            'type': type_,
                            'hash': hash_val
                        }
    return indexed_files

def get_head_tree():
    """Récupère les fichiers du dernier commit (HEAD)"""
    try:
        # Lire HEAD
        head_path = os.path.join(".gitC", "HEAD")
        if not os.path.exists(head_path):
            return {}
            
        with open(head_path, "r") as f:
            ref_line = f.read().strip()
        
        # Obtenir le commit SHA
        commit_sha = None
        if ref_line.startswith("ref: "):
            ref_path = os.path.join(".gitC", ref_line[5:])
            if os.path.exists(ref_path):
                with open(ref_path, "r") as f:
                    commit_sha = f.read().strip()
        else:
            commit_sha = ref_line
        
        if not commit_sha:
            return {}
        
        # Lire le commit pour obtenir le tree SHA
        # Pour simplifier, on retourne un dictionnaire vide 
        # (dans un vrai Git, on devrait parser le commit puis le tree)
        return {}
        
    except:
        return {}

def get_working_directory_files():
    """Récupère tous les fichiers du répertoire de travail (non .gitC)"""
    working_files = {}
    
    for root, dirs, files in os.walk("."):
        # Ignorer le dossier .gitC et ses sous-dossiers
        if ".gitC" in dirs:
            dirs.remove(".gitC")
        
        # Ignorer les dossiers cachés et __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        for file in files:
            # Ignorer les fichiers cachés et les .pyc
            if not file.startswith('.') and not file.endswith('.pyc'):
                filepath = os.path.join(root, file)
                # Normaliser le chemin (enlever ./ au début)
                if filepath.startswith("./"):
                    filepath = filepath[2:]
                working_files[filepath] = get_file_hash(filepath)
    
    return working_files

def git_status():
    """Affiche le statut du dépôt Git"""
    
    # Vérifier que le dépôt est initialisé
    if not os.path.exists(".gitC"):
        print("Error: Not a git repository (no .gitC directory found)")
        return
    
    # Lire l'index
    indexed_files = read_index()
    
    # Lire les fichiers du répertoire de travail
    working_files = get_working_directory_files()
    
    # Lire les fichiers du dernier commit
    committed_files = get_head_tree()
    
    # Analyser les changements
    staged_for_commit = []  # Fichiers dans l'index mais différents du dernier commit
    modified_not_staged = []  # Fichiers modifiés par rapport à l'index
    untracked_files = []  # Fichiers non suivis
    
    # Vérifier les fichiers du répertoire de travail
    for filepath, working_hash in working_files.items():
        if filepath in indexed_files:
            # Fichier dans l'index
            if indexed_files[filepath]['hash'] != working_hash:
                # Modifié par rapport à l'index
                modified_not_staged.append(filepath)
            # Si le fichier est dans l'index et pas dans le dernier commit, il est staged
            if filepath not in committed_files:
                staged_for_commit.append(filepath)
        else:
            # Fichier non suivi
            untracked_files.append(filepath)
    
    # Vérifier les fichiers supprimés
    for filepath in indexed_files:
        if filepath not in working_files:
            modified_not_staged.append(f"{filepath} (deleted)")
    
    # Afficher le statut
    print("On branch master")  # Pour simplifier, on assume toujours master
    
    if not staged_for_commit and not modified_not_staged and not untracked_files:
        print("nothing to commit, working tree clean")
        return
    
    print()
    
    # Changements à committer
    if staged_for_commit:
        print("Changes to be committed:")
        print("  (use \"git rm --cached <file>...\" to unstage)")
        print()
        for file in sorted(staged_for_commit):
            print(f"        new file:   {file}")
        print()
    
    # Changements non stagés
    if modified_not_staged:
        print("Changes not staged for commit:")
        print("  (use \"git add <file>...\" to update what will be committed)")
        print("  (use \"git checkout -- <file>...\" to discard changes in working directory)")
        print()
        for file in sorted(modified_not_staged):
            if "(deleted)" in file:
                print(f"        deleted:    {file.replace(' (deleted)', '')}")
            else:
                print(f"        modified:   {file}")
        print()
    
    # Fichiers non suivis
    if untracked_files:
        print("Untracked files:")
        print("  (use \"git add <file>...\" to include in what will be committed)")
        print()
        for file in sorted(untracked_files):
            print(f"        {file}")
        print()
