from helper import table_gateway
from helper import domainobject
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
    lastPage = None
        
    def nextPage(self):
        next_link = None
        try:
            self.driver.find_element(By.CSS_SELECTOR,"div.product.details.product-item-details > strong > a") # check if items exist
            
            print("Navigating to next page...")
            next_link = self.driver.find_elements(By.CSS_SELECTOR,"ul > li.item.pages-item-next > a")[-1]
            next_link.click()
            self.time.sleep(3) # 3 secs to load
            return True
        except:
            print("Page exhausted.")
            return False

    def init_login(self, un, pw):
        self.driver.get(self.url)
        self.time.sleep(2)
        
        print("Logging in...")
        
        try:
            # Try multiple selectors for email field
            try:
                email_field = self.driver.find_element(By.CSS_SELECTOR, "#login-form #email")
            except NoSuchElementException:
                try:
                    email_field = self.driver.find_element(By.ID, "email")
                except NoSuchElementException:
                    email_field = self.driver.find_element(By.NAME, "login[username]")
            
            # Try multiple selectors for password field
            try:
                pass_field = self.driver.find_element(By.CSS_SELECTOR, "#login-form #pass")
            except NoSuchElementException:
                try:
                    pass_field = self.driver.find_element(By.ID, "pass")
                except NoSuchElementException:
                    pass_field = self.driver.find_element(By.NAME, "login[password]")
            
            email_field.send_keys(self.uname)
            pass_field.send_keys(self.passw)
            pass_field.send_keys(Keys.ENTER)
            
            self.time.sleep(5)
            
        except Exception as e:
            print(f"Login form error: {e}")
            print("Please login manually in the browser...")
        
        # Manual confirmation for CAPTCHA or verification
        while True:
            inp = input("Login complete? Enter 'yes' to continue: ")
            if inp.lower() == "yes":
                self.time.sleep(1)
                break
            else:
                continue
        
        print("Login successful.")
        self.time.sleep(3)

    def get_all_items(self, cat_num=None):
        """Scrape all product URLs from WHD categories"""
        print("Starting sitewide scraping for Wholesale Home Decor...")
        
        # Main navigation links from homepage (priority order from nav bar)
        categories = [
            'https://www.whdfloral.com/new-2024.html',      # New 2025
            'https://www.whdfloral.com/everyday-decor.html',       # Florals
            'https://www.whdfloral.com/seasonal/fall.html',      # Fall
            'https://www.whdfloral.com/seasonal/christmas.html',      # Christmas
            'https://www.whdfloral.com/seasonal/spring.html', # Spring
        ]
        
        # If cat_num provided, only scrape that many categories
        if cat_num:
            categories = categories[:int(cat_num)]
        
        print(f"Processing {len(categories)} categories...")
        
        for i, category_url in enumerate(categories, 1):
            print(f"\n[{i}/{len(categories)}] Processing category: {category_url}")
            
            try:
                self.driver.get(category_url)
                self.time.sleep(self.delay)
                
                # Get items from first page
                try:
                    items = [
                        item.get_attribute("href") 
                        for item in self.driver.find_elements(By.CSS_SELECTOR, "div.product.details.product-item-details > strong > a")
                        if item.get_attribute("href") and item.get_attribute("href") not in self.links
                    ]
                    print(f"Found {len(items)} products on page 1")
                    self.links.extend(items)
                except Exception as e:
                    print(f"Error getting items from page: {e}")
                
                # Paginate through remaining pages
                page_num = 1
                while self.nextPage():
                    page_num += 1
                    print(f"Processing page {page_num}...")
                    try:
                        items = [
                            item.get_attribute("href") 
                            for item in self.driver.find_elements(By.CSS_SELECTOR, "div.product.details.product-item-details > strong > a")
                            if item.get_attribute("href") and item.get_attribute("href") not in self.links
                        ]
                        print(f"Found {len(items)} products on page {page_num}")
                        self.links.extend(items)
                    except Exception as e:
                        print(f"Error getting items from page {page_num}: {e}")
                        break
                
            except Exception as e:
                print(f"Error processing category {category_url}: {e}")
                continue
        
        # Remove duplicates
        self.links = list(set(self.links))
        print(f"\n✓ Total unique products found: {len(self.links)}")
        return self.links
                
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
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#description > div > div").text
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
        
        
    def search_item(self, row):
        """Search for a specific item by SKU or keyword"""
        print(f"Searching for item: {row}")
        
        self.links = []  # reset links
        
        # Navigate to search results
        search_url = f"{self.search}{row}"
        print(f"Navigating to: {search_url}")
        
        self.driver.get(search_url)
        self.time.sleep(self.delay)
        
        try:
            # Get items from first page
            items = [
                i.get_attribute("href") 
                for i in self.driver.find_elements(By.CSS_SELECTOR, "div.product.details.product-item-details > strong > a")
                if i.get_attribute("href") and i.get_attribute("href") not in self.links
            ]
            print(f"Found {len(items)} items on page 1")
            self.links.extend(items)
            
            # Paginate if needed
            while self.nextPage():
                items = [
                    i.get_attribute("href") 
                    for i in self.driver.find_elements(By.CSS_SELECTOR, "div.product.details.product-item-details > strong > a")
                    if i.get_attribute("href") and i.get_attribute("href") not in self.links
                ]
                print(f"Found {len(items)} items")
                self.links.extend(items)
        except Exception as e:
            print(f"Error during search: {e}")
            return None
        
        # Remove duplicates and return
        if len(self.links) > 0:
            results = list(set(self.links))
            print(f"Total unique results: {len(results)}")
            return results
        
        print("No results found")
        return None