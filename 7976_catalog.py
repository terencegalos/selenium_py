from xls_getter import TableData
import datetime

class Brazos_Walking_Sticks():
	prod = {}
	skus = None
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			if rsheet.row(x)[6].value == '':
				continue
				
			sku = rsheet.row(x)[3].value
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[4].value.strip()
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1
			self.prod[sku]['price1'] = rsheet.row(x)[6].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1
			self.prod[sku]['img400'] = "Brazos400"
			self.prod[sku]['img160'] = "Brazos160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Brazos800"
			self.prod[sku]['jpg800'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)