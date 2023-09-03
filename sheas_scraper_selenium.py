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
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

count = 0
br.find_element_by_css_selector("#menu > ul > li:nth-child(3) > a").click()
time.sleep(1)
br.find_element_by_css_selector("#content > div > center > form > span > a:nth-child(6)").click()
time.sleep(6)
items = [l.get_attribute("href") for l in br.find_elements_by_css_selector("#content > div > center > form > table > tbody > tr td:nth-child(2) > a")]


for item in items:
	while True:
		try:
			targetv.navigate(item) #navigate link product link
			break
		except Exception as e:
			print e
			continue
	#return gateway instance with info
	while True:
		try:
			db = targetv.get_info() # get product info
			break
		except:
			br.refresh()
			time.sleep(1)
			continue
	print db.retrieve()
	# print "Saved to active record."
	if db is not None:
		try:
			writer.writerow(db.retrieve())
			ar.save(db)
		except:
			for d in db:
				if d is not None:
					ar.save(d)
					writer.writerow(d.retrieve())
	else:
		try:
		# get attributes directly
			print "Action: Direct get info attempt."
			db = targetv.get_info()
			ar.save(db)
			if db is not None:
				writer.writerow(db.retrieve())
		except Exception as e:
			# raise e
			print e
			print "\nStatus: Item not found.\n"
			
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()