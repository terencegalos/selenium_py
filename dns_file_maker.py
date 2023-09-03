import xlwt,xlrd,os

tier = {3:2,4:4,5:6,6:8,7:12,8:16,9:24,10:32,11:48}

def getBook(book):
	rbook = xlrd.open_workbook(book)
	return rbook

def getSheet():
	book = getBook("./xls/dns.xls")
	return book.sheet_by_index(0)	

def main():
	all = []
	sheet = getSheet()
	for x in range(sheet.nrows):
		ls = []
		row = sheet.row(x)
		print row
		name = row[0].value
		sku = row[1].value
		ls.extend([name,sku])
		for x in range(3,12):
			value = row[x].value
			if value != "":
				min = tier[x]
				price = value
				ls.extend([min,price])
		print ls
		all.append(ls)
	
	wbook = xlwt.Workbook()
	wsheet = wbook.add_sheet("Sheet1")
	for x in range(len(all)):
		row = wsheet.row(x)
		for index in range(len(all[x])):
			row.write(index,all[x][index])
	wbook.save("./csv/outfile/dns.xls")
		



if __name__ == "__main__":
	main()