import os

def read_tree(tree_sha):
    """
    Lit un objet tree (format texte simplifié) et retourne une liste de tuples : (mode, type, sha, nom)
    """
    tree_path = os.path.join(".git", "objects", tree_sha)
    entries = []
    with open(tree_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 4:
                mode, type_, sha = parts[:3]
                name = " ".join(parts[3:])
                entries.append((mode, type_, sha, name))
    return entries
