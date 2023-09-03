import requests
import csv
from bs4 import BeautifulSoup

sections = ["http://www.absolutesoap.com/body-balm/","http://www.absolutesoap.com/crush-on-you-handmade-sugar-scrubs/","http://www.absolutesoap.com/handmade-perfume/","http://www.absolutesoap.com/handmade-soap/","http://www.absolutesoap.com/handmade-soap/ruby-rock-star-soap/"]

items = []
for section in sections:
    print "Getting items in: " + str(section)
    response = requests.get(section)
    html = response.content
    soup = BeautifulSoup(html,"lxml")
    for i in soup.findAll("div","ProductImage"):
        link = i.find("a")
        print str(link) + " found**"
        items.append(link["href"])
        
print "***Links scraped. Getting each item info***"

table = []
for item in items:
    print "Navigating to: " + str(item)
    response = requests.get(item)
    html = response.content
    soup = BeautifulSoup(html,"lxml")
    
    ls = []
    name = soup.find("h1",attrs={"itemprop":"name"})
    cat = soup.find("ul","breadcrumbs")
    minqty = soup.find("option",attrs={"selected":"selected"})
    price = soup.find("span",attrs={"itemprop":"price"})
    desc = soup.find("div",attrs={"itemprop":"description"})
    img = soup.find("img","wide-image main-image")
    
    ls.append(name.text.encode("utf-8"))
    ls.append(cat.text.encode("utf-8"))
    ls.append(desc.text.encode("utf-8"))
    ls.append(minqty.text.encode("utf-8"))
    ls.append(price.text.encode("utf-8"))
    try:
        ls.append(img["src"])
    except:
        ls.append("None")
    print ls
    table.append(ls)
        
outfile = open("./csv/outfile/absolutesoupitems_result.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"   
        
     