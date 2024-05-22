from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

import requests
from requests import Response

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
        response = cls._search_request(search_expression=title)
        paper_dicts = response.json()['results']
        relevant_papers = [p for p in paper_dicts if not p['doi'] is None]
        # print(f'Number of relevant papers = {len(relevant_papers)}')
        if work_type:
            relevant_papers = [p for p in relevant_papers if p['type'] == work_type]
        if author:
            relevant_papers = [p for p in relevant_papers if author in cls.get_author(p)]
        # print(f'relevant papers = {relevant_papers}')

        paper_doi = relevant_papers[0]['doi']
        crossref_item = cls.get_crossref_item(paper_doi=paper_doi)
        journal_item = crossref_item.get('container-title')
        if journal_item:
            journal = journal_item[0]
        else:
            journal = None

        new_work = Work(title= crossref_item['title'][0],
                        authors= crossref_item['author'],
                        year=crossref_item['published']['date-parts'][0][0],
                        doi= crossref_item['DOI'],
                        url= crossref_item['URL'],
                        work_type= crossref_item['type'],
                        journal=journal,
                        pages= crossref_item.get('page'),
                        volume= crossref_item.get('volume'))
        return new_work

    @staticmethod
    def get_author(paper_dict : dict):
        try:
            author_name = paper_dict['authorships'][0]['raw_author_name']
        except:
            author_name = ''
        return author_name

    @staticmethod
    def get_crossref_item(paper_doi : str) -> dict:
        url = f"https://api.crossref.org/works/{paper_doi}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"Request failed with status code {response.status_code}")
        data = response.json()
        return data['message']

    @staticmethod
    def _search_request(search_expression : str) -> Response:
        works_url = 'https://api.openalex.org/works'
        results_per_page = 200

        search_params = {
            'filter': f'default.search:{search_expression}',
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
        else:
            raise ValueError(f"Unsupported entry type: {self.work_type}")

        authors = " and ".join([f"{author['given']} {author['family']}" for author in self.authors])
        first_author_lastname = self.authors[0]['family']

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
    test_title = "Neural networks trained on synthetically generated crystals can extract structural information from ICSD powder X-ray diffractograms"
    introd_work = Work.from_query(title=test_title)
    print(f'Intro work bibtext = \n{introd_work.to_bibtex()}')
    # print(Work.get_crossref_item(paper_doi='10.1063/1.2807734'))


