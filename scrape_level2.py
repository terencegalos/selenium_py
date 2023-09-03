import csv
import requests
from BeautifulSoup import BeautifulSoup


url = 'http://www.packagingsource.com//store/p/2243-Blue-Gloss-Gift-Wrap.html'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)

sku = soup.find('span',{'class':'ProductItemNr'}).string

desc = soup.find('div',attrs={'class':'tab-pane fade in pad-20 no-pad-lr active'})
desc_text = desc.text

dim = soup.find('div',{'class':'pad-10 no-pad-tb'})
dim = dim.text

img = soup.find('img',{'class':'zoomImg'})
img = img


cells_list = []

cells_list.append(sku)
cells_list.append(desc_text)
cells_list.append(dim)
cells_list.append(img)

print cells_list
