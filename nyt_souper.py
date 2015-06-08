from bs4 import BeautifulSoup
from nytimesarticle import articleAPI
import csv
import sys
import requests
reload(sys)  
sys.setdefaultencoding('utf8')

r  = requests.get('http://query.nytimes.com/gst/fullpage.html?res=9B07E3DB1438F932A25756C0A9659D8B63')
data = r.text
soup = BeautifulSoup(data)
# print soup.prettify()
item = soup.find_all("p", {"class":["story-body-text story-content","story-body-text"]})
item.extend(soup.find_all(["p", {"itemprop":"articleBody"}]))
print item
