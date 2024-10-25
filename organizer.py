import os
import glob

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

    def set_paper_bibtex(self, paper_id: int, bibtex: str):
        paper: Paper = self.paper_dict[paper_id]
        paper.set_bibtex(bibtex)

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
                raise TypeError(f'{paper1_id} is not of int type')
            if not (isinstance(paper2_ids, int) or (isinstance(paper2_ids, list) and all(isinstance(item, int) for item in paper2_ids))):
                raise TypeError(f'{paper2_ids} is not of int or list[int] type')
            if not isinstance(mutual, bool):
                raise TypeError(f'{mutual} is not of bool type')
            if not isinstance(relation_type, str):
                raise TypeError(f'{relation_type} is not of str type')
            if not isinstance(note, str):
                raise TypeError(f'{note} is not of str type')
            
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

    def add_keyword(self, indices: list[int] | int, keywords: list[str] | str):
        if isinstance(indices, int):
            paper: Paper = self.paper_dict[indices]
            if isinstance(keywords, list):
                for keyword in keywords:
                    paper.add_keyword(keyword)
            else:
                paper.add_keyword(keywords)
        else:
            for index in indices:
                paper: Paper = self.paper_dict[index]
                if isinstance(keywords, list):
                    for keyword in keywords:
                        paper.add_keyword(keyword)
                else:
                    paper.add_keyword(keywords)
    
    def del_keyword(self, indices: list[int] | int, keywords: list[str] | str):
        if isinstance(indices, int):
            paper: Paper = self.paper_dict[indices]
            if isinstance(keywords, list):
                for keyword in keywords:
                    paper.del_keyword(keyword)
            else:
                paper.del_keyword(keywords)
        else:
            for index in indices:
                paper: Paper = self.paper_dict[index]
                if isinstance(keywords, list):
                    for keyword in keywords:
                        paper.del_keyword(keyword)
                else:
                    paper.del_keyword(keywords)

    def search_keyword(self, keyword: str) -> list[int]:
        result_names = []
        info = f'keyword serach for: {keyword}\n'
        for name, paper in self.paper_dict.items():
            if keyword in paper.keywords:
                result_names.append(name)
                info += f'{name}: {paper.title}\n'
        print(info)
        return result_names
    
    def get_all_keyword(self) -> list[str]:
        keyword_list = []
        for name, paper in self.paper_dict.items():
            keyword_list.extend(paper.keywords)
        return list(set(keyword_list))
    
    def rewrite_keyword(self, old_name: str, new_name: str):
        info = f'rename keyword {old_name} to {new_name}\n'
        for name, paper in self.paper_dict.items():
            if old_name in paper.keywords:
                self.paper_dict[name].keywords = [keyword if keyword != old_name else new_name for keyword in self.paper_dict[name].keywords]
                info += f'{name}: {paper.title}\n'
        print(info)

    def data_save(self):
        for paper in self.paper_dict.values():
            assert isinstance(paper, Paper)
            paper.data_save()

    def data_load(self):
        for paper in self.paper_dict.values():
            assert isinstance(paper, Paper)
            paper.data_load()

    def get_citation_key(self, indices: int | list[int]) -> str:
        if isinstance(indices, int):
            return self.paper_dict[indices].key
        else:
            key_list = []
            for index in indices:
                key_list.append(self.paper_dict[index].key)
            return ', '.join(key_list)
        
    def get_name_from_citation_key(self, keys: str | list[str]) -> int | list[int]:
        if isinstance(keys, str):
            found_name = None
            for name, paper in self.paper_dict.items():
                if paper.key == keys:
                    found_name = int(paper.paper_id)
                    break
            if found_name is not None:
                return found_name
            else:
                raise ValueError(f'{found_name} is not a valid key.')
        else:
            name_list = []
            for key in keys:
                found_name = None
                for name, paper in self.paper_dict.items():
                    if paper.key == key:
                        found_name = int(paper.paper_id)
                        break
                if found_name is not None:
                    name_list.append(found_name)
                else:
                    raise ValueError(f'{found_name} is not a valid key.')
            return name_list
        
    def get_citation_bib(self) -> str:
        bib = ''
        for name, paper in self.paper_dict.items():
            assert paper.bibtex is not None
            bib += paper.bibtex + '\n'

        return bib

    def print_info(self, indices: list[int] | int | None = None):
        info = ''

        if indices is None:
            for i in range(1, self.paper_no + 1):
                info += f'{i}: \n{self.paper_dict[i].__str__()}'
                if not 'bibtex' in self.paper_dict[i].active_attrs:
                    info += f'Warning: This paper does not have a bibtex.\n'
                info += '\n\n'
        elif isinstance(indices, int):
            info += f'{indices}: \n{self.paper_dict[indices].__str__()}'
            if not 'bibtex' in self.paper_dict[indices].active_attrs:
                info += f'Warning: This paper does not have a bibtex.\n'
            info += '\n\n'
        else:
            for i in indices:
                info += f'{i}: \n{self.paper_dict[i].__str__()}'
                if not 'bibtex' in self.paper_dict[i].active_attrs:
                    info += f'Warning: This paper does not have a bibtex.\n'
                info += '\n\n'
        print(info)

    def __str__(self) -> str:
        info = ''
        for i in range(1, self.paper_no + 1):
            info += f"{i}: Paper Title: {self.paper_dict[i].title if 'bibtex' in self.paper_dict[i].active_attrs else None}\n"
            if not 'bibtex' in self.paper_dict[i].active_attrs:
                info += f'Warning: This paper does not have a bibtex.\n'
        return info