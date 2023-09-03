from xls_getter import TableData
import datetime

class Home_Collections_by_Raghu_Closeouts():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(3,rsheet.nrows):
			
			if rsheet.row(x)[3].value == '':
				self.disc = True
			
			if self.disc is True and rsheet.row(x)[5].value < 10:
				continue
			elif self.disc is True:
				try:
					if rsheet.row(x)[8].value == '': #skip no image
						continue
					float(rsheet.row(x)[3].value)
					sku = "".join(rsheet.row(x)[0].value.split())
					self.prod[sku] = {}
					self.prod[sku]['name'] = rsheet.row(x)[2].value
					self.prod[sku]['sku'] = sku
					self.prod[sku]['cat'] = rsheet.row(x)[1].value
					self.prod[sku]['desc'] = ""
					self.prod[sku]['stock'] = "In stock while supply lasts"
					self.prod[sku]['sale'] = rsheet.row(x)[3].value * .5
					self.prod[sku]['set'] = ""
					self.prod[sku]['custom'] = ""
					self.prod[sku]['size'] = ""
					self.prod[sku]['top'] = ""
					self.prod[sku]['min'] = rsheet.row(x)[4].value
					self.prod[sku]['price1'] = rsheet.row(x)[3].value
					self.prod[sku]['min2'] = ""
					self.prod[sku]['price2'] = ""
					self.prod[sku]['min3'] = ""
					self.prod[sku]['price3'] = ""
					self.prod[sku]['multi'] = rsheet.row(x)[4].value
					self.prod[sku]['img400'] = "Raghu400"
					self.prod[sku]['img160'] = "Raghu160"
					self.prod[sku]['jpg400'] = rsheet.row(x)[8].value
					self.prod[sku]['jpg160'] = "".join(rsheet.row(x)[8].value.split("/")[-1:]) if "/" in rsheet.row(x)[8].value else ""
					self.prod[sku]['desc2'] = rsheet.row(x)[6].value
					self.prod[sku]['opt'] = ""
					self.prod[sku]['img800'] = "Raghu800"
					self.prod[sku]['jpg800'] = ""
					self.prod[sku]['isUpdateAvailable'] = ""
				except:
					continue
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)