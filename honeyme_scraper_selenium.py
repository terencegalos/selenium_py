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
	curr = [i.get_attribute("href") for i in br.find_elements_by_css_selector("body > main > section > main > div > div.product-listing > article > div.product-item-info > h3 > a")]
	print curr
	all.extend(curr)
	
def more_pages():
    # try:
    pages = br.find_elements_by_css_selector("body > main > section > main > div > div.pagination-container > div > div > a")
    links = [n.get_attribute("href") for n in pages]
    for link in links:
        index = link.split("page")[1].split("=")[1]
        print "Current:"+str(myCounter.counter)
        print "Index:"+str(index)
        if myCounter.counter == float(index):
            print "More pages found."
            br.get(link)
            time.sleep(1)
            myCounter.counter += 1
            return True
    myCounter.counter = 1
    return False
    # except:
    #     current = 0
    #     print "Pages exhausted."
    #     return False

#####
# #grab all items
# target = ["body > header > div.lower-header > nav > ul > li:nth-child(3) > a","body > header > div.lower-header > nav > ul > li:nth-child(4) > a","body > header > div.lower-header > nav > ul > li:nth-child(5) > a","body > header > div.lower-header > nav > ul > li:nth-child(6) > a","body > header > div.lower-header > nav > ul > li:nth-child(7) > a"]
# cats = []
# for t in target:
#     br.find_element_by_css_selector(t).click()
#     time.sleep(1)
#     cur = [a.get_attribute("href") for a in br.find_elements_by_css_selector("body > header > div.lower-header > nav > ul > li.nav-menu-item.dropdown-open > ul > li > a")]
#     print cur
#     cats.extend(cur)

myCounter = Counter()

br.get("https://honeyandme.com/sitemap/categories/")
time.sleep(1)

cats = [a.get_attribute("href") for a in br.find_elements_by_css_selector("body > main > section > section > div > article > div > ul li a")]
for cat in cats:
    print cat
    br.get(cat)
    time.sleep(1)
    grabber()
    while (more_pages()):
        grabber() 

	

for item in list(set(all)):
	# while True:
	if item in targetv.lastStop:
		targetv.flag = True
	if targetv.flag == True:
		try:
			targetv.navigate(item) #navigate link product link
			# break
		except Exception as e:
			print e
	else:
		continue
			# continue
	#return gateway instance with info
	targetv.navigate(item) # get product info
	time.sleep(1)
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