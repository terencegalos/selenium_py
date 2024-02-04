import xlrd,os,csv

def main():

    dir = "C:/Users/USER/Dropbox/Waresitat Files/2022 Upload/Waresitat Upload/"
    status = {}

    with open("./csv/outfile/vendor_ids.csv","r") as infile:
        reader = csv.reader(infile)
        xls = [i[3] for i in reader]
        for x in range(1,len(xls)):
            vendor = xls[x]
            try:
                rbook = xlrd.open_workbook(dir+vendor)
            except:
                print("File not found: "+vendor)
                continue
            
            rsheet = rbook.sheet_by_index(0)
            ls = []
            for c in range(rsheet.nrows):
                row = rsheet.row(c)
                ls.extend([cat for cat in row[2].value.split("|") if cat not in ls])
                
            status.update({vendor:ls})
			
    with open("./csv/outfile/category_status.csv","w") as outfile:
        writer = csv.writer(outfile)
        for v in status:
            writer.writerow([v,status[v]])
		
				



if __name__ == "__main__":
	main()