from helper.xls_getter import TableData
import datetime
import re

class JanMichaels_Crafts():
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
			# if rsheet.row(x)[9].value == "": #skip no min
			# 	continue
   
   
			if rsheet.row(x)[4].value == "": # skip no sku
				continue
			
			try: #skip no price
				float(rsheet.row(x)[7].value)
				pass
			except:
				continue
				

			# if "clearance" in rsheet.row(x)[0].value.lower(): # skip clearance
			# 	continue
				
			try:
				float(rsheet.row(x)[4].value)
				sku = str(int(rsheet.row(x)[4].value))
			except:
				sku = "".join(rsheet.row(x)[4].value.split())

				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku.upper()
			self.prod[sku]['cat'] = rsheet.row(x)[2].value
			self.prod[sku]['desc'] = rsheet.row(x)[6].value
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""#float(rsheet.row(x)[7].value) if self.is_num(rsheet.row(x)[7].value) else ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#"|".join([i.replace("Wall Decor/Shop by Frame Size","") for i in rsheet.row(x)[9].value.split(";") if "frame size" in i.lower()])
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[9].value) if isinstance(rsheet.row(x)[9].value,float) else 1
			
			self.prod[sku]['price1'] = round(float(rsheet.row(x)[7].value),2)
				
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = float(rsheet.row(x)[9].value) if isinstance(rsheet.row(x)[9].value,float) else 1
			self.prod[sku]['img400'] = "JanMichael400"
			self.prod[sku]['img160'] = "JanMichael160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "JanMichael800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)

	def __len__(self):
		return len(self.prod)