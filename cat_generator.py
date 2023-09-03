import os,sys,csv,time,shutil

print sys.argv
vendor = sys.argv[1]
freq = sys.argv[2]



with open("./csv/infile/upload file/"+vendor+".csv","rb") as file:
    reader = csv.reader(file)
    
    d = dict()
    ## reader the file first for lessten cats
    holder = []
    for line in reader:
        holder.append(line)
        cats = line[0].split(" ") #get cat
        # print line
        for cat in cats:
            cat = cat.rstrip()
            if cat not in d:
                d.update({cat:1})
            else:
                count = d[cat]
                d[cat] = count + 1
    
    
    #holds the lessten cats
    trimcat = [i for i in d if d[i] > int(freq)]
    for cat in trimcat:
        print cat + " is more than " + freq
        


print "Success!"
print "Script ended."