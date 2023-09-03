import xlrd,os,csv

def main():

	dir = "C:/Dropbox/Web Updates 2014/2017 Upload/Waresitat Upload/"
	status = {}

	with open("./csv/outfile/vendor_ids.csv","rb") as infile:
		reader = csv.reader(infile)
		xls = [i[3] for i in reader]
		for x in range(1,len(xls)):
			vendor = xls[x]
			try:
				rbook = xlrd.open_workbook(dir+vendor)
			except:
				print "File not found: "+vendor
				continue
			rsheet = rbook.sheet_by_index(0)
			ls = []
			for c in range(rsheet.nrows):
				row = rsheet.row(c)
				if row[8].value not in ls:
					ls.append(row[8].value)
			status.update({vendor:ls})
			
	with open("./csv/outfile/size_checker.csv","wb") as outfile:
		writer = csv.writer(outfile)
		for v in status:
			writer.writerow([v,status[v]])
		
				



if __name__ == "__main__":
	main()