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

def get_oid(name):
    """Helper to read oid from HEAD or refs."""
    head_path = os.path.join(".gitC", "HEAD")
    if not os.path.exists(head_path):
        return None
    with open(head_path, "r") as f:
        content = f.read().strip()
    if content.startswith("ref: "):
        ref_path = os.path.join(".gitC", content[5:])
        if os.path.exists(ref_path):
            with open(ref_path, "r") as rf:
                return rf.read().strip()
    else:
        # HEAD contains direct SHA
        return content
    return None

def get_current_branch():
    """Récupère le nom de la branche courante ou None si détachée"""
    head_path = os.path.join(".gitC", "HEAD")
    if not os.path.exists(head_path):
        return None
    with open(head_path, "r") as f:
        content = f.read().strip()
    if content.startswith("ref: "):
        # ex: "ref: refs/heads/master"
        return content[5:].split('/')[-1]
    else:
        # HEAD détaché sur un SHA
        return None

def get_head_tree():
    """Récupère les fichiers du dernier commit (HEAD) — temporairement vide"""
    # TODO: Implémenter le parsing des commits et trees pour un vrai résultat
    return {}

def get_working_directory_files():
    """Récupère tous les fichiers du répertoire de travail (hors .gitC)"""
    working_files = {}
    
    for root, dirs, files in os.walk("."):
        if ".gitC" in dirs:
            dirs.remove(".gitC")
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if not file.startswith('.') and not file.endswith('.pyc'):
                filepath = os.path.join(root, file)
                if filepath.startswith("./"):
                    filepath = filepath[2:]
                working_files[filepath] = get_file_hash(filepath)
    
    return working_files

def git_status():
    """Affiche le statut du dépôt Git"""
    
    if not os.path.exists(".gitC"):
        print("Error: Not a git repository (no .gitC directory found)")
        return
    
    branch = get_current_branch()
    if branch:
        print(f"On branch {branch}")
    else:
        head_oid = get_oid("HEAD")
        if head_oid:
            print(f"HEAD detached at {head_oid}")
        else:
            print("No commits yet")

    indexed_files = read_index()
    working_files = get_working_directory_files()
    committed_files = get_head_tree()
    
    staged_for_commit = []      # fichiers dans index mais différents du commit HEAD
    modified_not_staged = []    # fichiers modifiés par rapport à index
    untracked_files = []        # fichiers non suivis
    
    for filepath, working_hash in working_files.items():
        if filepath in indexed_files:
            if indexed_files[filepath]['hash'] != working_hash:
                modified_not_staged.append(filepath)
            if filepath not in committed_files:
                staged_for_commit.append(filepath)
        else:
            untracked_files.append(filepath)
    
    for filepath in indexed_files:
        if filepath not in working_files:
            modified_not_staged.append(f"{filepath} (deleted)")
    
    if not staged_for_commit and not modified_not_staged and not untracked_files:
        print("nothing to commit, working tree clean")
        return
    
    print()
    if staged_for_commit:
        print("Changes to be committed:")
        print('  (use "git rm --cached <file>..." to unstage)')
        print()
        for file in sorted(staged_for_commit):
            print(f"        new file:   {file}")
        print()
    
    if modified_not_staged:
        print("Changes not staged for commit:")
        print('  (use "git add <file>..." to update what will be committed)')
        print('  (use "git checkout -- <file>..." to discard changes in working directory)')
        print()
        for file in sorted(modified_not_staged):
            if "(deleted)" in file:
                print(f"        deleted:    {file.replace(' (deleted)', '')}")
            else:
                print(f"        modified:   {file}")
        print()
    
    if untracked_files:
        print("Untracked files:")
        print('  (use "git add <file>..." to include in what will be committed)')
        print()
        for file in sorted(untracked_files):
            print(f"        {file}")
        print()
