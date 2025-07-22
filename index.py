import os
import struct
from sys import path

GIT_DIR = ".git"
INDEX_PATH = os.path.join(GIT_DIR, "index")

def read_index():
    if not os.path.exists(INDEX_PATH):
        return {}

    entries = {}
    with open(INDEX_PATH, "r") as f:
        for line in f:
            path = line.strip()
            if path:
                entries[path] = None
    return entries
   