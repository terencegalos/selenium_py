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

# file = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance

lasturl = "https://www.bensonmarketinggroup.com/bags/fabric-bags/polka-dot-organza-bags.html"
lasturl1 = "https://www.bensonmarketinggroup.com/custom-packaging/jewelry-packaging/jewelry-boxes.html"

flag = 0

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error
writer = csv.writer(outfile)


all = []

def getmorecat():
    mc = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#page-columns > div.col-left.sidebar.sidebar-main > div.block.block-vertnav > div.block-content > ul > li.nav-item > a")]
    print mc
    morecat.extend(mc)

def grabber():
	print "\nGrabbing page items.\n"
	curr = [i.get_attribute("href") for i in br.find_elements_by_css_selector("#page-columns > div.column-main > div.category-products > ul > li > h2 > a")]
	print curr
	all.extend(curr)
	
def morepages():
	try:
		br.find_element_by_css_selector("#page-columns > div.column-main > div.category-products > div.toolbar > div.pager > div > ol > li.next > a").click()
		return True
	except:
		print "No more pages.\n"
		return False

#####
#grab all items
cats = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#mainmenu > ul > li > div > div > div > ul > li > a")]
morecat = []
# print cats
# for x in range(1,2):
for x in range(1,len(cats)):
	print "Getting more category"
	print cats[x]
	br.get(cats[x])
	time.sleep(1)
	getmorecat()

cats.extend(morecat)

	
for c in list(set(cats)):
	print c
	br.get(c)
	time.sleep(1)
	grabber()
	while(morepages()):
		print "Going next page.."
		grabber()

for item in list(set(all)):

	if item == lasturl1:
		flag = 1

	if flag == 0:
		continue

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
					ar.save(d)
					writer.writerow(d.retrieve())
		
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()