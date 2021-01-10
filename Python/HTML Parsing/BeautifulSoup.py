from bs4 import BeautifulSoup
import urllib.request

mysite = urllib.request.urlopen('http://www.imdb.com/chart/top/').read()
soup_mysite = BeautifulSoup(mysite,'html.parser')

description = soup_mysite.find("meta") # meta tag description
text = description 

print(text)
