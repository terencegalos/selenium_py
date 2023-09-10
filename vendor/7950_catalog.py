from xls_getter import TableData
import datetime

class Impressions_on_Market():
	prod = {}
	skus = None
	disc = False
	
	def __init__(self,vendor,mode=2):
		
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			
			# sku = " ".join(rsheet.row(x)[1].value.split())

			# sku = " ".join(rsheet.row(x)[1].value.split())
			try:
				float(rsheet.row(x)[1].value)
				sku = str(int(rsheet.row(x)[1].value))
			except:
				sku = "".join(rsheet.row(x)[1].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = rsheet.row(x)[0].value
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = rsheet.row(x)[19].value
			self.prod[sku]['desc'] = rsheet.row(x)[2].value
			self.prod[sku]['stock'] = rsheet.row(x)[3].value
			self.prod[sku]['sale'] = ""#rsheet.row(x)[16].value
			self.prod[sku]['set'] = ""#rsheet.row(x)[6].value
			self.prod[sku]['custom'] = ""#rsheet.row(x)[7].value
			self.prod[sku]['size'] = rsheet.row(x)[4].value
			self.prod[sku]['top'] = ""#rsheet.row(x)[9].value
			self.prod[sku]['min'] = rsheet.row(x)[5].value
			self.prod[sku]['price1'] = rsheet.row(x)[6].value
			self.prod[sku]['min2'] = ""#rsheet.row(x)[12].value
			self.prod[sku]['price2'] = ""#rsheet.row(x)[13].value if isinstance(rsheet.row(x)[13].value,float) else ""
			self.prod[sku]['min3'] = ""#rsheet.row(x)[14].value
			self.prod[sku]['price3'] = ""#rsheet.row(x)[15].value if isinstance(rsheet.row(x)[15].value,float) else ""
			self.prod[sku]['multi'] = rsheet.row(x)[11].value
			self.prod[sku]['img400'] = "Impressions400"
			self.prod[sku]['img160'] = "Impressions160"
			self.prod[sku]['jpg400'] = rsheet.row(x)[13].value
			self.prod[sku]['jpg160'] = rsheet.row(x)[13].value
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = rsheet.row(x)[21].value
			self.prod[sku]['img800'] = "Impressions800"
			self.prod[sku]['jpg800'] = rsheet.row(x)[13].value
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)