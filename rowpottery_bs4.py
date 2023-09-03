import requests
from bs4 import BeautifulSoup
import csv

url = "http://www.rowepottery.com/"
print "Grabbing categories..."
html = requests.get(url)
response = html.content
soup = BeautifulSoup(response)

# grab categories
cats = []
catss = []
for i in soup.findAll('li','level0'):
    page1 = i.find('a')
    cats.append(page1['href'])
    print "Category extracted: " + str(page1['href'])
    

# navigating and getting pagination in each category   
for cat in cats:
    print "Getting pagination from category: " + str(cat)   
    html = requests.get(cat)
    print "...loaded."
    response = html.content
    soup = BeautifulSoup(response)
    
    rawpage = soup.find('div','pages')
    try:
        print "...Getting more links."
        rawpages = rawpage.findAll('a')
        for link in rawpages:
            if link['href'] not in catss:
                print "Appending another link."
                cats.append(link['href'])
                print link['href']
            
    except:
        print "***Only one page available.***"

if cats not in catss:
    catss.append(cats)

#getting all items in each page
items = []
for link in catss:
    print "Navigating to page: " +str(link)
    html = requests.get(link)
    response = html.content
    soup = BeautifulSoup(response)
    for item in soup.findAll('a','product-image'):
        print "Getting item for: " + str(item['href'])
        items.append(item['href'])
        
table = []
# getting all items' attributes
for item in items:
    ls = []
    print "Navigating item: " + str(item)
    html = requests.get(item)
    response = html.content
    soup = BeautifulSoup(response)
    
    print "Getting attributes..."
    title = soup.find('h1')
    
    desc = soup.find('div','std')
    info = soup.find('tbody')
    image = soup.find('img',attrs={'id':'image'})
    
    ls.append(title.text.encode('utf-8'))
    ls.append(info.text.encode('utf-8'))
    ls.append(desc.text.encode('utf-8'))
    ls.append(image['src'])
    print ls
    table.append(ls)
    
outfile = open('./csv/rowepottery.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)