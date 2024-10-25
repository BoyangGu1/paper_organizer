safe_categories = ['survey']

possible_entries = [
    'article', 'book', 'inbook', 'inproceedings', 'phdthesis', 'mastersthesis', 'techreport', 'misc'
]

required_fields = {
    'article': ['author', 'title', 'year'],
    'book': ['author', 'title', 'publisher', 'year'],
    'inbook': ['author', 'title', 'chapter', 'pages', 'publisher', 'year'],
    'inproceedings': ['author', 'title', 'booktitle', 'year'],
    'phdthesis': ['author', 'title', 'school', 'year'],
    'mastersthesis': ['author', 'title', 'school', 'year'],
    'techreport': ['author', 'title', 'institution', 'year'],
    'misc': []
}

optional_fields = {
    'article': ['journal', 'volume', 'number', 'pages', 'month', 'note', 'key', 'publisher'],
    'book': ['volume', 'number', 'series', 'address', 'edition', 'month', 'note', 'key'],
    'inbook': ['volume', 'number', 'series', 'type', 'address', 'edition', 'month', 'note', 'key'],
    'inproceedings': ['editor', 'volume', 'number', 'series', 'pages', 'address', 'month', 'organization', 'publisher', 'note', 'key'],
    'phdthesis': ['type', 'address', 'month', 'note', 'key'],
    'mastersthesis': ['type', 'address', 'month', 'note', 'key'],
    'techreport': ['type', 'number', 'address', 'month', 'note', 'key'],
    'misc': ['author', 'title', 'howpublished', 'month', 'year', 'note', 'key']
}

# Get all items from both dictionaries
all_items = set()
for fields_dict in (required_fields, optional_fields):
    for field_list in fields_dict.values():
        all_items.update(field_list)
safe_attrs = ['bibtex', 'keywords', 'category', 'relations', 'entry', 'key', 'paper_id'] + list(all_items)