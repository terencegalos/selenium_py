## -*- coding: latin-1 -*-
from xls_getter import TableData
import datetime

class Homespice_Decor_Closeouts():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		print rsheet.nrows

		for x in range(1,rsheet.nrows):			
			
			# print x

			if "y" not in rsheet.row(x)[28].value.lower(): #skip closeouts
				continue

			if rsheet.row(x)[1].value == '': #skip emtpy row
				continue
				
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())

			# print rsheet.row(x)
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[6].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[4].value
			self.prod[sku]['desc'] = rsheet.row(x)[19].value
			self.prod[sku]['stock'] = ""#rsheet.row(x)[52].value
			self.prod[sku]['sale'] = rsheet.row(x)[7].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[13].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[12].value
			self.prod[sku]['price1'] = rsheet.row(x)[7].value * 2
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[12].value
			self.prod[sku]['img400'] = "Homespice400"
			self.prod[sku]['img160'] = "Homespice160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[40].value if "/" in rsheet.row(x)[40].value else rsheet.row(x)[41].value
			self.prod[sku]['jpg160'] = self.prod[sku]['jpg400'].split("/")[-1:]
			self.prod[sku]['desc2'] = rsheet.row(x)[29].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Homespice800"
			self.prod[sku]['jpg800'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)