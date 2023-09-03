from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException
from bs4 import BeautifulSoup
from urllib2 import urlopen
import csv

url = "http://www.oakstreetwholesale.com/"

def makesoup(url):
    html = requests.get(url)
    response = html.content
    soup = BeautifulSoup(response)
    return soup

def init_driver():
    path = "./chrome_drive/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.wait = WebDriverWait(browser,5)
    return browser

#initialize and open browser
br = init_driver()
    
results = []   
with open('./csv/infile/oakstreet search.csv','rb') as infile:
    for i in infile:
        br.get(url)
        br.find_element_by_id('keywords').send_keys(i)
        btn = br.find_element_by_class_name("search-button")
        btn.click
        links = WebDriverWait(br, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "image")))
        for link in links:
            lnk = link.get_attribute("href")
            results.append(lnk)
            print lnk
        
outfile = open("./csv/outfile/oakstreetsearchresult2.csv","wb")
writer = csv.writer(outfile)
writer.writerow(results)