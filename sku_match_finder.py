import csv,time


fopen = open("./csv/infile/upload file/JanMichael's_Crafts_7908.csv","rb")

freader = csv.reader(fopen)


final = []

fopen1 = open("./csv/infile/sku.csv","rb")
freader1 = csv.reader(fopen1)

uFile = []
skus = []
for line in freader:
	uFile.append(line)
	
for sk in freader1:
	skus.append(sk)

for line in uFile:
	print line
	for sku in skus:
		print sku[0]
		
		if sku[0] in line[1]:
			final.append(line[1])
			print "Match found"
			print sku[0]+" matched with " + line[1]
			# time.sleep(1)
				
			
outfile = open("./csv/outfile/sku_matched.csv","wb")
writer = csv.writer(outfile)
writer.writerow(final)
fopen.close()
fopen1.close()