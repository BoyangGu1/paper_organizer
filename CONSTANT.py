possible_entries = [
    'article', 'book', 'inbook', 'inproceedings', 'phdthesis', 'mastersthesis', 'techreport', 'misc'
]

required_fields = {
    'article': ['author', 'title', 'journal', 'year'],
    'book': ['author', 'title', 'publisher', 'year'],
    'inbook': ['author', 'title', 'chapter', 'pages', 'publisher', 'year'],
    'inproceedings': ['author', 'title', 'booktitle', 'year'],
    'phdthesis': ['author', 'title', 'school', 'year'],
    'mastersthesis': ['author', 'title', 'school', 'year'],
    'techreport': ['author', 'title', 'institution', 'year'],
    'misc': []
}

optional_fields = {
    'article': ['volume', 'number', 'pages', 'month', 'note', 'key'],
    'book': ['volume', 'number', 'series', 'address', 'edition', 'month', 'note', 'key'],
    'inbook': ['volume', 'number', 'series', 'type', 'address', 'edition', 'month', 'note', 'key'],
    'inproceedings': ['editor', 'volume', 'number', 'series', 'pages', 'address', 'month', 'organization', 'publisher', 'note', 'key'],
    'phdthesis': ['type', 'address', 'month', 'note', 'key'],
    'mastersthesis': ['type', 'address', 'month', 'note', 'key'],
    'techreport': ['type', 'number', 'address', 'month', 'note', 'key'],
    'misc': ['author', 'title', 'howpublished', 'month', 'year', 'note', 'key']
}
