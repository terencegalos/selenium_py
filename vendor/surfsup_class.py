from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class surfsup(domainobject.domainobject):

    vendor = "Surf's Up Candles"
    url = "https://surfsupcandle.faire.com"
    uname = "terence@waresitat.com"
    passw = "wolfville"
    delay = 1
    all = []
    
        
    def init_login(self,un,pw):
		self.driver.get("https://surfsupcandle.faire.com/user/sign-up?signIn=1")
		self.time.sleep(10)
		self.driver.find_element_by_css_selector("body > div.ReactModalPortal > div > div > div > div > div.layout__Flex-sc-1mq1rc4-0.layout__Column-sc-1mq1rc4-1.ffhbWg.hjyYkI > p:nth-child(11) > a:nth-child(1)").click()
		self.time.sleep(1)
		
		print "Logging in."
		self.driver.find_element_by_name("email").send_keys(un)
		self.driver.find_element_by_name("email").send_keys(Keys.ENTER)
		self.time.sleep(1)
		self.driver.find_element_by_name("password").send_keys(pw)
		self.driver.find_element_by_name("password").send_keys(Keys.ENTER)
		self.time.sleep(10)
		print "Success."

    def pagination(self):
        try:
            for x in range(5):
                self.driver.find_element_by_css_selector("html body").send_keys(Keys.PAGE_DOWN)
            self.time.sleep(1)
            # self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # self.time.sleep(1)
            # try:
            ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath("//*[@id='main']/div/div[1]/div[1]/div/div[7]/div[2]/div[2]/div[3]")).perform()
            self.time.sleep(2)
            # self.driver.get(self.driver.find_element_by_xpath("//*[@id='main']/div/div[1]/div[1]/div/div[7]/div[2]/div[2]/div[3]/a").get_attribute("href"))
            self.driver.find_element_by_css_selector("#main > div > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.Brand__BrandPageUpperPart-wvrzkz-0.btdUtK.kUGzUv > div.styled__MakerContainer-sc-17ihvht-0.bEbgNX > div > div.styled__BrandProductsContainer-sc-17ihvht-2.fYXeht > div.layout__Flex-sc-1mq1rc4-0.layout__Column-sc-1mq1rc4-1.BrandProducts__PaginationWrapper-sc-56cg4r-4.ikuGmT.hjyYkI.byOjsg > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.styles__Wrapper-sc-1t6b1ty-1.styles__DesktopWrapper-sc-1t6b1ty-2.hUdWNf.gdWMrX.bVOWHP > div:nth-child(3) > a").click()
            self.time.sleep(8)

            return True
        except:
            print "No pages left."
            return False

    def get_info(self,item=None):
        
        db = gateway()
        while True:
            try:
                try:
                    self.driver.find_element_by_css_selector("#main > div > svg")
                except:
                    self.driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div/div/p[2]/span")
                self.driver.refresh()
                self.time.sleep(5)
                continue
            except:
                break

        try:
            db.name = self.driver.find_element_by_xpath("//*[@id='main']/div/div[2]/div[2]/div[3]/div[1]/h1").text
        except:
            db.name = self.driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div/h3").text
        db.sku = db.name
        db.cat = "|".join([c.text.encode("utf-8") for c in self.driver.find_elements_by_xpath("//*[@id='main']/div/div[2]/div[1]/div[1]/ol/li/p")])
        db.desc = ""#self.driver.find_element_by_css_selector("p[itemprop='description']").text.encode("utf-8")
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
        try:
            db.img400 = self.driver.find_element_by_xpath("//*[@id='main']/div/div[2]/div[2]/div[2]/div[1]/div/picture/img").get_attribute("src").encode("utf-8")
        except:
            db.img400 = self.driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/img").get_attribute("src").encode("utf-8")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""#self.driver.find_element_by_css_selector("body > div.product.container > div > div.description > p").text.encode("utf-8")
        try:
            self.driver.find_element_by_xpath("//*[@id='main']/div/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div/div").click()
            self.time.sleep(1)
            db.option = "|".join([o.text for o in self.driver.find_elements_by_xpath("//*[@id='main']/div/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[2]/button")])
        except:
            db.option = ""
        db.dir800 = "Surfs800"
        db.img800 = db.img160
        print db
        return db
        
        
    def search_item(self,row=None):
        
        print "\nSearching for item: " + str(row)+"\n"
        for x in range(6):
            self.driver.find_element_by_css_selector("html body").send_keys(Keys.PAGE_DOWN)
        self.time.sleep(1)
        ActionChains(self.driver).move_to_element(self.driver.find_element_by_xpath("//*[@id='main']/div/div[1]/div[1]/div/div[7]/div[2]/div[2]/div[3]")).perform()
        self.time.sleep(2)
        # items = [i.get_attribute("href") for i in self.driver.find_elements_by_xpath("//*[@id='main']/div/div[1]/div[1]/div/div[7]/div[1]/div[2]/section/a")]
        # items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#main > div > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.Brand__BrandPageUpperPart-wvrzkz-0.btdUtK.kUGzUv > div.styled__MakerContainer-sc-17ihvht-0.bEbgNX > div > div.styled__BrandProductsContainer-sc-17ihvht-2.fYXeht > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.btdUtK > div:nth-child(2) > section > a")]
        items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("a[data-test-id=productTile]")]
        self.driver.execute_script("window.scrollTo(0,0);")
        print items
        self.all.extend(items)
        while self.pagination():
            # items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#main > div > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.Brand__BrandPageUpperPart-wvrzkz-0.btdUtK.kUGzUv > div.styled__MakerContainer-sc-17ihvht-0.bEbgNX > div > div.styled__BrandProductsContainer-sc-17ihvht-2.fYXeht > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.btdUtK > div:nth-child(2) > section > a")]
            # items = [i.get_attribute("href") for i in self.driver.find_elements_by_xpath("//*[@id='main']/div/div[1]/div[1]/div/div[7]/div[1]/div[2]/section/a")]
            # items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("#main > div > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.Brand__BrandPageUpperPart-wvrzkz-0.btdUtK.kUGzUv > div.styled__MakerContainer-sc-17ihvht-0.bEbgNX > div > div.styled__BrandProductsContainer-sc-17ihvht-2.fYXeht > div.layout__Flex-sc-1mq1rc4-0.layout__Row-sc-1mq1rc4-2.btdUtK > div:nth-child(2) > section > a")]
            items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("a[data-test-id=productTile]")]
            self.driver.execute_script("window.scrollTo(0,0);")
            print items
            self.all.extend(items)
        return self.all

