import csv
import requests
from BeautifulSoup import BeautifulSoup

links = ['http://www.packagingsource.com/store/c/3831-Baby-Gift-Wrap.html?ps=60','http://www.packagingsource.com/store/c/3837-Celebration/Kid-s/Birthday-Gift-Wrap.html?ps=60','http://www.packagingsource.com/store/c/3832-Christmas-Gift-Wrap-Paper.html?ps=90','http://www.packagingsource.com/store/c/3833-Everyday/Floral/Feminine-Gift-Wrap.html','http://www.packagingsource.com/store/c/3834-Masculine-Gift-Wrap.html','http://www.packagingsource.com/store/c/3838-Solids/Foils/Specialty-Kraft-Gift-Wrap.html','http://www.packagingsource.com/store/c/3836-Valentine-Gift-Wrap.html','http://www.packagingsource.com/store/c/3835-Wedding-Gift-Wrap.html']

pagesoup = []
linkss = []
table = []
for i in links:
    html = requests.get(i)
    page = html.content
    soup = BeautifulSoup(page)    
    
    
    for i in soup.findAll('div',attrs={'class':'no-m-b'}):
        links = i.find('a')
        links = 'http://www.packagingsource.com'+ links.get('href')
        linkss.append(links)

for i in linkss:
    pageinfo = []
   
    response = requests.get(i)
    text = response.content
    
    soup = BeautifulSoup(text)      
    
    img = soup.find('a',attrs={'class':'main-product-photo block zoom rel'})
    name = soup.find('h1')      
    sku = soup.find('span',attrs={'class':'ProductItemNr'})
    sku = sku.text
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

outfile = open('./csv/shamrock.csv','wb')
writer = csv.writer(outfile)
writer.writerows(table)