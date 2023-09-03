from xls_getter import TableData
import datetime
import re

class Carson_Home_Flags():
	prod = {}
	skus = None
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			if rsheet.row(x)[2].value == 0: # check price
				continue
			if rsheet.row(x)[0].value == '': # check blank line
				continue
				
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = " ".join(rsheet.row(x)[0].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['desc'] = rsheet.row(x)[7].value
			self.prod[sku]['stock'] = ""#rsheet.row(x)[7].value
			self.prod[sku]['sale'] = ""#rsheet.row(x)[4].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = 1 if "name drop" in rsheet.row(x)[1].value.lower() else ""
			self.prod[sku]['size'] = ""
			# self.prod[sku]['size'] = " x ".join(re.split('\n',rsheet.row(x)[9].value)[-2:])
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[3].value
			self.prod[sku]['price1'] = rsheet.row(x)[2].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[4].value
			self.prod[sku]['img400'] = "Carson400"
			self.prod[sku]['img160'] = "Carson160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = rsheet.row(x)[5].value
			self.prod[sku]['opt'] = ""#rsheet.row(x)[22].value
			self.prod[sku]['img800'] = "Carson800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)