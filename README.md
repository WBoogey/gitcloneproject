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


✍️ Auteurs
Ousmane Sacko
