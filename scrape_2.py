import csv
import requests
from BeautifulSoup import BeautifulSoup

link = 'http://www.packagingsource.com/store/c/3853-Hanukkah-Gift-Wrap-Paper.html?ps=60'
html = requests.get(link)
page = html.content
pagesoup = BeautifulSoup(page)
links = []
table = []
for i in pagesoup.findAll('div',attrs={'class':'no-m-b'}):
    links = i.find('a')
    links = 'http://www.packagingsource.com'+ links.get('href')
    
    for i in links:
    pageinfo = []
   
    response = requests.get(i)
    text = response.content
    
    soup = BeautifulSoup(text)      
 
    img = soup.find('a',attrs={'class':'main-product-photo block zoom rel'})
    name = soup.find('h1')      
    sku = soup.text.find('span')
    desc = soup.find('div',attrs={'class':'tab-pane fade in pad-20 no-pad-lr active'})
    cat = soup.find('span',attrs={'class':'ProductDetailsCategoryTrail'})    
    info1 = soup.findAll('option')    
    info2 = soup.findAll('span',attrs={'class':'ProductDetailsPrice PriceToUpdate'})
    
    
    pageinfo.append(name.text)
    pageinfo.append(sku)
    pageinfo.append(desc.text)
    pageinfo.append(cat.text)
    pageinfo.append(info1)
    pageinfo.append(info2)
    pageinfo.append('http://www.packagingsource.com'+img.get('href'))
    table.append(pageinfo)
    print pageinfo

outfile = open('./test.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)