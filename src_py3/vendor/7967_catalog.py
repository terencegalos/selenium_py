from helper.xls_getter import TableData
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
		
			# print rsheet.row(x)
			if rsheet.row(x)[4].value == '': # skip no price
				continue

			# if rsheet.row(x)[14].value < 4: #skip sold out
			# 	continue

			if not self.is_num(rsheet.row(x)[3].value):# or not self.is_num(rsheet.row(x)[4].value) or rsheet.row(x)[4].value == 0: #skip no price and qty
				continue

			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[5].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[3].value
			self.prod[sku]['stock'] = "In-Stock: Ships in 1 to 3 days" if rsheet.row(x)[4].value > 3 else "Out of stock"
			self.prod[sku]['sale'] = ""#rsheet.row(x)[5].value
			self.prod[sku]['set'] = ""#rsheet.row(x)[6].value
			self.prod[sku]['custom'] = ""#rsheet.row(x)[7].value
			self.prod[sku]['size'] = ""#str(rsheet.row(x)[8].value) +"l x "+ str(rsheet.row(x)[9].value) +"w x "+ str(rsheet.row(x)[10].value)+"h"
			self.prod[sku]['top'] = ""#rsheet.row(x)[9].value
			self.prod[sku]['min'] = 1#round(rsheet.row(x)[3].value,2)# if self.is_num(rsheet.row(x)[3].value) else rsheet.row(x)[10].value
			self.prod[sku]['price1'] = round(float(rsheet.row(x)[3].value),2)
			self.prod[sku]['min2'] = ""#float(rsheet.row(x)[5].value) if self.is_num(rsheet.row(x)[5].value) else ""
			self.prod[sku]['price2'] = ""#round(float(rsheet.row(x)[6].value),2) if self.is_num(rsheet.row(x)[6].value) and self.is_num(rsheet.row(x)[5].value) else ""
			self.prod[sku]['min3'] = ""#float(rsheet.row(x)[7].value) if self.is_num(rsheet.row(x)[7].value) else ""#float(rsheet.row(x)[14].value) if self.is_num(rsheet.row(x)[14].value) else rsheet.row(x)[14].value
			self.prod[sku]['price3'] = ""#round(float(rsheet.row(x)[8].value),2) if self.is_num(rsheet.row(x)[8].value) and self.is_num(rsheet.row(x)[7].value) else ""
			self.prod[sku]['multi'] = 1#round(rsheet.row(x)[3].value,2)# if self.is_num(rsheet.row(x)[16].value) else rsheet.row(x)[16].value
			self.prod[sku]['img400'] = "Ragon400"
			self.prod[sku]['img160'] = "Ragon160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[5].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[5].value.split("/")[-1]
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[9].value
			self.prod[sku]['opt'] = ""#rsheet.row(x)[22].value
			self.prod[sku]['img800'] = "Ragon800"
			self.prod[sku]['jpg800'] = rsheet.row(x)[5].value.split("/")[-1]
			self.prod[sku]['isUpdateAvailable'] = ""
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)