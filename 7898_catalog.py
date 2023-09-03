from xls_getter import TableData
import datetime

class KMI_International():
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
			
			sku = rsheet.row(x)[2].value
			# print rsheet.row(x)
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[4].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[1].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = rsheet.row(x)[0].value if len(rsheet.row(x)[0].value) > 1 else "In Stock & Shipping"
			self.prod[sku]['sale'] = round(float(rsheet.row(x)[5].value),2) if self.is_num(rsheet.row(x)[5].value) else rsheet.row(x)[5].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[7].value)
			self.prod[sku]['price1'] = float(rsheet.row(x)[6].value)
			self.prod[sku]['min2'] = float(rsheet.row(x)[9].value) if self.is_num(rsheet.row(x)[9].value) else rsheet.row(x)[9].value
			self.prod[sku]['price2'] = round(float(rsheet.row(x)[8].value),2) if self.is_num(rsheet.row(x)[8].value) else rsheet.row(x)[8].value
			self.prod[sku]['min3'] = float(rsheet.row(x)[11].value) if self.is_num(rsheet.row(x)[11].value) else rsheet.row(x)[11].value
			self.prod[sku]['price3'] = round(float(rsheet.row(x)[10].value),2) if self.is_num(rsheet.row(x)[10].value) else rsheet.row(x)[10].value
			self.prod[sku]['multi'] = float(rsheet.row(x)[7].value)
			self.prod[sku]['img400'] = "KMI400"
			self.prod[sku]['img160'] = "KMI160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[13].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "KMI800"
			self.prod[sku]['jpg800'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)