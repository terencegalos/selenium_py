from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class benson(domainobject.domainobject):

    vendor = "Benson_Country_Packaging"
    url = "http://bensonmarketinggroup.com/"
    home = "http://bensonmarketinggroup.com/"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    counter = 1
    last = "https://www.bensonmarketinggroup.com/bags/fabric-bags/polka-dot-organza-bags.html"
    flag = 0
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("#header-account > ul > li.last > a").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("login[username]").send_keys(un)
        self.driver.find_element_by_name("login[password]").send_keys(pw)
        self.driver.find_element_by_name("login[password]").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    #This is used for click options if available then save info
    def clickbtn(self,btn):
	
        opt = []
        optcount = len(btn)
		
        for x in range(optcount):
        
            b_nav = None
            info = None
            b = self.driver.find_elements_by_css_selector("#product-options-wrapper > div > dl")[x]
            b_inner = b.find_element_by_css_selector("dd").get_attribute("innerHTML").lower()
            b_label = b.find_element_by_css_selector("dt").text.encode("utf-8")
            if "type=text" in b_inner or "textarea" in b_inner: # textarea tag
                curr = "text input"
            elif "type=file" in b_inner: #input type=file tag
                curr = "file upload"
            elif "radio-checkbox-text" in b_inner and "$" not in b_inner: #radio button tag
                b_nav = b.find_elements_by_css_selector("dd div.radio-checkbox-text")
            # elif "img" in b_inner:
            #     curr =  b.find_element_by_css_selector("dd a").get_attribute("href")
            elif "<option" in b_inner and "$" in b_inner: #option tag
                b_nav = b.find_elements_by_css_selector("dd select option")
            elif "<ul" in b_inner and "$" in b_inner: # list tag
                b_nav = b.find_elements_by_css_selector("dd ul li")
            else:
                print "Some error occurred. Check again."
                curr = "**error**"
                self.time.sleep(1)

            if b_nav is not None:
                for nav in b_nav:
                    try:
                        nav.click()
                        info = nav.text.encode("utf-8")
                        self.time.sleep(.5)
                        db = self.save_info(b_label+" "+info)
                        nav.click()
                        self.time.sleep(.5)
                        opt.append(db)
                    except:
                        print "Not clickable"
                        continue
        return opt
    
    def get_option(self):
        option = self.driver.find_elements_by_css_selector("#product-options-wrapper > div > dl")
        optlist = []
        for count,opt in enumerate(option):
            curr = ""
            flag = 0
            try:
                label = opt.find_element_by_css_selector("dt").text.encode("utf-8")
            except:
                label = "No label"
            inner = opt.find_element_by_css_selector("dd").get_attribute("innerHTML").lower()
            if "type=text" in inner or "textarea" in inner: # textarea tag
                curr = "text input"
            elif "type=file" in inner: #input type=file tag
                curr = "file upload"
            elif "radio-checkbox-text" in inner and "$" not in inner: #radio button tag
                curr = "|".join([i.text.strip() for i in opt.find_elements_by_css_selector("dd div.radio-checkbox-text")])
            elif "img" in inner:
                curr =  opt.find_element_by_css_selector("dd a").get_attribute("href")
            elif "<option" in inner: #option tag
                curr = "|".join([i.text for i in opt.find_elements_by_css_selector("dd select option")])
            elif "<ul" in inner and "$" not in inner: # list tag
                curr = "|".join([i.text for i in opt.find_elements_by_css_selector("dd ul li")])
            else:
                print "Some error occurred. Check again."
                curr = "**error**"+inner
                self.time.sleep(5)

            print label
            print curr.encode("utf-8")
            curr = ":".join([label,curr.encode("utf-8")])
            optlist.append(curr)
        return ";".join(optlist)

    def get_info(self,item=None):
    
        option = []
        btn = self.driver.find_elements_by_css_selector("#product-options-wrapper > div > dl")
        print "Btn detected."
        db = self.clickbtn(btn)
        option.extend(db) #returns a list of items
        # except Exception as e:
        #     print e
        #     print "No option detected. Direct info get"
        #     res = self.get_option()
        #     db = self.save_info()
        #     option.append(db)
            
        return option
        
    def save_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("#page-columns > div > div.product-view.nested-container > div.product-primary-column.product-shop.grid12-5 > div.product-name > h1").text.encode("utf-8")
        except:
            db.name = self.driver.find_element_by_css_selector("#container > div > div.product-view.custom-product-view > div > div > h1").text.encode("utf-8")
        db.sku = self.counter
        db.cat = "|".join([c.text for c in self.driver.find_elements_by_css_selector("div.breadcrumbs ul li")][:-1])
        try:
            db.desc = self.driver.find_element_by_css_selector("#page-columns > div > div.product-view.nested-container > div.product-primary-column.product-shop.grid12-5 > div.short-description > div").text.encode("utf-8")
        except:
            db.desc = self.driver.find_element_by_css_selector("#product_addtocart_form > div.product-shop > div.short-description > div").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = item
        db.seller = ""
        db.min1 = 1
        try:
            db.price1 = self.driver.find_element_by_css_selector("#page-columns > div > div.product-view.nested-container > div.product-primary-column.product-shop.grid12-5 > div:nth-child(5) > div > div > span > span").text.encode("utf-8")
        except:
            db.price1 = ""
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "Benson400"
        db.dir160 = "Benson160"
        try:
            db.img400 = self.driver.find_element_by_css_selector("#zoom1").get_attribute("href")
        except:
            db.img400 = self.driver.find_element_by_css_selector("#image-zoom").get_attribute("href")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = self.get_option()
        db.dir800 = "Benson800"
        db.img800 = db.img160
        self.counter = self.counter + 1
        print db
        return db
        
        
    def search_item(self,row):
        self.driver.find_element_by_css_selector("body > header > div.upper-header > button.upper-header-item.search-wrapper").click()
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("search_query").clear()
                self.driver.find_element_by_name("search_query").send_keys(str(row))
                self.driver.find_element_by_name("search_query").send_keys(self.Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        try:
            item = self.driver.find_element_by_css_selector("body > main > section.catalog-wrapper.tab-search-results.tab-product-results.tab-selected > main > div > div.product-listing > article:nth-child(1) > div.product-item-info > h3 > a").get_attribute("href")
            print item
            return [item]
        except:
            return None

