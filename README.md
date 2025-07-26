Git from Scratch – Student Project
This project involves reimplementing core Git functionality in Python. It will help you understand Git's internal architecture and make you comfortable with both its plumbing and porcelain commands.

🎯 Project Scope
You will implement a subset of Git commands, both low-level (plumbing) and user-facing (porcelain). Your goal is to ensure they behave similarly to real Git, within clearly defined constraints.

🛠 Plumbing Commands
git hash-object [-w] <file>
Creates a blob object from file content and writes its SHA-1 to stdout.
❌ Reject directories or missing files.
git cat-file -t|-p <oid>
-t: Print object type.
-p: Pretty-print blob/tree/commit content.
❌ Reject invalid OIDs or missing options.
git write-tree
Create a tree object from the staging area.
Writes SHA-1 of the tree to stdout.
git commit-tree <tree_sha> -m "msg" [-p <parent>]
Creates a commit object pointing to a tree (and parent commit if any) and writes its oid to stdout
Requires -m message.
❌ No annotated tags.
🧑‍💻 Porcelain Commands
git init [<dir>]
Initializes a Git repository in the given directory.
Create .git/objects, .git/refs/heads, HEAD, and minimal config
git add <file>…
Adds files to the staging area (not directories).
❌ No -p, no wildcards.
git rm <file>…
Removes a file from working directory and index.
git commit -m "msg"
Runs write-tree, creates a commit with HEAD as parent.
❌ No editor or message prompt.
git status
Shows staged and unstaged changes.
git checkout [-b] <branch|sha>
Switch to existing commit or branch.
-b <branch> creates a new branch.
Change HEAD, update working dir, check for conflicts
git reset [--soft|--mixed|--hard] <sha>
--soft: move HEAD
--mixed: + reset index
--hard: + reset working directory
❌ No file-specific reset.
git log
Print commit history from HEAD (one-line summary ok).
git ls-files
List all files in the index.
git ls-tree <tree_sha>
List contents of a tree object.
git rev-parse <ref>
Convert ref/branch/HEAD into SHA-1.
❌ No complex selectors
git show-ref
List all refs and their hashes.
🧠 Advanced Feature: Merge Support
git merge <branch|sha>
Perform 3-way merge and create a merge commit with 2 parents.
On conflict: insert <<<<<<<, =======, >>>>>>> markers into file(s).
❌ No rebase, squash, or fast-forward-only merges.
📄 Gitignore
Handle .gitignore
Use simple glob-style matching (e.g., *.log, build/)
❌ No negation or nested .gitignore files.
🏗 Index Implementation
You are free to implement the index your way.
✅ Bonus if it matches Git’s format closely.
❌ Out of Scop
git push and git update-index are NOT required.
No support for remotes, rebase, tags, or stashing.
✅ Deliverables
A working implementation of the listed commands.
Tests and example usage for each.
Clean error handling for all unsupported cases.
⏱ Time Estimate
Total time: 6–9 days
Use AI if needed, but understand what you're coding.







# Mini Git – Commandes `ls-files` et `ls-tree`

Ce projet est une implémentation simplifiée de Git en Python.

## 📂 Commande `ls-files`

La commande `ls-files` affiche les fichiers actuellement présents dans l’index (aussi appelé *staging area*), c’est-à-dire les fichiers suivis par Git à ce moment.

### ➤ Utilisation

`
python3 main.py ls-files
Elle retourne la liste des fichiers indexés.

## 🌳 Commande ls-tree

La commande ls-tree <tree_sha> permet d’afficher le contenu d’un objet tree (répertoire) à partir de son SHA-1. Cela correspond à ce que fait git ls-tree dans un vrai dépôt Git.
```bash
➤ Utilisation
python3 main.py ls-tree <sha_du_tree>
🔍 Astuce : tu peux obtenir le SHA d’un tree avec la commande write-tree.
❌ Problème : Fichier index manquant ou corrompu

Si vous avez une erreur liée à un index manquant ou cassé, vous pouvez simplement le régénérer.

✅ Solution : Supprimer et régénérer l’index
Supprimez le fichier .git/index :
rm .git/index
Ajoutez de nouveau tous les fichiers pour recréer l’index :
python3 main.py add .
Cela va automatiquement recréer un nouvel index avec tous les fichiers actuels du projet.
🛠 Dépendances

Python 3.11+
Aucune librairie externe requise
Bon comme j'arrivais pas à merge, si vous cherchez les commandes LS c'est sur la branche Ousmane

✍️ Auteurs
Ehoura Christ-Yvann
Ousmane Sacko
Daniel Komoe
Kilian Izatoola
Lien du Trello:https://trello.com/invite/b/687e08fcf44c53c69e140d66/ATTI66b547653940f5429054368f8df8707a196E77E2/📌-a-faire
