import webdriver_config
import time,sys,os
import urllib
import requests
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import text_generator_cat_maker as catmaker

caps = DesiredCapabilities.FIREFOX





# Tell the Python bindings to use Marionette.
# This will not be necessary in the future,
# when Selenium will auto-detect what remote end
# it is talking to.
caps["marionette"] = True

vendor = sys.argv[1]
value = sys.argv[2]

url = "https://www.waresitat.com/waresitat.cfm"
# value = "8059" # vendor id
uname = "canada2"
passw = "2"

def init_driver():
    path = "./chrome_driver/chromedriver"
    #path = "./firefox_driver/geckodriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_name("login_username").send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_name("password").send_keys(Keys.RETURN)
    time.sleep(1)
    print "Logged in."
    
    

def scrape_page(driver,out):
    ls = []
    name = driver.find_element_by_name("p_productname").get_attribute("value")
    sku = driver.find_element_by_name("p_item_number").get_attribute("value")
    cat = "|".join([c.get_attribute("value") for c in driver.find_elements_by_css_selector("#CFForm_1 > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(9) > td > input[type=\"text\"]")])
    desc = driver.find_element_by_name("p_description").get_attribute("value")
    stock = driver.find_element_by_name("p_sold_out").get_attribute("value")
    sale = driver.find_element_by_name("p_sale_price").get_attribute("value")
    set = driver.find_element_by_name("p_units_per_box").get_attribute("value")
    custom = driver.find_element_by_name("p_comments").get_attribute("value")
    dim = driver.find_element_by_name("p_size").get_attribute("value")
    min1 = driver.find_element_by_name("p_minimum_quantity").get_attribute("value")
    price1 = driver.find_element_by_name("p_unit_price1").get_attribute("value")
    min2 = driver.find_element_by_name("p_minimum_quantityP2").get_attribute("value")
    price2 = driver.find_element_by_name("p_tier_2_price").get_attribute("value")
    min3 = driver.find_element_by_name("p_minimum_quantityP3").get_attribute("value")
    price3 = driver.find_element_by_name("p_tier_3_price").get_attribute("value")
    try:
        pic = driver.find_element_by_css_selector("#CFForm_1 > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr:nth-child(29) > td:nth-child(2) > select > option").get_attribute("value")
    except:
        pic = "No image."
    opt = driver.find_element_by_name("p_options").get_attribute("value")
    ls.append(name.encode("utf-8"))
    ls.append(sku.encode("utf-8"))
    ls.append(cat.encode("utf-8"))
    ls.append(desc.encode("utf-8"))
    ls.append(stock.encode("utf-8"))
    ls.append(sale.encode("utf-8"))
    ls.append(set.encode("utf-8"))
    ls.append(custom.encode("utf-8"))
    ls.append(dim.encode("utf-8"))
    ls.append(min1.encode("utf-8"))
    ls.append(price1.encode("utf-8"))
    ls.append(min2.encode("utf-8"))
    ls.append(price2.encode("utf-8"))
    ls.append(min3.encode("utf-8"))
    ls.append(price3.encode("utf-8"))
    ls.append(min1.encode("utf-8"))
    ls.append(pic.encode("utf-8"))
    ls.append(opt.encode("utf-8"))
    out.append(ls)
    print ls

### Uses products page
br = webdriver_config.init_driver()
time.sleep(1)
br.maximize_window()

#navigate with site credentials
br.get("https://wares:w@r3s@www.waresitat.com/adminpage/index.cfm")
time.sleep(1)

#reload to view site properly
br.get("https://www.waresitat.com/adminpage/index.cfm")
time.sleep(1)


br.find_element_by_link_text("Products").click()
time.sleep(1)

items = []
table = []

# click target vendor
br.find_element_by_css_selector("body > center > table > tbody > tr > td > div:nth-child(3) > table > tbody > tr > td > form > select > option[value=\""+value+"\"]").click()
time.sleep(6)

#get all edit buttons
items = [i.get_attribute("href") for i in br.find_elements_by_css_selector("body > center > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr > td > a") if "https://www.waresitat.com/adminpage/products/index.cfm?action=Edit&" in i.get_attribute("href")]
print items[0:10]
    

for x in range(3,len(items)):
    print "Getting item.."
    try:
        br.get(items[x])
        time.sleep(.5)
        scrape_page(br,table)
        br.back()
        time.sleep(.5)
    except Exception as e:
        print "Skipping..."
        print items[x]
        print e
        time.sleep(1)

outfile = open("./csv/outfile/waresitat_"+vendor+".csv","wb")
writer = csv.writer(outfile)
writer.writerows(table) 

print "**Job Done***"
br.close()