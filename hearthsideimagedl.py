import requests
import csv
import urllib
from bs4 import BeautifulSoup

with open("./csv/infile/lizbethpicsdl2.csv","rb") as infile:
    pair = infile.read().splitlines()
    for item in pair:
        itm = item.split(",")
        print itm[0]
        print itm[1]
        try:
            urllib.urlretrieve(itm[0],"./lizbethpicsdl2/"+itm[1])
        except:
            print "No big image available."