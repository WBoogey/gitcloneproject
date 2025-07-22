import sys
from commands import init, hash_object, cat_file, add, write_tree, commit_tree, commit, log, rm, status, ls_files, ls_tree

def main():
    print("[DEBUG] Entrée dans main()")

    if len(sys.argv) < 2:
        print("Usage: python git.py <command>")
        return

    if sys.argv[1] == "ls-files":
        ls_files.run(sys.argv[2:])
        return
    if sys.argv[1] == "ls-tree":
        ls_tree.run(sys.argv[2:])
        return

    command = sys.argv[1]

    if command == "init":
        init.git_init()

    elif command == "hash-object":
        if len(sys.argv) < 3:
            print("Usage: python git.py hash-object <file>")
            return
        path = sys.argv[2]
        hash_object.hash_object(path)

    elif command == "cat-file":
        if len(sys.argv) < 4 or sys.argv[2] != "-p":
            print("Usage: python git.py cat-file -p <sha>")
            return
        oid = sys.argv[3]
        cat_file.cat_file(oid)

    elif command == "add":
        if len(sys.argv) < 3:
            print("Usage: python git.py add <file>")
            return
        path = sys.argv[2]
        add.git_add(path)

    elif command == "write-tree":
        write_tree.write_tree()

    elif command == "commit-tree":
        if "-m" not in sys.argv:
            print("Usage: python git.py commit-tree <tree_sha> -m \"msg\" [-p <parent_sha>]")
            return
        tree_oid = sys.argv[2]
        msg_index = sys.argv.index("-m")
        message = sys.argv[msg_index + 1]

        parent = None
        if "-p" in sys.argv:
            p_index = sys.argv.index("-p")
            parent = sys.argv[p_index + 1]

        commit_tree.commit_tree(tree_oid, message, parent)

    elif command == "commit":
        if "-m" not in sys.argv:
            print("Usage: python git.py commit -m \"message\"")
            return
        msg_index = sys.argv.index("-m")
        message = sys.argv[msg_index + 1]
        commit.git_commit(message)

    elif command == "log":
        log.git_log()

    elif command == "rm":
        if len(sys.argv) < 3:
            print("Usage: python git.py rm [--cached] <file>")
            return
        
        if "--cached" in sys.argv:
            if len(sys.argv) < 4:
                print("Usage: python git.py rm --cached <file>")
                return
            path = sys.argv[3]
            rm.git_rm_cached(path)
        else:
            path = sys.argv[2]
            rm.git_rm(path)

    elif command == "status":
        status.git_status()

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()