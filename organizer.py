import os
import glob
from typing import Union, Type

import pandas as pd

from .paper import Paper


class Organizer():

    def __init__(self, collection_loc: str) -> None:
        self.paper_no: int = 0
        self.paper_dict: dict[int, Paper] = {}

        if os.path.exists(collection_loc):
            self.collection_loc: str = collection_loc
            self.papers_loc: str = collection_loc + '\\papers\\'
            self.notes_loc: str = collection_loc + '\\notes\\'
            self.papers_data_loc: str = collection_loc + '\\data\\'
        else:
            raise ValueError('This path does not exist for CollectionOfPapers to set up.')
        
        if not os.path.exists(self.papers_loc):
            os.makedirs(self.papers_loc)
        if not os.path.exists(self.notes_loc):
            os.makedirs(self.notes_loc)
        if not os.path.exists(self.papers_data_loc):
            os.makedirs(self.papers_data_loc)

    def add_paper(self, pdf_name: str, registered: bool, summary: bool = True) -> None:
        if not pdf_name.endswith('.pdf'):
            pdf_name += '.pdf'
        if os.path.exists(self.papers_loc + pdf_name):
            self.paper_no += 1
            if registered:
                paper_no = int(pdf_name[:-15])
                self.paper_dict[paper_no] = Paper(self.collection_loc, paper_no)
            else:
                os.rename(self.papers_loc + pdf_name, self.papers_loc + f'{self.paper_no}_registered.pdf')
                self.paper_dict[self.paper_no] = Paper(self.collection_loc, self.paper_no)
                paper_no = self.paper_no
            if summary:
                print(f'Added pdf with name {pdf_name} into the CollectionOfPapers dataset. Paper ID: {paper_no}')
        else:
            raise ValueError(f'This pdf does not exist under the path {self.papers_loc}.')
        
    def auto_add_papers(self, summary: bool = True) -> None:
        # get all pdf names under the path (remove .pdf suffix)
        pdf_names = [os.path.basename(file_path) for file_path in glob.glob(os.path.join(self.papers_loc, '*'))]
        pdf_names = [name[:-4] if name.endswith('.pdf') else name for name in pdf_names]

        registered_pdf_names = [name for name in pdf_names if name.endswith('_registered')]
        active_pdf_names = {str(name) for name in set(self.paper_dict.keys())}
        inactive_pdf_names = set(registered_pdf_names) - active_pdf_names
        unregistered_pdf_names = set(pdf_names) - set(registered_pdf_names)

        for pdf_name in inactive_pdf_names:
            self.add_paper(pdf_name, True, summary=summary)
            
        for pdf_name in unregistered_pdf_names:
            self.add_paper(pdf_name, False, summary=summary)

    def add_category(self, indices: list[int] | int, category: str):
        if isinstance(indices, int):
            paper: Paper = self.paper_dict[indices]
            paper.set_category(category)
        else:
            for index in indices:
                paper: Paper = self.paper_dict[index]
                paper.set_category(category)

    def add_relation(self, relations: list[list[int | list[int] | bool | str]]):
        for paper1_id, paper2_ids, mutual, relation_type, note in relations:

            if not isinstance(paper1_id, int):
                raise ValueError(f'{paper1_id} is not of int type')
            if not (isinstance(paper2_ids, int) or (isinstance(paper2_ids, list) and all(isinstance(item, int) for item in paper2_ids))):
                raise ValueError(f'{paper2_ids} is not of int or list[int] type')
            if not isinstance(mutual, bool):
                raise ValueError(f'{mutual} is not of bool type')
            if not isinstance(relation_type, str):
                raise ValueError(f'{relation_type} is not of str type')
            if not isinstance(note, str):
                raise ValueError(f'{note} is not of str type')
            
            paper1: Paper = self.paper_dict[paper1_id]
            if isinstance(paper2_ids, list):
                for paper2_id in paper2_ids:
                    paper2: Paper = self.paper_dict[paper2_id]
                    paper1.add_relation(paper2_id, relation_type, note)
                    if mutual:
                        paper2.add_relation(paper1_id, relation_type, note)
                    else:
                        paper2.add_relation(paper1_id, 'BE ' + relation_type, note)
            else:
                paper2_id = paper2_ids
                paper2: Paper = self.paper_dict[paper2_id]
                paper1.add_relation(paper2_id, relation_type, note)
                if mutual:
                    paper2.add_relation(paper1_id, relation_type, note)
                else:
                    paper2.add_relation(paper1_id, 'BE ' + relation_type, note)

    def add_keyword(self, indices: list[int] | int, keyword: str):
        if isinstance(indices, int):
            paper: Paper = self.paper_dict[indices]
            paper.add_keyword(keyword)
        else:
            for index in indices:
                paper: Paper = self.paper_dict[index]
                paper.add_keyword(keyword)

    def data_save(self):
        for paper in self.paper_dict.values():
            assert isinstance(paper, Paper)
            paper.data_save()

    def data_load(self):
        for paper in self.paper_dict.values():
            assert isinstance(paper, Paper)
            paper.data_load()

    def print_info(self):
        info = ''
        for i in range(1, self.paper_no + 1):
            info += f'{i}: \n{self.paper_dict[i].__str__()}'
            if not 'bibtex' in self.paper_dict[i].active_attrs:
                info += f'Warning: This paper does not have a bibtex.\n'
            info += '\n\n'
        print(info)

    def __str__(self) -> str:
        info = ''
        for i in range(1, self.paper_no + 1):
            info += f'{i}: Paper Title: {self.paper_dict[i].title}\n'
            if not 'bibtex' in self.paper_dict[i].active_attrs:
                info += f'Warning: This paper does not have a bibtex.\n'
        return info