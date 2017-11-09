from selenium import webdriver
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
import collections
import csv

# Creat a dictionary of dictionary to store the URL (as key), Name and scraped summary of the person


# This function waits for elements to load in case there's a redirect or javascript on the page. 
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            #print("Timing out after 10 seconds and returning")
            return
        time.sleep(5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return


#print("the URL is:",url)
def getSoup(driver, url):
# uses the phantomJS program to open a headless html driver. 
	# takes in the given url loads the html
	try:
	    driver.get(url)
	except:
	    print("not able to get the URL")
	    raise
	pageSource = driver.page_source
	# pass the html source to beatufiulsoup and makes it in an object.
	bsObj = BeautifulSoup(pageSource, "html.parser")
	#waitForLoad(driver)
	time.sleep(3)
	return bsObj

def getData(bsObj, writer):
	d = collections.defaultdict(dict)
	
# finds the top level "li" tag with class name of 'b_algo' which has the search results from the bing query.
	for header in bsObj.findAll('li', attrs={'class' : 'b_algo'}):
		try:
			a=header.find('a') # find all the 'a' tags with a url
			linked_url=a['href'] # get the URL
			name,_ignore_=a.text.split("|") # get the text with the url
			#firstname,lastname = name.split(" ")
			#div=header.find('div', attrs={'class' : 'b_caption'}) # this looks at the div class to scrape teh summary
			#summary=div.text # the scraped URL summary
			#lis = []
			p = header.find('p')
			summary = p.text
			for li in header.findAll('li'):
				#length_of_li = len(li)
				li_text = li.text
				#print(li_text)
				#lis.append(li_text)
				writer.writerow((name,linked_url,li_text,summary))
			#for li in lis:
				#print(li)
			
			#print(length_of_li)
			#print("P is:",p.text)
			print("Summary is:", summary)
			#print("UL is:", li,"P is:",p.text)
			d[linked_url][name] = summary # assign the summary as a value to the key of name which is also in a dict
			
			#print(d)
		except:
			break

	return d
	

def getNextPage(bsObj):
	try:
		paginate = bsObj.find('a', href=re.compile(".*FORM=PERE$"))
		pageUrl = paginate['href']
		nextUrl="http://www.bing.com"+pageUrl
		return(nextUrl)
	except:
		print("completed the bing scraping") #html = urlopen("http://www.bing.com"+pageUrl)
		return None

def phantomCreate():
	try:
	    driver = webdriver.PhantomJS(executable_path='/Users/khabib/Downloads/phantomjs-2.1.1-macosx/bin/phantomjs')
	    return driver
	except:
	    print("it didn't work")

def printDict(d,writer):
	for x in d:
		#print("I am in for loop in printDict")
		#print(x)
		#writer.writerow(([x]))
		for y in d[x]:
			pass
			#print("I am in 2nd for loop in printDict")
			#print([x],y,d[x][y])
			#writer.writerow((x,y,d[x][y]))


def main(url):
	csvFile = open("bing.csv", 'w')
	status = True
	count = 0
	try:
		writer = csv.writer(csvFile, dialect='excel')
		writer.writerow(('LINK','NAME', 'TITLE','SUMMARY'))
		driver = phantomCreate()
		soup = getSoup(driver, url) 	
		d = getData(soup, writer)
		#printDict(d,writer)
		while status is True:
			nexturl = getNextPage(soup)
			if nexturl is None:
				status = False
				break
			newsoup = getSoup(driver, nexturl)
			d = getData(newsoup,writer)
			#printDict(d,writer)
			count = count + 1
			print("Page Number:",count,"*****")

	finally:
		csvFile.close()
	#printDict(d)
	#print("\n\n\n")
	#print("-------------------------------------------------------")
	#printDict(dnew)
	#status = getNextPage(soup)
	#print(status)
        

if __name__ == '__main__':
	main(sys.argv[1])
#http://www.bing.com/search?q=site%3alinkedin.com%2fin+%22merkle+inc%22&qs=n&sp=-1&pq=site%3alinkedin.com%2fin+%22merkle+inc%22&sc=8-31&sk=&cvid=D3C7836A296B410E8884EF2A404B8B16&first=11&FORM=PERE
#http://www.bing.com/search?q=site%3alinkedin.com%2fin+%22merkle+inc%22&qs=n&sp=-1&pq=site%3alinkedin.com%2fin+%22merkle+inc%22&sc=8-31&sk=&cvid=D3C7836A296B410E8884EF2A404B8B16&first=21&FORM=PERE1
#http://www.bing.com/search?q=site%3alinkedin.com%2fin+%22merkle+inc%22&qs=n&sp=-1&pq=site%3alinkedin.com%2fin+%22merkle+inc%22&sc=8-31&sk=&cvid=D3C7836A296B410E8884EF2A404B8B16&first=31&FORM=PERE2
