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

missing = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance
print ar.container

class Counter:
	subtotal = 0

total = len(missing)
print total
myCounter = Counter()


def nextPage():
	try:
		br.find_element_by_link_text(">").click()
		time.sleep(1)
		return True
	except:
		print "Items extracted."
		return False
	
def getItems():
	item = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#content > div.product-list > div > div.left > div.name > a")]
	print item
	return item
	
def main():
	outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
	writer = csv.writer(outfile)

	targetv.get_cat_items()
	print "All links extracted."
	# print len(targetv.allitems)
	# print targetv.allitems
	print "Initiate scrape procedure."
	for item in targetv.allitems:
		targetv.navigate(item)
		db = targetv.get_info()
		if db is not None:
			writer.writerow(db.retrieve())
			ar.save(db)
	# for item in set(targetv.allitems):
	# 	while True:
	# 		try:
	# 			db = targetv.get_info() # get product info
	# 			break
	# 		except:
	# 			br.refresh()
	# 			time.sleep(1)
	# 			continue
	# 	if db is not None:
	# 		try:
	# 			writer.writerow(db.retrieve())
	# 			ar.save(db)
	# 		except:
	# 			for d in db:
	# 				if d is not None:
	# 					ar.save(d)
	# 					writer.writerow(d.retrieve())
			
	# send item to csv right away
			
	outfile.close()

	time.sleep(3)

	targetv.send_to_file(targetv.vendor,ar)
	targetv.driver.close()

if __name__ == "__main__":
	main()
    