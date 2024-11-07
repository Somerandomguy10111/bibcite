from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

import requests
from requests import Response
from fuzzywuzzy import fuzz

# ---------------------------------------------------------

@dataclass
class Work:
    title : str
    authors : list
    year : str
    doi : str
    url : str
    work_type : str
    journal : Optional[str] = None
    pages : Optional[str] = None
    volume : Optional[str] = None

    @classmethod
    def from_query(cls, title : str,
                   work_type : Optional[str] = None,
                   author : Optional[str] = None) -> Work:
        response = cls._search_request(title=title, author=author)
        paper_dicts = response.json()['results']

        if len(paper_dicts) == 0:
            raise ValueError(f"No papers found with title {title}")

        def paper_title_matches(p: dict) -> bool:
            # print(f'Title: {p["title"].lower()}, doi = {p["doi"]}')
            # print(f'Title len = {len(p["title"])}')

            try:
                match_score = fuzz.ratio(title.lower(), p['title'].lower())
                # print(f'Match score: {match_score}')
                return match_score > 95
            except Exception as e:
                return False

        relevant_papers = [p for p in paper_dicts if paper_title_matches(p)]
        relevant_papers = [p for p in relevant_papers if not p['doi'] is None]

        if len(relevant_papers) == 0:
            raise ValueError(f"No works or no works with doi found with title {title}")

        if work_type:
            relevant_papers = [p for p in relevant_papers if p['type'] == work_type]
        if len(relevant_papers) == 0:
            raise ValueError(f"No papers found with title {title} and author {author}")

        # print(f'Crossref item = {cls.get_crossref_item(paper_doi)}')
        crossref_item = cls.get_crossref_item(paper_doi=relevant_papers[0]['doi'])
        journal_item = crossref_item.get('container-title')
        if journal_item:
            journal = journal_item[0]
        else:
            journal = None

        new_work = Work(title= crossref_item['title'][0],
                        authors= crossref_item['author'],
                        year=crossref_item['published']['date-parts'][0][0],
                        doi=crossref_item['DOI'],
                        url= crossref_item['URL'],
                        work_type= crossref_item['type'],
                        journal=journal,
                        pages= crossref_item.get('page'),
                        volume= crossref_item.get('volume'))
        return new_work


    @staticmethod
    def get_crossref_item(paper_doi : str) -> dict:
        url = f"https://api.crossref.org/works/{paper_doi}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Request failed with status code {response.status_code}")
        data = response.json()
        return data['message']

    @staticmethod
    def _search_request(title: str, author: str = None) -> Response:
        author_url = 'https://api.openalex.org/authors'
        conditional_author_filter = ''
        if author:
            author_search_params = {
                'filter': f'display_name.search:{author}',
                'per_page': 1
            }
            author_response = requests.get(author_url, params=author_search_params)
            author_data = author_response.json()
            # print(f'Author data results = {author_data["results"]}')
            author_openalex_url = author_data['results'][0]['id']
            author_id = author_openalex_url.split('/')[-1]
            # print(f'Author id = {author_id}')
            conditional_author_filter = f',authorships.author.id:{author_id}'

        works_url = 'https://api.openalex.org/works'
        results_per_page = 200

        title_filter = f'default.search:{title}'

        search_params = {
            'filter': f'{title_filter}{conditional_author_filter}',
            'sort': 'relevance_score:desc',
            'per_page': results_per_page,
        }

        response = requests.get(works_url, params=search_params)
        return response

    # ---------------------------------------------------------

    def to_bibtex(self) -> str:
        if self.work_type == 'journal-article':
            bibtex_type = 'article'
        elif self.work_type == 'book':
            bibtex_type = 'book'
        elif self.work_type == 'proceedings-article':
            bibtex_type = 'inproceedings'
        elif self.work_type == 'monograph':
            bibtex_type = 'book'
        else:
            raise ValueError(f"Unsupported entry type: {self.work_type}")

        authors = " and ".join([f"{author['given']} {author['family']}" for author in self.authors])
        first_author_lastname = self.authors[0]['family']
        first_author_lastname = first_author_lastname.split()[-1]

        info_list = {
            'title': self.title,
            'author': authors,
            'journal': self.journal,
            'year': self.year,
            'volume': self.volume,
            'pages': self.pages,
            'doi': self.doi,
            'url': self.url
        }

        bibtex = f"@{bibtex_type}{{{first_author_lastname}{self.year},\n"
        for key, value in info_list.items():
            if value:
                bibtex += f"  {key}={{{value}}},\n"
        bibtex = bibtex.rstrip(',\n') + "\n}"

        return bibtex



if __name__ == "__main__":
    # Error titles: Titles for which currently no citation can be generated
    # -> t1: Missing author
    # -> t2: DOI not found in Crossref
    t1 = "Fundamentals of Powder Diffraction and Structural Characterization of Materials"
    t2 = "Attention is all you need"
    t3 = 'Supernova'
    t4, a4 = 'Elements of Modern X-ray Physics', 'J. Als-Nielsen'
    introd_work = Work.from_query(title=t4, author=a4)
    print(f'Paper doi is {introd_work.doi}')
    print(f'Intro work bibtext: \n{introd_work.to_bibtex()}')
    # print(Work.get_crossref_item(paper_doi='10.1063/1.2807734'))
