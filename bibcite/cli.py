import argparse
import pyperclip
from tabulate import tabulate
from bibcite.work import Work

def main():
    parser = argparse.ArgumentParser(description='Generate BibTeX citations from a title.')
    parser.add_argument('--title', type=str, help='The title of the work to generate a BibTeX citation for')
    parser.add_argument('--author', type=str, help='The author of the work', default=None)
    args = parser.parse_args()

    text = "Bibcite: Bibtex citations from the command line\n"
    table = [[text]]
    print(tabulate(table, tablefmt="grid"))

    title, author = args.title, args.author
    try:
        print(f'- Searching for title \"{title}\"')
        work = Work.from_query(title=title, author=author)
    except Exception as e:
        print(f'- An error occurred while trying to find work with title \"{title}\": {repr(e)}')
        return

    bibtex = work.to_bibtex()
    print(f'- Found BibTeX citation: \n{bibtex}')
    pyperclip.copy(bibtex)
    print(f'- Copied to clipboard!')

if __name__ == "__main__":
    main()
