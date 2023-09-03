from xls_getter import TableData
import datetime

class Wild_Wings():
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
		
		for x in range(3,rsheet.nrows):
			
			# if rsheet.row(x)[5].value == 0: #skip no price
			# 	continue

			if "disc" in rsheet.row(x)[6].value.lower(): #skip no stock
				continue
				
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = " ".join(rsheet.row(x)[0].value.split())

			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[9].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[3].value
			self.prod[sku]['stock'] = ""#"Currently In Stock" if rsheet.row(x)[4].value > 3 else "Out of stock"
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#rsheet.row(x)[8].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1#rsheet.row(x)[10].value
			self.prod[sku]['price1'] = float(rsheet.row(x)[3].value)
			self.prod[sku]['min2'] = ""#rsheet.row(x)[12].value
			self.prod[sku]['price2'] = ""#round(rsheet.row(x)[13].value * .8,2) if self.is_num(rsheet.row(x)[13].value) else ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1#rsheet.row(x)[16].value
			self.prod[sku]['img400'] = "wildwings400"
			self.prod[sku]['img160'] = "wildwings160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "wildwings800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)