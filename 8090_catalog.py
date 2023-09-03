from xls_getter import TableData
import datetime

class Designs_Combined_Closeouts():
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


			# if float(rsheet.row(x)[11].value) == 0: #check price
			# 	continue

			print rsheet.row(x)[0].value
			print rsheet.row(x)[2].value

			if rsheet.row(x)[3].value < 1: #check availability
				continue

			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			self.prod[sku] = {}
			self.prod[sku]['name'] = " ".join([line.capitalize() for line in rsheet.row(x)[2].value.split()[1:]]).split("List Price")[0]
			self.prod[sku]['sku'] = sku
			self.prod[sku]['cat'] = ""
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = ""
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = rsheet.row(x)[2].value.split("List Price:")[1].split()[5].split("/")[1] if "s/" in rsheet.row(x)[2].value.lower() else ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[2].value.split()[0]
			self.prod[sku]['top'] = ""

			try:
				self.prod[sku]['min'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[4])
				self.prod[sku]['price1'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[2])
			except:
				self.prod[sku]['min'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[4])
				self.prod[sku]['price1'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[2].strip("$"))

			try:
				self.prod[sku]['min2'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[8])
				self.prod[sku]['price2'] =float(rsheet.row(x)[2].value.split("List Price:")[1].split()[6])
				self.prod[sku]['min3'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[12])
				self.prod[sku]['price3'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[10])
			except:
				self.prod[sku]['min2'] = ""
				self.prod[sku]['price2'] = ""
				self.prod[sku]['min3'] = ""
				self.prod[sku]['price3'] = ""


			self.prod[sku]['multi'] = float(rsheet.row(x)[2].value.split("List Price:")[1].split()[4])
			self.prod[sku]['img400'] = "DCI400"
			self.prod[sku]['img160'] = "DCI160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = rsheet.row(x)[1].value
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "DCI800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['isUpdateAvailable'] = ""
			# print self.prod[sku]
			
		self._initialize_skus()
		
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)