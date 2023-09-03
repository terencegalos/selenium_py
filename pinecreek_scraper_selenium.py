from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys

from active_record import ActiveRecord
import webdriver_config

v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

missing = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = ActiveRecord()                                            #active_record instance
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

count = 0

class Counter:
	subtotal = 0

total = len(missing)
print total
myCounter = Counter()

sitemap = "https://www.shoppinecreek.com/sitemap.html"
br.get(sitemap)
time.sleep(1)

items = [i.get_attribute("href") for i in  br.find_elements_by_css_selector("#sitemap > div.product > div > a")]

# for sku in missing: # file is a csv reader obj
# 	print sku
	# myCounter.subtotal += 1.0
	# print "Progress:"+str(int((myCounter.subtotal/total) * 100)) + "%"
	# if sku not in [d.sku for d in ar.container] and len(sku) > 1:
	# 	items = targetv.search_item(sku.encode("latin-1")) #search item
	# 	print items
	# 	if targetv.results(items):
for item in items:
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
		# else:
		# 	print "Action: Direct get info attempt."
		# 	try:
		# 		db = targetv.get_info(sku)
		# 		# except:
		# 			# raise Exception
		# 		ar.save(db)
		# 		# if db is not None:
		# 		writer.writerow(db.retrieve())
		# 	except Exception as e:
		# 		# raise e
		# 		print e
		# 		print "\nStatus: Item not found.\n"
		
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()