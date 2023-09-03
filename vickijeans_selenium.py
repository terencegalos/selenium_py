from selenium import webdriver
import time
import urllib
import requests
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains



url = "http://www.vickiejeanscreations.com/index.php"
# uname = "rick@waresitat.com"
# passw = "wolfville"
uname = "Rick"
passw = "333333"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):
    driver.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) center:nth-child(2) b font a:nth-child(6)").click()
    time.sleep(1)   
    driver.find_element_by_name("bname").send_keys(un)
    driver.find_element_by_name("rnumber").send_keys(pw)
    driver.find_element_by_css_selector("#signup_form center input[type=\"submit\"]").click()
    time.sleep(5)
    print "Logged in."


        
br = init_driver()
br.get(url)
init_login(br,uname,passw)
time.sleep(1)
# btn = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl37_rpLinkList_ctl00_dvHorizontalNavItem a")))
# btn.click()
# time.sleep(2)


items = []
table = []
cats = []

cat = br.find_elements_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(1) a")
    
for xc in range(len(cat)-4):
    ct = cat[xc].get_attribute("href")
    print ct
    cats.append(ct)

    
    

for x in range(len(cats)):
    print "Navigating to: " + str(cats[x])
    br.get(cats[x])
    time.sleep(1)
    if x is not 0 and x is not 1:
        subcats = []
        print "Subcategory found. Looping each for items..."
        subcat = br.find_elements_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) table tbody tr td a")
        
        for sc in subcat:
            subc = sc.get_attribute("href")
            subcats.append(subc)
            print subc
            
        for sub in subcats:
            print "Getting items in this subcategory..."
            br.get(sub)        
            time.sleep(1)
            item = br.find_elements_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) table tbody tr td div a")
            for itm in item:
                it = itm.get_attribute("href")
                print it
                items.append(it)
    else:
        print "Not a subcategory. Getting all items in this page..."
        item = br.find_elements_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) table tbody tr td div a")
        for itm in item:
            it = itm.get_attribute("href")
            print it
            items.append(it)
            

print "All items now ready to scraped.**"  
          
ulist = list(set(items))
          
for i in ulist:
    ls = []
    print "Navigating to " + str(i)
    retry = 0

    try:
        br.get(i)
        time.sleep(1)
        name = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(1) span"))).text.encode("utf-8")
        try:
            sku = br.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(2) span").text.encode("utf-8")
        except:
            sku = "No SKU."
        desc = br.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(1) i").text.encode("utf-8")
        minqty = br.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(2) td span:nth-child(3)").text.encode("utf-8")
        price = br.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(2) td span:nth-child(1)").text.encode("utf-8")
        pic = br.find_element_by_css_selector("body center table tbody tr td center table tbody tr td table tbody tr td:nth-child(2) div:nth-child(3) table tbody tr:nth-child(1) td:nth-child(2) img").get_attribute("src")
        
        ls.append(name)
        ls.append(sku)
        ls.append(desc)
        ls.append(minqty)
        ls.append(price)
        ls.append(pic)
        table.append(ls)
        print ls
    except:
        if retry <= 3:
            retry = retry + 1
            print "Retry attempt: " + str(retry)
            br.refresh()
            continue
        else:
            print "Max retry attempt reached. Skipping this item and going to the next..."
            break
                

print "**Job Done***"    



    
        
outfile = open("./csv/outfile/vickiejeanscreations_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table) 