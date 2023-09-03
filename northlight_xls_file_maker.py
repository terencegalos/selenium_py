import xlwt,xlrd,csv,os
from urllib2 import urlopen,HTTPError,URLError
url = "http://inventory.northlightseasonal.com/WSinventory.csv"

from gateway import Vendor
					
from waresitat_class import Waresitat


def xls():
	wbook = xlwt.Workbook()
	return wbook
	
def isDownloaded():
	try:
		f = urlopen(url)
		print "downloading "+url
		
		with open("./csv/outfile/"+os.path.basename(url),"wb") as localfile:
			localfile.write(f.read())
		return True
	except HTTPError,e:
		print "HTTP Error:",e.code,url
	except URLError,e:
		print "URL Error:",e.code,url
			
	return False
	

def CSVToXLS(vendor):
	with open("./csv/outfile/"+os.path.basename(url)) as infile:
		wbook = xls()
		wsheet= wbook.add_sheet("Sheet1")
		rows = csv.reader(infile)
		for c,line in enumerate(rows):
			row = wsheet.row(c)
			if c > 0:
				for n,val in enumerate(line):
					try:
						row.write(n,float(val))
					except:
						# print val
						row.write(n,val.decode("latin-1"))
		wbook.save("./xls/"+vendor.filename)
		
		
		
def clearDownloadedFiles():
	dir = "C:\Users\Berries\Documents\Downloads"
	files = [file for file in os.listdir(dir) if "WSinventory" in file]
	for f in files:
		filename = dir+"\\"+file
		os.remove(filename)
		print filename + " removed."
			
			
def updateMasterFile(vendor): # in progress*****

	
	catalog = Waresitat("./xls/"+vendor.filename,fmt = "Northlight Seasonal")
	local = Waresitat("D:/Dropbox/Web Updates 2014/2017 Upload/Waresitat Upload/"+vendor.filename)
	# print catalog
	
	for line in catalog.prod:
		if line not in local.skus:
			print "Adding new product."
			local.add(catalog.prod[line])
		else:
			print "checking..."
			if local.prod[line]['price1'] == catalog.prod[line]['price1'] and local.prod[line]['min'] == catalog.prod[line]['min'] and local.prod[line]['jpg160'] == catalog.prod[line]['jpg160']:
				local.prod[line]['stock'] = catalog.prod[line]['stock']
			else:
				print "..Updating item"
				local.prod[line].clear()
				local.prod[line].update(catalog.prod[line])
	return local			
			
	
def makeXLS(wobj,vendor):
	wbook = xls()
	wsheet = wbook.add_sheet("Sheet1")
	for count,i in enumerate(wobj.prod):
		row = wsheet.row(count)
		val = [wobj.prod[i]['name'],wobj.prod[i]['sku'],wobj.prod[i]['cat'],wobj.prod[i]['desc'],wobj.prod[i]['stock'],str(wobj.prod[i]['sale']),wobj.prod[i]['set'],wobj.prod[i]['custom'],wobj.prod[i]['size'],wobj.prod[i]['top'],str(wobj.prod[i]['min']),str(wobj.prod[i]['price1']),wobj.prod[i]['min2'],wobj.prod[i]['price2'],wobj.prod[i]['min3'],wobj.prod[i]['price3'],wobj.prod[i]['multi'],wobj.prod[i]['img400'],wobj.prod[i]['img160'],wobj.prod[i]['jpg400'],wobj.prod[i]['jpg160'],wobj.prod[i]['desc2'],wobj.prod[i]['opt'],wobj.prod[i]['img800'],wobj.prod[i]['jpg800'],wobj.prod[i]['UPC']]
		for index,v in enumerate(val):
			try:
				row.write(index,float(v))
			except:
				row.write(index,v)
	wbook.save("./xls/output/"+vendor.filename)

def main():

	vendor = Vendor("8016")
	# print vendor.filename
	
	if isDownloaded():
		CSVToXLS(vendor)
	
	final = updateMasterFile(vendor)
	makeXLS(final,vendor)
	
	
	
if __name__ == "__main__":
	main()