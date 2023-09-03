import ftplib
import csv

ftp = ftplib.FTP("ftp.waresitat.com")
ftp.login("wares","w@r3s")

ftp.cwd("JDYEATTS800")
mylist = ftp.nlst()

outfile = open("./csv/outfile/ftp.csv","wb")
writer = csv.writer(outfile,delimiter=',')

# print mylist
for line in mylist:
	writer.writerow([line])
outfile.close()