import lxml.html
import urllib.request

mysite = urllib.request.urlopen('http://www.imdb.com/chart/top/').read()
lxml_mysite = lxml.html.fromstring(mysite)

description = lxml_mysite.xpath("//meta") # meta tag description
text = description # content attribute of the tag

print(text)


# beatiful soup
from bs4 import BeautifulSoup

mysite = urllib.request.urlopen('http://www.imdb.com/chart/top/').read()
soup_mysite = BeautifulSoup(mysite,'html.parser')

description = soup_mysite.find("meta") # meta tag description
text = description 

print(text)
