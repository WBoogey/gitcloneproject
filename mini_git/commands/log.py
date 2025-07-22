import os
import zlib

def get_commit(oid):
    path = os.path.join(".git", "objects", oid[:2], oid[2:])
    with open(path, "rb") as f:
        compressed = f.read()
    full_data = zlib.decompress(compressed)

    _, content = full_data.split(b'\x00', 1)
    lines = content.decode().splitlines()

    commit = {}
    i = 0
    while i < len(lines) and lines[i]:
        line = lines[i]
        if line.startswith("tree "):
            commit["tree"] = line[5:]
        elif line.startswith("parent "):
            commit["parent"] = line[7:]
        i += 1

    # Le reste, c'est le message
    commit["message"] = "\n".join(lines[i+1:])
    return commit

def get_head_oid():
    with open(".git/HEAD", "r") as f:
        ref_line = f.read().strip()
    if ref_line.startswith("ref: "):
        ref_path = os.path.join(".git", ref_line[5:])
        if os.path.exists(ref_path):
            with open(ref_path, "r") as f:
                return f.read().strip()
    return None

def git_log():
    oid = get_head_oid()
    while oid:
        print(f"commit {oid}")
        commit = get_commit(oid)
        print(f"    {commit['message']}\n")
        oid = commit.get("parent")
