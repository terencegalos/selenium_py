from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys

from active_record import active_record
import webdriver_config

def getLinks():
	links = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#tygh_main_container > div.tygh-content.clearfix > div > div:nth-child(2) > div > div > div > div > div:nth-child(3) > div > div.ty-sitemap__tree-section > ul > li > a")]
	return links

def getItems():
	
	br.find_elements_by_css_selector("#pagination_contents > form > div > div > div > div.ty-compact-list__title > div > span.ty-control-group__item")
	br.find_elements_by_css_selector("#pagination_contents > div.ty-compact-list > div > form > div > div.ty-compact-list__title > div > span")
	skus = [i.text for i in br.find_elements_by_css_selector("#pagination_contents > div.ty-compact-list > div > form > div > div.ty-compact-list__title > div > span")]
	print skus
	
	saveItem(skus)
	
def saveItem(list):
	skus.extend(list)
	
def paginator():
	#expand list
	WebDriverWait(br, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pagination_contents > div.ty-sort-container > div.ty-sort-container__views-icons > a:nth-child(3)"))).click()
	time.sleep(3)
	# WebDriverWait(br, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sw_elm_pagination_steps"))).click()
	# time.sleep(1)
	
	# try:
		# WebDriverWait(br, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#elm_pagination_steps > li:nth-child(4) > a"))).click()
		# time.sleep(1)
	# except:
		# pass
	
	# view as list
	# WebDriverWait(br, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#pagination_contents > div.ty-sort-container > div.ty-sort-container__views-icons > a:nth-child(3)"))).click()
	# time.sleep(3)
	
	getItems()
	
	while True:
		try:
			br.find_element_by_css_selector("#pagination_contents > div.ty-pagination__bottom > div > a.ty-pagination__item.ty-pagination__btn.ty-pagination__next.cm-history.cm-ajax > span").click()
			time.sleep(1)
			getItems()
		except:
			print "Page exhausted. Proceeding.."
			break
	
v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

# missing = targetv.get_missing(targetv.vendor)                         #get csv and store in a list
skus = [] # store missing
count = 0

ar = active_record()                                            #active_record instance
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)



br.get("https://www.thehearthsidecollection.com/shop/index.php?dispatch=sitemap.view")
time.sleep(5)
links = getLinks() # get sitemap links
print links 


for link in links: # start getting item skus
	print "Navigating.."
	print link
	br.get(link)
	time.sleep(2)
	paginator()

for sku in list(set(skus)): # file is a csv reader obj
	print sku
	if sku not in [d.sku for d in ar.container]:
		items = targetv.search_item(sku) #search item
		if targetv.results(items):
			for item in items:
				while True:
					try:
						print "Navigating.."
						targetv.navigate(item) #navigate link product link
						break
					except Exception as e:
						print "Navigation error:"+e
						continue
				#return gateway instance with info
				db = targetv.get_info(sku) # get product info
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
					else:
						print "Action: Direct get info attempt."
						try:
							db = targetv.get_info(sku)
							# except:
								# raise Exception
							ar.save(db)
							# if db is not None:
							writer.writerow(db.retrieve())
						except Exception as e:
							# raise e
							print e
							print "\nStatus: Item not found.\n"
		
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()