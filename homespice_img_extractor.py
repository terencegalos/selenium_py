import csv,os,sys,time
final = []
with open("./csv/infile/homespice.csv","rb") as infile:
	freader = csv.reader(infile)
	for line in freader:
		ls = []
		ls.append(line[1])
		for cell in line:
			if "http://i1307.photobucket.com" in cell:
				ls.append(cell)
		# print ls
		final.append(ls)
		# time.sleep(1)
		
outfile = open("./csv/outfile/homespice_out.csv","wb")
writer = csv.writer(outfile)
writer.writerows(final)
outfile.close()