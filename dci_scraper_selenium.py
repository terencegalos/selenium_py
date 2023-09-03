from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys
from selenium.webdriver.common.action_chains import ActionChains

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

def get_items():

	scrollDown()
	while more_items():
		scrollDown()
	
	itemDivs = br.find_elements_by_css_selector("#product-list-container > div > div.product-item-container")
	for div in range(len(itemDivs)):
		while True:
			try:
				print "Navigating item:"
				targetv.navigate(br.find_elements_by_css_selector("#product-list-container > div > div.product-item-container")[div])
				time.sleep(1)
				db = targetv.get_info() # get product info
				time.sleep(1)
				break
			except Exception as e:
				scrollDown()
				while more_items():
					scrollDown()
				continue
				

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
		
		#go back to previous page
		getItemPage()
		# counter += 1

def more_items():
	progress = br.find_element_by_css_selector("#product-list > div.col-md-12 > div.row").text
	print progress
	if progress.split()[1] == progress.split()[5]:
		print "All items showing..."
		return False
	else:
		return True

def scrollDown():
	# targetv.navigate(br.find_elements_by_css_selector("div.product-description.row > div.product-item-item.hyperlink-like")[-1])
	# ActionChains(br).move_to_element(br.find_element_by_css_selector("div.product-description.row > div.product-item-item.hyperlink-like")).perform()
	while True:
		try:
			br.execute_script("window.scrollTo(0,document.body.scrollHeight);")
			time.sleep(5)
			break
		except:
			time.sleep(1)
			continue

def scrollUp():
	while True:
		try:
			br.execute_script("window.scrollTo(document.body.scrollHeight,0);")
			time.sleep(1)
			break
		except:
			time.sleep(1)
			continue

def getCategoryPage():
	print "Going back to categories..."
	try:
		br.find_element_by_css_selector("#product-list-container > div.product-breadcrumb.col-sm-12 > div.col-md-6.col-sm-6.col-lg-3 > div.hidden-md.hidden-sm.hidden-xs > span:nth-child(2) > a").click()
		time.sleep(1)
	except:
		scrollUp()
		br.find_element_by_css_selector("#product-list-container > div.product-breadcrumb.col-sm-12 > div.col-md-6.col-sm-6.col-lg-3 > div.hidden-md.hidden-sm.hidden-xs > span:nth-child(2) > a").click()
		time.sleep(1)

def getItemPage():
	#go back to previous page
	print "Going back to items..."
	br.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div.product-breadcrumb > a").click()
	time.sleep(1)

def main():
	#show all categories
	targetv.navigate("https://shopdci.com/Product")
	time.sleep(3)

	#loop each of them
	# print br.find_element_by_css_selector("#product-cateogry-container").get_attribute("innerHTML")
	# cats =  br.find_elements_by_css_selector("#product-cateogry-container > div:nth-child(5) > div")
	cats =  br.find_elements_by_css_selector("#product-cateogry-container div.category-name-level-1")
	print len(cats)
	for x in range(16,len(cats)):
		br.find_elements_by_css_selector("#product-cateogry-container div.category-name-level-1")[x].click()
		time.sleep(30)

		get_items()

		time.sleep(3)

		getCategoryPage()

	# send item to csv right away
	outfile.close()

	time.sleep(3)

	targetv.send_to_file(targetv.vendor,ar)
	targetv.driver.close()

if __name__ == "__main__":
	main()