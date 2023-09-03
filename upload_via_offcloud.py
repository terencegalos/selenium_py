import os,time,sys,shutil
import webdriver_config
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

username = "tamic_888@yahoo.com"
passw = "watashiwaterencedesu"
counter = 0 # track count by limit then download\
holder = [] # holds link until reach the limit


def uploadByCount(infile,limit):
    for url in infile:
        if counter < limit:
            holder.append(url)
            counter = counter + 1
        else:
            batch = " ".join(holder)
            print batch
            time.sleep(1)
            sendBatch(counter,holder,batch)
            
def sendBatch(counter,holder,str):
    br.find_element_by_css_selector("#main > div > div.container-fluid > div > div:nth-child(2) > ul > li:nth-child(1) > form > textarea").clear()
    br.find_element_by_css_selector("#main > div > div.container-fluid > div > div:nth-child(2) > ul > li:nth-child(1) > form > textarea").send_keys(str)
    # upload to ftp
    # br.find_element_by_css_selector("#main > div > div.container-fluid > div > div:nth-child(2) > ul > li:nth-child(1) > form > div > div > div:nth-child(3) > div:nth-child(2) > button:nth-child(1)").click()
    WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > div.container-fluid > div > div:nth-child(2) > ul > li:nth-child(1) > form > div > div > div:nth-child(3) > div:nth-child(2) > button:nth-child(1)"))).click()
    time.sleep(1)
    counter = 0 # reset counter
    holder[:] = [] # reset holder
    
    # wait until batch uploaded
    while True:
        try:
            status = WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > div.container-fluid > div > div:nth-child(2) > ul > li.wrapper.ng-scope > ul > li:nth-child(1) > div.panel > div.panel-footer > div > span.semibold.text-default.ng-scope"))).text
            # status = br.find_element_by_css_selector("#main > div > div.container-fluid > div > div:nth-child(2) > ul > li.wrapper.ng-scope > ul > li:nth-child(1) > div.panel > div.panel-footer > div > span.semibold.text-default.ng-scope").text
            if "Downloading" in status:
                print "Job ongoing detected:"
                print status
                time.sleep(3)
        except:
            print "Fetching next batch."
            break
    
def login(br,uname,passw):
    br.get("http://offcloud.com/") # go to website
    time.sleep(1)
    br.find_element_by_css_selector("#subscribeForm > div > div > div.form-box > p > a").click() #click sign in
    time.sleep(1)
    
    br.find_element_by_css_selector("#login-email").send_keys(uname)
    br.find_element_by_css_selector("#login-pass").send_keys(passw)
    br.find_element_by_css_selector("#login-pass").send_keys(Keys.ENTER)
    time.sleep(1)
    
def goto_remote():
    # br.find_element_by_css_selector("body > aside > div > section > ul > li:nth-child(3) > a").click()
    WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "body > aside > div > section > ul > li:nth-child(3) > a"))).click()
    time.sleep(1)
    
# initialize web driver
br = webdriver_config.init_driver()

login(br,username,passw)

# go to remote page
goto_remote()

# get urls from file    
with open("./csv/infile/pbk.csv") as files:
    print files
    uploadByCount(files,2)