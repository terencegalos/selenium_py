from helper.table_gateway import gateway
from helper.domainobject import domainobject
import datetime,csv

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException as StateElementReferenceException

class ragon(domainobject):
    
    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode

    vendor = "Ragon House Collection"
    url = "http://ragonhouse.com/"
    home = "http://ragonhouse.com/"
    login = "https://ragonhouse.com/login.php"
    uname = "rick@waresitat.com"
    passw = "ragonhouse1"
    lastStop =  ""
    sitemap = 'https://ragonhouse.com/collections/'
    flag = False
    delay = 1
    counter = 190
    items = []
    links = []

    def export_all_product_urls(self, items):
        with open('./csv/outfile/' + self.vendor + '_product_urls.csv','wb') as ragon_file:
            writer = csv.writer(ragon_file)
            for item in items:
                writer.writerow([item])

    def nextPage(self):        
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR,"#product-listing-container > nav > ul > li.pagination-item.pagination-item--next > a")
            self.driver.execute_script("arguments[0].click();", next_button)
            self.time.sleep(2)
            return True
        except NoSuchElementException:
            # No more button mean no more pages
            print("No more pages.")
            return False
        except StateElementReferenceException:
            print("No more pages.")
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#sw_dropdown_2878 > a")).perform()
        # self.time.sleep(1)
        self.driver.find_element(By.XPATH,"/html/body/header/nav/ul/li[3]/a[1]").click()
        self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#account_info_2878 > div.ty-account-info__buttons.buttons-container > a.cm-dialog-opener.cm-dialog-auto-size.ty-btn.ty-btn__secondary").click()

        # self.time.sleep(1)
        print("Logging in...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_email"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(Keys.ENTER)
        self.time.sleep(3)
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > h1").text
        if not db.name:
            return

        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > dl.productView-custom > dd").text
        db.cat = "|".join([c.text for c in self.driver.find_elements(By.CSS_SELECTOR,"#main-content > div.container > nav > ol > li.breadcrumb > a > span")])
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#tab-description").text
        except:
            db.desc = ""
        try:
            db.stock = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > div.productView-availability > dd").text
        except:
            db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > div.productView-dimensions").text
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.XPATH,'//*[@id="qty[]"]').get_attribute('value')
        except:
            db.min1 = ""
        try:
            db.price1 = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div/div[1]/section[2]/div/div[1]/div[3]/span[3]').text
        except:
            db.price1 = ""
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > thead > tr > th:nth-child(3)").text.strip("+")
        except:
            db.min2 = ""
        try:
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > tbody > tr > td:nth-child(3) > bdi > span").text
        except:
            db.price2 = ""
        try:
            db.min3 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > thead > tr > th:nth-child(4)").text.strip("+")
        except:
            db.min3 = ""
        try:
            db.price3 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > tbody > tr > td:nth-child(4) > bdi > span").text
        except:
            db.price3 = ""
        try:
            db.multi = self.driver.find_element(By.XPATH,'//*[@id="qty[]"]').get_attribute('value')
        except:
            db.multi = ""
        db.dir400 = "Ragon400"
        db.dir160 = "Ragon160"
        #ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#fancybox-wrap")).perform()
        #self.time.sleep(1)
        try:
            db.img400 = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div.container > div > div.productView > section.productView-images > figure > div > a"))).get_attribute("href")
        except:
            return
        db.img160 = db.img400.split("/")[-1:][0]
        try:
            db.desc2 = self.driver.find_element(By.CSS_SELECTOR,"#content_description").text
        except:
            db.desc2 = ""
        db.option = ""
        db.dir800 = "Ragon800"
        db.img800 = db.img160
        print(db)
        return db


    def search_item(self,row=None):
        everydayfloral = ("https://ragonhouse.com/everyday/", "https://ragonhouse.com/rh-floral/")
        self.driver.get('https://ragonhouse.com/sitemap')

        allSeasons = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > ul > li:nth-child(2) > ul")
        allSeasons = [a.get_attribute("href") for a in allSeasons.find_elements(By.TAG_NAME,"a")]
        print(allSeasons)
        
        self.items = []
        # if row:
        #     print("\nSearching for item: " + row+"\n")
        #     while True:
        #         try:
        #             self.driver.find_element(By.CSS_SELECTOR,"#quick-search-expand").click()
        #             self.time.sleep(1)
        #             self.driver.find_element(By.NAME,"nav-quick-search").clear()
        #             self.driver.find_element(By.NAME,"nav-quick-search").send_keys(row)
        #             self.driver.find_element(By.NAME,"nav-quick-search").send_keys(Keys.ENTER)
        #             self.time.sleep(1)
        #             # self.driver.get("https://ragonhouse.com/index.php?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&q=+&dispatch=products.search&page=16")
        #             break
        #         except Exception as e:
        #             print(e)
        #             self.driver.refresh()
        #             self.time.sleep(1)
        #             continue
        # else:
        #     self.driver.get(self.sitemap)
        #     self.time.sleep(1)
        
        def extract_urls():
            # print("Loading...")
            # self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # self.time.sleep(1)
            # item = [a.get_attribute("href") for a in self.driver.find_elements(By.XPATH,'//*[@id="product-listing-container"]/div[1]/ul/li/article/div/h3/a')]
            # print("\n".join(item))
            # if item:
            #     return item
            # return False
            
            # load items first that are lazy loaded before extracting URLs - it might load more items if we scroll down
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.time.sleep(2)
                item = [a.get_attribute("href") for a in self.driver.find_elements(By.XPATH,'//*[@id="product-listing-container"]/div[1]/ul/li/article/div/h3/a')]
                if len(item) >= self.counter: # if no more new items loaded, break the loop
                    break
                self.counter = len(item)
            print("\n".join(item))
            if item:
                return item
            return False
        
        def get_unique(items):
            unique = [item for item in items if item not in self.items]
            return unique

        for page in allSeasons: # loop through the pages
            # Extract item URLs from the page
            print("Extracting page: %s",page)
            self.driver.get(page)
            self.time.sleep(1)
            items = extract_urls() # get all items in the page
            if not items: # if no items found, skip to the next page
                print("No items found.")
                continue
            unique = get_unique(items) # get unique items
            self.items.extend(unique) # add unique items to the list
            # previous_items = set(self.items)
            # Continue to extract more items until no new items are found
            # while True: 
            #     try:
            #         items = extract_urls()
            #         unique = get_unique(items)
            #         if not items or set(unique).issubset(previous_items):
            #             break
            #         self.items.extend(unique)
            #         previous_items = set(self.items)
            #         continue
            #     except Exception as e:
            #         print(e)
            #         break

        # self.items.extend(item)

            while self.nextPage():
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.time.sleep(2)
                try:
                    item = [a.get_attribute("href") for a in WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.card-title a')))]
                except:
                    item = []
                print(item)
                self.items.extend(item)

        return list(set(self.items))

    def get_links(self):
        """Return product links found on the current listing page."""
        try:
            items = [a.get_attribute("href") for a in self.driver.find_elements(By.XPATH,'//*[@id="product-listing-container"]/div[1]/ul/li/article/div/h3/a')]
        except:
            # fallback selector
            items = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR, '.card-title a')]
        print(items)
        return items

    def get_all_items(self):
        """Crawl the sitemap/collections, collect product URLs from each collection and paginate."""
        # go to sitemap to read collection links
        try:
            self.driver.get('https://ragonhouse.com/sitemap')
            self.time.sleep(1)
            # the sitemap stores collections in a nested list; target the second list as in search_item
            container = self.driver.find_element(By.CSS_SELECTOR, "#main-content > div.container > ul > li:nth-child(2) > ul")
            cats = [a.get_attribute('href') for a in container.find_elements(By.TAG_NAME, 'a')]
        except Exception:
            # fallback to the collections landing page
            cats = [self.sitemap]

        self.links = []
        for cat in cats:
            print(cat)
            try:
                self.driver.get(cat)
                self.time.sleep(1)
            except Exception:
                continue

            # gather links on the first page
            try:
                self.links.extend(self.get_links())
            except Exception:
                pass

            # paginate and gather more
            while self.nextPage():
                self.time.sleep(1)
                try:
                    self.links.extend(self.get_links())
                except Exception:
                    break

        return list(set(self.links))
