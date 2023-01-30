import io
import os

import requests
import PyPDF2
import pandas as pd


def find_full_text(paper_url):
    url = paper_url + '.pdf'

    r = requests.get(url)
    f = io.BytesIO(r.content)

    reader = PyPDF2.PdfReader(f, strict=False)
    contents = ''
    for num in range(len(reader.pages)):
        contents += reader.pages[num].extract_text()

    contents = contents[:contents.find('References')]

    contents = contents.replace('-\n', '')
    contents = contents.replace('\n', ' ')
    return contents


if __name__ == '__main__':
    conferences = ['.acl-', '.emnlp-', '.naacl-', '.inlg-']
    conference_ids = ['/P', '/D', '/N', '/W']
    testing_keywords = ['BLEU', 'Perplexity', 'perplexity', 'CONAN',
                        'SBIC', 'D-1', 'D-2', 'MTLD', 'MATTR', 'METEOR', 'ROUGE']
    human_eval_keywords = ['human evaluation', 'Turk']

    df = pd.read_csv(os.path.dirname(__file__) + '/../data/raw/all_papers.csv')

    # Choose the papers with keyword 'Generation' in the titles
    df_with_keyword = df.loc[df['title'].str.contains('Generation')]
    urls = [url for url in df_with_keyword['url']]

    # Filter papers by the selected conferences
    # paper_in_conferences_after_2020 = [url for url in urls if any([conf in url for conf in conferences])]
    # paper_in_conferences_before_2020 = [url for url in urls if any([conf in url for conf in conference_ids])]
    # paper_in_conferences = paper_in_conferences_after_2020 + paper_in_conferences_before_2020
    paper_in_conferences = [url for url in urls if any([conf in url for conf in conferences])] + \
                           [url for url in urls if any([conf in url for conf in conference_ids])]

    # Separate papers by published years
    paper_by_years = []
    for i in range(0, 23):
        # used to fit the different formats of acl identifier
        style_1 = f"{i:02d}."
        style_2 = f"{i:02d}-"
        temp = [url for url in paper_in_conferences if style_1 in url or style_2 in url]
        paper_by_years.append(temp)

    count = 0
    for papers in paper_by_years:
        texts = []
        for paper in papers:
            try:
                texts.append(find_full_text(paper))
            except:
                print('Error raised when reading text')
        testing_involved = [1 if any(testing_keyword in text for testing_keyword in testing_keywords)
                            else 0 for text in texts]
        human_involved = [1 if any(human_eval_keyword in text for human_eval_keyword in human_eval_keywords)
                          else 0 for text in texts]
        test_res = sum(testing_involved)
        human_eval_res = sum(human_involved)
        print(f'============================Year20{count:02d}===================================')
        print('# of papers having automatic testing: ', test_res)
        print('# of papers have human evals: ', human_eval_res)
        if test_res != 0:
            print('Proportion: ', (sum(human_involved) / sum(testing_involved)))
        else:
            print('Proportion: ', 0)
        count += 1

    # texts = []
    # for i in range(50):
    #     texts.append(find_full_text(urls[i]))
    #     print('finished ', i)
    # testing_involved = [1 if any(testing_keyword in text for testing_keyword in testing_keywords)
    #                     else 0 for text in texts]
    # human_involved = [1 if any(human_eval_keyword in text for human_eval_keyword in human_eval_keywords)
    #                   else 0 for text in texts]
