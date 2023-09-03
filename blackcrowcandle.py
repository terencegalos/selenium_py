import requests
from bs4 import BeautifulSoup
import csv

cats = ["http://blackcrowcandlecompany.com/index.php?route=product/category&path=59","http://blackcrowcandlecompany.com/index.php?route=product/category&path=59","http://blackcrowcandlecompany.com/index.php?route=product/category&path=60","http://blackcrowcandlecompany.com/index.php?route=product/category&path=62","http://blackcrowcandlecompany.com/index.php?route=product/category&path=66","http://blackcrowcandlecompany.com/index.php?route=product/category&path=65","http://blackcrowcandlecompany.com/index.php?route=product/category&path=63","http://blackcrowcandlecompany.com/index.php?route=product/category&path=64","http://blackcrowcandlecompany.com/index.php?route=product/category&path=61"]

table = []

def makesoup(url):
    html = requests.get(url)
    response = html.content
    soup = BeautifulSoup(response,"lxml")
    return soup
    
def init_scrape_date():
    title = item.find('h1')

    item_cat = item.find('div','breadcrumb')

    price = item.find('div','price')

    scent = [i for i in item.findAll('option')]

    desc = item.find('div',attrs={'id':'tab-description'})

    image = item.find('img',attrs={'id':'image'})
    
    print title.text
    print desc.text
    print item_cat.text
    print scent
    print price.text
    print image['src']
    
    ls.append(title.text.encode("utf-8"))
    ls.append(item_cat.text.encode("utf-8"))
    ls.append(price.text.encode("utf-8"))
    ls.append(scent)
    ls.append(desc.text.encode("utf-8"))
    ls.append(image['src'])
    
    table.append(ls)
    
for i in cats:
    items = []
    cat = makesoup(i)
    for i in cat.findAll('div','name'):
        lnk = i.find('a')
        print "Getting items url: " + lnk['href']
        items.append(lnk['href'])        
        for i in items:
            ls = []
            item = makesoup(i)

outfile = open('./csv/blackcrowcandles.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)