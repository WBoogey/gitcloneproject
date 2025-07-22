import os
from commands import write_tree, commit_tree

def get_head_ref():
    with open(".gitC/HEAD", "r") as f:
        ref_line = f.read().strip()
    if ref_line.startswith("ref: "):
        return ref_line[5:] 
    return None

def get_head_oid():
    ref = get_head_ref()
    ref_path = os.path.join(".gitC", ref)
    if os.path.exists(ref_path):
        with open(ref_path, "r") as f:
            return f.read().strip()
    return None

def update_ref(ref, oid):
    ref_path = os.path.join(".gitC", ref)
    with open(ref_path, "w") as f:
        f.write(oid + "\n")

def git_commit(message):
    # 1. write-tree
    tree_oid = write_tree.write_tree(return_oid=True)

    # 2. récupérer le commit parent (si HEAD pointe vers quelque chose)
    parent_oid = get_head_oid()

    # 3. commit-tree
    commit_oid = commit_tree.commit_tree(tree_oid, message, parent=parent_oid)

    # 4. mettre à jour la branche courante
    ref = get_head_ref()
    if ref:
        update_ref(ref, commit_oid)
        print(f"[commit {commit_oid}] {message}")
    else:
        print("HEAD is detached. Commit created but not referenced.")
