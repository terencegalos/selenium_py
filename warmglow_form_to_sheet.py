import xlrd,xlwt,time

def getScents():
	rbook = xlrd.open_workbook("C:/Users/Berries/Code/xls/7916.xls")
	rsheet = rbook.sheet_by_index(0)
	pricexscents = {2:{rsheet.row(0)[2].value + " " + rsheet.row(1)[2].value:rsheet.row(2)[2]},3:{rsheet.row(0)[3].value + " " + rsheet.row(1)[3].value:rsheet.row(2)[3].value},4:{rsheet.row(0)[4].value + " " + rsheet.row(1)[4].value:rsheet.row(2)[4].value},5:{rsheet.row(0)[5].value + " " + rsheet.row(1)[5].value:rsheet.row(2)[5].value},6:{rsheet.row(0)[6].value + " " + rsheet.row(1)[6].value:rsheet.row(2)[6].value},7:{rsheet.row(0)[7].value + " " + rsheet.row(1)[7].value:rsheet.row(2)[7].value},8:{rsheet.row(0)[8].value + " " + rsheet.row(1)[8].value:rsheet.row(2)[8].value},9:{rsheet.row(0)[9].value + " " + rsheet.row(1)[9].value:rsheet.row(2)[9].value}}
	return pricexscents

items = []

def sendToFile(ls):
	wbook = xlwt.Workbook()
	wsheet = wbook.add_sheet("Sheet1")
	for itemx in range(len(ls)): # loop all items
		print itemx
		for datax in range(len(ls[itemx])):
			print datax
			print ls[datax]
			if isinstance(ls[itemx][datax],xlrd.sheet.Cell):
				wsheet.write(itemx,datax,ls[itemx][datax].value)
			else:
				wsheet.write(itemx,datax,ls[itemx][datax])
	wbook.save("C:/Users/Berries/Code/csv/outfile/warmglow_form_to_sheet_out.xls")
	# wbook.close()
	
def main():
	#your code here
	rbook = xlrd.open_workbook("C:/Users/Berries/Code/xls/7916.xls")
	rsheet = rbook.sheet_by_index(0)
	pricexscents = getScents()
	for rowx in range(3,rsheet.nrows): # iterate rows
		if rsheet.row(rowx)[1].value == "": #skip not an item or season not indicated
			# print "skipping"
			continue
		# print [r.value for r in rsheet.row(rowx)]
		row = rsheet.row(rowx) # get row
		for cellx in range(2,len(rsheet.row(0))-3): # iterate columns
			# print row[cellx].value
			if "n/a" not in row[cellx].value.lower():
				key = pricexscents[cellx].keys()[0]
				name = row[0].value+" "+key
				price = pricexscents[cellx][key]
				cat = row[1].value
				print name,cat,price
				items.append([name,cat,price])
				
	sendToFile(items)
	
	
	
if __name__ == "__main__":
	main()