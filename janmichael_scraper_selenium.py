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

targetv.get_all_items()                                              #get item links

missing = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

count = 0

class Counter:
	subtotal = 0

total = len(missing)
print total
myCounter = Counter()


# for sku in missing: # file is a csv reader obj

for item in targetv.links:
    print "Navigating item:"
    targetv.navigate(item)
    
    #return gateway instance with info
    db = targetv.get_info() # get product info 
    
    # print "Saved to active record."
    if db is not None:
        if isinstance(db,list):
            for d in db:
                if d is not None:
                    ar.save(d)
                    writer.writerow(d.retrieve())
        else:
            writer.writerow(db.retrieve())
            ar.save(db)
		
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()