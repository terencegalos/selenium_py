from xls_getter import TableData
import datetime
import re

class Raghu_Home_Collections():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(3,rsheet.nrows):
			
			# print rsheet.row(x)[3]
			if rsheet.row(x)[3].value  == '': #flag on if line reached to closeouts
				self.disc = True
				
			if self.disc == True:
				continue

			if rsheet.row(x)[8].value == '': #skip no image
				continue
				
			sku = "".join(rsheet.row(x)[0].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[1].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = "In stock & shipping (checked " + str(datetime.datetime.today().strftime("%B %d, %Y")) +")" if rsheet.row(x)[5].value > 9 else ("Out of stock" if rsheet.row(x)[1].value.lower() != "fall" or rsheet.row(x)[1].value.lower != "xmas" else "Order now as Prebook")
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			# self.prod[sku]['size'] = "|".join([str(i) for i in re.findall('\d{1,}\w\sx\s\d{1,}\s\w'," ".join(rsheet.row(x)[9].value.split()))])
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
			self.prod[sku]['jpg160'] = rsheet.row(x)[8].value.split("/")[-1:] if "/" in rsheet.row(x)[8].value else ""
			self.prod[sku]['desc2'] = rsheet.row(x)[6].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Raghu800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)