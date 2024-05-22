from quickcite import Work
import pyperclip
from tabulate import tabulate

text = "Quickcite V1.0\n\nGenerate bibtex citations from only title"
table = [[text]]

print(tabulate(table, tablefmt="grid"))
while True:
    user_input = input(f'\n-> Enter the title of your work or press \"q\" to quit:\n')
    if user_input == 'q':
        break
    title = user_input
    try:
        print(f'- Searching for title \"{title}\"')
        work = Work.from_query(title=title)
    except Exception as e:
        print(f'- An error occured while trying to find work with title \"{title}\": {repr(e)}')
        continue

    bibtex = work.to_bibtex()
    print(f'- Found bibtext citation: \n {bibtex}')
    pyperclip.copy(bibtex)
    print(f'- Copied to clipboard!')


