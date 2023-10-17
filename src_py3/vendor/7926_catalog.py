from helper.xls_getter import TableData
import time
import datetime

class Gooseberry_Patch_Cookbooks():
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
		
		stock = "placeholder"
		for x in range(1,rsheet.nrows):
			
			# print rsheet.row(x)
			# skip discontinued or no price
			if "remove" in rsheet.row(x)[12].value.lower() or rsheet.row(x)[10].value == "":
				continue

			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			self.prod[sku] = {}
				
			self.prod[sku]['name'] = rsheet.row(x)[6].value
			# self.prod[sku]['sku'] = "'"+sku
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[13].value + "|"+ rsheet.row(x)[14].value
			self.prod[sku]['desc'] = rsheet.row(x)[15].value
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[8].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1
			self.prod[sku]['price1'] = round(float(rsheet.row(x)[10].value) * 0.5,2)
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1
			self.prod[sku]['img400'] = "Gooseberry400"
			self.prod[sku]['img160'] = "Gooseberry160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[5].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Gooseberry800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			# print self.prod[sku]
			# time.sleep(1)
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)

	def __len__(self):
		return len(self.prod)