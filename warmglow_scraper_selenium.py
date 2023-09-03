from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys,os

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

items = targetv.get_sitemap()

for item in items[1:]:
	targetv.navigate(item) #navigate link product link

	#return gateway instance with info
	if targetv.isBtn():
		db = targetv.clickBtn()
	else:
		db = targetv.get_info() # get product info

	if db is not None:
		if isinstance(db,list): # check if multiple items return (just like wingtai)
			print "Multiple items detected.."
			for d in db:
				if d is None:
					continue
				ar.save(d)
				writer.writerow(d.retrieve())
		else:
			ar.save(db)
			writer.writerow(db.retrieve())

# send item to csv right away

outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
# targetv.driver.close()
# os.system('shutdown -s')