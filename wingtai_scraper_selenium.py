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

# targetv.get_all_items()                                         #scraper mode; scanned vendor for all items

# missing = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)


cats = [i.get_attribute("href") for i in targetv.driver.find_elements_by_css_selector("#footer > div > a.footer_pagelink")] # get all category
# cats = [i.get_attribute("href") for i in targetv.driver.find_elements_by_css_selector("#ShopSite > li > div > ul > li > a")] # get all category

for count,cat in enumerate(cats):
    # print "Count:"+str(count)
    if count > 1:
        continue

    print "Navigating item:"
    targetv.navigate(cat) #navigate link product link
    targetv.time.sleep(5)

    db = targetv.get_info()
    print "Saving db."
    for d in db:
        ar.save(d)
        writer.writerow(d.retrieve())

    while targetv.nextPage():
        targetv.get_info()
        for d in db:
            ar.save(d)
            writer.writerow(d.retrieve())
		
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()