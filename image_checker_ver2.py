import ftplib,csv,os,sys,time,xlrd,xlwt

vendor = sys.argv[1]
counter = 0


ip = 'ftp.waresitat.com'
uname,passw = 'wares','w@r3s'

#GET vendor info from csv file
with open("./csv/outfile/vendor_ids.csv","rb") as infile:
	reader = csv.reader(infile)
	resized = [v.strip() for v in ([cell[4:7] for cell in reader if cell[1] == vendor][0])]
	resized = [i for i in resized if len(i) > 0] #FILTER if size 800 is not available
print resized
time.sleep(3)

ftp = ftplib.FTP(ip) #GET ftp access
ftp.login(uname,passw)

# latest = goto_lastmod_dir()     #GOTO last modified directory on local machine - NOT resized images folders
all = []
for x in range(len(resized)):     # LOOP using range to get count

    print resized[x]
    ftp.cwd('/'+resized[x])     #GOTO FTP size[x] subdir
    print ftp.pwd()

    size = [resized[x]]
    size.extend(ftp.nlst())
    # print size
    all.append(size)
    
outfile = open("./csv/outfile/ftp_result.csv","wb")
outfile = csv.writer(outfile)
for one in all:
    outfile.writerow(one)