import os,sys,csv,time

vendor = sys.argv[1]
limit = sys.argv[2]



print("Path: "+os.path.dirname(__file__))
with open(os.path.dirname(__file__)+"/csv/infile/upload file/"+vendor,"r",encoding="ISO-8859-1") as file:
    reader = csv.reader(file)
    
    d = dict()
    
    ## reader instance for category count
    holder = []
    for line in reader:
        holder.append(line)
        cats = line[2].split("|") #get cat
        # print line
        for cat in cats:
            cat = cat.rstrip()
            if cat not in d:
                d.update({cat:1})
            else:
                count = d[cat]
                d[cat] = count + 1
    
    
    #holds the lessten cats
    trimcat = [i for i in d if d[i] < int(limit)]
    for cat in trimcat:
        print(cat+ " is less than "+limit+".")
        
    time.sleep(5)
    
    #create new file with trimmed categories
    for line in holder:
        # print line
        cat = line[2].split("|") #get category
        newcat = [] # holds new category
        for c in cat:
            if c not in trimcat:
                newcat.append(str(c).strip())
			
        cat = "|".join(sorted(set(newcat))) #remove cat if its in trimcat(less than x)
        line[2] = cat

    print("\nMaking final file. Please wait...")
    final = []
    for line in holder:
        # print line
        if line[2] == "":
            line[2] = "Miscellaneous"
            final.append(line)
            # time.sleep(5)
        final.append(line)
        

    

with open(os.path.dirname(__file__)+"/csv/infile/upload file/"+vendor+".csv","w",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(final)

print("Success!")
print("Script ended.")