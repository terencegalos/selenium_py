import requests
import csv
from bs4 import BeautifulSoup

sections = ["http://www.kreativekraftwerks.com/Classes_in_Making_Soap_Lotion_and_Candles_s/1871.htm?searching=Y&sort=13&cat=1871&show=40&page=1","http://www.kreativekraftwerks.com/Handcrafted_Goat_Milk_Honey_Lotion_s/1477.htm?searching=Y&sort=7&cat=1477&show=20&page=1","http://www.kreativekraftwerks.com/Scented_Candles_s/1814.htm","http://www.kreativekraftwerks.com/Scented_Gifts_s/1861.htm?searching=Y&sort=13&cat=1861&show=100&page=1","http://www.kreativekraftwerks.com/category_s/1817.htm?searching=Y&sort=13&cat=1817&show=100&page=1"]

items = []
for section in sections:
    print "Getting items in: " + str(section)
    response = requests.get(section)
    html = response.content
    soup = BeautifulSoup(html,"lxml")
    for i in soup.findAll("a","productnamecolor colors_productname"):
        print str(i) + " found**"
        items.append(i["href"])
        
print "***Links scraped. Getting each item info***"

table = []
for item in items:
    print "Navigating to: " + str(item)
    response = requests.get(item)
    html = response.content
    soup = BeautifulSoup(html,"lxml")
    
    ls = []
    name = soup.find("span",attrs={"itemprop":"name"})
    img = soup.find("img","vCSS_img_product_photo")
    print img
    
    ls.append(name.text.encode("utf-8"))
    try:
        ls.append(img["src"])
    except:
        ls.append("None")
    print ls
    table.append(ls)
        
outfile = open("./csv/outfile/kreativekraftwerks_result.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)

print "***Job Done***"   
        
     