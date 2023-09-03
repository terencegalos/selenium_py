import requests
import csv
from bs4 import BeautifulSoup
import urllib

items = []
with open("./csv/infile/bigrockgoat.csv","rb") as infile:
    for i in infile:
        response = requests.get(i)
        html = response.content
        soup = BeautifulSoup(html,"lxml")  
        try:
            item = soup.find("a","product-name")
            items.append(item["href"])
            print item["href"]
        except:
            print "Item not available."
print "***All links saved***"
            
table = []            
for item in items:
    itm = item.split("?")
    ls = []
    print "Navigating to: " + str(itm[0])
    response = requests.get(itm[0])
    html = response.content
    soup = BeautifulSoup(html,"lxml")
    image = soup.find("img",attrs={"itemprop":"image"})
    print image["src"]
    sku = soup.find("span","editable")
    print sku
    ls.append(sku.text.encode("utf-8"))
    ls.append(image["src"])
    print ls
    table.append(ls)
    
    
outfile = open("./csv/outfile/bigrockgoatfarmimgsku.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)