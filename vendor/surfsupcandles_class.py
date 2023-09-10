from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class surfsupcandles(domainobject.domainobject):

    vendor = "Surf's Up Candles"
    url = "https://www.surfsupcandle.com/"
    uname = "terence@waresitat.com"
    passw = "wolfville"
    delay = 1
    all = []
    lastStop = "https://www.surfsupcandle.com/products/limited-edition-mothers-day-island-moon?_pos=1036&_sid=3cd6b491f&_ss=r"
    
        
    def init_login(self,un,pw):
		self.driver.get(self.url)
		self.time.sleep(1)
		# self.driver.find_element_by_css_selector("body > div.ReactModalPortal > div > div > div > div > div.layout__Flex-sc-1mq1rc4-0.layout__Column-sc-1mq1rc4-1.ffhbWg.hjyYkI > p:nth-child(11) > a:nth-child(1)").click()
		# self.time.sleep(1)
		
		print "Logging in."
		# self.driver.find_element_by_name("email").send_keys(un)
		# self.driver.find_element_by_name("email").send_keys(Keys.ENTER)
		# self.time.sleep(1)
		# self.driver.find_element_by_name("password").send_keys(pw)
		# self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
		# self.time.sleep(10)
		print "Success."

    def pagination(self):
        try:
            self.driver.find_element_by_css_selector("#PageContainer > main > div > div > div > div.pagination > span.next > a").click()
            self.time.sleep(1)
            return True
        except:
            print "No pages left."
            return False

    def get_info(self,item=None):
        
        db = gateway()
        # while True:
        #     try:
        #         try:
        #             self.driver.find_element_by_css_selector("#main > div > svg")
        #         except:
        #             self.driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/div/p[2]/span")
        #         self.driver.refresh()
        #         self.time.sleep(5)
        #         continue
        #     except:
        #         break

        db.name = self.driver.find_element_by_css_selector("#PageContainer > main > div > div:nth-child(1) > div > div.grid__item.product-single__meta--wrapper.medium--five-twelfths.large--five-twelfths > div > h1").text.encode("utf-8")
        db.sku = db.name
        db.cat = ""#"|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_xpath("//*[@id='main']/div/div[2]/div[1]/div[1]/ol/li/p")])
        db.desc = self.driver.find_element_by_css_selector("#PageContainer > main > div > div:nth-child(1) > div > div.grid__item.product-single__meta--wrapper.medium--five-twelfths.large--five-twelfths > div > div.product-single__description.rte").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""#self.driver.find_element_by_css_selector("body > div.product.container > div > div.description.col-tablet-7 > ul > li:nth-child(2)").text.encode("utf-8")
        db.seller = ""
        db.min1 = 3#self.driver.find_element_by_css_selector("body > div.product.margin--percent > div > div.flex-row.product-container > div.summary.summary-margin.flex-column.flex--justify-start > div.margin--viewport--small.flex-row.flex--wrap.flex--align-center.flex--justify-start > div.actions > form > div > input").get_attribute("value").encode("utf-8").strip()
        db.price1 = 99#self.driver.find_element_by_css_selector("body > div.product.container > div > div:nth-child(1) > div.summary.col-tablet-7 > div.pricing > div > div.item_price > div > span > span.price").text.encode("utf-8").strip()
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 3
        db.dir400 = "Surfs400"
        db.dir160 = "Surfs160"
        db.img400 = self.driver.find_element_by_css_selector("#ProductPhotoImg").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""#self.driver.find_element_by_css_selector("body > div.product.container > div > div.description > p").text.encode("utf-8")
        db.option = ""
        db.dir800 = "Surfs800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row=None):
        
        print "\nSearching for item: " + str(row)+"\n"
        while True:
            try:
                self.driver.find_element_by_css_selector("#AccessibleNav > li:nth-child(11) > a").click()
                self.time.sleep(1)

                self.driver.find_element_by_name("q").clear()
                self.driver.find_element_by_name("q").send_keys(row)
                self.driver.find_element_by_name("q").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue

        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#PageContainer > main > div > div > div > div.grid-uniform > div > div > div > a")]
        print items
        self.all.extend(items)
        while self.pagination():
            items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#PageContainer > main > div > div > div > div.grid-uniform > div > div > div > a")]
            print items
            self.all.extend(items)
        return self.all

