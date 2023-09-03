from selenium import webdriver
import time


home = "https://myip.ms/browse/sites/1/url/.com.au/own/376714"
dump = []

last = 291


def get_driver():
    path = "./chrome_driver/chromedriver"
    browser = webdriver.Chrome(executable_path = path)
    browser.maximize_window()
    return browser

def get_info():
    if noBot():
        pass
    else:
        delBot()

    rows = br.find_elements_by_css_selector("#sites_tbl > tbody > tr")
    rowpage = []
    for row in rows:
        rowval = "|".join([r.text for r in row.find_elements_by_css_selector("td")])
        rowpage.append(rowval)

    return rowpage

def get_urls():
    urls = [a.get_attribute("href") for a in br.find_elements_by_css_selector("#sites_tbl > tbody > tr:nth-child(1)") if ".com.au" in a.get_attribute("href")]
    return urls

def noBot():
    try:
        br.find_element_by_css_selector("#captcha_submit")
        return False
    except:
        return True
def delBot():
    br.find_element_by_css_selector("#captcha_submit").click()
    time.sleep(1)

def pagination(br):
    currentPage = int(br.find_element_by_css_selector("a.aqPagingSel:nth-child(1)").text)
    allPage = 291#br.find_element_by_css_selector("")
    next = currentPage+1
    print next
    nextPage = br.find_element_by_css_selector("a[href=#"+str(next)+"]")

    if currentPage != allPage:
        nextPage.click()
        time.sleep(1)
        return True

    return False

#################################################################################


br = get_driver()
br.get(home)
time.sleep(1)
totalurl = br.find_element_by_css_selector("#tabs-1 > table:nth-child(4) > tbody > tr > td > span > span:nth-child(1) > table:nth-child(3) > tbody > tr > td > div.right.nowrap.arial11 > b:nth-child(3)").text

res = get_info()
print res
dump.extend(res)

count = 1
while count <= last:
    br.get("https://myip.ms/browse/sites/"+str(count+1)+"/url/.com.au/own/376714")
    count += 1
    print count
    res = get_info()
    print res
    dump.extend(res)


print dump
print "Done***"