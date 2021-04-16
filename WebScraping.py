import requests, re
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/Pennsylvania_State_University"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', class_="infobox vcard")

data = []
data2 = []
c = ['Column 1', 'Column 2']

tag_exclude = 'sup'
tag2 = 'a'

for tr in table.find_all('tr'):
    heading = {}
    th = ''
    for thindex, thinfo in enumerate(tr.find_all('th')):
        if thinfo(tag_exclude):
            thinfo.find(tag_exclude).decompose()
        heading[c[thindex]] = thinfo.get_text()
        th = thinfo.get_text()

    for tdindex, tdinfo in enumerate(tr.find_all('td'), start=1):
        if tdinfo(tag_exclude):
            tdinfo.find(tag_exclude).decompose()
        heading[c[tdindex]] = tdinfo.get_text()
        data.append(heading)

    for divindex, divinfo in enumerate(tr.find_all('div'), start=1):
        if divinfo(tag_exclude):
            divinfo.find(tag_exclude).decompose()
        if divinfo.get_text() == th:
            break
        heading[c[tdindex]] = divinfo.get_text()
        data.append(heading)

    for supinfo in tr.find_all('sup'):
        if supinfo(tag2):
            supinfo.find(tag2).decompose()

for i in data:
    if i not in data2:
        data2.append(i)
    for key in i:
        if '\n' in i[key]:
            i[key] = i[key].replace('\n', '; ')
        if re.findall('\[\d\]', i[key]):
            i[key] = re.sub('\[\d\]', '', i[key])
data = data2[1:21]

with open('headings2.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, c)
    for i in data:
        writer.writerow(i)