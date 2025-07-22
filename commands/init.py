import os

def git_init():
    git_dir = ".gitC"
    if os.path.exists(git_dir):
        print("Repository already initialized.")
        return

    # Crée les sous-dossiers Git
    os.makedirs(os.path.join(git_dir, "objects"))
    os.makedirs(os.path.join(git_dir, "refs", "heads"))

    # Crée le fichier HEAD
    with open(os.path.join(git_dir, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    print("Initialized empty Git repository in .gitC/")
