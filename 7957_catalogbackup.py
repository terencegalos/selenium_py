from xls_getter import TableData
import datetime

class Adams_Co_Closeouts():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			if rsheet.row(x)[7].value > 0:
				if 'disc' in rsheet.row(x)[10].value.lower() or 'clearance' in rsheet.row(x)[10].value.lower():
					if rsheet.row(x)[7].value < 5: #skip less than 5 inventory
						continue

					try:
						float(rsheet.row(x)[1].value)
						sku = str(int(rsheet.row(x)[1].value))
					except:
						sku = "".join(rsheet.row(x)[1].value.split())
						
					self.prod[sku] = {}
					self.prod[sku]['name'] = rsheet.row(x)[3].value
					self.prod[sku]['sku'] = sku
					self.prod[sku]['cat'] = ""
					self.prod[sku]['desc'] = ""
					self.prod[sku]['stock'] = "Closeout price"
					self.prod[sku]['sale'] = rsheet.row(x)[6].value
					self.prod[sku]['set'] = ""
					self.prod[sku]['custom'] = ""
					self.prod[sku]['size'] = ""
					self.prod[sku]['top'] = ""
					self.prod[sku]['min'] = rsheet.row(x)[4].value
					self.prod[sku]['price1'] = rsheet.row(x)[6].value * 2
					self.prod[sku]['min2'] = rsheet.row(x)[5].value if rsheet.row(x)[4].value != rsheet.row(x)[5].value else ""
					self.prod[sku]['price2'] = (rsheet.row(x)[6].value * 2 *.9) if rsheet.row(x)[5].value != rsheet.row(x)[4].value else ""
					self.prod[sku]['min3'] = ""
					self.prod[sku]['price3'] = ""
					self.prod[sku]['multi'] = rsheet.row(x)[4].value
					self.prod[sku]['img400'] = "Adams400"
					self.prod[sku]['img160'] = "Adams160"
					self.prod[sku]['jpg400'] = ""
					self.prod[sku]['jpg160'] = ""
					self.prod[sku]['desc2'] = rsheet.row(x)[9].value
					self.prod[sku]['opt'] = ""
					self.prod[sku]['img800'] = "Adams800"
					self.prod[sku]['jpg800'] = ""
					self.prod[sku]['isUpdateAvailable'] = ""
					
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)