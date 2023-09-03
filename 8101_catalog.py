from xls_getter import TableData
import datetime
import re

class Valley_Wholesale_Products():
	prod = {}
	skus = None
	disc = False
	
	def is_num(self,x):
		try:
			float(x)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
							
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(3,rsheet.nrows):
			
			# print rsheet.row(x)

			if rsheet.row(x)[2].value == 0: # skip no price
				continue
			
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[5].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[3].value
			self.prod[sku]['stock'] = ""#"Avail"+ re.split("avail",rsheet.row(x)[1].value.lower(),re.I)[1].title() if "avail" in rsheet.row(x)[1].value.lower() else ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[2].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[4].value#re.split("min",rsheet.row(x)[4].value.lower(),re.I)[1] if "min" in rsheet.row(x)[4].value.lower() else 1
			self.prod[sku]['price1'] = rsheet.row(x)[3].value#float(rsheet.row(x)[3].value)
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[4].value#re.split("min",rsheet.row(x)[4].value.lower(),re.I)[1] if "min" in rsheet.row(x)[4].value.lower() else 1
			self.prod[sku]['img400'] = "Valley400"
			self.prod[sku]['img160'] = "Valley160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = 	"Valley800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)