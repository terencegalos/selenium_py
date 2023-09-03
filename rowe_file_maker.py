import xlrd,xlwt

def is_num(num):
	try:
		float(num)
		return True
	except:
		return False

items = []
rbook = xlrd.open_workbook("./csv/infile/rowe.xls")
rsheet = rbook.sheet_by_index(0)
for x in range(rsheet.nrows):
	row = rsheet.row(x)
	for o in row[3].value.split("|"):
		# for n in o.split():
		n = o.split()[0]
		# if is_num(n):
		item = []
		for c in row:
			item.append(c.value)
		item.append(row[1].value.split("-")[0]+"-"+n)
		print item
		items.append(item)
				
wbook = xlwt.Workbook()
wsheet = wbook.add_sheet("Sheet1")
for x in range(len(items)):
	for c in range(rsheet.ncols+1):
		wsheet.write(x,c,items[x][c])
	wbook.save("./csv/outfile/rowe.xls")