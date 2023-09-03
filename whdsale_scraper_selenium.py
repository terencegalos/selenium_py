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

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

count = 0

class Counter:
	subtotal = 0

total = len(missing)
print total
myCounter = Counter()

items = ["https://whdfloral.com/fall-cotton-4ft-garland.html","https://whdfloral.com/fall-cotton-4ft-garland.html","https://whdfloral.com/fall-cotton-4ft-garland.html","https://whdfloral.com/fall-cotton-4-5in-candle-ring.html","https://whdfloral.com/fall-cotton-2-5in-candle-ring.html","https://whdfloral.com/fall-cotton-2-5in-candle-ring.html","https://whdfloral.com/fall-cotton-2-5in-candle-ring.html","https://whdfloral.com/fall-cotton-2-5in-candle-ring.html","https://whdfloral.com/autumn-haze-4-5in-candle-ring.html","https://whdfloral.com/autumn-haze-4-5in-candle-ring.html","https://whdfloral.com/autumn-haze-4-5in-candle-ring.html","https://whdfloral.com/sunflower-grass-29in-pick.html","https://whdfloral.com/sunflower-grass-set-of-2-wreaths.html","https://whdfloral.com/sunflower-grass-4-5in-candle-ring.html","https://whdfloral.com/sunflower-grass-2-5in-candle-ring.html","https://whdfloral.com/harvest-grass-xl-4ft-garland.html","https://whdfloral.com/harvest-grass-xl-32in-pick.html","https://whdfloral.com/harvest-grass-xl-32in-pick.html","https://whdfloral.com/harvest-grass-xl4-5in-c-ring.html","https://whdfloral.com/harvest-grass-xl4-5in-c-ring.html","https://whdfloral.com/harvest-grass-xl4-5in-c-ring.html","https://whdfloral.com/harvest-grass-xl4-5in-c-ring.html","https://whdfloral.com/orange-berry-set-of-2-wreaths.html","https://whdfloral.com/orange-berry-4-5in-c-ring.html","https://whdfloral.com/orange-berry-4-5in-c-ring.html","https://whdfloral.com/fall-boxwood-4ft-garland.html","https://whdfloral.com/fall-boxwood-29in-pick.html","https://whdfloral.com/fall-boxwood-29in-pick.html","https://whdfloral.com/fall-boxwood-29in-pick.html","https://whdfloral.com/fall-boxwood-2-5in-candle-ring.html","https://whdfloral.com/fall-boxwood-2-5in-candle-ring.html","https://whdfloral.com/fall-boxwood-2-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-set-of-2-wreath.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/pumpkin-patch-4-5in-candle-ring.html","https://whdfloral.com/poppy-field-31in-pick.html","https://whdfloral.com/poppy-field-31in-pick.html","https://whdfloral.com/poppy-fields-4-5in-candle-ring.html","https://whdfloral.com/poppy-fields-4-5in-candle-ring.html","https://whdfloral.com/poppy-fields-4-5in-candle-ring.html","https://whdfloral.com/poppy-fields-4-5in-candle-ring.html","https://whdfloral.com/awesome-autumn-xxl-wreath-32-in.html"]
print items
for item in list(set(items)):
    while True:
        try:
            print "Navigating item:"
            targetv.navigate(item) #navigate link product link
            break
        except Exception as e:
            print e
            continue
    #return gateway instance with info
    db = targetv.get_info() # get product info
    # print db.retrieve()
    # print "Saved to active record."
    if db is not None:
        try:
            writer.writerow(db.retrieve())
            ar.save(db)
        except:
            try:
                for d in db:
                    if d is not None:
                        ar.save(d)
                        writer.writerow(d.retrieve())
            except:
                pass
		
		
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()