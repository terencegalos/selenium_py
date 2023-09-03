from xls_getter import TableData
import datetime,xlrd

class Adams_and_Company():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			# print rsheet.row(x)
			if not isinstance(rsheet.row(x)[7].value,float): #skip 0 price
				continue

			if 'disc' in rsheet.row(x)[13].value.lower() or 'clearance' in rsheet.row(x)[13].value.lower(): #skip clearance
				continue

			try:
				float(rsheet.row(x)[1].value)	
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[3].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[11].value
			self.prod[sku]['desc'] = ""
			if rsheet.row(x)[8].value > 4:
				self.prod[sku]['stock'] = "In stock & shipping (checked " + str(datetime.datetime.today().strftime("%B %d, %Y")) +")"
				
			else:
				self.prod[sku]['stock'] = "Order to ship after - "+ datetime.datetime(*xlrd.xldate_as_tuple(rsheet.row(x)[9].value,table.getBook().datemode)).strftime('%B %d, %Y') if rsheet.row(x)[9].ctype is 3 else rsheet.row(x)[9].value

			self.prod[sku]['sale'] = ""#rsheet.row(x)[14].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#str(rsheet.row(x)[12].value) + " x " + str(rsheet.row(x)[13].value) + " x " + str(rsheet.row(x)[14].value)
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[5].value
			self.prod[sku]['price1'] = round(rsheet.row(x)[7].value,2)
			self.prod[sku]['min2'] = rsheet.row(x)[6].value if rsheet.row(x)[5].value != rsheet.row(x)[6].value else ""
			self.prod[sku]['price2'] = round((rsheet.row(x)[7].value * .9),2) if rsheet.row(x)[5].value != rsheet.row(x)[6].value else ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[5].value
			self.prod[sku]['img400'] = "Adams400"
			self.prod[sku]['img160'] = "Adams160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[12].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[12].value.split("/")[-1] if rsheet.row(x)[12].ctype is 1 else ""
			self.prod[sku]['desc2'] = rsheet.row(x)[10].value
			self.prod[sku]['opt'] = ""	
			self.prod[sku]['img800'] = "Adams800"
			self.prod[sku]['jpg800'] = rsheet.row(x)[12].value.split("/")[-1] if rsheet.row(x)[12].ctype is 1 else ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)