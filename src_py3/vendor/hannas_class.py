from helper.table_gateway import gateway
from helper.domainobject import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class hannas(domainobject):

    def __init__(self, driver, scraper_mode=None):
        # Initialize base domainobject which will call init_login using
        # class-level uname/passw attributes. Store optional mode.
        super().__init__(driver)
        self.mode = scraper_mode

    vendor = "Hanna's Handiworks"
    products = "https://www.hannashandiworks.com/products.html"
    url = "http://www.hannashandiworks.com/"
    home = "http://www.hannashandiworks.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    lastStop = ""
    delay = 1
    flag = 0
    
    links = [] #for scraper; links to all items
    
        
    def nextPage(self):
        try:
            # self.driver.find_elements(By.CSS_SELECTOR,"a[title=Next]")[-1:].click()
            # self.driver_execute_script("window.scrollTo(0,document.body.scrollHeight)")
            self.time.sleep(5)
            self.driver.find_element(By.CSS_SELECTOR,"body").send_keys(Keys.END)
            self.time.sleep(5)
            self.driver.find_element(By.CSS_SELECTOR,"#layer-product-list > div:nth-child(4) > div.pages > ul > li.item.pages-item-next > a").click()
            return True
        except:
            print("Page exhausted.")
            return False

    def get_all_items(self):
        """
        Scrape product categories and paginate through each to collect all product links.
        Replaces the sitemap approach with category-based scraping.
        """
        print("Navigating to products page to extract categories...")
        self.driver.get(self.products)
        self.time.sleep(self.delay)
        
        # Extract category links from the products page
        # Common selectors: nav menu, sidebar, or category list
        # Adjust CSS selectors based on site structure
        categories = []
        
        try:
            # Try to find category links in the main navigation or sidebar
            # Attempt multiple selectors for robustness
            category_elements = self.driver.find_elements(By.CSS_SELECTOR, "nav a[href*='/products/']")
            
            if not category_elements:
                category_elements = self.driver.find_elements(By.CSS_SELECTOR, ".category-links a, .sidebar a[href*='/products/']")
            
            if not category_elements:
                # Fallback: look for any links in a categories section
                category_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='products']")
            
            # Filter and deduplicate category URLs
            for elem in category_elements:
                href = elem.get_attribute("href")
                if href and "/products/" in href and href not in categories:
                    categories.append(href)
                    
            # If no categories found, default to the main products page
            if not categories:
                print("No categories found, using main products page")
                categories = [self.products]
            else:
                print(f"Found {len(categories)} categories: {categories[:5]}..." if len(categories) > 5 else f"Found {len(categories)} categories: {categories}")
                
        except Exception as e:
            print(f"Error extracting categories: {e}")
            categories = [self.products]
        
        # Iterate through each category and paginate
        for category_url in categories:
            print(f"\nScraping category: {category_url}")
            self.driver.get(category_url)
            self.time.sleep(self.delay)
            
            page_num = 1
            while True:
                print(f"  Page {page_num}...")
                
                try:
                    # Extract product links from current page
                    # Adjust selector based on site structure
                    product_elements = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        "#layer-product-list a.product-item-link, .product-item a.product-item-photo, .product-item-details a"
                    )
                    
                    page_products = []
                    for elem in product_elements:
                        href = elem.get_attribute("href")
                        if href and ".html" in href and href not in self.links:
                            page_products.append(href)
                            self.links.append(href)
                    
                    print(f"    Found {len(page_products)} products on this page")
                    
                    if not page_products:
                        print("    No products found on this page, moving to next category")
                        break
                    
                    # Try to go to next page
                    if not self.nextPage():
                        break
                    
                    page_num += 1
                    
                except Exception as e:
                    print(f"    Error on page {page_num}: {e}")
                    break
        
        print(f"\nTotal products collected: {len(self.links)}")

    def init_login(self,un,pw):
        self.driver.get("https://www.hannashandiworks.com/customer/account/login/")
        self.time.sleep(1)
        
        print("Logging in.")
        
        # self.driver.find_element(By.CSS_SELECTOR,"#store\.menu > nav > ul > li:nth-child(7) > a").click()
        self.time.sleep(1)
        self.driver.find_element(By.NAME,"login[username]").send_keys(un)
        self.driver.find_element(By.NAME,"login[password]").send_keys(pw)
        self.driver.find_element(By.NAME,"login[password]").send_keys(Keys.ENTER)
        # self.driver.execute_script('document.querySelector("input[type=password]").setAttribute("value",arguments[0])',pw)
        # self.driver.execute_script('document.forms[0].submit();')
        self.time.sleep(1)
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.page-title-wrapper.product > h1 > span").text
        except:
            # self.time.sleep(3)
            # self.driver.refresh()
            # self.time.sleep(1)
            # db.name = self.driver.find_element(By.CSS_SELECTOR,"#product_addtocart_form > div.product-shop > div.product-name > span.h1").text
            return None

        db.sku = WebDriverWait(self.driver,2).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.product-info-stock-sku > div.product.attribute.sku > div"))).text
        db.cat = ""
        try:
            # keep description as text (str) under Python 3
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#description > div").text
        except:
            db.desc = ""
        try:
            db.stock = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.product-info-stock-sku > div.stock.available > span:nth-child(2)").text
        except:
            db.stock = ""
        try:
            db.sale = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.special-price > span > span.price-wrapper > span").text
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        try:
            db.size = self.driver.find_element(By.CSS_SELECTOR,"#description > div").text
        except:
            db.size = ""
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.CSS_SELECTOR,"#qty").get_attribute("value")
        except:
            db.min1 = "NA"
        try:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span.old-price > span > span.price-wrapper > span").text
        except:
            db.price1 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > div.product-info-price > div.price-box.price-final_price > span > span > span").text
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(1)").text.split()[1]
        except:
            db.min2 = ""
        try:
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(1)").text.split()[3]
        except:
            db.price2 = ""
        try:
            db.min3 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(2)").text.split()[1]
        except:
            db.min3 = ""
        try:
            db.price3 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product-info-main > ul > li:nth-child(2)").text.split()[3]
        except:
            db.price3 = ""
            
        db.multi = db.min1
        db.dir400 = "Hannas400"
        db.dir160 = "Hannas160"
        try:
            db.img400 = self.driver.find_element(By.CSS_SELECTOR,"img.fotorama__img").get_attribute("src")
        except:
            try:
                db.img400 = self.driver.find_element(By.CSS_SELECTOR,"#maincontent > div.columns > div > div.product.media > div.gallery-placeholder._block-content-loading > img").get_attribute("src")
            except:
                return None

        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""#self.driver.find_element(By.CSS_SELECTOR,"#product-attribute-specs-table > tbody > tr > td").text
        db.dir800 = "Hannas800"
        db.img800 = db.img160     
        db.img800 = db.img160     
        print(db)
        return db
        
        
    def search_item(self,row):
        print("\nSearching for item: " + row+"\n")
        # self.driver.get("https://www.hannashandiworks.com/products/fall.html")
        # self.time.sleep(1)
        # while True:
        #     try:
        #         self.driver.find_element(By.NAME,"q").clear()
        #         self.driver.find_element(By.NAME,"q").send_keys(str(row))
        #         self.driver.find_element(By.NAME,"q").send_keys(self.Keys.ENTER)
        #         self.time.sleep(1)
        #         break
        #     except:
        #         self.driver.get(self.products)
        #         self.time.sleep(10)
        #         continue

        # try:
        self.driver.get(f"https://www.hannashandiworks.com/catalogsearch/result/?q={row}")
        self.time.sleep(self.delay)
        try:
            elems = self.driver.find_elements(By.CSS_SELECTOR, "#layer-product-list > div > div.products.wrapper.grid.columns4.products-grid > ol > li > div > div.product.details.product-item-details > strong > a")
            item = [i.get_attribute("href") for i in elems if i.get_attribute("href")]
            # filter out links we already have
            new_items = [h for h in item if h not in self.links]
            print(new_items)
            return new_items
        except Exception as e:
            print(f"Error searching for item {row}: {e}")
            return []
        

