from table_gateway import gateway
from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class jonesrustic(domainobject.domainobject):

    vendor = "Jones' Rustic Signs"
    url = "https://www.jonesrusticsigns.com/customer/account/login/"
    home = "http://www.jonesrusticsigns.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
       
        print "Logging in..."
        self.driver.find_element_by_name('login[username]').send_keys(un)
        self.driver.find_element_by_name('login[password]').send_keys(pw)
        self.driver.find_element_by_name('login[password]').send_keys(Keys.ENTER)
        print "Login Success."
        self.time.sleep(3)
        # except:	
            # print "Login failed."

    def get_info(self,item=None):
		db = gateway()
		try:
			db.name = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-shop.col-md-8.col-sm-8.col-xs-12 > div > div.shop-content-lef > div.product-name > h1").text.encode("utf-8")
		except Exception as e:
			print e
			db.name = ""
		try:
			db.sku = self.driver.find_element_by_css_selector("body > div.wrapper > div > div.main-container.col1-layout.content-color.color > div.container > div > div > div > div.product-view > div.product-wapper-tab.clearfix > div > div > div").text.encode("utf-8").split()[1]
		except:
			db.sku= item
		try:
			db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("body > div.wrapper > div > div.main-container.col1-layout.content-color.color > div.breadcrumbs > div > ul > li")])
		except:
			db.cat = ""
		try:
			db.desc = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-shop.col-md-8.col-sm-8.col-xs-12 > div > div.shop-content-lef > div.short-description > div").text.encode("utf-8")
		except:
			db.desc = ""
		db.stock = ""
		db.sale = ""
		db.set = ""
		db.custom = ""
		db.size = ""
		db.seller = ""
		db.min1 = ""
		try:
			db.price1 = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-shop.col-md-8.col-sm-8.col-xs-12 > div > div.shop-content-right > div.price-box > span span").text.encode("utf-8")
		except:
			db.price1 = self.driver.find_element_by_css_selector("span.price").text.encode("utf-8")
		db.min2 = ""
		db.price2 = ""
		db.min3 = ""
		db.price3 = ""
		db.multi = ""
		db.dir400 = "jonesigns400"
		db.dir160 = "jonesigns160"
		try:
			db.img400 = self.driver.find_element_by_css_selector("#image-0").get_attribute("src")
		except:
			print "Image not detected."
			return
		db.img160 = db.img400.split("/")[-1:][0]
		try:
			db.desc2 = self.driver.find_element_by_css_selector("body > div > div > div.main-container.col2-right-layout > div > div.col-main > div.product-view > div.product-collateral > div > div").text.strip()
		except:
			db.desc2 = ""
		try:
			# self.driver.find_element_by_css_selector("#product-options-wrapper > dl > dd:nth-child(2) > div.input-box input[type=text]")
			self.driver.find_element_by_css_selector("#product-options-wrapper > dl > dd > div.input-box")
			db.option = self.driver.find_element_by_css_selector("#product-options-wrapper > dl > dt").text.encode("utf-8") +"\n"+ "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#product-options-wrapper > dl dd select option")])
		except:
			db.option = ""
		db.dir800 = "jonesigns800"
		db.img800 = db.img160
		print db
		return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("q").clear()
                self.driver.find_element_by_name("q").send_keys(str(row))
                self.driver.find_element_by_name("q").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
				try:
					self.driver.refresh()
					self.time.sleep(1)
					continue
				except:
					alert = self.driver.switch_to_alert()
					alert.accept()
					self.time.sleep(1)

        try:
            item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("h2.product-name a")]
            return item
        except:
            return  None

