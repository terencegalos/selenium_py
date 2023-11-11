from helper.xls_getter import TableData
import time
import datetime

class Zaer_Ltd_International():
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
		
		stock = "placeholder"
		for x in range(2,rsheet.nrows):

			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			
			
			# if rsheet.row(x)[9].ctype != 0:
			# 	continue
				
			self.prod[sku] = {}
				
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""
			self.prod[sku]['desc'] = rsheet.row(x)[11].value
			self.prod[sku]['stock'] = ""#"In stock & shipping (checked " + str(datetime.datetime.today().strftime("%b %d")) +")" if "available" in rsheet.row(x)[10].value.lower() else (rsheet.row(x)[10].value if "sold out" in rsheet.row(x)[10].value.lower() or "low" in rsheet.row(x)[10].value.lower() else "Order to ship after "+ str(rsheet.row(x)[11].value))
			# self.prod[sku]['stock'] = "In stock & shipping (checked " + str(datetime.datetime.today().strftime("%b %d")) +")" if rsheet.row(x)[10].value > 3 else ("Out of stock" if len(str(rsheet.row(x)[12].value)) < 1 else "Order to ship after "+ str(rsheet.row(x)[13].value))
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""#rsheet.row(x)[4].value
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = str(rsheet.row(x)[16].value) + " x " + str(rsheet.row(x)[17].value) + " x " + str(rsheet.row(x)[18].value)
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = rsheet.row(x)[9].value
			self.prod[sku]['price1'] = rsheet.row(x)[2].value
			self.prod[sku]['min2'] = rsheet.row(x)[10].value
			self.prod[sku]['price2'] = round(float(rsheet.row(x)[2].value * .9),2)
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = rsheet.row(x)[9].value
			self.prod[sku]['img400'] = "Zaer400"
			self.prod[sku]['img160'] = "Zaer160"
			self.prod[sku]['jpg400'] = ""

			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""#rsheet.row(x)[6].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Zaer800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			# print self.prod[sku]
			# time.sleep(1)
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)

	def __len__(self):
		return len(self.prod)