from xls_getter import TableData
import datetime

class Mullberry_Home_Wholesale():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(3,rsheet.nrows):
		
			# if rsheet.row(x)[43].value < 5: # skip less than 4 inventory
			# 	continue
			if rsheet.row(x)[4].value == 0: # skip no price
				continue
				
			if rsheet.row(x)[1].value == "": # skip no sku
				continue
			
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[5].value + "|" + rsheet.row(x)[6].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1
			self.prod[sku]['price1'] = float(rsheet.row(x)[4].value)
			self.prod[sku]['min2'] =""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1
			self.prod[sku]['img400'] = "Mulberry400"
			self.prod[sku]['img160'] = "Mulberry160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[17].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[17].value.split("/")[-1:]
			self.prod[sku]['desc2'] = rsheet.row(x)[0].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Mulberry800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[17].value.split("/")[-1:]
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)