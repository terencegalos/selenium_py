import ftplib,csv,os,sys,time,destination


vendor = sys.argv[1]

counter = 0

#navigate last created directory relative to which PC is used
def goto_lastmod_dir():
    os.chdir(destination.imgdir+"/"+vendor) #go to dir
    all_dir = [d for d in os.listdir(".") if os.path.isdir(d)]
    latest_dir = max(all_dir, key=os.path.getmtime) # get latest modified folder
    os.chdir(latest_dir)
    return destination.imgdir+"/"+vendor+"/"+latest_dir



sizes = [160,400,800]
ip = 'ftp.waresitat.com'
uname,passw = 'wares','w@r3s'

#GET vendor info from csv file
with open("./csv/outfile/vendor_ids.csv","rb") as file:
	freader = csv.reader(file)
	for line in freader:
		resized = [v.strip() for v in ([line[4:7] for line in freader if line[1] == vendor][0])]
		resized = [i for i in resized if len(i) > 0] #FILTER if size 800 is not available
print resized
time.sleep(3)



ftp = ftplib.FTP(ip) #GET ftp access
ftp.login(uname,passw)

latest = goto_lastmod_dir()     #GOTO last modified directory on local machine - NOT resized images folders

for x in range(len(resized)):     # LOOP using range to get count
    os.chdir(latest+"/"+repr(sizes[x]))    #GOTO sizes[x] subdir	
    print os.getcwd()
    print resized[x]
    try:
		ftp.cwd('/'+resized[x])     #GOTO FTP size[x] subdir
    except:
		ftp.mkd('/'+resized[x])     #GOTO FTP size[x] subdir
		ftp.cwd('/'+resized[x])     #GOTO FTP size[x] subdir
    print ftp.pwd()
    
    images = os.listdir(".")
    all = ftp.nlst()
    
    for im in images:
        print im
        #print ftp.storbinary.__doc__
        #print dir(ftp.storbinary)
        # if im not in all:
        code = ftp.storbinary('STOR '+im,open(im,'rb'))
        print code
        # else:
			# im+ ' skipped.'
        
    all = ftp.nlst()
    for im in images:
        if im in all:
            pass
        else:
            print im + ' not in ftp'
            counter += counter
    if counter > 0:
        print "Status: There is/are: "+counter+' image/s not uploaded'
    else:
        print "All "+str(len(images))+" images successfully uploaded."