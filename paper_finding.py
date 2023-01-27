import requests


def find_papers_by_meeting(url):
    """
    TODO: Docstring
    """
    response = requests.get(url)
    text = response.text
    text = text[text.find('section'):]
    text = text[text.find('/div'):]
    text = text[text.find('<div'):]
    sections = separate_text_by_tags(text, '<hr>')

    paper_urls = []
    for section in sections:
        section_name_start = section.find('id=') + 3
        section_name_end = section.find('>')
        section_name = section[section_name_start: section_name_end]
        print(section_name)

        section_text = section[section.find('<p') + 2:]
        paper_section = separate_text_by_tags(section_text, '<p')

        # extract url
        paper_url = extract_urls(paper_section)
        paper_urls.extend(paper_url)

        # extract name

        # extract affiliated section

    return paper_urls


# Helper Functions #
def separate_text_by_tags(text, tag):
    """
    TODO: Docstring
    """
    sections = []
    while text.find(tag) > 0:
        end = text.find(tag) + len(tag)
        sections.append(text[:end])
        text = text[end:]
    return sections


def extract_urls(text_list):
    """
    TODO: Docstring
    """
    urls = []
    for text in text_list:
        url_temp = text[text.find('href=') + 5:]
        if '.pdf' in url_temp:
            urls.append(url_temp[:url_temp.find(' ')])
    return urls


if __name__ == '__main__':
    meeting_url = 'https://aclanthology.org/events/acl-2022/'
    papers = find_papers_by_meeting(meeting_url)
