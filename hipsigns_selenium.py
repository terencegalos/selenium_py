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


url = "http://www.lorriepowellstudios.com/files/8-2015_INSPIRATIONAL.html"
uname = "rick@waresitat.com"
passw = "wolfville"



def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    browser.maximize_window()
    return browser
    
def init_login(driver,un,pw):
    br.get(url)
    time.sleep(2)
    print "Clicking login link..."
    btn = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#container div.Object102 a img")))
    btn.click()
    time.sleep(1)
    print "Logging in."
   
    uname = WebDriverWait(driver,30).until(EC.visibility_of_element_located((By.ID,"username")))
    uname.send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_css_selector("#login_form div.sc_login button").click()
    time.sleep(20)
    print "Logged in."



br = init_driver()
br.get(url)
time.sleep(10)




items = []
table = []

    
links = ["http://www.lorriepowellstudios.com/files/5-2015_COOL_GRAND_GALS.html","http://www.lorriepowellstudios.com/files/6-2015_COOL_GRAND_GUYS.html","http://www.lorriepowellstudios.com/files/7-2015_GRIN_AND_BEAR_IT.html","http://www.lorriepowellstudios.com/files/8-2015_INSPIRATIONAL.html","http://www.lorriepowellstudios.com/files/9-2015_GALS.html","http://www.lorriepowellstudios.com/files/10-2015_GUYS.html","http://www.lorriepowellstudios.com/files/11-2015_FRIENDSHIP.html","http://www.lorriepowellstudios.com/files/12-2015_HUMOROUS.html","http://www.lorriepowellstudios.com/files/13-2015_HOUSEHOLD.html","http://www.lorriepowellstudios.com/files/14-2015_LODGE.html","http://www.lorriepowellstudios.com/files/15-2015_COUNTRY_COWBOY_COWGIRL.html","http://www.lorriepowellstudios.com/files/16-2015_BEACH.html","http://www.lorriepowellstudios.com/files/17-2015_RETIREMENT.html","http://www.lorriepowellstudios.com/files/18-2015_BEVERAGES_WINE.html","http://www.lorriepowellstudios.com/files/19-2015_PETS.html"]
    
for link in links:
    br.get(link)
    time.sleep(1)
    
    WebDriverWait(br,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div#root div img")))
    img = br.find_elements_by_xpath("//img[contains(@width,'180')]")
    att = br.find_elements_by_xpath("//table[contains(@width,'180')]")
    
    for x in range(len(img)):
        ls = []
        image = img[x].get_attribute("src")        
        prop = att[x].text.encode("utf-8")
        
        ls.append(prop)
        ls.append(image)
        table.append(ls)
        print ls
            
            
print "***Job Done***"        
        
outfile = open("./csv/outfile/hipsigns_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)