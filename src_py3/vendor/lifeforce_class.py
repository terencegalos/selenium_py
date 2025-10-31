from helper import table_gateway
from helper import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class lifeforce(domainobject.domainobject):

    def __init__(self,driver,mode):
        super().__init__(driver)
        self.mode = mode
        self.links = []

    vendor = "Lifeforce"
    url = "https://lifeforceglass.com/sitemap/categories"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    lastStop = "https://lifeforceglass.com/jesus-our-shepherd/"
        
    def init_login(self,un,pw):
        # try:
        #     self.driver.find_element_by_css_selector("#JS_PROD > div.content-container > div > div > div > div.row > div.col-sm-7 > div.well.well-prod > a").click()
        # except:
            # self.driver.get(self.url)
        # self.time.sleep(3)
        self.driver.get(self.url)
        self.time.sleep(self.delay)
        
        # print("Logging in.")
        # self.driver.find_element(By.NAME,"Customer_LoginEmail").send_keys(un)
        # self.driver.find_element(By.NAME,"Customer_Password").send_keys(pw)
        # self.driver.find_element(By.NAME,"Customer_Password").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        print("Success.")

    def save_info(self,item=None):
        db = table_gateway.gateway()
        try:
            db.name = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-details > form > div.product-details-top > h1").text
        except:
            print("Item not found!")
            return
        try:
            db.sku = self.driver.execute_script("return BCData.product_attributes.sku;")
        except:
            print("SKU not found!")
            return
        try:
            db.cat = "|".join([a.text for a in self.driver.find_elements(By.CSS_SELECTOR,"body > section > div.page-wrap > main > section.breadcrumbs > a")])
        except:
            db.cat = ""
        db.desc = self.driver.find_element(By.CSS_SELECTOR,"#description").text
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-details > form > div.product-details-top > div.product-details-price > div.lifeforce-product-page-quantity-pricing-wrapper > div.js-pricing-table > div > table > tbody > tr:nth-child(1) > td:nth-child(1)").text.split()[0]
        except:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-details > form > div.product-details-top > span > input").get_attribute("value")
        try:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-details > form > div.product-details-top > div.product-details-price > div.lifeforce-product-page-quantity-pricing-wrapper > div.js-pricing-table > div > table > tbody > tr:nth-child(1) > td:nth-child(2)").text.strip("$")
        except NoSuchElementException:
            try:
                db.price1 = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-details > form > div.product-details-top > div.product-details-price > div.price > div > div > span.price-value").text.strip("$")
            except NoSuchElementException:
                return
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-details > form > div.product-details-top > div.product-details-price > div.lifeforce-product-page-quantity-pricing-wrapper > div.js-pricing-table > div > table > tbody > tr:nth-child(2) > td:nth-child(1)").text.split()[0]
        except NoSuchElementException:
            db.min2 = ""
        except IndexError:
            db.min2 = ""
        try:
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-details > form > div.product-details-top > div.product-details-price > div.lifeforce-product-page-quantity-pricing-wrapper > div.js-pricing-table > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text.strip("$")
        except NoSuchElementException:
            db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Lifeforce400"
        db.dir160 = "Lifeforce160"
        img_element = None
        try:
            img_element = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-image > div.product-image-main-image.flickity-enabled.is-draggable > div > div > img.product-main-image-slide.flickity-lazyloaded.is-selected")
        except NoSuchElementException:
            try:
                img_element = self.driver.find_element(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.single-product > section.product-image > div.product-image-main-image.flickity-enabled > div > div > img")
            except NoSuchElementException:
                print("Image not found!")
        finally:
            if img_element is not None:
                db.img400 = self.driver.execute_script("return arguments[0].getAttribute('data-flickity-lazyload-src') || arguments[0].src;", img_element)
            else:
                print("Image element is None!")
                return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Lifeforce800"
        db.img800 = db.img160
        print(db)
        return db

    def get_info(self,item=None):
        db = self.save_info()
        return db
        # while True:
        #     try:
        #         db = self.save_info()
        #         return db
        #         break
        #     except:
        #         self.init_login(self.uname,self.passw)
        #         db = self.save_info()
        #         return db
        #         break       
        
    def get_categories(self):
        return [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"body > section > div.page-wrap > main > section > div.sitemap-container > div > ul li a")]
    
    def get_items(self):
        items = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR,"body > section > div.page-wrap > main > div.product-listing.products-section-grid > article > div.product-item-details > h1 > a")]
        return items
    
    def next_page(self):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR,".listing-pagination-link.next")
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", element)
            self.time.sleep(1)  # Allow time for smooth scroll
            element.click()
            self.time.sleep(1)
            return True
        except:
            return False
        
    def get_all_items(self):
        categories = self.get_categories()
        print(f"Found {len(categories)} categories")
        for cat in categories:
            print(f"Getting items for category: {cat}")
            self.driver.get(cat)
            self.time.sleep(self.delay)
            items = self.get_items()
            print(f"Found {len(items)} items")
            self.links = self.links + items
            while self.next_page():
                items = self.get_items()
                print(f"Found {len(items)} items")
                self.links = self.links + items
        self.links = list(set(self.links))
        print(f"Found {len(self.links)} total items")
        return self.links
    
        
    
    def search_item(self,row):
        
        # print("\nSearching for item: " + row+"\n")
        # if len(row.split(",")[1].strip()) > 1:
        # while True:
        #     try:
        #         self.driver.find_element(By.NAME,"Search").clear()
        #         self.driver.find_element(By.NAME,"Search").send_keys(row)
        #         self.driver.find_element(By.NAME,"Search").send_keys(Keys.ENTER)
        #         self.time.sleep(2)
        #         break
        #     except Exception as e:
        #         print("Search fail:")
        #         print(e)
        #         self.driver.refresh()
        #         self.time.sleep(1)
        #         continue
        try:
            # items = [i.get_attribute("href") for i in self.driver.find_elements(By.CSS_SELECTOR,"#JS_SRCH > div.content-container > div > div > div > div.row.row-masonry > div.ctgy-item > a")]
            # return items
            items = self.get_all_items()
            return items
        except:
            return None
            

