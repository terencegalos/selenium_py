import xlwt,xlrd,csv,os

class Waresitat():
	prod = {}
	
	def __init__(self,f):
		rbook = xlrd.open_workbook(f)
		rsheet = rbook.sheet_by_index(0)
		# print rsheet.row(1)
		for x in range(1,rsheet.nrows):
			cur = {}
			sku = rsheet.row(x)[0].value
			self.prod[sku] = {}
			
			self.prod[sku]['name'] = rsheet.row(x)[1].value
			self.prod[sku]['sku'] = rsheet.row(x)[0].value
			self.prod[sku]['cat'] = rsheet.row(x)[3].value
			self.prod[sku]['desc'] = ""
			self.prod[sku]['stock'] = rsheet.row(x)[6].value
			self.prod[sku]['sale'] = ""
			self.prod[sku]['set'] = ""
			self.prod[sku]['custom'] = ""
			self.prod[sku]['size'] = rsheet.row(x)[2].value
			self.prod[sku]['top'] = ""
			self.prod[sku]['min'] = 1
			self.prod[sku]['price1'] = rsheet.row(x)[4].value
			self.prod[sku]['min2'] = ""
			self.prod[sku]['price2'] = ""
			self.prod[sku]['min3'] = ""
			self.prod[sku]['price3'] = ""
			self.prod[sku]['multi'] = 1
			self.prod[sku]['img400'] = "Cap 400"
			self.prod[sku]['img160'] = "Cap 160"
			self.prod[sku]['jpg400'] = ""
			self.prod[sku]['jpg160'] = ""
			self.prod[sku]['desc2'] = ""
			self.prod[sku]['opt'] = ""
			self.prod[sku]['img800'] = "Cap 800"
			self.prod[sku]['jpg800'] = ""
			self.prod[sku]['UPC'] = ""

			
			
			


def main():
	os.chdir("./xls/")
	wares = Waresitat("capitol.xls")
	os.chdir('../csv/outfile')
	wbook = xlwt.Workbook()
	rsheet = wbook.add_sheet("Sheet1")
	for count,i in enumerate(wares.prod):
		row = rsheet.row(count)
		val = [wares.prod[i]['name'],wares.prod[i]['sku'],wares.prod[i]['cat'],wares.prod[i]['desc'],wares.prod[i]['stock'],str(wares.prod[i]['sale']),wares.prod[i]['set'],wares.prod[i]['custom'],wares.prod[i]['size'],wares.prod[i]['top'],str(wares.prod[i]['min']),str(wares.prod[i]['price1']),wares.prod[i]['min2'],wares.prod[i]['price2'],wares.prod[i]['min3'],wares.prod[i]['price3'],wares.prod[i]['multi'],wares.prod[i]['img400'],wares.prod[i]['img160'],wares.prod[i]['jpg400'],wares.prod[i]['jpg160'],wares.prod[i]['desc2'],wares.prod[i]['opt'],wares.prod[i]['img800'],wares.prod[i]['jpg800'],wares.prod[i]['UPC']]
		for index,v in enumerate(val):
			try:
				row.write(index,float(v))
			except:
				row.write(index,v)
	wbook.save("Northlight_Seasonal_8016.xls")
	
	
	
if __name__ == "__main__":
	main()