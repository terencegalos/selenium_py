from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys

from active_record import active_record
import webdriver_config
w_opt = ["http://www.millerdecor.com/catalog/item/9042085/10309596.htm","http://www.millerdecor.com/catalog/item/7953102/8561627.htm"]
v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance
br.execute_script("document.body.style.zoom='zoom50%'")

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

file = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)


cats = [link.get_attribute("href") for link in br.find_elements_by_css_selector("#colTable > tbody > tr> td > p > a")]
print cats
print "Waiting for homepage to load..."
time.sleep(1)

items = []
table = []

# def test():
for cat in cats:
	# if "porcelain" not in cat.lower():
		# continue
	if "http" not in cat:
		continue
		
	print "Navigating to " + cat
	br.get(cat)
	time.sleep(1)
	
	try:
		dim = br.find_element_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > p:nth-child(6) > span:nth-child(1) > strong").text.encode("utf-8")
	except:
		dim = "No dim."
	
	try:
		item = [i.get_attribute("href") for i in br.find_elements_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > div.catalog-container > table > tbody > tr > td > div > a")]
		print item
		items.extend(item)
	except Exception as e:
		raise e
	
	while True:
		try:
			br.get(br.find_element_by_css_selector("a.catalog-pagination-next").get_attribute("href"))
			time.sleep(1)
			print "Loading next page...\n"
			time.sleep(3)
			item = [i.get_attribute("href") for i in br.find_elements_by_css_selector("#quirks > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > div.catalog-container > table > tbody > tr > td > div > a")]
			print item
			items.extend(item)
		except Exception as e:
			print "Page exhausted"
			break
			raise e
			
		


for item in items:
	targetv.navigate(item) #navigate link product link
	#return gateway instance with info
	while True:
		try:
			db = targetv.get_info() # get product info
			break
		except:
			WebDriverWait(br, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
			alert = br.switch_to.alert()
			alert.accept()
			continue
	try:
		ar.save(db)
		writer.writerow(db.retrieve())
	except:
		for d in db:
			ar.save(d)
			writer.writerow(d.retrieve())
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()