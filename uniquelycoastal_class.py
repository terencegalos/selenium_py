from table_gateway import gateway
import json
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class uniquelycoastal(domainobject.domainobject):

    vendor = "Uniquely Coastal"
    url = "https://uniquelycoastal.com/"
    # home = "https://shopdci.com/Product"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # self.driver.find_element_by_css_selector("#pre-login-navbar > li.signIn-li > a").click()
        # self.time.sleep(1)
        
        # print "Logging in."
        # self.driver.find_element_by_name("LogonEmail").send_keys(un)
        # self.driver.find_element_by_name("LogonPassword").send_keys(pw)
        # self.driver.find_element_by_name("LogonPassword").send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        # db.name = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > h3").text.encode("utf-8")
        db.name = self.driver.find_element_by_css_selector("#ProductSection > div.grid > div.grid-item.large--three-fifths > h1").text.encode("utf-8")
        # text = self.driver.find_element_by_css_selector("head > meta:nth-child(11)").text.replace("Product","|Product")
        # print text
        # js = json.loads(text)
        db.option = "|".join([o.text for o in self.driver.find_elements_by_css_selector("#productSelect-product-template-option-0 > option")])
        try:
            db.sku = "".join(db.name.split("-")[-1]).strip()
        except:
            db.sku = db.option
        #db.sku = self.driver.find_element_by_css_selector("#product-detail-container > div.col-lg-12.col-md-11.col-sm-10 > div:nth-child(3) > div > div > div.col-lg-8.col-sm-10.col-xs-12.product-detail-container-table > div.productDetail-item-pnumber > span:nth-child(2)").text.encode("utf-8")
        try:
            db.cat = ""#self.driver.find_element_by_css_selector("#slick-container4 > div > div > div > div > div > div > div > div").text.encode("utf-8")
        except:
            db.cat = ""
        db.desc = self.driver.find_element_by_css_selector("#ProductSection > div.grid > div.grid-item.large--three-fifths > div.product-description.rte").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("#quantity").get_attribute("value")
        db.price1 = self.driver.find_element_by_css_selector("#productPrice-product-template > span.visually-hidden").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = self.driver.find_element_by_css_selector("#quantity").get_attribute("value")
        db.dir400 = "UC400"
        db.dir160 = "UC160"
        db.img400 = self.driver.find_element_by_css_selector("div > img.zoomImg").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        # db.option = ""
        db.dir800 = "UC800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		self.driver.find_element_by_name("q").clear()
		self.driver.find_element_by_name("q").send_keys(str(row))
		self.driver.find_element_by_name("q").send_keys(self.Keys.ENTER)
		self.time.sleep(2)
		# ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#product-list-container > div:nth-child(5) > div.product-item-container.center-block > div.product-description.row > div.product-item-item.hyperlink-like")).perform()
		# self.time.sleep(1)
		# btn  = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#product-list-container > div:nth-child(5) > div.product-item-container.center-block > div.product-description.row > div.product-item-item.hyperlink-like")))
                # break
            # except:
                # self.driver.get(self.url)
                # self.time.sleep(1)
                # continue
		try:
			return [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("a.product-grid-item")]
		except:
			print "Search found nothing."
			return None

