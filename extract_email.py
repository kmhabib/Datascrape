from urllib.request import urlopen
from bs4 import BeautifulSoup 
import re
import sys

url = sys.argv[1]
html = urlopen(url)
bsObj = BeautifulSoup(html,"html.parser")
#for link in bsObj.findAll("a",href=re.compile("[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net|co)\.?")):
#    if 'href' in link.attrs:
#        print(link.attrs['href'])

for link in bsObj.findAll("a",href=re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")):
	if 'href' in link.attrs:
		print(link.attrs['href'])

tags = bsObj('a')
for tag in tags:
    # Look at the parts of a tag
    print('TAG:',tag)
    #print('URL:',tag.get('href', None))
    #print('Contents:',tag.contents[0])
    #print ('Attrs:',tag.attrs)