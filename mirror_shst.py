import os
from urllib2 import urlopen,HTTPError,URLError
url = "http://inventory.northlightseasonal.com/WSinventory.csv"

from waresitat import Waresitat
# from gateway import Vendor
from shst import SHST

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
	local = Waresitat("C:/Dropbox/Web Updates 2014/2017 Upload/Waresitat Upload/"+vendor.filename)
	
	# for line in catalog.prod:
		# if line[sku] in catalog.skus:
		# print line
			# your code here
			# pass
		# else:
			# local.add(line)
			# pass
			
	
def makeXLS(w):
	wbook = xls()
	wsheet = wbook.add_sheet("Sheet1")
	for count,i in enumerate(w.prod):
		row = wsheet.row(count)
		val = [w.prod[i]['name'],w.prod[i]['sku'],w.prod[i]['cat'],w.prod[i]['desc'],w.prod[i]['stock'],str(w.prod[i]['sale']),w.prod[i]['set'],w.prod[i]['custom'],w.prod[i]['size'],w.prod[i]['top'],str(w.prod[i]['min']),str(w.prod[i]['price1']),w.prod[i]['min2'],w.prod[i]['price2'],w.prod[i]['min3'],w.prod[i]['price3'],w.prod[i]['multi'],w.prod[i]['img400'],w.prod[i]['img160'],w.prod[i]['jpg400'],w.prod[i]['jpg160'],w.prod[i]['desc2'],w.prod[i]['opt'],w.prod[i]['img800'],w.prod[i]['jpg800'],w.prod[i]['UPC']]
		for index,v in enumerate(val):
			try:
				row.write(index,float(v))
			except:
				row.write(index,v)
	wbook.save("./xls/output/Northlight_Seasonal_8016.xls")

def main():

	dir = "C:/Dropbox/Web Updates 2014/2017 Upload/Waresitat Upload/"
	files = [file for file in os.listdir(dir) if os.path.splitext(file)[1] == ".xls"]
	for file in files:
		print dir+file+"\n"
		
		obj = Waresitat(dir+file)
		obj.prod = None
	
	
	
if __name__ == "__main__":
	main()