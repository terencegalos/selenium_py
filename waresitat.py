import xlrd,xlwt,csv
					
class Waresitat(): # make Waresitat format from file
	prod = {}
	skus = None
	# f = "WSinventory"
	
	def __init__(self,f,fmt = None):
	
		rbook = xlrd.open_workbook(path+f)
		rsheet = rbook.sheet_by_index(0)
		for x in range(rsheet.nrows):
			# print rsheet.row(x)
			if fmt == "Northlight Seasonal":
				cur = {}
				sku = ("_".join(rsheet.row(x)[0].value.split())).strip()
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
				self.prod[sku]['UPC'] = rsheet.row(x)[2].value
			else:
				try:
					float(rsheet.row(x)[1].value)
					sku = "".join(str(int(rsheet.row(x)[1].value)))
				except:	
					sku = rsheet.row(x)[1].value
				self.prod[sku] = {}
				self.prod[sku]['name'] = rsheet.row(x)[0].value
				self.prod[sku]['sku'] = sku
				self.prod[sku]['cat'] = rsheet.row(x)[2].value
				self.prod[sku]['desc'] = rsheet.row(x)[3].value
				self.prod[sku]['stock'] = rsheet.row(x)[4].value
				self.prod[sku]['sale'] = rsheet.row(x)[5].value
				self.prod[sku]['set'] = rsheet.row(x)[6].value
				self.prod[sku]['custom'] = rsheet.row(x)[7].value
				self.prod[sku]['size'] = rsheet.row(x)[8].value
				self.prod[sku]['top'] = rsheet.row(x)[9].value
				self.prod[sku]['min'] = rsheet.row(x)[10].value
				self.prod[sku]['price1'] = rsheet.row(x)[11].value
				self.prod[sku]['min2'] = rsheet.row(x)[12].value
				self.prod[sku]['price2'] = rsheet.row(x)[13].value
				self.prod[sku]['min3'] = rsheet.row(x)[14].value
				self.prod[sku]['price3'] = rsheet.row(x)[15].value
				self.prod[sku]['multi'] = rsheet.row(x)[16].value
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
				try:
					self.prod[sku]['UPC'] = rsheet.row(x)[25].value
				except:
					self.prod[sku]['UPC'] = ""
				
		self._initialize_skus()
	
	def __str__(self):
		return str("\n".join(self.skus))
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def add(self,row):
		sku = row['sku']
		self.prod[sku]['name'] = row[sku]['name']
		self.prod[row[sku]['sku']]['sku'] = row[sku]['sku']
		self.prod[row[sku]['sku']]['cat'] = row[sku]['cat']
		self.prod[row[sku]['sku']]['desc'] = row[sku]['desc']
		self.prod[row[sku]['sku']]['stock'] = row[sku]['stock']
		self.prod[row[sku]['sku']]['sale'] = row[sku]['sale']
		self.prod[row[sku]['sku']]['set'] = row[sku]['set']
		self.prod[row[sku]['sku']]['custom'] = row[sku]['custom']
		self.prod[row[sku]['sku']]['size'] = row[sku]['size']
		self.prod[row[sku]['sku']]['top'] = row[sku]['top']
		self.prod[row[sku]['sku']]['min'] = row[sku]['min']
		self.prod[row[sku]['sku']]['price1'] = row[sku]['price1']
		self.prod[row[sku]['sku']]['min2'] = row[sku]['min2']
		self.prod[row[sku]['sku']]['price2'] = row[sku]['price2']
		self.prod[row[sku]['sku']]['min3'] = row[sku]['min3']
		self.prod[row[sku]['sku']]['price3'] = row[sku]['price3']
		self.prod[row[sku]['sku']]['multi'] = row[sku]['multi']
		self.prod[row[sku]['sku']]['img400'] = row[sku]['img400']
		self.prod[row[sku]['sku']]['img160'] = row[sku]['img160']
		self.prod[row[sku]['sku']]['jpg400'] = row[sku]['jpg400']
		self.prod[row[sku]['sku']]['jpg160'] = row[sku]['jpg160']
		self.prod[row[sku]['sku']]['desc2'] = row[sku]['desc2']
		self.prod[row[sku]['sku']]['opt'] = row[sku]['opt']
		self.prod[row[sku]['sku']]['img800'] = row[sku]['img800']
		self.prod[row[sku]['sku']]['jpg800'] = row[sku]['jpg800']
		self.prod[row[sku]['sku']]['UPC'] = row[sku]['UPC']
		