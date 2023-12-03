import xlwt,csv,os,sys,importlib
import time
# from urllib2 import urlopen,HTTPError,URLError
#!/usr/bin/env python # -*- coding: utf-8 -*-

url = "http://inventory.northlightseasonal.com/WSinventory.csv"

from helper.gateway import Vendor
					
from helper.waresitat_class import Waresitat




def xls():
	wbook = xlwt.Workbook()
	return wbook

# def isDownloaded():
# 	try:
# 		f = urlopen(url)
# 		print(f"downloading {url}")
		
# 		with open(os.path.dirname(__file__)+"/csv/outfile/"+os.path.basename(url),"wb") as localfile:
# 			localfile.write(f.read())
# 		return True
# 	except (HTTPError) as e:
# 		print("HTTP Error:",e.code,url)
# 	except (URLError) as e:
# 		print("URL Error:",e.code,url)
			
# 	return False
	



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
		wbook.save("./xls/"+vendor.code)



# def clearDownloadedFiles():
# 	dir = r"C:\Users\Berries\Documents\Downloads"
# 	files = [file for file in os.listdir(dir) if "WSinventory" in file]
# 	for f in files:
# 		filename = dir+"\\"+file
# 		os.remove(filename)
# 		print(filename + " removed.")
					
def remove_inactive(local,wares):
	print("Removing all inactive items...")
	all = wares.skus
	for i in local.skus:
		if i not in all:
			del local.prod[i]
	local._initialize_skus()
	
	return local

def is_num(num):

	try:
		float(num)
		return True
	except:
		False

def updateMasterFile(vendor):

	mutator = '{}_catalog'.format(vendor.code)
	parent_dir = os.path.dirname(__file__)
	vendor_module_path = os.path.join(parent_dir,'vendor','{}.py'.format(mutator))

	# _vendorcat_mod = imp.load_source(mutator,module_path) # dynamic module import
	# use importlib to dynamically load the module
	spec = importlib.util.spec_from_file_location(mutator,vendor_module_path)
	vendor_module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(vendor_module)
	cat = getattr(vendor_module,vendor.classname) # dynamic class import
	
	print("Loading data from catalog file...")
	catalog = cat(vendor) # object instance for catalog file
	# print len(catalog)
	time.sleep(1)

	print("Loading data from Waresitat file..")
	local = Waresitat(vendor) # object instance for Master file
	
	
	print("Scanning items for discrepancy...")
	# LOOP all items and CHECK each data
	# count = 1
	for line in catalog.prod:
	
		# if not is_num(catalog.prod[line]['price1']) or not is_num(catalog.prod[line]['min']):
		# 	continue
		
		
		# add item if its new
		if line not in local.prod:
			# print "Count"+str(count)
			print("Adding new product.")
			local.add(catalog.prod[line])
			# count = count + 1
			# otherwise check prices,min,images then update stock
		else:
			print("checking...")
			# print local.prod[line]
			
				# local.prod[line]['size'] == catalog.prod[line]['size'] and \
				# local.prod[line]['name'] == catalog.prod[line]['name'] and \
			if local.prod[line]['stock'] == catalog.prod[line]['stock'] and \
				local.prod[line]['sale'] == catalog.prod[line]['sale'] and \
				float(local.prod[line]['min']) == float(catalog.prod[line]['min']) and \
				float(local.prod[line]['price1']) == float(catalog.prod[line]['price1']) and \
				local.prod[line]['min2'] == catalog.prod[line]['min2'] and \
				local.prod[line]['price2'] == catalog.prod[line]['price2'] and \
				local.prod[line]['min3'] == catalog.prod[line]['min3'] and \
				local.prod[line]['price3'] == catalog.prod[line]['price3'] and \
				float(local.prod[line]['multi']) == float(catalog.prod[line]['multi']):
				
				local.prod[line]['name'] = catalog.prod[line]['name']
				local.prod[line]['stock'] = catalog.prod[line]['stock']
				local.prod[line]['set'] = catalog.prod[line]['set']
				local.prod[line]['cat'] = catalog.prod[line]['cat']

				local.prod[line]['size'] = catalog.prod[line]['size']
				local.prod[line]['desc2'] = catalog.prod[line]['desc2']
				local.prod[line]['isUpdateAvailable'] = ""
			else:
				print("..Updating item")
				local.prod[line]['name'] = catalog.prod[line]['name']
				local.prod[line]['sale'] = catalog.prod[line]['sale'] if catalog.prod[line]['sale'] != 0 else ""
				local.prod[line]['set'] = catalog.prod[line]['set']
				local.prod[line]['size'] = catalog.prod[line]['size']
				local.prod[line]['min'] = catalog.prod[line]['min']
				local.prod[line]['price1'] = catalog.prod[line]['price1'] if catalog.prod[line]['price1'] != 0 else ""
				local.prod[line]['min2'] = catalog.prod[line]['min2'] if catalog.prod[line]['min2'] != 0 else ""
				local.prod[line]['price2'] = catalog.prod[line]['price2'] if catalog.prod[line]['price2'] != 0 else ""
				local.prod[line]['min3'] = catalog.prod[line]['min3'] if catalog.prod[line]['min3'] != 0 else ""
				local.prod[line]['price3'] = catalog.prod[line]['price3'] if catalog.prod[line]['price3'] != 0 else ""
				local.prod[line]['multi'] = catalog.prod[line]['multi']
				local.prod[line]['stock'] = catalog.prod[line]['stock']
				local.prod[line]['desc2'] = catalog.prod[line]['desc2']
				local.prod[line]['cat'] = catalog.prod[line]['cat']
				local.prod[line]['isUpdateAvailable'] = 1
				# local.prod[line]['desc'] = catalog.prod[line]['desc']
				
	local = remove_inactive(local,catalog) # remove discontinued items
	return local
	
def makeXLS(obj,vendor):
	
	wbook = xls()
	wsheet = wbook.add_sheet("Sheet1")

	for count,i in enumerate(obj.prod):
		row = wsheet.row(count)
		val = [obj.prod[i]['name'],obj.prod[i]['sku'],obj.prod[i]['cat'],obj.prod[i]['desc'],obj.prod[i]['stock'],\
		str(obj.prod[i]['sale']),obj.prod[i]['set'],obj.prod[i]['custom'],obj.prod[i]['size'],obj.prod[i]['top'],str(obj.prod[i]['min']),str(obj.prod[i]['price1']),obj.prod[i]['min2'],obj.prod[i]['price2'],obj.prod[i]['min3'],obj.prod[i]['price3'],obj.prod[i]['multi'],obj.prod[i]['img400'],obj.prod[i]['img160'],obj.prod[i]['jpg400'],obj.prod[i]['jpg160'],obj.prod[i]['desc2'],obj.prod[i]['opt'],obj.prod[i]['img800'],obj.prod[i]['jpg800'],obj.prod[i]['isUpdateAvailable']]
		for index,v in enumerate(val):
			# print v.encode("utf-8")
			try:
				row.write(index,float(v))
			except:
				# print v
				try:
					row.write( index,v)
				except:
					row.write( index,v.encode("utf-8"))
				
	wbook.save(os.path.dirname(__file__)+"/xls/output/waresitat/auto_"+vendor.filename)

def main(vendor_ids):

	for id in vendor_ids:
		
		vendor = Vendor(id)		
		# if isDownloaded(): #For Northlight
			# CSVToXLS(vendor)
		
		final = updateMasterFile(vendor)
		makeXLS(final,vendor)
		
		del final
	
if __name__ == "__main__":
	vendor_ids = sys.argv[1:]
	main(vendor_ids)