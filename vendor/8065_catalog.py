from xls_getter import TableData
import datetime

class Primitives_by_Kathy_50_Off_Closeouts():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			if rsheet.row(x)[5].value == 0: #skip 0 price
				continue

			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				continue
			if "http" not in str(rsheet.row(x)[7].value):
				continue
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[2].value
			self.prod[sku]['desc'] = rsheet.row(x)[3].value
			self.prod[sku]['stock'] = "In stock"
			self.prod[sku]['sale'] = rsheet.row(x)[6].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[9].value
			self.prod[sku]['size'] = rsheet.row(x)[9].value
			self.prod[sku]['size'] = rsheet.row(x)[9].value
			self.prod[sku]['size'] = rsheet.row(x)[9].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[4].value
			self.prod[sku]['price1'] = rsheet.row(x)[5].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[4].value
			self.prod[sku]['img400'] = "PBK400"
			self.prod[sku]['img160'] = "PBK160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[7].value
			self.prod[sku]['jpg160'] = "".join(rsheet.row(x)[7].value.split("/")[-1:]) if "/" in rsheet.row(x)[7].value else ""
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "PBK800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)