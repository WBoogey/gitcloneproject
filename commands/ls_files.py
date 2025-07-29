from index import read_index

def run(args):
    # args doit être vide pour ls-files
    entries = read_index()
    for path in sorted(entries):
        print(path)
