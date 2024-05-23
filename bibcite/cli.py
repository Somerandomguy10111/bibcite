import argparse
import pyperclip
from tabulate import tabulate
from work import Work

def main():
    parser = argparse.ArgumentParser(description='Generate BibTeX citations from a title.')
    parser.add_argument('title', type=str, help='The title of the work to generate a BibTeX citation for.')
    args = parser.parse_args()

    text = "Quickcite V0.5\nGenerate bibtex citations from only title"
    table = [[text]]
    print(tabulate(table, tablefmt="grid"))

    title = args.title
    try:
        print(f'- Searching for title \"{title}\"')
        work = Work.from_query(title=title)
    except Exception as e:
        print(f'- An error occurred while trying to find work with title \"{title}\": {repr(e)}')
        return

    bibtex = work.to_bibtex()
    print(f'- Found BibTeX citation: \n{bibtex}')
    pyperclip.copy(bibtex)
    print(f'- Copied to clipboard!')

if __name__ == "__main__":
    main()
