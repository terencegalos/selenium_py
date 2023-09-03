import time
import csv   
    
####################################################################################################################################################################################################################################



def make_cats(skus,feed):
	items = []
	cats = []
	#with open("./csv/infile/waresitat_kraftklub_sku.csv","rb") as skus:
	for sku in skus:
		print "Getting cats for " + sku
		#time.sleep(3)
		#with open("./csv/infile/waresitat_kraftklub.csv","rb") as lines:
		cat = []
		for line in feed:
			attr = line
			if(sku.strip() ==  attr[1].strip()):
				cat.append(attr[2].strip())
				print "match found: " + attr[1].strip()
		result = [sku.strip(),"|".join(cat)]
		print result
		cats.append(result)
	return cats
	
        
# outfile = open("./csv/outfile/text_generated_cats.csv","wb")
# writer = csv.writer(outfile)
# writer.writerows(cats)