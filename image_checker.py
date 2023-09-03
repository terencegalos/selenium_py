import time
import csv
import os, sys, shutil
from selenium.webdriver.common.keys import Keys

import webdriver_config as driver
#import image_download as img
#from thread_inc import threadclass
vendors = [i.strip() for i in sys.argv[1:]]
print vendors[0].decode("latin-1")
print 'input vendors: '+str(vendors)
time.sleep(1)




def get_img_stat(row,out):
    try:
        stock = row.find_element_by_css_selector("td:nth-child(4) > strong > font[color=RED]").text
        print stock
        # if stock == "IMAGE DOES NOT EXIST":     #check EACH items if image does not exist
        name = row.find_element_by_css_selector("td:nth-child(2)").text.encode("utf-8")
        sku = row.find_element_by_css_selector("td:nth-child(3)").text.encode("utf-8")
        print [name,sku]
        out.append([name.strip().replace(",", "\comma"),sku.strip()])
    except Exception as e:
        print e
        #print "Skipped row: Image status not visible."
        # time.sleep(1)
		
		
#-------------------------------------------------------------------------------------------------
br = driver.init_driver()
time.sleep(1)
#navigate with site credentials
br.get("https://wares:w@r3s@www.waresitat.com/adminpage/index.cfm")
time.sleep(1)

#reload to view site properly
br.get("https://www.waresitat.com/adminpage/index.cfm")
time.sleep(1)

br.get("https://www.waresitat.com/adminpage/products/index.cfm")
time.sleep(1)

#get vendors element
allvendors = br.find_elements_by_css_selector("body > center > table > tbody > tr > td > div:nth-child(3) > table > tbody > tr > td > form > select > option")


for x in range(len(allvendors)):   #loop each vendor in webpage
    cvendor = br.find_elements_by_css_selector("body > center > table > tbody > tr > td > div:nth-child(3) > table > tbody > tr > td > form > select > option")[x]
    print 'current vendor: '+cvendor.text.strip().encode("latin-1")
    if cvendor.text.strip().encode("latin-1") in vendors:
        vendortxt = cvendor.text.strip()
        print "Match found."
        time.sleep(1)
        cvendor.click()
        time.sleep(3)
        rows = br.find_elements_by_css_selector("body > center > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr") #get all rows for current vendor
        # rows = br.find_elements_by_css_selector("body > center > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(11) > td:nth-child(4) > strong > font[color=RED]") #get all rows for current vendor
        table = []
        
        ### selenium not thread-safe###
        #thread = threadclass() #new threader instance
        #thread.threader(get_img_stat,rows,table,4)
        
        for row in rows:
            get_img_stat(row,table)
        
        #print vendortxt
        outfile = open("./csv/outfile/noimg/"+vendortxt.replace(" ","_").replace("/","&")+".csv","wb")   #save current vendor to csv
        writer = csv.writer(outfile)
        writer.writerows(table)
        outfile.close()
        print "Done.\nNext vendor..."
            
    else:
        print "No match found for: "+ cvendor.text.strip()
        # time.sleep(1)

br.close()        
                
                

