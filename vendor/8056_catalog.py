from xls_getter import TableData
import datetime

class Special_T_Imports_Closeouts():
	prod = {}
	skus = None
	
	def is_num(self,x):
		try:
			float(x)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			# print rsheet.row(x)
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
			
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku		
			self.prod[sku]['cat'] = ""
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = ""#"In Stock"#"In stock & shipping (checked " + str(datetime.datetime.today().strftime("%b %d")) +")"
			self.prod[sku]['sale'] = round(rsheet.row(x)[9].value,2)
			self.prod[sku]['set'] = rsheet.row(x)[3].value
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#str(rsheet.row(x)[5].value) + " x " + str(rsheet.row(x)[6].value) + " x " + str(rsheet.row(x)[7].value)
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[7].value# if rsheet.row(x)[1].value > 0 else 1
			self.prod[sku]['price1'] = rsheet.row(x)[8].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[7].value# if rsheet.row(x)[1].value > 0 else 1
			self.prod[sku]['img400'] = "specialtimports400"
			self.prod[sku]['img160'] = "specialtimports160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[10].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "specialtimports800"
			self.prod[sku]['jpg800'] = ""
			# print self.prod[sku]
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)