import requests
from bs4 import BeautifulSoup
import json
import re
from html.parser import HTMLParser
import time

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

emails = set()
session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) \
                         AppleWebKit 537.36 (KHTML, like Gecko) Chrome",\
           "Accept":"text/html,application/xhtml+xml,application/xml;\
                     q=0.9,image/webp,*/*;q=0.8"}
base_url = "https://www.google.com/search?q="
#req = session.get(url, headers=headers)

#print(req.headers)
#bsObj = BeautifulSoup(req.text, "html.parser")
#print(bsObj)
#print(bsObj.find("div",{"class":"user-agent"}).get_text)

num_page = 1
with open("input.txt", 'r') as domainfile:
   for line in domainfile:
      line = line.rstrip()
      search_query = "mails+" + "\"@" + line + "\""
      query = base_url + search_query 
      #print(query)
      req = session.get(query, headers=headers)
      stripped = strip_tags(req.text)
      new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z/n]*", stripped, re.I))
      emails.update(new_emails)
      time.sleep(5)
      #random.seed(datetime.now())
      #print(req.text)
      #print(stripped)
      #bsObj = BeautifulSoup(req.text, "html.parser")
      #print(bsObj) 
#print(emails)

with open("output.txt", 'w') as outputfile:
   for email in emails:
      email = email.rstrip('.')
      outputfile.write("%s\n" % email)

   
