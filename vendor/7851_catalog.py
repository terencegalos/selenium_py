from xls_getter import TableData
import time
import datetime

class Artistic_Reflections():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
							
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		stock = "placeholder"
		for x in range(1,rsheet.nrows):
			
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			self.prod[sku] = {}
				
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['desc'] = rsheet.row(x)[2].value
			self.prod[sku]['stock'] = ""#"In stock & shipping (checked " + str(datetime.datetime.today().strftime("%b %d")) +")" if "-" not in rsheet.row(x)[9].value else "Out of stock - order to ship after "+ " ".join(rsheet.row(x)[9].value.split("-"))
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#rsheet.row(x)[9].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[5].value
			self.prod[sku]['price1'] = rsheet.row(x)[3].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[5].value
			self.prod[sku]['img400'] = "NorthAmerican400"
			self.prod[sku]['img160'] = "NorthAmerican160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[1].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[1].value
			self.prod[sku]['desc2'] = rsheet.row(x)[3].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "NorthAmerican800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)