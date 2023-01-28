import bibtexparser
import pandas as pd
import os.path

with open(os.path.dirname(__file__) + '/../data/source/anthology.bib', 'r', encoding='utf-8') as bibtex_file:
    bib_db = bibtexparser.load(bibtex_file)


titles = [entry['title'].replace('{', '').replace('}', '') for entry in bib_db.entries]
dates = [entry['year'] for entry in bib_db.entries]
publishers = [entry['publisher'] if 'publisher' in entry.keys() else 'None' for entry in bib_db.entries]
urls = [entry['url'] for entry in bib_db.entries]

df = pd.DataFrame({
    'title': titles,
    'date': dates,
    'publisher': publishers,
    'url': urls
})

df.to_csv(os.path.dirname(__file__) + '/../data/raw/all_papers.csv')
