from table_gateway import gateway
import domainobject
from selenium.webdriver.common.keys import Keys
from datetime import datetime

class primitivescrowhollow(domainobject.domainobject):

    vendor = "Primitives at Crow Hollow"
    url = "http://www.primitivesatcrowhollow.com/store/Default.asp"
    uname = "service@waresitat.com"
    passw = "wolfville"
    delay = 1
    # lastStop = "http://www.primitivesatcrowhollow.com/store/WsDefault.asp?One=644"
    # covered = "178,185,186,183,182,181,208,179,189,203,176,175,174,172,171,180,195,125,206,205,204,199,198,187,196,188,194,202,201,191,190,168,197,142,170,153,152,151,140,139,158,134,159,132,131,129,128,127,126,137,146,209,167,224,231,150,149,155,147,169,144,143,163,162,161,160,148,253,260,259,258,257,256,207,254,268,252,251,250,249,248,247,255,272,279,280,267,262,269,244,274,217,246,264,263,222,221,223,225,218,226,216,215,214,212,211,210,219,234,135,243,242,240,239,238,265,235,245,233,232,230,229,228,227,236,80,56,55,54,53,52,51,77,49,59,48,47,46,45,44,43,50,65,64,63,62,61,39,136,14,42,20,19,17,16,22,24,23,13,12,11,10,7,9,8,15,41,72,38,37,36,35,34,21,60,40,31,30,29,28,27,26,25,33,109,96,97,98,99,78,101,102,103,104,105,106,95,108,100,114,111,113,115,116,117,118,119,120,122,123,107,94,79,81,154,133,83,84,85,86,87,88,89,90,92,93,285,531,308,300,311,299,350,335,332,284,289,302,283,304,305,306,368,296,297,307,331,294,286,325,287,288,290,291,438,391,301,293,326,295,298,454,282,396,374,424,303,328,292,521,512,533,532,530,528,527,535,529,536,519,518,517,516,515,514,553,524,544,473,551,550,549,548,547,534,545,511,543,542,541,540,539,538,537,546,482,513,490,489,487,486,485,492,483,493,503,640,590,596,595,594,593,643,598,651,636,752,592,552,642,611,618,617,616,614,613,610,597,612,589,609,608,607,605,604,602,601,603,562,591,569,568,567,566,565,571,575,574,573,583,364,355,488,371,370,369,367,504,365,375,363,361,360,359,358,357,394,372,383,474,390,389,388,387,386,373,384,354,382,381,380,379,378,377,376,385,317,356,330,329,327,392,320,334,318,336,316,315,314,313,312,619,310,319,344,353,352,351,349,348,347,333,345,395,343,342,341,340,339,338,337,346,445,436,452,451,450,449,448,455,446,456,444,443,442,441,440,439,393,447,464,600,471,470,469,468,467,453,465,435,463,462,461,460,459,458,457,466,406,437,414,413,411,410,412,416,407,417,405,404,403,402,401,400,399,408,426,434,433,432,431,430,429,415,427,425,423,422,421,420,419,418,428,661,695,664,670,662,671,679,678,677,676,675,674,663,687,620,693,692,691,690,668,688,660,685,684,686,681,683,672,689,627,634,633,632,631,630,673,628,645,626,625,624,623,621,629,652,696,659,658,657,656,655,635,653"
        
    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # print self.covered.split(",")
        
        # print "Logging in."
        # self.driver.find_element_by_name("email1").send_keys(un)
        # self.driver.find_element_by_name("text1").send_keys(pw)
        # self.driver.find_element_by_css_selector(".button166").click()
        # self.time.sleep(1)
        # print "Success."

    def get_info(self,item=None):
        db = gateway()
        try:
            db.name = self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(2) > p:nth-child(1) > font").text.encode("utf-8")
        except:
            return None
        db.sku = self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(2) > p:nth-child(1) > font").text.encode("utf-8")
        db.cat = ""

        db.desc = self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(2) > font:nth-child(4)").text.encode("utf-8")
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = ""
        db.seller = ""
        db.min1 = 1
        try:
            db.price1 = self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(2) > div:nth-child(7) > table > tbody > tr > td > font:nth-child(1) > b").text.split()[-1]
        except:
            return None
            
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "PrimitiveCrow400"
        db.dir160 = "PrimitiveCrow160"
        try:
            db.img400 = "http://www.primitivesatcrowhollow.com/fpdb/images/"+self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(1) > p > a").get_attribute("onclick").split("'")[1]
        except:
            db.img400 = "http://www.primitivesatcrowhollow.com/fpdb/images/"+self.driver.find_element_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(2) > tbody > tr > td > div:nth-child(5) > center > table > tbody > tr:nth-child(1) > td:nth-child(1) > p > a").get_attribute("onclick")
        db.img160 = db.img400.split("/")[-1:][0]
        db.desc2 = ""
        db.option = ""
        db.dir800 = "PrimitiveCrow800"
        db.img800 = db.img160
        print db
        return db
        
    def search_item(self,row):
        
        
        print "\nSearching for item: " + row+"\n"
        # if len(row.split(",")[1].strip()) > 1:
        while True:
            try:
                self.driver.find_element_by_name("qrySearch").clear()
                self.driver.find_element_by_name("qrySearch").send_keys(row)
                self.driver.find_element_by_name("qrySearch").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search fail:"
                print e
                print datetime.now()
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            items = [i.get_attribute("href") for i in self.driver.find_elements_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(1) > tbody > tr > td > table:nth-child(4) > tbody > tr > td > table > tbody > tr:nth-child(1) > td > a")]
            print set(items)
            print len(set(items))
            return list(set(items))
        except:
            return None

    def get_images(self,row):
        
        print "\nSearching for item: " + row+"\n"
        # if len(row.split(",")[1].strip()) > 1:
        while True:
            try:
                self.driver.find_element_by_name("qrySearch").clear()
                self.driver.find_element_by_name("qrySearch").send_keys(row)
                self.driver.find_element_by_name("qrySearch").send_keys(self.Keys.ENTER)
                self.time.sleep(1)
                break
            except Exception as e:
                print "Search fail:"
                print e
                print datetime.now()
                self.driver.refresh()
                self.time.sleep(1)
                continue
        try:
            items = [i for i in self.driver.find_elements_by_css_selector("body > div > center > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > table > tbody > tr > td > p > font > table:nth-child(1) > tbody > tr > td > table:nth-child(4) > tbody > tr > td")]
            return list(set(items))
        except:
            return None
            

