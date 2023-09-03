# indicate the file source in args like so python rename.py [source]



import os,csv,sys
from shutil import copyfile

source = sys.argv[1]
print
print "Source: \n"+ source+"\n"

with open("./csv/infile/rename.csv","rb") as infile:
    reader = csv.reader(infile)
    os.mkdir(source+"/renamed/")
    for line in reader:
        try:
            print line
            print source+"/"+line[0]
            # print "C:/Waresitat Images/Impressions on Market/New folder/"+line[1]
            # print source+line[0]
            # os.rename(source+"/"+line[0],source+"/renamed/"+line[1])
            os.rename(source+"/"+line[0],source+"/renamed/"+line[1])
            # copyfile("C:/Waresitat Images/Impressions on Market/New folder (2)/"+line[2],"C:/Waresitat Images/Impressions on Market/impressions rename/"+line[2])
        except:
            print "Skipped."
            print line
        