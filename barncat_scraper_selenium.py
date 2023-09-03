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

# missing = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

br.get("https://barncatmercantile.com/collections/all?page=1")
time.sleep(1)

def get_items():
	while True:
		try:
			item = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#CollectionSection > div.grid-uniform.grid-link__container > div > div > a")]
			print item
			items.extend(item)
			time.sleep(1)
			break
		except:
			time.sleep(1)
			continue
	
def nextPage():
	try:
		br.get(br.find_element_by_css_selector("#CollectionSection > div.text-center > ul > li:nth-child(6) a").get_attribute("href"))
		print "Next page."
		time.sleep(3)
		return True
	except Exception as e:
		print e
		print "Exhausted all pages."
		return False

items = []

get_items()
while nextPage():
    get_items()


for item in set(items):
	targetv.navigate(item) #navigate link product link
	db = targetv.get_info() # get product info
	if db is not None:
		try:
			writer.writerow(db.retrieve())
			ar.save(db)
		except:
			for d in db:
				if d is not None:
					ar.save(d)
					writer.writerow(d.retrieve())
		
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()