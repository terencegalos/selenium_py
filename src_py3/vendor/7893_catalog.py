from helper.xls_getter import TableData
import datetime
from decimal import Decimal 

class A_Cheerful_Giver():
	prod = {}
	skus = None
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(4,rsheet.nrows):
			
			# print rsheet.row(x)

			# if rsheet.row(x)[3].value == '': # skip no min
			# 	continue
			
			if rsheet.row(x)[0].value == '': # skip empty row
				continue
				
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = " ".join(rsheet.row(x)[0].value.upper().split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[4].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[3].value
			self.prod[sku]['stock'] = ""#"Available "+rsheet.row(x)[8].value
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[6].value)
			TWOPLACES = Decimal(10) ** -2
			self.prod[sku]['price1'] = Decimal(float(rsheet.row(x)[7].value)).quantize(TWOPLACES)
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = float(rsheet.row(x)[6].value)
			self.prod[sku]['img400'] = "ACG400"
			self.prod[sku]['img160'] = "ACG160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[10].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[10].value.split("/")[-1]
			self.prod[sku]['desc2'] = rsheet.row(x)[9].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "ACG800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)