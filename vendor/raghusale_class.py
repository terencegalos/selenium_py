from table_gateway import gateway
import domainobject

class raghusale(domainobject.domainobject):

    vendor = "Home Collections by Raghu Closeouts"
    url = "http://www.hcbyraghu.com/"
    uname = "service@waresitat.com"
    passw = "wolfville"
    login = "https://www.hcbyraghu.com/index.php?main_page=login"
    delay = 1
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        self.driver.find_element_by_css_selector("#logoWrapper div:nth-child(2) table tbody tr:nth-child(2) td:nth-child(1) a:nth-child(3)").click()
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_css_selector("#login-email-address").send_keys(un)
        self.driver.find_element_by_id("login-password").send_keys(pw)
        self.driver.find_element_by_css_selector("#loginForm div.buttonRow.forward input[type=\"image\"]").click()
        self.time.sleep(1)
        self.driver.get(self.url)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#productName").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#productDetailsList li").text.split()[1]
        db.cat = self.driver.find_element_by_css_selector("#productListHeading a").text.encode("utf-8")
        db.desc = self.driver.find_element_by_css_selector("#productDescription").text.encode("utf-8")
        db.stock = ""
        try:
            db.sale = self.driver.find_element_by_css_selector("#productPrices > span.productSpecialPrice").text.encode("utf-8")
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("#cartAdd > input[type=\"text\"]:nth-child(1)").get_attribute("value")
        db.price1 = self.driver.find_element_by_css_selector("#productPrices").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = ""
        db.dir400 = "Raghu400"
        db.dir160 = "Raghu160"
        db.img400 = self.driver.find_element_by_css_selector("#productMainImage a img").get_attribute("src")
        if "no_image" in db.img400:
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Raghu800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        self.driver.find_element_by_id("searchboxinput").clear()
        self.driver.find_element_by_id("searchboxinput").send_keys(str(row))
        self.driver.find_element_by_id("searchboxinput").send_keys(self.Keys.ENTER)
        self.time.sleep(1)

        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#productListing > div > div.itemTitle > a")]
        return items

