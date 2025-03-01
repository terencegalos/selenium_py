from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
import logging,sys,re

logging.basicConfig(level=logging.INFO,stream=sys.stdout)

class surfsup(domainobject):

    vendor = "Surfs Up Candles"
    url = "https://www.surfsupcandle.com/"
    uname = "terence@waresitat.com"
    passw = "wolfville"
    delay = 1
    is_overlay_removed = False
    last_stop = 'https://www.surfsupcandle.com/products/gift-certificate?_pos=1426&_sid=c52f9987b&_ss=r'
    all = []
    
        
    def init_login(self,un,pw):
        # print("Logging in.")
        # self.driver.get("https://www.surfsupcandle.com/customer_authentication/redirect?locale=en&region_country=US")
        # self.driver.get(self.url)
        # self.time.sleep(1)
        # resp = 'n'
        # while resp != 'y':
        #     resp = input('Overlay shown?')
        # self.driver.find_element(By.XPATH,'/html/body/div[14]/div[2]/div[2]/div/div/div/div/div/form/div[2]/div/img').click()
        print("Login success.")

    def pagination(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR,"[rel=next]").click()
            self.time.sleep(2)
            return True
        except:
            print("No pages left.")
            return False
        
    def click_size(self,el):
        while True:
                try:
                    el.click()
                    self.time.sleep(0.3)
                    break
                    
                except ElementClickInterceptedException:
                    logging.info('Overlay intercepting. Click manually')
                    res = input('Done? ')
                    while res.lower() != 'y':
                        continue
        
    def select_size(self):
        size_results = []
        try:
            size_wrapper = self.driver.find_elements(By.CSS_SELECTOR,'div.block-swatch-list')[0]
        except IndexError:
            logging.info('No size option. Extracting info directly.')
            result = self.extract_info()
            size_results.append(result)
            return size_results
        # logging.info(f"innerhtml:{size_wrapper.get_attribute('innerHTML')}")
        
        sizes = size_wrapper.find_elements(By.CSS_SELECTOR,'div')
        # Rotate sizes
        for size in sizes:
            # logging.info(f"size: {size.get_attribute('innerHTML')}")
            self.click_size(size)
            results = self.select_scents()
            
            if results is not None:
                size_results.extend(results)
            # If there are no scent options, extract data directly
            else:
                result = self.extract_info()
                size_results.append(result)
            
        return size_results
            
            
            
    def select_scents(self):
        scent_results = []
        logging.info(f"Rotate: scents")
        try:
            scent_wrapper = self.driver.find_elements(By.CSS_SELECTOR,'div.block-swatch-list')[1]
            scents = scent_wrapper.find_elements(By.CSS_SELECTOR,'div')
            for scent in scents:
                scent.click()
                self.time.sleep(0.5)
                result = self.extract_info()
                scent_results.append(result)
                
            return scent_results
        
        except IndexError:
            logging.info(f"No scents to choose")
            
            
            
    def get_info(self,item=None):
        logging.info(self.driver.current_url)
        print('Rotate: size')
        results = self.select_size()
        return results
        
        
            

    def extract_info(self,item=None):
        
        db = gateway()
        db.name = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[2]/product-meta/h1').text
        db.sku = db.name
        db.cat = ""
        try:
            db.desc = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[2]/div/div[5]/div').text
        except NoSuchElementException:
            try:
                db.desc = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[2]/div/div[5]').text
            except NoSuchElementException:
                db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        try:
            db.size = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[2]/div/product-variants/div[1]/div[1]/span[2]').text
        except NoSuchElementException:
            db.size = ""
        db.seller = ""
        db.min1 = 3
        try:
            full_text = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[2]/product-meta/div/div[1]/span').get_attribute('textContent').strip()
            price_match = re.search(r'\$\d+.\d+',full_text)
            db.price1 = price_match.group(0) if price_match else ""
        except NoSuchElementException:
            db.price1 = 99
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 3
        db.dir400 = "Surfs400"
        db.dir160 = "Surfs160"
        try:
            db.img400 = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[1]/product-media/div/flickity-carousel/div/div/div[contains(@class, "is-selected") and contains(@class, "product__media-item")]/div/img').get_attribute("src")
        except NoSuchElementException:
            try:
                db.img400 = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[1]/product-media/div/flickity-carousel/div/div/img').get_attribute("src")
            except NoSuchElementException:
                db.img400 = 'No image.jpg'
        db.img160 = db.img400.split("/")[-1:][0]
        try:
            db.desc2 = self.driver.find_element(By.XPATH,'//*[@id="main"]/div[1]/section/div/div/div[2]/div/product-variants/div[2]/div[1]/span[2]').text
        except NoSuchElementException:
            db.desc2 = ""
        db.option = ""
        db.dir800 = "Surfs800"
        db.img800 = db.img160
        print(db)
        return db
        
        
    def search_item(self,row=None):
        
        print("\nSearching for item: " + str(row)+"\n")
        # for x in range(6):
        #     self.driver.find_element(By.CSS_SELECTOR,"html body").send_keys(Keys.PAGE_DOWN)
        # self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.XPATH,"//*[@id='main']/div/div[1]/div[1]/div/div[7]/div[2]/div[2]/div[3]")).perform()
        # self.time.sleep(2)
        # items = [i.get_attribute("href") for i in self.driver.find_elements(By.XPATH,"//*[@id='main']/div/div[1]/div[1]/div/div[7]/div[1]/div[2]/section/a")]
        self.driver.get('https://www.surfsupcandle.com/search?type=product&q=*')
        
        items = [i.get_attribute("href") for i in self.driver.find_elements(By.XPATH,'//*[@id="facet-main"]/product-list/div/product-item/div[2]/div/a')]
        print(items)
        
        self.driver.execute_script("window.scrollTo(0,0);")
        self.all.extend(items)
        
        while True:
            if not self.is_overlay_removed:
                logging.info("Close email subscription popup...")
                res = input('Closed? ')
                if res.lower() != 'y':
                    continue
                self.is_overlay_removed = True
            break
            
        
        while self.pagination():
            items = [i.get_attribute("href") for i in self.driver.find_elements(By.XPATH,'//*[@id="facet-main"]/product-list/div/product-item/div[2]/div/a')]
            print(items)
            
            self.driver.execute_script("window.scrollTo(0,0);")
            self.all.extend(items)
            
        if self.last_stop:
            start_index = self.all.index(self.last_stop)
            return self.all[start_index:]
        return self.all

