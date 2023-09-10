from xls_getter import TableData
					
# Waresitat object
class Waresitat():
	prod = {}
	skus = None

	def __len__(self):
		return len(self.prod)
		
	def is_num(self,num):
		try:
			float(num)
			return True
		except:
			return False
	
	def __init__(self,vendor,mode = None,fmt = None):
	
		table = TableData(vendor,mode,fmt) # instantiate vendor file into an object
		print table.path
		print table.filename
		rsheet = table.getSheet()
		for x in range(rsheet.nrows):
		
			# print rsheet.row(x)
			# catalog mode
			if fmt == "Northlight Seasonal":
				sku = "_".join(rsheet.row(x)[0].value.split())
				
				if rsheet.row(x)[1].value == '':
					continue
					
				print rsheet.row(x)
				self.prod[sku] = {}
				self.prod[sku]['name'] = rsheet.row(x)[1].value
				self.prod[sku]['sku'] = sku
				self.prod[sku]['cat'] = "|".join(rsheet.row(x)[7].value.split("/"))
				self.prod[sku]['desc'] = rsheet.row(x)[10].value
				self.prod[sku]['stock'] = rsheet.row(x)[5].value
				self.prod[sku]['sale'] = ""
				self.prod[sku]['set'] = ""
				self.prod[sku]['custom'] = ""
				self.prod[sku]['size'] = ""
				self.prod[sku]['top'] = ""
				self.prod[sku]['min'] = 1
				self.prod[sku]['price1'] = rsheet.row(x)[3].value
				self.prod[sku]['min2'] = ""
				self.prod[sku]['price2'] = ""
				self.prod[sku]['min3'] = ""
				self.prod[sku]['price3'] = ""
				self.prod[sku]['multi'] = 1
				self.prod[sku]['img400'] = "Northlight400"
				self.prod[sku]['img160'] = "Northlight160"
				self.prod[sku]['jpg400'] = rsheet.row(x)[11].value
				self.prod[sku]['jpg160'] = rsheet.row(x)[11].value.split("/")[-1:]
				self.prod[sku]['desc2'] = ""
				self.prod[sku]['opt'] = ""
				self.prod[sku]['img800'] = "Northlight800"
				self.prod[sku]['jpg800'] = rsheet.row(x)[11].value.split("/")[-1:]
				self.prod[sku]['isUpdateAvailable'] = ""
				
			# waresitat mode
			else:
				# print rsheet.row(x)
				# if rsheet.row(x)[11].value == 0:# check if no price
				# 	continue
				try: # check if item number looks like an int
					float(rsheet.row(x)[1].value)
					sku = str(int(rsheet.row(x)[1].value))
				except:	
					sku = " ".join(rsheet.row(x)[1].value.split())
				
				self.prod[sku] = {}
				self.prod[sku]['name'] = rsheet.row(x)[0].value
				self.prod[sku]['sku'] = sku
				self.prod[sku]['cat'] = rsheet.row(x)[2].value
				self.prod[sku]['desc'] = rsheet.row(x)[3].value
				self.prod[sku]['stock'] = rsheet.row(x)[4].value
				self.prod[sku]['sale'] = round(float(rsheet.row(x)[5].value),2) if self.is_num(rsheet.row(x)[5].value) else rsheet.row(x)[5].value
				self.prod[sku]['set'] = rsheet.row(x)[6].value
				self.prod[sku]['custom'] = rsheet.row(x)[7].value
				self.prod[sku]['size'] = rsheet.row(x)[8].value
				self.prod[sku]['top'] = rsheet.row(x)[9].value
				self.prod[sku]['min'] = float(rsheet.row(x)[10].value) if self.is_num(rsheet.row(x)[10].value) else rsheet.row(x)[10].value
				self.prod[sku]['price1'] = round(float(rsheet.row(x)[11].value),2) if self.is_num(rsheet.row(x)[11].value) else rsheet.row(x)[11].value
				self.prod[sku]['min2'] = float(rsheet.row(x)[12].value) if self.is_num(rsheet.row(x)[12].value) else rsheet.row(x)[12].value
				self.prod[sku]['price2'] = round(float(rsheet.row(x)[13].value),2) if self.is_num(rsheet.row(x)[13].value) else rsheet.row(x)[13].value
				self.prod[sku]['min3'] = float(rsheet.row(x)[14].value) if self.is_num(rsheet.row(x)[14].value) else rsheet.row(x)[14].value
				self.prod[sku]['price3'] = round(float(rsheet.row(x)[15].value),2) if self.is_num(rsheet.row(x)[15].value) else rsheet.row(x)[15].value
				self.prod[sku]['multi'] = float(rsheet.row(x)[16].value) if self.is_num(rsheet.row(x)[16].value) else rsheet.row(x)[16].value
				self.prod[sku]['img400'] = rsheet.row(x)[17].value
				self.prod[sku]['img160'] = rsheet.row(x)[18].value
				self.prod[sku]['jpg400'] = rsheet.row(x)[19].value
				self.prod[sku]['jpg160'] = rsheet.row(x)[20].value
				try:
					self.prod[sku]['desc2'] = rsheet.row(x)[21].value
				except:
					self.prod[sku]['desc2'] = ""
				try:
					self.prod[sku]['opt'] = rsheet.row(x)[22].value
				except:
					self.prod[sku]['opt'] = ""
				try:
					self.prod[sku]['img800'] = rsheet.row(x)[23].value
				except:
					self.prod[sku]['img800'] = ""
				try:
					self.prod[sku]['jpg800'] = rsheet.row(x)[24].value
				except:
					self.prod[sku]['jpg800'] = ""
				
				self.prod[sku]['isUpdateAvailable'] = ""
				#print self.prod[sku]
				
		self._initialize_skus()
	
	def __str__(self):
		return str("\n".join(self.skus))
		
	def _initialize_skus(self):
		# self.skus = [str(sk) for sk in self.prod]
		self.skus = [sk for sk in self.prod]
		
	def add(self,row):
		sku = row['sku']
		self.prod[sku] = {}
		self.prod[sku]['name'] = row['name']
		self.prod[sku]['sku'] = sku
		self.prod[sku]['cat'] = row['cat']
		self.prod[sku]['desc'] = row['desc']
		self.prod[sku]['stock'] = row['stock']
		self.prod[sku]['sale'] = row['sale']
		self.prod[sku]['set'] = row['set']
		self.prod[sku]['custom'] = row['custom']
		self.prod[sku]['size'] = row['size']
		self.prod[sku]['top'] = row['top']
		self.prod[sku]['min'] = row['min']
		self.prod[sku]['price1'] = row['price1']
		self.prod[sku]['min2'] = row['min2']
		self.prod[sku]['price2'] = row['price2']
		self.prod[sku]['min3'] = row['min3']
		self.prod[sku]['price3'] = row['price3']
		self.prod[sku]['multi'] = row['multi']
		self.prod[sku]['img400'] = row['img400']
		self.prod[sku]['img160'] = row['img160']
		self.prod[sku]['jpg400'] = row['jpg400']
		self.prod[sku]['jpg160'] = row['jpg160']
		self.prod[sku]['desc2'] = row['desc2']
		self.prod[sku]['opt'] = row['opt']
		self.prod[sku]['img800'] = row['img800']
		self.prod[sku]['jpg800'] = row['jpg800']
		self.prod[sku]['isUpdateAvailable'] = "New"