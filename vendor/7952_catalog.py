from xls_getter import TableData
import time
import datetime

class DNS_Designs():
	prod = {}
	skus = None
	disc = False
	
	def remWhiteSpace(self,x):
		if self.is_num(x):
			return round(x,2)
		else:
			if len(x) > 0:
				return round(float(str("".join(x.split()))),2)
			else:
				return ""

	def is_num(self,num):
		try:
			float(num)
			return True
		except:
			return False

	def __init__(self,vendor,mode=2):
							
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		stock = "placeholder"
		for x in range(1,rsheet.nrows):
			
			# print rsheet.row(x)[0]
			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
				
			self.prod[sku] = {}
				
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['desc'] = ""#rsheet.row(x)[2].value
			self.prod[sku]['stock'] = ""#rsheet.row(x)[4].value
			self.prod[sku]['sale'] = ""#rsheet.row(x)[4].value
			self.prod[sku]['set'] = ""#rsheet.row(x)[5].value
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = ""#rsheet.row(x)[7].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[2].value
			self.prod[sku]['price1'] = rsheet.row(x)[3].value
			self.prod[sku]['min2'] = rsheet.row(x)[4].value
			self.prod[sku]['price2'] = rsheet.row(x)[5].value
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			
			# tier = ['price1','price2','price3']
			# mins = ['min','min2','min3']
			# counter = 0
			# for i in range(2,len(rsheet.row(x))): #loop pricing row starting from cell with pricing
			# 	if isinstance(rsheet.row(x)[i].value,float):
			# 		self.prod[sku][mins[counter]] = float(rsheet.row(0)[i].value)
			# 		self.prod[sku][tier[counter]] = float(rsheet.row(x)[i].value)
			# 		counter += 1
					

			self.prod[sku]['multi'] = rsheet.row(x)[2].value#self.prod[sku]['min']
			self.prod[sku]['img400'] = "DNS400"
			self.prod[sku]['img160'] = "DNS160"
			self.prod[sku]['jpg400'] = ""#rsheet.row(x)[19].value
			self.prod[sku]['jpg160'] = ""#rsheet.row(x)[20].value
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[29].value
			self.prod[sku]['opt'] = ""#rsheet.row(x)[23].value
			self.prod[sku]['img800'] = "DNS800"
			self.prod[sku]['jpg800'] = ""#rsheet.row(x)[24].value
			self.prod[sku]['isUpdateAvailable'] = ""
			counter = 0
			# print self.prod[sku]
			# time.sleep(1)
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)

	def __len__(self):
		return len(self.prod)