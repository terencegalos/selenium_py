from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys,os

from active_record import active_record
import webdriver_config

v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

#missing = targetv.get_missing(targetv.vendor)                   #get csv and store in a list

ar = active_record()                                            #active_record instance


outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

cats = targetv.aside_grabber()
items = []

for cat in cats:
    targetv.navigate(cat)
    
    item = targetv.item_grabber()
    items.extend(item)
    while targetv.nextPage():
        item = targetv.item_grabber()
        items.extend(item)

for item in set(items):
    targetv.navigate(item) #navigate link product link
    time.sleep(1)
    #return gateway instance with info
    db = targetv.get_info() # get product info

    if db is not None:
        if isinstance(db,list): # check if multiple items return (just like wingtai)
            print "Multiple items detected.."
            for d in db:
                if d is None:
                    continue
                ar.save(d)
                writer.writerow(d.retrieve())
        else:
            ar.save(db)
            writer.writerow(db.retrieve())

# send item to csv right away

outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
# targetv.driver.close()
# os.system('shutdown -s')