from xls_getter import TableData
import datetime
import re

class The_Hearthside_Collection():
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

			# print(rsheet.row(x))
			# if "*" in rsheet.row(x)[1].value: #skip no discontinued
			# 	continue

			if not self.is_num(rsheet.row(x)[4].value) or rsheet.row(x)[4].value == 0: #skip no price1
				continue
				
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = " ".join(rsheet.row(x)[0].value.split())

			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[8].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[0].value
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""#rsheet.row(x)[5].value
			self.prod[sku]['set'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[9].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[3].value#rsheet.row(x)[10].value if self.is_num(rsheet.row(x)[10].value) else rsheet.row(x)[10].value
			self.prod[sku]['price1'] = rsheet.row(x)[4].value#float(rsheet.row(x)[11].value)
			self.prod[sku]['min2'] = rsheet.row(x)[5].value if self.is_num(rsheet.row(x)[5].value) and rsheet.row(x)[5].value != rsheet.row(x)[3].value else ""
			self.prod[sku]['price2'] = float(rsheet.row(x)[6].value) if self.is_num(rsheet.row(x)[6].value) and rsheet.row(x)[6].value != rsheet.row(x)[4].value else ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[3].value
			self.prod[sku]['img400'] = "Hearthside400"
			self.prod[sku]['img160'] = "Hearthside160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[7].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Hearthside800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[8].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)