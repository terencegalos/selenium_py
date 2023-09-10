from xls_getter import TableData
import time
import datetime

class ELC_Designs_Group():
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
		for x in range(rsheet.nrows):
			
			if not self.is_num(rsheet.row(x)[4].value): #skip no price
				continue

			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			
			try: # detect price
				float(rsheet.row(x)[4].value)
			except:
				print "Skipping no price."
				continue
			
			# if rsheet.row(x)[9].ctype != 0:
			# 	continue
				
			self.prod[sku] = {}
				
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[2].value + "|" + rsheet.row(x)[7].value
			self.prod[sku]['desc'] = ""	
			self.prod[sku]['stock'] = ""#rsheet.row(x)[6].value
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""#rsheet.row(x)[4].value
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#rsheet.row(x)[6].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[3].value
			self.prod[sku]['price1'] = rsheet.row(x)[4].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[3].value
			self.prod[sku]['img400'] = "ELC400"
			self.prod[sku]['img160'] = "ELC160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[2].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "ELC400"
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