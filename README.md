# 🧪 Mini Git – Implémentation Simplifiée de Git en Python

Ce projet est une reconstitution simplifiée de Git, codée en Python. Il a été développé à des fins pédagogiques afin de mieux comprendre le fonctionnement interne de Git (index, objets, arbres, commits…).

---

## 🛠️ Prérequis

* Python 3.11 ou supérieur
* Système Unix (Linux/macOS recommandé)

---

## 🚀 Installation & Initialisation

```bash
python main.py init
```

Cette commande crée la structure `.git/` dans votre dossier de travail, avec tous les sous-dossiers nécessaires (`objects/`, `refs/`, `HEAD`, etc.).

---

## 📂 Commandes Disponibles

### 📦 `init`

Initialise un dépôt Git vide dans le dossier courant.

```bash
python main.py init
```

---

### ➕ `add`

Ajoute un fichier à l’index (zone de staging).

```bash
python main.py add <nom_fichier>
```

---

### 🧱 `commit`

Crée un commit à partir des fichiers présents dans l’index.

```bash
python main.py commit -m "Message du commit"
```

---

### 🌳 `write-tree`

Construit un objet arbre à partir de l’index.

```bash
python main.py write-tree
```

---

### 📜 `log`

Affiche l’historique des commits.

```bash
python main.py log
```

---

### 📄 `ls-files`

Affiche tous les fichiers présents dans l’index.

```bash
python main.py ls-files
```

⚠️ **Attention** : si vous obtenez une erreur de type `index file corrupt`, il faut :

1. Supprimer le fichier `index` :

   ```bash
   rm .git/index
   ```
2. Re-stager les fichiers :

   ```bash
   python main.py add <fichier>
   ```

---

### 🌲 `ls-tree`

Affiche le contenu d’un objet `tree`.

```bash
python main.py ls-tree <sha_du_tree>
```

Pour tester, vous pouvez d’abord écrire un arbre avec :

```bash
python main.py write-tree
```

Puis utiliser le hash retourné :

```bash
python main.py ls-tree <sha>
```

---

### 🔎 `cat-file`

Permet d’inspecter un objet Git (blob, tree, commit).

```bash
python main.py cat-file -p <sha>
```

---

### 🧪 `hash-object`

Calcule le hash SHA-1 d’un fichier, le stocke comme objet blob.

```bash
python main.py hash-object -w <nom_fichier>
```

---
## 🧼 Nettoyage en cas de bug

Si vous rencontrez des erreurs avec l’index :

```bash
rm .git/index
python main.py add <fichiers>
```

---

Tu veux que je le mette aussi dans un fichier `README.md` prêt à push ?


Bon comme j'arrivais pas à merge, si vous cherchez les commandes LS c'est sur la branche Ousmane

✍️ Auteurs:
Ehoura Christ-Yvann

Ousmane Sacko

Daniel Komoe

Kilian Izatoola

Lien du Trello: https://trello.com/invite/b/687e08fcf44c53c69e140d66/ATTI66b547653940f5429054368f8df8707a196E77E2/📌-a-faire
