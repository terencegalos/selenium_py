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

for sku in missing: # file is a csv reader obj
	print sku
	myCounter.subtotal += 1.0
	print "Progress:"+str(int((myCounter.subtotal/total) * 100)) + "%"

	items = targetv.get_images(sku) #search item
	
	store = []
	for item in items:
	    # print item.get_attribute("innerHTML")
	    name = item.find_element_by_css_selector("table > tbody > tr:nth-child(2) > td").text
	    image = item.find_element_by_css_selector("table > tbody > tr:nth-child(1) > td > a > img").get_attribute("src").split("=")[-1]
	    print [name,image]
        store.append([name,"http://www.primitivesatcrowhollow.com/fpdb/images/"+image])

	# print store

# send item to csv right away

outfile.close()

time.sleep(3)

# targetv.send_to_file(targetv.vendor,ar)
print "Execute finished time:"
print datetime.now()
targetv.driver.close()	
# os.system('shutdown -s')