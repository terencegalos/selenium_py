from xls_getter import TableData
import datetime

class Hannas_Handiworks():
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
				
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = " ".join(rsheet.row(x)[0].value.split())
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ''#rsheet.row(x)[2].value
			self.prod[sku]['desc'] = ''#rsheet.row(x)[3].value
			self.prod[sku]['stock'] = ''#rsheet.row(x)[4].value
			self.prod[sku]['sale'] = ''#float(rsheet.row(x)[5].value) if self.is_num(rsheet.row(x)[5].value) else rsheet.row(x)[5].value#rsheet.row(x)[4].value.split("/")[1] if rsheet.row(x)[3].value.split("/")[0] == rsheet.row(x)[4].value.split("/")[0] else ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ''#rsheet.row(x)[8].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[3].value.split("/")[0]) if self.is_num(rsheet.row(x)[3].value) else rsheet.row(x)[3].value
			self.prod[sku]['price1'] = float(rsheet.row(x)[3].value.split("/")[1]) if self.is_num(rsheet.row(x)[3].value) else rsheet.row(x)[3].value
			self.prod[sku]['min2'] = float(rsheet.row(x)[4].value.split("/")[0]) if self.is_num(rsheet.row(x)[4].value) else rsheet.row(x)[4].value
			self.prod[sku]['price2'] = float(rsheet.row(x)[4].value.split("/")[1]) if self.is_num(rsheet.row(x)[4].value) else rsheet.row(x)[4].value
			self.prod[sku]['min3'] = float(rsheet.row(x)[5].value.split("/")[0]) if self.is_num(rsheet.row(x)[5].value) else rsheet.row(x)[5].value
			self.prod[sku]['price3'] = float(rsheet.row(x)[5].value.split("/")[1]) if self.is_num(rsheet.row(x)[5].value) else rsheet.row(x)[5].value
			self.prod[sku]['multi'] = float(rsheet.row(x)[3].value.split("/")[0]) if self.is_num(rsheet.row(x)[3].value) else rsheet.row(x)[3].value
			self.prod[sku]['img400'] = "Hannas400"
			self.prod[sku]['img160'] = "Hannas160"
			self.prod[sku]['jpg400'] =""#rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[21].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Hannas800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)