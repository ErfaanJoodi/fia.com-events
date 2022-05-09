import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

rec = requests.get('https://www.fia.com/')
soup = BeautifulSoup(rec.text , 'html.parser')
bl = str(soup.find_all('div' , attrs={'class' : 'top'}))
bl = bl.split('</div>, <div class="top">')
bl.pop()

def event(i) :
    d = re.findall(r'\"day\"\>(.+?)\<' , i)
    m = re.findall(r'\"month\"\>(.+?)\<' , i)
    en = re.findall(r'\"event\-name\scell\"\>\s+(.+?)\n' , i)
    dm = ''
    if en[0][:2]=='<a' :
        en = re.findall(r'self\"\>(.+)\<' , en[0])
    for n in range(0 , len(d)) :
        dm += '%s %s  -  '%(d[n] , m[n])
    return dm + en[0]

bl = list(map(event , bl))
bl= list(map(lambda x: x.split('  -  '), bl))
bl= list(map(lambda x: [x[0], x[0], x[1]] if len(x)<3 else x, bl))
df= pd.DataFrame(bl, index= [str(x) for x in range(1, len(bl)+ 1)], columns= ['start', 'end', 'subject'])

ha = open('D:\\fia events.txt' , 'w')
ha.write(str(df))
ha.close()