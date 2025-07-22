from objects.tree import read_tree

def run(args):
    if len(args) != 1:
        print("Usage: git ls-tree <tree_sha>")
        return
    tree_sha = args[0]
    try:
        entries = read_tree(tree_sha)
    except Exception as e:
        print(f"Erreur lors de la lecture du tree {tree_sha}: {e}")
        return
    for mode, type_, sha, name in entries:
        print(f"{mode} {type_} {sha}\t{name}")
