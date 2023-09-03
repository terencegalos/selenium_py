from xls_getter import TableData
import datetime

class Ragon_House_Collection():
	prod = {}
	skus = None
	disc = False
	
	def is_num(self,num):
		try:
			float(num)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
		

			if "no" in rsheet.row(x)[9].value.lower(): #skip if not available
				continue
				
			if not self.is_num(rsheet.row(x)[4].value) or not self.is_num(rsheet.row(x)[3].value) or rsheet.row(x)[3].value == 0: #skip no price and qty
				continue

			if isinstance(rsheet.row(x)[3].value,str) and rsheet.row(x)[3] == "": #skip emtpy minimum/price
				continue

			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[2].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[0].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = "In stock & shipping (checked " + str(datetime.datetime.today().strftime("%b %d")) +")"
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#rsheet.row(x)[11].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = round(float(rsheet.row(x)[3].value),2)
			self.prod[sku]['price1'] = round(float(rsheet.row(x)[4].value),2)
			self.prod[sku]['min2'] = rsheet.row(x)[5].value
			self.prod[sku]['price2'] = round(float(rsheet.row(x)[6].value),2)
			self.prod[sku]['min3'] = rsheet.row(x)[7].value
			self.prod[sku]['price3'] = round(float(rsheet.row(x)[8].value),2)
			self.prod[sku]['multi'] = rsheet.row(x)[3].value
			self.prod[sku]['img400'] = "Ragon400"
			self.prod[sku]['img160'] = "Ragon160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[11].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Ragon800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)