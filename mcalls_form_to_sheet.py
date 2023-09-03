import csv,xlrd,xlwt


def main():
	items = []
	rbook = xlrd.open_workbook("./csv/infile/mccalls.xls")
	rsheet = rbook.sheet_by_index(0)
	for x in range(rsheet.nrows):
		if x > 5:
			row = rsheet.row(x)
			for c in range(2,len(row)):
				print c
				if "N/A" not in row[c].value.upper():
					name = rsheet.row(0)[c].value.encode("utf-8")
					scent = rsheet.row(x)[1].value.encode("utf-8")
					min = rsheet.row(4)[c].value
					price = rsheet.row(1)[c].value.encode("utf-8")
					case = rsheet.row(3)[c].value.encode("utf-8")
					caseprice = rsheet.row(2)[c].value.encode("utf-8")
					item = [scent + " " + name,min,price.split("/")[0],case.split()[0],caseprice.split("/")[0]]
					print item
					items.append(item)
	# rsheet.close()
	
	with open("./csv/outfile/mccalls_output.csv","wb") as outfile:
		writer = csv.writer(outfile)
		writer.writerows(items)



if __name__ == "__main__":
	main()