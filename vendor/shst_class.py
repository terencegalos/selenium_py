from xls_getter import TableData
					
# SHST Object
class SHST():
	prod = {}
	skus = None
	path = None
	
	def __init__(self,vendor,mode = None,fmt = None):
	
		print "Initializing SHST instance.."
	
		table = TableData(vendor,mode,fmt) #TableData instance
		rsheet = table.getSheet()
		
		for x in range(1,rsheet.nrows):
			# SHST mode
			try: # check if item number looks like an int
				float(rsheet.row(x)[1].value)
				item = str(int(rsheet.row(x)[1].value))
			except:	
				item = " ".join(rsheet.row(x)[1].value.split())
			
			# print rsheet.row(x)
			if rsheet.row(x)[7].value == 0: #check if no price
				print "Skipping."
				continue

			self.prod[item] = {}
			self.prod[item]['name'] = rsheet.row(x)[0].value
			self.prod[item]['sku'] = item
			self.prod[item]['cat'] = rsheet.row(x)[2].value
			self.prod[item]['desc'] = rsheet.row(x)[3].value
			self.prod[item]['stock'] = rsheet.row(x)[4].value
			self.prod[item]['size'] = rsheet.row(x)[5].value
			self.prod[item]['min'] = float(rsheet.row(x)[6].value) if self.is_num(rsheet.row(x)[6].value) else rsheet.row(x)[6].value
			self.prod[item]['price1'] = float(rsheet.row(x)[7].value) if self.is_num(rsheet.row(x)[7].value) else rsheet.row(x)[7].value
			self.prod[item]['min2'] = float(rsheet.row(x)[8].value) if self.is_num(rsheet.row(x)[8].value) else rsheet.row(x)[8].value
			self.prod[item]['price2'] = float(rsheet.row(x)[9].value) if self.is_num(rsheet.row(x)[9].value) else rsheet.row(x)[9].value
			self.prod[item]['min3'] = float(rsheet.row(x)[10].value) if self.is_num(rsheet.row(x)[10].value) else rsheet.row(x)[10].value
			self.prod[item]['price3'] = float(rsheet.row(x)[11].value) if self.is_num(rsheet.row(x)[11].value) else rsheet.row(x)[11].value
			self.prod[item]['multi'] = float(rsheet.row(x)[12].value) if self.is_num(rsheet.row(x)[12].value) else rsheet.row(x)[12].value
			self.prod[item]['jpg800'] = rsheet.row(x)[13].value
			self.prod[item]['minretail'] = float(1)
			self.prod[item]['msrp'] = float(self.prod[item]['price1'] * 2)
			self.prod[item]['sale'] = float(rsheet.row(x)[16].value) if self.is_num(rsheet.row(x)[16].value) else rsheet.row(x)[16].value
			self.prod[item]['ship'] = 14
			self.prod[item]['isactive'] = rsheet.row(x)[18].value
			self.prod[item]['brand'] = " ".join(rsheet.row(x)[19].value.split())
			self.prod[item]['category'] = " ".join(rsheet.row(x)[20].value.split())
			self.prod[item]['opt'] = rsheet.row(x)[21].value
			self.prod[item]['section'] = " ".join(rsheet.row(x)[22].value.split())
			self.prod[item]['desc2'] = rsheet.row(x)[23].value
			self.prod[item]['isImageAvailable'] = rsheet.row(x)[24].value
			self.prod[item]['isUpdateAvailable'] = ""
			# print self.prod[item]
				
				
		self._initialize_skus()
	
	def __str__(self):
		return str("\n".join(self.skus))
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def is_num(self,val):
		try:
			float(val)
			return True
		except:
			return False
			
	def add(self,row):
		item = row['sku']
		self.prod[item] = {}
		self.prod[item]['name'] = row['name']
		self.prod[item]['sku'] = item
		self.prod[item]['cat'] = row['cat']
		self.prod[item]['desc'] = row['desc']
		self.prod[item]['stock'] = row['stock']
		self.prod[item]['size'] = row['size']
		self.prod[item]['min'] = row['min']
		self.prod[item]['price1'] = row['price1']
		self.prod[item]['min2'] = row['min2']
		self.prod[item]['price2'] = row['price2']
		self.prod[item]['min3'] = row['min3']
		self.prod[item]['price3'] = row['price3']
		self.prod[item]['multi'] = row['multi']
		self.prod[item]['jpg800'] = row['jpg800']
		self.prod[item]['minretail'] = row['minretail'] if 'minretail' in row else 1
		self.prod[item]['msrp'] = row['msrp'] if 'msrp' in row else row['price1'] * 2
		self.prod[item]['sale'] = row['sale']
		self.prod[item]['ship'] = row['ship'] if 'ship' in row else self.prod[self.skus[0]]['ship']
		self.prod[item]['isactive'] = row['isactive'] if 'isactive' in row else 1
		self.prod[item]['brand'] = row['brand'] if 'brand' in row else self.prod[self.skus[0]]['brand']
		self.prod[item]['category'] = row['category'] if 'category' in row else ""
		self.prod[item]['opt'] = row['opt']
		self.prod[item]['section'] = row['section'] if 'section' in row else ""
		self.prod[item]['desc2'] = row['desc2'] if 'desc2' in row else ""
		self.prod[item]['isImageAvailable'] = 1 if 'jpg800' in row else 0
		self.prod[item]['isUpdateAvailable'] = "New"
	