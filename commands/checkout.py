import os
from utils import (
    read_object, update_HEAD, get_commit_tree_oid,
    read_tree, get_oid, read_tree_into_index
)

def git_checkout(target, new_branch=False):
    if not os.path.exists(".gitC"):
        print("Error: Not a git repository")
        return

    if new_branch:
        # Création d'une nouvelle branche à partir de HEAD
        oid = get_oid("HEAD")
        ref_path = os.path.join(".gitC", "refs", "heads", target)

        if os.path.exists(ref_path):
            print(f"fatal: A branch named '{target}' already exists.")
            return

        with open(ref_path, "w") as f:
            f.write(oid + "\n")

        update_HEAD(f"refs/heads/{target}")

        # Checkout commit pointé par HEAD pour update WD et index
        tree_oid = get_commit_tree_oid(oid)
        read_tree(tree_oid)
        read_tree_into_index(tree_oid)

        print(f"Switched to a new branch '{target}'")

    else:
        # Checkout simple (branch ou commit SHA)
        oid = get_oid(target)
        tree_oid = get_commit_tree_oid(oid)

        read_tree(tree_oid)
        read_tree_into_index(tree_oid)

        ref_path = os.path.join(".gitC", "refs", "heads", target)
        if os.path.exists(ref_path):
            update_HEAD(f"refs/heads/{target}")
        else:
            update_HEAD(oid)  # HEAD détaché sur commit

        print(f"Checked out {target}")
