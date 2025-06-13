import os

def run(args):
    # dossier cible = args[0] ou dossier courant
    target_dir = args[0] if args else os.getcwd()
    git_dir = os.path.join(target_dir, ".git")

    if os.path.exists(git_dir):
        print(f"Répertoire git déjà initialisé dans {git_dir}")
        return

    os.makedirs(os.path.join(git_dir, "objects"))
    os.makedirs(os.path.join(git_dir, "refs", "heads"))

    with open(os.path.join(git_dir, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(os.path.join(git_dir, "config"), "w") as f:
        f.write("[core]\n")
        f.write("    repositoryformatversion = 0\n")
        f.write("    filemode = false\n")
        f.write("    bare = false\n")
        f.write("    logallrefupdates = true\n")
        f.write("    ignorecase = true\n")
        f.write("    precomposeunicode = false\n")

    print(f"Initialisé vide Git repository dans {git_dir}")
    print(f"Configuration de base écrite dans {os.path.join(git_dir, 'config')}")
    print(f"Git repository initialisé dans {git_dir}")
    print("Vous pouvez maintenant utiliser les commandes gitlite comme 'gitlite add', 'gitlite commit', etc.")
    print("Pour plus d'informations, consultez la documentation de gitlite.")
    print("Bienvenue dans gitlite !")
    print("Pour commencer, utilisez 'gitlite add <fichier>' pour ajouter des fichiers à l'index.")      