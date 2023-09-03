from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from urllib2 import urlopen
import csv,time,re,sys,os

from active_record import ActiveRecord
import webdriver_config

v_arg = sys.argv[1]                                             #pass vendor name in command line
mutator = v_arg+"_class"

_vendor_mod = __import__(mutator,globals(),locals(),[],-1)      #dynamic module import

vendor_class_ = getattr(_vendor_mod,v_arg)                      #dynamic class import

br = webdriver_config.init_driver()                             #selenium instance

targetv = vendor_class_(br)                                     #vendor instance; selenium injected, automatic login

missing = targetv.get_missing(targetv.vendor)                   #get csv and store in a list
items = []

ar = active_record()                                            #active_record instance

def instantGet(pair):
    print "Getting items."
    results = [[[pair[0]],a.get_attribute("href")] for a in br.find_elements_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) table tbody tr td div a")]
    print results
    return results

def getSub():
    subspair = [[[p.text], p.find_element_by_css_selector("a").get_attribute("href")] for p in br.find_elements_by_css_selector("body > center > table > tbody > tr > td > center > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr > td > p")]
    return subspair



outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error	
writer = csv.writer(outfile)





catspair = [ [a.get_attribute("href").split("/")[-1], a.get_attribute("href")] for a in br.find_elements_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(1) a")]
print catspair

for x in range(len(catspair)-4):
    br.get(catspair[x][1])
    time.sleep(1)
    if x < 2:
        items.extend(instantGet(catspair[x]))
    else:
        subspair = getSub()
        print "Looping subs"
        for pair in subspair:
            # print pair
            br.get(pair[1])
            time.sleep(1)
            pair[0].append(catspair[x][0]) #add category/subcategory
            items.extend(instantGet(pair))





for item in items:
    targetv.navigate(item[1]) #navigate link product link

    #return gateway instance with info
    db = targetv.get_info(item[0]) # get product info

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