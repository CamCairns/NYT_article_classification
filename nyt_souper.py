from bs4 import BeautifulSoup
from nytimesarticle import articleAPI
import csv
import sys
import requests
reload(sys)  
sys.setdefaultencoding('utf8')

r  = requests.get('http://query.nytimes.com/gst/fullpage.html?res=940DE5D6123DF934A25756C0A9649D8B63')
data = r.text
soup = BeautifulSoup(data)
#print soup.prettify()
item = soup.find_all([("p", {"class":"story-body-text story-content"}), ("p", {"itemprop":"articleBody"})])
print item
