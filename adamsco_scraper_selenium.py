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

class Counter():
    counter = 1


all = []
def grabber():
	curr = [i.get_attribute("href") for i in br.find_elements_by_css_selector("body > div.category.container > div > div.products.list.col-tablet-9 > div > div > div.summary.col-tablet-8.col-phone-7 > div.title > a")]
	print curr
	all.extend(curr)
	
def more_pages():
    # try:
    pages = br.find_elements_by_css_selector("body > div.category.container > div > div.products.list.col-tablet-9 > nav:nth-child(28) > ul > li")[1:]
    indexes = [n.text for n in pages]
    print indexes
    for index in indexes:
        print index
        try:
            float(index)
        except:
            continue
        # print "Current:"+str(myCounter.counter)
        # print "Index:"+str(index)
        if myCounter.counter == float(index):
            print "More pages found."
            br.find_elements_by_css_selector("body > div.category.container > div > div.products.list.col-tablet-9 > nav:nth-child(28) > ul > li > a")[int(index)+1].click()
            myCounter.counter += 1
            time.sleep(1)
            return True
    myCounter.counter = 1
    return False
    # except:
    #     current = 0
    #     print "Pages exhausted."
    #     return False

#####
#grab all items
br.get("https://www.adamsandco.net/clearance.html")
myCounter = Counter()
grabber()
while (more_pages()):
    grabber() 

	

for item in all:
	while True:
		try:
			targetv.navigate(item) #navigate link product link
			break
		except Exception as e:
			print e
			continue
	#return gateway instance with info
	db = targetv.get_info() # get product info
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
		
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()