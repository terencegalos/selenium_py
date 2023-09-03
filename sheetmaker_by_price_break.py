import csv, time

fopen = open("./csv/infile/sheetmaker.csv","rb")

r = csv.reader(fopen)
# print reader


final = []

# for line in r:
	# print line
	# time.sleep(1)
for line in r:
	print line
	arr = []
	arr.append(line[0])
	arr.append(line[1])
	if line[10]:
		arr.append(2)
		arr.append(line[10])
	if line[11]:
		arr.append(4)
		arr.append(line[11])
	if line[12]:
		arr.append(6)
		arr.append(line[12])
	if line[13]:
		arr.append(8)
		arr.append(line[13])
	if line[14]:
		arr.append(12)
		arr.append(line[14])
	if line[15]:
		arr.append(16)
		arr.append(line[15])
	if line[16]:
		arr.append(24)
		arr.append(line[16])
	if line[17]:
		arr.append(32)
		arr.append(line[17])
	if line[18]:
		arr.append(48)
		arr.append(line[18])
	if line[19]:
		arr.append(96)
		arr.append(line[19])
		
	print arr
	final.append(arr)

fopen.close()	
fopen = open("./csv/outfile/sheetmaker_output.csv","wb")
writer = csv.writer(fopen)
writer.writerows(final)
fopen.close()

		