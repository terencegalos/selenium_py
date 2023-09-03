from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
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

# file = targetv.get_file(targetv.vendor)                         #get csv and store in a list

ar = active_record()                                            #active_record instance

outfile = open("./csv/outfile/"+targetv.vendor+"_output_fail_safe.csv","wb")	#back up in case of error
writer = csv.writer(outfile)

class Counter():
    counter = 1

def go_to_main():
    br.switch_to.default_content()
    time.sleep(1)

def go_to_iframe():
    iframe = br.find_element_by_css_selector("body > div.wrapper > div.main-content > div:nth-child(2) > iframe")
    br.switch_to.frame(iframe)
    time.sleep(1)

def grabber():
    try:
        go_to_iframe()
    except:
        go_to_main()
        go_to_iframe()
    cat = br.find_element_by_css_selector("body > div:nth-child(1) > h1").text.encode("utf-8")
    items = [a.get_attribute("href") for a in br.find_elements_by_css_selector("div.p-name > a")]
    print "Show items..\n"
    print items
    for i in range(len(items)):
        go_to_main()
        time.sleep(.5)
        ActionChains(br).move_to_element(br.find_element_by_css_selector("body > div.wrapper > div.main-content > div:nth-child(2) > iframe")).perform()
        time.sleep(.5)
        try:
            br.find_elements_by_css_selector("div.p-name > a")[i].click()
        except:
            go_to_iframe()
            br.find_elements_by_css_selector("div.p-name > a")[i].click()
        time.sleep(1)
        
        #return gateway instance with info
        db = targetv.get_info(cat) # get product info
        print db

        # saving
        if db is not None:
            try:
                writer.writerow(db.retrieve())
                ar.save(db)
            except:
                for d in db:
                    if d is not None:
                        ar.save(db)
                        writer.writerow(d.retrieve())
	
def more_pages():
    try:
        go_to_iframe()
    except:
        pass
    try:
        br.find_element_by_css_selector("#prevnexttop > div:nth-child(3) > a").click()
        time.sleep(1)
        return True
    except:
        return False




#################################################################
#grab all items
# target = ["body > div > div.main-content > div.left-col > ul > li > ul > li > a"]
target = ["body > div > div.main-content > div.left-col > ul > li > a"]
cats = []
for t in target:
    links = br.find_elements_by_css_selector(t) # get all cats
    #navigate cats
    for x in range(2,len(links)):
        try:
            go_to_main()
        except:
            go_to_iframe()
        ActionChains(br).move_to_element(br.find_elements_by_css_selector("body > div > div.main-content > div.left-col > ul > li > a")[x]).perform()
        cat = br.find_elements_by_css_selector("body > div > div.main-content > div.left-col > ul > li")[x] # get current cat
        subcat = cat.find_elements_by_css_selector("ul li a") # get all subcats from current cat
        # cat expander ( main iframe )
        for c in range(1,len(subcat)): # specify starting range to 1 or will throw error. index 0 is current cat
            # if c > len(subcat)-3:
            
            print "Showing categories."
            while True:
                try:
                    go_to_main()

                    br.find_elements_by_css_selector("body > div > div.main-content > div.left-col > ul > li")[x].click() # expand cat
                    time.sleep(1)
                    cat.find_elements_by_css_selector("ul li a")[c].click() # click subcat
                    break
                except:
                    continue
                    
            time.sleep(1)

            #get all item links
            grabber()
            go_to_iframe()
            while(more_pages()):
                print "More pages"
                grabber()
		
        
outfile.close()

time.sleep(3)

targetv.send_to_file(targetv.vendor,ar)
targetv.driver.close()