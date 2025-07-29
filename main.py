import sys
from gitlite.commands import init, add, commit, status

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <command> [args...]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init.run(sys.argv[2:])
    elif command == "add":
        add.run(sys.argv[2:])
    elif command == "commit":
        commit.run(sys.argv[2:])
    elif command == "status":
        status.run(sys.argv[2:])
    else:
        print(f"Commande inconnue: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
