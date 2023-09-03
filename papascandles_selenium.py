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



url = "https://www.barncandles.com/"
uname = "rick@waresitat.com"
passw = "wolfville"




def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#TopMenu ul li:nth-child(4) div a:nth-child(1)")))
    btn.click()
    time.sleep(1)
    print "Logging in."
   
    driver.find_element_by_id("login_email").send_keys(un)
    driver.find_element_by_id("login_pass").send_keys(pw)
    driver.find_element_by_id("LoginButton").click()
    time.sleep(5)
    print "Logged in."


        
br = init_driver()
br.get("http://www.papascandleshoppe.com/")
time.sleep(3)
# btn = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#ctl37_rpLinkList_ctl00_dvHorizontalNavItem a")))
# btn.click()
time.sleep(2)



items = []
table = []
links = ["http://www.papascandleshoppe.com/2-Pack-Wax-Melts-s/1882.htm","http://www.papascandleshoppe.com/3-pack-wax-melts-s/1870.htm","http://www.papascandleshoppe.com/Soy-Candle-Wax-Melts-s/1514.htm","http://www.papascandleshoppe.com/Soy-Candle-Wax-Melts-s/1514.htm"]

for i in links:
    br.get(i)
    time.sleep(2)
    try:
        print "Viewing more items..."
        br.find_element_by_css_selector("select.results_per_page_select").click()
        time.sleep(1)
        viewmore = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"select.results_per_page_select option:nth-child(5)")))
        viewmore.click()
        time.sleep(2)
    except:
        print "Cannot view more items."
        
    try:
        WebDriverWait(br,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"a.productnamecolor.colors_productname")))
        item = br.find_elements_by_css_selector("a.productnamecolor.colors_productname")
    except:
        item = br.find_elements_by_css_selector("#content_area table:nth-child(6) tbody tr td table:nth-child(1) tbody tr td table tbody tr td div:nth-child(3) span a")
    
    for i in item:
        items.append(i.get_attribute("href"))
        print i.get_attribute("href")

    


for i in items:
    ls = []
    br.get(i)
    print "Navigating to:\n" + str(i)
    time.sleep(5)

    name = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"font.productnamecolorLARGE.colors_productname span")))
    sku = WebDriverWait(br,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"span.product_code")))
    cat = br.find_element_by_css_selector("td.vCSS_breadcrumb_td")
    try:
        desc = br.find_element_by_css_selector("span.Apple-style-span")
    except:
        desc = br.find_element_by_css_selector("#ProductDetail_ProductDetails_div")
    else:
        print "No description"
        desc = "None"

    try:
        options = br.find_element_by_css_selector("#options_table")
    except:
        print "No options available."
        options = "None"

    min = br.find_element_by_css_selector("input.v65-productdetail-cartqty")
    try:
        price = br.find_element_by_css_selector("div.product_productprice")
    except:
        continue
    try:
        image = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product_photo_zoom_url2")))
    except:
        image = WebDriverWait(br,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"img.vCSS_img_product_photo")))
    ls.append(name.text.encode("utf-8"))
    ls.append(sku.text.encode("utf-8"))
    ls.append(cat.text.encode("utf-8"))
    try:
        ls.append(desc.text.encode("utf-8"))
    except:
        ls.append(desc)
    # ls.append(variation)
    ls.append(min.get_attribute("value"))
    ls.append(price.text.encode("utf-8"))
    try:
        ls.append(image.get_attribute("href"))
    except:
        ls.append(image.get_attribute("src"))
    try:
        ls.append(options.text.encode("utf-8"))
    except:
        ls.append(options)
    table.append(ls)
    print ls


print "***Job Done***"        
        
outfile = open("./csv/outfile/papascandleshoppe1.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)