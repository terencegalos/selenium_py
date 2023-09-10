from xls_getter import TableData
import time
import datetime

class Albert_Estate_LTD():
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
			
			# print rsheet.row(x)

			if rsheet.row(x)[11].value == 0: #skip 0 price
				continue

			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "_".join(rsheet.row(x)[1].value.split())
			
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[2].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = rsheet.row(x)[4].value
			self.prod[sku]['sale'] = float(rsheet.row(x)[5].value) if self.is_num(rsheet.row(x)[5].value) else ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[8].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[10].value) if self.is_num(rsheet.row(x)[10].value) else rsheet.row(x)[10].value
			self.prod[sku]['price1'] = float(rsheet.row(x)[11].value) if self.is_num(rsheet.row(x)[11].value) else rsheet.row(x)[11].value
			self.prod[sku]['min2'] = ""#float(rsheet.row(x)[12].value) if self.is_num(rsheet.row(x)[12].value) and round(float(rsheet.row(x)[13].value),2) < round(float(rsheet.row(x)[11].value),2) else ""
			self.prod[sku]['price2'] = ""#round(float(rsheet.row(x)[13].value),2) if self.is_num(rsheet.row(x)[13].value) and rsheet.row(x)[13].value != rsheet.row(x)[11].value else ""
			self.prod[sku]['min3'] = ""#float(rsheet.row(x)[14].value) if self.is_num(rsheet.row(x)[14].value) and round(float(rsheet.row(x)[15].value),2) < round(float(rsheet.row(x)[13].value),2) else "
			self.prod[sku]['price3'] = ""#float(rsheet.row(x)[15].value) if self.is_num(rsheet.row(x)[15].value) and rsheet.row(x)[15].value != rsheet.row(x)[13].value else ""
			self.prod[sku]['multi'] = float(rsheet.row(x)[16].value) if self.is_num(rsheet.row(x)[16].value) else rsheet.row(x)[16].value
			self.prod[sku]['img400'] = "Albert400"
			self.prod[sku]['img160'] = "Albert160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Albert800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)

	def __len__(self):
		return len(self.prod)