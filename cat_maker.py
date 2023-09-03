import os,sys,csv,time,shutil

vendor = sys.argv[1]

cats = ["Canvas","Pick","Orn","Green","Berry","Snowman","Doll","Jingle","Christmas","Fall","Jar","Pillow","Clock","Stand","Sign","Ornament","Farm","Tray","Hat","Enamel","Lantern","Pumpkin","Tree","Candle","Enamelware","Wreath","Garland","LED","Bell","Buckets"]

with open("./csv/infile/upload file/"+vendor+".csv","rb") as file:
    reader = csv.reader(file)
    
    d = dict()
    ## reader the file first for less ten cats
    holder = []
    for line in reader:
        holder.append(line)

    
    final = []
    for line in holder:
        for cat in cats:
            if cat in line[0]:
                line[2] = cat
				final.append(line)
                    
    
        


    

with open("./csv/infile/upload file/"+vendor+".csv","wb") as file:
    writer = csv.writer(file)
    writer.writerows(final)

print "Success!"
print "Script ended."