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

file = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

targetv.navigate("http://www.toteandable.com/categories.php")
time.sleep(1)

cats = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#main_contain > section > section > div > div.container_16 > div > div.categories > div > div.catimage.top_most_image > a")]
items = []

for cat in cats[:-6]:
	print "Getting items in "+cat
	br.get(cat)
	time.sleep(1)
	item = [it.get_attribute("href") for it in br.find_elements_by_css_selector("div.prodimage > a")]
	print item
	items.extend(item)
	
for item in items:
	print item
	# while True:
		# try:
	targetv.navigate(item) #navigate link product link
			# break
		# except Exception as e:
			# print e
			# continue
	#return gateway instance with info
	db = targetv.get_info() # get product info
	print db
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