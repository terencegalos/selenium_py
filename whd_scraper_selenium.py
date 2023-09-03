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

missing = targetv.get_missing(targetv.vendor)                   #get csv and store in a list

ar = active_record()                                            #active_record instance

count = 0
class Counter:
	subtotal = 0

total = len(missing)
print total
myCounter = Counter()



outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

# for sku in missing: # file is a csv reader obj
# 	print sku
# 	myCounter.subtotal += 1.0
# 	print "Progress:"+str(int((myCounter.subtotal/total) * 100)) + "%"
	# if sku not in [d.sku for d in ar.container] and len(sku) > 1: #skipping item already in db

	# items = targetv.search_item(sku.encode("latin-1")) #search item
	
	# outfilemissing = open("./csv/outfile/noimg/whd.csv","wb")
	# writermissing = csv.writer(outfilemissing)
	# writermissing.writerow(items)
	# outfilemissing.close()
items = []
cats = [a.get_attribute("href") for a in br.find_elements_by_css_selector("a.ammenu-link")]
for cat in cats:
	while True:
		try:
			br.get(cat)
			break
		except:
			continue
	time.sleep(3)
	if br.find_elements_by_css_selector("a.product.photo.product-item-photo"):
		items.extend([a.get_attribute("href") for a in br.find_elements_by_css_selector("a.product")])
		print items
		while targetv.nextPage():
			items.extend([a.get_attribute("href") for a in br.find_elements_by_css_selector("a.product")])
			print items
	else:
		print "Skipping.."


	# if targetv.results(items):
for item in list(set(items)):
# for item in missing: #for whd
	if item == targetv.lastPage:
		targetv.flag = False
	if targetv.flag:
		continue
	else:
		targetv.navigate(item) #navigate link product link

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
	# else:
		#getting data immediately if no result shown

		# print "\Direct get info attempt.\n"

		# try:
		# 	db = targetv.get_info(sku)
		# 	if db is not None:
		# 		if isinstance(db,list): # check if multiple items return (just like wingtai)
		# 			print "Multiple items detected.."
		# 			for d in db:
		# 				ar.save(d)
		# 				writer.writerow(d.retrieve())
		# 		else:
		# 			ar.save(db)
		# 			writer.writerow(db.retrieve())
			
		# except:
		# 	print "Item not found."

# send item to csv right away

outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
# targetv.driver.close()