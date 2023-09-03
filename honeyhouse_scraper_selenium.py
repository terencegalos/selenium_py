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

file = targetv.get_file(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error
writer = csv.writer(outfile)


all = []
def grabber():
	curr = [i.get_attribute("href") for i in br.find_elements_by_css_selector("div.CatNameCell > div > a")]
	print curr
	all.extend(curr)
	
def more_pages():
	try:
		next = br.find_element_by_css_selector("a[title='Next page']")
		if next.is_displayed():
			print "More pages found."
			br.find_element_by_css_selector("a[title='Next page']").click()
			return True
	except:
		return False

#####
#grab all items
cats = br.find_elements_by_css_selector("#ParentCats > ul > li a")
for n in range(len(cats)-1):
	cat = br.find_elements_by_css_selector("#ParentCats > ul > li a")[n]
	print cat.text
	br.get(cat.get_attribute("href"))
	time.sleep(1)
	grabber()
	while (more_pages()):
		grabber() 

	
print "Status: Begin item scraping."
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