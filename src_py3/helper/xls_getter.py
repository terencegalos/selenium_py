import xlrd, os

# grabs file depending on which type and detects file attachment
class TableData():
	path = ""
	rsheet = ""
	rbook = ""
	
	def __init__(self,vendor,mode=None,fmt=None):
	
		print("M code: "+str(mode))
		if mode == None or mode == 0:
			print("Normal mode.")
			self.path = "E:/Dropbox/Waresitat Files/2022 Upload/Waresitat Upload/"
			self.filename = vendor.filename
		elif mode == 1:
			print("SHST mode.")
			self.path = "C:/Dropbox/SHST Files/BRANDS Updated Sheet 2019/"
			if vendor.shst:
				self.filename = vendor.shst
			else:
				self.filename = "File does not exist."
		elif mode == 2:
			print("Catalog mode.")
			self.path = os.path.dirname(__file__)+"/xls/"
			self.filename = str(vendor.code)+".xls"
		elif mode == 3:
			print("BHBT mode.")
			self.path = "E:/Dropbox/Waresitat Files/2022 Upload/BuyHereBuyThere/"
			if vendor.bhbt:
				self.filename = vendor.bhbt
		if self._paramcheck():
			self.rbook = xlrd.open_workbook(self.path+self.filename)
		else:
			print("Vendor file does not exist.")

		self.rsheet = self.rbook.sheet_by_index(0)
		
	
	
	
	def _paramcheck(self):
		if hasattr(self,'path') and hasattr(self,'filename') and hasattr(self,'rsheet') and hasattr(self,'rbook'):
			return True
		else:

			print("TableData initialization failed. Please check.")
			return False
			
	def getBook(self):
		return self.rbook
		
	def getSheet(self):
		return self.rsheet
