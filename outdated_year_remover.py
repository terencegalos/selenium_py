import xlrd,os,csv,sys

def main():
    dir = "C:/Dropbox/Web Updates 2014/2017 Upload/Waresitat Upload/"
    status = {} # dictionary for each item
	
    with open("./csv/outfile/vendor_ids.csv","rb") as infile:
        
        reader = csv.reader(infile)
        filenames = [i[3] for i in reader] # get vendor filenames in csv list
        for x in range(1,len(filenames)):
            filename = filenames[x]
            print "Filename: "+filename

            try:
                rbook = xlrd.open_workbook(dir+filename) # xlrd instance for current vendot
            except:
                print "File not found: "+filename

            rsheet = rbook.sheet_by_index(0) # pull tab1 content for current sheet

            ls = [] # list instance for vendor categories
            for c in range(rsheet.nrows):
                row = rsheet.row(c)
                cats = row[2].value.split("|") if "|" in row[2].value else [row[2].value]
                for cat in cats:
                    ls.append(cat)
            status.update({filename:list(set(ls))})

			
	
	with open("./csv/outfile/outdated_section_output.csv","wb") as outfile:
		writer = csv.writer(outfile)
		for v in status:
			writer.writerow([v,status[v]])
		
				



if __name__ == "__main__":
	main()