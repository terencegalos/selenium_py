from xls_getter import TableData
import datetime

class Primitives_at_Crow_Hollow():
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
			
			# if rsheet.row(x)[3].value  == '':
			# 	self.disc = True
				
			# if self.disc == True:
			# 	continue
				
			sku = rsheet.row(x)[1].value
			
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku 
			self.prod[sku]['cat'] = rsheet.row(x)[2].value
			self.prod[sku]['desc'] = rsheet.row(x)[3].value
			self.prod[sku]['stock'] = rsheet.row(x)[4].value
			self.prod[sku]['sale'] = rsheet.row(x)[5].value
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[8].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = float(rsheet.row(x)[10].value) if self.is_num(rsheet.row(x)[10].value) else rsheet.row(x)[10].value
			self.prod[sku]['price1'] = float(rsheet.row(x)[11].value)/2 if self.is_num(rsheet.row(x)[11].value) else rsheet.row(x)[11].value/2
			self.prod[sku]['min2'] = float(rsheet.row(x)[12].value) if self.is_num(rsheet.row(x)[12].value) else rsheet.row(x)[12].value
			self.prod[sku]['price2'] = float(rsheet.row(x)[13].value) if self.is_num(rsheet.row(x)[13].value) else rsheet.row(x)[13].value
			self.prod[sku]['min3'] = float(rsheet.row(x)[14].value) if self.is_num(rsheet.row(x)[14].value) else rsheet.row(x)[14].value
			self.prod[sku]['price3'] = float(rsheet.row(x)[15].value) if self.is_num(rsheet.row(x)[15].value) else rsheet.row(x)[15].value
			self.prod[sku]['multi'] = float(rsheet.row(x)[16].value) if self.is_num(rsheet.row(x)[16].value) else rsheet.row(x)[16].value
			self.prod[sku]['img400'] = "PrimitiveCrow400"
			self.prod[sku]['img160'] = "PrimitiveCrow160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[12].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "PrimitiveCrow800"
			self.prod[sku]['jpg800'] = rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)