from xls_getter import TableData
import datetime

class Wholesale_Home_decor_Harvest_Scents():
	prod = {}
	skus = None
	disc = False
	
	def is_num(self,num):
		try:
			float(num)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['desc'] = rsheet.row(x)[3].value
			self.prod[sku]['stock'] = rsheet.row(x)[4].value
			self.prod[sku]['sale'] = ""#float(rsheet.row(x)[5].value) if self.is_num(rsheet.row(x)[5].value) else rsheet.row(x)[5].value
			self.prod[sku]['set'] = ""#rsheet.row(x)[6].value
			self.prod[sku]['custom'] = ""#rsheet.row(x)[7].value
			self.prod[sku]['size'] = ""#rsheet.row(x)[8].value
			self.prod[sku]['top'] = ""#rsheet.row(x)[9].value
			self.prod[sku]['min'] = float(rsheet.row(x)[10].value)
			self.prod[sku]['price1'] = float(rsheet.row(x)[11].value)
			self.prod[sku]['min2'] = float(rsheet.row(x)[12].value) if self.is_num(rsheet.row(x)[12].value) else ""
			self.prod[sku]['price2'] = float(rsheet.row(x)[13].value) if self.is_num(rsheet.row(x)[13].value) else ""
			self.prod[sku]['min3'] = float(rsheet.row(x)[14].value) if self.is_num(rsheet.row(x)[14].value) else ""
			self.prod[sku]['price3'] = float(rsheet.row(x)[15].value) if self.is_num(rsheet.row(x)[15].value) else ""
			self.prod[sku]['multi'] = float(rsheet.row(x)[10].value)
			self.prod[sku]['img400'] = "Harv400"
			self.prod[sku]['img160'] = "Harv160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Harv800"
			self.prod[sku]['jpg800'] = rsheet.row(x)[23].value
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)