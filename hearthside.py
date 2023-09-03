import requests
from urllib2 import urlopen
from bs4 import BeautifulSoup
import csv

BASE_URL = "http://www.thehearthsidecollection.com/store/index.php?dispatch=categories.catalog"
ITEM_URL = "http://www.thehearthsidecollection.com/store/"

def makesoup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html,'lxml')

soup = makesoup(BASE_URL)
cat = [ITEM_URL + x for in x.findAll('a')]

for i in cat:
    soup = makesoup(i)
    print soup