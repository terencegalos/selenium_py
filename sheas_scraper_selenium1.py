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

file = targetv.get_missing(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance
print ar.container

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)

count = 0
br.find_element_by_css_selector("#menu > ul > li:nth-child(3) > a").click()
time.sleep(1)
br.find_element_by_css_selector("#content > div > center > form > span > a:nth-child(6)").click()
time.sleep(6)
items = [l.get_attribute("href") for l in br.find_elements_by_css_selector("#content > div > center > form > table > tbody > tr td:nth-child(2) > a")]

pairs = []
rows = br.find_elements_by_css_selector("#content > div > center > form > table > tbody > tr")
for line in rows:
	try:
		sku = line.find_element_by_css_selector("td:nth-child(2) > a").text.encode("utf-8")
		min = line.find_element_by_css_selector("td:nth-child(8)").text.split()[-1]
		print [sku,min]
		pairs.append([sku,min])
	except:
		print "Skipped"
writer.writerows(pairs)
outfile.close()
			
# send item to csv right away
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()