import os

tree_sha = "demo_tree"
tree_content = [
    "100644 blob deadbeef fichier.txt",
    "040000 tree cafebabe dossier"
]

tree_dir = os.path.join(".git", "objects")
os.makedirs(tree_dir, exist_ok=True)

tree_path = os.path.join(tree_dir, tree_sha)
with open(tree_path, "w") as f:
    for line in tree_content:
        f.write(line + "\n")

print(f"Tree {tree_sha} créé avec {len(tree_content)} entrées.")
