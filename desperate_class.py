from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys

class desperate(domainobject.domainobject):

    vendor = "Desperate Tin Signs"
    url = "http://www.desperate.com/shophome.cfm"
    home = "http://www.desperate.com/shophome.cfm"
    uname = "rick@waresitat.com"
    passw = "wolfville"
    delay = 1
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        inp = raw_input("Done?")
        while True:
            if "y" not in inp:
                continue
            break

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element_by_css_selector("#product-page-with-sidenav > div.product-schema > div.productView.thumbnail-unclicked.qty-box-visible > section > div > h1").text.encode("utf-8")
        db.sku = self.driver.find_element_by_css_selector("#product-page-with-sidenav > div.product-schema > div.productView.thumbnail-unclicked.qty-box-visible > section > div > div > dl > dd").text.encode("utf-8")
        try:
            db.cat = self.driver.find_element_by_css_selector("#product-page-with-sidenav > div.product-schema > div.productView.thumbnail-unclicked.qty-box-visible > section > div > h2 > a > span").text.encode("utf-8")
        except:
            db.cat = "|".join([bread.text.encode("utf-8") for bread in self.driver.find_elements_by_css_selector("#product-page-with-sidenav > div.product-schema > ul > li.breadcrumb > a")])
        try:
            db.desc = self.driver.find_element_by_css_selector("#tab-description > p:nth-child(2)").text.encode("utf-8")
        except:
            db.desc = self.driver.find_element_by_css_selector("#tab-description").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        try:
            db.size = self.driver.find_element_by_css_selector("#tab-description > p:nth-child(2)").text.encode("utf-8").splitlines()[2]
        except:
            db.size = ""#self.driver.find_element_by_css_selector("#tab-description > p:nth-child(2)").text.splitlines()[2]
        db.seller = ""
        db.min1 = 1
        db.price1 = self.driver.find_element_by_css_selector("#product-page-with-sidenav > div.product-schema > div.productView.thumbnail-unclicked.qty-box-visible > section > div > div > div.price-section.price-section--withoutTax.current-price.regular-price > span.price.price--withoutTax").text.encode("utf-8")
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "desperate400"
        db.dir160 = "desperate160"
        try:
            db.img400 = self.driver.find_element_by_css_selector("#product-images-container > div.main-image-container > div.productImageSlider.slider-for.slick-initialized.slick-slider.ready > div > div > div > div > li > figure > img").get_attribute("src")
        except:
            print "Image not detected."
            return
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "desperate800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row):
        
        print "\nSearching for item: " + row+"\n"
        while True:
            try:
                self.driver.find_element_by_name("search_query").clear()
                self.driver.find_element_by_name("search_query").send_keys(str(row))
                self.driver.find_element_by_name("search_query").send_keys(self.Keys.ENTER)
                self.time.sleep(2)
                break
            except:
                self.driver.refresh()
                self.time.sleep(1)
                continue

        try:
        # print self.driver.find_element_by_css_selector("#product-listing-container > form.both-grid-default > ul.productGrid--maxCol4.grid-default > ul > li:nth-child(1) > article > div > h4 > a").get_attribute("innerHTML").encode("utf-8")
            self.driver.find_element_by_tag_name("body").send_keys(Keys.PAGE_DOWN)
            self.time.sleep(1)
            item = self.driver.find_element_by_css_selector("#product-listing-container > form.both-grid-default > ul > ul > li:nth-child(1) > article > div > h4 > a").get_attribute("href")
            print item
            return [item]
        except:
            return  None

