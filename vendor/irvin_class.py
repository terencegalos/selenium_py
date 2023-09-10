from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class irvin(domainobject.domainobject):

    vendor = "Irvin's Tinware"
    url = "https://www.irvinstinware.com/"
    sitemap = "https://www.irvinstinware.com/sitemap"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []
    
        
    def get_all_items(self):
        self.driver.get(self.sitemap)
        self.time.sleep(1)
        self.links.extend([l.get_attribute("href") for l in self.driver.find_elements_by_css_selector("#js-SMAP > main > section:nth-child(3) > div > ul:nth-child(5) > li > a")])

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
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#js-PROD > main > div > div > section > form > ul > li:nth-child(1) > h1 > span:nth-child(3)"))).text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#js-PROD > main > div > div > section > form > ul > li:nth-child(1) > h1").text.encode("utf-8").splitlines()[0].split()[2]
        db.cat = "|".join([i.text.encode("utf-8") for i in self.driver.find_elements_by_css_selector("#js-PROD > nav > ul.o-list-inline.x-collapsing-breadcrumbs__list > li > a > span")])
        db.desc = self.driver.find_element_by_css_selector("#js-PROD > main > div > section > div > div > div").text.encode("utf-8")
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
        db.dir400 = "Irvins400"
        db.dir160 = "Irvins160"
        db.img400 = self.driver.find_element_by_css_selector("#main_image").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Irvins800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        self.driver.find_element_by_css_selector("header > section.o-wrapper.t-site-header__masthead > div > div.o-layout__item.u-width-12.u-width-4--l > form > fieldset > ul > li > input").click()
        self.time.sleep(1)

        self.driver.find_element_by_css_selector("header > section.o-wrapper.t-site-header__masthead > div > div.o-layout__item.u-width-12.u-width-4--l > form > fieldset > ul > li > input").send_keys(str(row))
        self.driver.find_element_by_css_selector("header > section.o-wrapper.t-site-header__masthead > div > div.o-layout__item.u-width-12.u-width-4--l > form > fieldset > ul > li > input").send_keys(Keys.ENTER)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("header > section.o-wrapper.t-site-header__masthead > div > div.o-layout__item.u-width-12.u-width-4--l > form > fieldset > ul > li > input").clear()
		# while True:
		# 	try:
			# 	break
			# except:
			# 	self.driver.get(self.url)
			# 	self.time.sleep(1)
			# 	continue
        try:
			btn = self.driver.find_element_by_css_selector("main > section > div > section.o-layout.u-grids-2.u-grids-3--l.x-product-list > div > a").get_attribute("href")
			self.time.sleep(1)
			print btn
			return [btn]
        except:
			print "Search found nothing."
			return None