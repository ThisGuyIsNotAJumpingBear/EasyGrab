import io

import requests
import PyPDF2


def find_full_text(paper_url):
    url = paper_url + '.pdf'

    r = requests.get(url)
    f = io.BytesIO(r.content)

    reader = PyPDF2.PdfReader(f)
    contents = ''
    for num in range(len(reader.pages)):
        contents += reader.pages[num].extract_text()

    contents = contents[:contents.find('References')]

    contents = contents.replace('-\n', '')
    contents = contents.replace('\n', ' ')
    return contents


if __name__ == '__main__':
    template = 'https://aclanthology.org/2022.wnu-1.2'
    content = find_full_text(template)
