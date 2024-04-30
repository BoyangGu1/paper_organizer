import os
import re
from typing import Optional

import pandas as pd

from .CONSTANT import *


class Paper():

    def __init__(self, 
                 loc: str,
                 paper_id: str | int,
                 bibtex: Optional[str] = None) -> None:
        
        # link paper pdf
        self.paper_loc: str = loc + 'papers' + str(paper_id) + '.pdf'
        if not os.path.exists(self.paper_loc):
            raise ValueError(f'{paper_id}.pdf is not in the {loc} folder.')

        # link csv to Paper object data storage
        self.datasave_loc: str = loc + 'data' + str(paper_id) + '.csv'
        if not os.path.exists(self.datasave_loc):
            df = pd.DataFrame([], columns=['attribute name', 'attribute data'])
            df.to_csv(self.datasave_loc, index=False)

        # link txt for notes
        self.notes_loc: str = loc + 'notes' + str(paper_id) + '.txt'
        if not os.path.exists(self.notes_loc):
            with open(self.notes_loc, 'w'):
                pass
        
        self.paper_id: str | int = paper_id
        self.bibtex: Optional[str] = None
        self.active_attrs: set[str] = set(['paper_id'])
        if bibtex is not None:
            self.set_bibtex(bibtex)
        self.category: Optional[str] = None
        self.keywords: list[str] = []
        self.relations: list[list[str]] = []
        self.update_notes()

    def set_bibtex(self, bibtex: str):
        if self.bibtex is not None:
            print(f'Warning, bibtex for paper {self.paper_id} has been overwrited. The while object has been re-initialized.')
        self.bibtex = bibtex
        self.active_attrs.add('bibtex')
        self.active_attrs = set(['paper_id', 'bibtex'])
        self._bibtex2attr()

    def _bibtex2attr(self):
        entry_pattern = re.compile(r'@(?P<entry_type>\w+)\s*{\s*(?P<key>[^,]+),\s*(?P<content>.+)\s*}\s*,?', re.DOTALL)
        field_pattern = re.compile(r'\s*(?!,\n)(?P<field>[^=]+)\s*=\s*{(?P<value>[^{}]+)}')

        assert self.bibtex is not None
        match = entry_pattern.findall(self.bibtex)[0]
        entry = {'entry_type': match[0], 'key': match[1]}
        fields = field_pattern.findall(match[2])
        for field, value in fields:
            entry[field.strip()] = value.strip()
        return entry
    
    def check_bibtex_exist(self):
        if self.bibtex is None:
            raise ValueError('You have not assigned a bibtex yet. Use .set_bibtex() to set the bibtex first.')

    def update_notes(self) -> None:
        with open(self.notes_loc, 'r') as file:
            notes = file.read()
        notes = notes.split("THIS IS A SPLIT LINE\n")
        self.notes = [note.rstrip('\n') for note in notes if (note.strip() != '') and (not note.startswith('RELATION '))]

    def set_category(self, cat: str) -> None:
        self.check_bibtex_exist()
        # paper category like survey
        safe_cat = ['survey']
        if cat in safe_cat:
            self.category = cat
            self.active_attrs.add('category')
        else:
            raise ValueError(f'{cat} is not a valid cateogry type. Please use category from {safe_cat}')

    def add_keyword(self, keyword: str) -> None:
        self.check_bibtex_exist()
        if not keyword in self.keywords:
            self.keywords.append(keyword)
        else:
            print(f'No Action: the keyword {keyword} has already been added to paper: {self.name}.')
        self.active_attrs.add('keywords')
    
    def add_relation(self, another_paper: str | int, relation: str, note: str) -> None:
        self.check_bibtex_exist()
        # relation should not include any underscore (_)
        self.relations.append([str(another_paper), relation, note])
        self.active_attrs.add('relations')
    
    def data_save(self) -> None:
        self.check_bibtex_exist()
        # replace local csv data with class data, the opposite of data_update
        df_data = []
        for attr in self.active_attrs:
            if attr == 'keywords':
                df_data.append(['keywords', ','.join(self.keywords)])
            elif attr == 'relations':
                for relation in self.relations:
                    df_data.append(['relations', '_'.join(relation)])
            else:
                df_data.append([attr, getattr(self, attr)])
        df = pd.DataFrame(df_data, columns=['attribute name', 'attribute data'])
        df.to_csv(self.datasave_loc, index=False)

        # also tidy up notes in text
        self.update_notes()
        with open(self.notes_loc, 'w') as file:
            # write in actual notes
            for note in self.notes:
                file.write(note + '\n')
                file.write("THIS IS A SPLIT LINE\n")
            # write in relations
            for relation, another_paper, note in self.relations:
                file.write(f'RELATION {relation} to {another_paper}: {note}\n')
                file.write("THIS IS A SPLIT LINE\n")
    
    def data_load(self) -> None:
        # replace class data with local csv data, the opposite of data_update
        safe_attr_list = ['name', 'bibtex', 'keywords', 'category']
        self.active_attrs = set()
        df = pd.read_csv(self.datasave_loc)
        for _, row in df.iterrows():
            attr = row['attribute name']
            info = row['attribute data']
            assert attr in safe_attr_list, f'{attr} is not a legal property for a paper'
            if attr == 'keywords':
                self.keywords = info.split(',')
            elif attr == 'relations':
                splits = info.split('_')
                self.relations.append([splits[0], splits[1], '_'.join(splits[2:])])
            else:
                setattr(self, attr, info)
            self.active_attrs.add(attr)

    def show_notes(self) -> None:
        self.update_notes()
        if self.notes == []:
            print('No notes for this paper')
        else:
            for i, note in enumerate(self.notes):
                print(f'{i+1}: {note}')
    
    def __str__(self) -> str:
        self.check_bibtex_exist()

        info = f"Paper Title: {self.paper_id}: {'[' + self.category + ']' if self.category else ''}{self.name}\n"

        if self.keywords != []:
            info += "Keywords: " + ', '.join(self.keywords) + '\n'

        self.update_notes()
        if self.notes != []:
            info += "Notes:\n" + "\n".join(self.notes)

        if self.relations != []:
            relations_info = ''
            for relation, another_paper, note in self.relations:
                relations_info += f'{relation} to {another_paper}: {note}\n'
            info += "Relations:\n" + relations_info

        return info