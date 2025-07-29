import os

# Liste de tous les fichiers à indexer
files = [
    "README.md",
    "git.py",
    "index.py",
    "utils.py",
    "commands/add.py",
    "commands/cat_file.py",
    "commands/commit.py",
    "commands/commit_tree.py",
    "commands/hash_object.py",
    "commands/init.py",
    "commands/log.py",
    "commands/ls_files.py",
    "commands/rm.py",
    "commands/status.py",
    "commands/write_tree.py",
    "objects/blob.py",
    "objects/commit.py",
    "objects/tree.py"
]

index_path = os.path.join(".git", "index")

with open(index_path, "w") as f:
    for file in files:
        f.write(file + "\n")

print(f"Index mis à jour avec {len(files)} fichiers.")
