import xlrd, os, platform
from helper import config

# grabs file depending on which type and detects file attachment
class TableData():
	path = ""
	rsheet = ""
	rbook = ""
	
	def __init__(self,vendor,mode=None,fmt=None):
	
		print("M code: "+str(mode))
		if mode == None or mode == 0:
			print("Normal mode.")
			self.path = config.WARESITAT_UPLOAD_PATH + '/'
			# Convert Windows path to WSL path if running on Linux
			if platform.system() == 'Linux' and self.path.startswith('C:/'):
				self.path = self.path.replace('C:/', '/mnt/c/', 1).replace('\\', '/')
			self.filename = vendor.filename
		elif mode == 1:
			print("SHST mode.")
			self.path = r"/mnt/c/Dropbox/SHST Files/BRANDS Updated Sheet 2019/"
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
			self.path = config.BHBT_UPLOAD_PATH + '/'
			# Convert Windows path to WSL path if running on Linux
			if platform.system() == 'Linux' and self.path.startswith('c:/'):
				self.path = self.path.replace('c:/', '/mnt/c/', 1).replace('\\', '/')
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
