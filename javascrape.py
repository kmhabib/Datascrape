from selenium import webdriver
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

try:
    url = sys.argv[1]
except:
    url = "http://www.zoominfo.com/s/#!search/profile/person?personId=83847290&targetid=profile"
#print("the URL is:",url)

email_set = set()
try:
    driver = webdriver.PhantomJS(executable_path='/Users/khabib/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
except:
    print("it didn't work")

# "http://pythonscraping.com/pages/javascript/ajaxDemo.html"
try:
    driver.get(url)
except:
    print("not able to get the URL")
    raise


waitForLoad(driver)
#print(driver.page_source)
#print(driver.find_element_by_id("content").text)
#time.sleep(3)


pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource, "html.parser")

for link in bsObj.findAll("a", href=re.compile("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\??.*")):
    # print(link)
    if 'href' in link.attrs:
        if "?" in link.attrs['href']:
        # print("..",link.get_text())
            email_set.add(link.get_text())
        else:
            (_m2_, email)=link.attrs['href'].split(":")
            email_set.add(email)
            # print(email,"**")
#print(bsObj.prettify())

for zoom_email in bsObj.findAll("e"):
    print(zoom_email)

if len(email_set)==0:
    #print(len(email_set))
    print("There were no emails found on this url:", url)
else:
    print("These are the emails found on this url:", url)
    for email in email_set:
        print(email)
driver.close()
