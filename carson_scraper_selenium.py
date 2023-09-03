from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys,os,datetime

from active_record import active_record
import webdriver_config

v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

missing = targetv.get_missing(targetv.vendor)                   #get csv and store in a list

ar = active_record()                                            #active_record instance

globaldelay = 5
count = 0
class Counter:
	subtotal = 0

total = len(missing)
print total
myCounter = Counter()



outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

# for sku in missing: # file is a csv reader obj
# 	print sku
# 	myCounter.subtotal += 1.0
# 	print "Progress:"+str(int((myCounter.subtotal/total) * 100)) + "%"

# 	items = targetv.search_item(sku) #search item
    
# 	linkoutfile = open("./csv/outfile/carson_links.csv","wb")
# 	carsonwriter = csv.writer(linkoutfile)
# 	for it in items:
# 		carsonwriter.writerow([it])
# 	linkoutfile.close()
	
# 	if targetv.results(items):

# for item in items:

csvinfile = open("./csv/outfile/carson_links.csv","rb")
reader = csv.reader(csvinfile.read().splitlines())
for row in reader:
	item = row[0]
	print str(datetime.datetime.now()) + "\n" # print time
	if item == targetv.lastStop:
		targetv.flag = True
		
	if item == None or targetv.flag == False:
		continue

	targetv.navigate(item) #navigate link product link

	db = targetv.get_info() # get product info
	time.sleep(targetv.delay)

	if db is not None:
		if isinstance(db,list): # check if multiple items return (just like wingtai)
			print "Multiple items detected.."
			for d in db:
				if d is None:
					print "Skipping 'none' type"
					continue
				ar.save(d)
				writer.writerow(d.retrieve())
		else:
			ar.save(db)
			writer.writerow(db.retrieve())
# 	else:
# 		#getting data immediately if no result shown

# 		print "\Direct get info attempt.\n"

# 		try:
# 			db = targetv.get_info(sku)
# 			time.sleep(targetv.delay)
# 			# print db
# 			print type(db)
# 			if db is not None:
# 				if isinstance(db,list): # check if multiple items return (just like wingtai)
# 					print "Multiple items detected.."
# 					for d in db:
# 						ar.save(d)
# 						writer.writerow(d.retrieve())
# 				else:
# 					print "Single item only.."
# 					ar.save(db)
# 					writer.writerow(db.retrieve())
			
# 		except:
# 			print "Item not found."

# # send item to csv right away

outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()
# os.system('shutdown -s')