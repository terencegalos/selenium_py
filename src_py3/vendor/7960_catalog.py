from helper.xls_getter import TableData
import datetime

class Capitol_Discounted_Closeouts():
	prod = {}
	skus = None
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			if rsheet.row(x)[1].value == '':
				continue
				
			sku = "".join(rsheet.row(x)[0].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value + " " + rsheet.row(x)[1].value + " " + rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = "Closeout Price" if rsheet.row(x)[5].value > 3 else "Out of stock"
			self.prod[sku]['sale'] = rsheet.row(x)[4].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[3].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1
			self.prod[sku]['price1'] = rsheet.row(x)[4].value * 2
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1
			self.prod[sku]['img400'] = "Cap 400"
			self.prod[sku]['img160'] = "Cap 160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Cap 800"
			self.prod[sku]['jpg800'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)