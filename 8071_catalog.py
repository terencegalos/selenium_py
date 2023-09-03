from xls_getter import TableData
import datetime

class Irvins_Tinware():
	prod = {}
	skus = None

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
			
			if rsheet.row(x)[8].value == 0: #skip no price
				continue
				
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = " ".join(rsheet.row(x)[0].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[3].value+"|"+rsheet.row(x)[4].value+"|"+rsheet.row(x)[4].value
			self.prod[sku]['desc'] = rsheet.row(x)[7].value
			self.prod[sku]['stock'] = rsheet.row(x)[9].value
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[6].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[11].value
			self.prod[sku]['price1'] = rsheet.row(x)[8].value
			self.prod[sku]['min2'] = ""#rsheet.row(x)[8].value
			self.prod[sku]['price2'] = ""#rsheet.row(x)[9].value
			self.prod[sku]['min3'] = ""#rsheet.row(x)[10].value
			self.prod[sku]['price3'] = ""#rsheet.row(x)[11].value
			self.prod[sku]['multi'] = rsheet.row(x)[11].value
			self.prod[sku]['img400'] = "Irvins400"
			self.prod[sku]['img160'] = "Irvins160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[10].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[10].value
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[13].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Irvins800"
			self.prod[sku]['jpg800'] = rsheet.row(x)[10].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)