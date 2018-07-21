import bs4
import re
import requests
import json

url = 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Status'
httpResponses = dict()
data = []

def generateStatusFile(data, name, append = False, beautify = True):
    mode = 'w'
    indent = 4

    if append == True:
        mode = 'a'
    
    if beautify == False:
        indent = None

    with open((name + '.json'), mode=mode, encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=indent)

html = (requests.get(url)).text
soup = bs4.BeautifulSoup(html, "html.parser")
dls = soup.body.main.find('div', {'class':'center clear'}).find(id='document-main').find('div', {'class':'center'}).find(id='wiki-column-container').find(class_='column-container').find(id='wiki-content').find(id='wikiArticle').find_all('dl')

for dl in dls:
    for dt in dl.find_all('dt'):
        if dt.code != None:
            data.append(dt.code.get_text())

for inf in data:
    code = re.search(r'\d+', inf).group()
    description = re.search(r'\D+', inf).group()
    httpResponses[code] = description.strip()
    
generateStatusFile(httpResponses, 'responses')

print('Check the responses.json file to see the collected data. Done!')