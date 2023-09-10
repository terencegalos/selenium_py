from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class colorfulgarden(domainobject.domainobject):

    vendor = "Colorful Garden Flags"
    url = "http://www.colorful-garden.com/"
    home = "http://www.colorful-garden.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
       
        # print "Logging in..."
        # self.driver.find_element_by_name('login[username]').send_keys(un)
        # self.driver.find_element_by_name('login[password]').send_keys(pw)
        # self.driver.find_element_by_name('login[password]').send_keys(Keys.ENTER)
        # self.time.sleep(1)
        # print "Login Success."
        # except:
            # print "Login failed."

    def get_info(self,item=None):
        db = gateway()
        try:
			db.name = self.driver.find_element_by_css_selector("#add > div.container > div.secondary > div.product-info > h1").text.encode("utf-8")
        except:
			db.name = ""
        try:
			db.sku = self.driver.find_element_by_css_selector("#product_id").text.encode("utf-8")
        except:
			return None
        db.cat = ""
        try:
			db.desc = self.driver.find_element_by_css_selector("#add > div.container > div.secondary > div.product-info > div.productFeaturesBlock > ul > li > span.feat-name").text.encode("utf-8")
        except:
			db.desc = ""
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = ""
        db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "colorfulgarden400"
        db.dir160 = "colorfulgarden160"
        try:
            db.img400 = self.driver.find_element_by_css_selector("#mediaBlock > div.mobile-images.visible-xs > ul > div > div > li > a").get_attribute("href")
        except:
            print "Image not detected."
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "colorfulgarden800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
		print "\nSearching for item: " + row+"\n"
		while True:
			try:
				search = self.driver.find_element_by_name("keyword")
				self.driver.execute_script('document.querySelector("input[type=search]").setAttribute("value",arguments[0])',row)
				self.driver.execute_script('document.forms[0].submit()')
				self.time.sleep(1)
				break
			except Exception as e:
				print 
				self.driver.refresh()
				self.time.sleep(1)
				continue
		try:
			item = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("#itemsBlock > div > div.row.product-featured.product-listing.category-3dcart-page > div > div > div > div.title > a")]
			return item
		except:
			return  None

