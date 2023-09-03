from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time,json
from itertools import islice


store = []


class mylist:
    playlist = None
    total = 0
    def __init__(self,list):
        self.playlist = list
        self.total = list[2]

    def __str__(self):
        return str(self.playlist)
        

    def is_qualified(self):
        if float(self.total) > 19 and float(self.total) < 201:
            return True
        return False

    def toJSON(self):
        myDict = {self.playlist[0] : self.playlist[1]}
        js = json.dumps(myDict)
        print js


def get_data():
    rlist = br.find_elements_by_css_selector("#main > div > div")
    for row in rlist:
        try:
            meta = row.find_element_by_css_selector("div.list_meta").text.splitlines()
            total = meta[0].split()[-2]
            link = row.find_element_by_css_selector("div.list_name > strong > a").get_attribute("href")
            # print [link.split("/")[-1].split("?")[0],link,total]
            return [link.split("/")[-1].split("?")[0],link,total]
        except:
            print "List exhausted."
            
def get_playlists():
    pair = []
    

    rlist = br.find_elements_by_css_selector("#main > div > div")
    for row in rlist:
        try:
            meta = row.find_element_by_css_selector("div.list_meta").text.splitlines()
            total = meta[0].split()[-2]
            link = row.find_element_by_css_selector("div.list_name > strong > a").get_attribute("href")
            # print [link.split("/")[-1].split("?")[0],link,total]
            pair.append([link.split("/")[-1].split("?")[0],link,total])
        except:
            print "List exhausted."
        
    try:
        while "disabled" not in br.find_element_by_css_selector("#main > div > div.list-pagination > a.flat-button.next-page").get_attribute("class"):
            br.find_element_by_css_selector("#main > div > div.list-pagination > a.flat-button.next-page").click()
            time.sleep(1)

            rlist = br.find_elements_by_css_selector("#main > div > div")
            for row in rlist:
                try:
                    meta = row.find_element_by_css_selector("div.list_meta").text.splitlines()
                    total = meta[0].split()[-2]
                    link = row.find_element_by_css_selector("div.list_name > strong > a").get_attribute("href")
                    # print [link.split("/")[-1].split("?")[0],link,total]
                    pair.append([link.split("/")[-1].split("?")[0],link,total])
                except:
                    print "List exhausted."
    except:
        print("No pagination")

    return pair




def get_driver():
    path = "./chrome_driver/chromedriver"
    # path = "./firefox_driver/geckodriver"
    br = webdriver.Chrome(executable_path = path)
    # br = webdriver.Firefox(executable_path = path)

    br.wait = WebDriverWait(br,5)

    br.maximize_window()
    return br


br = get_driver()

with open("./csv/infile/imdb.csv",'r') as infile:
    for i,x in islice(enumerate(infile),1):
        print i,x
        br.get(x)
        time.sleep(1)
        

        playlists = get_playlists()
        for list in playlists:
            ml = mylist(list)
            print ml
            if ml.is_qualified():
                store.append(ml)
                print("Success.")
                # print ml
            else:
                print("Not qualified.")
            ml = None


myStore = []
for i in store:
    myStore.append(i.toJSON())

print "\n".join(myStore)