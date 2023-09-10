from xls_getter import TableData
import datetime

class Bright_Ideas():
	prod = {}
	skus = None
	disc = False
	
	def is_num(self,n):
		try:
			float(n)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
		
			# if rsheet.row(x)[4].value < 4:
			# 	print "Skipping..."
			# 	continue
			
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[10].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[2].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[4].value
			self.prod[sku]['price1'] = rsheet.row(x)[5].value
			self.prod[sku]['min2'] = rsheet.row(x)[6].value
			self.prod[sku]['price2'] = round(rsheet.row(x)[7].value,2) if self.is_num(rsheet.row(x)[7].value) else rsheet.row(x)[7].value
			self.prod[sku]['min3'] = rsheet.row(x)[8].value
			self.prod[sku]['price3'] = round(rsheet.row(x)[9].value,2) if self.is_num(rsheet.row(x)[9].value) else rsheet.row(x)[9].value
			self.prod[sku]['multi'] = rsheet.row(x)[4].value
			self.prod[sku]['img400'] = "brightideas400"
			self.prod[sku]['img160'] = "brightideas160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[3].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "brightideas800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)