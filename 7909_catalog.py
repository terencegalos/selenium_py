from xls_getter import TableData
import time
import datetime

class North_Country_Wind_Bells():
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
			
			print rsheet.row(x)
			if not self.is_num(rsheet.row(x)[3].value): #skip no price
				continue

			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			
			# if rsheet.row(x)[9].ctype != 0:
			# 	continue
				
			self.prod[sku] = {}
				
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[5].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[8].value
			self.prod[sku]['stock'] = rsheet.row(x)[4].value
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""#rsheet.row(x)[4].value
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#str(rsheet.row(x)[5].value) + " x " + str(rsheet.row(x)[6].value) + " x " + str(rsheet.row(x)[7].value)
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1#rsheet.row(x)[1].value
			self.prod[sku]['price1'] = rsheet.row(x)[3].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1#rsheet.row(x)[4].value
			self.prod[sku]['img400'] = "Northcountry400"
			self.prod[sku]['img160'] = "Northcountry160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[11].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[11].value.split("/")[-1]
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[6].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Northcountry800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[11].value.split("/")[-1]
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