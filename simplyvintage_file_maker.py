import xlrd,xlwt,csv



def main():
	items = []
	rbook = xlrd.open_workbook("./xls/simplyvintage.xls")
	rsheet = rbook.sheet_by_index(0)
	for n in range(1,rsheet.nrows):
		row = rsheet.row(n)
		name = row[0].value
		sku = row[1].value
		for x in range(2,rsheet.ncols):
			# ls = []
			if x == 2 and row[x].value is not "":
				items.append([name,sku,"16oz"])
			if x == 3 and row[x].value is not "":
				items.append([name,sku,"8oz"])
			if x == 4 and row[x].value is not "":
				items.append([name,sku,"4oz"])
			if x == 5 and row[x].value is not "":
				items.append([name,sku,"Tart"])
			if x == 5 and row[x].value is not "":
				items.append([name,sku,"Tea"])
			# print 
			# items.append(ls)
	wbook = xlwt.Workbook()
	wsheet = wbook.add_sheet("Sheet1")
	for n,x in enumerate(items):
		print n,x
		for c in range(len(x)):
			wsheet.write(n,c,x[c])
	wbook.save("./csv/outfile/simplyvintage.xls")

if __name__ == "__main__":
	main()