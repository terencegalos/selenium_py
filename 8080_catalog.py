from xls_getter import TableData
import datetime

class Christian_Art_Gifts():
	prod = {}
	skus = None
	
	def is_num(self,num):
		try:
			float(num)
			return True
		except:
			return False

	def is_num(self,x):
		try:
			float(x)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(2,rsheet.nrows):
			
			# if not self.is_num(rsheet.row(x)[8].value):
			# 	continue

			# if rsheet.row(x)[1].value == '':
			# 	continue
				
			sku = "".join(rsheet.row(x)[1].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[3].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[0].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[0].value
			self.prod[sku]['stock'] = ""#"In stock & shipping (checked "+str(datetime.datetime.today().strftime("%b %d"))+")" if rsheet.row(x)[4].value > 4 else ("Out of stock - order to ship after " + " ".join(rsheet.row(0)[6].value.split()[-2:]) if rsheet.row(x)[6].value > 0 else "Out of stock")
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[4].value)
			self.prod[sku]['price1'] = round(float(rsheet.row(x)[6].value),2) if self.is_num(rsheet.row(x)[6].value) else rsheet.row(x)[6].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = float(rsheet.row(x)[4].value)
			self.prod[sku]['img400'] = "ChristianArt400"
			self.prod[sku]['img160'] = "ChristianArt160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[10].value
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[2].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "ChristianArt800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)