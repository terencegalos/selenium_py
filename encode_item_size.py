import csv,time,sys

final = []

with open("./csv/infile/upload file/hannas.csv","rb") as file:
	reader = csv.reader(file)
	for line in reader:
		print line
		# print line[8].encode("utf-8")
		# try:
		line[8] = str(line[8])
		# except:
			# pass
		
		final.append(line)
			
outfile = open("./csv/outfile/hannas_size_fix.csv","wb")
writer = csv.writer(outfile)
writer.writerows(final)
outfile.close()