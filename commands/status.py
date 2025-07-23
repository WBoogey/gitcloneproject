import os
import hashlib
import zlib

def get_file_hash(filepath):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        header = f"blob {len(data)}\0".encode()
        full_data = header + data
        return hashlib.sha1(full_data).hexdigest()
    except:
        return None

def read_index():
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
        
        # Lire l'objet commit
        commit_obj_path = os.path.join(".gitC", "objects", commit_sha[:2], commit_sha[2:])
        if not os.path.exists(commit_obj_path):
            return {}
        
        with open(commit_obj_path, "rb") as f:
            compressed_data = f.read()
        
        full_data = zlib.decompress(compressed_data)
        header, content = full_data.split(b'\x00', 1)
        
        if not header.startswith(b'commit '):
            return {}
        
        # Parser le commit pour obtenir le tree SHA
        lines = content.decode().splitlines()
        tree_sha = None
        
        for line in lines:
            if line.startswith("tree "):
                tree_sha = line[5:]
                break
        
        if not tree_sha:
            return {}
        
        # Lire l'objet tree
        return parse_tree_object(tree_sha)
        
    except Exception as e:
        return {}

def parse_tree_object(tree_sha):
    """Parse un objet tree et retourne un dictionnaire des fichiers"""
    try:
        tree_obj_path = os.path.join(".gitC", "objects", tree_sha[:2], tree_sha[2:])
        if not os.path.exists(tree_obj_path):
            return {}
        
        with open(tree_obj_path, "rb") as f:
            compressed_data = f.read()
        
        full_data = zlib.decompress(compressed_data)
        header, content = full_data.split(b'\x00', 1)
        
        if not header.startswith(b'tree '):
            return {}
        
        tree_files = {}
        pos = 0
        
        while pos < len(content):
            # Trouver l'espace après le mode
            space_pos = content.find(b' ', pos)
            if space_pos == -1:
                break
            
            mode = content[pos:space_pos].decode()
            
            # Trouver le null byte après le nom du fichier
            null_pos = content.find(b'\x00', space_pos + 1)
            if null_pos == -1:
                break
            
            filename = content[space_pos + 1:null_pos].decode()
            
            # Les 20 bytes suivants sont le SHA-1
            if null_pos + 21 > len(content):
                break
            
            sha_bytes = content[null_pos + 1:null_pos + 21]
            sha_hex = sha_bytes.hex()
            
            tree_files[filename] = {
                'mode': mode,
                'hash': sha_hex
            }
            
            pos = null_pos + 21
        
        return tree_files
        
    except Exception as e:
        return {}

def get_working_directory_files():
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
    deleted_not_staged = []  # Fichiers supprimés du working directory
    staged_deletions = []  # Fichiers supprimés de l'index
    
    # Ensemble de tous les fichiers connus
    all_files = set(working_files.keys()) | set(indexed_files.keys()) | set(committed_files.keys())
    
    for filepath in all_files:
        in_working = filepath in working_files
        in_index = filepath in indexed_files
        in_commit = filepath in committed_files
        
        working_hash = working_files.get(filepath)
        index_hash = indexed_files.get(filepath, {}).get('hash')
        commit_hash = committed_files.get(filepath, {}).get('hash')
        
        # Fichier non suivi (dans working, pas dans index)
        if in_working and not in_index:
            untracked_files.append(filepath)
        
        # Fichier dans l'index
        elif in_index:
            # Changements staged (index différent du commit)
            if not in_commit or index_hash != commit_hash:
                if in_commit:
                    staged_for_commit.append(('modified', filepath))
                else:
                    staged_for_commit.append(('new', filepath))
            
            # Changements non staged (working différent de l'index)
            if in_working:
                if index_hash != working_hash:
                    modified_not_staged.append(filepath)
            else:
                # Fichier supprimé du working directory
                deleted_not_staged.append(filepath)
        
        # Fichier supprimé de l'index (était dans commit, plus dans index)
        elif in_commit and not in_index:
            staged_deletions.append(filepath)
    
    # Afficher le statut
    print("On branch master")  # Pour simplifier, on assume toujours master
    
    # Vérifier s'il y a des changements
    has_changes = (staged_for_commit or staged_deletions or 
                   modified_not_staged or deleted_not_staged or untracked_files)
    
    if not has_changes:
        print("nothing to commit, working tree clean")
        return
    
    print()
    
    # Changements à committer
    if staged_for_commit or staged_deletions:
        print("Changes to be committed:")
        print("  (use \"git rm --cached <file>...\" to unstage)")
        print()
        
        # Fichiers ajoutés/modifiés
        for change_type, filepath in sorted(staged_for_commit):
            if change_type == 'new':
                print(f"        new file:   {filepath}")
            else:
                print(f"        modified:   {filepath}")
        
        # Fichiers supprimés
        for filepath in sorted(staged_deletions):
            print(f"        deleted:    {filepath}")
        
        print()
    
    # Changements non stagés
    if modified_not_staged or deleted_not_staged:
        print("Changes not staged for commit:")
        print("  (use \"git add <file>...\" to update what will be committed)")
        print("  (use \"git checkout -- <file>...\" to discard changes in working directory)")
        print()
        
        # Fichiers modifiés
        for filepath in sorted(modified_not_staged):
            print(f"        modified:   {filepath}")
        
        # Fichiers supprimés
        for filepath in sorted(deleted_not_staged):
            print(f"        deleted:    {filepath}")
        
        print()
    
    # Fichiers non suivis
    if untracked_files:
        print("Untracked files:")
        print("  (use \"git add <file>...\" to include in what will be committed)")
        print()
        for filepath in sorted(untracked_files):
            print(f"        {filepath}")
        print()
