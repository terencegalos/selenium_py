from helper.xls_getter import TableData
import datetime

class The_Country_House_Collection():
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
		for x in range(6,rsheet.nrows):
			
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			
			if not self.is_num(rsheet.row(x)[3].value): # skip no price
				continue
			
			if "+" in rsheet.row(x)[2].value: # skip closeouts
				continue
				
			self.prod[sku] = {}
				
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""
			self.prod[sku]['desc'] = ""
			# self.prod[sku]['stock'] = "In stock & shipping (checked " + str(datetime.datetime.today().strftime("%b %d")) +")" if rsheet.row(x)[9].value > 10 else "Out of stock"
			self.prod[sku]['stock'] = "In stock & shipping (checked " + str(datetime.datetime.today().strftime("%b %d")) +")"
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[5].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[4].value
			self.prod[sku]['price1'] = rsheet.row(x)[3].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[4].value
			self.prod[sku]['img400'] = "TheCountryHouse400"
			self.prod[sku]['img160'] = "TheCountryHouse160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[6].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "TheCountryHouse800"
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