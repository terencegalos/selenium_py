from table_gateway import gateway
import domainobject
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import InvalidElementStateException as ES
from selenium.webdriver.common.action_chains import ActionChains

class beyondborders(domainobject.domainobject):

    vendor = "Beyond Borders"
    url = "http://www.beyondbordersfairtrade.com/"
    home = "https://beyondbordersfairtrade.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get("https://beyondborders.handshake.com/account/login")
        self.time.sleep(1)
        
        print "Logging in."
        # self.driver.find_element_by_css_selector("#home > div.page > div.header > div > div.TopMenu > div > ul > li:nth-child(3) > a").click()
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("#id_username").send_keys(un)
        self.driver.find_element_by_css_selector("#id_password").send_keys(pw)
        self.driver.find_element_by_css_selector("#id_password").send_keys(Keys.ENTER)
        self.time.sleep(10)
        print "Success."

    def get_info(self,item=None):
		db = gateway()
		db.name = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > h3"))).text.encode("utf-8").split()[1]
		db.sku = self.driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > p.price-and-sku > span.sku").text.split()[1]
		db.cat = "|".join([i.text for i in self.driver.find_elements_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > div > a")])
		db.desc = self.driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > p.pre").text.encode("utf-8")
		try:
			db.stock = self.driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > table > tbody > tr:nth-child(1) > td > strong").text.encode("utf-8")
		except:
			db.stock = ""
		db.sale = ""
		db.set = ""
		db.custom = ""
		db.size = ""
		db.seller = ""
		db.min1 = ""
		db.price1 = self.driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-details > p.price-and-sku > span.unit-price > span").text.split("/")[0]
		db.min2 = ""
		db.price2 = ""
		db.min3 = ""
		db.price3 = ""
		db.multi = ""
		db.dir400 = "Beyond400"
		db.dir160 = "Beyond160"
		try:
			db.img400 = self.driver.find_element_by_css_selector("body > div.item-detail-modal-wrapper.in > div > div.modal-body > div.item-details-body-content > div.row-fluid.with-thumbnails > div.span6.product-images > div > a > div.square-wrapper > img").get_attribute("src")
		except:
			db.img400 = self.driver.find_element_by_css_selector("#modal-carousel > div > a.item.toggle-zoom.active > div.square-wrapper > img").get_attribute("src")
		db.img160 = db.img400.split("/")[-1:][0]
		db.desc2 = ""
		db.option = ""
		db.dir800 = "Beyond800"
		db.img800 = db.img160     
		print db
		# self.driver.find_element_by_css_selector("body").click()
		# ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
		# self.driver.find_element_by_css_selector("a.btn.btn-link.close-modal").send_keys(Keys.ESCAPE)
		self.driver.back()
		self.time.sleep(1)
		return db
        
        
    def search_item(self,row):
        
        self.driver.get(self.home)
        self.time.sleep(1)
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
				WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#direct > div.v-top-bar.has-two-navbars > div > nav.brand-nav #buyer-nav-search input.react-autosuggest__input")))
				# ActionChains(self.driver).move_to_element(self.driver.find_element_by_css_selector("#direct > div.v-top-bar.has-two-navbars > div > nav.brand-nav #buyer-nav-search input.react-autosuggest__input")).perform()
				self.driver.find_element_by_css_selector("#direct > div.v-top-bar.has-two-navbars > div > nav.brand-nav #buyer-nav-search input.react-autosuggest__input").clear()
				self.driver.find_element_by_css_selector("#direct > div.v-top-bar.has-two-navbars > div > nav.brand-nav #buyer-nav-search input").send_keys(row.rstrip())
				self.driver.find_element_by_css_selector("#direct > div.v-top-bar.has-two-navbars > div > nav.brand-nav #buyer-nav-search input.react-autosuggest__input").send_keys(Keys.ENTER)
				self.time.sleep(3)
				break
            except:
                self.driver.get(self.home)
                self.time.sleep(3)
                continue

        
        try:
			item = self.driver.find_element_by_css_selector("#taxonomy_catalog > div > div.results > ul > li.span4.quote-line-image > div > a.square-image-wrapper.show-details-modal").click()
			self.time.sleep(1)
        except:
			print "No items found."
        return None


