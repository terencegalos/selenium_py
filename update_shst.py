import xlwt,xlrd,csv,os,sys,json,time
from urllib2 import urlopen,HTTPError,URLError


from gateway import Vendor
					
from waresitat_class import Waresitat

from shst_class import SHST

from xls_getter import TableData

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
			
			
def remove_inactive(local,wares):
	print "Removing all inactive items..."
	all = wares.skus
	for i in local.skus:
		if i not in all:
			del local.prod[i]
	local._initialize_skus()
	
	return local
	
def updateSHST(vendor,mode=None):

	print "Loading data from Waresitat file..."
	wares = Waresitat(vendor) # shst instance of waresitat file
	time.sleep(3)
	print "Loading data from SHST file..."
	local = SHST(vendor,1) #  shst instance of shst file
	# print local
	
	#remove inactive	
	print "Scanning items for discrepancy..."
	for key in wares.prod:
		if key not in local.prod: # add new
			if len( wares.prod[key]['jpg800'] ) > 4: #add if image available
				# print wares.prod[key]
				local.add(wares.prod[key])
			else:
				print wares.prod[key]
				print "No image. Skipping..."
		else: #check prices
			
			#  local.prod[key]['cat'] == wares.prod[key]['cat'] and \
			#  local.prod[key]['sale'] == wares.prod[key]['sale'] and \
			if local.prod[key]['price1'] == wares.prod[key]['price1'] and \
			 local.prod[key]['min'] == wares.prod[key]['min'] and \
			 local.prod[key]['min2'] == wares.prod[key]['min2'] and \
			 local.prod[key]['price2'] == wares.prod[key]['price2'] and \
			 local.prod[key]['min3'] == wares.prod[key]['min3'] and \
			 local.prod[key]['price3'] == wares.prod[key]['price3'] and \
			 local.prod[key]['multi'] == wares.prod[key]['multi'] and \
			 local.prod[key]['stock'] == wares.prod[key]['stock'] and \
			 local.prod[key]['msrp'] == wares.prod[key]['price1'] * 2:
				local.prod[key]['stock'] = " ".join(wares.prod[key]['stock'].strip().split())
				local.prod[key]['cat'] = wares.prod[key]['cat']
				local.prod[key]['desc'] = wares.prod[key]['desc']
				local.prod[key]['cat'] = " ".join(wares.prod[key]['cat'].strip().split())
				local.prod[key]['size'] = wares.prod[key]['size']
				local.prod[key]['jpg800'] = wares.prod[key]['jpg800']
			else:
				local.prod[key]['stock'] = " ".join(wares.prod[key]['stock'].strip().split())
				local.prod[key]['msrp'] = wares.prod[key]['price1'] * 2
				local.prod[key]['cat'] = wares.prod[key]['cat']
				local.prod[key]['price1'] = wares.prod[key]['price1']
				local.prod[key]['price2'] = wares.prod[key]['price2']
				local.prod[key]['price3'] = wares.prod[key]['price3']
				local.prod[key]['dize'] = wares.prod[key]['size']
				local.prod[key]['min'] = wares.prod[key]['min']
				local.prod[key]['min2'] = wares.prod[key]['min2']
				local.prod[key]['min3'] = wares.prod[key]['min3']
				local.prod[key]['sale'] = wares.prod[key]['sale']
				local.prod[key]['multi'] = wares.prod[key]['multi']
				local.prod[key]['cat'] = " ".join(wares.prod[key]['cat'].strip().split())
				local.prod[key]['desc'] = " ".join(wares.prod[key]['desc'].strip().split())
				local.prod[key]['jpg800'] = wares.prod[key]['jpg800']
				local.prod[key]['isUpdateAvailable'] = 1
	
	local = remove_inactive(local,wares)
	del wares # unset object		
	return local
				
def makeXLS(wobj,vendor):
	wbook = xls()
	wsheet = wbook.add_sheet("Sheet1")

	for count,i in enumerate(wobj.prod):
		row = wsheet.row(count)
		val = [wobj.prod[i]['name'],wobj.prod[i]['sku'],wobj.prod[i]['cat'],wobj.prod[i]['desc'],wobj.prod[i]['stock'],wobj.prod[i]['size'],wobj.prod[i]['min'],wobj.prod[i]['price1'],wobj.prod[i]['min2'],wobj.prod[i]['price2'],wobj.prod[i]['min3'],wobj.prod[i]['price3'],wobj.prod[i]['multi'],wobj.prod[i]['jpg800'],wobj.prod[i]['minretail'],wobj.prod[i]['msrp'],wobj.prod[i]['sale'],wobj.prod[i]['ship'],wobj.prod[i]['isactive'],wobj.prod[i]['brand'],wobj.prod[i]['category'],wobj.prod[i]['opt'],wobj.prod[i]['section'],wobj.prod[i]['desc2'],wobj.prod[i]['isImageAvailable'],wobj.prod[i]['isUpdateAvailable']]

		for index,v in enumerate(val):
			try:
				row.write(index,float(v))
			except:
				row.write(index,v)
	
	wbook.save("./xls/output/shst/auto_"+vendor.shst)





def main():
	vendors = sys.argv[1:]
	with open("./csv/outfile/vendor_ids.csv","rb") as infile:
		freader = csv.reader(infile)	
		for i,line in enumerate(freader): # loop all vendor names
			if i > 0:
				id = line[0]
				if id in vendors:
					
					vendor = Vendor(id)
					print vendor.name
					print vendor.filename
					
					final = updateSHST(vendor)
					
					# for i,sku in enumerate(final.prod):
						# if i < 100: # print first 100 items for viewing
							# print final.prod[sku]
							
					makeXLS(final,vendor)
					final = None
			
	
if __name__ == "__main__":
	main()
	