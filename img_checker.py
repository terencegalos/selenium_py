import ftplib,os,xlrd,xlwt,csv,sys,time

delay = 0

v_args =  sys.argv[1:]
#--------------------------------------------------------------------------------------
# ['7900', 'Wing Tai Trading', 'Wing_Tai_Trading', 'Wing_Tai_Trading_7900.xls', 'WingTai160', 'WingTai400', 'WingTai800', '']

class ftp_class():
	image400 = []
	image160 = []
	image800 = []
	
	def con(self):
		ftp = ftplib.FTP("ftp.waresitat.com")
		ftp.login("wares","w@r3s")
		print "Connection succesful!"
		return ftp
		
	def __init__(self,vendor):
		print "FTP retrieval for "+vendor
		print "Establishing ftp connection..."
		time.sleep(delay)
		while True:
			try:
				ftp = self.con()
				break
			except:
				time.sleep(delay)
				print "Reconnecting..."
				continue
		time.sleep(delay)
		
		dirs = self.img_dir(vendor)
		print dirs
		
		print "Loading images..."
		time.sleep(delay)
		for dir in dirs:
			try:
				ftp.cwd(dir)
			except:
				ftp.mkd(dir)
				time.sleep(1)
				ftp.cwd(dir)
			while True:
				try:
					all = [i.lower() for i in ftp.nlst()]
					break
				except:
					ftp = self.con()
					time.sleep(delay)
					continue
			time.sleep(3)
			if "160" in dir:
				print "..size160"
				self.image160 += all
				ftp.cwd("/")
			elif "400" in dir:
				print "..size400"
				self.image400 += all
				ftp.cwd("/")
			else:
				print "..size800"
				self.image800 += all
				ftp.cwd("/")
				
		print "Done loading."
		time.sleep(delay)
				
	def img_dir(self,vendor):
		with open("C:/Users/Berries/Code/csv/outfile/vendor_ids.csv") as infile:
			rcsv = csv.reader(infile)
			sizes = [file[4:7] for file in rcsv if file[1] == vendor][0]
			return sizes
	
	
	
		
class vendor_class():

	file = ""
	name = ""
	image400 = {}
	image160 = {}
	image800 = {}
	noimage = []
	book = None
	sheet = None
	
	def __init__(self,vendor):
		print "Initializing vendor: " + vendor
		time.sleep(delay)
		file = get_files(vendor)
		self.name = vendor
		self.file = file
		self.book = xlrd.open_workbook(file)
		self.sheet = self.book.sheet_by_name("Sheet1")
		
		for x in range(self.sheet.nrows):
			sk = self.sheet.row(x)[1].value
			if is_number(sk):
				sk = int(sk)
				sk = str(sk)
			sk =  (" ".join(sk.split())).strip()
			try:
				self.image400[sk] = self.sheet.row(x)[19].value.lower()
				self.image160[sk] = self.sheet.row(x)[20].value.lower()
			except:
				self.image400[sk] = self.sheet.row(x)[19].value
				self.image160[sk] = self.sheet.row(x)[20].value
			try:
				self.image800[sk] = self.sheet.row(x)[24].value.lower()
			except:
				try:
					self.image800[sk] = self.sheet.row(x)[19].value.lower()
				except:
					self.image800[sk] = self.sheet.row(x)[19].value
					
			
		print "Vendor ready."
		time.sleep(delay)



#===================================================================================
		

def get_input():
	inp = [i for i in raw_input("Enter the name of the vendor:").split(",")]
	print inp
	return inp
		
#get vendor excel filename from csv list
def get_files(vendor):
	with open("C:/Users/Berries/Code/csv/outfile/vendor_ids.csv") as infile:
		rcsv = csv.reader(infile)
		print vendor
		vfiles = [file[3] for file in rcsv if file[1] == vendor][0]
		print vfiles.decode("latin-1")
		if vfiles:
			return vfiles
		else:
			return False
		
def goto_dir():
	if "Code" in os.getcwd():
		os.chdir("C:/Dropbox/Waresitat Files/2022 Upload/Waresitat Upload/")

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
		
def main():

	log = {}
	
	# vendor_s = get_input() #specify vendor/s
	
	for vendor in v_args:
		print vendor
		
		goto_dir()
		
		file = get_files(vendor) #get excel filenames		
		if file == False or file not in os.listdir("."):
			print "Vendor file missing."
			continue
			
		myFTP = ftp_class(vendor) #ftp class instance
		
		myVendor = vendor_class(vendor) #vendor class instance
		
		print "Checking for missing images..."
		time.sleep(delay)
		
		for x in range(myVendor.sheet.nrows):
			sku = myVendor.sheet.row(x)[1].value
			if is_number(sku):
				sku = int(sku)
				sku = str(sku)
			sku = (" ".join(sku.split())).strip()
			# print sku
			if myVendor.image160[sku] not in myFTP.image160 or \
				myVendor.image160[sku] not in myFTP.image400 or \
				myVendor.image160[sku] not in myFTP.image800 or \
				myVendor.image160[sku] == "":
				myVendor.noimage += [sku]
				

		# send to csv file
		outfile = open("C:/Users/Berries/Code/csv/outfile/noimg/"+vendor.replace("/","&")+".csv","wb")
		writer = csv.writer(outfile)
		
		print str(len(myVendor.noimage)) + " images missing."
		
		#write logs
		log.update({myVendor.name:len(myVendor.noimage)})
		with open("C:/Users/Berries/Code/csv/outfile/noimg/logs.csv","wb") as txt:
			l = csv.writer(txt)
			# print log.items()
			for k,v in log.items():
				l.writerow([k,v])
				
		#log missing images
		for x in range(len(myVendor.noimage)): #write no images
			sku = myVendor.noimage[x]
			writer.writerow([sku])
		
		#reset dicts, lists and working directories
		myVendor.noimage[:] = []
		myVendor.image160.clear()
		myVendor.image400.clear()
		myVendor.image800.clear()
		myFTP.image160[:] = []
		myFTP.image400[:] = []
		myFTP.image800[:] = []
		outfile.close()
		os.chdir("C:/Users/Berries/Code/")
		
		print "Done."
		
				
				
#--------------------------------------------------------------------------------------

if __name__ == "__main__":

	main()