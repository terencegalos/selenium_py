from xls_getter import TableData
import datetime

class Northlight_Seasonal():
	prod = {}
	skus = None
	
	def is_num(self,x):
		try:
			float(x)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
				
			if rsheet.row(x)[2].value < 4: # check quantity
				continue

			if rsheet.row(x)[3].value == "": #skip missimg images
				continue

			if self.is_num(rsheet.row(x)[4].value) and float(rsheet.row(x)[4].value) == 0: #skip no price
				continue
			
			sku = "_".join(rsheet.row(x)[1].value.split())
			
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#"|".join(rsheet.row(x)[26].value.split("/"))
			self.prod[sku]['desc'] = ""#rsheet.row(x)[5].value
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1
			self.prod[sku]['price1'] = rsheet.row(x)[4].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1
			self.prod[sku]['img400'] = "northlight400"
			self.prod[sku]['img160'] = "northlight160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[3].value if rsheet.row(x)[3].value != "" else rsheet.row(x)[3].value
			self.prod[sku]['jpg160'] = self.prod[sku]['jpg400'].split("/")[-1]
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[12].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "northlight800"
			self.prod[sku]['jpg800'] = self.prod[sku]['jpg400'].split("/")[-1]
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)