from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys
from active_record import active_record

import webdriver_config
# from access_file import get_file

#import image_download.imageDownload as imgdl

v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

file = targetv.get_file(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance

outfile = open("./csv/outfile/Adams_and_Company_output.csv","wb")
writer = csv.writer(outfile)

for row in file:
    ##search mode OR scraper mode?##
    items = targetv.search_item(row[1])
    if targetv.results(items):
        for item in items:
            targetv.navigate(item)
            
            db = targetv.get_info()                         #return gateway instance with info
            
            if db is not None:
                res = db.retrieve()
                print res
                writer.writerow(res)
            #ar.save(db)
            
    else:
        try:
        #get attributes directly
            db = targetv.get_info()
            
            if db is not None:
                res = db.retrieve()
                print res
                writer.writerow(res)
            
            #ar.save(db)
        except:
            print "Item not found."
        
#print len(ar)
time.sleep(3)

#targetv.send_to_file(targetv.vendor,ar)

outfile.close()

#targetv.driver.close()