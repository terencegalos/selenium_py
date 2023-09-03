from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys,os
from datetime import datetime

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



items = []
items.extend(targetv.get_cat_items())

if targetv.results(items):
	for item in items:

		# print item
		# if targetv.lastStop in item:
		# 	targetv.flag = True

		# if targetv.flag == False:
		# 	print "Skipping**"
		# 	continue
		# else:
		# 	print "Initiate scrape**"

		targetv.navigate(item) #navigate link product link

		#return gateway instance with info
		db = targetv.get_info() # get product info
		time.sleep(targetv.delay)

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
print "Execute finished time:"
print datetime.now()
# targetv.driver.close()
# os.system('shutdown -s')