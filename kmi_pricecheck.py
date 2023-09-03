import xlwt,xlrd,csv,os




def main():
	file = [file for file in os.listdir("C:\Dropbox\Web Updates 2014\procedure") if os.path.splitext(file)[0] == "KMI"][0]
	print file
	book = xlrd.open_workbook("C:\Dropbox\Web Updates 2014\procedure\\"+file)
	sheet1 = book.sheet_by_name("Sheet1")
	for x in range(sheet1.nrows):
		row = sheet1.row(x)
		for c in range(sheet1.ncols):
			print row[c].value









if __name__ == "__main__":
	main()