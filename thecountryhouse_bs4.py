import csv
import requests
from bs4 import BeautifulSoup
import urllib
import urlparse


with open("./csv/infile/thecountryhouseinfile.csv","rb") as infile:
    for i in infile:
        response = requests.get(i)
        html = response.content
        soup = BeautifulSoup(html,"lxml")
        sku = i
        image = soup.find("div",attrs={"class":"productImg"})
        print sku
        print soup
        print image
        