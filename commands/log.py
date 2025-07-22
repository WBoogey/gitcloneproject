import os
import zlib

def get_commit(oid):
    """Récupère et parse un objet commit"""
    try:
        path = os.path.join(".gitC", "objects", oid[:2], oid[2:])
        if not os.path.exists(path):
            print(f"Error: commit object {oid} not found")
            return None
            
        with open(path, "rb") as f:
            compressed = f.read()
        full_data = zlib.decompress(compressed)

        # Séparer l'en-tête du contenu
        header, content = full_data.split(b'\x00', 1)
        
        # Vérifier que c'est bien un commit
        if not header.startswith(b'commit '):
            print(f"Error: {oid} is not a commit object")
            return None
            
        lines = content.decode().splitlines()

        commit = {}
        i = 0
        # Parser les métadonnées du commit
        while i < len(lines) and lines[i]:
            line = lines[i]
            if line.startswith("tree "):
                commit["tree"] = line[5:]
            elif line.startswith("parent "):
                commit["parent"] = line[7:]
            elif line.startswith("author "):
                commit["author"] = line[7:]
            elif line.startswith("committer "):
                commit["committer"] = line[10:]
            i += 1

        # Le message commence après la ligne vide
        if i < len(lines):
            commit["message"] = "\n".join(lines[i+1:]).strip()
        else:
            commit["message"] = ""
            
        return commit
        
    except Exception as e:
        print(f"Error reading commit {oid}: {e}")
        return None

def get_head_oid():
    """Récupère l'OID du commit HEAD"""
    try:
        head_path = os.path.join(".gitC", "HEAD")
        if not os.path.exists(head_path):
            print("Error: No HEAD found. Repository not initialized or no commits yet.")
            return None
            
        with open(head_path, "r") as f:
            ref_line = f.read().strip()
            
        if ref_line.startswith("ref: "):
            # HEAD pointe vers une référence
            ref_path = os.path.join(".gitC", ref_line[5:])
            if os.path.exists(ref_path):
                with open(ref_path, "r") as f:
                    return f.read().strip()
            else:
                print(f"Error: Reference {ref_line[5:]} not found. No commits yet?")
                return None
        else:
            # HEAD contient directement un SHA
            return ref_line
            
    except Exception as e:
        print(f"Error reading HEAD: {e}")
        return None

def git_log():
    """Affiche l'historique des commits"""
    if not os.path.exists(".gitC"):
        print("Error: Not a git repository (no .gitC directory found)")
        return
        
    oid = get_head_oid()
    if not oid:
        print("No commits found.")
        return
        
    while oid:
        commit = get_commit(oid)
        if not commit:
            break
            
        print(f"commit {oid}")
        if "author" in commit:
            print(f"Author: {commit['author']}")
        if "committer" in commit:
            print(f"Date: {commit['committer']}")
        print()
        print(f"    {commit['message']}")
        print()
        
        # Passer au commit parent
        oid = commit.get("parent")