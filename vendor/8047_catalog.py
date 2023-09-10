from xls_getter import TableData
import datetime

class VIP_International_Home_Garden():
	prod = {}
	skus = None
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(2,rsheet.nrows):
			
			# print rsheet.row(x)


			if rsheet.row(x)[5].value == 'DISCONTINUED':
				continue
				
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = " ".join(rsheet.row(x)[1].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[13].value+"|"+rsheet.row(x)[14].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = "In stock" if rsheet.row(x)[6].value > 3 else ("Available "+rsheet.row(x)[50].value if rsheet.row(x)[50].value != "" else "Out of stock")
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[24].value#str(rsheet.row(x)[3].value) + " x " + str(rsheet.row(x)[4].value) + " x " + str(rsheet.row(x)[5].value)
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 2#float(rsheet.row(x)[7].value)
			self.prod[sku]['price1'] = float(rsheet.row(x)[4].value)
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 2#float(rsheet.row(x)[7].value)
			self.prod[sku]['img400'] = "VIP400"
			self.prod[sku]['img160'] = "VIP160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[3].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "VIP800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)