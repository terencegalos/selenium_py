from xls_getter import TableData
import datetime

class Adams_and_Company():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			if rsheet.row(x)[6].value == 0: #skip 0 price
				continue

			if 'disc' in rsheet.row(x)[10].value.lower() or 'clearance' in rsheet.row(x)[10].value.lower(): #skip clearance
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
			if rsheet.row(x)[7].value > 4:
				# if 'active' in rsheet.row(x)[10].value.lower():
				try:
					self.prod[sku]['stock'] = "In stock & shipping (checked "+str(datetime.datetime.today().strftime("%b %d"))+")"
				except:
					self.prod[sku]['stock'] = rsheet.row(x)[8].value
				# elif 'disc' in rsheet.row(x)[10].value.lower():
				# 	continue
				# else:
				# 	self.prod[sku]['stock'] = rsheet.row(x)[8].value
			# else:
			# 	if 'active' in rsheet.row(x)[10].value.lower():
			# 		try:
			# 			self.prod[sku]['stock'] = "Out of stock - order to ship after " + str(datetime.datetime(int(rsheet.row(x)[11].value.split("-")[2]),int(rsheet.row(x)[11].value.split("-")[0]),int(rsheet.row(x)[11].value.split("-")[1])).strftime("%b %d"))
			# 		except:
			# 			self.prod[sku]['stock'] = rsheet.row(x)[8].value
			# 	else:
			# 		self.prod[sku]['stock'] = rsheet.row(x)[10].value
			
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[4].value
			self.prod[sku]['price1'] = rsheet.row(x)[6].value
			self.prod[sku]['min2'] = rsheet.row(x)[5].value if rsheet.row(x)[4].value != rsheet.row(x)[5].value else ""
			self.prod[sku]['price2'] = (rsheet.row(x)[6].value * .9) if rsheet.row(x)[4].value != rsheet.row(x)[5].value else ""
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