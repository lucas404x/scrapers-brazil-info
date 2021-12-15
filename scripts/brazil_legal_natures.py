import json

import requests
from bs4 import BeautifulSoup

class LegalNature:
    def __init__(self, code, activity, group):
        self.code = code
        self.activity = activity
        self.group = group

def get_html_string(td):
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    return td.p.span.string.strip().translate(translator)

def main():
    URL = 'https://www.lefisc.com.br/news/novatabelanaturezajuridica.htm'

    html_content = requests.get(URL).content
    html_content = BeautifulSoup(html_content, features='html.parser')

    html_content = html_content.find_all('table', {'class': 'MsoNormalTable'})[0]

    legal_natures = []
    last_group = None

    # extracting the values of html document
    for tr in html_content.find_all('tr')[1:]:
        td = tr.find_all('td')
        if get_html_string(td[0]) == "Código":
            continue

        if len(td) < 2:
            last_group = get_html_string(td[0])
            continue

        code = get_html_string(td[0])
        activity = get_html_string(td[1])
        
        legal_natures.append(LegalNature(code, activity, last_group))
    
    # Making a json file with these info
    with open('legal_natures.json', mode='w',encoding='utf-8') as fp:
        fp.write('[')
        for legal_nature in legal_natures:
            fp.write(json.dumps(legal_nature.__dict__, ensure_ascii=False))
            fp.write(',')
        fp.write(']')
main()