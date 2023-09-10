from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class delton(domainobject.domainobject):

    vendor = "Delton Products"
    url = "http://delton.cameoez.com/Scripts/PublicSite/?template=Login"
    home = "http://delton.cameoez.com/Scripts/Secure/index.php"
    uname = "waresitat"
    passw = "wolfville"
    delay = 1
    count = 1
    links = []
    
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("username").send_keys(un)
        self.driver.find_element_by_name("password").send_keys(pw)
        self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_all_items(self):
        self.driver.get("https://delton.cameoez.com/Scripts/Secure/index.php?template=Search&userid=2813354&term=")
        self.time.sleep(1)


    def nextPage(self):
        try:
            print "Next page..."
            self.driver.find_element_by_css_selector("#pageNav > tbody > tr > td:nth-child(3) > a").click()
            return True
        except:
            print "Status: No more pages left"
            return False

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-product-info.col-md-4.col-sm-10 > div > h1").text.encode("utf-8")
        except:
            db.name = self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-product-info.col-md-4.col-sm-10 > div > h2").text.encode("utf-8")
        db.sku = ((self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-product-info.col-md-4.col-sm-10 > div > table > tbody > tr:nth-child(1) > td").text.encode("utf-8")).split(":")[1]).strip()
        db.cat = ""#"|".join([c.text for c in self.driver.find_elements_by_css_selector("a.SectionTitleText")])
        db.desc = ""#self.driver.find_element_by_css_selector("#descCell > p.desc").text.encode("utf-8")
        db.stock = ""
        db.sale = ""#self.driver.find_element_by_css_selector("#descCell > p.price").text.splitlines()[0].split()[0] if "regular price" in db.desc.lower() else ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-product-info.col-md-4.col-sm-10 > div > table > tbody > tr > td > input").get_attribute("value")
        db.price1 = self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-product-info.col-md-4.col-sm-10 > div > table > tbody > tr:nth-child(3) > td > span").text.encode("utf-8")
        try:
            db.min2 = self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-product-info.col-md-4.col-sm-10 > div > table > tbody > tr:nth-child(3) > td").text.splitlines()[1].split()[2]
            db.price2 = self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-product-info.col-md-4.col-sm-10 > div > table > tbody > tr:nth-child(3) > td").text.splitlines()[1].split()[-1:][0].strip(")")
        except:
            db.min2 = ""
            db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        try:
            db.multi = db.min1
        except:
            db.multi = db.min1
        db.dir400 = "delton400"
        db.dir160 = "delton160"
        db.img400 = self.driver.find_element_by_css_selector("#main-content > div.container > form > div > div.detail-pop-main-img.col-lg-6.col-md-6.col-sm-10 > img.zoomImg").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "delton800"
        db.img800 = db.img160     
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("term").clear()
                self.driver.find_element_by_name("term").send_keys(str(row))
                self.driver.find_element_by_name("term").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except:
                self.driver.get(self.home)
                self.time.sleep(1)
                continue

        self.links = []
        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#loadCart > div > div > div > div > div > span.details > a")]
        self.links.extend(items)
        print items
        # while self.nextPage():
        #     items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("a.popup.cboxElement")]
        #     self.links.extend(items)
        #     print items

        return self.links

