import os
import glob
from typing import Union, Type

import pandas as pd

from .paper import Paper


class Organizer():

    def __init__(self, collection_loc: str) -> None:
        self.paper_no = 0
        self.paper_dict = {}

        if os.path.exists(collection_loc):
            self.collection_loc = collection_loc
            self.papers_loc = collection_loc + '\\papers\\'
            self.notes_loc = collection_loc + '\\notes\\'
            self.papers_data_loc = collection_loc + '\\data\\'
        else:
            raise ValueError('This path does not exist for CollectionOfPapers to set up.')
        
        if not os.path.exists(self.papers_loc):
            os.makedirs(self.papers_loc)
        if not os.path.exists(self.notes_loc):
            os.makedirs(self.notes_loc)
        if not os.path.exists(self.papers_data_loc):
            os.makedirs(self.papers_data_loc)

    def add_paper(self, pdf_name: str) -> None:
        if not pdf_name.endswith('.pdf'):
            pdf_name += '.pdf'
        if os.path.exists(self.papers_loc + pdf_name):
            self.paper_no += 1
            os.rename(self.papers_loc + pdf_name, self.papers_loc + f'{self.paper_no}.pdf')
            self.paper_dict[self.paper_no] = Paper(self.papers_loc + f'{self.paper_no}.pdf', 
                                                   self.papers_data_loc + f'{self.paper_no}.csv',
                                                   self.notes_loc + f'{self.paper_no}.txt')
            print(f'Added pdf with name {pdf_name} into the CollectionOfPapers dataset. Paper ID {self.paper_no}')
        else:
            raise ValueError(f'This pdf does not exist under the path {self.papers_loc}.')
        
    def auto_add_papers(self, summary: bool = False) -> None:
        pdf_names = [os.path.basename(file_path) for file_path in glob.glob(os.path.join(self.papers_loc, '*'))]

        while (str(self.paper_no + 1) + '.pdf') in pdf_names:
            pdf_names.remove(str(self.paper_no + 1) + '.pdf')
            self.paper_no += 1
            if not f'{self.paper_no}' in self.paper_dict:
                self.paper_dict[self.paper_no] = Paper(self.papers_loc + f'{self.paper_no}.pdf', 
                                                    self.papers_data_loc + f'{self.paper_no}.csv',
                                                    self.notes_loc + f'{self.paper_no}.txt')
                if summary:
                    print(f'Added pdf with name {self.paper_no + 1}.pdf into the CollectionOfPapers dataset.')
            
        for pdf_name in pdf_names:
            if pdf_name.endswith('.pdf'):
                self.paper_no += 1
                os.rename(self.papers_loc + pdf_name, self.papers_loc + f'{self.paper_no}.pdf')
                self.paper_dict[self.paper_no] = Paper(self.papers_loc + f'{self.paper_no}.pdf', 
                                                        self.papers_data_loc + f'{self.paper_no}.csv',
                                                        self.notes_loc + f'{self.paper_no}.txt')
                if summary:
                    print(f'Added pdf with name {pdf_name} into the CollectionOfPapers dataset.')

    def add_category(self, indices: Union[list[int], int], cat: str):
        if isinstance(indices, int):
            paper = self.paper_dict[indices]
            paper.set_category(cat)
        else:
            for index in indices:
                paper = self.paper_dict[index]
                paper.set_category(cat)

    def add_relation(self, relations: list[list[int, Union(int, list[int]), bool, str, str]]):
        for paper1_id, paper2_ids, mutual, relation_type, note in relations:
            paper1: Type[Paper] = self.paper_dict[paper1_id]
            if isinstance(paper2_ids) == list:
                for paper2_id in paper2_ids:
                    paper2: Type[Paper] = self.paper_dict[paper2_id]
                    paper1.add_relation(paper2_id, relation_type, note)
                    if mutual:
                        paper2.add_relation(paper1_id, relation_type, note)
                    else:
                        paper2.add_relation(paper1_id, 'BE ' + relation_type, note)
            else:
                paper2_id = paper2_ids
                paper2: Type[Paper] = self.paper_dict[paper2_id]
                paper1.add_relation(paper2_id, relation_type, note)
                if mutual:
                    paper2.add_relation(paper1_id, relation_type, note)
                else:
                    paper2.add_relation(paper1_id, 'BE ' + relation_type, note)

    def add_keyword(self, indices: Union[list[int], int], keyword: str):
        if isinstance(indices, int):
            paper = self.paper_dict[indices]
            paper.add_keyword(keyword)
        else:
            for index in indices:
                paper = self.paper_dict[index]
                paper.add_keyword(keyword)

    def data_save(self):
        for paper in self.paper_dict.values():
            paper.data_save()

    def data_update(self):
        for paper in self.paper_dict.values():
            paper.data_update()

    def __str__(self, full: bool = False) -> str:
        info = ''
        for i in range(1, self.paper_no + 1):
            if full:
                info += f'{i}: \n{self.paper_dict[i].__str__()}'
            else:
                info += f'{i}: Paper Title: {self.paper_dict[i].name}\n'
            if not 'bibtex' in self.paper_dict[i].active_attr_list:
                info += f'Warning: This paper does not have a bibtex.\n'
        return info