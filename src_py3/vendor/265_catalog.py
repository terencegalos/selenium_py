from helper.xls_getter import TableData
import datetime

class Wholesale_Home_decor_Harvest_Scents():
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
			
			# print rsheet.row(x)
			# if not self.is_num(rsheet.row(x)[8].value):
			# 	continue

			if rsheet.row(x)[1].value == '':
				continue
				
			sku = "".join(rsheet.row(x)[1].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""
			self.prod[sku]['desc'] = rsheet.row(x)[3].value
			self.prod[sku]['stock'] = rsheet.row(x)[4].value
			self.prod[sku]['sale'] = rsheet.row(x)[5].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[8].value #" x ".join([str(c.value) for c in rsheet.row(x)[13:15]])
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[10].value) if self.is_num(rsheet.row(x)[10].value) else 1
			self.prod[sku]['price1'] = float(rsheet.row(x)[11].value)
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = self.prod[sku]['min']
			self.prod[sku]['img400'] = "Harv400"
			self.prod[sku]['img160'] = "Harv160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[20].value.split("/")[-1]
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Harv800"
			self.prod[sku]['jpg800'] = rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)