

import os,csv,sys,shutil,requests,csv,urllib2,time,threading

vendor = sys.argv[1] # specify vendor

class imgDL:

    def __init__(self,vendor):
        self.curDest = None
        #self.vendor = vendor
        self.counter = 0

    def create_dir(self):
        
        #navigate directory relative to which PC is used
        dir = os.getcwd()
        if dir == "C:\\Users\\Berries\\Code":
            dest = "C:\\Waresitat Images\\" + vendor
        else:
            dest = "D:\\Rick\\" + vendor

        #adding new directory
        try:
            print "Creating directory for this vendor..."
            time.sleep(3)
            self.curDest = dest+"\\"+"New folder"
            os.makedirs(self.curDest)
        except:
            self.counter = 1
            while True:
                try:
                    print "That directory already exists. Making a new one..."
                    self.curDest = dest+"\\"+"New folder ("+ str(self.counter) +")"
                    os.makedirs(self.curDest)
                    self.counter = 0
                    break
                except:
                    self.counter = self.counter + 1
                    print self.counter
                    print self.curDest
                    time.sleep(1)
                    continue
        
        #go to directory for saving
        os.chdir(self.curDest)
        print os.getcwd()
        
        
    def download_images(self,link):
        try:
            print "\nDownloading image...\n"
            print link
            filename =  link.split("/")[-1:][0] #create filename
            filename = filename.strip()
            print self.curDest+'\\'+filename
            req = urllib2.Request(link,headers={"User-agent":'Mozilla/5.0'})
            res = urllib2.urlopen(req) #download link
            #saving
            if ".jpg?" in filename:
                filename = filename.split("?")[0]
            output = open(self.curDest+"\\"+filename,"wb")
            output.write(res.read())
            output.close

        except Exception as e:
            print e
            time.sleep(1)

#####################################################            
            
#loop links and download; get input file
with open("./csv/outfile/"+vendor+" output.csv","rb") as infile:
    reader = csv.reader(infile)
    lnks = [line[19] for line in reader]

#remove dupes
links = list(set(lnks))
# for i in lnks:
    # if i not in links:
        # links.append(i)

for l in links:
    print l
      
img = imgDL(vendor)   #class instance

dest = img.create_dir()      #create new directory

#print_lock = threading.Lock()

from thread_inc import thread_class #import threading

thread = thread_class()

thread.threader(img.download_images,links,3)
    
print "Images downloaded"