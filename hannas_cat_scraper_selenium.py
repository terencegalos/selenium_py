from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys
from active_record import active_record
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import webdriver_config

def scrollDown():
	br.execute_script("window.scrollTo(0,document.body.scrollHeight);")
	
def isLoaded():
	# loaded = br.find_element_by_css_selector("#product-list > div.col-md-12 > div.row > div.col-md-12.total-items-container > span:nth-child(2)")
	while True:
		try:
			loaded = WebDriverWait(br,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-list > div.col-md-12 > div.row > div.col-md-12.total-items-container > span:nth-child(2)")))
			break
		except:
			br.refresh()
	content = br.find_element_by_css_selector("#product-list > div.col-md-12 > div.row > div.col-md-12.total-items-container > span:nth-child(4)")
	if(loaded.text.encode("utf-8") != content.text.encode("utf-8")):
		print loaded.text + " is less than " + content.text
		return False
	else:
		return True
		print "Finish loading."
	
# @cat string for setting category	
def grabInfo(cat):
	result = [[sku.text.split()[2],cat] for sku in br.find_elements_by_css_selector("body > div.wrapper > div > div.main-container.col1-layout > div > div.col-main > div.category-products > ul > li > div > p")]
	print result
	return result
	
def hasPages():
	try:
		br.find_element_by_css_selector("a[title=Next]").click()
		return True
	except:
		return False

v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

# file = targetv.get_file(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance

final = []
curCat = ""
prodURL = "https://www.hannashandiworks.com/products.html"
time.sleep(5)
# WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.index-cats a")))
# print br.find_element_by_css_selector("div.col-main div a").get_attribute("innerHTML")
cats = br.find_elements_by_css_selector("div.col-main div a")
# print cats

for x in range(len(cats)-3):
	cat = br.find_elements_by_css_selector("div.col-main div a")[x] # go to current cat
	curCat = cat.text
	cat.click()
	#show 36 items
	br.find_element_by_css_selector("body > div.wrapper > div > div.main-container.col1-layout > div > div.col-main > div.category-products > div.toolbar > div.pager > div.count-container > div > select > option:nth-child(3)").click()
	time.sleep(2)
	# scrollDown()
	# time.sleep(2)
	final.extend(grabInfo(curCat))
	while(hasPages() == True):
		final.extend(grabInfo(curCat))
		time.sleep(2)
	
	br.get(prodURL)
	time.sleep(1)


# #return gateway instance with info
# db = targetv.get_info() # get product info
# # print "Saved to active record."
# if db is not None:
	# try:
		# writer.writerow(db.retrieve())
		# ar.save(db)
	# except:
		# for d in db:
			# if d is not None:
				# ar.save(db)
				# writer.writerow(d.retrieve())
# else:
	# try:
		# # get attributes directly
		# db = targetv.get_info(row[1].encode("utf-8"))
		# print "Action: Direct get info attempt."
		# ar.save(db)
		# if db is not None:
			# writer.writerow(db.retrieve())
	# except Exception as e:
		# # raise e
		# # print e
		# print "\nStatus: Item not found.\n"

# # send item to csv right away

# outfile.close()

# time.sleep(3)

# targetv.send_to_file(targetv.vendor,ar)
outfile = open("./csv/outfile/hannas_cat_scraper_output.csv","wb")
writer = csv.writer(outfile)
writer.writerows(final)
outfile.close()
targetv.driver.close()