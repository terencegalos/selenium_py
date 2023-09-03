from xls_getter import TableData
import datetime

class Flags_Galore_Decor():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			if rsheet.row(x)[6].value == 0 or "disc" in rsheet.row(x)[3].value.lower(): #skip no price
				print "Skipping"
				continue

			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "_".join(rsheet.row(x)[1].value.split())
			
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[3].value+"|"+rsheet.row(x)[4].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#'Size:  12.5" X 18'
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 3
			self.prod[sku]['price1'] = rsheet.row(x)[6].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 3
			self.prod[sku]['img400'] = "FlagsGaloreDecor400"
			self.prod[sku]['img160'] = "FlagsGaloreDecor160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[0].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "FlagsGaloreDecor800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)