from helper.xls_getter import TableData
import datetime
import re

class Lifeforce():
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
			
			# print rsheet.row(x)
			# if rsheet.row(x)[1].value == "": #skip no sku
			# 	continue
			
			#skip no price
			# try:
			# 	float(rsheet.row(x)[7].value)
			# 	pass
			# except:
			# 	continue
				
			# if rsheet.row(x)[12].value != 'Y': #skip inactive
			# 	continue

			# if "clearance" not in rsheet.row(x)[9].value.lower(): # skip clearance
			# 	continue
				
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())

				
			self.prod[sku] = {}
			# print rsheet.row(x)
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku.upper()
			self.prod[sku]['cat'] = rsheet.row(x)[2].value
			self.prod[sku]['desc'] = rsheet.row(x)[3].value
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = float(rsheet.row(x)[5].value) if self.is_num(rsheet.row(x)[5].value) else ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[8].value if not isinstance(rsheet.row(x)[8].value,float) else ""
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[10].value)
			
			self.prod[sku]['price1'] = round(float(rsheet.row(x)[11].value),2)				
			self.prod[sku]['min2'] = float(rsheet.row(x)[12].value ) if self.is_num(rsheet.row(x)[12].value) else ""
			self.prod[sku]['price2'] = round(float(rsheet.row(x)[13].value),2) if self.is_num(rsheet.row(x)[13].value) else ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = float(rsheet.row(x)[10].value)
			self.prod[sku]['img400'] = "Lifeforce400"
			self.prod[sku]['img160'] = "Lifeforce160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Lifeforce800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)

	def __len__(self):
		return len(self.prod)