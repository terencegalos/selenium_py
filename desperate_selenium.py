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


url = "http://www.desperate.com/shophome.cfm"
uname = "rick@waresitat.com"
passw = "wolfville"



def init_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser
    
def init_login(driver,un,pw):
    br.get("https://www.ahomesteadshoppe.com/index.php?main_page=login")
    time.sleep(1)
    print "Logging in."
    
    driver.find_element_by_name("email_address").send_keys(un)
    driver.find_element_by_name("password").send_keys(pw)
    driver.find_element_by_css_selector("#loginForm div.buttonRow.forward input[type=\"image\"]").click()
    time.sleep(5)
    print "Logged in."

def get_info(driver,link,out):
    print "Navigating to: \n" + str(link)
    driver.get(link)
    time.sleep(1)  
    
    try:
        sku = driver.find_element_by_xpath("/html/body/table[3]/tbody/tr[1]/td[2]/div/center/table/tbody/tr/td[2]/form[1]/font/text()[3]")
    except:
        sku = "None"

    try:
        cats = []
        cat = driver.find_elements_by_css_selector("body table:nth-child(4) tbody tr:nth-child(1) td:nth-child(1) b")   
        for i in cat:
            cats.append(i.text.encode("utf-8"))
    except:
        cats = "None"
        
    dim = br.find_element_by_css_selector("div#productDetailsList").text.encode("utf-8")

    try:
        image = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#productMainImage a")))
        image = image.get_attribute("href")
    except:
        image = "none"
        

    ls = []
    

    ls.append(sku)
    
    ls.append(cats)
    
    ls.append(dim)

    ls.append(image)
    
    print ls
    
    out.append(ls)


    
    
####################################################################################################################################################################################################################################
    
                
br = init_driver()
time.sleep(1)

br.get(url)
print "Waiting for homepage to load..."
time.sleep(3)


items = []
table = []
cats = []
catstring = []

#click tin signs for more cats
br.find_element_by_link_text("+ Tin Signs").click()
time.sleep(2)

#get cat links
print "Getting all tin signs and displaying..."
cat = br.find_elements_by_partial_link_text("+")
for i in range(len(cat)-2):
    itm = cat[i].get_attribute("href")
    print itm
    cats.append(itm)
    catstring.append(cat[i].text.encode("utf-8"))
    
print "Tin sign links has been saved. Going each one for skus..."    

#go to each cats    
for i in range(len(cats)):
    print "Navigating to " + str(cats[i])
    br.get(cats[i])
    time.sleep(1)
    
    print "Displaying more items in a page..."
    try:
        br.find_element_by_css_selector("body table:nth-child(4) tbody tr:nth-child(1) td:nth-child(2) div center center:nth-child(14) form select option:nth-child(5)").click()
    except:
        print "\nAll items are in here. No need to get show more in this page. Printing each items' texts...\n"
        
        
        
    #scrape for sku first at least 1 time then repeat for the succeeding pages for more skus
    try:
        sku = br.find_elements_by_css_selector("body table:nth-child(4) tbody tr:nth-child(1) td:nth-child(2) div center table tbody tr td")
        for sk in sku:
            print sk.text        
        print "All items texts should have been displayed above."
        time.sleep(3)         
            
        
        for s in range(len(sku)):
            ls = []
            prodstring = sku[s].text.split()

            ls.append(prodstring[len(prodstring)-1])

            ls.append(catstring[i])
            print ls
            table.append(ls)
    except:
        sku = br.find_elements_by_css_selector("body table:nth-child(4) tbody tr:nth-child(1) td:nth-child(2) div center table:nth-child(11) tbody tr td")
        for sk in sku:
            print sk.text        
        print "All items texts should have been displayed above."
        time.sleep(3)           
            
        
        for s in range(len(sku)):
            ls = []
            prodstring = sku[s].text.split()

            ls.append(prodstring[len(prodstring)-1])

            ls.append(catstring[i])
            print ls
            table.append(ls)
        
    while True:
        try:
            nextbtn = br.find_element_by_name("Submit")
            next = nextbtn.get_attribute("value").split()
            if(next[0] == "Next"):
                nextbtn.click()
                print "More items found. Next page clicked.."
                time.sleep(1)
                
                try:
                    sku = br.find_elements_by_css_selector("body table:nth-child(4) tbody tr:nth-child(1) td:nth-child(2) div center table tbody tr td")
                    for sk in sku:
                        print sk.text        
                    print "All items texts should have been displayed above."
                    time.sleep(3)         
                        
                    
                    for s in range(len(sku)):
                        ls = []
                        prodstring = sku[s].text.split()

                        ls.append(prodstring[len(prodstring)-1])

                        ls.append(catstring[i])
                        print ls
                        table.append(ls)
                except:
                    sku = br.find_elements_by_css_selector("body table:nth-child(4) tbody tr:nth-child(1) td:nth-child(2) div center table:nth-child(11) tbody tr td")
                    for sk in sku:
                        print sk.text        
                    print "All items texts should have been displayed above."
                    time.sleep(3)           
                        
                    
                    for s in range(len(sku)):
                        ls = []
                        prodstring = sku[s].text.split()

                        ls.append(prodstring[len(prodstring)-1])

                        ls.append(catstring[i])
                        print ls
                        table.append(ls)
            else:
                break
                print "All page has been exhausted. Going to the next category..."
        except:
            print "This is the only page for this category. Going to the next category..."
            break

        
            
print "***Job Done***"
              
        
        
outfile = open("./csv/outfile/desperate_results.csv","wb")
writer = csv.writer(outfile)
writer.writerows(table)