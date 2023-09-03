from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys
from active_record import active_record

import webdriver_config

v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

# file = targetv.get_file(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

cats = ["https://www.hcbyraghu.com/index.php?main_page=index&cPath=33_40","https://www.hcbyraghu.com/index.php?main_page=index&cPath=33_34_35","https://www.hcbyraghu.com/index.php?main_page=index&cPath=33_34_35&sort=20a&page=2","https://www.hcbyraghu.com/index.php?main_page=index&cPath=33_34_39","https://www.hcbyraghu.com/index.php?main_page=index&cPath=33_34_38","https://www.hcbyraghu.com/index.php?main_page=index&cPath=33_34_38&sort=20a&page=2","https://www.hcbyraghu.com/index.php?main_page=index&cPath=33_42"]

items = []
for cat in cats:
	print cat
	br.get(cat)
	time.sleep(1)
	item = [i.get_attribute("href") for i in targetv.driver.find_elements_by_css_selector("#productListing > div > div.itemTitle > a")]
	print item
	items.extend(item)

count = 0

for row in items:
	print "Navigating to "+str(row)
	targetv.navigate(row) #navigate link product link
	#return gateway instance with info
	db = targetv.get_info(row) # get product info
	# print "Saved to active record."
	if db is not None:
		try:
			writer.writerow(db.retrieve())
			ar.save(db)
		except:
			for d in db:
				if d is not None:
					ar.save(db)
					writer.writerow(d.retrieve())

# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()