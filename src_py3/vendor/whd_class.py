from helper import table_gateway
from helper import domainobject
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re

class whd(domainobject.domainobject):
    
    def __init__(self,driver,scraper_mode=None):
        super().__init__(driver)
        self.mode = scraper_mode

    vendor = "Wholesale Home decor (Harvest Scents)"
    url = "https://whdfloral.com/customer/account/login/"
    home = "http://whdfloral.com/"
    search = "https://whdfloral.com/catalogsearch/result/?q="
    uname = "rick@waresitat.com"
    passw = "Wolfville4"
    delay = 3
    links = []
    flag = True
    now = ""
    lastPage = "https://www.whdfloral.com/christmas-cardinal-house-flag-28x40in.html"
        
    def nextPage(self):
        
        try:
            while True:
                try:
                    self.driver.find_element(By.CSS_SELECTOR,"div.product.details.product-item-details > strong > a")
                    break
                except:
                    print("Marker not detected.")
                    self.driver.refresh()
                    self.time.sleep(1)
                    continue
            self.driver.find_elements(By.CSS_SELECTOR,"ul > li.item.pages-item-next > a")[-1].click()
            self.time.sleep(3) # 3 secs to load
            return True

        except:
            print("Page exhausted.")
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # print self.driver.find_element(By.CSS_SELECTOR,"#login-form").get_attribute("innerHTML")
        
        print("Logging in.")
        self.driver.find_element(By.CSS_SELECTOR,"#login-form #email").send_keys(self.uname)
        self.driver.find_element(By.CSS_SELECTOR,"#login-form #pass").send_keys(self.passw)
        self.driver.find_element(By.CSS_SELECTOR,"#login-form #pass").send_keys(Keys.ENTER)
        self.time.sleep(5)
        # self.driver.find_element(By.CSS_SELECTOR,"#login-form #pass").send_keys(Keys.ENTER)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#send2"))
        # self.driver.find_element(By.CSS_SELECTOR,"#send2").click()
        while True:
            inp = input("Enter yes if done.")
            if inp == "yes":
                # self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            else:
                continue
        
        print("Success.")
        self.time.sleep(5)

    def get_info(self,item=None):
        
        db = table_gateway.gateway()
        self.time.sleep(1)
        self.now = self.driver.current_url

        try:
            db.name = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[1]/div[2]/div/div[2]/h1/span'))).text
        except:
            return
            
        db.sku = self.driver.find_element(By.XPATH,'//*[@id="maincontent"]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[2]/div').text
        db.cat = ""
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#description > div > div").text.encode("utf-8")
        except:
            db.desc = ""

        try:
            db.stock = self.driver.find_element(By.XPATH,'//*[@id="maincontent"]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/span').text
        except:
            db.stock = ""

        # db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""

        try:
            db.min1 = self.driver.find_element(By.XPATH,'//*[@id="qty"]').get_attribute("value")
        except:
            db.min1 = 1

        try:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.old-price > span > span.price-wrapper > span").text.strip("$")
            db.sale = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-primary-column.product-shop.grid12-5.product-info-main > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.special-price > span > span.price-wrapper").text.strip("$")
        except:
            db.price1 = self.driver.find_element(By.XPATH,'//*[@id="maincontent"]/div[2]/div/div[1]/div[2]/div/div[3]/div[2]/span/span/span').text.strip("$")
        
        # WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-info-main"))).get_attribute("innerHTML")
        # print " ".join(WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.prices-tier li"))).text.split())
        # print " ".join(WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.prices-tier li"))).get_attribute("textContent").split())
        # try:
        #     db.min2 = " ".join(self.driver.find_elements(By.CSS_SELECTOR,"ul.prices-tier li")[0].get_attribute("textContent").split()).split()[1]
        #     db.price2 = " ".join(self.driver.find_elements(By.CSS_SELECTOR,"ul.prices-tier li")[0].get_attribute("textContent").split()).split()[3].strip("$")
        # except:
        db.min2 = ""
        db.price2 = ""
        # try:
        #     db.min3 = " ".join(self.driver.find_elements(By.CSS_SELECTOR,"ul.prices-tier li")[1].get_attribute("textContent").split()).split()[1]
        #     db.price3 = " ".join(self.driver.find_elements(By.CSS_SELECTOR,"ul.prices-tier li")[0].get_attribute("textContent").split()).split()[1][3].strip("$")
        # except:
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Harv400"
        # db.dir160 = "Harv160"
        # self.driver.execute_script("""
        # var jq = document.createElement('script');
        # jq.type = 'text/javascript';
        # jq.src = 'https://code.jquery.com/jquery-3.4.1.min.js';
        # jq.integrity = 'sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=';
        # jq.crossorigin = 'anonymous';
        # document.getElementsByTagName('head')[0].append(jq); """)

        # self.driver.execute_script('''
        #         if(document.readyState="Loading"){
        #             document.addEventListener("DOMContentLoaded",function(){
        #                 var img=document.querySelector("#product_addtocart_form > div > div.product-left.col-sm-12"); 
        #                 img.parentNode.removeChild(img);
        #             });
        #         }
        # ''')
        
        # WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#product_addtocart_form > div > div.product-left.col-sm-12"))) #detect items for 3 seconds
        # WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-img-column"))) #detect items for 3 seconds
        # self.driver.execute_script('window.stop(); var img=document.querySelector("#maincontent > div.columns > div > div.product-view.product-columns-wrapper > div.product-img-column"); img.parentNode.innerHTML = "<script type=text/javascript></script>";')
        # db.img400 = "http://imagecat/imagename.jpg"

        try:
            db.img400 = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="magnifier-item-0"]'))).get_attribute("src")
        except:
            db.img400 = "http://imagecat/imagename.jpg"

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Harv800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row):
        
        new_2025 = ['https://www.whdfloral.com/everyday.html','https://www.whdfloral.com/pottery-vases.html','https://www.whdfloral.com/seasonal/everyday.html']
        
        self.links = []

        # print("\nSearching for item: " + row+"\n")
        # print(self.search+row)
        
        
        for link in new_2025:

            self.driver.get(link)#self.search+row)
            self.time.sleep(1)

            items = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"div.product.details.product-item-details > strong > a") if i.get_attribute("href") not in self.links]
            print(items)
            self.links.extend(items)
            while self.nextPage():
                items = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"div.product.details.product-item-details > strong > a") if i.get_attribute("href") not in self.links]
                print(items)
                self.links.extend(items)
                
                
            
        if len(self.links) > 0:
            results = set(self.links)
            print(f"Total: {len(results)}")
            return results
        
        
            
        return

        # self.driver.get(r'https://whdfloral.com/catalogsearch/result/?q=" "')
        # https://whdfloral.com/catalogsearch/result/?q=""