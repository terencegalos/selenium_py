from helper.xls_getter import TableData
import xlrd
import datetime

class Audreys_Your_Hearts_Delight():

	def __init__(self,vendor,mode=2):

		self.prod = {}
		self.skus = None
		self.disc = False
							
		table = TableData(vendor,mode) # instantiate vendor file into an object
		rsheet = table.getSheet()
		
		stock = "placeholder"
		for x in range(rsheet.nrows):
			
			print(rsheet.row(x))
			if not self.is_num(rsheet.row(x)[5].value): #skip no price
				continue

			try:
				float(rsheet.row(x)[0].value)
				sku = str(int(rsheet.row(x)[0].value))
			except ValueError:
				sku = "".join(rsheet.row(x)[0].value.split())
				
			
			try: # detect price
				float(rsheet.row(x)[5].value)
			except ValueError:
				print("Skipping no price.")
				continue
			

			self.prod[sku] = {
                'name': rsheet.row(x)[2].value,
                'sku': sku,
                'cat': '',
                'desc': rsheet.row(x)[1].value,
                'stock': "In stock & shipping (checked " + str(datetime.datetime.today().strftime("%B %d, %Y")) +")" if "available" in rsheet.row(x)[10].value.lower() else ("Low inventory - expected " + datetime.datetime(*xlrd.xldate_as_tuple(rsheet.row(x)[9].value,table.getBook().datemode)).strftime('%B %d, %Y') if "low"  in rsheet.row(x)[10].value.lower() and rsheet.row(x)[9].value > 1 else ("Out of stock - order to ship after "+datetime.datetime(*xlrd.xldate_as_tuple(rsheet.row(x)[9].value,table.getBook().datemode)).strftime('%B %d, %Y') ) if isinstance(rsheet.row(x)[9].value,float) and "no stock" in rsheet.row(x)[10].value.lower() else rsheet.row(x)[10].value),
                'sale': '',
                'set': rsheet.row(x)[4].value,
                'custom': '',
                'size': rsheet.row(x)[3].value,
                'top': '',
                'min': 1,
                'price1': rsheet.row(x)[5].value,
                'min2': '',
                'price2': '',
                'min3': '',
                'price3': '',
                'multi': 1,
                'img400': 'Audreys400a',
                'img160': 'Audreys160',
                'jpg400': '',
                'jpg160': '',
                'desc2': rsheet.row(x)[6].value,
                'opt': '',
                'img800': 'Audreys800',
                'jpg800': '',
                'isUpdateAvailable': '',
            }
			
		self._initialize_skus()
	
	def is_num(self,num):
		try:
			float(num)
			return True
		except:
			return False
	
	def _initialize_skus(self):
		self.skus = [sk for sk in self.prod]
		
	def __str__(self):
		return "\n".join(self.skus)

	def __len__(self):
		return len(self.prod)