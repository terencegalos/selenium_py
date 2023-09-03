from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xml.etree.ElementTree as tree
import requests,xmltodict

class bethany(domainobject.domainobject):

    vendor = "Bethany Lowe"
    url = "http://bethanylowe.com/login"
    search = "https://www.blossombucket.com/shop/"
    all = 'https://bethanylowe.com/?s=""'
    home = "http://bethanylowe.com"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
    links = []

    def init_xml(self):
        print "Extracting xml..."
        xmlfile = requests.get("https://bethanylowe.com/sitemap_index.xml")
        data = xmltodict.parse(xmlfile.content)
        sitemap = ['http://'+sitemap['loc'].strip("//") for sitemap in data['sitemapindex']['sitemap'] if 'product-sitemap' in sitemap['loc']]
        for site in sitemap:
            response = requests.get(site)
            data = xmltodict.parse(response.content)
            url = ["http:"+line['loc'] for line in data['urlset']['url']]
            print url
            self.links.extend(url)

    # xml = tree.parse("./csv/infile/sitemap_index.xml")
    # links = [loc.text for loc in xml.findall('sitemap/loc') if "product-sitemap" in loc.text]
        
    def nextPage(self):
        try:
            self.driver.find_element_by_css_selector("body > div.middle-section > div > div > div > div > div > div.col-sm-9.cart-right-section > ul.pagination-bottom.text-center > li:nth-child(3) > a").click()
            self.time.sleep(1)
            return True
        except:
            print "Page exhausted."
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        
        print "Logging in."
        self.driver.find_element_by_name("log").send_keys(un)
        self.driver.find_element_by_name("pwd").send_keys(pw)
        self.driver.find_element_by_name("pwd").send_keys(Keys.ENTER)
        self.time.sleep(1)
        print "Success."

    def get_info(self,item=None):
        db = gateway()
        # db.name = WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#popupwrapper > table > tbody > tr:nth-child(1) > td > strong"))).text.encode("utf-8")
        try:
            db.name = self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-head > h3").text.encode("utf-8")
        except:
            return
        db.sku = self.driver.find_element_by_css_selector("span.cart-number").text.encode("utf-8").split()[-1:][0]
        db.cat = ""
        db.desc = ""
        db.stock = ""
        try:
            db.sale = self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-head > span:nth-child(6)").text.split()[1].strip("$")
        except:
            db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-content > p").text.encode("utf-8")
        db.seller = ""
        db.min1 = self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-head > span.cart-price").text.split()[-1:][0] if db.sale == "" else self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-head > span:nth-child(6)").text.split()[-1:][0]
        db.price1 = self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-head > span.cart-price").text.split()[0] if db.sale == "" else self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-7.cart-text-area > div.cart-head > span.cart-price").text.split()[-1:][0]
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = db.min1
        db.dir400 = "Bethany400"
        db.dir160 = "Bethany160"
        db.img400 = self.driver.find_element_by_css_selector("body > div.middle-section > div > div > article > div > form > div.col-sm-5 > a > img").get_attribute("src")
        db.img160 = db.img400.split("/")[-1:][0] #if ".jpg?" not in db.img400.split("/")[-1:][0] else (db.img400.split("/")[-1:][0]).split("?")[0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "Bethany800"
        db.img800 = db.img160     
        print db
        self.driver.back()
        return db
        
        
    def search_item(self,row):
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_id("s").clear()
                self.driver.find_element_by_id("s").send_keys(row)
                self.driver.find_element_by_id("s").send_keys(Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search failed:"
                self.driver.get(self.home)
                print e
                self.time.sleep(1)
                continue

        items = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("body > div.middle-section > div > div > div > div > div > div.col-sm-9 > div > div > a")]
        print items
        self.links.extend(items)
        while self.nextPage():
            items = [a.get_attribute("href") for a in self.driver.find_elements_by_css_selector("body > div.middle-section > div > div > div > div > div > div.col-sm-9 > div > div > a")]
            print items
            self.links.extend(items)
            
        return self.links